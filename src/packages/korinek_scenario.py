"""Package H: Korinek-Scenario-Conditional.

Korinek (2024) "Scenarios for the Transition to AGI" NBER WP 32549 lays
out four transition scenarios with distinct macroeconomic dynamics:

    Scenario 1: Slow Growth (continued automation; ~0.5-1.0%/yr TFP boost)
    Scenario 2: Faster Growth (substantial productivity gains; ~1.5-2.5%/yr)
    Scenario 3: Faster Acceleration (transformative productivity; ~3-5%/yr)
    Scenario 4: Transformative AI (full automation possible; >5%/yr)

A scenario-conditional policy package adapts pillar intensity to the
realized AI productivity trajectory:

- Under Slow Growth: minimal intervention sufficient; tax + reskilling
  at modest scale handle distributional pressure.

- Under Faster Growth: sovereign equity + AI tax at framework scale;
  reskilling expanded; capability disclosure activated.

- Under Faster Acceleration: full framework + CERN-AI lab + compute
  governance treaty; UBI introduced as labor-displacement insurance.

- Under Transformative AI: UBI + UBC at maximum scale; sovereign equity
  at expanded scale; CERN-AI as primary AI development institution;
  full compute governance treaty.

This package operationalizes the adaptive-policy concept from Korinek
(2024) §4 (policy implications). The simulator activates the
scenario-appropriate intensity based on the realized
`ai_productivity_growth` parameter at runtime.

Reference:
    Korinek, A. (2024). "Scenarios for the Transition to AGI"
    NBER Working Paper No. 32549.
"""

from src.packages.base import (
    LeverTarget,
    PolicyLever,
    PolicyPackage,
    Reversibility,
)


# =============================================================================
# Scenario-conditional levers
# =============================================================================
# Each lever's effect scales with the realized AI productivity growth.
# The scaling is baked into the parameter_changes via a *high-intensity*
# specification, and a "korinek_scenario_scaler" parameter in the
# simulator determines how much of that intensity activates.

# Under Slow Growth (≤1.0%): minimal intervention
# Under Faster Growth (1.0-2.5%): framework-scale intervention
# Under Faster Acceleration (2.5-5.0%): expanded framework + CERN-AI
# Under Transformative (>5.0%): maximum-scale intervention


SCENARIO_ADAPTIVE_AI_TAX = PolicyLever(
    name="Scenario-Adaptive AI Tax (Korinek-conditional)",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "AI tax rate scales with realized productivity growth: 2% under "
        "Slow Growth; 5% under Faster Growth; 8% under Faster Acceleration; "
        "12% under Transformative AI. Higher productivity gains → larger "
        "rent pool → larger sustainable tax rate. Adapted from Korinek "
        "(2024) §4 policy implications."
    ),
    parameter_changes={
        # Specified at maximum scale; simulator scales down per
        # realized productivity scenario
        "ai_sector_tax_rate": 0.08,  # midpoint scenario
        "transfer_funding_per_gdp": 0.015,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.40,
    citation=(
        "Korinek (2024) NBER WP 32549 §4; EMPIRICAL_ANALOGS.md §3.5 "
        "(AI tax incidence under OECD coordination)."
    ),
)


SCENARIO_ADAPTIVE_UBI_UBC = PolicyLever(
    name="Scenario-Adaptive UBI + UBC (Korinek-conditional)",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "Direct transfer scale conditional on realized scenario: at Slow "
        "Growth, modest UBC only ($25K at 18); at Faster Acceleration, "
        "UBC + partial UBI ($600/mo); at Transformative AI, full UBI "
        "($1,500/mo) + full UBC. Adapted from Korinek (2024) §4 + Atkinson "
        "(2015) capital endowment proposal."
    ),
    parameter_changes={
        "ubi_monthly_per_adult": 1500.0,  # transformative-scale
        "ubc_grant_per_capita": 50000.0,
        "transfer_funding_per_gdp": 0.07,  # high; scaled by simulator
        "labor_supply_elasticity": -0.04,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation=(
        "Korinek (2024) NBER WP 32549; Atkinson (2015) capital endowment; "
        "OpenResearch UBI Study 2024 final results."
    ),
)


SCENARIO_ADAPTIVE_SOVEREIGN_EQUITY = PolicyLever(
    name="Scenario-Adaptive Sovereign Equity (Korinek-conditional)",
    target=LeverTarget.CAPITAL,
    description=(
        "Sovereign equity acquisition fraction scales with realized AI "
        "capital concentration. 5% under Slow Growth; 15% under Faster "
        "Growth; 25% under Faster Acceleration; 35% under Transformative AI. "
        "Higher concentration → larger socially-optimal public stake."
    ),
    parameter_changes={
        "sovereign_acquisition_fraction": 0.20,  # midpoint
        "cost_of_equity_premium": 0.005,
        "dividend_rate": 0.04,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation=(
        "Korinek (2024); Saudi HUMAIN + UAE MGX + Stargate analogs for "
        "scaling argument; Norway GPFG for governance."
    ),
)


SCENARIO_ADAPTIVE_CERN_AI = PolicyLever(
    name="Scenario-Adaptive CERN-AI Lab (Korinek-conditional)",
    target=LeverTarget.COMPETITION,
    description=(
        "CERN-AI public lab activates only when realized AI productivity "
        "exceeds Faster Growth threshold (>2.5%/yr). Below that, smaller "
        "NAIRR-scale public compute; above it, full CERN-AI scope. Hausenloy "
        "et al. (2023) MAGIC at full scale; AISI Network at modest scale."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.40,  # scaled per scenario
        "frontier_capability_diffusion": 0.15,
        "public_funding_per_gdp": 0.0015,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.30,
    citation=(
        "Hausenloy-Miotti-Dennis (2023) MAGIC; Bengio et al. (2025) "
        "International AI Safety Report; AISI Network."
    ),
)


SCENARIO_ADAPTIVE_RESKILLING = PolicyLever(
    name="Scenario-Adaptive Reskilling (Korinek-conditional)",
    target=LeverTarget.LABOR,
    description=(
        "Reskilling intensity scales with displacement velocity. Under Slow "
        "Growth, standard ALMP scope; under Transformative AI, near-universal "
        "lifelong-learning entitlement. Card-Kluve-Weber 2018 + Brookings "
        "Hamilton 2024 base; AI-specific extension."
    ),
    parameter_changes={
        "epsilon_sub_shift": 1.5,
        "skill_mix_complement_shift": 0.06,
        "reskilling_earnings_effect": 0.10,  # high end of CKW
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="EMPIRICAL_ANALOGS.md §7.5 (v2.0)",
)


SCENARIO_ADAPTIVE_COMPUTE_GOVERNANCE = PolicyLever(
    name="Scenario-Adaptive Compute Governance (Korinek-conditional)",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Compute governance treaty activates above Faster Growth (>2.5%/yr) "
        "with capability thresholds tightening as productivity grows. Under "
        "Transformative AI, compute monitoring becomes near-real-time; "
        "capability thresholds invoke pause authority."
    ),
    parameter_changes={
        "ai_arms_race_intensity": -0.25,
        "geopolitical_stability_index": 7.0,
        "frontier_compute_concentration": -0.10,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.50,
    citation=(
        "Sastry-Heim-Belfield 2024 'Computing Power and the Governance of AI'; "
        "Korinek (2024) §4 on Transformative AI scenario governance needs."
    ),
)


SCENARIO_ADAPTIVE_CAPABILITY_DISCLOSURE = PolicyLever(
    name="Scenario-Adaptive Capability Disclosure (Korinek-conditional)",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Capability disclosure obligation tier-by-tier: under Slow Growth, "
        "voluntary AISI participation; under Faster Growth, mandatory above "
        "threshold; under Faster Acceleration, mandatory + pause authority; "
        "under Transformative AI, treaty-grade verification."
    ),
    parameter_changes={
        "capability_disclosure_compliance": 0.80,
        "ai_safety_audit_coverage": 0.75,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.40,
    citation=(
        "Bengio et al. (2025) International AI Safety Report; "
        "AISI Network institutional analog."
    ),
)


# =============================================================================
# Package definition
# =============================================================================

KORINEK_SCENARIO = PolicyPackage(
    code="H",
    name="Korinek-Scenario-Conditional",
    description=(
        "Adapts pillar intensity to the realized AI productivity trajectory. "
        "Anchored to Korinek (2024) NBER WP 32549 four-scenario taxonomy: "
        "Slow Growth, Faster Growth, Faster Acceleration, Transformative AI. "
        "Under low productivity scenarios, intervention is modest; under "
        "high productivity / transformative AI scenarios, intervention "
        "expands to UBI scale + CERN-AI + compute governance treaty. "
        "Each lever is specified at near-maximum intensity; the simulator "
        "scales activation per the realized ai_productivity_growth "
        "parameter. This is the live alternative most engaged with the "
        "Korinek-Stiglitz transformation-economics tradition."
    ),
    levers=(
        SCENARIO_ADAPTIVE_AI_TAX,
        SCENARIO_ADAPTIVE_UBI_UBC,
        SCENARIO_ADAPTIVE_SOVEREIGN_EQUITY,
        SCENARIO_ADAPTIVE_CERN_AI,
        SCENARIO_ADAPTIVE_RESKILLING,
        SCENARIO_ADAPTIVE_COMPUTE_GOVERNANCE,
        SCENARIO_ADAPTIVE_CAPABILITY_DISCLOSURE,
    ),
    activation_year=2026,
    sequencing="sequential",  # treaty + lab take time to stand up
)
