"""Package D: Compute-Centric.

Treats compute as the actual chokepoint. Compute tax + access mandates +
structural separation of compute providers from model labs. Domestic-feasible
(doesn't require multilateral coordination), works against the actual
concentration point in the AI value chain.

Theoretical basis:
- Sastry, Heim, Belfield et al. (2024) "Computing Power and the Governance
  of AI"
- Khan (2017) "Amazon's Antitrust Paradox"
- Wu (2018) "The Curse of Bigness"
- Heim et al. (2024) "Compute Funds"
- Hovenkamp (2021) on platform monopoly antitrust
"""

from src.packages.base import (
    LeverTarget,
    PolicyLever,
    PolicyPackage,
    Reversibility,
)


COMPUTE_TAX = PolicyLever(
    name="Compute Tax (FLOPs-Based)",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "Tax measured per training-run FLOPs above threshold. Solves "
        "incidence problem of revenue-based taxes: incidence falls on "
        "compute consumers (frontier labs) directly, not on AI service "
        "users via prices. Modeled on carbon tax mechanics."
    ),
    parameter_changes={
        "compute_tax_per_pflop_day": 100.0,  # USD per pflop-day above threshold
        "transfer_funding_per_gdp": 0.006,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,  # domestic feasibility
    coalition_threshold=0.0,
    citation="Sastry, Heim, Belfield et al. 2024; Heim et al. 2024",
)

COMPUTE_ACCESS_MANDATE = PolicyLever(
    name="Non-Discriminatory Compute Access Mandate",
    target=LeverTarget.COMPETITION,
    description=(
        "Hyperscalers must provide compute on non-discriminatory terms; "
        "no bundled-equity deals (Microsoft-OpenAI, Anthropic-Amazon "
        "patterns). Compute is treated as common-carrier utility. Models "
        "on telecom common-carrier regulation."
    ),
    parameter_changes={
        "compute_access_premium_for_independents": -0.40,  # 40% drop
        "ai_lab_concentration": -0.10,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Khan 2017; Wu 2018; Hovenkamp 2021",
)

PUBLIC_COMPUTE_INFRASTRUCTURE = PolicyLever(
    name="Public Compute Infrastructure (NSF NAIRR Scaled)",
    target=LeverTarget.GOVERNANCE,
    description=(
        "National AI Research Resource (NAIRR) and equivalents at $50–100B/yr "
        "scale. Public compute available to academia, public-purpose AI "
        "research, small firms. Reduces frontier-AI rent extraction by "
        "providing exit option to private-compute dependence."
    ),
    parameter_changes={
        "public_compute_per_gdp": 0.003,
        "ai_lab_entry_barrier": -0.30,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Sastry et al. 2024; NAIRR Task Force reports",
)

STRUCTURAL_SEPARATION_AI_VALUE_CHAIN = PolicyLever(
    name="Structural Separation of AI Value Chain",
    target=LeverTarget.COMPETITION,
    description=(
        "Antitrust action: model labs cannot be vertically integrated with "
        "cloud providers or with application-layer deployers. Three layers "
        "must be separately owned. Modeled on AT&T 1982 breakup, more "
        "recently Sherman Act § 2 application to platform monopolies."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.45,
        "ai_sector_concentration_shift": -0.20,
        "compute_layer_profit_share_cap": 0.15,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,  # remerger requires antitrust waiver
    requires_coordination=False,
    citation="Khan 2017; Hovenkamp 2021; AT&T 1982 historical analog",
)

AI_LIABILITY_INSURANCE = PolicyLever(
    name="AI Liability + Mandatory Insurance",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Strict liability for harms from above-threshold AI deployment; "
        "mandatory liability insurance. Self-enforcing — uninsured "
        "deployment economically irrational. Models on environmental "
        "Superfund liability, nuclear operator insurance (Price-Anderson)."
    ),
    parameter_changes={
        "deployment_risk_pricing": 1.0,  # presence indicator
        "ai_misuse_externality_internalization": 0.60,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Bengio et al. 2024; nuclear/environmental liability analogs",
)

CAPABILITY_DISCLOSURE_DOMESTIC = PolicyLever(
    name="Mandatory Capability Disclosure (Domestic)",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Same as Package C version but implementable unilaterally as US "
        "regulation. Above-threshold training runs and deployments require "
        "evaluation and disclosure to AISI. Tightens existing US AI "
        "executive orders."
    ),
    parameter_changes={
        "capability_disclosure_compliance": 0.90,
        "ai_safety_audit_coverage": 0.75,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="US AI Executive Orders; AISI Network; Anderljung et al. 2023",
)

COMPUTE_CENTRIC = PolicyPackage(
    code="D",
    name="Compute-Centric Package",
    description=(
        "Treats compute as the actual policy chokepoint. Compute tax + "
        "non-discriminatory access mandates + public compute infrastructure "
        "+ structural separation of compute / model / application layers + "
        "AI liability with mandatory insurance + capability disclosure. "
        "All levers domestic-feasible — does not require multilateral "
        "coordination, which makes it the most politically tractable "
        "package."
    ),
    levers=(
        COMPUTE_TAX,
        COMPUTE_ACCESS_MANDATE,
        PUBLIC_COMPUTE_INFRASTRUCTURE,
        STRUCTURAL_SEPARATION_AI_VALUE_CHAIN,
        AI_LIABILITY_INSURANCE,
        CAPABILITY_DISCLOSURE_DOMESTIC,
    ),
    activation_year=2026,
    sequencing="simultaneous",
)
