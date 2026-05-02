"""Run the status-quo baseline and print key indicators.

Usage:
    python scripts/run_baseline.py
    python scripts/run_baseline.py --csv results/baseline.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Make repo root importable when running this script directly
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.core import BilateralSimulator


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, help="Optional output CSV path")
    args = parser.parse_args()

    sim = BilateralSimulator()
    result = sim.run()
    df = result.to_dataframe()

    print("=" * 70)
    print("STATUS QUO BASELINE — Q1 2026 trajectory continuation")
    print("=" * 70)
    print()
    print(f"  Years simulated: {df.index.min()} → {df.index.max()}")
    print()
    print("  Backtest period (2015 → 2025):")
    print(f"    US labor share:   {df.loc[2015, 'us_labor_share']:.3f} → {df.loc[2025, 'us_labor_share']:.3f}")
    print(f"    US top 1% wealth: {df.loc[2015, 'us_top_1pct']:.3f} → {df.loc[2025, 'us_top_1pct']:.3f}")
    print(f"    US mean markup:   {df.loc[2015, 'us_markup']:.3f} → {df.loc[2025, 'us_markup']:.3f}")
    us_g = df.loc[2025, "us_real_gdp"] / df.loc[2015, "us_real_gdp"] - 1
    cn_g = df.loc[2025, "cn_real_gdp"] / df.loc[2015, "cn_real_gdp"] - 1
    print(f"    US cumul real GDP growth: {us_g:.1%}")
    print(f"    CN cumul real GDP growth: {cn_g:.1%}")
    print()
    print("  Forward projection (2025 → 2036, status quo):")
    print(f"    US labor share:   {df.loc[2025, 'us_labor_share']:.3f} → {df.loc[2036, 'us_labor_share']:.3f}")
    print(f"    US top 1% wealth: {df.loc[2025, 'us_top_1pct']:.3f} → {df.loc[2036, 'us_top_1pct']:.3f}")
    print(f"    US mean markup:   {df.loc[2025, 'us_markup']:.3f} → {df.loc[2036, 'us_markup']:.3f}")
    print(f"    US sub-worker emp idx: {df.loc[2025, 'us_sub_emp_idx']:.1f} → {df.loc[2036, 'us_sub_emp_idx']:.1f}")
    us_proj = df.loc[2036, "us_real_gdp"] / df.loc[2025, "us_real_gdp"] - 1
    cn_proj = df.loc[2036, "cn_real_gdp"] / df.loc[2025, "cn_real_gdp"] - 1
    print(f"    US cumul real GDP growth: {us_proj:.1%}")
    print(f"    CN cumul real GDP growth: {cn_proj:.1%}")
    print()
    print(f"    Geopolitical stability: {df.loc[2025, 'geopolitical_stability']:.1f} → {df.loc[2036, 'geopolitical_stability']:.1f}")
    print()

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.csv)
        print(f"  Wrote: {args.csv}")


if __name__ == "__main__":
    main()
