"""Nebulai Framework v3 — Political-Variant Tests.

Tests whether the Nebulai framework's mechanics are politically-robust
by specifying three variants representing distinct political-economic
traditions:

    v3-A Conservative — Market-Sovereign Architecture
        Intellectual basis: Cowen / Cochrane / national-security AI hawks
        Emphasizes: economic dynamism, national competitiveness, property
        rights, work incentives, private-sector primacy with strategic
        public-sector role.
        Skeptical of: aggressive redistribution, large UBI, mandatory
        labor rules.

    v3-B Progressive — Workers' AI Economy Architecture
        Intellectual basis: Stiglitz / Saez / Mazzucato / progressive
        labor economists
        Emphasizes: distribution, worker power, public ownership,
        decommodification, care economy.
        Skeptical of: capital-friendly policies, market-only solutions.

    v3-C Centrist Mix — same as Nebulai v2 (already specified)
        Serves as the natural midpoint reference. Not duplicated here;
        use NEBULAI_V2 for the comparison.

The test answers: across the political spectrum, which welfare priorities
does each variant deliver, and at what cost? Does any political
alignment dominate the others on multi-metric performance, or does the
centrist Nebulai v2 hold up as the empirical best-balanced architecture?

Reference for variant grounding:
- Conservative: Cowen "Average Is Over"; Cochrane on macroeconomic
  prudence; CSIS national-security AI work; recent FTC backlash framing
- Progressive: Stiglitz Globalization and Its Discontents; Saez-Zucman
  2019 wealth tax; Mazzucato Mission Economy; Acemoglu-Johnson
  Power and Progress (worker-rights interpretation)
"""

from src.packages.base import (
    LeverTarget,
    PolicyLever,
    PolicyPackage,
    Reversibility,
)


# ============================================================================
# v3-A CONSERVATIVE: Market-Sovereign Architecture
# ============================================================================

V3A_SOVEREIGN_EQUITY_MODEST = PolicyLever(
    name="v3A-1 Modest Sovereign Equity (5-15%, private-primacy)",
    target=LeverTarget.CAPITAL,
    description=(
        "Conservative variant: modest sovereign equity (5% Slow Growth → "
        "15% Faster Acceleration). Preserves private capital primacy. "
        "Justified on national-security grounds rather than redistribution. "
        "Modeled on Norway GPFG (foreign assets only — domestic stake "
        "limited to strategic AI capacity)."
    ),
    parameter_changes={
        # Midpoint: 10%
        "sovereign_acquisition_fraction": 0.10,
        "cost_of_equity_premium": 0.003,  # smaller premium with smaller stake
        "dividend_rate": 0.04,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation="Norway GPFG; CSIS national-security AI work",
)


V3A_NATIONAL_SECURITY_COMPUTE = PolicyLever(
    name="v3A-2 National Security Compute (strategic public infrastructure)",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Conservative variant: national-security-framed public compute "
        "($15B/yr, smaller than v2's $55B). NSF NAIRR + strategic-reserve "
        "compute. No CERN-AI consortium (sovereignty concerns). Focus on "
        "domestic capability advantage and export-control infrastructure."
    ),
    parameter_changes={
        "ai_lab_entry_barrier": -0.08,
        "frontier_capability_diffusion": 0.05,
        "public_compute_per_gdp": 0.0006,
        "public_funding_per_gdp": 0.0008,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="NSF NAIRR Task Force; CSIS national-security framing",
)


V3A_BIS_EXPORT_CONTROLS = PolicyLever(
    name="v3A-3 Strengthened Export Controls + Strategic Competition Posture",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Conservative variant: strengthen BIS export controls and "
        "tech-decoupling regime. AISI International only with allies "
        "(no China). Strategic posture toward US-China competition, "
        "not cooperation. No compute governance treaty with adversaries."
    ),
    parameter_changes={
        "ai_arms_race_intensity": +0.10,  # accepts arms race for advantage
        "geopolitical_stability_index": -2.0,  # bipolar tension increases
        "capability_disclosure_compliance": 0.65,
        "ai_safety_audit_coverage": 0.60,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.35,  # allies-only coalition
    citation="BIS export controls; CSIS / Hudson strategic competition framing",
)


V3A_RESKILLING_TAX_CREDITS = PolicyLever(
    name="v3A-4 Market-Based Reskilling (tax credits, not entitlement)",
    target=LeverTarget.LABOR,
    description=(
        "Conservative variant: reskilling delivered via tax credits for "
        "private employers, not as universal entitlement. No worker "
        "codetermination. Effect size at low end of Card-Kluve-Weber "
        "range (5%) due to less concentrated delivery mechanism."
    ),
    parameter_changes={
        "epsilon_sub_shift": 1.2,  # smaller outside-option boost
        "skill_mix_complement_shift": 0.03,
        "reskilling_earnings_effect": 0.05,  # CKW low end
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Trade Adjustment Assistance + employer tax credit precedents",
)


V3A_LIGHT_ANTITRUST = PolicyLever(
    name="v3A-5 Light Antitrust (national-competitiveness framing)",
    target=LeverTarget.COMPETITION,
    description=(
        "Conservative variant: targeted antitrust focused on foreign "
        "capture and competition-with-China rather than concentration "
        "per se. No structural separation. No mandatory open-weights. "
        "Preserves US AI lab market position vs. Chinese competitors."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.15,  # modest dampening
        "ai_sector_concentration_shift": -0.05,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="National-competitiveness antitrust framing; CSIS",
)


V3A_MODEST_AI_TAX = PolicyLever(
    name="v3A-6 Modest AI Tax (2-4%, growth-friendly)",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "Conservative variant: AI tax scaling 2% (Slow Growth) → 4% "
        "(Transformative). Below revenue-maximizing rate to preserve "
        "growth incentives. OECD-coordinated when possible."
    ),
    parameter_changes={
        # Midpoint Faster Growth: 3%
        "ai_sector_tax_rate": 0.03,
        "transfer_funding_per_gdp": 0.005,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.30,
    citation="OECD Pillar 1/2; lower-rate calibration for growth preservation",
)


V3A_UBC_ONLY_NO_UBI = PolicyLever(
    name="v3A-7 UBC Only (no UBI — preserves work incentives)",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "Conservative variant: Universal Basic Capital ($30K at 18) as "
        "one-time grant, NOT UBI. Preserves work incentives. UBC delivered "
        "via tax credit to be invested in approved vehicles (401k, "
        "retirement, education, small business)."
    ),
    parameter_changes={
        "ubc_grant_per_capita": 30000.0,
        "transfer_funding_per_gdp": 0.012,
        "wealth_distribution_floor": 0.008,
        "labor_supply_elasticity": 0.0,  # no labor supply impact (no UBI)
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation="Atkinson 2015 UBC; conservative work-incentive framing",
)


V3A_DIRECTED_AI_NATIONAL = PolicyLever(
    name="v3A-8 Directed AI for National Competitiveness",
    target=LeverTarget.PRODUCTION,
    description=(
        "Conservative variant: directed R&D framed as national "
        "competitiveness (vs. China) rather than labor-complementarity. "
        "DARPA model. Heavy federal procurement preference for domestic "
        "AI capability."
    ),
    parameter_changes={
        "labor_augmenting_productivity_growth": 0.008,
        "automation_threshold_growth_dampening": 0.15,
        "skill_mix_complement_shift": 0.04,
        "public_rd_per_gdp": 0.0015,  # higher than v2 (national priority)
        "ai_market_share_complement_systems": 0.05,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="DARPA model; Cowen national-competitiveness framing",
)


V3A_AI_LIABILITY = PolicyLever(
    name="v3A-9 AI Liability + Insurance (market mechanism)",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Conservative variant: AI liability + mandatory insurance "
        "(Price-Anderson nuclear analog). Market-based safety mechanism. "
        "No mandatory pre-deployment government review."
    ),
    parameter_changes={
        "deployment_risk_pricing": 1.0,
        "ai_misuse_externality_internalization": 0.45,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Price-Anderson Act; market-mechanism safety regime",
)


NEBULAI_V3_CONSERVATIVE = PolicyPackage(
    code="K",  # K for "Konservative" (avoids conflicts with A-H, N, R, V)
    name="Nebulai v3-A Conservative (Market-Sovereign)",
    description=(
        "Conservative variant of Nebulai framework: emphasizes private "
        "capital primacy, work incentives, national competitiveness, and "
        "strategic competition. Modest sovereign equity (5-15%), UBC-only "
        "(no UBI), tax-credit reskilling, light antitrust, national-"
        "security compute. Grounded in Cowen / Cochrane / CSIS strategic "
        "competition tradition. Tested against centrist Nebulai v2."
    ),
    levers=(
        V3A_SOVEREIGN_EQUITY_MODEST,
        V3A_NATIONAL_SECURITY_COMPUTE,
        V3A_BIS_EXPORT_CONTROLS,
        V3A_RESKILLING_TAX_CREDITS,
        V3A_LIGHT_ANTITRUST,
        V3A_MODEST_AI_TAX,
        V3A_UBC_ONLY_NO_UBI,
        V3A_DIRECTED_AI_NATIONAL,
        V3A_AI_LIABILITY,
    ),
    activation_year=2026,
    sequencing="sequential",
)


# ============================================================================
# v3-B PROGRESSIVE: Workers' AI Economy Architecture
# ============================================================================

V3B_AGGRESSIVE_SOVEREIGN_EQUITY = PolicyLever(
    name="v3B-1 Aggressive Sovereign Equity (25-50%, public-primacy)",
    target=LeverTarget.CAPITAL,
    description=(
        "Progressive variant: aggressive sovereign equity (25% Slow Growth "
        "→ 50% Transformative AI). Major public stake in AI capital. "
        "Justified on distributive grounds. Modeled on Singapore Temasek "
        "+ Norway GPFG combined approach."
    ),
    parameter_changes={
        # Midpoint Faster Acceleration: 35%
        "sovereign_acquisition_fraction": 0.35,
        "cost_of_equity_premium": 0.015,  # larger premium
        "dividend_rate": 0.05,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation="Singapore Temasek + Norway GPFG; Stiglitz on public capital",
)


V3B_MAXIMUM_PUBLIC_INFRASTRUCTURE = PolicyLever(
    name="v3B-2 Maximum Public AI Infrastructure ($80B/yr CERN-AI scale)",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Progressive variant: $80B/yr public AI infrastructure (vs. v2's "
        "$55B). NSF NAIRR scaled + CERN-AI global consortium at full "
        "scale + public training data trusts. Frontier AI as public good."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.55,
        "ai_lab_entry_barrier": -0.25,
        "frontier_capability_diffusion": 0.25,
        "public_compute_per_gdp": 0.0015,
        "public_funding_per_gdp": 0.0028,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.30,
    citation="Hausenloy MAGIC at maximum scale; Mazzucato",
)


V3B_GLOBAL_COMMONS_GOVERNANCE = PolicyLever(
    name="v3B-3 Global Commons Governance (treaty-grade, inclusive)",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Progressive variant: inclusive global governance including China, "
        "Global South. AISI International with strong public-interest "
        "mandate. Compute governance treaty with mandatory transparency. "
        "Strong open-weights mandate within consortium framework."
    ),
    parameter_changes={
        "ai_arms_race_intensity": -0.35,
        "geopolitical_stability_index": 9.0,
        "frontier_compute_concentration": -0.15,
        "capability_disclosure_compliance": 0.95,
        "ai_safety_audit_coverage": 0.90,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.55,
    citation="Stiglitz on global commons; Trager et al. inclusive governance",
)


V3B_UNIVERSAL_RESKILLING_PLUS_CODETERMINATION = PolicyLever(
    name="v3B-4 Universal Reskilling + Mandatory Codetermination + Care Economy ($300B/yr)",
    target=LeverTarget.LABOR,
    description=(
        "Progressive variant: universal lifelong-learning entitlement + "
        "mandatory worker codetermination at ALL firms (not just >1,000 "
        "employees) + major care economy expansion ($300B/yr into "
        "childcare/eldercare/mental health). Acemoglu-Johnson interpreted "
        "as worker-power framework."
    ),
    parameter_changes={
        "epsilon_sub_shift": 2.0,
        "skill_mix_complement_shift": 0.10,
        "reskilling_earnings_effect": 0.15,  # high end of CKW
        "displacement_speed_dampening": 0.40,
        "care_sector_employment_share": 0.060,
        "median_wage_floor": 0.12,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation="Acemoglu-Johnson Power and Progress; Stiglitz on care economy",
)


V3B_AGGRESSIVE_STRUCTURAL_SEPARATION = PolicyLever(
    name="v3B-5 Aggressive Structural Separation + Mandatory Open Weights",
    target=LeverTarget.COMPETITION,
    description=(
        "Progressive variant: aggressive structural separation (model "
        "labs ≠ cloud ≠ apps) + mandatory open-weights for all foundation "
        "models above threshold (no tiered exception). Maximum antitrust "
        "enforcement posture."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.60,
        "ai_sector_concentration_shift": -0.30,
        "compute_layer_profit_share_cap": 0.10,
        "compute_access_premium_for_independents": -0.55,
        "safety_audit_capacity": 2.0,
    },
    reversibility=Reversibility.IRREVERSIBLE,  # open weights mandate is irreversible
    requires_coordination=True,
    coalition_threshold=0.45,
    citation="Khan 2017; Wu 2018; aggressive Brandeisian interpretation",
)


V3B_MAXIMUM_AI_TAX = PolicyLever(
    name="v3B-6 Maximum AI Tax (8-15% OECD-coordinated)",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "Progressive variant: AI tax scaling 8% (Slow Growth) → 15% "
        "(Transformative). At revenue-maximizing rates. OECD-coordinated."
    ),
    parameter_changes={
        # Midpoint Faster Acceleration: 12%
        "ai_sector_tax_rate": 0.12,
        "transfer_funding_per_gdp": 0.022,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.40,
    citation="Saez-Zucman 2019; OECD Pillar 1/2 + sector-specific surcharge",
)


V3B_FULL_UBI_PLUS_WEALTH_TAX = PolicyLever(
    name="v3B-7 Full UBI ($1,500/mo) + UBC ($75K) + Progressive Wealth Tax",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "Progressive variant: full UBI ($1,500/mo) immediately (not "
        "scenario-conditional). UBC at $75K. Progressive wealth tax "
        "(Saez-Zucman 2019 design: 2% above $50M, 3% above $1B). Major "
        "decommodification of basic income security."
    ),
    parameter_changes={
        "ubi_monthly_per_adult": 1500.0,
        "ubc_grant_per_capita": 75000.0,
        "wealth_tax_marginal_top": 0.03,
        "transfer_funding_per_gdp": 0.090,  # ~9% of GDP
        "labor_supply_elasticity": -0.05,  # higher than v2.0 with full UBI
        "wealth_distribution_floor": 0.025,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.40,
    citation="Saez-Zucman 2019; OpenResearch 2024 + Van Parijs Basic Income",
)


V3B_DIRECTED_AI_LABOR_COMPLEMENT = PolicyLever(
    name="v3B-8 Directed AI for Worker Complementarity",
    target=LeverTarget.PRODUCTION,
    description=(
        "Progressive variant: directed R&D framed for labor "
        "complementarity (Acemoglu-Johnson literal interpretation). "
        "Heavy federal procurement of complement-AI. Worker voice in "
        "deployment decisions via codetermination."
    ),
    parameter_changes={
        "labor_augmenting_productivity_growth": 0.020,
        "automation_threshold_growth_dampening": 0.50,
        "skill_mix_complement_shift": 0.12,
        "public_rd_per_gdp": 0.0015,
        "ai_market_share_complement_systems": 0.20,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Acemoglu-Johnson Power and Progress; Mazzucato Mission Economy",
)


V3B_PUBLIC_INTEREST_SAFETY = PolicyLever(
    name="v3B-9 Public-Interest AI Safety (mandatory pre-deployment + pause authority)",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Progressive variant: public-interest safety regime. Mandatory "
        "pre-deployment evaluation by AISI International. Pause authority "
        "exercised on public-interest grounds. AI liability + mandatory "
        "insurance + public investigation rights."
    ),
    parameter_changes={
        "deployment_risk_pricing": 1.0,
        "ai_misuse_externality_internalization": 0.80,
        "capability_disclosure_compliance": 0.95,
        "ai_safety_audit_coverage": 0.95,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.40,
    citation="Bengio 2025 + public-interest framing",
)


NEBULAI_V3_PROGRESSIVE = PolicyPackage(
    code="P",  # P for "Progressive"
    name="Nebulai v3-B Progressive (Workers' AI Economy)",
    description=(
        "Progressive variant of Nebulai framework: emphasizes public "
        "ownership, worker power, decommodification, care economy. "
        "Aggressive sovereign equity (25-50%), full UBI immediately, "
        "universal codetermination, aggressive antitrust + structural "
        "separation, mandatory open-weights. Grounded in Stiglitz / Saez / "
        "Mazzucato / Acemoglu-Johnson left-interpretation tradition. "
        "Tested against centrist Nebulai v2 and conservative v3-A."
    ),
    levers=(
        V3B_AGGRESSIVE_SOVEREIGN_EQUITY,
        V3B_MAXIMUM_PUBLIC_INFRASTRUCTURE,
        V3B_GLOBAL_COMMONS_GOVERNANCE,
        V3B_UNIVERSAL_RESKILLING_PLUS_CODETERMINATION,
        V3B_AGGRESSIVE_STRUCTURAL_SEPARATION,
        V3B_MAXIMUM_AI_TAX,
        V3B_FULL_UBI_PLUS_WEALTH_TAX,
        V3B_DIRECTED_AI_LABOR_COMPLEMENT,
        V3B_PUBLIC_INTEREST_SAFETY,
    ),
    activation_year=2026,
    sequencing="sequential",
)
