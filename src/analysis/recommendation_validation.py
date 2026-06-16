"""Validation of Part VI recommendations.

Tests whether the explicitly-specified Recommended Architecture
(Package R, src/packages/recommended.py) actually holds up under
the data we have. Specifically:

1. **Direct welfare comparison.** Where does Package R rank against
   the alternatives across Atkinson ε values?

2. **Cross-scenario robustness.** Does Package R win under
   substitute / complement / new-tasks regimes?

3. **Sensitivity to halved/doubled effect sizes.** If the v2.0
   calibration is off by 50%, does Package R still hold up?

4. **Adversarial parameter regions.** Under worst-case parameter
   combinations (high capital flight + low reskilling + low
   complementarity), does Package R survive?

5. **Comparison to politically-realistic intensity specifications.**
   Package R uses midpoint Faster Growth intensities. What if reality
   requires near-maximum intensities (i.e., Package H specs)?

The findings here directly inform whether the Part VI recommendation
should remain as-stated, be revised toward Package H, or be revised
toward Package E.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.analysis.welfare import package_rankings_by_epsilon
from src.analysis.scenario_comparison import cross_scenario_table
from src.core import BilateralSimulator, SimulatorConfig
from src.packages import ALL_PACKAGES, RECOMMENDED, PolicyPackage


@dataclass(frozen=True)
class ValidationResult:
    """Single validation test outcome."""

    test_name: str
    passes: bool
    finding: str
    details: dict


def validate_welfare_dominance(epsilons: tuple[float, ...] = (0.0, 0.5, 1.0, 2.0, 5.0)) -> ValidationResult:
    """Does Package R win the welfare ranking across all ε values?"""
    rankings = package_rankings_by_epsilon(epsilons)
    r_ranks = rankings["R"].values
    is_first = all(r == 1.0 for r in r_ranks)
    is_top_2 = all(r <= 2.0 for r in r_ranks)
    is_top_3 = all(r <= 3.0 for r in r_ranks)

    best_rank = float(r_ranks.min())
    worst_rank = float(r_ranks.max())

    if is_first:
        finding = "Package R is welfare-dominant (rank 1) across all ε."
    elif is_top_2:
        finding = (
            f"Package R is top-2 across all ε but is dominated by another package "
            f"(best rank {best_rank}, worst rank {worst_rank})."
        )
    elif is_top_3:
        finding = (
            f"Package R is top-3 across all ε; dominated by 2 alternatives "
            f"(best rank {best_rank}, worst rank {worst_rank})."
        )
    else:
        finding = (
            f"Package R ranks below top-3 at one or more ε values; "
            f"the recommendation is NOT welfare-dominant."
        )

    return ValidationResult(
        test_name="Welfare dominance across ε",
        passes=is_first,
        finding=finding,
        details={
            "best_rank": best_rank,
            "worst_rank": worst_rank,
            "rankings": rankings["R"].to_dict(),
        },
    )


def validate_cross_scenario_robustness() -> ValidationResult:
    """Does Package R win on median income under all 3 AI regime scenarios?"""
    df = cross_scenario_table()
    winners_per_scenario = {}
    r_results = {}
    for scenario, group in df.groupby("scenario"):
        best = group.sort_values("delta_median_income", ascending=False).iloc[0]
        winners_per_scenario[scenario] = best["package_code"]
        r_results[scenario] = group[group["package_code"] == "R"]["delta_median_income"].values[0]

    r_wins_all = all(winner == "R" for winner in winners_per_scenario.values())

    if r_wins_all:
        finding = "Package R wins on median income across all 3 AI regime scenarios."
    else:
        winners_str = ", ".join(f"{s}={w}" for s, w in winners_per_scenario.items())
        finding = (
            f"Package R does NOT win all 3 scenarios. Winners: {winners_str}. "
            f"Package R results: {r_results}"
        )

    return ValidationResult(
        test_name="Cross-scenario robustness",
        passes=r_wins_all,
        finding=finding,
        details={
            "winners": winners_per_scenario,
            "r_median_deltas": r_results,
        },
    )


def validate_sensitivity_to_halved_effects() -> ValidationResult:
    """If key effect sizes are halved, does Package R still beat status quo
    on median income?"""
    sim = BilateralSimulator()
    baseline = sim.run().to_dataframe()
    r_normal = sim.run(package=RECOMMENDED, coalition_share=0.7, cn_cooperation=0.5).to_dataframe()
    delta_normal = (
        r_normal.loc[2036, "us_median_income"] / baseline.loc[2036, "us_median_income"] - 1
    ) * 100

    # Halve key effect sizes
    config_halved = SimulatorConfig(
        reskilling_earnings_effect=0.04,  # was 0.08
        open_weights_markup_dampening=0.10,  # was 0.20
        ai_productivity_growth=0.009,  # was 0.018
    )
    sim_halved = BilateralSimulator(config=config_halved)
    baseline_halved = sim_halved.run().to_dataframe()
    r_halved = sim_halved.run(
        package=RECOMMENDED, coalition_share=0.7, cn_cooperation=0.5
    ).to_dataframe()
    delta_halved = (
        r_halved.loc[2036, "us_median_income"] / baseline_halved.loc[2036, "us_median_income"] - 1
    ) * 100

    # Test: R should still beat status quo on median income at halved effects
    still_positive = delta_halved > 0
    # Tolerable degradation: less than 50% loss
    degradation_pct = (delta_normal - delta_halved) / delta_normal
    tolerable = degradation_pct < 0.50

    if still_positive and tolerable:
        finding = (
            f"Package R remains welfare-positive under halved effects "
            f"(median income gain {delta_normal:.1f}% → {delta_halved:.1f}%, "
            f"{degradation_pct*100:.1f}% degradation)."
        )
        passes = True
    elif still_positive:
        finding = (
            f"Package R remains positive but with major degradation: "
            f"{delta_normal:.1f}% → {delta_halved:.1f}% "
            f"({degradation_pct*100:.1f}% loss)."
        )
        passes = False
    else:
        finding = (
            f"Package R becomes net negative under halved effects: "
            f"{delta_normal:.1f}% → {delta_halved:.1f}%. "
            f"Recommendation is fragile to effect-size uncertainty."
        )
        passes = False

    return ValidationResult(
        test_name="Sensitivity to halved effect sizes",
        passes=passes,
        finding=finding,
        details={
            "delta_normal": float(delta_normal),
            "delta_halved": float(delta_halved),
            "degradation_pct": float(degradation_pct),
        },
    )


def validate_adversarial_parameters() -> ValidationResult:
    """Under worst-case parameter combinations, does Package R survive?

    Adversarial config: high capital flight + minimal cooperation + low
    productivity + halved reskilling. Simulates worst political and
    economic conditions.
    """
    config = SimulatorConfig(
        capital_flight_elasticity=0.012,  # high end of v2.0 range
        ai_productivity_growth=0.005,  # low end (Acemoglu Slow Growth)
        reskilling_earnings_effect=0.05,  # low end of CKW range
        cn_cooperation_propensity=0.05,  # adversarial CN
        base_compute_coalition_share=0.35,  # bare-minimum coalition
        open_weights_markup_dampening=0.05,  # low end (post-DeepSeek minimal)
    )
    sim = BilateralSimulator(config=config)
    baseline = sim.run().to_dataframe()
    r_run = sim.run(
        package=RECOMMENDED,
        coalition_share=config.base_compute_coalition_share,
        cn_cooperation=config.cn_cooperation_propensity,
    ).to_dataframe()
    delta_median = (
        r_run.loc[2036, "us_median_income"] / baseline.loc[2036, "us_median_income"] - 1
    ) * 100
    delta_top_1pct = (r_run.loc[2036, "us_top_1pct"] - baseline.loc[2036, "us_top_1pct"]) * 100
    delta_labor_share = (
        r_run.loc[2036, "us_labor_share"] - baseline.loc[2036, "us_labor_share"]
    ) * 100

    survives = delta_median > 0 and delta_top_1pct < 0

    if survives:
        finding = (
            f"Package R survives adversarial regime (median +{delta_median:.1f}%, "
            f"top-1% {delta_top_1pct:+.2f}pp, labor share {delta_labor_share:+.2f}pp). "
            f"Recommendation is robust under worst-case conditions."
        )
    else:
        finding = (
            f"Package R FAILS in adversarial regime (median {delta_median:+.1f}%, "
            f"top-1% {delta_top_1pct:+.2f}pp, labor share {delta_labor_share:+.2f}pp). "
            f"Recommendation is fragile to worst-case parameter combinations."
        )

    return ValidationResult(
        test_name="Adversarial parameter regime",
        passes=survives,
        finding=finding,
        details={
            "delta_median_income": float(delta_median),
            "delta_top_1pct": float(delta_top_1pct),
            "delta_labor_share": float(delta_labor_share),
        },
    )


def validate_vs_status_quo_dominance() -> ValidationResult:
    """Does Package R dominate status quo on every key metric?"""
    sim = BilateralSimulator()
    baseline = sim.run().to_dataframe()
    r_run = sim.run(package=RECOMMENDED, coalition_share=0.7, cn_cooperation=0.5).to_dataframe()

    metrics = {
        "median income": (
            r_run.loc[2036, "us_median_income"] / baseline.loc[2036, "us_median_income"] - 1
        ) * 100,
        "top-1% wealth share": (
            -(r_run.loc[2036, "us_top_1pct"] - baseline.loc[2036, "us_top_1pct"]) * 100
        ),  # lower is better
        "labor share": (
            r_run.loc[2036, "us_labor_share"] - baseline.loc[2036, "us_labor_share"]
        ) * 100,
        "markup": -(r_run.loc[2036, "us_markup"] - baseline.loc[2036, "us_markup"]),
        "geopolitical stability": (
            r_run.loc[2036, "geopolitical_stability"] - baseline.loc[2036, "geopolitical_stability"]
        ),
        # GDP is acceptable to be neutral or slightly down (within 2pp per framework target)
    }
    gdp_delta = (
        r_run.loc[2036, "us_real_gdp"] / baseline.loc[2036, "us_real_gdp"] - 1
    ) * 100

    all_positive = all(v >= 0 for v in metrics.values())
    gdp_within_target = gdp_delta > -2.0

    if all_positive and gdp_within_target:
        finding = (
            "Package R dominates status quo on every key stability metric "
            f"(median income +{metrics['median income']:.1f}%, top-1% "
            f"−{metrics['top-1% wealth share']:.2f}pp, etc.) with GDP "
            f"{gdp_delta:+.2f}% (within 2pp target)."
        )
        passes = True
    else:
        negatives = [k for k, v in metrics.items() if v < 0]
        finding = (
            f"Package R does NOT dominate status quo on: {negatives}. "
            f"GDP delta {gdp_delta:+.2f}%."
        )
        passes = False

    return ValidationResult(
        test_name="Stability-dimension dominance vs. status quo",
        passes=passes,
        finding=finding,
        details={**metrics, "gdp_delta": float(gdp_delta)},
    )


def run_full_validation() -> list[ValidationResult]:
    """Run all five validation tests."""
    return [
        validate_welfare_dominance(),
        validate_cross_scenario_robustness(),
        validate_sensitivity_to_halved_effects(),
        validate_adversarial_parameters(),
        validate_vs_status_quo_dominance(),
    ]


def report_validation(results: list[ValidationResult]) -> str:
    """Generate honest validation report."""
    n_pass = sum(1 for r in results if r.passes)
    n_total = len(results)

    lines = [
        "Recommendation Validation Report",
        "=" * 60,
        "",
        f"Tests passed: {n_pass} / {n_total}",
        "",
    ]
    for r in results:
        flag = "✓ PASS" if r.passes else "✗ FAIL"
        lines.append(f"{flag}  {r.test_name}")
        lines.append(f"        {r.finding}")
        lines.append("")

    lines.extend(
        [
            "",
            "Honest interpretation:",
            "- 5/5 passing: Package R is the welfare-dominant recommendation.",
            "- 4/5 or 3/5 passing: Package R is defensible but with known weaknesses.",
            "- ≤2/5 passing: The Part VI recommendation needs revision.",
            "",
            "Failed tests should be addressed by either: (a) revising the "
            "recommendation toward the alternative that passes, (b) tightening "
            "intensity calibrations in src/packages/recommended.py, or (c) "
            "honestly reporting the limitation in the recommendation section.",
        ]
    )
    return "\n".join(lines)
