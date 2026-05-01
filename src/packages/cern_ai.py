"""Package C: CERN-AI Centered.

Global public frontier lab + compute governance treaty + tiered openness +
supporting transfers. Replaces or subsumes Pillar 5 of Package B with a
stronger mechanism: rather than mandating openness for private firms,
build a public alternative that produces open frontier capability.

Theoretical basis:
- Hausenloy, Miotti & Dennis (2023) "MAGIC" proposal
- Bengio et al. (2024) "Managing AI Risks"
- Sastry, Heim, Belfield et al. (2024) "Computing Power and the
  Governance of AI"
- Ostrom (1990) — applies the eight design principles to AI capability as
  commons

This is one of the central candidates and is the focus of Hypothesis 1
(open-weights inversion) and Hypothesis 9 (package dominance).
"""

from src.packages.base import (
    LeverTarget,
    PolicyLever,
    PolicyPackage,
    Reversibility,
)


CERN_AI_PUBLIC_LAB = PolicyLever(
    name="Global Public Frontier Lab (CERN-AI / MAGIC)",
    target=LeverTarget.COMPETITION,
    description=(
        "Multilateral public lab building open-weights frontier models at "
        "or near private-lab capability. ~$30B/yr funding from 12-country "
        "consortium. Outputs: open weights, training methodology, eval "
        "results, interpretability research. Effect: collapses private "
        "frontier rents at the source rather than redistributing them."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.55,  # stronger than mandate alone
        "ai_sector_concentration_shift": -0.15,
        "frontier_capability_diffusion": 0.20,  # speeds up downstream access
        "public_funding_per_gdp": 0.0015,  # ~0.15% of frontier-bloc GDP
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,  # institution survives partial defunding
    requires_coordination=True,
    coalition_threshold=0.30,  # US+EU+JP+KR alone ~30% of frontier compute is enough
    citation="Hausenloy et al. 2023; Bengio et al. 2024; CERN historical analog",
)

COMPUTE_GOVERNANCE_TREATY = PolicyLever(
    name="Multilateral Compute Governance Treaty",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Treaty-grade compute monitoring and capability-threshold "
        "agreements modeled on NPT + Wassenaar. Verification via fab "
        "inspection, power monitoring, customs reporting. Defection "
        "produces detectable signature; punishment is reciprocal compute "
        "restriction. Solves the verification problem that pure open-"
        "weights mandates cannot."
    ),
    parameter_changes={
        "ai_arms_race_intensity": -0.30,
        "geopolitical_stability_index": 8.0,  # +8 points
        "frontier_compute_concentration": -0.10,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.50,  # need supply-chain controllers
    citation="Sastry, Heim, Belfield et al. 2024; Heim et al. 2024",
)

TIERED_OPENNESS_FOR_FRONTIER = PolicyLever(
    name="Tiered Openness for Above-Threshold Capability",
    target=LeverTarget.COMPETITION,
    description=(
        "Below capability-threshold T1: full open weights mandate. Above "
        "T1: open methodology, training data, eval results, internal "
        "activations for safety research, but weights behind controlled "
        "API. Replaces Pillar 5 of Package B with safety-aware version. "
        "Preserves auditability without solving misuse problems by "
        "creating them."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.30,  # smaller than full open mandate
        "safety_audit_capacity": 1.5,  # 1.5x researcher access to internals
        "misuse_proliferation_risk": -0.05,  # net safer than full open
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.50,
    citation="Solaiman 2023; Seger et al. 2023; Bommasani et al. 2024",
)

CAPABILITY_DISCLOSURE_AND_EVAL = PolicyLever(
    name="Mandatory Capability Disclosure + Pre-Deployment Eval",
    target=LeverTarget.GOVERNANCE,
    description=(
        "All frontier training runs above compute threshold must register "
        "with AISI Network; pre-deployment evals required for systems "
        "above capability threshold. Builds on existing AISI infrastructure "
        "(UK, US, JP, SG, CA, IN, KR, FR, EU AI Office). Marginal "
        "contribution over status quo: enforceability + threshold rigor."
    ),
    parameter_changes={
        "capability_disclosure_compliance": 0.85,
        "ai_safety_audit_coverage": 0.80,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.40,  # AISI Network already covers ~40% of frontier compute
    citation="International AI Safety Report 2025; Bengio et al. 2024",
)

UBC_AT_18_FUNDED_BY_LAB_OUTPUTS = PolicyLever(
    name="Universal Basic Capital (at-18 grant) Funded by CERN-AI Surplus",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "Citizens receive a one-time capital grant at age 18, funded by "
        "CERN-AI consortium operating surplus + AI tax. Replaces Pillar 1 "
        "(sovereign equity) of Package B with mechanism that doesn't "
        "require backward expropriation of existing capital owners. Atkinson "
        "2015 / Sherraden 1991."
    ),
    parameter_changes={
        "ubc_grant_per_capita": 25000.0,  # USD at age 18
        "wealth_distribution_floor": 0.005,  # 0.5pp gain to bottom 50% share
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    coalition_threshold=0.0,
    citation="Atkinson 2015; Sherraden 1991",
)

AI_TAX_OECD_COORDINATED = PolicyLever(
    name="AI Tax (5%, OECD-Coordinated)",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "Slightly stronger than Pillar 6 (5% vs 3%) and explicitly OECD-"
        "coordinated to prevent tax base flight. Funds the lab + UBC. "
        "Modeled on OECD Pillar 1/2 minimum tax framework."
    ),
    parameter_changes={
        "ai_sector_tax_rate": 0.05,
        "transfer_funding_per_gdp": 0.008,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.40,
    citation="OECD Pillar 1/2; SOURCES.md addendum",
)

RESKILLING_RETAINED = PolicyLever(
    name="Reskilling at scale (retained from Package B)",
    target=LeverTarget.LABOR,
    description=(
        "Pillar 4 of Package B retained — reskilling passed game-theoretic "
        "robustness test; no reason to redesign."
    ),
    parameter_changes={
        "epsilon_sub_shift": 1.5,
        "skill_mix_complement_shift": 0.05,
        "reskilling_earnings_effect": 0.10,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="SOURCES.md addendum: Card-Kluve-Weber 2018",
)

CERN_AI = PolicyPackage(
    code="C",
    name="CERN-AI Centered",
    description=(
        "Centered on a global public frontier lab (CERN-AI / MAGIC) plus "
        "compute governance treaty. Replaces Pillar 5 (open-weights "
        "mandate) with public open-frontier production — solves the "
        "open-weights inversion. Replaces Pillar 1 (sovereign equity) "
        "with Universal Basic Capital — avoids backward expropriation. "
        "Retains Pillars 4 (reskilling) and a strengthened Pillar 6 "
        "(coordinated AI tax). Adds capability disclosure as treaty-grade "
        "requirement."
    ),
    levers=(
        CERN_AI_PUBLIC_LAB,
        COMPUTE_GOVERNANCE_TREATY,
        TIERED_OPENNESS_FOR_FRONTIER,
        CAPABILITY_DISCLOSURE_AND_EVAL,
        UBC_AT_18_FUNDED_BY_LAB_OUTPUTS,
        AI_TAX_OECD_COORDINATED,
        RESKILLING_RETAINED,
    ),
    activation_year=2026,
    sequencing="sequential",  # treaty + lab take time to stand up
)
