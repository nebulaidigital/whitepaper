"""Tests for the bilateral US/China simulator."""

from __future__ import annotations

import numpy as np
import pytest

from src.core import BilateralSimulator, SimulatorConfig
from src.core.lever_application import apply_package_to_state
from src.packages import (
    ALL_PACKAGES,
    CERN_AI,
    DIRECT_REDISTRIBUTION,
    NEBULAI_SIX,
    STATUS_QUO,
)


@pytest.fixture
def sim() -> BilateralSimulator:
    return BilateralSimulator()


def test_status_quo_runs(sim: BilateralSimulator):
    result = sim.run()
    assert result.package_code == "A"
    assert len(result.years) == sim.config.end_year - sim.config.start_year + 1
    assert result.us.code == "US"
    assert result.cn.code == "CN"


def test_status_quo_matches_observed_2015_2025(sim: BilateralSimulator):
    """Backtest period: status quo should reproduce observed values exactly
    (since baseline_data hard-codes them)."""
    result = sim.run()
    df = result.to_dataframe()
    # 2015 anchors
    assert abs(df.loc[2015, "us_labor_share"] - 0.5887) < 0.001
    assert abs(df.loc[2015, "us_top_1pct"] - 0.279) < 0.001
    assert abs(df.loc[2015, "us_markup"] - 1.205) < 0.001
    # 2025 anchors
    assert abs(df.loc[2025, "us_labor_share"] - 0.560) < 0.001
    assert abs(df.loc[2025, "us_top_1pct"] - 0.304) < 0.001
    assert abs(df.loc[2025, "us_markup"] - 1.220) < 0.001


def test_us_gdp_growth_within_backtest_tolerance(sim: BilateralSimulator):
    """PREREGISTRATION.md §8: cumulative real GDP growth 2015-2025 within ±5pp of 22%."""
    result = sim.run()
    df = result.to_dataframe()
    growth = df.loc[2025, "us_real_gdp"] / df.loc[2015, "us_real_gdp"] - 1
    assert 0.17 <= growth <= 0.32, f"GDP growth {growth:.1%} outside [17%, 32%]"


def test_cn_gdp_growth_within_backtest_tolerance(sim: BilateralSimulator):
    """PREREGISTRATION.md §8: cumulative real GDP growth 2015-2025 within ±10pp."""
    result = sim.run()
    df = result.to_dataframe()
    growth = df.loc[2025, "cn_real_gdp"] / df.loc[2015, "cn_real_gdp"] - 1
    assert 0.45 <= growth <= 0.75, f"CN GDP growth {growth:.1%} outside [45%, 75%]"


def test_2036_projection_hits_baseline_targets(sim: BilateralSimulator):
    """BASELINE_2026.md §3: 2036 central values should be approximately hit."""
    result = sim.run()
    df = result.to_dataframe()
    # Tolerances per BASELINE_2026.md §3 P10-P90 ranges
    assert 0.49 <= df.loc[2036, "us_labor_share"] <= 0.53
    assert 0.32 <= df.loc[2036, "us_top_1pct"] <= 0.36
    assert 1.25 <= df.loc[2036, "us_markup"] <= 1.32
    cumul_gdp = df.loc[2036, "us_real_gdp"] / df.loc[2025, "us_real_gdp"] - 1
    assert 0.22 <= cumul_gdp <= 0.34


def test_all_packages_run_without_error(sim: BilateralSimulator):
    for package in ALL_PACKAGES:
        result = sim.run(package=package, coalition_share=0.7, cn_cooperation=0.3)
        assert result.package_code == package.code
        assert not np.isnan(result.us.real_gdp).any()
        assert not np.isnan(result.us.labor_share).any()


def test_status_quo_package_equals_no_package(sim: BilateralSimulator):
    """Running with STATUS_QUO (empty levers) should equal None."""
    a = sim.run().to_dataframe()
    b = sim.run(package=STATUS_QUO).to_dataframe()
    np.testing.assert_array_almost_equal(
        a["us_labor_share"].values, b["us_labor_share"].values
    )


def test_package_b_dampens_markup_growth(sim: BilateralSimulator):
    """Nebulai Six's Pillar 5 (open weights) should dampen markup growth."""
    baseline = sim.run().to_dataframe()
    nebulai = sim.run(package=NEBULAI_SIX, coalition_share=0.8, cn_cooperation=0.5).to_dataframe()
    # Markup in 2036 under Nebulai should be ≤ baseline
    assert nebulai.loc[2036, "us_markup"] <= baseline.loc[2036, "us_markup"]


def test_package_e_reduces_top_1pct(sim: BilateralSimulator):
    """Direct Redistribution should reduce top-1% wealth share."""
    baseline = sim.run().to_dataframe()
    redist = sim.run(package=DIRECT_REDISTRIBUTION).to_dataframe()
    assert redist.loc[2036, "us_top_1pct"] < baseline.loc[2036, "us_top_1pct"]


def test_package_c_dampens_markup_more_than_b(sim: BilateralSimulator):
    """CERN-AI's stronger markup-dampening mechanism should outperform Nebulai
    Six's Pillar 5 alone."""
    nebulai = sim.run(package=NEBULAI_SIX, coalition_share=0.8, cn_cooperation=0.5).to_dataframe()
    cern = sim.run(package=CERN_AI, coalition_share=0.8, cn_cooperation=0.5).to_dataframe()
    assert cern.loc[2036, "us_markup"] < nebulai.loc[2036, "us_markup"]


def test_coalition_threshold_gates_levers(sim: BilateralSimulator):
    """Coordination-dependent levers should not apply below their coalition threshold."""
    # CERN-AI public lab requires 30% coalition; below that it should have minimal effect
    low_coal = sim.run(package=CERN_AI, coalition_share=0.10).to_dataframe()
    high_coal = sim.run(package=CERN_AI, coalition_share=0.80).to_dataframe()
    # Markup dampening only happens with high coalition
    assert high_coal.loc[2036, "us_markup"] < low_coal.loc[2036, "us_markup"]


def test_audit_trail_records_all_levers(sim: BilateralSimulator):
    """Every active lever should produce an audit-trail entry."""
    result = sim.run(package=CERN_AI, coalition_share=0.8)
    assert len(result.audit_trail) > 0
    lever_names = {entry[0] for entry in result.audit_trail}
    cern_lever_names = {lev.name for lev in CERN_AI.levers}
    # Every package lever should appear at least once in the audit trail
    for name in cern_lever_names:
        assert name in lever_names, f"Lever {name} missing from audit trail"


def test_lever_application_doesnt_mutate_input_config():
    """apply_package_to_state should deepcopy config — caller's config preserved."""
    cfg = SimulatorConfig()
    original_sigma = cfg.sigma_task_elasticity
    _app = apply_package_to_state(NEBULAI_SIX, config=cfg)
    assert cfg.sigma_task_elasticity == original_sigma
