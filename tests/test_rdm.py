"""Tests for the RDM wrapper."""

from __future__ import annotations

import pandas as pd
import pytest

from src.analysis.rdm import (
    OUTCOME_METRICS,
    UNCERTAINTY_RANGES,
    _sample_uncertainties,
    policy_regret,
    run_rdm_for_all_packages,
    run_rdm_for_package,
)


def test_lhs_sampling_dimensions():
    samples = _sample_uncertainties(n=100)
    assert len(samples) == 100
    assert set(samples.columns) == set(UNCERTAINTY_RANGES.keys())
    for col, (lo, hi) in UNCERTAINTY_RANGES.items():
        assert samples[col].min() >= lo
        assert samples[col].max() <= hi


def test_lhs_seed_reproducibility():
    a = _sample_uncertainties(n=50, seed=42)
    b = _sample_uncertainties(n=50, seed=42)
    pd.testing.assert_frame_equal(a, b)


def test_run_rdm_for_single_package():
    res = run_rdm_for_package("A", n_scenarios=10)
    assert len(res.experiments) == 10
    assert len(res.outcomes) == 10
    for metric in OUTCOME_METRICS:
        assert metric in res.outcomes.columns


def test_run_rdm_all_packages_smoke():
    res = run_rdm_for_all_packages(n_scenarios=20)
    # 20 scenarios x 9 packages = 180 rows (Package R added v0.3 for validation)
    assert len(res.experiments) == 180
    assert len(res.outcomes) == 180
    # Every package code should appear
    assert set(res.experiments["package"].unique()) == {"A", "B", "C", "D", "E", "F", "G", "H", "R"}


def test_policy_regret_well_formed():
    res = run_rdm_for_all_packages(n_scenarios=30)
    regret = policy_regret(res, "us_top_1pct_wealth_2036", higher_is_better=False)
    assert "mean_regret" in regret.columns
    assert "max_regret" in regret.columns
    assert "fraction_best" in regret.columns
    # All packages should be in the regret table
    assert len(regret) == 9  # Nine packages compared (Package R added v0.3)
    # mean_regret >= 0 always
    assert (regret["mean_regret"] >= 0).all()
    # fraction_best should sum to ≥ 1 across packages — every scenario has at
    # least one winner, and ties cause multiple packages to share "best"
    assert regret["fraction_best"].sum() >= 1.0 - 1e-6


def test_status_quo_regret_on_gdp():
    """Status quo (Package A) should NOT win on GDP under most parameter draws —
    Package F (Build-Different-AI) has labor-augmenting productivity boost."""
    res = run_rdm_for_all_packages(n_scenarios=50)
    regret = policy_regret(res, "us_real_gdp_growth", higher_is_better=True)
    assert regret.loc["F", "fraction_best"] >= regret.loc["A", "fraction_best"]
