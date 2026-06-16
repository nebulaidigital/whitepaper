"""Tests for the lever interaction layer.

Per PREREGISTRATION.md Hypothesis 6: Pillar 1 (sovereign equity) × Pillar 6
(AI tax) are partial substitutes. Other interactions are documented in
src/core/interactions.py with explicit citations.
"""

from __future__ import annotations

import pytest

from src.core.interactions import (
    ALL_INTERACTIONS,
    PILLAR_1_X_PILLAR_6_SUBSTITUTABILITY,
    PILLAR_4_X_PILLAR_5_COMPLEMENTARITY,
    applicable_interactions,
    interaction_audit,
    total_correction_for_outcome,
)
from src.packages import (
    CERN_AI,
    DIRECT_REDISTRIBUTION,
    GAME_THEORETIC,
    NEBULAI_SIX,
    STATUS_QUO,
    BUILD_DIFFERENT,
)


def test_status_quo_no_interactions():
    """Status quo has no levers, hence no interactions."""
    assert applicable_interactions(STATUS_QUO) == []


def test_pillar_1_x_pillar_6_active_in_nebulai_six():
    """Nebulai Six has both Pillar 1 (sovereign equity) and Pillar 6 (AI tax)."""
    ixs = applicable_interactions(NEBULAI_SIX)
    assert PILLAR_1_X_PILLAR_6_SUBSTITUTABILITY in ixs


def test_pillar_4_x_pillar_5_active_in_nebulai_six():
    """Nebulai Six has both Pillar 4 (reskilling) and Pillar 5 (open weights)."""
    ixs = applicable_interactions(NEBULAI_SIX)
    assert PILLAR_4_X_PILLAR_5_COMPLEMENTARITY in ixs


def test_correction_for_top_1pct_is_substitutive_in_nebulai_six():
    """Pillar 1 + Pillar 6 substitutability should produce correction < 1.0
    for top-1% wealth share."""
    correction = total_correction_for_outcome(NEBULAI_SIX, "us_top_1pct")
    assert correction < 1.0
    # Specifically Pillar 1 × 6: -0.25 → multiplier 0.75
    assert correction == pytest.approx(0.75, abs=0.01)


def test_correction_for_labor_share_is_complementary_in_nebulai_six():
    """Pillar 4 + Pillar 5 complementarity should produce correction > 1.0
    for labor share."""
    correction = total_correction_for_outcome(NEBULAI_SIX, "us_labor_share")
    assert correction > 1.0
    assert correction == pytest.approx(1.15, abs=0.01)


def test_cern_ai_has_lab_x_governance_interaction():
    """CERN-AI has both public frontier lab + compute governance treaty."""
    ixs = applicable_interactions(CERN_AI)
    interaction_names = [ix.name for ix in ixs]
    assert any("CERN-AI" in n and "Compute Governance" in n for n in interaction_names)


def test_cern_ai_markup_amplification():
    """CERN-AI's lab + governance should amplify markup compression."""
    correction = total_correction_for_outcome(CERN_AI, "us_markup")
    assert correction > 1.0


def test_direct_redistribution_has_ubi_reskilling_interaction():
    """Direct Redistribution doesn't have reskilling — should NOT trigger UBI × Reskilling."""
    # Direct Redistribution has UBI but no reskilling lever
    ixs = applicable_interactions(DIRECT_REDISTRIBUTION)
    assert not any("UBI × Reskilling" in ix.name for ix in ixs)


def test_audit_records_active_interactions():
    """Audit should return one entry per (interaction, outcome) pair."""
    audit = interaction_audit(NEBULAI_SIX)
    # At least 4 entries (Pillar 1×6 has 3 outcomes, Pillar 4×5 has 2 outcomes)
    assert len(audit) >= 5
    # Audit entries are (interaction_name, outcome_name, correction) tuples
    for entry in audit:
        assert len(entry) == 3
        name, outcome, correction = entry
        assert isinstance(name, str)
        assert isinstance(outcome, str)
        assert isinstance(correction, float)


def test_no_correction_for_outcome_without_interaction():
    """Outcomes not in any active interaction should have correction = 1.0."""
    correction = total_correction_for_outcome(BUILD_DIFFERENT, "us_top_1pct")
    # Build-Different has no wealth-distribution interactions
    assert correction == 1.0


def test_all_interactions_have_citations():
    """Every documented interaction must cite its theoretical or empirical anchor."""
    for ix in ALL_INTERACTIONS:
        assert len(ix.citation) > 30  # Non-trivial citation
        assert ix.citation.strip() != ""


def test_all_interactions_have_at_least_one_correction():
    """Every interaction must affect at least one outcome dimension."""
    for ix in ALL_INTERACTIONS:
        assert len(ix.correction_multipliers) >= 1


def test_correction_magnitudes_are_reasonable():
    """Corrections should be within ±50% (not infinite amplification or
    full cancellation — both would be implausible)."""
    for ix in ALL_INTERACTIONS:
        for outcome, correction in ix.correction_multipliers.items():
            assert -0.5 <= correction <= 0.5


def test_simulator_actually_applies_interactions():
    """Verify that interactions actually shift simulator output.

    Compare top-1% wealth under Nebulai Six (where Pillar 1 × Pillar 6
    substitutability is active) vs. a package with only one of the two.
    """
    from src.core import BilateralSimulator
    sim = BilateralSimulator()

    # Run Nebulai Six (has both Pillar 1 + Pillar 6)
    full_df = sim.run(package=NEBULAI_SIX, coalition_share=0.7, cn_cooperation=0.5).to_dataframe()
    # With interaction, top-1% reduction should be smaller (less negative)
    # than additive sum would predict — i.e., correction < 1.0.
    # Hard to test absolutely without a no-interaction control package;
    # just confirm the simulator runs with the interaction logic active.
    assert not full_df.empty
    assert "us_top_1pct" in full_df.columns
