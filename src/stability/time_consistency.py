"""Time-consistency stress test.

Introduce stochastic policy reversal (50% probability per pillar in years
5–10) and measure expected welfare. Tests whether the package survives
political reversal pressure.

Per PREREGISTRATION.md §5 Hypothesis 10. Stub — full implementation depends
on bilateral simulator (Phase 3) and Monte Carlo wrapper (Phase 4).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.packages.base import PolicyPackage, Reversibility


@dataclass(frozen=True)
class TimeConsistencyResult:
    """Outcome of time-consistency stress test.

    Attributes
    ----------
    package_code : single-letter code of package under test
    n_draws : number of Monte Carlo draws
    expected_welfare_full_persistence : E[welfare] without any reversal
    expected_welfare_under_stochastic_reversal : E[welfare] with reversal pressure
    welfare_loss_from_political_risk : difference (positive = vulnerable)
    most_vulnerable_lever : lever name whose reversal causes largest welfare loss
    """

    package_code: str
    n_draws: int
    expected_welfare_full_persistence: float
    expected_welfare_under_stochastic_reversal: float
    welfare_loss_from_political_risk: float
    most_vulnerable_lever: str


class TimeConsistencyTest:
    """Run time-consistency stress test.

    Plan (Phase 4):
    - For each lever in package, assign reversal probability based on its
      Reversibility property:
        REVERSIBLE       → 0.50/yr in years 5–10
        SEMI_REVERSIBLE  → 0.20/yr in years 5–10
        IRREVERSIBLE     → 0.05/yr in years 5–10 (reversal essentially fails)
    - Monte Carlo over reversal realizations + RDM parameter draws
    - Compute expected welfare under stochastic reversal
    - Identify most-vulnerable lever
    """

    REVERSAL_PROBABILITIES_PER_YEAR: dict[Reversibility, float] = {
        Reversibility.REVERSIBLE: 0.50,
        Reversibility.SEMI_REVERSIBLE: 0.20,
        Reversibility.IRREVERSIBLE: 0.05,
    }

    def __init__(self, package: PolicyPackage, n_draws: int = 1000) -> None:
        self.package = package
        self.n_draws = n_draws
        self.rng = np.random.default_rng(seed=20260501)

    def reversal_probability_per_year(self) -> dict[str, float]:
        """Return per-lever reversal probability per year in stress window."""
        return {
            lever.name: self.REVERSAL_PROBABILITIES_PER_YEAR[lever.reversibility]
            for lever in self.package.levers
        }

    def run(self) -> TimeConsistencyResult:
        """Execute time-consistency stress test.

        Stub. Returns NaN-filled result until simulator + MC wrapper exist.
        """
        return TimeConsistencyResult(
            package_code=self.package.code,
            n_draws=0,
            expected_welfare_full_persistence=float("nan"),
            expected_welfare_under_stochastic_reversal=float("nan"),
            welfare_loss_from_political_risk=float("nan"),
            most_vulnerable_lever="<unimplemented>",
        )
