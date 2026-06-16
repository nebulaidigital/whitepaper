"""AI economic transition scenarios.

The simulator's default calibration represents a Q1 2026 best-estimate
trajectory. The Acemoglu-Restrepo task-based framework distinguishes three
fundamentally different AI development regimes:

    1. Substitute-dominant: AI replaces labor at scale (automation
       displacement dominates; reinstatement minimal). Most aligned with
       SF Consensus scenarios.

    2. Complement-dominant: AI augments labor (productivity boost without
       proportionate displacement). Most aligned with Brynjolfsson-Li-Raymond
       (2023) firm-level evidence; Pizzinelli IMF 2024 complementarity
       fraction.

    3. New-tasks-dominant: AI as general-purpose technology that creates
       new sectors (analogous to electricity, IT, internet). Reinstatement
       effect dominates.

A PhD-level critique correctly objected that the default simulation
under-develops the productivity upside by blending these regimes. This
module exposes them as explicit alternative SimulatorConfig values so
policy comparisons can be run under each regime separately.

References:
    Acemoglu & Restrepo (2019) JEP — three effects taxonomy
    Acemoglu & Restrepo (2022) Econometrica — displacement vs reinstatement
    Brynjolfsson, Li & Raymond (2023) NBER WP 31161 — complement evidence
    Korinek (2024) NBER WP 32549 — scenario taxonomy
"""

from src.scenarios.substitute_dominant import SUBSTITUTE_DOMINANT_CONFIG
from src.scenarios.complement_dominant import COMPLEMENT_DOMINANT_CONFIG
from src.scenarios.new_tasks_dominant import NEW_TASKS_DOMINANT_CONFIG

ALL_SCENARIOS = {
    "substitute": SUBSTITUTE_DOMINANT_CONFIG,
    "complement": COMPLEMENT_DOMINANT_CONFIG,
    "new_tasks": NEW_TASKS_DOMINANT_CONFIG,
}

__all__ = [
    "SUBSTITUTE_DOMINANT_CONFIG",
    "COMPLEMENT_DOMINANT_CONFIG",
    "NEW_TASKS_DOMINANT_CONFIG",
    "ALL_SCENARIOS",
]
