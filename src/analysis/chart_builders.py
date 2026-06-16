"""Chart-building pipeline for paper figures.

Generates publication-grade figures from simulator + RDM output:
    Fig 1. Status-quo baseline trajectory (2015-2036)
    Fig 2. Package comparison heatmap @ 2036 (Δ vs status quo)
    Fig 3. Cross-class welfare distribution per package (10 deciles × 2 countries)
    Fig 4. Coalition formation sweep (welfare vs coalition share)
    Fig 5. Policy regret surface — RDM (fraction-best per package per metric)
    Fig 6. Time-consistency stress (expected welfare under stochastic reversal)

Nebulai brand palette per paper/draft/README.md:
    Purple #7C3AED — primary accent, package highlights
    Indigo #1E1B4B — titles, axes
    Lavender #F5F3FF — backgrounds
    Plus a categorical palette for the 7 packages.

Usage
-----
    python -m src.analysis.chart_builders                    # all figures
    python -m src.analysis.chart_builders --fig 3 --fig 5   # selected
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.analysis.rdm import (
    OUTCOME_METRICS,
    policy_regret,
    run_rdm_for_all_packages,
)
from src.core import BilateralSimulator
from src.packages import ALL_PACKAGES, get_package
from src.stability import CoalitionTest, CrossClassTest, TimeConsistencyTest


# =============================================================================
# Styling
# =============================================================================

NEBULAI_PURPLE = "#7C3AED"
NEBULAI_INDIGO = "#1E1B4B"
NEBULAI_LAVENDER = "#F5F3FF"

PACKAGE_COLORS = {
    "A": "#9CA3AF",  # gray — status quo
    "B": NEBULAI_PURPLE,  # purple — Nebulai (highlight)
    "C": "#10B981",  # emerald — CERN-AI
    "D": "#F59E0B",  # amber — compute-centric
    "E": "#3B82F6",  # blue — direct redistribution
    "F": "#EC4899",  # pink — build-different
    "G": NEBULAI_INDIGO,  # indigo — game-theoretic-derived
}

HIGHER_IS_BETTER = {
    "us_real_gdp_growth": True,
    "us_median_income_2036": True,
    "us_substitute_emp_2036": True,
    "us_labor_share_2036": True,
    "cn_real_gdp_growth": True,
    "cn_labor_share_2036": True,
    "geopolitical_stability_2036": True,
    "us_top_1pct_wealth_2036": False,
    "us_markup_2036": False,
    "cn_top_1pct_wealth_2036": False,
    "arms_race_2036": False,
}


def _setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.labelsize": 10,
            "axes.edgecolor": NEBULAI_INDIGO,
            "axes.labelcolor": NEBULAI_INDIGO,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.color": NEBULAI_INDIGO,
            "ytick.color": NEBULAI_INDIGO,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.bbox": "tight",
            "savefig.dpi": 150,
        }
    )


def _save_figure(fig, path: Path, *, also_svg: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    if also_svg:
        fig.savefig(path.with_suffix(".svg"))
    print(f"  Wrote {path}")


# =============================================================================
# Figure 1 — Status-quo baseline trajectory
# =============================================================================


def fig_baseline_trajectory(out_dir: Path) -> Path:
    _setup_style()
    sim = BilateralSimulator()
    df = sim.run().to_dataframe()

    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    fig.suptitle(
        "Q1 2026 Status-Quo Baseline (BASELINE_2026.md §3)",
        color=NEBULAI_INDIGO,
        fontsize=14,
        fontweight="bold",
    )

    # US labor share
    ax = axes[0, 0]
    ax.plot(df.index, df["us_labor_share"], color=NEBULAI_PURPLE, lw=2, label="US")
    ax.plot(df.index, df["cn_labor_share"], color=NEBULAI_INDIGO, lw=2, label="CN")
    ax.axvspan(2015, 2025, alpha=0.08, color="gray", label="Backtest period")
    ax.set_title("Labor share of GDP")
    ax.set_ylabel("Share")
    ax.legend(frameon=False)

    # US top 1% wealth
    ax = axes[0, 1]
    ax.plot(df.index, df["us_top_1pct"], color=NEBULAI_PURPLE, lw=2, label="US")
    ax.plot(df.index, df["cn_top_1pct"], color=NEBULAI_INDIGO, lw=2, label="CN")
    ax.axvspan(2015, 2025, alpha=0.08, color="gray")
    ax.set_title("Top 1% wealth share")
    ax.set_ylabel("Share")
    ax.legend(frameon=False)

    # Mean markup
    ax = axes[1, 0]
    ax.plot(df.index, df["us_markup"], color=NEBULAI_PURPLE, lw=2, label="US")
    ax.plot(df.index, df["cn_markup"], color=NEBULAI_INDIGO, lw=2, label="CN")
    ax.axvspan(2015, 2025, alpha=0.08, color="gray")
    ax.set_title("Sales-weighted mean markup")
    ax.set_ylabel("Markup")
    ax.legend(frameon=False)

    # Real GDP (indexed to 2015 = 100)
    ax = axes[1, 1]
    us_idx = df["us_real_gdp"] / df["us_real_gdp"].iloc[0] * 100
    cn_idx = df["cn_real_gdp"] / df["cn_real_gdp"].iloc[0] * 100
    ax.plot(df.index, us_idx, color=NEBULAI_PURPLE, lw=2, label="US")
    ax.plot(df.index, cn_idx, color=NEBULAI_INDIGO, lw=2, label="CN")
    ax.axvspan(2015, 2025, alpha=0.08, color="gray")
    ax.set_title("Real GDP (2015 = 100)")
    ax.set_ylabel("Index")
    ax.legend(frameon=False)

    fig.tight_layout()
    path = out_dir / "fig01_baseline_trajectory.png"
    _save_figure(fig, path)
    plt.close(fig)
    return path


# =============================================================================
# Figure 2 — Package comparison heatmap
# =============================================================================


def fig_package_comparison_heatmap(out_dir: Path) -> Path:
    _setup_style()
    sim = BilateralSimulator()
    baseline = sim.run().to_dataframe()

    metrics = [
        ("us_labor_share", "US labor share", "pp", True),
        ("us_top_1pct", "US top 1% wealth", "pp", False),
        ("us_markup", "US markup", "abs", False),
        ("us_real_gdp", "US real GDP", "%", True),
        ("us_median_income", "US median income", "%", True),
        ("geopolitical_stability", "Geopolitical stability", "pts", True),
    ]
    matrix = np.zeros((len(ALL_PACKAGES), len(metrics)))
    row_labels = []

    for i, pkg in enumerate(ALL_PACKAGES):
        row_labels.append(f"{pkg.code}. {pkg.name[:35]}")
        df = sim.run(package=pkg, coalition_share=0.7, cn_cooperation=0.5).to_dataframe()
        for j, (metric, _, unit, _) in enumerate(metrics):
            if unit == "pp":
                matrix[i, j] = (df.loc[2036, metric] - baseline.loc[2036, metric]) * 100
            elif unit == "abs":
                matrix[i, j] = df.loc[2036, metric] - baseline.loc[2036, metric]
            elif unit == "%":
                matrix[i, j] = (df.loc[2036, metric] / baseline.loc[2036, metric] - 1) * 100
            else:  # pts
                matrix[i, j] = df.loc[2036, metric] - baseline.loc[2036, metric]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    # Symmetric colormap so positive=blue, negative=red
    vmax = float(np.nanmax(np.abs(matrix)))
    im = ax.imshow(matrix, cmap="RdBu", vmin=-vmax, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(metrics)))
    ax.set_xticklabels([m[1] for m in metrics], rotation=30, ha="right")
    ax.set_yticks(range(len(ALL_PACKAGES)))
    ax.set_yticklabels(row_labels)
    ax.set_title(
        "Package comparison @ 2036: Δ vs status quo\n(coalition_share=0.7, cn_cooperation=0.5)",
        color=NEBULAI_INDIGO,
        fontsize=12,
        fontweight="bold",
    )

    # Annotate each cell with the value
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            unit = metrics[j][2]
            val = matrix[i, j]
            txt = f"{val:+.2f}{unit}" if unit in ("%", "pp", "pts") else f"{val:+.3f}"
            ax.text(j, i, txt, ha="center", va="center", fontsize=8,
                    color="black" if abs(val) < vmax * 0.5 else "white")

    fig.colorbar(im, ax=ax, label="Δ (signed)")
    path = out_dir / "fig02_package_comparison_heatmap.png"
    _save_figure(fig, path)
    plt.close(fig)
    return path


# =============================================================================
# Figure 3 — Cross-class welfare matrix
# =============================================================================


def fig_cross_class_welfare(out_dir: Path) -> Path:
    _setup_style()
    fig, axes = plt.subplots(1, 6, figsize=(15, 5), sharey=True)
    fig.suptitle(
        "Cross-class welfare distribution per package (Hypothesis 4)\n"
        "Δ(decile median real income) vs status quo; red = decile is worse off",
        color=NEBULAI_INDIGO,
        fontsize=12,
        fontweight="bold",
    )

    packages_to_plot = [p for p in ALL_PACKAGES if p.code != "A"]  # skip status quo
    vmax_all = 0.0
    matrices = []
    for pkg in packages_to_plot:
        m = CrossClassTest(pkg).run().welfare_delta_matrix * 100
        matrices.append(m)
        vmax_all = max(vmax_all, float(np.nanmax(np.abs(m))))

    for ax, pkg, m in zip(axes, packages_to_plot, matrices):
        im = ax.imshow(m, cmap="RdBu", vmin=-vmax_all, vmax=vmax_all, aspect="auto")
        ax.set_title(f"{pkg.code}. {pkg.name[:18]}", fontsize=10, color=NEBULAI_INDIGO)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["US", "CN"], fontsize=9)
        ax.set_yticks(range(10))
        ax.set_yticklabels([f"D{d+1}" for d in range(10)], fontsize=8)
        for i in range(10):
            for j in range(2):
                v = m[i, j]
                ax.text(j, i, f"{v:+.1f}", ha="center", va="center", fontsize=7,
                        color="black" if abs(v) < vmax_all * 0.5 else "white")

    fig.colorbar(im, ax=axes, label="Δ income vs baseline (%)")
    path = out_dir / "fig03_cross_class_welfare.png"
    _save_figure(fig, path)
    plt.close(fig)
    return path


# =============================================================================
# Figure 4 — Coalition formation sweep
# =============================================================================


def fig_coalition_sweep(out_dir: Path) -> Path:
    _setup_style()
    fig, ax = plt.subplots(figsize=(10, 6))

    for pkg in ALL_PACKAGES:
        if pkg.code == "A":
            continue
        result = CoalitionTest(pkg).run(n_steps=15)
        ax.plot(
            result.coalition_thresholds,
            result.welfare_deltas,
            color=PACKAGE_COLORS[pkg.code],
            lw=2,
            marker="o",
            markersize=4,
            label=f"{pkg.code}. {pkg.name[:30]}",
        )
        if not np.isnan(result.breakeven_threshold):
            ax.axvline(
                result.breakeven_threshold,
                color=PACKAGE_COLORS[pkg.code],
                ls="--",
                alpha=0.25,
            )

    ax.axhline(0, color="gray", lw=1, alpha=0.5)
    ax.set_xlabel("Coalition share of frontier compute")
    ax.set_ylabel("Δ median real income vs status quo (level)")
    ax.set_title(
        "Coalition formation: welfare vs coalition share\n"
        "Dashed lines = breakeven threshold per package",
        color=NEBULAI_INDIGO,
        fontsize=12,
        fontweight="bold",
    )
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    fig.tight_layout()
    path = out_dir / "fig04_coalition_sweep.png"
    _save_figure(fig, path)
    plt.close(fig)
    return path


# =============================================================================
# Figure 5 — Policy regret surface (RDM)
# =============================================================================


def fig_policy_regret_surface(out_dir: Path, n_scenarios: int = 500) -> Path:
    _setup_style()
    print(f"  Running RDM sweep: {n_scenarios} scenarios × 7 packages = "
          f"{n_scenarios * 7} sims...")
    results = run_rdm_for_all_packages(n_scenarios=n_scenarios)

    metrics_to_plot = [
        "us_top_1pct_wealth_2036",
        "us_median_income_2036",
        "us_real_gdp_growth",
        "us_labor_share_2036",
        "us_markup_2036",
        "geopolitical_stability_2036",
    ]

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    fig.suptitle(
        f"Policy regret surface over RDM uncertainty ({n_scenarios * 7} sims)\n"
        "Fraction of plausible futures where each package wins (PREREG Hypothesis 9)",
        color=NEBULAI_INDIGO,
        fontsize=12,
        fontweight="bold",
    )

    for ax, metric in zip(axes.flat, metrics_to_plot):
        higher_better = HIGHER_IS_BETTER.get(metric, True)
        regret = policy_regret(results, metric, higher_is_better=higher_better).sort_values(
            "fraction_best", ascending=False
        )
        codes = list(regret.index)
        fractions = regret["fraction_best"].values * 100
        colors = [PACKAGE_COLORS[c] for c in codes]
        ax.barh(codes, fractions, color=colors, edgecolor=NEBULAI_INDIGO, linewidth=0.5)
        direction = "↑ higher better" if higher_better else "↓ lower better"
        ax.set_title(f"{metric}\n({direction})", fontsize=9, color=NEBULAI_INDIGO)
        ax.set_xlabel("% of scenarios won")
        ax.set_xlim(0, 100)
        ax.invert_yaxis()
        for i, (code, frac) in enumerate(zip(codes, fractions)):
            ax.text(frac + 1, i, f"{frac:.0f}%", va="center", fontsize=8)

    fig.tight_layout()
    path = out_dir / "fig05_policy_regret_surface.png"
    _save_figure(fig, path)
    plt.close(fig)
    return path


# =============================================================================
# Figure 6 — Time-consistency stress
# =============================================================================


def fig_time_consistency(out_dir: Path, n_draws: int = 100) -> Path:
    _setup_style()
    fig, ax = plt.subplots(figsize=(10, 6))

    summaries = []
    for pkg in ALL_PACKAGES:
        if pkg.code == "A":
            continue
        result = TimeConsistencyTest(pkg, n_draws=n_draws).run()
        summaries.append(
            {
                "code": pkg.code,
                "name": pkg.name,
                "full": result.expected_welfare_full_persistence,
                "partial": result.expected_welfare_under_stochastic_reversal,
                "loss": result.welfare_loss_from_political_risk,
                "fraction_below_baseline": result.fraction_draws_below_baseline,
            }
        )

    df = pd.DataFrame(summaries).set_index("code")
    df = df.sort_values("loss")  # least loss first (most durable)

    codes = df.index.tolist()
    colors = [PACKAGE_COLORS[c] for c in codes]
    y = np.arange(len(codes))

    ax.barh(y - 0.18, df["full"], 0.35, color=colors, label="Full persistence", edgecolor=NEBULAI_INDIGO)
    ax.barh(y + 0.18, df["partial"], 0.35, color=colors, alpha=0.5, label=f"Under stochastic reversal (n={n_draws})", edgecolor=NEBULAI_INDIGO, hatch="//")

    ax.set_yticks(y)
    ax.set_yticklabels([f"{c}. {df.loc[c, 'name'][:30]}" for c in codes])
    ax.set_xlabel("Expected US median income index, 2036")
    ax.set_title(
        f"Time-consistency stress: welfare under stochastic policy reversal\n"
        "(reversal probability per lever weighted by Reversibility)",
        color=NEBULAI_INDIGO,
        fontsize=12,
        fontweight="bold",
    )
    ax.legend(loc="lower right", frameon=False)
    fig.tight_layout()
    path = out_dir / "fig06_time_consistency.png"
    _save_figure(fig, path)
    plt.close(fig)
    return path


# =============================================================================
# CLI
# =============================================================================

FIGURES = {
    1: ("Baseline trajectory", fig_baseline_trajectory),
    2: ("Package comparison heatmap", fig_package_comparison_heatmap),
    3: ("Cross-class welfare", fig_cross_class_welfare),
    4: ("Coalition formation sweep", fig_coalition_sweep),
    5: ("Policy regret surface (RDM)", fig_policy_regret_surface),
    6: ("Time-consistency stress", fig_time_consistency),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("paper/figures"),
        help="Output directory (default: paper/figures/)",
    )
    parser.add_argument(
        "--fig",
        type=int,
        action="append",
        choices=list(FIGURES.keys()),
        help="Generate only this figure(s); may be repeated",
    )
    parser.add_argument(
        "--rdm-scenarios",
        type=int,
        default=500,
        help="RDM scenarios for Figure 5 (default 500)",
    )
    parser.add_argument(
        "--time-draws",
        type=int,
        default=100,
        help="Monte Carlo draws for Figure 6 (default 100)",
    )
    args = parser.parse_args()

    targets = args.fig or list(FIGURES.keys())
    print(f"Generating figures: {sorted(targets)} → {args.out_dir}")
    for n in sorted(targets):
        name, fn = FIGURES[n]
        print(f"\nFig {n}: {name}")
        if n == 5:
            fn(args.out_dir, n_scenarios=args.rdm_scenarios)
        elif n == 6:
            fn(args.out_dir, n_draws=args.time_draws)
        else:
            fn(args.out_dir)


if __name__ == "__main__":
    # Add repo root to sys.path when invoked directly via -m
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    main()
