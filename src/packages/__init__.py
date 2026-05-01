"""Policy packages compared in the simulation.

Each package is a typed PolicyPackage dataclass with a documented mapping
from each policy lever to its target mechanism. See PREREGISTRATION.md §2
for the full comparison set.

Packages:
    A. status_quo            — Patchwork baseline (no new framework)
    B. nebulai_six           — The original six-pillar framework
    C. cern_ai               — Global public lab + compute governance
    D. compute_centric       — Compute tax + access mandates + structural separation
    E. direct_redistribution — UBI + wealth tax + UBC + care economy
    F. build_different       — Acemoglu directed-AI; procurement; codetermination
    G. game_theoretic        — Eight pillars derived from robustness constraints
"""

from src.packages.base import (
    LeverTarget,
    PolicyLever,
    PolicyPackage,
    Reversibility,
)
from src.packages.registry import (
    ALL_PACKAGES,
    BUILD_DIFFERENT,
    CERN_AI,
    COMPUTE_CENTRIC,
    DIRECT_REDISTRIBUTION,
    GAME_THEORETIC,
    NEBULAI_SIX,
    NEBULAI_SIX_SEQUENTIAL,
    NEBULAI_SIX_VARIANTS,
    PACKAGES_BY_CODE,
    STATUS_QUO,
    get_package,
    list_packages,
)

__all__ = [
    "PolicyPackage",
    "PolicyLever",
    "LeverTarget",
    "Reversibility",
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
]
