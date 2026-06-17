"""Tests for scenario configurations and cross-scenario comparison."""

from __future__ import annotations

import pandas as pd
import pytest

from src.analysis.scenario_comparison import (
    cross_scenario_table,
    package_robustness,
    scenario_winners,
)
from src.core import BilateralSimulator
from src.scenarios import (
    ALL_SCENARIOS,
    COMPLEMENT_DOMINANT_CONFIG,
    NEW_TASKS_DOMINANT_CONFIG,
    SUBSTITUTE_DOMINANT_CONFIG,
)


def test_three_scenarios_defined():
    assert len(ALL_SCENARIOS) == 3
    assert "substitute" in ALL_SCENARIOS
    assert "complement" in ALL_SCENARIOS
    assert "new_tasks" in ALL_SCENARIOS


def test_substitute_has_faster_labor_share_decay():
    """Substitute-dominant should have faster labor-share decline."""
    assert SUBSTITUTE_DOMINANT_CONFIG.us_labor_share_decay_rate > 0.010


def test_complement_has_slower_labor_share_decay():
    """Complement-dominant should have slower labor-share decline."""
    assert COMPLEMENT_DOMINANT_CONFIG.us_labor_share_decay_rate < 0.005


def test_new_tasks_has_highest_productivity():
    """New-tasks-dominant (GPT scenario) should have highest AI productivity."""
    assert NEW_TASKS_DOMINANT_CONFIG.ai_productivity_growth > 0.040


def test_scenarios_produce_different_baselines():
    """Each scenario should produce a different 2036 labor share."""
    results = {}
    for name, config in ALL_SCENARIOS.items():
        df = BilateralSimulator(config=config).run().to_dataframe()
        results[name] = df.loc[2036, "us_labor_share"]
    # All three should be distinct
    assert len(set(round(v, 4) for v in results.values())) == 3


def test_cross_scenario_table_shape():
    """Should have 3 scenarios × 10 packages = 30 rows (v0.5 added Nebulai v2)."""
    df = cross_scenario_table()
    assert len(df) == 36
    assert set(df["scenario"].unique()) == {"substitute", "complement", "new_tasks"}
    assert len(df["package_code"].unique()) == 12


def test_package_robustness_returns_aggregated():
    df = cross_scenario_table()
    robust = package_robustness(df)
    assert len(robust) == 12
    # Higher mean delta = more welfare-improving on average
    assert "delta_median_income_mean" in robust.columns
    assert "delta_median_income_std" in robust.columns


def test_scenario_winners_runs():
    df = cross_scenario_table()
    winners = scenario_winners(df)
    assert len(winners) == 3
    # Status quo (A) should not win on any positive delta
    for _, row in winners.iterrows():
        assert row["winning_package"] != "A"


def test_substitute_dominant_status_quo_has_lower_labor_share():
    """The substitute-dominant scenario's status-quo trajectory should
    show worse labor share at 2036 than the complement-dominant
    scenario's status quo."""
    sub_df = BilateralSimulator(config=SUBSTITUTE_DOMINANT_CONFIG).run().to_dataframe()
    comp_df = BilateralSimulator(config=COMPLEMENT_DOMINANT_CONFIG).run().to_dataframe()
    assert sub_df.loc[2036, "us_labor_share"] < comp_df.loc[2036, "us_labor_share"]


def test_substitute_dominant_status_quo_has_higher_top_1pct():
    """Substitute-dominant should produce higher wealth concentration than
    complement-dominant under status quo."""
    sub_df = BilateralSimulator(config=SUBSTITUTE_DOMINANT_CONFIG).run().to_dataframe()
    comp_df = BilateralSimulator(config=COMPLEMENT_DOMINANT_CONFIG).run().to_dataframe()
    assert sub_df.loc[2036, "us_top_1pct"] > comp_df.loc[2036, "us_top_1pct"]
