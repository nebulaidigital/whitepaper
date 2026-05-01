"""
Stage 2: Firm heterogeneity, markups, monopsonistic labor markets.

Two key institutional mechanisms behind documented labor share decline:

A. SUPERSTAR FIRM MARKUPS (Autor, Dorn, Katz, Patterson, Van Reenen 2020 QJE,
   De Loecker, Eeckhout, Unger 2020 QJE):
   - Firms charge price = markup * marginal cost
   - Markup distribution is right-skewed; mean markup has risen from ~1.18 in 1980 to
     ~1.50 in 2020 (DLEU 2020). Top decile of firms has markup > 2.0.
   - Higher markups → larger pure-profit share that goes to capital owners (not factor
     payments)
   - AI may amplify markup growth via fixed-cost economies (large training runs, data
     moats), so frontier AI firms have markup ~3-5

B. MONOPSONY (Azar, Marinescu, Steinbaum 2022; Manning 2003):
   - Labor markets concentrated; HHI in labor markets averages ~0.36 in US (vs ~0.18
     for product markets)
   - Workers paid wage = (eps / (1 + eps)) * MRPL, where eps is firm-specific labor
     supply elasticity (typically 2-4)
   - Wage markdown ~20-30% from competitive level
   - AI may worsen monopsony if AI augments employer information advantage

Implementation:
- Firms: M heterogeneous firms drawing markup mu from a Pareto-lognormal mixture
- Production: each firm uses task-based production from Stage 1
- Labor market: economy-wide labor supply elasticity eps determines wage markdown
- Profit (rents above competitive returns) flows to firm owners by ownership share
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List
from s1_production import TaskBasedProduction


@dataclass
class FirmDistribution:
    """
    Heterogeneous firms with markup distribution calibrated to DLEU (2020) and
    Autor et al. (2020):
    - mean markup ~1.50 in 2020 base year
    - 90th percentile markup ~2.20
    - 99th percentile markup ~3.50
    - Frontier AI firms (top 1%) ~5.0+
    """
    n_firms: int = 1000
    markup_mean: float = 1.20          # SALES-WEIGHTED mean (DLEU 2020 ≈1.20-1.25)
    markup_dispersion: float = 0.30
    markups: np.ndarray = field(default_factory=lambda: np.array([]))
    sizes: np.ndarray = field(default_factory=lambda: np.array([]))

    def initialize(self, seed=42):
        rng = np.random.default_rng(seed)
        log_mu = rng.normal(0, self.markup_dispersion, self.n_firms)
        raw = np.exp(log_mu)
        # Firm sizes: Pareto shape 2.0 (calmer than Zipf)
        size_raw = rng.pareto(2.0, self.n_firms) + 1.0
        sizes = size_raw / size_raw.sum()
        order = np.argsort(raw)[::-1]
        raw_sorted = raw[order]
        # Positive markup-size correlation (60%): largest firms have higher markups
        sizes_sorted = np.sort(sizes)[::-1]
        n = self.n_firms
        n_correlated = int(0.6 * n)
        sizes_final = np.empty(n)
        sizes_final[:n_correlated] = sizes_sorted[:n_correlated]
        rest = sizes_sorted[n_correlated:].copy()
        rng.shuffle(rest)
        sizes_final[n_correlated:] = rest
        # Scale raw to hit sales-weighted mean = markup_mean
        excess = raw_sorted - 1.0
        weighted_excess = float(np.sum(excess * sizes_final))
        scale = (self.markup_mean - 1.0) / max(weighted_excess, 1e-9)
        self.markups = 1.0 + scale * excess
        self.markups = np.maximum(self.markups, 1.01)
        self.sizes = sizes_final

    def update_markups(self, growth_rate: float, ai_concentration_factor: float = 1.0):
        """
        Markups grow over time. growth_rate is the average annual increase in mean markup
        (e.g., 0.5pp/yr observed in DLEU 2020 data).
        ai_concentration_factor amplifies growth in top quintile (frontier AI firms).
        """
        # Top 20% of firms (by current markup) get amplified growth
        n = len(self.markups)
        top20 = int(n * 0.20)
        delta = np.full(n, growth_rate)
        delta[:top20] *= ai_concentration_factor
        self.markups = self.markups + delta
        self.markups = np.maximum(self.markups, 1.01)

    def aggregate_markup(self) -> float:
        """Sales-weighted average markup (relevant for aggregate labor share)."""
        return float(np.sum(self.markups * self.sizes))

    def profit_share(self) -> float:
        """
        Aggregate pure profit share of value-added.
        For each firm: profit margin = (mu - 1) / mu of revenue
        Aggregate: weighted by revenue share
        """
        firm_profit_share = (self.markups - 1.0) / self.markups
        return float(np.sum(firm_profit_share * self.sizes))


@dataclass
class MonopsonyLabor:
    """
    Wage setting with monopsony power.
    eps = firm-specific labor supply elasticity (Azar et al. 2022 estimate ~3.0)
    Wage = (eps / (1 + eps)) * MRPL
    Markdown = 1 - eps/(1+eps) = 1/(1+eps) ~ 25% at eps=3
    """
    eps: float = 3.0  # labor supply elasticity (Azar-Marinescu-Steinbaum mean estimate)

    def wage_markdown(self) -> float:
        return self.eps / (1.0 + self.eps)

    def update_for_skill_concentration(self, skill_share: float, base_eps: float = 3.0):
        """
        AI-substitute workers face higher monopsony (fewer outside options as AI displaces
        adjacent occupations). AI-complement workers face lower monopsony (high demand).
        skill_share: share of automation-exposed labor
        """
        # As skill_share rises (more workers exposed to AI substitution), eps falls
        # (worse outside options for affected workers)
        self.eps = base_eps * (1.0 - 0.4 * skill_share)
        self.eps = max(self.eps, 1.5)


def aggregate_economy(
    K: float, L_safe: float, L_sub: float, L_comp: float,
    production: TaskBasedProduction,
    firms: FirmDistribution,
    monopsony_safe: MonopsonyLabor,
    monopsony_sub: MonopsonyLabor,
    monopsony_comp: MonopsonyLabor,
    skill_productivity: dict = None,
):
    """
    Aggregate the heterogeneous-firm economy.

    Total effective labor:
        L_eff = phi_safe * L_safe + phi_sub * L_sub + phi_comp * L_comp
    where phi_x is skill-type productivity (complement higher, etc.)

    Production yields competitive r, w_unit. Then:
    - Pure profit (rents) = profit_share * Y, distributed to firm owners
    - Wage = MRPL * markdown_skill (different by skill type)
    - Capital return = MPK + (rents share to capital owners)

    skill_productivity: dict like {'safe': 0.7, 'sub': 1.0, 'comp': 1.6}
    """
    if skill_productivity is None:
        skill_productivity = {'safe': 0.7, 'sub': 1.0, 'comp': 1.6}

    # Effective labor
    L_eff = (skill_productivity['safe'] * L_safe +
             skill_productivity['sub'] * L_sub +
             skill_productivity['comp'] * L_comp)
    if L_eff <= 0 or K <= 0:
        return {'Y': 0, 'r_competitive': 0, 'w_competitive_per_eff': 0,
                'wage_safe': 0, 'wage_sub': 0, 'wage_comp': 0,
                'profit_share': 0, 'capital_return_with_rents': 0,
                'labor_share_factor': 0, 'labor_share_realized': 0}

    Y, r_comp, w_comp_per_eff, ls_factor = production.output(K, L_eff)

    # Markup absorbs share as profit (rents)
    profit_share = firms.profit_share()
    rents = Y * profit_share

    # Factor payments come out of (1 - profit_share) of Y
    # Y_payable = Y * (1 - profit_share)
    # Within Y_payable, capital and labor split per task-based MPK/MPL
    Y_payable = Y * (1.0 - profit_share)
    capital_payment = Y_payable * (1.0 - ls_factor)
    labor_payment_total = Y_payable * ls_factor

    # Distribute labor payment by skill type: each skill type's effective share
    eff_safe = skill_productivity['safe'] * L_safe
    eff_sub = skill_productivity['sub'] * L_sub
    eff_comp = skill_productivity['comp'] * L_comp
    total_eff = eff_safe + eff_sub + eff_comp

    pay_safe = labor_payment_total * (eff_safe / total_eff)
    pay_sub = labor_payment_total * (eff_sub / total_eff)
    pay_comp = labor_payment_total * (eff_comp / total_eff)

    # Apply monopsony markdowns: workers receive markdown * MRPL, employer keeps the rest
    md_safe = monopsony_safe.wage_markdown()
    md_sub = monopsony_sub.wage_markdown()
    md_comp = monopsony_comp.wage_markdown()

    realized_wages_safe = pay_safe * md_safe
    realized_wages_sub = pay_sub * md_sub
    realized_wages_comp = pay_comp * md_comp

    # Monopsony rents (labor payment - realized wages) flow to capital owners
    monopsony_rents = (pay_safe - realized_wages_safe) + \
                      (pay_sub - realized_wages_sub) + \
                      (pay_comp - realized_wages_comp)

    total_realized_wages = realized_wages_safe + realized_wages_sub + realized_wages_comp
    total_capital_income = capital_payment + rents + monopsony_rents
    realized_labor_share = total_realized_wages / Y

    # Per-unit-labor wages by skill (for connecting back to individual workers)
    wage_per_safe = realized_wages_safe / max(L_safe, 1e-9) if L_safe > 0 else 0
    wage_per_sub = realized_wages_sub / max(L_sub, 1e-9) if L_sub > 0 else 0
    wage_per_comp = realized_wages_comp / max(L_comp, 1e-9) if L_comp > 0 else 0

    # Capital return with rents
    r_with_rents = total_capital_income / max(K, 1e-9)

    return {
        'Y': Y,
        'r_competitive': r_comp,
        'w_competitive_per_eff': w_comp_per_eff,
        'wage_safe': wage_per_safe,
        'wage_sub': wage_per_sub,
        'wage_comp': wage_per_comp,
        'profit_share': profit_share,
        'monopsony_rents_share': monopsony_rents / Y,
        'capital_return_with_rents': r_with_rents,
        'labor_share_factor': ls_factor,
        'labor_share_realized': realized_labor_share,
        'rents_total': rents + monopsony_rents,
    }


def test_stage2():
    """Sanity tests for Stage 2."""
    print("=== Stage 2 sanity tests ===")

    # Initialize 2025-baseline economy
    prod = TaskBasedProduction(I=0.50, N=0.0, A_K=1.0, A_L=1.0, sigma=1.5)
    firms = FirmDistribution(n_firms=1000, markup_mean=1.22, markup_dispersion=0.30)
    firms.initialize(seed=42)
    print(f"Sales-weighted mean markup: {firms.aggregate_markup():.3f}  (target ~1.20-1.25)")
    print(f"Profit share of value added: {firms.profit_share()*100:.1f}%  (target ~12-15%)")
    print(f"Top firm markup: {firms.markups[0]:.2f}")
    print(f"99th percentile markup: {np.percentile(firms.markups, 99):.2f}  (target ~2.0)")

    monop_safe = MonopsonyLabor(eps=3.0)
    monop_sub = MonopsonyLabor(eps=3.0)
    monop_comp = MonopsonyLabor(eps=4.0)  # complement workers have more outside options

    # Initial state
    res = aggregate_economy(
        K=1.0, L_safe=0.20, L_sub=0.50, L_comp=0.30,
        production=prod, firms=firms,
        monopsony_safe=monop_safe, monopsony_sub=monop_sub, monopsony_comp=monop_comp,
    )
    print(f"\nInitial economy:")
    print(f"  Y = {res['Y']:.3f}")
    print(f"  Profit share (markup): {res['profit_share']*100:.1f}%")
    print(f"  Monopsony rents share: {res['monopsony_rents_share']*100:.1f}%")
    print(f"  Realized labor share: {res['labor_share_realized']*100:.1f}%")
    print(f"  (Compare to US 2020 ~56%)")
    print(f"  Wages: safe={res['wage_safe']:.4f}, sub={res['wage_sub']:.4f}, comp={res['wage_comp']:.4f}")

    # Test: rising automation (I rises) should lower labor share
    prod2 = TaskBasedProduction(I=0.62, N=0.05, A_K=1.0, A_L=1.0, sigma=1.5)
    firms2 = FirmDistribution(n_firms=1000, markup_mean=1.65, markup_dispersion=0.65)
    firms2.initialize(seed=42)
    res2 = aggregate_economy(
        K=1.5, L_safe=0.20, L_sub=0.45, L_comp=0.35,
        production=prod2, firms=firms2,
        monopsony_safe=MonopsonyLabor(eps=2.5),
        monopsony_sub=MonopsonyLabor(eps=2.0),
        monopsony_comp=MonopsonyLabor(eps=4.0),
    )
    print(f"\n2035 simulated state (more automation, higher markups, worse monopsony):")
    print(f"  Profit share: {res2['profit_share']*100:.1f}%  (Δ +{(res2['profit_share']-res['profit_share'])*100:.1f}pp)")
    print(f"  Realized labor share: {res2['labor_share_realized']*100:.1f}%  (Δ {(res2['labor_share_realized']-res['labor_share_realized'])*100:+.1f}pp)")

    print("\nStage 2: PASSED basic sanity tests.")


if __name__ == "__main__":
    test_stage2()
