"""Cross-class welfare distribution test.

By-decile welfare deltas across 30 cells (10 deciles × 3 country tiers).
Per PREREGISTRATION.md Hypothesis 4 (median-voter sufficiency) and
Hypothesis 10 (game-theoretic robustness).

Stub — full implementation depends on bilateral simulator with country
disaggregation (Phase 3).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.packages.base import PolicyPackage


@dataclass(frozen=True)
class CrossClassResult:
    """Outcome of cross-class welfare test.

    Attributes
    ----------
    package_code : single-letter code of package
    welfare_delta_matrix : (10, 3) array — deciles × country tiers
        Cell [d, t] = median household Δ(real income) in decile d, tier t
    n_cells_positive_p50 : count of cells with positive P50 delta
    n_cells_positive_p10 : count of cells with positive P10 delta
    fails_hypothesis_4 : bool — whether the test refutes the framework's
        adoption-equilibrium claim (Hypothesis 4 in PREREGISTRATION.md)
    most_disadvantaged_cell : (decile, tier) with smallest P50 delta
    """

    package_code: str
    welfare_delta_matrix: np.ndarray
    n_cells_positive_p50: int
    n_cells_positive_p10: int
    fails_hypothesis_4: bool
    most_disadvantaged_cell: tuple[int, str]


class CrossClassTest:
    """Run cross-class welfare distribution test.

    Plan (Phase 3+):
    - Run bilateral simulator with country disaggregation enabled
    - For each tier (Frontier / Emerging / Developing) and decile (1–10),
      compute median household Δ(real income) under the package vs. baseline
    - Aggregate into (10, 3) matrix
    - Apply Hypothesis 4 validation: pass if all 30 P50 deltas positive
      AND ≥25 P10 deltas positive
    """

    TIERS: tuple[str, str, str] = ("Frontier", "Emerging", "Developing")
    N_DECILES: int = 10

    def __init__(self, package: PolicyPackage) -> None:
        self.package = package

    def run(self) -> CrossClassResult:
        """Execute cross-class test.

        Stub. Returns NaN-filled result until simulator with country
        disaggregation exists.
        """
        empty_matrix = np.full((self.N_DECILES, len(self.TIERS)), np.nan)
        return CrossClassResult(
            package_code=self.package.code,
            welfare_delta_matrix=empty_matrix,
            n_cells_positive_p50=0,
            n_cells_positive_p10=0,
            fails_hypothesis_4=True,  # default fail until validated
            most_disadvantaged_cell=(0, "<unimplemented>"),
        )
