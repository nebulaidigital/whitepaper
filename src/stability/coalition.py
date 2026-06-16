"""Coalition formation stress test.

Vary participating coalition share from 0.3 to 1.0 and identify the
breakeven threshold at which the package is welfare-positive vs.
status quo.

Per PREREGISTRATION.md §5 Hypothesis 10.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.core import BilateralSimulator, SimulatorConfig
from src.packages.base import PolicyPackage


@dataclass(frozen=True)
class CoalitionResult:
    """Coalition-size sweep for a package."""

    package_code: str
    coalition_thresholds: np.ndarray
    welfare_deltas: np.ndarray  # vs status quo at each coalition size
    breakeven_threshold: float  # smallest coalition for which welfare ≥ 0
    package_threshold_specified: float  # max coalition_threshold declared in package
    threshold_consistency: bool  # actual breakeven ≤ specified threshold

    def to_dict(self) -> dict:
        return {
            "package_code": self.package_code,
            "breakeven_threshold": float(self.breakeven_threshold),
            "package_threshold_specified": float(self.package_threshold_specified),
            "threshold_consistency": bool(self.threshold_consistency),
            "min_coalition_tested": float(self.coalition_thresholds.min()) if len(self.coalition_thresholds) > 0 else float("nan"),
            "max_welfare_delta": float(self.welfare_deltas.max()) if len(self.welfare_deltas) > 0 else float("nan"),
        }


class CoalitionTest:
    """Coalition-size sweep.

    For each coalition share in [0.30, 1.00] step 0.05, run the package
    through the simulator and compute welfare delta vs. status quo.
    Then identify the smallest coalition that achieves welfare ≥ 0.
    """

    def __init__(
        self,
        package: PolicyPackage,
        welfare_metric: str = "us_median_income",
    ) -> None:
        self.package = package
        self.welfare_metric = welfare_metric

    def specified_threshold(self) -> float:
        coord_levers = self.package.coordination_dependent_levers()
        if not coord_levers:
            return 0.0
        return max(lev.coalition_threshold for lev in coord_levers)

    def _final_metric(self, df) -> float:
        return float(df[self.welfare_metric].iloc[-1])

    def run(self, n_steps: int = 15) -> CoalitionResult:
        sim = BilateralSimulator(config=SimulatorConfig())
        baseline_welfare = self._final_metric(sim.run().to_dataframe())

        thresholds = np.linspace(0.30, 1.00, n_steps)
        deltas = np.zeros(n_steps)

        for i, share in enumerate(thresholds):
            df = sim.run(
                package=self.package,
                coalition_share=float(share),
                cn_cooperation=0.5,
            ).to_dataframe()
            deltas[i] = self._final_metric(df) - baseline_welfare

        # Smallest threshold where welfare delta ≥ 0
        positive = thresholds[deltas >= 0]
        breakeven = float(positive.min()) if len(positive) > 0 else float("nan")
        specified = self.specified_threshold()
        consistency = (not np.isnan(breakeven)) and (breakeven <= specified + 0.05)

        return CoalitionResult(
            package_code=self.package.code,
            coalition_thresholds=thresholds,
            welfare_deltas=deltas,
            breakeven_threshold=breakeven,
            package_threshold_specified=specified,
            threshold_consistency=consistency,
        )
