"""Tests for the recommendation validation module."""

from __future__ import annotations

import pytest

from src.analysis.recommendation_validation import (
    ValidationResult,
    report_validation,
    run_full_validation,
    validate_adversarial_parameters,
    validate_cross_scenario_robustness,
    validate_sensitivity_to_halved_effects,
    validate_vs_status_quo_dominance,
    validate_welfare_dominance,
)


def test_welfare_dominance_runs():
    result = validate_welfare_dominance()
    assert isinstance(result, ValidationResult)
    assert "Welfare" in result.test_name


def test_cross_scenario_robustness_runs():
    result = validate_cross_scenario_robustness()
    assert isinstance(result, ValidationResult)


def test_sensitivity_runs():
    result = validate_sensitivity_to_halved_effects()
    assert isinstance(result, ValidationResult)
    assert "delta_normal" in result.details
    assert "delta_halved" in result.details


def test_adversarial_runs():
    result = validate_adversarial_parameters()
    assert isinstance(result, ValidationResult)


def test_status_quo_dominance_runs():
    result = validate_vs_status_quo_dominance()
    assert isinstance(result, ValidationResult)


def test_full_validation_returns_five_results():
    results = run_full_validation()
    assert len(results) == 5
    for r in results:
        assert isinstance(r, ValidationResult)


def test_validation_report_is_string():
    results = run_full_validation()
    report = report_validation(results)
    assert isinstance(report, str)
    assert "Tests passed" in report


def test_package_r_dominates_status_quo():
    """Package R should beat status quo on stability metrics. This is the
    minimum bar — if it doesn't even beat doing nothing, the recommendation
    is indefensible."""
    result = validate_vs_status_quo_dominance()
    assert result.passes, (
        f"Package R does not dominate status quo: {result.finding}"
    )


def test_package_r_robust_to_halved_effects():
    """The recommendation should not be fragile to v2.0 calibration. If
    halving effect sizes destroys the gain, the calibration assumptions
    are too aggressive."""
    result = validate_sensitivity_to_halved_effects()
    assert result.details["delta_halved"] > 0, (
        "Package R becomes net-negative under halved effects"
    )


def test_package_r_survives_adversarial_regime():
    """The recommendation should survive worst-case parameter combinations
    that adversarial reviewers would attack with."""
    result = validate_adversarial_parameters()
    assert result.passes, (
        f"Package R fails adversarial test: {result.finding}"
    )
