"""Package E: Direct Redistribution.

UBI + wealth tax + Universal Basic Capital + care-economy expansion.
Skips capital-ownership mechanics; redistributes outcomes directly.
Politically harder to enact than partial measures, but lock-in is strong
once enacted (Alaska Permanent Fund, Social Security demonstrate this).

Theoretical basis:
- Atkinson (2015) capital endowment proposal
- Sherraden (1991) Assets and the Poor
- Saez & Zucman (2019) wealth tax design
- Korinek & Juelfs (2023) on UBI under transformative AI
- Van Parijs & Vanderborght (2017) basic income foundation
"""

from src.packages.base import (
    LeverTarget,
    PolicyLever,
    PolicyPackage,
    Reversibility,
)


UBI = PolicyLever(
    name="Universal Basic Income",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "Unconditional cash transfer of $1,200/month to all adults. "
        "Funded by AI tax + wealth tax + capital gains reform. Replaces "
        "fragmented means-tested programs. Calibrated to Y Combinator "
        "OpenResearch UBI study + Stockton SEED + Kenya GiveDirectly "
        "long-term."
    ),
    parameter_changes={
        "ubi_monthly_per_adult": 1200.0,
        "transfer_funding_per_gdp": 0.060,  # 6% of GDP — substantial
        # v2.0: OpenResearch UBI final results (3-year RCT, late 2024)
        # found ~4% labor supply reduction (1.3 hours/week of 33h avg)
        # — narrower confidence interval than Marinescu 2018 range.
        # See EMPIRICAL_ANALOGS.md §7.6.
        "labor_supply_elasticity": -0.04,
        "monopsony_outside_option_strength": 1.3,
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,  # politically locked once enacted
    requires_coordination=False,
    citation="EMPIRICAL_ANALOGS.md §7.6 (v2.0); OpenResearch UBI Study 2024 final + Marinescu 2018",
)

WEALTH_TAX_PROGRESSIVE = PolicyLever(
    name="Progressive Wealth Tax",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "2% on net wealth above $50M, 3% above $1B (Saez-Zucman 2019 "
        "design). Targets the stock side, not flows. Calibrated to "
        "produce ~1.5% of GDP in revenue at announced rates."
    ),
    parameter_changes={
        "wealth_tax_marginal_top": 0.03,
        "transfer_funding_per_gdp": 0.015,
        "capital_flight_responsiveness": 0.005,  # additional flight pressure
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=True,  # high-end mobility requires OECD coord
    coalition_threshold=0.40,
    citation="Saez-Zucman 2019; Bach et al. 2014",
)

UNIVERSAL_BASIC_CAPITAL = PolicyLever(
    name="Universal Basic Capital (Atkinson 2015)",
    target=LeverTarget.HOUSEHOLDS,
    description=(
        "$50K capital grant to every citizen at age 18. Distributed via "
        "sovereign-managed portfolio with 5-year vesting, then subject "
        "to recipient discretion. Atkinson 2015 design."
    ),
    parameter_changes={
        "ubc_grant_per_capita": 50000.0,
        "wealth_distribution_floor": 0.012,  # 1.2pp gain to bottom 50%
    },
    reversibility=Reversibility.SEMI_REVERSIBLE,
    requires_coordination=False,
    citation="Atkinson 2015; Sherraden 1991",
)

CARE_ECONOMY_EXPANSION = PolicyLever(
    name="Care Economy Expansion",
    target=LeverTarget.LABOR,
    description=(
        "Direct public funding to grow childcare, elder care, mental "
        "health, and education sectors — mathematically the AI-complement "
        "labor market. Wage floors above current sector medians; training "
        "pipelines; subsidized provider entry. ~3% of GDP investment."
    ),
    parameter_changes={
        "care_sector_employment_share": 0.05,  # +5pp of employment
        "median_wage_floor": 0.10,  # 10% increase in care-sector wages
        "skill_mix_complement_shift": 0.08,  # 8pp shift from sub→complement
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,
    citation="Acemoglu & Johnson 2023 *Power and Progress*; Folbre on care economy",
)

INHERITANCE_TAX_REFORM = PolicyLever(
    name="Inheritance / Estate Tax Reform",
    target=LeverTarget.REDISTRIBUTION,
    description=(
        "Tighten inheritance tax: 50% above $5M, 70% above $50M. Eliminate "
        "step-up basis at death. Targets the inheritance flow that "
        "preserves top-decile concentration across generations (Piketty-"
        "Postel-Vinay-Rosenthal 2014)."
    ),
    parameter_changes={
        "inheritance_top_decile_recirculation": -0.40,  # 40% reduction in flow
        "transfer_funding_per_gdp": 0.005,
    },
    reversibility=Reversibility.REVERSIBLE,
    requires_coordination=False,  # mostly domestic, some cross-border
    citation="Piketty-Postel-Vinay-Rosenthal 2014; Saez-Zucman 2019",
)

DIRECT_REDISTRIBUTION = PolicyPackage(
    code="E",
    name="Direct Redistribution Package",
    description=(
        "Skips capital-ownership mechanics and AI-sector-specific "
        "interventions. Pure redistribution: UBI + wealth tax + Universal "
        "Basic Capital + care-economy expansion + inheritance tax reform. "
        "Politically hardest to enact but strongest lock-in once enacted. "
        "Important counterfactual: shows what AI policy looks like when "
        "you treat AI as just-another-shock and respond with general "
        "redistribution, vs. AI-specific mechanisms."
    ),
    levers=(
        UBI,
        WEALTH_TAX_PROGRESSIVE,
        UNIVERSAL_BASIC_CAPITAL,
        CARE_ECONOMY_EXPANSION,
        INHERITANCE_TAX_REFORM,
    ),
    activation_year=2026,
    sequencing="simultaneous",
)
