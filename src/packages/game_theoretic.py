"""Package G: Game-Theoretic-Derived.

Eight pillars derived by reverse-engineering "what set of policies passes
all five game-theoretic constraints across all relevant actors":

1. Individual rationality (every actor)
2. Coalition stability
3. Incentive compatibility
4. Verifiability / enforceability
5. Time consistency

This package is the direct test of Hypothesis 10 — does game-theoretic
robustness produce a better policy package than the framework's
chat-derived six pillars?

Theoretical basis:
- Ostrom (1990) eight design principles for commons governance
- Schelling (1960) focal-point coordination
- Olson (1965) collective action theory
- Maskin (2008) mechanism design
- Acemoglu & Robinson (2019) institutional dynamics
- Tirole (2017) public goods and incentives

Pillar selection logic:
- Each pillar passes all five game-theoretic constraints
- Each pillar's mechanism is verifiable
- Coalition formation is feasible at the specified threshold
- Time consistency: enacted pillars resist political reversal
- The package as a whole is incentive-compatible across major actors

Differences from Package B (Nebulai original):
- Pillar 1 (sovereign equity) → REPLACED with Universal Basic Capital
  (avoids individual-rationality failure for capital owners)
- Pillar 5 (open weights mandate) → REPLACED with compute governance treaty
  (open weights fails verifiability + has open-weights inversion problem)
- Adds: capability disclosure, AI liability, structural separation
"""

from src.packages.base import (
    LeverTarget,
    PolicyLever,
    PolicyPackage,
    Reversibility,
)


GT_COMPUTE_GOVERNANCE = PolicyLever(
    name="Compute Governance Treaty (Verifiable)",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Multilateral treaty on compute monitoring, capability thresholds, "
        "and reciprocal restriction. Passes all five constraints: (1) "
        "individual rationality — both US and China benefit from "
        "preventing third-party catastrophic AI; (2) coalition — US + EU "
        "+ JP + KR + TW controls supply chain; (3) incentive-compatible "
        "— defection detected via fab/power monitoring; (4) verifiable; "
        "(5) time-consistent — modeled on NPT durability."
    ),
    parameter_changes={
        "ai_arms_race_intensity": -0.30,
        "geopolitical_stability_index": 8.0,
        "frontier_compute_concentration": -0.10,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.50,
    citation="Sastry et al. 2024; NPT historical analog; Heim et al. 2024",
)

GT_CERN_AI_PUBLIC_LAB = PolicyLever(
    name="CERN-AI Global Public Frontier Lab",
    target=LeverTarget.COMPETITION,
    description=(
        "Solves open-weights inversion at the source. Passes constraints: "
        "(1) participants gain access to public capability they couldn't "
        "afford alone; (2) coalition starts at 30% of frontier compute "
        "and grows; (3) outputs are public — no defection through "
        "non-disclosure; (4) verifiable via open weights; (5) durable — "
        "scientific institutions are sticky."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.55,
        "ai_sector_concentration_shift": -0.15,
        "frontier_capability_diffusion": 0.20,
        "public_funding_per_gdp": 0.0015,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.30,
    citation="Hausenloy et al. 2023; Bengio et al. 2024",
)

GT_CAPABILITY_DISCLOSURE = PolicyLever(
    name="Mandatory Capability Disclosure + Pre-Deployment Eval",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Frontier training runs above compute threshold register with "
        "AISI Network. Passes constraints: (1) compliance cost low "
        "relative to capability gain from peer evals; (2) coalition "
        "already exists (~40% of frontier compute); (3) hard to defect "
        "publicly without market exclusion; (4) inspections verifiable; "
        "(5) builds on Bletchley → Seoul → Paris precedent durability."
    ),
    parameter_changes={
        "capability_disclosure_compliance": 0.85,
        "ai_safety_audit_coverage": 0.80,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.40,
    citation="International AI Safety Report 2025; Bengio et al. 2024",
)

GT_STRUCTURAL_SEPARATION = PolicyLever(
    name="Antitrust Structural Separation",
    target=LeverTarget.COMPETITION,
    description=(
        "Model labs ≠ cloud providers ≠ application layers. Passes "
        "constraints: (1) downstream users gain; concentrated cost on "
        "~5 firms; (2) domestic — no coalition needed; (3) corporate "
        "structure observable, defection via remerger requires antitrust "
        "waiver; (4) verifiable; (5) once enacted, reconstitution is "
        "politically costly."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.45,
        "ai_sector_concentration_shift": -0.20,
        "compute_layer_profit_share_cap": 0.15,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation="Khan 2017; Hovenkamp 2021; AT&T 1982 analog",
)

GT_AI_LIABILITY = PolicyLever(
    name="AI Liability + Mandatory Insurance Regime",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Self-enforcing through markets. Passes constraints: (1) "
        "insurance internalizes risk, market-compatible; (2) domestic — "
        "no coalition needed; (3) uninsured deployment economically "
        "irrational, no incentive to defect; (4) insurance contracts "
        "auditable; (5) durable via existing tort/insurance "
        "infrastructure."
    ),
    parameter_changes={
        "deployment_risk_pricing": 1.0,
        "ai_misuse_externality_internalization": 0.60,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Bengio et al. 2024; nuclear/environmental liability analogs",
)

GT_UNIVERSAL_BASIC_CAPITAL = PolicyLever(
    name="Universal Basic Capital (replaces Pillar 1)",
    target=LeverTarget.HOUSEHOLDS,
    description=(
        "Capital grant at age 18. Passes constraints where Pillar 1 "
        "fails: (1) individual rationality — distributes ownership "
        "*forward* from each citizen's birth, no backward expropriation "
        "of existing owners; (2) coalition — bottom 80% of voters benefit "
        "= electorally decisive; (3) flat structure no incentive to "
        "cheat; (4) administered transfer, verifiable; (5) Alaska / "
        "Social Security demonstrate political durability of universal "
        "transfers."
    ),
    parameter_changes={
        "ubc_grant_per_capita": 50000.0,
        "wealth_distribution_floor": 0.012,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation="Atkinson 2015; Sherraden 1991; Alaska PFD historical analog",
)

GT_AI_TAX_OECD = PolicyLever(
    name="AI Tax (OECD-Coordinated, 5–8%)",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "Tax on AI sector value-added; OECD-coordinated to prevent base "
        "flight. Passes constraints: (1) revenue funds transfers that "
        "median voter benefits from; (2) OECD coordination mechanism "
        "exists; (3) revenue auditable; (4) verifiable; (5) reversible "
        "but politically lock-in moderate."
    ),
    parameter_changes={
        "ai_sector_tax_rate": 0.06,  # midpoint of 5–8%
        "transfer_funding_per_gdp": 0.010,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.40,
    citation="OECD Pillar 1/2 framework; SOURCES.md addendum",
)

GT_RESKILLING_RETAINED = PolicyLever(
    name="Reskilling at scale (retained — passes test)",
    target=LeverTarget.LABOR,
    description=(
        "Pillar 4 of Package B retained — passes all five constraints "
        "as originally specified. No redesign needed."
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

GAME_THEORETIC = PolicyPackage(
    code="G",
    name="Game-Theoretic-Derived Eight Pillars",
    description=(
        "Pillars derived by passing each through five constraints: "
        "individual rationality, coalition stability, incentive "
        "compatibility, verifiability, time consistency. Replaces "
        "Pillar 1 (sovereign equity) of Package B with UBC (avoids "
        "individual-rationality failure). Replaces Pillar 5 (open weights "
        "mandate) with compute governance + CERN-AI (avoids verifiability "
        "and open-weights inversion failures). Adds capability disclosure, "
        "AI liability, structural separation. Tested in Hypothesis 10 "
        "against Package B for stability under defection, coalition "
        "variation, and time-consistency stress."
    ),
    levers=(
        GT_COMPUTE_GOVERNANCE,
        GT_CERN_AI_PUBLIC_LAB,
        GT_CAPABILITY_DISCLOSURE,
        GT_STRUCTURAL_SEPARATION,
        GT_AI_LIABILITY,
        GT_UNIVERSAL_BASIC_CAPITAL,
        GT_AI_TAX_OECD,
        GT_RESKILLING_RETAINED,
    ),
    activation_year=2026,
    sequencing="sequential",  # treaties + lab take time to stand up
)
