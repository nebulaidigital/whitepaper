"""
Stage 4: Integrated dynamic model.

Brings together Stages 1-3 into an annual time-step simulation. Tracks:
- Production and factor returns (task-based + heterogeneous firms + monopsony)
- Wealth distribution by household decile (with skill type and capital-mobility heterogeneity)
- Capital market dynamics (sovereign acquisition, flight, depreciation, investment)
- Standard inequality metrics (Gini, P90/P10, top 1% share, labor share)

Designed to backtest against US 2015-2025 observed data:
- Labor share fell from ~58% (2015) to ~56% (2025) per BLS
- Top 1% wealth share rose from ~28% (2015) to ~30% (2025) per Saez-Zucman
- Real GDP grew ~22% cumulative (BEA)
- Aggregate markup rose from ~1.18 (2015) to ~1.22 (2025) per DLEU updated
- AI capital share of total grew from ~2% (2015) to ~6% (2025)

If the model can reproduce 2015-2025 within reasonable tolerance, projections
2025-2035 carry weight.
"""

import numpy as np
from dataclasses import dataclass, field
from s1_production import TaskBasedProduction
from s2_firms_labor import FirmDistribution, MonopsonyLabor, aggregate_economy
from s3_capital_markets import CapitalMarkets, HouseholdSavings, State


@dataclass
class HouseholdEconomy:
    """Heterogeneous household population: 10 deciles + top-1 % subdivision."""
    n_per_decile: int = 1000
    # Skill type: 0 = AI-safe (manual), 1 = AI-substitute (clerical/cognitive routine),
    #             2 = AI-complement (high-skill cognitive)
    # Skill distribution (Frey-Osborne 2017, BLS occupation classifications):
    skill_by_decile: list = field(default_factory=lambda: [
        # D1   D2   D3   D4   D5   D6   D7   D8   D9   D10
        0,   0,   1,   1,   1,   1,   1,   2,   2,   2
    ])
    # Wealth distribution (% of total wealth by decile, US 2025 SCF approximation)
    wealth_decile: list = field(default_factory=lambda: [
        0.001, 0.003, 0.005, 0.008, 0.013, 0.020, 0.033, 0.060, 0.097, 0.760
    ])
    top1_wealth: float = 0.30        # within top decile, this share goes to top 1%
    # Wage endowment (units of effective labor, before market wage applied)
    labor_endow_decile: list = field(default_factory=lambda: [
        0.5, 0.7, 0.9, 1.0, 1.2, 1.5, 1.9, 2.5, 3.5, 6.0
    ])
    top1_labor_endow: float = 15.0
    # MPC (Marginal Propensity to Consume)
    mpc_decile: list = field(default_factory=lambda: [
        0.95, 0.95, 0.95, 0.93, 0.91, 0.87, 0.83, 0.78, 0.70, 0.55
    ])
    top1_mpc: float = 0.40

    def initialize(self, total_wealth: float = 1000.0) -> dict:
        """Return arrays of household state."""
        n10 = self.n_per_decile
        N = 10 * n10
        # Subtract top 1% from top decile
        top1_n = max(1, n10 // 100)  # 1% of decile = 0.1% of pop
        wealth = np.zeros(N)
        labor_endow = np.zeros(N)
        mpc = np.zeros(N)
        skill = np.zeros(N, dtype=int)

        for d in range(10):
            s, e = d * n10, (d + 1) * n10
            wealth[s:e] = self.wealth_decile[d] * total_wealth / n10
            labor_endow[s:e] = self.labor_endow_decile[d]
            mpc[s:e] = self.mpc_decile[d]
            skill[s:e] = self.skill_by_decile[d]
        # Top 1% (last top1_n households of D10)
        top1_start = N - top1_n
        next99_share = self.wealth_decile[9] - self.top1_wealth
        wealth[9 * n10:top1_start] = next99_share * total_wealth / (top1_start - 9 * n10)
        wealth[top1_start:] = self.top1_wealth * total_wealth / top1_n
        labor_endow[top1_start:] = self.top1_labor_endow
        mpc[top1_start:] = self.top1_mpc
        skill[top1_start:] = 2  # top 1% are complement (CEOs, owners)

        # Each household holds a mix of K_T and K_AI proportional to current AI share
        # (we'll track this in the dynamic model)
        return {
            'wealth': wealth, 'labor_endow': labor_endow, 'mpc': mpc, 'skill': skill,
            'N': N, 'top1_n': top1_n, 'n_per_decile': n10
        }


@dataclass
class Scenario:
    """Defines policy/exogenous parameters for one scenario."""
    name: str
    # AI productivity growth
    ai_tfp_growth: float = 0.015
    # Automation expansion: rate at which I (automation threshold) rises per year
    automation_rate: float = 0.012        # I rises ~1.2 pp/yr (Acemoglu-Restrepo 2022 calibration)
    # New tasks reinstatement rate
    reinstatement_rate: float = 0.005     # N rises ~0.5 pp/yr (slower than displacement)
    # Markup growth (excess pricing power)
    markup_growth: float = 0.005          # +0.5 pp/yr (DLEU pace)
    # Monopsony tightening
    monopsony_tightening: float = 0.05    # eps falls 5%/yr for AI-substitute workers
    # Pillar 1: sovereign fund acquisition rate
    sov_acquisition_rate: float = 0.0     # 0 = none, 0.05 = 5%/yr until 30% cap
    sov_acquisition_cap: float = 0.30
    # Pillar 4: portable benefits / reskilling effect on automation_rate experienced by labor
    reskilling_buffer: float = 0.0        # 0 = none, 1.0 = labor experiences zero displacement
    # Pillar 5: open weights effect on markup growth
    open_weights_markup_dampening: float = 0.0   # 0 = none, 1.0 = markup growth fully dampened
    # Pillar 6: AI tax rate on top-decile capital income
    ai_tax_rate: float = 0.0
    # Foreign tax rate (for capital-flight calculation; lower than domestic if Pillar 6 active)
    foreign_tax_rate: float = 0.0


SCENARIOS = {
    'historical': Scenario(
        name='Historical 2015-2025 backtest',
        ai_tfp_growth=0.012, automation_rate=0.010, reinstatement_rate=0.005,
        markup_growth=0.0035, monopsony_tightening=0.02,
    ),
    'patchwork_2025_2035': Scenario(
        name='Patchwork (current trajectory) 2025-2035',
        ai_tfp_growth=0.018, automation_rate=0.018, reinstatement_rate=0.004,
        markup_growth=0.005, monopsony_tightening=0.04,
    ),
    'sf_consensus': Scenario(
        name='SF Consensus (AGI-adjacent acceleration)',
        ai_tfp_growth=0.040, automation_rate=0.030, reinstatement_rate=0.003,
        markup_growth=0.008, monopsony_tightening=0.06,
    ),
    'participatory_universal': Scenario(
        name='Participatory framework (full)',
        ai_tfp_growth=0.018, automation_rate=0.018, reinstatement_rate=0.012,
        markup_growth=0.005, monopsony_tightening=0.04,
        sov_acquisition_rate=0.05, sov_acquisition_cap=0.30,
        reskilling_buffer=0.50,
        open_weights_markup_dampening=0.40,
        ai_tax_rate=0.30, foreign_tax_rate=0.10,
    ),
    'participatory_capflight_test': Scenario(
        name='Participatory + adverse capital flight assumption',
        ai_tfp_growth=0.018, automation_rate=0.018, reinstatement_rate=0.012,
        markup_growth=0.005, monopsony_tightening=0.04,
        sov_acquisition_rate=0.05, sov_acquisition_cap=0.30,
        reskilling_buffer=0.50,
        open_weights_markup_dampening=0.40,
        ai_tax_rate=0.30, foreign_tax_rate=0.05,  # bigger differential
    ),
    'coerced_2032': Scenario(
        name='Coerced redistribution (post-crisis 2032)',
        ai_tfp_growth=0.005,  # capital strike + capability caps
        automation_rate=0.008, reinstatement_rate=0.003,
        markup_growth=0.0,  # caps imposed
        monopsony_tightening=-0.02,
        sov_acquisition_rate=0.0,
        ai_tax_rate=0.70,    # confiscatory windfall tax
        foreign_tax_rate=0.00,
    ),
}


def gini(x):
    x = np.sort(np.maximum(x, 0))
    n = len(x); s = x.sum()
    if s <= 0: return 0.0
    return float((2 * np.sum(np.arange(1, n + 1) * x) - (n + 1) * s) / (n * s))


def p90_p10(x):
    x = np.maximum(x, 1e-9)
    return float(np.percentile(x, 90) / np.percentile(x, 10))


def top1_share(x, top1_n):
    sx = np.sort(x)[::-1]
    return float(sx[:top1_n].sum() / max(sx.sum(), 1e-9))


def run_dynamic(
    scenario: Scenario,
    n_years: int,
    initial_state: dict = None,
    seed: int = 42,
    start_year: int = None,
) -> dict:
    """
    Run integrated dynamic simulation.

    Returns dict with annual time series of all key indicators.
    Uses per-capita normalization to avoid runaway capital deepening.
    """
    np.random.seed(seed)

    # Initialize household economy
    he = HouseholdEconomy()
    hh_state = he.initialize(total_wealth=400.0)  # K/Y ≈ 4 (US empirical)
    wealth_T = hh_state['wealth'].copy() * 0.94
    wealth_AI = hh_state['wealth'].copy() * 0.06
    labor_endow = hh_state['labor_endow']
    mpc = hh_state['mpc']
    skill = hh_state['skill']
    N = hh_state['N']
    top1_n = hh_state['top1_n']
    n10 = hh_state['n_per_decile']

    if initial_state is None:
        # Calibrated baseline for 2015 (sigma=1, I=0.20 to match initial labor share ~58%)
        if scenario.name.startswith('Historical'):
            prod = TaskBasedProduction(I=0.20, N=0.0, A_K=1.0, A_L=1.0, sigma=1.0)
            firms = FirmDistribution(n_firms=1000, markup_mean=1.18, markup_dispersion=0.30)
        else:
            prod = TaskBasedProduction(I=0.26, N=0.0, A_K=1.0, A_L=1.0, sigma=1.0)
            firms = FirmDistribution(n_firms=1000, markup_mean=1.22, markup_dispersion=0.30)
        firms.initialize(seed=seed)
    else:
        prod = initial_state['production']
        firms = initial_state['firms']

    monop_safe = MonopsonyLabor(eps=10.0)
    monop_sub = MonopsonyLabor(eps=10.0)
    monop_comp = MonopsonyLabor(eps=15.0)

    cm = CapitalMarkets()
    sov_K_AI = 0.0
    fled_K_AI = 0.0

    # Population growth (slows over time per US trend)
    L_growth_rate = 0.005  # 0.5%/yr
    A_growth_baseline = scenario.ai_tfp_growth  # baseline TFP growth

    H = {k: [] for k in [
        'year', 'Y', 'gdp_idx', 'gdp_pc_idx', 'labor_share', 'profit_share',
        'monopsony_rents_share', 'top1_wealth_share', 'top10_wealth_share',
        'gini_wealth', 'gini_income', 'p90_p10_income',
        'wage_safe', 'wage_sub', 'wage_comp', 'mean_markup',
        'I_threshold', 'N_new_tasks', 'sov_share_AI', 'fled_share_AI',
        'consumption_by_decile', 'income_by_decile', 'cap_flight_rate',
        'K_per_Y', 'r_capital'
    ]}

    Y_prev = None
    Y_t0 = None
    income_t0 = None
    L_scale = 1.0  # tracks labor force growth

    if start_year is None:
        start_year = 2015 if scenario.name.startswith('Historical') else 2025

    for t in range(n_years):
        # 1. Update parameters
        if t > 0:
            net_displacement = scenario.automation_rate * (1 - scenario.reskilling_buffer * 0.5)
            net_reinstatement = scenario.reinstatement_rate + scenario.automation_rate * (scenario.reskilling_buffer * 0.5)
            prod.I = min(0.95, prod.I + net_displacement)
            prod.N = prod.N + net_reinstatement
            # AI productivity grows in capital-augmenting only
            prod.A_K *= (1 + scenario.ai_tfp_growth)
            prod.A_L *= (1 + scenario.ai_tfp_growth * 0.2)

            effective_markup_growth = scenario.markup_growth * (1 - scenario.open_weights_markup_dampening)
            firms.update_markups(growth_rate=effective_markup_growth, ai_concentration_factor=1.5)

            mono_shock = scenario.monopsony_tightening * (1 - scenario.reskilling_buffer)
            monop_sub.eps = max(2.0, monop_sub.eps * (1 - mono_shock))
            monop_safe.eps = max(2.5, monop_safe.eps * (1 - mono_shock * 0.5))

            # Population growth scales effective labor
            L_scale *= (1 + L_growth_rate)

        # 2. Effective labor (with growth)
        L_safe = labor_endow[skill == 0].sum() * L_scale
        L_sub = labor_endow[skill == 1].sum() * L_scale
        L_comp = labor_endow[skill == 2].sum() * L_scale

        K_total_owned = wealth_T.sum() + wealth_AI.sum() + sov_K_AI + fled_K_AI
        K_productive = wealth_T.sum() + wealth_AI.sum() + sov_K_AI

        # 3. Production
        agg = aggregate_economy(
            K=K_productive, L_safe=L_safe, L_sub=L_sub, L_comp=L_comp,
            production=prod, firms=firms,
            monopsony_safe=monop_safe, monopsony_sub=monop_sub, monopsony_comp=monop_comp,
        )
        Y = agg['Y']
        if Y_t0 is None:
            Y_t0 = Y
            Y_prev = Y
        Y_growth = (Y - Y_prev) / max(Y_prev, 1e-9)
        Y_prev = Y

        # 4. Household incomes
        wage_income = np.zeros(N)
        wage_income[skill == 0] = labor_endow[skill == 0] * agg['wage_safe']
        wage_income[skill == 1] = labor_endow[skill == 1] * agg['wage_sub']
        wage_income[skill == 2] = labor_endow[skill == 2] * agg['wage_comp']

        sov_div = (sov_K_AI * agg['capital_return_with_rents']) / N
        cap_income_priv = (wealth_T + wealth_AI) * agg['capital_return_with_rents']
        cap_income = cap_income_priv + sov_div

        income_pre_tax = wage_income + cap_income

        # 5. AI tax
        ai_tax_paid = np.zeros(N)
        if scenario.ai_tax_rate > 0:
            top10_idx = slice(9 * n10, N)
            ai_tax_paid[top10_idx] = cap_income[top10_idx] * scenario.ai_tax_rate
        income_post_tax = income_pre_tax - ai_tax_paid
        if income_t0 is None:
            income_t0 = income_post_tax.copy()

        # 6. Consumption (subsistence floor scales with output to keep relevance)
        cons_floor = 0.005 * (Y / Y_t0) ** 0.5
        consumption = np.maximum(income_post_tax * mpc, cons_floor)

        # 7. Saving and capital accumulation
        saving = income_post_tax - consumption

        # Per-decile aggregate saving update (avoid per-household loop for speed)
        for d in range(10):
            ds, de = d * n10, (d + 1) * n10
            tot_dec = wealth_T[ds:de] + wealth_AI[ds:de]
            ai_share_dec = wealth_AI[ds:de] / np.maximum(tot_dec, 1e-9)
            # Top decile drifts up; bottom drifts down
            if d == 9:
                ai_share_dec = np.minimum(0.40, ai_share_dec + 0.005)
            else:
                ai_share_dec = np.maximum(0.02, ai_share_dec - 0.001)
            sav_d = saving[ds:de]
            pos_mask = sav_d > 0
            wealth_T[ds:de][pos_mask] += sav_d[pos_mask] * (1 - ai_share_dec[pos_mask])
            wealth_AI[ds:de][pos_mask] += sav_d[pos_mask] * ai_share_dec[pos_mask]
            # Disaving: drop from T first
            neg = ~pos_mask
            for i, gi in enumerate(np.where(neg)[0]):
                actual_i = ds + gi
                amt = saving[actual_i]
                if abs(amt) <= wealth_T[actual_i]:
                    wealth_T[actual_i] += amt
                else:
                    rem = amt + wealth_T[actual_i]
                    wealth_T[actual_i] = 0
                    wealth_AI[actual_i] = max(0, wealth_AI[actual_i] + rem)

        # 8. Depreciation
        wealth_AI *= (1 - cm.depreciation_AI)
        wealth_T *= (1 - cm.depreciation_T)
        sov_K_AI *= (1 - cm.depreciation_AI)
        fled_K_AI *= (1 - cm.depreciation_AI)

        # 9. Sovereign acquisition
        if scenario.sov_acquisition_rate > 0:
            top10_AI = wealth_AI[9 * n10:].sum()
            current_sov_share = sov_K_AI / max(top10_AI + sov_K_AI, 1e-9)
            if current_sov_share < scenario.sov_acquisition_cap:
                acquire = top10_AI * scenario.sov_acquisition_rate
                sov_K_AI += acquire
                wealth_AI[9 * n10:] *= (1 - scenario.sov_acquisition_rate)

        # 10. Capital flight
        flight_rate = 0.0
        if scenario.ai_tax_rate > scenario.foreign_tax_rate:
            flight_rate = cm.capital_flight_rate(scenario.ai_tax_rate, scenario.foreign_tax_rate)
            top1_idx = slice(N - top1_n, N)
            flight_amount = wealth_AI[top1_idx].sum() * flight_rate
            wealth_AI[top1_idx] *= (1 - flight_rate)
            fled_K_AI += flight_amount

        # 11. Tracking
        wealth_total = wealth_T + wealth_AI
        H['year'].append(start_year + t)
        H['Y'].append(Y)
        H['gdp_idx'].append(Y / Y_t0)
        H['gdp_pc_idx'].append((Y / Y_t0) / L_scale)
        H['labor_share'].append(agg['labor_share_realized'])
        H['profit_share'].append(agg['profit_share'])
        H['monopsony_rents_share'].append(agg['monopsony_rents_share'])
        H['top1_wealth_share'].append(top1_share(wealth_total, top1_n))
        H['top10_wealth_share'].append(np.sort(wealth_total)[::-1][:1000].sum() / max(wealth_total.sum(), 1e-9))
        H['gini_wealth'].append(gini(wealth_total))
        H['gini_income'].append(gini(income_post_tax))
        H['p90_p10_income'].append(p90_p10(income_post_tax))
        H['wage_safe'].append(float(agg['wage_safe']))
        H['wage_sub'].append(float(agg['wage_sub']))
        H['wage_comp'].append(float(agg['wage_comp']))
        H['mean_markup'].append(float(firms.aggregate_markup()))
        H['I_threshold'].append(prod.I)
        H['N_new_tasks'].append(prod.N)
        H['sov_share_AI'].append(sov_K_AI / max(wealth_AI.sum() + sov_K_AI + fled_K_AI, 1e-9))
        H['fled_share_AI'].append(fled_K_AI / max(wealth_AI.sum() + sov_K_AI + fled_K_AI, 1e-9))
        cons_dec = [float(np.mean(consumption[d * n10:(d + 1) * n10])) for d in range(10)]
        inc_dec = [float(np.mean(income_post_tax[d * n10:(d + 1) * n10])) for d in range(10)]
        H['consumption_by_decile'].append(cons_dec)
        H['income_by_decile'].append(inc_dec)
        H['cap_flight_rate'].append(flight_rate)
        H['K_per_Y'].append(K_productive / max(Y, 1e-9))
        H['r_capital'].append(agg['capital_return_with_rents'])

    return H


def backtest_2015_2025():
    """Backtest the model against US 2015-2025 observed macro data."""
    print("=== Backtest: simulating 2015-2025 ===")
    h = run_dynamic(SCENARIOS['historical'], n_years=11)

    # Observed targets
    targets = {
        'labor_share_2025': 0.56,        # BLS
        'top1_wealth_share_2025': 0.30,  # SCF
        'gdp_growth_cumulative': 0.22,   # BEA, real
        'mean_markup_2025': 1.22,        # DLEU
    }

    print(f"\n{'Indicator':<35} {'Model':>10} {'Observed':>10} {'Δ':>10}")
    print(f"{'-'*65}")
    items = [
        ('Labor share 2025', h['labor_share'][-1], targets['labor_share_2025']),
        ('Top 1% wealth share 2025', h['top1_wealth_share'][-1], targets['top1_wealth_share_2025']),
        ('Cumulative GDP growth', h['gdp_idx'][-1] - 1, targets['gdp_growth_cumulative']),
        ('Mean markup 2025', h['mean_markup'][-1], targets['mean_markup_2025']),
    ]
    for label, model_v, observed in items:
        err = (model_v - observed)
        print(f"{label:<35} {model_v:>10.4f} {observed:>10.4f} {err:>+10.4f}")

    print(f"\nFull labor share trajectory:")
    for y, ls in zip(h['year'], h['labor_share']):
        print(f"  {y}: {ls*100:.2f}%")
    print(f"\nFull top 1% wealth share trajectory:")
    for y, t1 in zip(h['year'], h['top1_wealth_share']):
        print(f"  {y}: {t1*100:.2f}%")
    return h


if __name__ == "__main__":
    backtest_2015_2025()
