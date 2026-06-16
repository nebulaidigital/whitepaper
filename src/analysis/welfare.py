"""Formal welfare framework.

The v0.2 paper treats package comparisons via direct indicator deltas
("Package E wins on top-1% wealth share, Package F wins on GDP growth")
without a formal welfare aggregation. A PhD-level critique correctly
asks: compared to what objective function? Different welfare functions
produce different optimal packages.

This module implements:

1. **Atkinson-Sen social welfare function** with explicit inequality
   aversion parameter ε ∈ [0, ∞):
       W(ε) = [(1/N) Σ y_i^(1-ε)]^(1/(1-ε))   for ε ≠ 1
       W(1) = exp[(1/N) Σ ln(y_i)]              for ε = 1 (geometric mean)

   ε = 0: utilitarian (welfare = mean income)
   ε = 1: equal weight to log income (geometric mean)
   ε = 2: standard inequality aversion
   ε → ∞: Rawlsian (welfare = min income / bottom decile)

2. **Bergson-Samuelson explicit weights** as a generalization, for cases
   where the policy decision wants to weight specific deciles by their
   political-influence weight rather than by income.

3. **Package ranking under each welfare function** — for each ε,
   compute each package's welfare delta vs. status quo and rank.

References:
    Atkinson (1970) "On the measurement of inequality" JET 2(3).
    Sen (1976) "Real National Income" RES 43(1).
    Bergson (1938) "A Reformulation of Certain Aspects of Welfare Economics."
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.core import BilateralSimulator
from src.packages import ALL_PACKAGES, PolicyPackage


@dataclass(frozen=True)
class WelfareResult:
    """Welfare evaluation result for one package."""

    package_code: str
    package_name: str
    epsilon: float
    welfare_us: float  # absolute SWF value, US
    welfare_cn: float
    welfare_us_baseline: float  # comparison vs status quo
    welfare_cn_baseline: float
    delta_us: float
    delta_cn: float
    delta_global_mean: float

    def to_dict(self) -> dict:
        return {
            "package_code": self.package_code,
            "package_name": self.package_name,
            "epsilon": float(self.epsilon),
            "welfare_us": float(self.welfare_us),
            "welfare_cn": float(self.welfare_cn),
            "delta_us": float(self.delta_us),
            "delta_cn": float(self.delta_cn),
            "delta_global_mean": float(self.delta_global_mean),
        }


def atkinson_swf(incomes: np.ndarray, epsilon: float) -> float:
    """Atkinson-Sen social welfare function.

    Parameters
    ----------
    incomes : array of decile median incomes
    epsilon : inequality aversion parameter ∈ [0, ∞)
        0   = utilitarian (mean)
        1   = geometric mean (log utility)
        2   = standard inequality aversion
        ∞   = Rawlsian (min)

    Returns
    -------
    The equally-distributed-equivalent income, i.e., the income level
    that, if everyone received it, would be welfare-equivalent to the
    actual distribution.
    """
    if len(incomes) == 0:
        return 0.0
    if np.any(incomes <= 0):
        # Cannot evaluate Atkinson SWF on non-positive incomes; treat
        # as bottom-bound (would be welfare-zero).
        return 0.0

    if epsilon == 0:
        return float(np.mean(incomes))
    elif np.isinf(epsilon):
        return float(np.min(incomes))  # Rawlsian
    elif abs(epsilon - 1.0) < 1e-9:
        # Geometric mean
        return float(np.exp(np.mean(np.log(incomes))))
    else:
        # General case: ((1/N) Σ y^(1-ε))^(1/(1-ε))
        weighted = np.power(incomes, 1.0 - epsilon)
        mean_weighted = float(np.mean(weighted))
        return float(np.power(mean_weighted, 1.0 / (1.0 - epsilon)))


def bergson_samuelson(
    incomes: np.ndarray,
    weights: np.ndarray | None = None,
) -> float:
    """Bergson-Samuelson explicit-weights social welfare.

    Parameters
    ----------
    incomes : array of decile median incomes
    weights : array of explicit weights per decile (default uniform).

    Returns
    -------
    Weighted sum: Σ w_i · y_i.
    """
    if weights is None:
        weights = np.ones_like(incomes) / len(incomes)
    weights = np.asarray(weights)
    if abs(weights.sum() - 1.0) > 1e-6:
        weights = weights / weights.sum()  # normalize
    return float(np.dot(weights, incomes))


def evaluate_package_welfare(
    package: PolicyPackage,
    epsilon: float = 1.0,
) -> WelfareResult:
    """Compute Atkinson SWF for one package vs. status quo baseline."""
    sim = BilateralSimulator()
    baseline = sim.run()
    package_run = sim.run(package=package, coalition_share=0.7, cn_cooperation=0.5)

    us_baseline_incomes = baseline.us.decile_real_income[-1]
    cn_baseline_incomes = baseline.cn.decile_real_income[-1]
    us_package_incomes = package_run.us.decile_real_income[-1]
    cn_package_incomes = package_run.cn.decile_real_income[-1]

    w_us = atkinson_swf(us_package_incomes, epsilon)
    w_cn = atkinson_swf(cn_package_incomes, epsilon)
    w_us_base = atkinson_swf(us_baseline_incomes, epsilon)
    w_cn_base = atkinson_swf(cn_baseline_incomes, epsilon)

    delta_us = w_us - w_us_base
    delta_cn = w_cn - w_cn_base
    delta_global = (delta_us + delta_cn) / 2.0

    return WelfareResult(
        package_code=package.code,
        package_name=package.name,
        epsilon=epsilon,
        welfare_us=w_us,
        welfare_cn=w_cn,
        welfare_us_baseline=w_us_base,
        welfare_cn_baseline=w_cn_base,
        delta_us=delta_us,
        delta_cn=delta_cn,
        delta_global_mean=delta_global,
    )


def evaluate_all_packages_welfare(
    epsilons: tuple[float, ...] = (0.0, 0.5, 1.0, 2.0, 5.0),
) -> pd.DataFrame:
    """Evaluate every package across a range of inequality aversion values."""
    rows = []
    for eps in epsilons:
        for pkg in ALL_PACKAGES:
            result = evaluate_package_welfare(pkg, epsilon=eps)
            rows.append(result.to_dict())
    return pd.DataFrame(rows)


def package_rankings_by_epsilon(epsilons: tuple[float, ...] | None = None) -> pd.DataFrame:
    """For each ε, rank packages by delta welfare vs. status quo.

    Returns a DataFrame with epsilon × package codes, values = ranks
    (1 = best).
    """
    if epsilons is None:
        epsilons = (0.0, 0.5, 1.0, 2.0, 5.0)

    df = evaluate_all_packages_welfare(epsilons)
    pivot = df.pivot_table(
        index="epsilon",
        columns="package_code",
        values="delta_global_mean",
    )
    # Rank each row (lower rank = higher welfare)
    rankings = pivot.rank(axis=1, ascending=False, method="min")
    return rankings


def report_welfare_evaluation(
    epsilons: tuple[float, ...] = (0.0, 0.5, 1.0, 2.0, 5.0),
) -> str:
    """Human-readable report on welfare evaluation across ε values."""
    df = evaluate_all_packages_welfare(epsilons)
    lines = [
        "Welfare evaluation across Atkinson inequality aversion ε",
        "=" * 60,
        "",
        "ε = 0:  utilitarian (mean income)",
        "ε = 1:  log utility (geometric mean)",
        "ε = 2:  standard inequality aversion",
        "ε = ∞:  Rawlsian (min income)",
        "",
    ]
    for eps in epsilons:
        sub = df[df["epsilon"] == eps].sort_values("delta_global_mean", ascending=False)
        lines.append(f"\nε = {eps}:  ranked by delta global welfare")
        for _, row in sub.iterrows():
            lines.append(
                f"  {row['package_code']}: {row['package_name'][:30]:30s}  "
                f"delta_US={row['delta_us']:+.3f}  delta_CN={row['delta_cn']:+.3f}  "
                f"delta_global={row['delta_global_mean']:+.3f}"
            )

    lines.extend(
        [
            "",
            "Interpretation:",
            "- At ε=0 (utilitarian), the package maximizing total income wins.",
            "- At ε=1 (log utility), the package balancing income across deciles wins.",
            "- At higher ε, packages that lift the bottom deciles most are favored.",
            "- If a package consistently dominates across ε values, it's "
            "welfare-robust. If rankings shift sharply with ε, the choice depends "
            "on the policymaker's prior on inequality aversion.",
        ]
    )
    return "\n".join(lines)
