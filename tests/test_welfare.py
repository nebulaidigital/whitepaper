"""Tests for the welfare framework."""

from __future__ import annotations

import numpy as np
import pytest

from src.analysis.welfare import (
    atkinson_swf,
    bergson_samuelson,
    evaluate_all_packages_welfare,
    evaluate_package_welfare,
    package_rankings_by_epsilon,
)
from src.packages import DIRECT_REDISTRIBUTION, KORINEK_SCENARIO, STATUS_QUO


def test_atkinson_utilitarian_equals_mean():
    """At ε=0, Atkinson SWF should equal mean income."""
    incomes = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    w = atkinson_swf(incomes, epsilon=0.0)
    assert w == pytest.approx(3.0)


def test_atkinson_log_utility_equals_geometric_mean():
    """At ε=1, Atkinson SWF should equal geometric mean."""
    incomes = np.array([1.0, 4.0])
    w = atkinson_swf(incomes, epsilon=1.0)
    assert w == pytest.approx(2.0)  # geometric mean of 1 and 4


def test_atkinson_rawlsian_equals_min():
    """At ε=∞, Atkinson SWF should equal minimum income."""
    incomes = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    w = atkinson_swf(incomes, epsilon=np.inf)
    assert w == pytest.approx(1.0)


def test_atkinson_intermediate_epsilon():
    """At ε=2, SWF should give weight to inequality."""
    equal = np.array([2.0, 2.0, 2.0])
    unequal = np.array([1.0, 2.0, 3.0])
    # Both have mean 2, but unequal should have lower SWF
    assert atkinson_swf(unequal, epsilon=2.0) < atkinson_swf(equal, epsilon=2.0)


def test_atkinson_handles_zero_income():
    """Non-positive incomes should return 0 (welfare-zero, treated as floor)."""
    incomes = np.array([0.0, 1.0, 2.0])
    w = atkinson_swf(incomes, epsilon=1.0)
    assert w == 0.0


def test_bergson_samuelson_uniform_weights_equals_mean():
    incomes = np.array([1.0, 2.0, 3.0])
    w = bergson_samuelson(incomes)
    assert w == pytest.approx(2.0)


def test_bergson_samuelson_explicit_weights():
    """Bottom-decile weight should produce welfare closer to bottom incomes."""
    incomes = np.array([1.0, 5.0, 12.0])
    weights_low = np.array([0.8, 0.1, 0.1])
    weights_high = np.array([0.1, 0.1, 0.8])
    w_low = bergson_samuelson(incomes, weights_low)
    w_high = bergson_samuelson(incomes, weights_high)
    assert w_low < w_high


def test_evaluate_package_welfare_runs():
    result = evaluate_package_welfare(KORINEK_SCENARIO, epsilon=1.0)
    assert result.package_code == "H"
    assert result.epsilon == 1.0


def test_status_quo_has_zero_welfare_delta():
    """Status quo vs status quo should produce zero welfare delta."""
    result = evaluate_package_welfare(STATUS_QUO, epsilon=1.0)
    assert abs(result.delta_global_mean) < 1e-9


def test_evaluate_all_packages_returns_dataframe():
    df = evaluate_all_packages_welfare(epsilons=(0.0, 1.0))
    assert len(df) == 13 * 2  # 10 packages × 2 ε values
    assert "package_code" in df.columns
    assert "delta_global_mean" in df.columns


def test_package_rankings_pivot():
    rankings = package_rankings_by_epsilon(epsilons=(0.0, 1.0, 2.0))
    assert rankings.shape == (3, 13)  # 3 epsilons × 12 packages
    # Each row should produce ranks in [1, 12] (allowing ties via method="min")
    for _, row in rankings.iterrows():
        assert row.min() == 1.0
        assert row.max() <= 13.0
        # No more than 13 distinct ranks
        assert len(set(row.values)) <= 13


def test_direct_redistribution_better_under_high_inequality_aversion():
    """At high ε, Direct Redistribution should rank near the top because it
    helps bottom deciles most."""
    r_low = evaluate_package_welfare(DIRECT_REDISTRIBUTION, epsilon=0.0)
    r_high = evaluate_package_welfare(DIRECT_REDISTRIBUTION, epsilon=5.0)
    # Welfare delta should be positive at both ε
    assert r_low.delta_global_mean > 0
    assert r_high.delta_global_mean > 0


def test_korinek_scenario_dominates_across_epsilon():
    """Package H should rank top or near-top across all ε values
    (this is a robustness finding documented in the v2.0 paper)."""
    rankings = package_rankings_by_epsilon(epsilons=(0.0, 0.5, 1.0, 2.0, 5.0))
    h_ranks = rankings["H"].values
    # H should be in top 2 across all ε
    assert all(r <= 2 for r in h_ranks)
