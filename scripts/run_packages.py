"""Run all 7 policy packages and report 2036 deltas vs status quo.

This is the deterministic Tier 1 + Tier 2 comparison from PREREGISTRATION.md
§Simulation Matrix. For RDM uncertainty bounds, use scripts/run_rdm.py.

Usage:
    python scripts/run_packages.py
    python scripts/run_packages.py --coalition 0.6 --cn-cooperation 0.4
    python scripts/run_packages.py --csv results/packages_2036.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.core import BilateralSimulator
from src.packages import ALL_PACKAGES


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coalition", type=float, default=0.7,
                        help="Compute coalition share (default 0.7)")
    parser.add_argument("--cn-cooperation", type=float, default=0.30,
                        help="China cooperation propensity (default 0.30)")
    parser.add_argument("--year", type=int, default=2036,
                        help="Comparison year (default 2036)")
    parser.add_argument("--csv", type=Path, help="Optional output CSV path")
    args = parser.parse_args()

    sim = BilateralSimulator()
    baseline = sim.run().to_dataframe()

    rows = []
    for pkg in ALL_PACKAGES:
        result = sim.run(
            package=pkg,
            coalition_share=args.coalition,
            cn_cooperation=args.cn_cooperation,
        )
        df = result.to_dataframe()
        y = args.year
        rows.append(
            {
                "code": pkg.code,
                "name": pkg.name,
                "us_labor_share_d_pp": (df.loc[y, "us_labor_share"] - baseline.loc[y, "us_labor_share"]) * 100,
                "us_top_1pct_d_pp": (df.loc[y, "us_top_1pct"] - baseline.loc[y, "us_top_1pct"]) * 100,
                "us_markup_d": df.loc[y, "us_markup"] - baseline.loc[y, "us_markup"],
                "us_gdp_d_pct": (df.loc[y, "us_real_gdp"] / baseline.loc[y, "us_real_gdp"] - 1) * 100,
                "us_median_income_d_pct": (df.loc[y, "us_median_income"] / baseline.loc[y, "us_median_income"] - 1) * 100,
                "us_sub_emp_d_pct": (df.loc[y, "us_sub_emp_idx"] / baseline.loc[y, "us_sub_emp_idx"] - 1) * 100,
                "cn_top_1pct_d_pp": (df.loc[y, "cn_top_1pct"] - baseline.loc[y, "cn_top_1pct"]) * 100,
                "geo_stability_d": df.loc[y, "geopolitical_stability"] - baseline.loc[y, "geopolitical_stability"],
                "n_audit_entries": len(result.audit_trail),
            }
        )

    out = pd.DataFrame(rows)

    print("=" * 100)
    print(f"PACKAGE COMPARISON @ {args.year}: Δ vs status quo")
    print(f"  coalition_share = {args.coalition}, cn_cooperation = {args.cn_cooperation}")
    print("=" * 100)
    print()
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
    pd.set_option("display.float_format", "{:+.3f}".format)
    print(out.set_index("code")[
        [
            "name",
            "us_labor_share_d_pp",
            "us_top_1pct_d_pp",
            "us_markup_d",
            "us_gdp_d_pct",
            "us_median_income_d_pct",
            "us_sub_emp_d_pct",
            "cn_top_1pct_d_pp",
            "geo_stability_d",
        ]
    ].to_string())
    print()
    print("Legend: d_pp = percentage-point delta;  d_pct = percent delta;  d = absolute delta")

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        out.to_csv(args.csv, index=False)
        print(f"\nWrote: {args.csv}")


if __name__ == "__main__":
    main()
