"""Tests for the four stability stress tests.

Per PREREGISTRATION.md §5 Hypothesis 10 and Hypothesis 4.
"""

from __future__ import annotations

import numpy as np
import pytest

from src.packages import (
    CERN_AI,
    DIRECT_REDISTRIBUTION,
    GAME_THEORETIC,
    NEBULAI_SIX,
    STATUS_QUO,
)
from src.stability import (
    CoalitionTest,
    CrossClassTest,
    DefectionTest,
    TimeConsistencyTest,
)


# ---------------------------------------------------------------------------
# Defection
# ---------------------------------------------------------------------------


def test_defection_returns_one_result_per_coord_lever():
    test = DefectionTest(NEBULAI_SIX)
    results = test.run()
    # Nebulai Six has 2 coordination-dependent levers
    assert len(results) == len(NEBULAI_SIX.coordination_dependent_levers())


def test_defection_no_coord_levers_no_results():
    test = DefectionTest(STATUS_QUO)
    results = test.run()
    # Status quo has no levers, hence no coordination-dependent ones
    assert len(results) == 0


def test_defection_summary_well_formed():
    test = DefectionTest(CERN_AI)
    results = test.run()
    summary = test.summary(results)
    assert summary["package_code"] == "C"
    assert summary["n_defections_tested"] == len(results)
    assert 0.0 <= summary["fraction_fragile"] <= 1.0
    assert summary["mean_welfare_loss_from_defection"] >= 0.0


# ---------------------------------------------------------------------------
# Coalition
# ---------------------------------------------------------------------------


def test_coalition_threshold_array_shape():
    test = CoalitionTest(CERN_AI)
    result = test.run(n_steps=8)
    assert len(result.coalition_thresholds) == 8
    assert len(result.welfare_deltas) == 8


def test_coalition_specified_threshold_matches_package():
    """The 'specified' threshold equals max coalition_threshold across
    coordination-dependent levers."""
    test = CoalitionTest(CERN_AI)
    expected = max(
        lev.coalition_threshold
        for lev in CERN_AI.coordination_dependent_levers()
    )
    assert test.specified_threshold() == expected


def test_coalition_status_quo_zero_threshold():
    """Status quo has no coordination requirements."""
    test = CoalitionTest(STATUS_QUO)
    assert test.specified_threshold() == 0.0


# ---------------------------------------------------------------------------
# Time consistency
# ---------------------------------------------------------------------------


def test_time_consistency_runs():
    test = TimeConsistencyTest(NEBULAI_SIX, n_draws=20)
    result = test.run()
    assert result.n_draws == 20
    assert result.package_code == "B"
    # Loss from political risk should be non-negative
    # (random reversal can only reduce or maintain welfare)
    assert result.welfare_loss_from_political_risk >= -1e-6


def test_time_consistency_seeds_reproducible():
    a = TimeConsistencyTest(CERN_AI, n_draws=20, seed=42).run()
    b = TimeConsistencyTest(CERN_AI, n_draws=20, seed=42).run()
    assert (
        a.expected_welfare_under_stochastic_reversal
        == b.expected_welfare_under_stochastic_reversal
    )


def test_time_consistency_most_vulnerable_lever_identified():
    test = TimeConsistencyTest(GAME_THEORETIC, n_draws=30)
    result = test.run()
    assert result.most_vulnerable_lever != "<none>"


# ---------------------------------------------------------------------------
# Cross-class
# ---------------------------------------------------------------------------


def test_cross_class_matrix_shape():
    test = CrossClassTest(NEBULAI_SIX)
    result = test.run()
    assert result.welfare_delta_matrix.shape == (10, 2)


def test_cross_class_counts_consistent():
    test = CrossClassTest(NEBULAI_SIX)
    result = test.run()
    # 20 total cells (10 deciles x 2 countries)
    total = result.n_cells_positive + result.n_cells_negative
    # Allow for some cells to be exactly zero
    assert total <= 20


def test_direct_redistribution_pareto_improves():
    """Direct Redistribution should make every decile better off
    in both countries (it's pure transfers)."""
    test = CrossClassTest(DIRECT_REDISTRIBUTION)
    result = test.run()
    assert result.n_cells_negative == 0
    assert not result.fails_hypothesis_4
    # Most disadvantaged cell should still have positive delta
    assert result.most_disadvantaged_delta > 0


def test_status_quo_cross_class_all_zero():
    """Status quo against itself: all deltas should be zero."""
    test = CrossClassTest(STATUS_QUO)
    result = test.run()
    assert np.allclose(result.welfare_delta_matrix, 0.0, atol=1e-9)
