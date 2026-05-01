"""Defection stress test.

For each lever in a package, simulate the most likely defection
(capital flight, jurisdiction shopping, weight non-release, treaty exit).
Measure whether welfare under defection beats baseline.

Per PREREGISTRATION.md §5 Hypothesis 10. Stub — full implementation depends
on bilateral simulator (Phase 3).
"""

from __future__ import annotations

from dataclasses import dataclass

from src.packages.base import PolicyLever, PolicyPackage


@dataclass(frozen=True)
class DefectionResult:
    """Outcome of a single defection scenario.

    Attributes
    ----------
    package_code : single-letter code of package under test
    defecting_lever : the lever whose coordination requirement was violated
    defector : country / actor that defected (e.g., 'CN', 'EU', 'private_capital')
    welfare_delta_vs_baseline : Δ welfare vs. status quo if defection occurs
    welfare_delta_vs_full_compliance : Δ welfare relative to full compliance
    coalition_share_remaining : fraction of compute / actors still participating
    """

    package_code: str
    defecting_lever: str
    defector: str
    welfare_delta_vs_baseline: float
    welfare_delta_vs_full_compliance: float
    coalition_share_remaining: float


class DefectionTest:
    """Run defection scenarios for a package.

    Plan (Phase 3+):
    - For each coordination-dependent lever, identify the most-likely defector
    - Re-run bilateral simulator with that lever inactive in defector country
    - Compute welfare delta vs. baseline and vs. full-compliance scenario
    - Aggregate results into DefectionResult set
    """

    def __init__(self, package: PolicyPackage) -> None:
        self.package = package

    def candidate_defections(self) -> list[tuple[PolicyLever, str]]:
        """Return (lever, likely defector) pairs for each coordination-dependent
        lever in the package.

        Defector heuristic (refined in implementation):
        - Compute governance treaty: likely defector is the highest-capability
          jurisdiction outside the coalition
        - AI tax (OECD-coordinated): likely defector is a tax haven
        - Open weights mandate: likely defector is the leading frontier lab
          jurisdiction with strong commercial incentive to retain weights
        - Capability disclosure: likely defector is a state actor with strategic-
          competition incentive to obscure capability
        """
        pairs: list[tuple[PolicyLever, str]] = []
        for lever in self.package.coordination_dependent_levers():
            if "compute" in lever.name.lower():
                pairs.append((lever, "CN"))
            elif "tax" in lever.name.lower():
                pairs.append((lever, "tax_haven"))
            elif "open" in lever.name.lower() or "weight" in lever.name.lower():
                pairs.append((lever, "frontier_lab"))
            elif "disclosure" in lever.name.lower():
                pairs.append((lever, "CN"))
            else:
                pairs.append((lever, "default_defector"))
        return pairs

    def run(self) -> list[DefectionResult]:
        """Execute all defection scenarios.

        Stub. Returns empty list until bilateral simulator is built (Phase 3).
        """
        # Implemented in Phase 3 once bilateral simulator is available.
        return []
