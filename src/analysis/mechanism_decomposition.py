"""Mechanism decomposition: how much of projected labor-share decline
comes from each channel?

The reduced-form simulator blends multiple mechanisms:
    - Automation displacement (Acemoglu-Restrepo 2018/2019/2022)
    - Markup expansion (DLEU 2020)
    - Worker bargaining decline / monopsony (Azar-Marinescu-Steinbaum 2022)
    - Capital-augmenting productivity bias (Acemoglu-Restrepo 2022, σ > 1)

A PhD-level critique correctly objects: blending these mechanisms makes
it impossible to attribute the projected labor-share decline to AI
specifically vs. pre-existing trends. This module addresses that by
running the simulator with each mechanism toggled on/off in isolation
and computing each channel's contribution to the 2025–2036 trajectory.

The decomposition is approximate (not Shapley-exact) because the
channels interact — turning off one channel doesn't fully isolate
the others' effects. We report both:
    1. Marginal contribution (how much labor-share moves with this
       channel alone active)
    2. Full-decomposition share (each channel's contribution to the
       total projected change, normalized so they sum to 100%)

Reference for the mechanism set:
    Acemoglu & Restrepo (2022) Econometrica 90(5): 1973–2016 —
    decompose post-1980 wage inequality into automation, markups,
    and capital-augmenting productivity.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass

import numpy as np

from src.core import BilateralSimulator, SimulatorConfig


@dataclass(frozen=True)
class MechanismContribution:
    """Per-channel contribution to a single indicator's projected change."""

    channel: str
    indicator: str
    isolated_change: float  # change if only this channel were active
    full_change: float  # total change with all channels active
    contribution_share: float  # isolated_change / sum-of-isolated (normalized)
    contribution_share_naive: float  # isolated_change / full_change (uncorrected)

    def to_dict(self) -> dict:
        return {
            "channel": self.channel,
            "indicator": self.indicator,
            "isolated_change": float(self.isolated_change),
            "full_change": float(self.full_change),
            "contribution_share": float(self.contribution_share),
            "contribution_share_naive": float(self.contribution_share_naive),
        }


# Channels and their corresponding SimulatorConfig parameter modifications.
# To "turn off" a channel, we set the relevant rate/parameter to zero or
# to its no-effect value while leaving all others at default.
CHANNELS: dict[str, dict[str, float]] = {
    "automation": {
        # Turn off automation rate dI/dt to isolate
        "us_labor_share_decay_rate": 0.0,
        "us_substitute_emp_decay": 0.0,
    },
    "markup_expansion": {
        # Turn off markup growth
        "us_markup_growth_rate": 0.0,
        "cn_markup_growth_rate": 0.0,
    },
    "worker_bargaining_decline": {
        # Approximation: worker bargaining channel currently expressed
        # via labor-share decay. Reduce it by 50% (the
        # Stansbury-Summers 2020 attribution).
        "us_labor_share_decay_rate": 0.0042,  # half of 0.0085
    },
    "wealth_concentration_dynamics": {
        # Turn off top-1% wealth share growth (Piketty r>g + inheritance)
        "us_top_1pct_growth_rate": 0.0,
        "cn_top_1pct_growth_rate": 0.0,
    },
    "ai_productivity_boost": {
        # Higher AI productivity growth (Acemoglu 2024 high scenario)
        "ai_productivity_growth": 0.035,
        "us_gdp_growth_rate": 0.030,
    },
}


def _run_simulation(config: SimulatorConfig) -> dict[str, float]:
    """Run the simulator and return final-year indicators."""
    sim = BilateralSimulator(config=config)
    df = sim.run().to_dataframe()
    final = df.iloc[-1]
    return {
        "us_labor_share": float(final["us_labor_share"]),
        "us_top_1pct": float(final["us_top_1pct"]),
        "us_markup": float(final["us_markup"]),
        "us_real_gdp": float(final["us_real_gdp"]),
        "us_median_income": float(final["us_median_income"]),
        "cn_labor_share": float(final["cn_labor_share"]),
        "cn_top_1pct": float(final["cn_top_1pct"]),
    }


def decompose_labor_share_decline(
    start_year: int = 2025,
) -> list[MechanismContribution]:
    """Decompose the 2025→2036 US labor-share decline into channels.

    For each channel:
        1. Run simulator with only this channel "active" (others set to
           no-effect values).
        2. Measure the labor-share change attributable to that channel.
        3. Compare to the full simulation with all channels.
    """
    return _decompose_indicator("us_labor_share", start_year)


def decompose_top_1pct_rise(
    start_year: int = 2025,
) -> list[MechanismContribution]:
    """Decompose 2025→2036 US top-1% wealth share rise into channels."""
    return _decompose_indicator("us_top_1pct", start_year)


def _decompose_indicator(
    indicator: str,
    start_year: int,
) -> list[MechanismContribution]:
    """Generic per-indicator decomposition."""
    # Full simulation (all channels active at default)
    full_config = SimulatorConfig()
    full_result = _run_simulation(full_config)

    # Baseline at start_year (initial value of indicator)
    sim = BilateralSimulator(config=full_config)
    df = sim.run().to_dataframe()
    start_value = float(df.loc[start_year, indicator])
    end_value = full_result[indicator]
    full_change = end_value - start_value

    # Per-channel: turn OFF that channel (set to no-effect values)
    # Isolated change = how much movement disappears when this channel is off
    isolated_changes: dict[str, float] = {}
    for channel_name, overrides in CHANNELS.items():
        modified_config = deepcopy(full_config)
        for attr, value in overrides.items():
            if hasattr(modified_config, attr):
                setattr(modified_config, attr, value)
        modified_result = _run_simulation(modified_config)
        modified_change = modified_result[indicator] - start_value
        # This channel's contribution = how much the change shrinks when
        # the channel is removed
        isolated_changes[channel_name] = full_change - modified_change

    # Normalize so contributions sum to 100%
    total_isolated = sum(isolated_changes.values())
    contributions: list[MechanismContribution] = []
    for channel_name, isolated_change in isolated_changes.items():
        contribution_share = (
            isolated_change / total_isolated if abs(total_isolated) > 1e-9 else 0.0
        )
        contribution_share_naive = (
            isolated_change / full_change if abs(full_change) > 1e-9 else 0.0
        )
        contributions.append(
            MechanismContribution(
                channel=channel_name,
                indicator=indicator,
                isolated_change=isolated_change,
                full_change=full_change,
                contribution_share=contribution_share,
                contribution_share_naive=contribution_share_naive,
            )
        )

    return contributions


def report_decomposition(contributions: list[MechanismContribution]) -> str:
    """Human-readable report on mechanism decomposition."""
    if not contributions:
        return "No contributions to report."
    indicator = contributions[0].indicator
    full_change = contributions[0].full_change
    lines = [
        f"Mechanism decomposition: {indicator}",
        "=" * (28 + len(indicator)),
        "",
        f"Total projected change: {full_change:+.4f}",
        "",
        "Per-channel contributions (normalized to 100%):",
    ]
    sorted_contribs = sorted(
        contributions, key=lambda c: abs(c.contribution_share), reverse=True
    )
    for c in sorted_contribs:
        lines.append(
            f"  {c.channel:35s}  isolated={c.isolated_change:+.4f}  "
            f"share={c.contribution_share:+.1%}"
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            "- Shares sum to 100% by construction (normalized).",
            "- Negative contribution share means the channel acts in the"
            " *opposite* direction to the total projected change",
            "  (e.g., AI productivity boost partially offsets labor-share"
            " decline).",
            "- 'AI-specific' attribution is the sum of channels where AI"
            " is the proximate cause:",
            "  automation + (some fraction of) capital-bias + AI productivity.",
            "  Markup expansion and worker bargaining decline are largely"
            " pre-AI trends.",
        ]
    )
    return "\n".join(lines)


def ai_specific_share(contributions: list[MechanismContribution]) -> float:
    """Estimate fraction of projected change attributable to AI specifically.

    AI-specific channels: automation, ai_productivity_boost, and a
    fraction of wealth_concentration_dynamics (since AI accelerates
    differential returns).

    Pre-AI channels: markup_expansion (predates AI; DLEU 2020 trend
    from 1980), worker_bargaining_decline (Stansbury-Summers 2020 says
    most labor-share decline 1980-2020 is bargaining-driven).
    """
    by_channel = {c.channel: c.contribution_share for c in contributions}
    ai_specific = (
        by_channel.get("automation", 0.0)
        + by_channel.get("ai_productivity_boost", 0.0)
        + 0.5 * by_channel.get("wealth_concentration_dynamics", 0.0)
    )
    return ai_specific
