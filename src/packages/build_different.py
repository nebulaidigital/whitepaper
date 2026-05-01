"""Package F: Build-Different-AI (Acemoglu-Johnson).

Targets *what AI is built for* rather than redistributing AI's gains.
Directed R&D for human-complementary AI + procurement preference + worker
codetermination on AI deployment + targeted antitrust.

Theoretical basis:
- Acemoglu (2021) "Harms of AI"
- Acemoglu & Johnson (2023) Power and Progress (Ch 11)
- Mazzucato (2013, 2021) entrepreneurial state / mission economy
- Cherif & Hasanov (2019) industrial policy principles
- Juhász, Lane & Rodrik (2024) new economics of industrial policy

Distinctive feature: this package operates upstream of distribution.
If AI is built as labor complement rather than substitute, the
redistribution problem the other packages address gets smaller.
"""

from src.packages.base import (
    LeverTarget,
    PolicyLever,
    PolicyPackage,
    Reversibility,
)


DIRECTED_RD_FOR_COMPLEMENT_AI = PolicyLever(
    name="Directed R&D for Human-Complementary AI",
    target=LeverTarget.PRODUCTION,
    description=(
        "Public R&D funding ($30B/yr) directed specifically at AI that "
        "augments rather than substitutes for labor. Funding criteria: "
        "demonstrated complement-rather-than-substitute deployment, "
        "explicit human-in-loop architectures, evidence of worker "
        "productivity boost without displacement. NIH/DARPA institutional "
        "model."
    ),
    parameter_changes={
        "labor_augmenting_productivity_growth": 0.015,  # added on top of baseline
        "automation_threshold_growth_dampening": 0.40,
        "skill_mix_complement_shift": 0.10,
        "public_rd_per_gdp": 0.0012,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Acemoglu 2021; Acemoglu & Johnson 2023; Mazzucato 2021",
)

PROCUREMENT_PREFERENCE_NON_DISPLACING = PolicyLever(
    name="Federal Procurement Preference for Non-Displacing AI",
    target=LeverTarget.PRODUCTION,
    description=(
        "US federal procurement (the largest single AI customer) "
        "preferentially purchases AI tools that augment public-sector "
        "workers rather than substitute for them. Procurement criteria "
        "explicitly evaluate worker outcomes. Uses procurement leverage "
        "(~$700B/yr federal spending) to shape what gets built."
    ),
    parameter_changes={
        "ai_market_share_complement_systems": 0.15,  # +15pp shift in share
        "ai_dev_resource_allocation_complement": 0.20,  # private R&D follows
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Mazzucato 2021; Cherif-Hasanov 2019",
)

WORKER_CODETERMINATION_AI_DEPLOYMENT = PolicyLever(
    name="Worker Codetermination on AI Deployment",
    target=LeverTarget.LABOR,
    description=(
        "German Mitbestimmung-style codetermination on AI deployment "
        "decisions in firms above 1,000 employees. Workers have voice on "
        "implementation pace, retraining requirements, displacement "
        "mitigation. Reduces unilateral capital control over deployment "
        "timing — empirically associated with smoother automation "
        "transitions in German manufacturing."
    ),
    parameter_changes={
        "displacement_speed_dampening": 0.30,
        "epsilon_sub_shift": 1.4,  # workers have stronger outside options
        "automation_threshold_growth_dampening": 0.20,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,  # domestic
    citation="German Mitbestimmungsgesetz; Aghion-Antonin-Bunel 2023",
)

TARGETED_ANTITRUST_AI = PolicyLever(
    name="Targeted Antitrust on AI Lab Concentration",
    target=LeverTarget.COMPETITION,
    description=(
        "Active enforcement against AI lab acquisitions, exclusive "
        "deals, and market-power abuse. Less aggressive than Package D's "
        "structural separation; relies on existing Sherman Act § 2 "
        "enforcement with FTC + DOJ resourcing. Modeled on Khan-era FTC "
        "approach."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.25,
        "ai_lab_entry_barrier": -0.15,
        "ai_sector_concentration_shift": -0.10,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Khan 2017; Wu 2018; FTC AI cloud-provider investigations",
)

CARE_INFRASTRUCTURE_PUBLIC_INVESTMENT = PolicyLever(
    name="Public Investment in Human-Only Sectors",
    target=LeverTarget.LABOR,
    description=(
        "Direct expansion of childcare, elder care, mental health, "
        "skilled trades training. Smaller version of Package E's care "
        "economy lever — intended as labor-market shock absorber rather "
        "than primary redistribution. ~1.5% of GDP."
    ),
    parameter_changes={
        "care_sector_employment_share": 0.025,
        "median_wage_floor": 0.05,
        "skill_mix_complement_shift": 0.04,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Acemoglu & Johnson 2023; Folbre care economy literature",
)

BUILD_DIFFERENT = PolicyPackage(
    code="F",
    name="Build-Different-AI (Acemoglu-Johnson)",
    description=(
        "Operates upstream of distribution: shapes what AI is built for "
        "rather than redistributing AI's gains. Directed R&D + procurement "
        "preference + worker codetermination + targeted antitrust + care "
        "infrastructure. Distinctive thesis: if AI is built as labor "
        "complement rather than substitute (per Acemoglu's actual policy "
        "argument), the redistribution problem gets smaller. This is the "
        "intellectual lineage closest to Acemoglu-Restrepo's own "
        "preferred policy program."
    ),
    levers=(
        DIRECTED_RD_FOR_COMPLEMENT_AI,
        PROCUREMENT_PREFERENCE_NON_DISPLACING,
        WORKER_CODETERMINATION_AI_DEPLOYMENT,
        TARGETED_ANTITRUST_AI,
        CARE_INFRASTRUCTURE_PUBLIC_INVESTMENT,
    ),
    activation_year=2026,
    sequencing="simultaneous",
)
