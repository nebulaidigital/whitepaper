"""Complement-dominant AI scenario.

Calibrated to the "AI augments labor" regime where complementarity
dominates and AI raises worker productivity rather than displacing it.
Aligned with:
    - Brynjolfsson-Li-Raymond (2023) low-skill complement evidence
    - Pizzinelli IMF 2024 high-complementarity-fraction interpretation
    - Acemoglu-Johnson (2023) directed-AI program
    - Korinek (2024) Faster Growth (not Acceleration) scenario

Distinguishing features:
- Lower automation rate (dI/dt subdued)
- Higher reinstatement (dN/dt elevated via complement task creation)
- Labor share more stable
- AI productivity contributes via labor-augmenting channel
- Skill mix shifts further toward complement
- Wage gains for substitute workers via AI tools
"""

from src.core import SimulatorConfig

COMPLEMENT_DOMINANT_CONFIG = SimulatorConfig(
    # Labor share more stable — 56% → 54% by 2036 (vs 51% default)
    us_labor_share_decay_rate=0.003,
    cn_labor_share_decay_rate=0.004,
    # Top-1% rises but more slowly (productivity captured more broadly)
    us_top_1pct_growth_rate=0.005,
    cn_top_1pct_growth_rate=0.002,
    # Markup growth dampened (broad productivity disperses rents)
    us_markup_growth_rate=0.002,
    cn_markup_growth_rate=0.003,
    # AI productivity at upper end (Cazzaniga high)
    ai_productivity_growth=0.030,
    us_gdp_growth_rate=0.028,
    cn_gdp_growth_rate=0.050,
    # Substitute employment stable to growing (workers augmented by AI)
    us_substitute_emp_decay=0.005,
    # Lower capital flight (productive capital stays domestic)
    capital_flight_elasticity=0.003,
    # Skill mix is conceptually biased toward complement (0.18/0.30/0.52,
    # Pizzinelli high-complementarity calibration) but lives in the structural
    # production module, not the reduced-form SimulatorConfig.
)
