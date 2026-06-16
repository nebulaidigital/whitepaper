"""Time-consistency stress test.

Introduce stochastic policy reversal (probability per lever weighted by
reversibility) and measure expected welfare. Tests whether the package
survives political reversal pressure.

Per PREREGISTRATION.md §5 Hypothesis 10.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field

import numpy as np

from src.core import BilateralSimulator, SimulatorConfig
from src.packages.base import PolicyLever, PolicyPackage, Reversibility


@dataclass(frozen=True)
class TimeConsistencyResult:
    """Outcome of time-consistency stress test."""

    package_code: str
    n_draws: int
    expected_welfare_full_persistence: float
    expected_welfare_under_stochastic_reversal: float
    welfare_loss_from_political_risk: float
    most_vulnerable_lever: str
    fraction_draws_below_baseline: float


class TimeConsistencyTest:
    """Time-consistency stress test.

    Per-year reversal probability by reversibility category (years 5+):
        REVERSIBLE       → 0.50/yr
        SEMI_REVERSIBLE  → 0.20/yr
        IRREVERSIBLE     → 0.05/yr (released weights cannot really be retracted)

    Monte Carlo over reversal realizations to compute expected welfare
    under stochastic reversal. Most-vulnerable lever is whose absence
    causes the largest welfare drop.
    """

    REVERSAL_PROBABILITIES_PER_YEAR: dict[Reversibility, float] = field(
        default_factory=lambda: {}
    )

    def __init__(
        self,
        package: PolicyPackage,
        n_draws: int = 200,
        welfare_metric: str = "us_median_income",
        seed: int = 20260616,
    ) -> None:
        self.package = package
        self.n_draws = n_draws
        self.welfare_metric = welfare_metric
        self.rng = np.random.default_rng(seed=seed)
        self._reversal_probs = {
            Reversibility.REVERSIBLE: 0.50,
            Reversibility.SEMI_REVERSIBLE: 0.20,
            Reversibility.IRREVERSIBLE: 0.05,
        }

    def _build_partial_package(
        self,
        keep: list[PolicyLever],
    ) -> PolicyPackage:
        """Return a copy of the package containing only the `keep` levers."""
        return PolicyPackage(
            code=self.package.code,
            name=self.package.name + " (partial reversal)",
            description=self.package.description,
            levers=tuple(keep),
            activation_year=self.package.activation_year,
            sequencing=self.package.sequencing,
        )

    def _final_metric(self, df) -> float:
        return float(df[self.welfare_metric].iloc[-1])

    def run(self) -> TimeConsistencyResult:
        sim = BilateralSimulator(config=SimulatorConfig())
        baseline_welfare = self._final_metric(sim.run().to_dataframe())

        # Full-persistence welfare
        full_welfare = self._final_metric(
            sim.run(
                package=self.package, coalition_share=0.7, cn_cooperation=0.5
            ).to_dataframe()
        )

        # Monte Carlo over reversal realizations
        draw_welfares = np.zeros(self.n_draws)
        # For most-vulnerable analysis, track per-lever effect when removed
        per_lever_when_removed = {lev.name: [] for lev in self.package.levers}

        for d in range(self.n_draws):
            kept_levers = []
            for lev in self.package.levers:
                p_reverse = self._reversal_probs[lev.reversibility]
                # Over the simulation horizon (5+ years stress window),
                # probability of survival = (1 - p_reverse)^window
                # We use a 6-year stress window for the reversal events
                p_survive = (1.0 - p_reverse) ** 6
                if self.rng.random() < p_survive:
                    kept_levers.append(lev)
            partial = self._build_partial_package(kept_levers)
            df = sim.run(
                package=partial,
                coalition_share=0.7,
                cn_cooperation=0.5,
            ).to_dataframe()
            draw_welfares[d] = self._final_metric(df)

            # Update per-lever-when-removed series
            for lev in self.package.levers:
                if lev not in kept_levers:
                    per_lever_when_removed[lev.name].append(draw_welfares[d])

        E_partial = float(np.mean(draw_welfares))
        loss = full_welfare - E_partial
        fraction_below_baseline = float(np.mean(draw_welfares < baseline_welfare))

        # Most-vulnerable lever = whose absence has the largest negative
        # mean welfare relative to full persistence
        worst_lever = "<none>"
        worst_gap = -np.inf
        for name, welfares in per_lever_when_removed.items():
            if not welfares:
                continue
            gap = full_welfare - float(np.mean(welfares))
            if gap > worst_gap:
                worst_gap = gap
                worst_lever = name

        return TimeConsistencyResult(
            package_code=self.package.code,
            n_draws=self.n_draws,
            expected_welfare_full_persistence=full_welfare,
            expected_welfare_under_stochastic_reversal=E_partial,
            welfare_loss_from_political_risk=loss,
            most_vulnerable_lever=worst_lever,
            fraction_draws_below_baseline=fraction_below_baseline,
        )
