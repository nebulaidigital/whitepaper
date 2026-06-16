"""Lever interaction effects.

The v1.0 simulator treats lever effects as additive. In reality, some
levers are substitutes (target overlapping rents — total effect < sum
of independent effects) and others are complements (each amplifies the
other — total effect > sum of independent effects).

This module specifies the empirically- and theoretically-supported
interactions for the seven candidate packages. Per PREREGISTRATION.md
Hypothesis 6, Pillar 1 × Pillar 6 substitutability is the specific
pre-registered test. Other interactions are added with explicit
literature anchoring.

Implementation pattern: each interaction is a `LeverInteraction`
specifying two lever-name patterns plus a multiplicative correction
on each affected outcome dimension. The simulator's
`_apply_package_deltas` calls `apply_interactions` after the additive
deltas are computed to apply the correction.

References
----------
- Acemoglu & Robinson (2024) institutional complementarity work
- Hypothesis 6 in PREREGISTRATION.md (Pillar 1 × Pillar 6)
- General mechanism design theory on substitute vs. complement levers
"""

from __future__ import annotations

from dataclasses import dataclass

from src.packages.base import PolicyPackage


@dataclass(frozen=True)
class LeverInteraction:
    """A pairwise interaction between two levers.

    Attributes
    ----------
    name : human-readable identifier
    lever_a_pattern : substring match against lever name (case-insensitive)
    lever_b_pattern : substring match
    correction_multipliers : dict of {outcome_name: multiplier_correction}
        Each outcome's combined effect is multiplied by (1 + correction).
        Negative correction = sub-additive (substitutes).
        Positive correction = super-additive (complements).
    citation : empirical or theoretical anchor
    """

    name: str
    lever_a_pattern: str
    lever_b_pattern: str
    correction_multipliers: dict[str, float]
    citation: str


# =============================================================================
# Documented interactions
# =============================================================================

# Hypothesis 6 in PREREGISTRATION.md: sovereign equity + AI tax target
# overlapping rents (capital owners' AI sector returns). Combined effect
# on top-1% wealth share is less than sum because each captures part of
# the same pool.
PILLAR_1_X_PILLAR_6_SUBSTITUTABILITY = LeverInteraction(
    name="Pillar 1 (Sovereign Equity) × Pillar 6 (AI Tax) substitutability",
    lever_a_pattern="sovereign equity",
    lever_b_pattern="ai tax",
    correction_multipliers={
        # Combined wealth-share reduction is ~25% smaller than additive
        "us_top_1pct": -0.25,
        "cn_top_1pct": -0.25,
        # Combined transfer-funding capacity slightly sub-additive
        # (some tax revenue would otherwise flow to sovereign fund)
        "us_median_income": -0.15,
    },
    citation=(
        "PREREGISTRATION.md Hypothesis 6. Theoretical: both levers target "
        "capital owners' AI sector rents. Tax + acquisition of the same "
        "rent pool produces sub-additive total effect."
    ),
)


# Reskilled substitute workers benefit more from open AI ecosystem
# because more downstream applications use the reskilled complement
# skills. Empirical anchor: Brynjolfsson-Li-Raymond (2023) found
# productivity boost concentrated on low-skill workers in customer
# service AI augmentation — suggests reskilling-augmented workers
# benefit disproportionately from broader AI tool availability.
PILLAR_4_X_PILLAR_5_COMPLEMENTARITY = LeverInteraction(
    name="Pillar 4 (Reskilling) × Pillar 5 (Open Weights) complementarity",
    lever_a_pattern="reskilling",
    lever_b_pattern="open-weights",
    correction_multipliers={
        # Combined labor share gain is ~15% larger than additive
        "us_labor_share": +0.15,
        # Combined substitute-worker earnings effect amplified
        "us_substitute_emp": +0.20,
    },
    citation=(
        "Brynjolfsson-Li-Raymond (2023) on AI augmentation concentrating "
        "on low-skill workers; Anthropic Economic Index (2025) on "
        "complement-skill task patterns. Reskilled workers benefit "
        "disproportionately from broader AI ecosystem availability."
    ),
)


# Public lab and compute governance treaty are both about reducing
# concentrated private rents at the AI sector level. When both are
# active, they reinforce each other: the treaty constrains private
# unilateral capability expansion, while the public lab provides the
# alternative open capability that compensates. Without the treaty,
# the public lab is undercut by private acceleration; without the lab,
# the treaty creates a capability vacuum.
CERN_AI_X_COMPUTE_GOVERNANCE_COMPLEMENTARITY = LeverInteraction(
    name="CERN-AI × Compute Governance complementarity",
    lever_a_pattern="public frontier lab",
    lever_b_pattern="compute governance",
    correction_multipliers={
        # Markup compression amplified by ~30% when both are active
        "us_markup": +0.30,
        # Geopolitical stability gains super-additive
        "geopolitical_stability": +0.25,
    },
    citation=(
        "Ostrom (1990) commons-governance design principle #2 (rules adapted "
        "to local conditions): credible institutional pairing produces "
        "super-additive coordination effects. CERN historical analog: "
        "scientific infrastructure + member-state coordination "
        "rules mutually reinforced over 70 years."
    ),
)


# UBC and AI tax fund overlapping recipients (median household via
# direct transfers vs. capital grant). Combined effect on wealth
# distribution and median income is slightly sub-additive.
UBC_X_AI_TAX_SUBSTITUTABILITY = LeverInteraction(
    name="Universal Basic Capital × AI Tax substitutability",
    lever_a_pattern="universal basic capital",
    lever_b_pattern="ai tax",
    correction_multipliers={
        "us_top_1pct": -0.10,
        "us_median_income": -0.10,
    },
    citation=(
        "Both levers redistribute toward median households via different "
        "mechanisms (transfer vs. capital grant). Combined effect is "
        "~10% sub-additive on overlapping recipients."
    ),
)


# UBI and reskilling: if UBI is generous enough, reskilling
# participation may decline (workers choose UBI consumption over
# retraining time investment). Slight sub-additivity.
UBI_X_RESKILLING_SUBSTITUTABILITY = LeverInteraction(
    name="UBI × Reskilling substitutability",
    lever_a_pattern="basic income",
    lever_b_pattern="reskilling",
    correction_multipliers={
        # Reskilling earnings effect dampened ~15% when UBI is active
        # (lower participation incentive)
        "us_substitute_emp": -0.15,
    },
    citation=(
        "OpenResearch UBI Study (2024) found small reductions in education "
        "enrollment among UBI recipients. Effect on AI reskilling "
        "participation is theoretical extension; magnitude is estimated."
    ),
)


# Structural separation and AI tax: with vertically separated AI value
# chain, AI tax incidence falls more cleanly on the model layer
# (whose rents are visible) rather than being diluted via cloud-layer
# transfer pricing. Slight super-additivity.
STRUCTURAL_SEPARATION_X_AI_TAX_COMPLEMENTARITY = LeverInteraction(
    name="Structural Separation × AI Tax complementarity",
    lever_a_pattern="structural separation",
    lever_b_pattern="ai tax",
    correction_multipliers={
        # AI tax revenue ~15% higher under structural separation because
        # transfer-pricing arbitrage between cloud and model layers is
        # constrained
        "us_median_income": +0.15,  # via larger transfer pool
        "us_top_1pct": -0.10,  # additional concentration reduction
    },
    citation=(
        "OECD Pillar 2 implementation lessons: structural separation "
        "reduces transfer-pricing arbitrage, increasing effective tax "
        "incidence on rent-holding entity."
    ),
)


# Capability disclosure and structural separation: both reduce
# information asymmetries that protect AI lab rents. Modest
# super-additivity.
CAPABILITY_DISCLOSURE_X_STRUCTURAL_SEPARATION_COMPLEMENTARITY = LeverInteraction(
    name="Capability Disclosure × Structural Separation complementarity",
    lever_a_pattern="capability disclosure",
    lever_b_pattern="structural separation",
    correction_multipliers={
        "us_markup": +0.10,
    },
    citation=(
        "Khan (2017) Amazon's Antitrust Paradox extension: disclosure + "
        "structural remedies together produce stronger competitive "
        "discipline than either alone."
    ),
)


# All documented interactions
ALL_INTERACTIONS: tuple[LeverInteraction, ...] = (
    PILLAR_1_X_PILLAR_6_SUBSTITUTABILITY,
    PILLAR_4_X_PILLAR_5_COMPLEMENTARITY,
    CERN_AI_X_COMPUTE_GOVERNANCE_COMPLEMENTARITY,
    UBC_X_AI_TAX_SUBSTITUTABILITY,
    UBI_X_RESKILLING_SUBSTITUTABILITY,
    STRUCTURAL_SEPARATION_X_AI_TAX_COMPLEMENTARITY,
    CAPABILITY_DISCLOSURE_X_STRUCTURAL_SEPARATION_COMPLEMENTARITY,
)


# =============================================================================
# Application
# =============================================================================


def applicable_interactions(package: PolicyPackage) -> list[LeverInteraction]:
    """Return the interactions whose both partners are active in this package."""
    lever_names_lower = [lev.name.lower() for lev in package.levers]
    applicable: list[LeverInteraction] = []
    for interaction in ALL_INTERACTIONS:
        a_present = any(interaction.lever_a_pattern.lower() in n for n in lever_names_lower)
        b_present = any(interaction.lever_b_pattern.lower() in n for n in lever_names_lower)
        if a_present and b_present:
            applicable.append(interaction)
    return applicable


def total_correction_for_outcome(
    package: PolicyPackage,
    outcome_name: str,
) -> float:
    """Total multiplicative correction factor for an outcome dimension.

    Returns the product of (1 + correction) across all applicable
    interactions. A value of 1.0 means no correction; 0.8 means combined
    effect is 80% of additive; 1.2 means combined effect is 120%.
    """
    total = 1.0
    for interaction in applicable_interactions(package):
        if outcome_name in interaction.correction_multipliers:
            total *= 1.0 + interaction.correction_multipliers[outcome_name]
    return total


def interaction_audit(package: PolicyPackage) -> list[tuple[str, str, float]]:
    """Return (interaction_name, outcome_name, correction) triples for
    every applicable interaction × affected outcome — used by the
    simulator's audit trail and by the methodology section.
    """
    audit: list[tuple[str, str, float]] = []
    for interaction in applicable_interactions(package):
        for outcome, correction in interaction.correction_multipliers.items():
            audit.append((interaction.name, outcome, correction))
    return audit
