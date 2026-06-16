"""Defection stress test.

For each coordination-dependent lever, simulate the most likely defection
and measure whether welfare under defection beats baseline.

Per PREREGISTRATION.md §5 Hypothesis 10.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.core import BilateralSimulator, SimulatorConfig
from src.packages.base import PolicyLever, PolicyPackage


@dataclass(frozen=True)
class DefectionResult:
    """Outcome of a single defection scenario."""

    package_code: str
    defecting_lever: str
    defector: str  # 'CN', 'tax_haven', 'frontier_lab', 'EU'
    welfare_delta_vs_baseline: float
    welfare_delta_vs_full_compliance: float
    coalition_share_remaining: float
    fragile: bool  # True if defection makes the package worse than no-policy


class DefectionTest:
    """Run defection scenarios for a package.

    For each coordination-dependent lever:
    1. Identify the most-likely defector based on the lever's mechanism
    2. Re-run the simulator with that defector removed from the coalition
    3. Compare welfare to: (a) status quo baseline, (b) full compliance
    4. Flag the lever as 'fragile' if it's net negative under defection
    """

    def __init__(
        self,
        package: PolicyPackage,
        welfare_metric: str = "us_median_income",
    ) -> None:
        self.package = package
        self.welfare_metric = welfare_metric

    @staticmethod
    def _likely_defector(lever: PolicyLever) -> str:
        """Map lever to its most-likely defector based on the mechanism.

        Heuristic from the strategic-interaction literature:
        - Compute governance, capability disclosure, treaty obligations:
          CN is most likely defector (strategic-competition incentive)
        - AI tax / OECD-coordinated tax: tax-haven jurisdictions
        - Open-weights mandate: frontier-lab jurisdiction with strongest
          commercial incentive to retain weights
        - CERN-AI / global lab: smaller member states with limited
          fiscal capacity
        """
        n = lever.name.lower()
        if "compute" in n or "treaty" in n:
            return "CN"
        if "tax" in n:
            return "tax_haven"
        if "open" in n or "weight" in n:
            return "frontier_lab"
        if "cern" in n or "lab" in n:
            return "minor_member"
        if "disclosure" in n or "eval" in n:
            return "CN"
        return "unspecified"

    def candidate_defections(self) -> list[tuple[PolicyLever, str]]:
        """Return the (lever, defector) pairs to test."""
        return [
            (lever, self._likely_defector(lever))
            for lever in self.package.coordination_dependent_levers()
        ]

    def _final_metric(self, df, metric: str) -> float:
        if metric in df.columns:
            return float(df[metric].iloc[-1])
        raise KeyError(f"Metric {metric!r} not in simulator output columns")

    def run(self, base_coalition: float = 0.70) -> list[DefectionResult]:
        sim = BilateralSimulator(config=SimulatorConfig())
        baseline_df = sim.run().to_dataframe()
        baseline_welfare = self._final_metric(baseline_df, self.welfare_metric)
        full_df = sim.run(
            package=self.package, coalition_share=base_coalition, cn_cooperation=0.5
        ).to_dataframe()
        full_welfare = self._final_metric(full_df, self.welfare_metric)

        # Defector share of frontier compute — calibrated to actual
        # geographic distribution per AI Index 2025
        defector_share = {
            "CN": 0.25,
            "tax_haven": 0.08,
            "frontier_lab": 0.30,  # collective frontier US labs
            "minor_member": 0.10,
            "EU": 0.20,
            "unspecified": 0.15,
        }

        results: list[DefectionResult] = []
        for lever, defector in self.candidate_defections():
            share_loss = defector_share.get(defector, 0.15)
            new_coalition = max(0.0, base_coalition - share_loss)
            # Run package at reduced coalition; if defection drops below
            # lever's threshold, the simulator will gate the lever.
            defect_df = sim.run(
                package=self.package,
                coalition_share=new_coalition,
                cn_cooperation=0.2 if defector == "CN" else 0.3,
            ).to_dataframe()
            defect_welfare = self._final_metric(defect_df, self.welfare_metric)
            d_vs_baseline = defect_welfare - baseline_welfare
            d_vs_full = defect_welfare - full_welfare
            fragile = (full_welfare > baseline_welfare) and (
                defect_welfare < baseline_welfare
            )

            results.append(
                DefectionResult(
                    package_code=self.package.code,
                    defecting_lever=lever.name,
                    defector=defector,
                    welfare_delta_vs_baseline=d_vs_baseline,
                    welfare_delta_vs_full_compliance=d_vs_full,
                    coalition_share_remaining=new_coalition,
                    fragile=fragile,
                )
            )

        return results

    def summary(self, results: list[DefectionResult]) -> dict[str, float]:
        if not results:
            return {
                "package_code": self.package.code,
                "n_defections_tested": 0,
                "n_fragile": 0,
                "fraction_fragile": 0.0,
                "mean_welfare_loss_from_defection": 0.0,
            }
        n = len(results)
        n_fragile = sum(1 for r in results if r.fragile)
        mean_loss = float(
            np.mean([abs(r.welfare_delta_vs_full_compliance) for r in results])
        )
        return {
            "package_code": self.package.code,
            "n_defections_tested": n,
            "n_fragile": n_fragile,
            "fraction_fragile": n_fragile / n,
            "mean_welfare_loss_from_defection": mean_loss,
        }
