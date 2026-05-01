"""Coalition formation stress test.

Vary participating coalition from 30% to 100% of global AI compute.
Identify minimum threshold for each lever to be welfare-positive.

Per PREREGISTRATION.md §5 Hypothesis 10. Stub — full implementation depends
on bilateral simulator (Phase 3).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.packages.base import PolicyPackage


@dataclass(frozen=True)
class CoalitionResult:
    """Outcome of coalition-size sweep for a package.

    Attributes
    ----------
    package_code : single-letter code of package under test
    coalition_thresholds : array of compute-share values swept
    welfare_deltas : array of welfare deltas at each coalition size
    breakeven_threshold : smallest coalition size for which welfare ≥ 0
        (NaN if package fails at all coalition sizes)
    package_threshold_specified : the package's own claimed minimum coalition
    threshold_consistency : whether actual breakeven is ≤ specified threshold
    """

    package_code: str
    coalition_thresholds: np.ndarray
    welfare_deltas: np.ndarray
    breakeven_threshold: float
    package_threshold_specified: float
    threshold_consistency: bool


class CoalitionTest:
    """Run coalition-size sweep for a package.

    Plan (Phase 3+):
    - Sweep coalition share from 0.3 to 1.0 in steps of 0.05
    - At each share, run bilateral simulator with that fraction of global
      compute participating in coordination-dependent levers
    - Compute welfare delta vs. baseline at each coalition share
    - Identify breakeven threshold
    - Compare to package's specified coalition_threshold values
    """

    def __init__(self, package: PolicyPackage) -> None:
        self.package = package

    def specified_threshold(self) -> float:
        """Maximum coalition_threshold across coordination-dependent levers.

        This is the minimum coalition the package itself claims is needed
        for all coordination-dependent levers to function.
        """
        coord_levers = self.package.coordination_dependent_levers()
        if not coord_levers:
            return 0.0
        return max(lev.coalition_threshold for lev in coord_levers)

    def run(self) -> CoalitionResult:
        """Execute coalition sweep.

        Stub. Returns empty arrays until bilateral simulator is built (Phase 3).
        """
        return CoalitionResult(
            package_code=self.package.code,
            coalition_thresholds=np.array([]),
            welfare_deltas=np.array([]),
            breakeven_threshold=float("nan"),
            package_threshold_specified=self.specified_threshold(),
            threshold_consistency=False,
        )
