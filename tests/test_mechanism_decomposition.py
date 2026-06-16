"""Tests for the mechanism decomposition module."""

from __future__ import annotations

import pytest

from src.analysis.mechanism_decomposition import (
    CHANNELS,
    MechanismContribution,
    ai_specific_share,
    decompose_labor_share_decline,
    decompose_top_1pct_rise,
    report_decomposition,
)


def test_channels_documented():
    """Each channel must have at least one parameter override."""
    assert len(CHANNELS) >= 4
    for channel_name, overrides in CHANNELS.items():
        assert len(overrides) >= 1
        for attr in overrides:
            assert isinstance(attr, str)


def test_decompose_labor_share_runs():
    contributions = decompose_labor_share_decline()
    assert len(contributions) == len(CHANNELS)
    for c in contributions:
        assert isinstance(c, MechanismContribution)
        assert c.indicator == "us_labor_share"


def test_contributions_sum_to_unity():
    contributions = decompose_labor_share_decline()
    total_share = sum(c.contribution_share for c in contributions)
    # Should sum to 1.0 (100%) by normalization
    assert total_share == pytest.approx(1.0, abs=1e-6)


def test_decompose_top_1pct_runs():
    contributions = decompose_top_1pct_rise()
    assert len(contributions) == len(CHANNELS)
    for c in contributions:
        assert c.indicator == "us_top_1pct"


def test_automation_is_dominant_channel_for_labor_share():
    """Automation should be the dominant channel for labor-share decline in
    the current reduced-form simulator (where automation directly drives
    labor-share decay rate)."""
    contributions = decompose_labor_share_decline()
    automation = [c for c in contributions if c.channel == "automation"][0]
    assert abs(automation.contribution_share) >= 0.5


def test_ai_specific_share_is_reasonable():
    """AI-specific share of labor-share decline should be a reasonable
    fraction (between 30% and 90%) — not 0% (would mean simulator
    doesn't attribute change to AI) or 100% (would imply implausibly
    monocausal attribution)."""
    contributions = decompose_labor_share_decline()
    share = ai_specific_share(contributions)
    assert 0.30 < share < 0.90


def test_report_decomposition_string():
    contributions = decompose_labor_share_decline()
    report = report_decomposition(contributions)
    assert "Mechanism decomposition" in report
    assert "automation" in report


def test_mechanism_contribution_to_dict():
    contributions = decompose_labor_share_decline()
    c = contributions[0]
    d = c.to_dict()
    assert "channel" in d
    assert "isolated_change" in d
    assert "contribution_share" in d
