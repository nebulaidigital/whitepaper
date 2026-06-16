"""Cross-scenario package comparison.

Run every package under every AI scenario (substitute / complement /
new-tasks-dominant) and report comparative welfare. The objective is
to show *how recommendations shift* across regimes — addressing the
PhD-level critique that the v0.2 paper conflates scenarios.

Output structure:
    - For each scenario, full per-package comparison
    - Aggregate dominance: which package wins under most scenarios
    - Robustness: which packages are best on the same metric across all scenarios
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.core import BilateralSimulator, SimulatorConfig
from src.packages import ALL_PACKAGES, PolicyPackage
from src.scenarios import ALL_SCENARIOS


@dataclass(frozen=True)
class ScenarioPackageResult:
    """One simulation result indexed by (scenario, package)."""

    scenario: str
    package_code: str
    package_name: str
    delta_labor_share: float
    delta_top_1pct: float
    delta_markup: float
    delta_gdp_pct: float
    delta_median_income: float
    delta_geopolitical_stability: float

    def to_dict(self) -> dict:
        return {
            "scenario": self.scenario,
            "package_code": self.package_code,
            "package_name": self.package_name,
            "delta_labor_share": float(self.delta_labor_share),
            "delta_top_1pct": float(self.delta_top_1pct),
            "delta_markup": float(self.delta_markup),
            "delta_gdp_pct": float(self.delta_gdp_pct),
            "delta_median_income": float(self.delta_median_income),
            "delta_geopolitical_stability": float(self.delta_geopolitical_stability),
        }


def _eval_package_under_scenario(
    package: PolicyPackage,
    config: SimulatorConfig,
    scenario_name: str,
) -> ScenarioPackageResult:
    sim_baseline = BilateralSimulator(config=config).run()
    sim_package = BilateralSimulator(config=config).run(
        package=package, coalition_share=0.7, cn_cooperation=0.5
    )
    bdf = sim_baseline.to_dataframe()
    pdf = sim_package.to_dataframe()
    return ScenarioPackageResult(
        scenario=scenario_name,
        package_code=package.code,
        package_name=package.name,
        delta_labor_share=(pdf.loc[2036, "us_labor_share"] - bdf.loc[2036, "us_labor_share"]) * 100,
        delta_top_1pct=(pdf.loc[2036, "us_top_1pct"] - bdf.loc[2036, "us_top_1pct"]) * 100,
        delta_markup=pdf.loc[2036, "us_markup"] - bdf.loc[2036, "us_markup"],
        delta_gdp_pct=(pdf.loc[2036, "us_real_gdp"] / bdf.loc[2036, "us_real_gdp"] - 1) * 100,
        delta_median_income=(pdf.loc[2036, "us_median_income"] / bdf.loc[2036, "us_median_income"] - 1) * 100,
        delta_geopolitical_stability=pdf.loc[2036, "geopolitical_stability"]
        - bdf.loc[2036, "geopolitical_stability"],
    )


def cross_scenario_table() -> pd.DataFrame:
    """Run every package under every scenario, return tabular results."""
    rows = []
    for scenario_name, config in ALL_SCENARIOS.items():
        for pkg in ALL_PACKAGES:
            result = _eval_package_under_scenario(pkg, config, scenario_name)
            rows.append(result.to_dict())
    return pd.DataFrame(rows)


def package_robustness(
    df: pd.DataFrame | None = None,
    metric: str = "delta_median_income",
) -> pd.DataFrame:
    """For each package, report mean and std of the metric across scenarios.

    Low std = robust (insensitive to scenario). High std = scenario-dependent.
    """
    if df is None:
        df = cross_scenario_table()
    agg = (
        df.groupby("package_code")[metric]
        .agg(["mean", "std", "min", "max"])
        .sort_values("mean", ascending=False)
    )
    agg.columns = [f"{metric}_{c}" for c in agg.columns]
    return agg


def scenario_winners(
    df: pd.DataFrame | None = None,
    metric: str = "delta_median_income",
) -> pd.DataFrame:
    """For each scenario, identify the winning package on the given metric."""
    if df is None:
        df = cross_scenario_table()
    winners = []
    for scenario, group in df.groupby("scenario"):
        best = group.sort_values(metric, ascending=False).iloc[0]
        winners.append(
            {
                "scenario": scenario,
                "winning_package": best["package_code"],
                "package_name": best["package_name"],
                f"winning_{metric}": best[metric],
            }
        )
    return pd.DataFrame(winners).set_index("scenario")
