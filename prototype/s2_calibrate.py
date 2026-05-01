"""Calibrate Stage 2 components to match US 2020 baseline:
labor share = 0.56, capital factor share = 0.26, profit share = 0.18."""

import numpy as np
from s1_production import TaskBasedProduction
from s2_firms_labor import FirmDistribution, MonopsonyLabor, aggregate_economy


def grid_search():
    """Find I, sigma, monopsony eps that hit US 2020 baseline."""
    target_labor_share = 0.56
    target_profit_share = 0.18

    # Fixed: markup distribution calibrated to DLEU 2020
    firms = FirmDistribution(n_firms=1000, markup_mean=1.22, markup_dispersion=0.30)
    firms.initialize(seed=42)
    actual_profit_share = firms.profit_share()
    print(f"Profit share from markup distribution: {actual_profit_share*100:.1f}% (target 18%)")

    best = None
    best_err = 1e9

    for I in np.linspace(0.18, 0.42, 25):
        for sigma in np.linspace(0.7, 1.5, 9):
            for eps in np.linspace(4.0, 20.0, 17):
                prod = TaskBasedProduction(I=float(I), N=0.0, A_K=1.0, A_L=1.0, sigma=float(sigma))
                m_safe = MonopsonyLabor(eps=float(eps))
                m_sub = MonopsonyLabor(eps=float(eps))
                m_comp = MonopsonyLabor(eps=float(eps) * 1.5)  # higher-skill less monopsonized
                res = aggregate_economy(
                    K=1.0, L_safe=0.20, L_sub=0.50, L_comp=0.30,
                    production=prod, firms=firms,
                    monopsony_safe=m_safe, monopsony_sub=m_sub, monopsony_comp=m_comp,
                )
                err = (res['labor_share_realized'] - target_labor_share)**2 + \
                      (res['profit_share'] - target_profit_share)**2
                if err < best_err:
                    best_err = err
                    best = {'I': float(I), 'sigma': float(sigma), 'eps': float(eps),
                            'labor_share': res['labor_share_realized'],
                            'profit_share': res['profit_share'],
                            'capital_share_with_rents': res['capital_return_with_rents']}

    print(f"\nBest fit:")
    for k, v in best.items():
        print(f"  {k}: {v:.4f}")
    print(f"\nLabor share target=0.56, got {best['labor_share']:.4f}")
    print(f"Profit share target=0.18, got {best['profit_share']:.4f}")
    return best


if __name__ == "__main__":
    grid_search()
