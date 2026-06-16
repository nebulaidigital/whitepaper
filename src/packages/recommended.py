"""Package R: The Recommended Architecture.

Operationalizes Part VI's eight-pillar recommendation (A1–A8) as a
runnable PolicyPackage so it can be tested directly rather than
inferred from Package H.

The eight pillars synthesize:
- Package H's scenario-adaptive intensity structure
- Package C's CERN-AI public lab + compute governance
- Package E's UBC + AI tax distributional mechanisms
- Package G's antitrust structural separation
- Pillar 4 (reskilling) from the original framework

Validation: if Package R doesn't dominate the alternatives on welfare,
the Part VI recommendations need revision. This package exists to
make that test possible.

References:
    Korinek (2024) NBER WP 32549 (scenario taxonomy)
    Hausenloy-Miotti-Dennis (2023) (MAGIC consortium)
    Khan (2017), Hovenkamp (2021) (antitrust)
    Atkinson (2015) (Universal Basic Capital)
    OECD Pillar 1/2 (international coordination)
"""

from src.packages.base import (
    LeverTarget,
    PolicyLever,
    PolicyPackage,
    Reversibility,
)


PILLAR_A1_SCENARIO_AI_TAX = PolicyLever(
    name="A1 Scenario-Adaptive AI Tax (3-8% OECD-coordinated)",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "AI sector value-added tax scaling 3% (Slow Growth) → 8% "
        "(Transformative AI). OECD-coordinated to prevent base erosion. "
        "Revenue allocation: 60% UBI/UBC, 30% CERN-AI, 10% AISI. "
        "Synthesizes original Pillar 6 + Package C/G calibration."
    ),
    parameter_changes={
        # Specified at midpoint Faster Growth intensity
        "ai_sector_tax_rate": 0.05,
        "transfer_funding_per_gdp": 0.010,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.40,
    citation="EMPIRICAL_ANALOGS.md §3.5; OECD Pillar 1/2 framework",
)


PILLAR_A2_DIRECT_REDISTRIBUTION = PolicyLever(
    name="A2 Scenario-Adaptive Direct Redistribution (UBC + scenario-UBI)",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "UBC ($50K at age 18) baseline. UBI activates at Faster "
        "Acceleration ($600/mo) → Transformative ($1,500/mo). "
        "Synthesizes Package E mechanisms with scenario gating. "
        "Funded from Pillar A1 revenue."
    ),
    parameter_changes={
        # Midpoint Faster Growth intensity: UBC + partial UBI
        "ubc_grant_per_capita": 50000.0,
        "ubi_monthly_per_adult": 600.0,
        "transfer_funding_per_gdp": 0.040,
        "labor_supply_elasticity": -0.04,  # v2.0 OpenResearch
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation="EMPIRICAL_ANALOGS.md §1.2 + §2.1 + §7.6; Atkinson 2015",
)


PILLAR_A3_SCENARIO_SOVEREIGN_EQUITY = PolicyLever(
    name="A3 Scenario-Adaptive Sovereign Equity (5-35% acquisition)",
    target=LeverTarget.CAPITAL,
    description=(
        "Public fund acquisition fraction scales with realized AI capital "
        "concentration: 5% Slow Growth → 15% Faster Growth → 25% Faster "
        "Acceleration → 35% Transformative AI. Calibrated to Q1 2026 "
        "state-affiliated capital baseline (Stargate-scale)."
    ),
    parameter_changes={
        # Midpoint Faster Growth intensity: 15%
        "sovereign_acquisition_fraction": 0.15,
        "cost_of_equity_premium": 0.005,
        "dividend_rate": 0.04,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation="EMPIRICAL_ANALOGS.md §1.1; Norway GPFG + 2026 state-capital baseline",
)


PILLAR_A4_CERN_AI_LAB = PolicyLever(
    name="A4 CERN-AI Public Frontier Lab ($30B/yr, 12-country consortium)",
    target=LeverTarget.COMPETITION,
    description=(
        "Multilateral public lab producing open-weights frontier capability. "
        "Activates above Faster Growth threshold; scales to full capacity "
        "under Faster Acceleration. Solves the open-weights inversion at "
        "the source. Replaces original Pillar 5 mandate approach."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.45,  # midpoint between full and zero
        "frontier_capability_diffusion": 0.15,
        "ai_sector_concentration_shift": -0.10,
        "public_funding_per_gdp": 0.0015,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.30,
    citation="EMPIRICAL_ANALOGS.md §4.1; Hausenloy et al. 2023",
)


PILLAR_A5_RESKILLING_ENTITLEMENT = PolicyLever(
    name="A5 Reskilling Entitlement (scaling with displacement velocity)",
    target=LeverTarget.LABOR,
    description=(
        "Standard ALMP scope under Slow Growth → universal lifelong-learning "
        "entitlement under Transformative AI. v2.0 calibration (Brookings "
        "Hamilton 2024) for central estimate."
    ),
    parameter_changes={
        "epsilon_sub_shift": 1.5,
        "skill_mix_complement_shift": 0.05,
        "reskilling_earnings_effect": 0.08,  # v2.0 central
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="EMPIRICAL_ANALOGS.md §7.5 (v2.0); Card-Kluve-Weber 2018 + Brookings 2024",
)


PILLAR_A6_COMPUTE_GOVERNANCE_TREATY = PolicyLever(
    name="A6 Compute Governance Treaty (verifiable, NPT-style)",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Treaty-grade compute monitoring + capability thresholds. Activates "
        "above Faster Growth threshold; capability thresholds tighten with "
        "realized productivity. Mutual pause authority for above-threshold "
        "systems."
    ),
    parameter_changes={
        "ai_arms_race_intensity": -0.25,
        "geopolitical_stability_index": 7.0,
        "frontier_compute_concentration": -0.10,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.50,
    citation="EMPIRICAL_ANALOGS.md §4.2; Sastry-Heim-Belfield 2024",
)


PILLAR_A7_CAPABILITY_DISCLOSURE = PolicyLever(
    name="A7 Mandatory Capability Disclosure + Pre-Deployment Eval",
    target=LeverTarget.GOVERNANCE,
    description=(
        "AISI Network mandatory tier. Above-threshold training runs "
        "register with AISI International; pre-deployment evals required. "
        "Builds on Bletchley → Seoul → Paris precedent."
    ),
    parameter_changes={
        "capability_disclosure_compliance": 0.85,
        "ai_safety_audit_coverage": 0.80,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.40,
    citation="EMPIRICAL_ANALOGS.md §4.3; Bengio et al. 2025",
)


PILLAR_A8_STRUCTURAL_SEPARATION = PolicyLever(
    name="A8 Antitrust Structural Separation",
    target=LeverTarget.COMPETITION,
    description=(
        "Sherman Act § 2 + DMA-style obligations. Model labs ≠ cloud "
        "providers ≠ application-layer firms. Domestic enforcement, no "
        "international coordination required."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.45,
        "ai_sector_concentration_shift": -0.20,
        "compute_layer_profit_share_cap": 0.15,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation="EMPIRICAL_ANALOGS.md §3.4; Khan 2017, Hovenkamp 2021",
)


# Note: code "R" is the explicit Recommended package, distinct from the
# eight A-H packages already specified. The base class validates A-H + R.
RECOMMENDED = PolicyPackage(
    code="R",
    name="Recommended Architecture (Part VI v0.3)",
    description=(
        "Operationalizes the Part VI eight-pillar recommendation (A1–A8) "
        "at midpoint Faster Growth intensity. Synthesizes Package H's "
        "scenario-adaptive structure with Package C's CERN-AI + compute "
        "governance, Package E's UBC distributional mechanism, Package G's "
        "antitrust structural separation, and the original Pillar 4 "
        "reskilling at v2.0 calibration. This is the explicit recommendation "
        "being made; it must be testable, not just inferred from Package H."
    ),
    levers=(
        PILLAR_A1_SCENARIO_AI_TAX,
        PILLAR_A2_DIRECT_REDISTRIBUTION,
        PILLAR_A3_SCENARIO_SOVEREIGN_EQUITY,
        PILLAR_A4_CERN_AI_LAB,
        PILLAR_A5_RESKILLING_ENTITLEMENT,
        PILLAR_A6_COMPUTE_GOVERNANCE_TREATY,
        PILLAR_A7_CAPABILITY_DISCLOSURE,
        PILLAR_A8_STRUCTURAL_SEPARATION,
    ),
    activation_year=2026,
    sequencing="sequential",  # Reversibility-weighted phased rollout
)
