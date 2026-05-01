"""
Stage 1: Task-based production core.

Following Acemoglu & Restrepo (2018, 2019, 2022):
- Output produced by continuum of tasks indexed [0, 1]
- Tasks are ordered by labor's comparative advantage (high indices = labor-intensive)
- An automation threshold I separates capital-only tasks [0, I] from labor tasks [I, 1]
- New tasks N can be created at the labor end, expanding the labor-eligible set
- Net change in labor share = -(displacement effect from rising I) + (reinstatement from N)

Production function:
Y = B * [int_{[0,I]} q_K(z)^((sigma-1)/sigma) dz + int_{[I,1+N]} q_L(z)^((sigma-1)/sigma) dz]^(sigma/(sigma-1))

where q_K, q_L are productivities, sigma is task elasticity (≠ KL elasticity).

Key result (Acemoglu-Restrepo 2019): labor share = (1 - I + N) * (productivity-weighted)
displacement effect — when I rises by dI without N rising, labor share falls.
reinstatement effect — when N rises with I held constant, labor share rises.
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class TaskBasedProduction:
    """
    State variables:
      I: automation threshold (fraction of original tasks done by capital)
      N: new tasks added (extends labor-eligible region beyond original 1.0)
      A_K: capital-augmenting productivity
      A_L: labor-augmenting productivity
      sigma: elasticity across tasks (default 1.5 per Humlum 2019, Acemoglu 2024)
    """
    I: float = 0.50         # Initial automation threshold (~half of tasks automated)
    N: float = 0.00         # Initial new tasks
    A_K: float = 1.0
    A_L: float = 1.0
    sigma: float = 1.5

    def output(self, K: float, L: float) -> tuple:
        """
        Compute output, factor returns, and labor share.

        At σ→1, use Cobb-Douglas limit explicitly.
        """
        s = self.sigma
        I = self.I
        N = self.N
        L_share_tasks = max(1.0 + N - I, 0.001)

        # Cobb-Douglas limit (σ ≈ 1)
        if abs(s - 1.0) < 0.02:
            # In this limit, with our task structure where tasks split into
            # measure I (capital) and 1+N-I (labor), Cobb-Douglas with shares
            # alpha = I / (1+N), 1-alpha = (1+N-I) / (1+N) is appropriate
            alpha = I / (1.0 + N)
            Y = (self.A_K * K)**alpha * (self.A_L * L)**(1.0 - alpha)
            if K <= 0 or L <= 0:
                return 0.0, 0.0, 0.0, 0.0
            r = alpha * Y / K
            w = (1.0 - alpha) * Y / L
            return Y, r, w, 1.0 - alpha

        # Effective inputs per CES aggregation
        K_eff = (I ** (1.0 / s)) * (self.A_K * K) ** ((s - 1.0) / s)
        L_eff = (L_share_tasks ** (1.0 / s)) * (self.A_L * L) ** ((s - 1.0) / s)
        bracket = K_eff + L_eff
        if bracket <= 0:
            return 0.0, 0.0, 0.0, 0.0

        Y = bracket ** (s / (s - 1.0))

        # Marginal products via envelope:
        # dY/dK: chain rule through bracket and K_eff
        # dY/dK = (Y/bracket) * dK_eff/dK = (Y/bracket) * (I^(1/s)) * A_K * ((s-1)/s) * (A_K*K)^(-1/s)
        # but cleaner: factor share = K_eff / bracket; then r = (Y/K) * (K_eff/bracket)
        K_share = K_eff / bracket
        L_share = L_eff / bracket
        r = (Y / max(K, 1e-9)) * K_share
        w = (Y / max(L, 1e-9)) * L_share

        return Y, r, w, L_share


def test_task_based():
    """Smoke test: at I=0.5, N=0, A_K=A_L=1, K=L=1: should give symmetric labor share ~0.5."""
    p = TaskBasedProduction(I=0.50, N=0.0, A_K=1.0, A_L=1.0, sigma=1.5)
    Y, r, w, ls = p.output(K=1.0, L=1.0)
    print(f"Test 1 (symmetric): Y={Y:.4f}, r={r:.4f}, w={w:.4f}, labor_share={ls:.4f}")
    assert abs(ls - 0.5) < 0.01, f"Expected labor share ~0.5, got {ls}"

    # Automate more tasks (I rises) → labor share should fall (displacement)
    p2 = TaskBasedProduction(I=0.65, N=0.0, A_K=1.0, A_L=1.0, sigma=1.5)
    Y2, r2, w2, ls2 = p2.output(K=1.0, L=1.0)
    print(f"Test 2 (more automation, I=0.65): labor_share={ls2:.4f}  (should be < 0.5)")
    assert ls2 < ls, "Displacement effect: rising I should lower labor share"

    # Add new tasks (N rises) → labor share should rise (reinstatement)
    p3 = TaskBasedProduction(I=0.65, N=0.20, A_K=1.0, A_L=1.0, sigma=1.5)
    Y3, r3, w3, ls3 = p3.output(K=1.0, L=1.0)
    print(f"Test 3 (reinstatement, I=0.65, N=0.20): labor_share={ls3:.4f}  (should rise back)")
    assert ls3 > ls2, "Reinstatement effect: rising N should raise labor share"

    # AI capital-augmenting productivity rises (A_K up) → labor share falls (under sigma > 1)
    p4 = TaskBasedProduction(I=0.50, N=0.0, A_K=1.5, A_L=1.0, sigma=1.5)
    Y4, r4, w4, ls4 = p4.output(K=1.0, L=1.0)
    print(f"Test 4 (capital-augmenting tech, A_K=1.5, sigma=1.5): labor_share={ls4:.4f}  (should fall, sigma>1)")
    # When sigma > 1, capital-augmenting tech reduces labor share
    assert ls4 < ls, "Productivity effect: A_K rise with sigma>1 reduces labor share"

    print("\nStage 1 task-based production: PASSED all sanity checks.\n")


if __name__ == "__main__":
    test_task_based()
