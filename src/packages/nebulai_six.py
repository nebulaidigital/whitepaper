"""Package B: Nebulai Six-Pillar Framework.

The original framework as specified in the Nebulai whitepaper v2 (April 2026).
Six pillars activated simultaneously. This is the package the project is
evaluating, not assuming optimal — it's compared against alternatives in
Hypothesis 9.

Note that Pillars 2 and 3 are placeholders pending whitepaper review;
their parameter changes are stubbed and need refinement once the
whitepaper text is parsed.
"""

from src.packages.base import (
    LeverTarget,
    PolicyLever,
    PolicyPackage,
    Reversibility,
)


PILLAR_1_SOVEREIGN_EQUITY = PolicyLever(
    name="Pillar 1: Sovereign Equity Acquisition (10%)",
    target=LeverTarget.CAPITAL,
    description=(
        "Public fund acquires fraction of new top-decile AI capital at "
        "annual rate; pays distributed dividend. Modeled on Norway GPFG + "
        "Alaska Permanent Fund."
    ),
    parameter_changes={
        "sovereign_acquisition_fraction": 0.10,
        "cost_of_equity_premium": 0.005,  # 50bps per 10% acquisition
        "dividend_rate": 0.04,  # of acquired AUM
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    coalition_threshold=0.0,
    citation="SOURCES.md §Capital markets; Sundaresan-Sushko 2014; Norway GPFG impact studies",
)

PILLAR_2_PLACEHOLDER = PolicyLever(
    name="Pillar 2: [Placeholder pending whitepaper parse]",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Pillar 2 specification deferred — whitepaper parse needed. "
        "Likely candidate: governance/coordination architecture."
    ),
    parameter_changes={},
    reversibility=Reversibility.SEMI_REVERSIBLE,
    citation="paper/draft/ — pending review",
)

PILLAR_3_PLACEHOLDER = PolicyLever(
    name="Pillar 3: [Placeholder pending whitepaper parse]",
    target=LeverTarget.GOVERNANCE,
    description=(
        "Pillar 3 specification deferred — whitepaper parse needed. "
        "Likely candidate: international coordination layer."
    ),
    parameter_changes={},
    reversibility=Reversibility.SEMI_REVERSIBLE,
    citation="paper/draft/ — pending review",
)

PILLAR_4_RESKILLING = PolicyLever(
    name="Pillar 4: Reskilling at scale",
    target=LeverTarget.LABOR,
    description=(
        "Active labor market program for displaced substitute workers. "
        "Calibrated to high end of Card-Kluve-Weber 2018 effect range; "
        "shifts substitute-worker monopsony elasticity ε_sub upward "
        "(better outside options); shifts effective skill mix toward "
        "complement category."
    ),
    parameter_changes={
        "epsilon_sub_shift": 1.5,  # outside-option improvement
        "skill_mix_complement_shift": 0.05,  # 5pp shift sub→complement
        "reskilling_earnings_effect": 0.10,  # 10% earnings boost (mid CKW)
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    coalition_threshold=0.0,
    citation="SOURCES.md addendum: Card-Kluve-Weber 2018; Heckman-LaLonde-Smith 1999",
)

PILLAR_5_OPEN_WEIGHTS = PolicyLever(
    name="Pillar 5: Open-weights mandate",
    target=LeverTarget.COMPETITION,
    description=(
        "Mandate open release of frontier model weights for participating "
        "jurisdictions. Intended mechanism: dampen markup growth in AI "
        "sector. NOTE: Hypothesis 1 tests whether this mechanism operates "
        "in Q1 2026 conditions (post-DeepSeek open-weights inversion)."
    ),
    parameter_changes={
        "ai_markup_growth_dampening": 0.40,
        "ai_sector_concentration_shift": -0.05,
    },
    reversibility=Reversibility.IRREVERSIBLE,  # released weights cannot be retracted
    requires_coordination=True,  # unilateral version creates open-weights inversion
    coalition_threshold=0.50,
    citation="SOURCES.md §Firm markup distribution; SOURCES.md addendum: Bommasani 2024, Kapoor 2024",
)

PILLAR_6_AI_TAX = PolicyLever(
    name="Pillar 6: AI tax (3% of AI revenue)",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "Tax on AI sector value-added; revenue funds Pillar 4 reskilling "
        "and direct transfers. Modeled on OECD Pillar 1/2 digital services "
        "tax mechanics."
    ),
    parameter_changes={
        "ai_sector_tax_rate": 0.03,
        "transfer_funding_per_gdp": 0.005,  # ~0.5% of GDP at AI sector ~17% VA
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,  # tax base flight without OECD coordination
    coalition_threshold=0.40,
    citation="SOURCES.md addendum: OECD digital tax incidence studies",
)

NEBULAI_SIX = PolicyPackage(
    code="B",
    name="Nebulai Six-Pillar Framework",
    description=(
        "The original framework as proposed in the Nebulai whitepaper v2. "
        "Six pillars activated simultaneously starting 2026. Evaluated "
        "against alternative packages C–G in Hypothesis 9. NOTE: Pillars 2 "
        "and 3 are placeholders pending parse of whitepaper draft."
    ),
    levers=(
        PILLAR_1_SOVEREIGN_EQUITY,
        PILLAR_2_PLACEHOLDER,
        PILLAR_3_PLACEHOLDER,
        PILLAR_4_RESKILLING,
        PILLAR_5_OPEN_WEIGHTS,
        PILLAR_6_AI_TAX,
    ),
    activation_year=2026,
    sequencing="simultaneous",
)


# Alternate sequencing variant for Hypothesis 2 test.
NEBULAI_SIX_SEQUENTIAL = PolicyPackage(
    code="B",
    name="Nebulai Six-Pillar Framework (Sequential)",
    description=(
        "Same six pillars as NEBULAI_SIX but sequenced by reversibility: "
        "Pillars 4 + 6 (reversible) at year 0; Pillar 1 (semi-reversible) "
        "at year 3 conditional on Pillar 4 leading indicator hit; Pillar 5 "
        "(irreversible) at year 6 conditional on Pillar 1 leading "
        "indicator hit. Pillars 2 and 3 placeholder activation at year 0."
    ),
    levers=(
        PILLAR_1_SOVEREIGN_EQUITY,
        PILLAR_2_PLACEHOLDER,
        PILLAR_3_PLACEHOLDER,
        PILLAR_4_RESKILLING,
        PILLAR_5_OPEN_WEIGHTS,
        PILLAR_6_AI_TAX,
    ),
    activation_year=2026,
    sequencing="sequential",
)
