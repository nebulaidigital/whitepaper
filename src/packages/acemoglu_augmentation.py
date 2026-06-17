"""Acemoglu-Augmentation Maximum — Pre-Distribution Architecture.

Operationalizes the Acemoglu-Johnson (2023) "redirect technology toward
human complementarity" framework at maximum intensity. The core thesis:
the fundamental policy question is not how to redistribute AI gains
after automation; it is how to incentivize firms to build augmentation
AI rather than replacement AI in the first place.

The standard packages in this simulation focus on REDISTRIBUTION
mechanisms (UBI, UBC, sovereign equity, AI tax — Packages E, H, N, P).
Package F (Build-Different-AI) was the framework's only pre-distribution
package but was specified at modest intensity and consequently
under-performs in the empirical comparison.

This package — Acemoglu-Augmentation Maximum (code "M") — implements
the Acemoglu-Johnson framework at maximum intensity to test the strong
version of the pre-distribution claim:

    If incentives shift so that firms predominantly build complement-AI
    rather than substitute-AI, the redistribution problem becomes
    substantially smaller because labor share doesn't fall, median
    wages rise, and inequality moderates endogenously.

The empirical question this package answers: does aggressive
pre-distribution dominate aggressive redistribution on welfare metrics?
If yes, the paper's central focus needs to shift toward Acemoglu-
Johnson. If no, the redistribution-heavy framing is empirically
defensible despite the theoretical critique.

References:
- Acemoglu, D. & Johnson, S. (2023) "Power and Progress: Our
  Thousand-Year Struggle Over Technology and Prosperity," PublicAffairs.
  Chapter 11 specifically on AI.
- Acemoglu, D. (2021) "Harms of AI," NBER Working Paper 29247.
- Acemoglu, D. & Restrepo, P. (2018, 2019, 2022) task-based framework.
- Brynjolfsson, E., Li, D. & Raymond, L. (2023) "Generative AI at
  Work," NBER Working Paper 31161 — empirical support showing AI
  benefits low-skilled workers most when used as augmentation.
- Thompson, N. et al. (2024) on partial automation being economically
  optimal because near-perfect AI is disproportionately expensive.
- Klinova, K. & Korinek, A. (2021) "AI and Shared Prosperity,"
  on per-deployment evaluation framework.
"""

from src.packages.base import (
    LeverTarget,
    PolicyLever,
    PolicyPackage,
    Reversibility,
)


PILLAR_M1_DIFFERENTIAL_TAX_INCENTIVES = PolicyLever(
    name="M-1 Differential Tax Incentives (penalize replacement, reward augmentation)",
    target=LeverTarget.PRODUCTION,
    description=(
        "Acemoglu-Johnson central proposal: differential tax treatment of "
        "AI capital depending on whether it replaces or augments labor. "
        "Mechanisms: (1) End accelerated depreciation for capital that "
        "replaces labor; (2) R&D credits restricted to human-complementary "
        "AI; (3) Payroll tax credits for firms whose AI deployment raises "
        "rather than reduces headcount or hours. Operates at firm-level "
        "incentive structure, not at deployment-time intervention."
    ),
    parameter_changes={
        "labor_augmenting_productivity_growth": 0.025,  # high end
        "automation_threshold_growth_dampening": 0.60,  # very high
        "skill_mix_complement_shift": 0.15,
        "public_rd_per_gdp": 0.0015,
        "ai_market_share_complement_systems": 0.30,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation="Acemoglu & Johnson 2023 Power and Progress Ch. 11",
)


PILLAR_M2_PROCUREMENT_AUGMENTATION_ONLY = PolicyLever(
    name="M-2 Federal Procurement Restricted to Augmentation AI",
    target=LeverTarget.PRODUCTION,
    description=(
        "$700B/yr federal procurement leverage exclusively for "
        "augmentation AI (defined per Klinova-Korinek shared prosperity "
        "criteria: jobs displaced ≤ jobs created; wages preserved or "
        "rising; worker autonomy preserved). Largest single AI demand "
        "lever in the US economy redirected entirely toward complementarity. "
        "Private R&D follows procurement direction within 2-3 years."
    ),
    parameter_changes={
        "ai_market_share_complement_systems": 0.30,
        "ai_dev_resource_allocation_complement": 0.40,
        "skill_mix_complement_shift": 0.10,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Klinova & Korinek 2021 Shared Prosperity; Mazzucato 2021",
)


PILLAR_M3_MANDATORY_CODETERMINATION_ALL_FIRMS = PolicyLever(
    name="M-3 Mandatory Worker Codetermination on AI Deployment (all firms)",
    target=LeverTarget.LABOR,
    description=(
        "German Mitbestimmungsgesetz model extended to ALL firms above "
        "100 employees (not just 1,000+ as in standard German law). "
        "Workers have formal voice in AI deployment decisions, "
        "implementation pace, retraining requirements, displacement "
        "mitigation. Reduces unilateral capital control over deployment "
        "timing. Empirically associated with smoother automation "
        "transitions (Jäger-Schoefer 2021)."
    ),
    parameter_changes={
        "displacement_speed_dampening": 0.50,
        "epsilon_sub_shift": 1.8,
        "skill_mix_complement_shift": 0.06,
        "automation_threshold_growth_dampening": 0.30,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation="Jäger-Schoefer 2021 QJE; Aghion-Antonin-Bunel 2023",
)


PILLAR_M4_KLINOVA_KORINEK_EVALUATOR = PolicyLever(
    name="M-4 Mandatory Shared-Prosperity Evaluation Per AI Deployment",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Every AI deployment above capability threshold must undergo "
        "Klinova-Korinek shared prosperity evaluation BEFORE deployment: "
        "(1) jobs displaced, (2) jobs created, (3) wages affected, "
        "(4) productivity gains, (5) distributional incidence. Net-"
        "destructive deployments face additional regulatory hurdles "
        "(transition fund contribution, retraining mandate). Net-"
        "creative deployments fast-tracked. Operationalizes Klinova-"
        "Korinek (2021) framework into mandatory regulatory standard."
    ),
    parameter_changes={
        "capability_disclosure_compliance": 0.92,
        "ai_safety_audit_coverage": 0.85,
        "displacement_speed_dampening": 0.25,
        "ai_market_share_complement_systems": 0.15,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.40,
    citation="Klinova & Korinek 2021 Partnership on AI shared prosperity",
)


PILLAR_M5_ANTITRUST_AGAINST_AUTOMATION_LOCK_IN = PolicyLever(
    name="M-5 Antitrust Against Automation Lock-In",
    target=LeverTarget.COMPETITION,
    description=(
        "Antitrust enforcement specifically targeting firms whose "
        "automation strategy locks customers into labor-replacing AI "
        "platforms. Distinct from standard concentration-based antitrust: "
        "examines downstream effects on labor markets, not just consumer "
        "prices. Khan-Wu-Hovenkamp Brandeisian interpretation extended "
        "to labor-market harms."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.40,
        "ai_sector_concentration_shift": -0.18,
        "ai_lab_entry_barrier": -0.15,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation="Khan 2017, Wu 2018; extended to labor-market harm framework",
)


PILLAR_M6_PUBLIC_RD_COMPLEMENTARITY_ONLY = PolicyLever(
    name="M-6 Public R&D Directed Exclusively to Complementarity Research",
    target=LeverTarget.PRODUCTION,
    description=(
        "Public R&D ($50B/yr — larger than NIH AI budget) directed "
        "exclusively to AI systems that augment human work. NSF NAIRR + "
        "DARPA + IARPA budgets redirected. Output metric: papers and "
        "systems that empirically demonstrate worker complementarity, "
        "per Brynjolfsson-Li-Raymond research design."
    ),
    parameter_changes={
        "labor_augmenting_productivity_growth": 0.020,
        "skill_mix_complement_shift": 0.10,
        "public_rd_per_gdp": 0.0025,
        "ai_market_share_complement_systems": 0.20,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Brynjolfsson-Li-Raymond 2023; Mazzucato Mission Economy",
)


PILLAR_M7_REINSTATEMENT_BOUNTY_PROGRAM = PolicyLever(
    name="M-7 Reinstatement Bounty Program (rewards for new-task creation)",
    target=LeverTarget.PRODUCTION,
    description=(
        "Direct payments to firms that demonstrate creation of new "
        "high-wage tasks. Operationalizes Acemoglu-Restrepo reinstatement "
        "effect into policy: pay firms when AI deployment results in "
        "net new high-wage jobs, not just productivity gains for existing "
        "workers. Calibrated such that bounty exceeds tax savings from "
        "labor replacement."
    ),
    parameter_changes={
        "labor_augmenting_productivity_growth": 0.015,
        "skill_mix_complement_shift": 0.08,
        "automation_threshold_growth_dampening": 0.20,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Acemoglu-Restrepo 2019 reinstatement effect; novel policy operationalization",
)


PILLAR_M8_MODEST_REDISTRIBUTION_BACKSTOP = PolicyLever(
    name="M-8 Modest Redistribution Backstop (UBC only, smaller AI tax)",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "Acemoglu position: aggressive pre-distribution reduces but does "
        "not eliminate need for some redistribution. This pillar provides "
        "a backstop: UBC at $25K + modest AI tax at 3% (well below "
        "revenue-maximizing rate). Notable absence: no UBI. The Acemoglu-"
        "Johnson thesis is that if direction shifts adequately, UBI "
        "should be unnecessary."
    ),
    parameter_changes={
        "ubc_grant_per_capita": 25000.0,
        "ai_sector_tax_rate": 0.03,
        "transfer_funding_per_gdp": 0.008,
        "wealth_distribution_floor": 0.006,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,
    coalition_threshold=0.30,
    citation="Acemoglu position on minimal redistribution if pre-distribution succeeds",
)


PILLAR_M9_LABOR_INSTITUTION_STRENGTHENING = PolicyLever(
    name="M-9 Labor Institution Strengthening (sectoral bargaining + works councils)",
    target=LeverTarget.LABOR,
    description=(
        "Beyond codetermination at firm level: sectoral bargaining "
        "(Scandinavian / German Tarifvertrag model) for entire industries "
        "where AI displacement is concentrated. Works councils with formal "
        "AI-deployment review authority. Stansbury-Summers (2020) attribute "
        "majority of post-1980 labor share decline to worker bargaining "
        "decline; this lever directly addresses that channel."
    ),
    parameter_changes={
        "epsilon_sub_shift": 2.0,
        "skill_mix_complement_shift": 0.05,
        "displacement_speed_dampening": 0.40,
        "median_wage_floor": 0.10,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation="Stansbury-Summers 2020 declining worker power; German Tarifvertrag",
)


ACEMOGLU_AUGMENTATION = PolicyPackage(
    code="M",  # M for "Maximum augmentation" / Acemoglu-Johnson
    name="Acemoglu-Augmentation Maximum (Pre-Distribution Architecture)",
    description=(
        "Operationalizes Acemoglu-Johnson (2023) Power and Progress "
        "framework at maximum intensity. Central thesis: change the "
        "direction of AI innovation BEFORE automation occurs, rather "
        "than redistribute gains AFTER. Nine pillars target firm-level "
        "incentives (differential taxation, procurement, codetermination, "
        "shared-prosperity evaluation), institutional structure "
        "(antitrust, labor institutions), and public R&D direction. "
        "Modest redistribution backstop (UBC only, no UBI). Tests the "
        "strong claim: if pre-distribution works, redistribution-heavy "
        "frameworks like Package P are unnecessary."
    ),
    levers=(
        PILLAR_M1_DIFFERENTIAL_TAX_INCENTIVES,
        PILLAR_M2_PROCUREMENT_AUGMENTATION_ONLY,
        PILLAR_M3_MANDATORY_CODETERMINATION_ALL_FIRMS,
        PILLAR_M4_KLINOVA_KORINEK_EVALUATOR,
        PILLAR_M5_ANTITRUST_AGAINST_AUTOMATION_LOCK_IN,
        PILLAR_M6_PUBLIC_RD_COMPLEMENTARITY_ONLY,
        PILLAR_M7_REINSTATEMENT_BOUNTY_PROGRAM,
        PILLAR_M8_MODEST_REDISTRIBUTION_BACKSTOP,
        PILLAR_M9_LABOR_INSTITUTION_STRENGTHENING,
    ),
    activation_year=2026,
    sequencing="sequential",
)
