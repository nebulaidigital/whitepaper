"""Base types for policy packages.

A PolicyPackage is a typed bundle of PolicyLever instances, each mapping a
specific intervention onto a simulator parameter shift. Packages are the
unit of comparison in the simulation — see PREREGISTRATION.md §2 and
Hypothesis 9.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class LeverTarget(str, Enum):
    """Which simulator subsystem a lever modifies."""

    PRODUCTION = "production"  # task elasticity, automation rate, productivity growth
    FIRMS = "firms"  # markup distribution, markup growth
    LABOR = "labor"  # monopsony elasticity, skill mix
    CAPITAL = "capital"  # depreciation, cost of equity, flight elasticity
    HOUSEHOLDS = "households"  # saving rates, MPC, wealth distribution
    REDISTRIBUTION = "redistribution"  # transfers, taxes, dividends
    CROSS_BORDER = "cross_border"  # capital / services / talent flows
    GOVERNANCE = "governance"  # institutional architecture
    COMPETITION = "competition"  # market structure, antitrust


class Reversibility(str, Enum):
    """Time-consistency property of the lever — used in Hypothesis 2 test."""

    REVERSIBLE = "reversible"  # can be unwound at low cost
    SEMI_REVERSIBLE = "semi_reversible"  # unwinding politically costly
    IRREVERSIBLE = "irreversible"  # cannot meaningfully be reversed


@dataclass(frozen=True)
class PolicyLever:
    """A single intervention.

    Attributes
    ----------
    name : human-readable identifier
    target : which simulator subsystem this modifies
    description : short prose specification
    parameter_changes : dict of {simulator_param_name: shift_value}
        Each shift is applied multiplicatively (1 + shift) for fraction-valued
        params, or additively for rate params. The simulator's lever-application
        layer normalizes per parameter.
    reversibility : time-consistency property
    requires_coordination : if True, lever fails without a coalition of size
        at least `coalition_threshold`
    coalition_threshold : minimum fraction of global AI compute that must
        participate for the lever to function (0.0 if domestic)
    citation : source from SOURCES.md justifying parameter values
    """

    name: str
    target: LeverTarget
    description: str
    parameter_changes: dict[str, float] = field(default_factory=dict)
    reversibility: Reversibility = Reversibility.SEMI_REVERSIBLE
    requires_coordination: bool = False
    coalition_threshold: float = 0.0
    citation: str = ""


@dataclass(frozen=True)
class PolicyPackage:
    """A complete policy package — comparison unit for the simulation.

    Attributes
    ----------
    code : single-letter code (A–G) per PREREGISTRATION.md §2
    name : full name
    description : one-paragraph specification
    levers : list of PolicyLever
    activation_year : year levers begin (2026 for forward-looking; 2026 for status quo)
    sequencing : 'simultaneous' or 'sequential' (only sequential triggers
        Hypothesis 2 evidence-gating)
    """

    code: str
    name: str
    description: str
    levers: tuple[PolicyLever, ...]
    activation_year: int = 2026
    sequencing: str = "simultaneous"

    def __post_init__(self) -> None:
        if self.code not in {"A", "B", "C", "D", "E", "F", "G"}:
            raise ValueError(f"Package code {self.code} not in A–G")
        if self.sequencing not in {"simultaneous", "sequential"}:
            raise ValueError(f"sequencing must be 'simultaneous' or 'sequential'")

    def levers_by_target(self, target: LeverTarget) -> tuple[PolicyLever, ...]:
        """Return all levers acting on a particular simulator subsystem."""
        return tuple(lev for lev in self.levers if lev.target == target)

    def irreversible_levers(self) -> tuple[PolicyLever, ...]:
        """Return all levers that cannot be unwound — used in stress tests."""
        return tuple(
            lev for lev in self.levers if lev.reversibility == Reversibility.IRREVERSIBLE
        )

    def coordination_dependent_levers(self) -> tuple[PolicyLever, ...]:
        """Return levers that fail without coalition formation."""
        return tuple(lev for lev in self.levers if lev.requires_coordination)
