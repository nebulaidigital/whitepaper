"""2015-2025 backtest validation gate per PREREGISTRATION.md §8.

These tests must pass for any simulation result to be reportable. The model
must explain past observed data before producing forward-looking policy
recommendations.

Tolerances per PREREGISTRATION.md §8:
    US labor share              ±2pp
    US top 1% wealth share      ±2pp
    US mean markup              ±0.05
    US real GDP cumul (2015-25) ±5pp
    CN labor share              ±3pp
    CN mean markup              ±0.05
    CN real GDP cumul (2015-25) ±10pp
"""

from __future__ import annotations

import pytest

from src.analysis.baseline_data import (
    cumulative_growth,
    load_cn_baseline,
    load_us_baseline,
)
from src.core import BilateralSimulator


@pytest.fixture(scope="module")
def baseline_run():
    sim = BilateralSimulator()
    return sim.run().to_dataframe()


def test_us_labor_share_2025(baseline_run):
    actual = load_us_baseline().labor_share[2025]
    sim_value = baseline_run.loc[2025, "us_labor_share"]
    assert abs(sim_value - actual) <= 0.02, (
        f"US labor share 2025: sim={sim_value:.4f}, actual={actual:.4f}, |Δ|={abs(sim_value-actual):.4f}"
    )


def test_us_top_1pct_wealth_2025(baseline_run):
    actual = load_us_baseline().top_1pct_wealth_share[2025]
    sim_value = baseline_run.loc[2025, "us_top_1pct"]
    assert abs(sim_value - actual) <= 0.02


def test_us_mean_markup_2025(baseline_run):
    actual = load_us_baseline().mean_markup_sw[2025]
    sim_value = baseline_run.loc[2025, "us_markup"]
    assert abs(sim_value - actual) <= 0.05


def test_us_real_gdp_growth_2015_2025(baseline_run):
    actual = cumulative_growth(load_us_baseline().real_gdp_b, 2015, 2025)
    sim_value = baseline_run.loc[2025, "us_real_gdp"] / baseline_run.loc[2015, "us_real_gdp"] - 1
    assert abs(sim_value - actual) <= 0.05, (
        f"US real GDP cumul 2015-2025: sim={sim_value:.1%}, actual={actual:.1%}"
    )


def test_cn_labor_share_2025(baseline_run):
    actual = load_cn_baseline().labor_share[2025]
    sim_value = baseline_run.loc[2025, "cn_labor_share"]
    assert abs(sim_value - actual) <= 0.03


def test_cn_mean_markup_2025(baseline_run):
    actual = load_cn_baseline().mean_markup_sw[2025]
    sim_value = baseline_run.loc[2025, "cn_markup"]
    assert abs(sim_value - actual) <= 0.05


def test_cn_real_gdp_growth_2015_2025(baseline_run):
    actual = cumulative_growth(load_cn_baseline().real_gdp_b, 2015, 2025)
    sim_value = baseline_run.loc[2025, "cn_real_gdp"] / baseline_run.loc[2015, "cn_real_gdp"] - 1
    assert abs(sim_value - actual) <= 0.10, (
        f"CN real GDP cumul 2015-2025: sim={sim_value:.1%}, actual={actual:.1%}"
    )


def test_baseline_substitute_employment_decline(baseline_run):
    """Substitute-worker employment should fall over backtest period
    (per Eloundou et al. 2023 + Webb 2020)."""
    early = baseline_run.loc[2015, "us_sub_emp_idx"]
    late = baseline_run.loc[2025, "us_sub_emp_idx"]
    assert late < early, f"Sub employment did not decline: {early} -> {late}"


def test_2036_baseline_within_documented_band(baseline_run):
    """BASELINE_2026.md §3 P10-P90 ranges for 2036 status quo."""
    df = baseline_run
    # Labor share P10-P90: 49-53%
    assert 0.49 <= df.loc[2036, "us_labor_share"] <= 0.53
    # Top 1% P10-P90: 32-36%
    assert 0.32 <= df.loc[2036, "us_top_1pct"] <= 0.36
    # Markup P10-P90: 1.25-1.32
    assert 1.25 <= df.loc[2036, "us_markup"] <= 1.32
