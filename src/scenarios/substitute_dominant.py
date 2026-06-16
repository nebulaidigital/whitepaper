"""Substitute-dominant AI scenario.

Calibrated to the "AI replaces labor at scale" regime where automation
displacement dominates and reinstatement is minimal. Aligned with:
    - SF Consensus / IMF SDN/2026/001 acceleration scenarios
    - Eloundou-Manning-Mishkin-Rock (2023) high-exposure interpretation
    - Worker-bargaining-low regime

Distinguishing features:
- Higher automation rate (dI/dt elevated)
- Lower reinstatement (dN/dt minimal)
- Faster labor share decline
- Substitute-worker employment falls faster
- AI productivity growth at high end of range
- Skill mix shifts further toward substitute-dominant
"""

from src.core import SimulatorConfig

SUBSTITUTE_DOMINANT_CONFIG = SimulatorConfig(
    # Labor share falls faster — 56% → 47% by 2036 (vs 51% default)
    us_labor_share_decay_rate=0.015,
    cn_labor_share_decay_rate=0.013,
    # Top-1% rises faster (capital captures more)
    us_top_1pct_growth_rate=0.013,
    cn_top_1pct_growth_rate=0.007,
    # Markup growth elevated (concentration intensifies under substitution)
    us_markup_growth_rate=0.008,
    cn_markup_growth_rate=0.010,
    # AI productivity high (Goldman base + acceleration)
    ai_productivity_growth=0.035,
    us_gdp_growth_rate=0.028,
    cn_gdp_growth_rate=0.055,
    # Substitute employment crashes
    us_substitute_emp_decay=0.030,
    # Higher capital flight (mobile AI capital relocates to AI-friendly
    # jurisdictions)
    capital_flight_elasticity=0.008,
    # Skill mix is conceptually biased toward substitute (0.15/0.55/0.30)
    # but is captured in the structural production module, not the reduced-
    # form SimulatorConfig. See EMPIRICAL_ANALOGS.md §7.2.
)
