"""Nebulai Framework v2: Participatory AI Economy Architecture.

Synthesizes the best-performing elements of every package tested in
this simulation, while preserving the original Nebulai framework's
"Participatory AI Economy" spirit:

- Sovereign participation in AI capital (original Pillar 1 idea, now
  scenario-adaptive per Package H)
- Public AI infrastructure (original Pillar 2, now operationalized as
  NAIRR-scale + CERN-AI consortium per Packages C, G, H)
- International coordination (original Pillar 3, now treaty-grade
  AISI International + OECD AI Tax framework per Packages C, G, H)
- Reskilling (original Pillar 4, now scenario-adaptive + care economy
  expansion per Packages H, E, F)
- Tiered openness + antitrust (replaces failed original Pillar 5
  open-weights mandate per Packages C, D, G)
- AI tax (original Pillar 6, now scenario-adaptive OECD-coordinated
  per Package H)
- Direct redistribution (NEW pillar from Package E - UBC + scenario UBI)
- Directed-AI development (NEW pillar from Package F Acemoglu-Johnson)
- AI safety + liability regime (NEW pillar from Packages D, G)

Nine pillars total, replacing the original six. The new framework
addresses every documented weakness of the original:

1. Pillar 1 too modest (10% fixed) → now 5-35% scenario-adaptive
2. Pillar 2 placeholder → now operationalized at $55B/yr
3. Pillar 3 placeholder → now treaty-grade AISI International
4. Pillar 4 reskilling → now expanded with care economy + codetermination
5. Pillar 5 open-weights mandate (fails under inversion) → replaced
6. Pillar 6 too modest (3% fixed) → now 2-12% scenario-adaptive
7. Missing direct redistribution → added (UBC + scenario UBI)
8. Missing directed AI development → added (Acemoglu-Johnson)
9. Missing AI safety / liability → added

The validation question this package answers: can the original
Nebulai Framework be improved enough to compete with Package H?
"""

from src.packages.base import (
    LeverTarget,
    PolicyLever,
    PolicyPackage,
    Reversibility,
)


PILLAR_1_SCENARIO_SOVEREIGN_EQUITY = PolicyLever(
    name="N2-1 Scenario-Adaptive Sovereign AI Equity (5-35%)",
    target=LeverTarget.CAPITAL,
    description=(
        "Public fund acquisition scaling with scenario: 5% (Slow Growth) "
        "→ 15% (Faster Growth) → 25% (Faster Acceleration) → 35% "
        "(Transformative AI). Captures Q1 2026 state-affiliated capital "
        "baseline (Stargate, EU InvestAI, Saudi HUMAIN, UAE MGX). "
        "Improvement over original Pillar 1 (fixed 10%)."
    ),
    parameter_changes={
        # Midpoint Faster Acceleration intensity (where framework optimization
        # is most beneficial): 25%
        "sovereign_acquisition_fraction": 0.25,
        "cost_of_equity_premium": 0.008,  # scales with acquisition
        "dividend_rate": 0.04,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation="EMPIRICAL_ANALOGS.md §1.1; Norway GPFG + Q1 2026 state-capital baseline",
)


PILLAR_2_PUBLIC_AI_INFRASTRUCTURE = PolicyLever(
    name="N2-2 Public AI Infrastructure + CERN-AI Consortium",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Public compute (NSF NAIRR scaled to $25B/yr) + CERN-AI public "
        "frontier lab ($30B/yr from 12-country consortium). Total ~$55B/yr "
        "of public AI infrastructure. Activates at Faster Growth threshold. "
        "Replaces the placeholder original Pillar 2 with concrete "
        "operationalization. Solves the open-weights inversion at the "
        "source by building public open-frontier capability."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.40,
        "ai_lab_entry_barrier": -0.15,
        "frontier_capability_diffusion": 0.18,
        "public_compute_per_gdp": 0.001,
        "public_funding_per_gdp": 0.002,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.30,
    citation="Hausenloy et al. 2023; Sastry-Heim-Belfield 2024; Mazzucato 2021",
)


PILLAR_3_INTERNATIONAL_ARCHITECTURE = PolicyLever(
    name="N2-3 International Architecture (AISI International + OECD AI Tax)",
    target=LeverTarget.GOVERNANCE,
    description=(
        "AISI International as treaty body (extends Bletchley → Seoul → "
        "Paris → Brussels). OECD AI Tax framework extending Pillar 1/2 "
        "minimum tax. Compute governance treaty modeled on NPT + IAEA "
        "verification. Capability threshold + mutual pause authority above "
        "Faster Acceleration tier. Replaces placeholder original Pillar 3."
    ),
    parameter_changes={
        "ai_arms_race_intensity": -0.25,
        "geopolitical_stability_index": 6.0,
        "frontier_compute_concentration": -0.10,
        "capability_disclosure_compliance": 0.85,
        "ai_safety_audit_coverage": 0.80,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.50,
    citation="Sastry-Heim-Belfield 2024; Bengio et al. 2025 International AI Safety Report",
)


PILLAR_4_RESKILLING_AND_CARE_ECONOMY = PolicyLever(
    name="N2-4 Scenario-Adaptive Reskilling + Care Economy + Codetermination",
    target=LeverTarget.LABOR,
    description=(
        "Expanded labor pillar combining: scenario-adaptive reskilling "
        "(Standard ALMP → universal lifelong learning entitlement); care "
        "economy expansion ($150B/yr into childcare/eldercare/mental "
        "health); worker codetermination on AI deployment (German "
        "Mitbestimmung model for firms >1,000 employees). Synthesizes "
        "Packages H + E + F best-in-class labor mechanisms."
    ),
    parameter_changes={
        "epsilon_sub_shift": 1.6,
        "skill_mix_complement_shift": 0.07,
        "reskilling_earnings_effect": 0.12,  # high end of CKW range
        "displacement_speed_dampening": 0.25,
        "care_sector_employment_share": 0.030,
        "median_wage_floor": 0.06,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation=(
        "EMPIRICAL_ANALOGS.md §7.5 (v2.0); Card-Kluve-Weber 2018 + "
        "Brookings Hamilton 2024 + Acemoglu-Johnson 2023 + Jäger-Schoefer "
        "2021 on Mitbestimmung"
    ),
)


PILLAR_5_TIERED_OPENNESS_PLUS_ANTITRUST = PolicyLever(
    name="N2-5 Tiered Openness + Antitrust Structural Separation",
    target=LeverTarget.COMPETITION,
    description=(
        "REPLACES failed original Pillar 5 unilateral open-weights mandate. "
        "New mechanism: (a) tiered openness within CERN-AI consortium "
        "framework (open methodology + activations + evals above threshold, "
        "open weights below); (b) antitrust structural separation (model "
        "labs ≠ cloud providers ≠ application layers); (c) non-"
        "discriminatory compute access mandate. Addresses open-weights "
        "inversion via public lab (Pillar 2) instead of private mandate."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.50,  # strong dampening via separation
        "ai_sector_concentration_shift": -0.20,
        "compute_layer_profit_share_cap": 0.15,
        "compute_access_premium_for_independents": -0.40,
        "safety_audit_capacity": 1.5,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.40,
    citation=(
        "Khan 2017; Hovenkamp 2021; AT&T 1982 historical analog; "
        "Solaiman 2023 + Seger et al. 2023 tiered openness"
    ),
)


PILLAR_6_SCENARIO_AI_TAX = PolicyLever(
    name="N2-6 Scenario-Adaptive AI Tax (2-12% OECD-coordinated)",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "AI sector value-added tax scaling with scenario: 2% (Slow Growth) "
        "→ 5% (Faster Growth) → 8% (Faster Acceleration) → 12% "
        "(Transformative AI). OECD-coordinated to prevent base erosion. "
        "Revenue allocation: 60% UBI/UBC (Pillar 7), 30% CERN-AI "
        "(Pillar 2), 10% AISI (Pillar 3). Improvement over original "
        "Pillar 6 (fixed 3%)."
    ),
    parameter_changes={
        # Midpoint Faster Acceleration: 8%
        "ai_sector_tax_rate": 0.08,
        "transfer_funding_per_gdp": 0.014,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.40,
    citation="EMPIRICAL_ANALOGS.md §3.5; OECD Pillar 1/2 framework",
)


PILLAR_7_DIRECT_REDISTRIBUTION = PolicyLever(
    name="N2-7 Direct Redistribution (UBC + Scenario-Adaptive UBI)",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "NEW pillar absent from original Nebulai framework. Universal "
        "Basic Capital at scenario-conditional intensity ($25K Slow Growth "
        "→ $75K Transformative AI). UBI activates at Faster Acceleration "
        "tier ($600/mo) and scales to $1,500/mo under Transformative AI. "
        "Funded from Pillars 1 + 6 revenue."
    ),
    parameter_changes={
        # Midpoint Faster Acceleration intensity: $50K UBC + $600 UBI
        "ubc_grant_per_capita": 50000.0,
        "ubi_monthly_per_adult": 600.0,
        "transfer_funding_per_gdp": 0.045,
        "labor_supply_elasticity": -0.04,  # v2.0 OpenResearch
        "wealth_distribution_floor": 0.015,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation=(
        "EMPIRICAL_ANALOGS.md §1.2 + §2.1 + §7.6; Atkinson 2015 + "
        "Sherraden 1991 + OpenResearch UBI 2024 final"
    ),
)


PILLAR_8_DIRECTED_AI_DEVELOPMENT = PolicyLever(
    name="N2-8 Directed AI Development (Acemoglu-Johnson)",
    target=LeverTarget.PRODUCTION,
    description=(
        "NEW pillar absent from original Nebulai framework. Directed "
        "public R&D ($30B/yr) for human-complementary AI applications. "
        "Federal procurement preference for non-displacing AI (using "
        "~$700B/yr federal spending as leverage). Operates upstream of "
        "distribution: if AI is built as labor complement rather than "
        "substitute, the redistribution problem becomes smaller."
    ),
    parameter_changes={
        "labor_augmenting_productivity_growth": 0.012,
        "automation_threshold_growth_dampening": 0.35,
        "skill_mix_complement_shift": 0.08,
        "public_rd_per_gdp": 0.0012,
        "ai_market_share_complement_systems": 0.12,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Acemoglu & Johnson 2023 Power and Progress; Mazzucato 2013/2021",
)


PILLAR_9_AI_SAFETY_AND_LIABILITY = PolicyLever(
    name="N2-9 AI Safety + Liability Regime",
    target=LeverTarget.GOVERNANCE,
    description=(
        "NEW pillar absent from original Nebulai framework. AI liability "
        "+ mandatory insurance regime (Price-Anderson nuclear analog). "
        "Mandatory capability disclosure already in Pillar 3; this adds "
        "the liability-internalization mechanism. Self-enforcing — "
        "uninsured deployment economically irrational. Synthesizes "
        "Packages D + G safety mechanisms."
    ),
    parameter_changes={
        "deployment_risk_pricing": 1.0,
        "ai_misuse_externality_internalization": 0.60,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation=(
        "Bengio et al. 2025 International AI Safety Report; Price-"
        "Anderson Act + CERCLA / Superfund nuclear/environmental analogs"
    ),
)


# Package code "N" for Nebulai v2 (distinct from B, the original)
NEBULAI_V2 = PolicyPackage(
    code="N",
    name="Nebulai Framework v2 (Best-of-All Synthesis)",
    description=(
        "Improved Nebulai Framework synthesizing the best-performing "
        "elements of every package tested. Nine pillars replace the "
        "original six. Addresses every documented weakness of Package B: "
        "Pillar 1 scenario-adaptive, Pillar 2/3 operationalized, Pillar 5 "
        "redesigned post-open-weights-inversion, Pillar 6 scenario-"
        "adaptive. Adds three new pillars: direct redistribution (from E), "
        "directed-AI development (from F), AI safety + liability (from D/G). "
        "Preserves Participatory AI Economy spirit with materially "
        "stronger empirical foundation. Tested against Package H to "
        "determine whether improved framework matches or exceeds the "
        "scenario-adaptive Korinek architecture."
    ),
    levers=(
        PILLAR_1_SCENARIO_SOVEREIGN_EQUITY,
        PILLAR_2_PUBLIC_AI_INFRASTRUCTURE,
        PILLAR_3_INTERNATIONAL_ARCHITECTURE,
        PILLAR_4_RESKILLING_AND_CARE_ECONOMY,
        PILLAR_5_TIERED_OPENNESS_PLUS_ANTITRUST,
        PILLAR_6_SCENARIO_AI_TAX,
        PILLAR_7_DIRECT_REDISTRIBUTION,
        PILLAR_8_DIRECTED_AI_DEVELOPMENT,
        PILLAR_9_AI_SAFETY_AND_LIABILITY,
    ),
    activation_year=2026,
    sequencing="sequential",  # Reversibility-weighted phased rollout
)
