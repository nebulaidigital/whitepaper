"""Run RDM scenario discovery across all packages.

This runs the Latin Hypercube sample × all packages × computes the
policy regret surface per metric. Per PREREGISTRATION.md Hypothesis 9,
this is the central deliverable of the project.

Usage:
    python scripts/run_rdm.py                                     # 1000 scenarios
    python scripts/run_rdm.py --scenarios 200 --csv results/rdm.csv
    python scripts/run_rdm.py --scenarios 5000 --metric us_top_1pct_wealth_2036
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analysis.rdm import OUTCOME_METRICS, policy_regret, run_rdm_for_all_packages


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenarios", type=int, default=1000,
                        help="Number of LHS scenarios per package (default 1000)")
    parser.add_argument("--csv", type=Path,
                        help="Optional output CSV path for full results")
    parser.add_argument("--metric", type=str,
                        help="Show regret for one specific metric only")
    parser.add_argument("--seed", type=int, default=20260501,
                        help="LHS seed for reproducibility")
    args = parser.parse_args()

    print(f"Running RDM: {args.scenarios} scenarios × 7 packages = "
          f"{args.scenarios * 7} simulations...")
    t0 = time.time()
    results = run_rdm_for_all_packages(n_scenarios=args.scenarios, seed=args.seed)
    elapsed = time.time() - t0
    print(f"  Done in {elapsed:.1f}s ({len(results.experiments)} experiments)")
    print()

    metrics = [args.metric] if args.metric else list(OUTCOME_METRICS)
    higher_better = {
        "us_real_gdp_growth": True,
        "us_median_income_2036": True,
        "us_substitute_emp_2036": True,
        "us_labor_share_2036": True,
        "cn_real_gdp_growth": True,
        "cn_labor_share_2036": True,
        "geopolitical_stability_2036": True,
        # Lower is better
        "us_top_1pct_wealth_2036": False,
        "us_markup_2036": False,
        "cn_top_1pct_wealth_2036": False,
        "arms_race_2036": False,
    }

    print("=" * 80)
    print("POLICY REGRET BY METRIC")
    print("=" * 80)
    for metric in metrics:
        direction = "↑ higher is better" if higher_better.get(metric, True) else "↓ lower is better"
        print(f"\n  {metric}  ({direction})")
        regret = policy_regret(
            results,
            metric,
            higher_is_better=higher_better.get(metric, True),
        )
        regret = regret.sort_values("mean_regret")
        for code, row in regret.iterrows():
            print(f"    {code}:  mean_regret={row['mean_regret']:+.4f}  "
                  f"max_regret={row['max_regret']:+.4f}  "
                  f"fraction_best={row['fraction_best']*100:5.1f}%")

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        results.merge().to_csv(args.csv, index=False)
        print(f"\nWrote: {args.csv}")


if __name__ == "__main__":
    main()
