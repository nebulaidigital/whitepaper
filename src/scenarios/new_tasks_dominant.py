"""New-tasks-dominant (GPT-like) scenario.

Calibrated to the "AI as general-purpose technology creating new sectors"
regime — historically analogous to electricity, IT, and the internet.
The reinstatement effect (Acemoglu-Restrepo 2019) dominates: new tasks
created at the labor-intensive end of the production continuum offset
displacement.

Aligned with:
    - Acemoglu-Restrepo (2019) JEP reinstatement framework
    - Aghion-Jones-Jones (2017) AI as growth-engine framing
    - Korinek (2024) Faster Acceleration scenario (productivity-side)
    - Historical analogs: 1920s-1950s electricity sector, 1990s-2020s IT

Distinguishing features:
- Modest automation rate (dI/dt at default)
- Strong reinstatement (dN/dt elevated; new sectors created)
- Labor share recovers as new tasks created
- Highest AI productivity growth
- New industries → labor force expansion + wage gains
- Top-1% concentration moderate (new entrants vs. incumbents)
"""

from src.core import SimulatorConfig

NEW_TASKS_DOMINANT_CONFIG = SimulatorConfig(
    # Labor share modest decline then recovery — 56% → 53% by 2036
    us_labor_share_decay_rate=0.005,
    cn_labor_share_decay_rate=0.005,
    # Top-1% rise moderate (productivity gains shared with new entrants)
    us_top_1pct_growth_rate=0.006,
    cn_top_1pct_growth_rate=0.003,
    # Markup growth moderate (new entrants disperse rents)
    us_markup_growth_rate=0.003,
    cn_markup_growth_rate=0.004,
    # AI productivity highest (GPT effect)
    ai_productivity_growth=0.045,
    us_gdp_growth_rate=0.035,
    cn_gdp_growth_rate=0.055,
    # Substitute employment recovers via new sectors
    us_substitute_emp_decay=0.008,
    # Capital flight moderate
    capital_flight_elasticity=0.004,
    # Skill mix is conceptually balanced (0.22/0.35/0.43) but lives in the
    # structural production module, not the reduced-form SimulatorConfig.
)
