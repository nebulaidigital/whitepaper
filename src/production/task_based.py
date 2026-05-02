"""Task-based production module (Acemoglu-Restrepo).

Ported from prototype/s1_production.py with type hints and a structured
return type. Implements the three core comparative statics:
    1. Displacement: ∂(labor share)/∂I < 0
    2. Reinstatement: ∂(labor share)/∂N > 0
    3. Productivity bias: ∂(labor share)/∂A_K < 0 when σ > 1

References
----------
- Acemoglu & Restrepo (2018), "The Race between Man and Machine"
- Acemoglu & Restrepo (2019), "Automation and New Tasks", JEP 33(2)
- Acemoglu & Restrepo (2022), "Tasks, Automation, and the Rise in U.S.
  Wage Inequality", Econometrica 90(5)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProductionResult:
    """Output of a single production-function evaluation.

    Attributes
    ----------
    Y : aggregate output
    r : marginal product of capital (rental rate before markups/monopsony)
    w_unit : marginal product per unit effective labor
    labor_share_factor : factor labor share before markups/monopsony extraction
        — this is the model intermediate, NOT the realized labor share that
        BLS reports. Realized labor share = factor share × (1 - markup_share)
        × monopsony_markdown. Confusing these is documented in CLAUDE.md as
        a likely failure mode.
    """

    Y: float
    r: float
    w_unit: float
    labor_share_factor: float


@dataclass
class TaskBasedProduction:
    """Acemoglu-Restrepo task-based production function.

    Parameters
    ----------
    I : automation threshold ∈ [0, 1+N]; tasks z<I done by capital, z≥I by labor
    N : new tasks added at the labor-eligible end
    A_K : capital-augmenting productivity
    A_L : labor-augmenting productivity
    sigma : task elasticity of substitution
        — defaults to 1.5 per Acemoglu-Restrepo 2022 Table 3 mid-estimate
        — Cobb-Douglas branch used when |σ - 1| < 0.02 for numerical safety
    """

    I: float = 0.50
    N: float = 0.00
    A_K: float = 1.0
    A_L: float = 1.0
    sigma: float = 1.5  # Acemoglu-Restrepo 2022 Table 3 mean

    def output(self, K: float, L: float) -> ProductionResult:
        """Compute output, factor returns, and labor share at given (K, L)."""
        s = self.sigma
        I = self.I
        N = self.N
        L_share_tasks = max(1.0 + N - I, 0.001)

        # Cobb-Douglas branch (σ ≈ 1)
        if abs(s - 1.0) < 0.02:
            alpha = I / (1.0 + N)
            if K <= 0 or L <= 0:
                return ProductionResult(0.0, 0.0, 0.0, 0.0)
            Y = (self.A_K * K) ** alpha * (self.A_L * L) ** (1.0 - alpha)
            r = alpha * Y / K
            w = (1.0 - alpha) * Y / L
            return ProductionResult(Y, r, w, 1.0 - alpha)

        # General CES branch
        K_eff = (I ** (1.0 / s)) * (self.A_K * K) ** ((s - 1.0) / s)
        L_eff = (L_share_tasks ** (1.0 / s)) * (self.A_L * L) ** ((s - 1.0) / s)
        bracket = K_eff + L_eff
        if bracket <= 0:
            return ProductionResult(0.0, 0.0, 0.0, 0.0)

        Y = bracket ** (s / (s - 1.0))
        K_share = K_eff / bracket
        L_share = L_eff / bracket
        r = (Y / max(K, 1e-9)) * K_share
        w = (Y / max(L, 1e-9)) * L_share
        return ProductionResult(Y, r, w, L_share)

    def update_automation(self, dI: float, dN: float) -> None:
        """Apply automation expansion (dI) and reinstatement (dN) for one period.

        I is capped at 0.95 to prevent labor-eligible task region collapsing
        to zero, which is empirically implausible and numerically unstable.
        """
        self.I = min(0.95, self.I + dI)
        self.N = self.N + dN

    def update_productivity(self, gK: float, gL: float) -> None:
        """Apply growth rates to A_K and A_L for one period."""
        self.A_K *= 1.0 + gK
        self.A_L *= 1.0 + gL
