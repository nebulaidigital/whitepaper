"""Game-theoretic robustness stress tests.

These tests evaluate whether a policy package survives realistic strategic
behavior by relevant actors. See PREREGISTRATION.md Hypothesis 10.

Four test families:
    defection      — what happens when an actor defects from a coordination requirement
    coalition      — what fraction of global AI compute must participate for the
                     package to function
    time_consistency — what happens under stochastic political reversal
    cross_class    — by-decile and by-country welfare distribution
"""

from src.stability.defection import DefectionTest, DefectionResult
from src.stability.coalition import CoalitionTest, CoalitionResult
from src.stability.time_consistency import TimeConsistencyTest, TimeConsistencyResult
from src.stability.cross_class import CrossClassTest, CrossClassResult

__all__ = [
    "DefectionTest",
    "DefectionResult",
    "CoalitionTest",
    "CoalitionResult",
    "TimeConsistencyTest",
    "TimeConsistencyResult",
    "CrossClassTest",
    "CrossClassResult",
]
