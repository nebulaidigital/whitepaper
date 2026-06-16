"""Cross-class welfare distribution test.

By-decile welfare deltas. Tests Hypothesis 4 (median-voter sufficiency):
under the package, the median household in every income decile in every
country tier should be better off vs. status quo.

Per PREREGISTRATION.md Hypothesis 4 and Hypothesis 10.

This implementation works on the bilateral US/CN model. The framework's
adoption-equilibrium claim is by-decile in 'every country tier'; with the
bilateral model we have Frontier (US, CN as representatives) and skip
Emerging/Developing tiers until Phase 7. Status of three-tier extension
is documented in ROADMAP.md.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.core import BilateralSimulator, SimulatorConfig
from src.packages.base import PolicyPackage


@dataclass(frozen=True)
class CrossClassResult:
    """Cross-class welfare distribution outcome.

    Attributes
    ----------
    welfare_delta_matrix : (10, 2) array — deciles × countries (US, CN)
        Cell [d, c] = median household Δ(real income) in decile d, country c
    n_cells_positive : count of cells with positive delta
    n_cells_negative : count with negative delta
    fails_hypothesis_4 : True if ANY decile is worse off — refutes the
        framework's adoption-equilibrium claim
    most_disadvantaged_cell : (decile, country) with smallest delta
    """

    package_code: str
    welfare_delta_matrix: np.ndarray
    n_cells_positive: int
    n_cells_negative: int
    fails_hypothesis_4: bool
    most_disadvantaged_cell: tuple[int, str]
    most_disadvantaged_delta: float

    def to_dict(self) -> dict:
        return {
            "package_code": self.package_code,
            "n_cells_positive": int(self.n_cells_positive),
            "n_cells_negative": int(self.n_cells_negative),
            "fails_hypothesis_4": bool(self.fails_hypothesis_4),
            "most_disadvantaged_decile": int(self.most_disadvantaged_cell[0]),
            "most_disadvantaged_country": self.most_disadvantaged_cell[1],
            "most_disadvantaged_delta_pct": float(self.most_disadvantaged_delta),
        }


class CrossClassTest:
    """Cross-class welfare distribution test.

    Run the simulator twice (baseline + package), then compute
    Δ(real income) for each (decile, country) cell. Hypothesis 4
    passes only if every cell is positive at the median estimate.
    """

    COUNTRIES: tuple[str, str] = ("US", "CN")
    N_DECILES: int = 10

    def __init__(self, package: PolicyPackage) -> None:
        self.package = package

    def run(self, coalition_share: float = 0.7, cn_cooperation: float = 0.5) -> CrossClassResult:
        sim = BilateralSimulator(config=SimulatorConfig())
        baseline = sim.run()
        package_run = sim.run(
            package=self.package,
            coalition_share=coalition_share,
            cn_cooperation=cn_cooperation,
        )

        # Pull final-year decile_real_income matrices
        us_baseline_final = baseline.us.decile_real_income[-1]
        cn_baseline_final = baseline.cn.decile_real_income[-1]
        us_package_final = package_run.us.decile_real_income[-1]
        cn_package_final = package_run.cn.decile_real_income[-1]

        # Δ as % of baseline decile income
        us_delta_pct = (us_package_final - us_baseline_final) / np.where(
            us_baseline_final > 0, us_baseline_final, 1.0
        )
        cn_delta_pct = (cn_package_final - cn_baseline_final) / np.where(
            cn_baseline_final > 0, cn_baseline_final, 1.0
        )

        matrix = np.column_stack([us_delta_pct, cn_delta_pct])  # (10, 2)

        n_pos = int(np.sum(matrix > 0))
        n_neg = int(np.sum(matrix < 0))
        fails = bool(n_neg > 0)

        # Find most disadvantaged cell
        flat_idx = int(np.argmin(matrix))
        decile_idx = flat_idx // matrix.shape[1]
        country_idx = flat_idx % matrix.shape[1]
        most_disadv = (decile_idx + 1, self.COUNTRIES[country_idx])
        most_disadv_delta = float(matrix[decile_idx, country_idx])

        return CrossClassResult(
            package_code=self.package.code,
            welfare_delta_matrix=matrix,
            n_cells_positive=n_pos,
            n_cells_negative=n_neg,
            fails_hypothesis_4=fails,
            most_disadvantaged_cell=most_disadv,
            most_disadvantaged_delta=most_disadv_delta,
        )
