"""Tests for the out-of-sample backtest module."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.analysis.out_of_sample import (
    OOSResult,
    TOLERANCES,
    _fit_exponential_rate,
    _project_forward,
    oos_summary,
    report_oos_findings,
    run_oos_backtest,
)


def test_fit_exponential_rate_known_input():
    """5% per year for 4 years should fit to 0.05."""
    series = pd.Series({2015: 100.0, 2016: 105.0, 2017: 110.25, 2018: 115.7625, 2019: 121.550625})
    rate = _fit_exponential_rate(series, 2015, 2019)
    assert rate == pytest.approx(0.05, abs=1e-6)


def test_fit_exponential_rate_negative_growth():
    series = pd.Series({2015: 100.0, 2019: 90.0})
    rate = _fit_exponential_rate(series, 2015, 2019)
    # Should be negative
    assert rate < 0
    # 90/100 = 0.9; (0.9)^(1/4) = 0.9740
    expected = 0.9740 - 1
    assert rate == pytest.approx(expected, abs=1e-3)


def test_project_forward_compounding():
    """Project 100 forward 3 years at 10%/yr."""
    result = _project_forward(100.0, 0.10, 3)
    np.testing.assert_allclose(result, [110.0, 121.0, 133.1])


def test_oos_backtest_runs():
    results = run_oos_backtest()
    assert len(results) > 0
    for r in results:
        assert isinstance(r, OOSResult)
        assert r.train_window == (2015, 2019)
        assert r.test_window == (2020, 2025)


def test_oos_backtest_us_labor_share_within_tolerance():
    """US labor share should be within 2pp tolerance based on training calibration."""
    results = run_oos_backtest()
    us_ls = [r for r in results if r.indicator == "us_labor_share"][0]
    assert us_ls.mae < 0.02


def test_oos_backtest_us_gdp_within_tolerance():
    """US real GDP MAPE should be within 5% based on training calibration."""
    results = run_oos_backtest()
    us_gdp = [r for r in results if r.indicator == "us_real_gdp_b"][0]
    assert us_gdp.mae_pct < 0.05


def test_oos_summary_returns_dataframe():
    results = run_oos_backtest()
    summary = oos_summary(results)
    assert isinstance(summary, pd.DataFrame)
    assert "indicator" in summary.columns
    assert "mae" in summary.columns
    assert len(summary) == len(results)


def test_oos_report_is_string():
    results = run_oos_backtest()
    report = report_oos_findings(results)
    assert isinstance(report, str)
    assert "Out-of-sample backtest" in report
    assert "Training window" in report


def test_majority_of_indicators_within_tolerance():
    """Strong claim: most indicators should pass OOS validation. If they
    don't, the model's projection mechanism is structurally weak and the
    paper's forward projections are not credible."""
    results = run_oos_backtest()
    n_passing = sum(1 for r in results if r.within_tolerance)
    assert n_passing / len(results) >= 0.6, (
        f"Only {n_passing}/{len(results)} indicators within tolerance; "
        "model projection mechanism may be inadequate"
    )


def test_tolerances_are_documented():
    """Tolerances should match PREREGISTRATION.md §8 — explicit documentation."""
    assert TOLERANCES["us_labor_share"] == 0.02
    assert TOLERANCES["us_top_1pct_wealth_share"] == 0.02
    assert TOLERANCES["us_mean_markup_sw"] == 0.05


def test_fit_rate_raises_on_missing_year():
    series = pd.Series({2015: 100.0, 2019: 121.0})
    with pytest.raises(KeyError):
        _fit_exponential_rate(series, 2014, 2019)


def test_fit_rate_raises_on_non_positive_start():
    series = pd.Series({2015: 0.0, 2019: 100.0})
    with pytest.raises(ValueError):
        _fit_exponential_rate(series, 2015, 2019)
