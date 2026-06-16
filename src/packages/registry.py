"""Central registry of all policy packages.

Importing this module gives access to all seven packages by their letter
code, by name, and as a list. Used by the simulator's CLI and by analysis
scripts.
"""

from src.packages.base import PolicyPackage
from src.packages.build_different import BUILD_DIFFERENT
from src.packages.cern_ai import CERN_AI
from src.packages.compute_centric import COMPUTE_CENTRIC
from src.packages.direct_redistribution import DIRECT_REDISTRIBUTION
from src.packages.game_theoretic import GAME_THEORETIC
from src.packages.korinek_scenario import KORINEK_SCENARIO
from src.packages.nebulai_six import NEBULAI_SIX, NEBULAI_SIX_SEQUENTIAL
from src.packages.nebulai_v2 import NEBULAI_V2
from src.packages.recommended import RECOMMENDED
from src.packages.status_quo import STATUS_QUO


ALL_PACKAGES: tuple[PolicyPackage, ...] = (
    STATUS_QUO,
    NEBULAI_SIX,
    CERN_AI,
    COMPUTE_CENTRIC,
    DIRECT_REDISTRIBUTION,
    BUILD_DIFFERENT,
    GAME_THEORETIC,
    KORINEK_SCENARIO,
    RECOMMENDED,
    NEBULAI_V2,
)


PACKAGES_BY_CODE: dict[str, PolicyPackage] = {
    pkg.code: pkg for pkg in ALL_PACKAGES
}


# Sequencing variants of Package B for Hypothesis 2 (reversibility test)
NEBULAI_SIX_VARIANTS: dict[str, PolicyPackage] = {
    "simultaneous": NEBULAI_SIX,
    "sequential": NEBULAI_SIX_SEQUENTIAL,
}


def get_package(code: str) -> PolicyPackage:
    """Look up a package by its single-letter code."""
    if code not in PACKAGES_BY_CODE:
        raise KeyError(
            f"No package with code {code!r}. Valid codes: "
            f"{sorted(PACKAGES_BY_CODE.keys())}"
        )
    return PACKAGES_BY_CODE[code]


def list_packages() -> str:
    """Return a human-readable summary of all packages — used for CLI help."""
    lines = ["Policy packages compared in this simulation:\n"]
    for pkg in ALL_PACKAGES:
        n_levers = len(pkg.levers)
        n_irrev = len(pkg.irreversible_levers())
        n_coord = len(pkg.coordination_dependent_levers())
        lines.append(
            f"  {pkg.code}. {pkg.name}\n"
            f"     Levers: {n_levers} total, {n_irrev} irreversible, "
            f"{n_coord} coordination-dependent\n"
            f"     Sequencing: {pkg.sequencing}\n"
        )
    return "\n".join(lines)


__all__ = [
    "ALL_PACKAGES",
    "PACKAGES_BY_CODE",
    "NEBULAI_SIX_VARIANTS",
    "get_package",
    "list_packages",
    "STATUS_QUO",
    "NEBULAI_SIX",
    "NEBULAI_SIX_SEQUENTIAL",
    "CERN_AI",
    "COMPUTE_CENTRIC",
    "DIRECT_REDISTRIBUTION",
    "BUILD_DIFFERENT",
    "GAME_THEORETIC",
    "KORINEK_SCENARIO",
    "RECOMMENDED",
    "NEBULAI_V2",
]
