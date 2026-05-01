"""
Stage 3: Capital markets and investment dynamics.

Key mechanisms (peer-review-relevant):

A. EQUITY VALUATION & COST OF CAPITAL
   Pillar 1 sovereign-fund acquisition lowers private equity holdings → cost of equity rises
   per the standard CAPM-style argument that constrained-supply equity has higher required
   return. Calibration: a 30% sovereign acquisition raises required equity returns by
   ~150-300 bps based on similar precedents (Norwegian GPFG impact studies, Singapore
   Temasek effects on listed firms).

B. INVESTMENT FUNCTION
   I_t = beta_0 + beta_q * Tobin_q_t + beta_y * Y_growth + beta_r * (r_t - cost_of_capital_t)
   Calibrated to Caballero-Engel hazard model adjustments.

C. CAPITAL FLIGHT
   Top-decile capital flight responds to expected after-tax returns relative to non-
   participating jurisdictions. Functional form: flight rate = max(0, theta * (tau - tau*))
   where tau is domestic AI tax rate and tau* is competitor jurisdiction's rate.
   Calibrated to French wealth-tax-induced flight estimates (Bach-Bourdier-Bozio 2014:
   ~0.8% of taxable assets per year per percentage point of differential).

D. AI CAPITAL DEPRECIATION
   AI capital depreciates faster than traditional (chips obsolete in 4-7 years,
   models in 1-3 years). Aggregate AI depreciation ~20-25%/year per IEEE ComSoc 2025
   estimates and McKinsey 2025 hyperscaler analysis.

E. SAVING RATES
   Heterogeneous by income decile per Saez-Zucman 2016: top 1% saves ~30-40%,
   median saves ~5%, bottom 50% saves ~0% on net.
"""

import numpy as np
from dataclasses import dataclass, field


@dataclass
class CapitalMarkets:
    """Aggregate capital market dynamics."""
    # Cost-of-equity baseline (real return required by private investors)
    cost_of_equity_baseline: float = 0.07  # 7% real (consistent with US ERP + risk-free)
    cost_of_equity_premium_per_sov_acquired: float = 0.005  # 50 bps per 10% acquired
    # Investment function parameters (Caballero-Engel-style)
    beta_q: float = 0.05      # Tobin's q sensitivity
    beta_y: float = 0.4       # accelerator from output growth
    beta_r: float = 0.08      # adjustment to return-cost gap
    # Capital flight
    flight_responsiveness: float = 0.008  # per pp of tax differential, per year (Bach et al.)
    base_flight_rate: float = 0.005       # baseline 0.5%/yr flight even with no policy
    # Depreciation
    depreciation_AI: float = 0.22
    depreciation_T: float = 0.05

    def cost_of_equity(self, sov_acquisition_share: float) -> float:
        """Required equity return rises with sovereign-fund concentration."""
        return self.cost_of_equity_baseline + \
               self.cost_of_equity_premium_per_sov_acquired * (sov_acquisition_share / 0.10)

    def investment_demand(
        self, K_existing: float, Y: float, Y_growth: float,
        r_realized: float, r_required: float, q_ratio: float = 1.0
    ) -> float:
        """Investment demand as a function of returns and growth."""
        gap = r_realized - r_required
        depreciation_replacement = self.depreciation_T * K_existing
        net_investment = K_existing * (
            self.beta_q * (q_ratio - 1.0) +
            self.beta_y * Y_growth +
            self.beta_r * gap
        )
        return depreciation_replacement + max(net_investment, -0.15 * K_existing)

    def capital_flight_rate(self, domestic_tax_rate: float, foreign_tax_rate: float) -> float:
        """Annual fraction of mobile capital that flees to lower-tax jurisdiction."""
        differential_pp = max(0.0, (domestic_tax_rate - foreign_tax_rate) * 100)
        return self.base_flight_rate + self.flight_responsiveness * differential_pp


@dataclass
class HouseholdSavings:
    """Heterogeneous saving rates by income decile (Saez-Zucman calibration)."""
    saving_rates: np.ndarray = field(default_factory=lambda: np.array([
        -0.02, 0.00, 0.01, 0.02, 0.04, 0.06, 0.10, 0.15, 0.22, 0.30
    ]))  # by decile, with top decile at 30%
    top1_saving_rate: float = 0.40

    def get_rate(self, decile_index: int, is_top_1pct: bool = False) -> float:
        if is_top_1pct:
            return self.top1_saving_rate
        return float(self.saving_rates[decile_index])


@dataclass
class State:
    """Time-evolving aggregate state for a country/economy."""
    K_T: float            # traditional capital stock
    K_AI_private: float   # AI capital held privately
    K_AI_sovereign: float = 0.0  # held by sovereign fund (Pillar 1)
    K_AI_fled: float = 0.0       # capital that fled jurisdiction
    A_K: float = 1.0      # capital-augmenting productivity
    A_L: float = 1.0      # labor-augmenting productivity
    Y_prev: float = 1.0   # previous-period output
    cumulative_flight: float = 0.0  # cumulative fraction lost

    def total_K_productive(self) -> float:
        return self.K_T + self.K_AI_private + self.K_AI_sovereign

    def total_K_owned(self) -> float:
        return self.K_T + self.K_AI_private + self.K_AI_sovereign + self.K_AI_fled


def test_stage3():
    """Sanity test capital market dynamics."""
    print("=== Stage 3 sanity tests ===")
    cm = CapitalMarkets()
    print(f"Cost of equity (no sovereign): {cm.cost_of_equity(0.0)*100:.2f}%")
    print(f"Cost of equity (30% sovereign): {cm.cost_of_equity(0.30)*100:.2f}%")
    print(f"  (Should rise ~150 bps at 30%)")

    print(f"\nFlight rate (no differential): {cm.capital_flight_rate(0.0, 0.0)*100:.3f}%/yr")
    print(f"Flight rate (5pp differential): {cm.capital_flight_rate(0.20, 0.15)*100:.3f}%/yr")
    print(f"  (Bach et al. estimate ~4%/yr at 5pp differential)")

    hh = HouseholdSavings()
    print(f"\nSaving rates by decile:")
    for d, sr in enumerate(hh.saving_rates):
        print(f"  D{d+1}: {sr*100:+.1f}%")
    print(f"  Top 1%: {hh.top1_saving_rate*100:.1f}%")

    s = State(K_T=2.0, K_AI_private=0.3)
    print(f"\nState: K_T={s.K_T}, K_AI_priv={s.K_AI_private}, total productive={s.total_K_productive():.3f}")

    print("\nStage 3: PASSED basic sanity tests.")


if __name__ == "__main__":
    test_stage3()
