"""Out-of-sample backtest.

The v0.2 simulator's in-sample backtest reproduces 2015–2025 observed
values exactly because `_baseline_trajectory` copies observed values
directly in the backtest window. This is *not* validation — it's
tautology. A PhD-level critique correctly flags this.

This module addresses the critique by:
1. Fitting trajectory rates (decay / growth) from a training window
   (default 2015–2019) without using the test window data.
2. Projecting forward from the training endpoint to the test window
   (default 2020–2025) using only those fitted rates.
3. Comparing predicted to actual observed values in the test window.
4. Reporting mean absolute error and percent-within-tolerance per
   indicator.

This produces a genuine out-of-sample test of the underlying
trajectory mechanism. Results document what the model can and cannot
predict — converting "reproduces past by construction" into
"predicts held-out future within ±X."

Limitation: this validates only the reduced-form trajectory mechanics,
not the structural mechanisms in `src/production/task_based.py`. A
fuller validation would also need to test the production module's
predictions, which requires more granular task-level data than we have.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.analysis.baseline_data import (
    load_cn_baseline,
    load_us_baseline,
)


@dataclass(frozen=True)
class OOSResult:
    """Out-of-sample backtest result for one indicator."""

    indicator: str
    country: str
    train_window: tuple[int, int]
    test_window: tuple[int, int]
    fitted_rate: float
    predictions: np.ndarray  # predicted values for test years
    actuals: np.ndarray  # observed values for test years
    test_years: np.ndarray
    mae: float
    mae_pct: float  # mean absolute percentage error
    max_error: float
    within_tolerance: bool  # whether MAE is within the documented tolerance

    def to_dict(self) -> dict:
        return {
            "indicator": self.indicator,
            "country": self.country,
            "train_window": self.train_window,
            "test_window": self.test_window,
            "fitted_rate": float(self.fitted_rate),
            "mae": float(self.mae),
            "mae_pct": float(self.mae_pct),
            "max_error": float(self.max_error),
            "within_tolerance": bool(self.within_tolerance),
        }


def _fit_exponential_rate(series: pd.Series, start: int, end: int) -> float:
    """Fit a continuous exponential rate from series[start] to series[end].

    Returns the per-year growth rate g such that:
        series[end] = series[start] * (1 + g)^(end - start)
    """
    if start not in series.index or end not in series.index:
        raise KeyError(f"Years {start} or {end} not in series index")
    if series[start] <= 0:
        raise ValueError(f"Cannot fit growth rate from non-positive value {series[start]}")
    return float((series[end] / series[start]) ** (1.0 / (end - start)) - 1.0)


def _project_forward(start_value: float, rate: float, n_periods: int) -> np.ndarray:
    """Project forward N periods at compound rate."""
    return np.array(
        [start_value * (1.0 + rate) ** t for t in range(1, n_periods + 1)]
    )


# Tolerance per PREREGISTRATION.md §8 — these are the maximum allowable
# absolute errors for backtest validation. Out-of-sample errors at or
# below tolerance suggest model captures dynamics genuinely; errors
# above suggest the model's projection mechanism is mis-specified.
TOLERANCES: dict[str, float] = {
    "us_labor_share": 0.02,  # ±2pp
    "us_top_1pct_wealth_share": 0.02,  # ±2pp
    "us_mean_markup_sw": 0.05,  # ±0.05
    "us_real_gdp_b": 0.05,  # ±5% of value
    "us_substitute_employment_idx": 3.0,  # ±3 index points
    "cn_labor_share": 0.03,  # ±3pp
    "cn_mean_markup_sw": 0.05,  # ±0.05
    "cn_real_gdp_b": 0.10,  # ±10% of value
    "cn_top_1pct_wealth_share": 0.03,  # ±3pp
}


def run_oos_backtest(
    train_start: int = 2015,
    train_end: int = 2019,
    test_end: int = 2025,
) -> list[OOSResult]:
    """Run out-of-sample backtest for both countries across key indicators.

    Default: train on 2015–2019, predict 2020–2025. Reports MAE per indicator.
    """
    results: list[OOSResult] = []
    us = load_us_baseline()
    cn = load_cn_baseline()

    indicators = [
        ("us_labor_share", us.labor_share, "US"),
        ("us_top_1pct_wealth_share", us.top_1pct_wealth_share, "US"),
        ("us_mean_markup_sw", us.mean_markup_sw, "US"),
        ("us_real_gdp_b", us.real_gdp_b, "US"),
        ("cn_labor_share", cn.labor_share, "CN"),
        ("cn_top_1pct_wealth_share", cn.top_1pct_wealth_share, "CN"),
        ("cn_mean_markup_sw", cn.mean_markup_sw, "CN"),
        ("cn_real_gdp_b", cn.real_gdp_b, "CN"),
    ]
    if us.substitute_employment_idx is not None:
        indicators.append(("us_substitute_employment_idx", us.substitute_employment_idx, "US"))

    for indicator_name, series, country in indicators:
        try:
            rate = _fit_exponential_rate(series, train_start, train_end)
        except (KeyError, ValueError):
            continue

        n_test = test_end - train_end
        start_value = float(series[train_end])
        predictions = _project_forward(start_value, rate, n_test)
        test_years = np.arange(train_end + 1, test_end + 1)
        actuals = np.array([float(series[y]) for y in test_years])

        abs_errors = np.abs(predictions - actuals)
        mae = float(np.mean(abs_errors))
        # MAPE relative to actuals magnitude
        mae_pct = float(np.mean(abs_errors / np.maximum(np.abs(actuals), 1e-9)))
        max_error = float(np.max(abs_errors))

        tol = TOLERANCES.get(indicator_name, np.inf)
        # For GDP-like values where tolerance is a fraction, compare to mae_pct
        if indicator_name.endswith("_real_gdp_b"):
            within = mae_pct <= tol
        else:
            within = mae <= tol

        results.append(
            OOSResult(
                indicator=indicator_name,
                country=country,
                train_window=(train_start, train_end),
                test_window=(train_end + 1, test_end),
                fitted_rate=rate,
                predictions=predictions,
                actuals=actuals,
                test_years=test_years,
                mae=mae,
                mae_pct=mae_pct,
                max_error=max_error,
                within_tolerance=within,
            )
        )

    return results


def oos_summary(results: list[OOSResult]) -> pd.DataFrame:
    """Tabular summary of OOS results."""
    return pd.DataFrame([r.to_dict() for r in results])


def report_oos_findings(results: list[OOSResult]) -> str:
    """Human-readable report on OOS backtest findings."""
    lines = [
        "Out-of-sample backtest results",
        "================================",
        "",
        f"Training window: {results[0].train_window[0]}–{results[0].train_window[1]} "
        f"({results[0].train_window[1] - results[0].train_window[0]} years)",
        f"Test window: {results[0].test_window[0]}–{results[0].test_window[1]} "
        f"({results[0].test_window[1] - results[0].test_window[0] + 1} years)",
        "",
        "Per-indicator results:",
    ]

    n_passing = sum(1 for r in results if r.within_tolerance)
    for r in results:
        flag = "✓" if r.within_tolerance else "✗"
        lines.append(
            f"  {flag} {r.indicator:35s}  fitted_rate={r.fitted_rate:+.4f}/yr  "
            f"MAE={r.mae:.4f}  MAE%={r.mae_pct:.1%}  max_err={r.max_error:.4f}"
        )

    lines.extend(
        [
            "",
            f"Summary: {n_passing} / {len(results)} indicators within tolerance.",
            "",
            "Interpretation:",
            "- 'Within tolerance' means the simulator's trajectory mechanism"
            " could be calibrated from training-window data alone and would"
            " have predicted the test window within documented bounds.",
            "- Indicators outside tolerance reveal where the linear-rate"
            " projection mechanism is structurally insufficient — likely"
            " requiring richer (e.g., regime-switching, COVID-shock) dynamics.",
        ]
    )

    return "\n".join(lines)
