"""Robust Decision Making (RDM) wrapper around the bilateral simulator.

Uses EMA Workbench (Kwakkel-Pruyt) to run the simulator across thousands
of parameter draws sampling from the literature-anchored distributions
declared in PREREGISTRATION.md §7. Output is a policy-regret surface that
identifies the conditions under which each package wins or loses — see
PREREGISTRATION.md Hypothesis 9.

References
----------
Lempert, Popper & Bankes (2003) RAND foundational text.
Kwakkel & Pruyt (2013) EMA Workbench.
Kasprzyk et al. (2013) many-objective robust decision making.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
import pandas as pd

from ema_workbench import (
    Model,
    RealParameter,
    ScalarOutcome,
    perform_experiments,
    ema_logging,
)

from src.core import BilateralSimulator, SimulatorConfig
from src.packages import ALL_PACKAGES, PolicyPackage, get_package


# Quiet down EMA Workbench's default INFO chatter.
ema_logging.log_to_stderr(logging.WARNING)


# =============================================================================
# Parameter distributions per PREREGISTRATION.md §7
# =============================================================================
# Each tuple is (low, high) for uniform sampling over the literature range.
# Distributions in the prereg document are richer (truncated normals etc.);
# uniform is a defensible first pass and what EMA Workbench's
# perform_experiments default LHS sampler uses.

UNCERTAINTY_RANGES: dict[str, tuple[float, float]] = {
    # σ ∈ [1.1, 2.0] — Acemoglu-Restrepo 2022 Table 3
    "sigma_task_elasticity": (1.1, 2.0),
    # Capital flight ε ∈ [0.002, 0.012] — v2.0 Jakobsen 2020 + Saez-Zucman 2022;
    # was [0.003, 0.015] in v1.0 (Bach 2014 + Brülhart 2022).
    "capital_flight_elasticity": (0.002, 0.012),
    # Reskilling earnings effect ∈ [0.05, 0.20] — CKW 2018 + Brookings Hamilton 2024
    "reskilling_earnings_effect": (0.05, 0.20),
    # Open-weights markup dampening ∈ [0.05, 0.35] — v2.0 post-DeepSeek
    # supersedes [0.10, 0.50] of v1.0 (DeepSeek absorbed the high-end effect
    # endogenously; remaining policy-induced dampening is smaller).
    "open_weights_markup_dampening": (0.05, 0.35),
    # AI productivity growth ∈ [0.005, 0.055] — v2.0 Cazzaniga IMF 2024;
    # was [0.005, 0.05] in v1.0.
    "ai_productivity_growth": (0.005, 0.055),
    # US-China cooperation propensity ∈ [0, 1] — subjective prior; declared
    "cn_cooperation_propensity": (0.05, 0.95),
    # Coalition share ∈ [0.30, 1.00] — coalition formation test
    "base_compute_coalition_share": (0.30, 1.00),
}


# =============================================================================
# Outcome metrics
# =============================================================================
# These are what the policy-regret surface is computed over. Each one
# corresponds to one of the indicators tracked in PREREGISTRATION.md.

OUTCOME_METRICS: tuple[str, ...] = (
    "us_labor_share_2036",
    "us_top_1pct_wealth_2036",
    "us_markup_2036",
    "us_real_gdp_growth",  # cumulative 2025-2036
    "us_median_income_2036",
    "us_substitute_emp_2036",
    "cn_labor_share_2036",
    "cn_top_1pct_wealth_2036",
    "cn_real_gdp_growth",
    "geopolitical_stability_2036",
    "arms_race_2036",
)


# =============================================================================
# Single-package model factory
# =============================================================================


def make_simulator_function(package: PolicyPackage):
    """Return a callable that EMA Workbench can use as a model.

    EMA Workbench expects a function returning a dict of {outcome_name: value}.
    """
    def sim_fn(
        sigma_task_elasticity: float = 1.5,
        capital_flight_elasticity: float = 0.005,
        reskilling_earnings_effect: float = 0.10,
        open_weights_markup_dampening: float = 0.40,
        ai_productivity_growth: float = 0.020,
        cn_cooperation_propensity: float = 0.30,
        base_compute_coalition_share: float = 0.70,
    ) -> dict[str, float]:
        config = SimulatorConfig(
            sigma_task_elasticity=sigma_task_elasticity,
            capital_flight_elasticity=capital_flight_elasticity,
            reskilling_earnings_effect=reskilling_earnings_effect,
            open_weights_markup_dampening=open_weights_markup_dampening,
            ai_productivity_growth=ai_productivity_growth,
            cn_cooperation_propensity=cn_cooperation_propensity,
            base_compute_coalition_share=base_compute_coalition_share,
        )
        sim = BilateralSimulator(config=config)
        result = sim.run(
            package=package if package.code != "A" else None,
            coalition_share=base_compute_coalition_share,
            cn_cooperation=cn_cooperation_propensity,
        )
        # Find the index of 2036 (or end_year)
        years = result.years
        idx_2025 = int(np.where(years == 2025)[0][0])
        idx_end = -1

        return {
            "us_labor_share_2036": float(result.us.labor_share[idx_end]),
            "us_top_1pct_wealth_2036": float(result.us.top_1pct_wealth[idx_end]),
            "us_markup_2036": float(result.us.mean_markup[idx_end]),
            "us_real_gdp_growth": float(
                result.us.real_gdp[idx_end] / result.us.real_gdp[idx_2025] - 1.0
            ),
            "us_median_income_2036": float(result.us.median_real_income[idx_end]),
            "us_substitute_emp_2036": float(result.us.substitute_employment_idx[idx_end]),
            "cn_labor_share_2036": float(result.cn.labor_share[idx_end]),
            "cn_top_1pct_wealth_2036": float(result.cn.top_1pct_wealth[idx_end]),
            "cn_real_gdp_growth": float(
                result.cn.real_gdp[idx_end] / result.cn.real_gdp[idx_2025] - 1.0
            ),
            "geopolitical_stability_2036": float(result.geopolitical_stability[idx_end]),
            "arms_race_2036": float(result.arms_race_intensity[idx_end]),
        }

    return sim_fn


def build_ema_model(package: PolicyPackage) -> Model:
    """Build an EMA Workbench Model object for one policy package."""
    fn = make_simulator_function(package)
    m = Model(f"package{package.code}", function=fn)
    m.uncertainties = [
        RealParameter(name, lo, hi) for name, (lo, hi) in UNCERTAINTY_RANGES.items()
    ]
    m.outcomes = [ScalarOutcome(o) for o in OUTCOME_METRICS]
    return m


# =============================================================================
# Sweep runner
# =============================================================================


@dataclass
class RDMResults:
    """Results of an RDM sweep for one or more packages.

    Attributes
    ----------
    experiments : DataFrame with one row per (package, parameter draw)
    outcomes : DataFrame with one row per (package, parameter draw),
        columns = OUTCOME_METRICS
    """

    experiments: pd.DataFrame
    outcomes: pd.DataFrame

    def merge(self) -> pd.DataFrame:
        """Combine experiments and outcomes into a single wide DataFrame."""
        # Drop any duplicate columns from outcomes side (e.g., 'package' tag)
        out = self.outcomes.reset_index(drop=True)
        exp = self.experiments.reset_index(drop=True)
        out = out.loc[:, ~out.columns.isin(exp.columns)]
        return pd.concat([exp, out], axis=1)

    def package_summary(self) -> pd.DataFrame:
        """For each package, report P10/P50/P90 of each outcome."""
        merged = self.merge()
        if "package" not in merged.columns:
            return merged.describe()
        rows = []
        for pkg, grp in merged.groupby("package"):
            row = {"package": pkg}
            for metric in OUTCOME_METRICS:
                if metric in grp.columns:
                    row[f"{metric}_p10"] = grp[metric].quantile(0.10)
                    row[f"{metric}_p50"] = grp[metric].quantile(0.50)
                    row[f"{metric}_p90"] = grp[metric].quantile(0.90)
            rows.append(row)
        return pd.DataFrame(rows).set_index("package")


def run_rdm_for_package(
    package_code: str,
    n_scenarios: int = 1000,
) -> RDMResults:
    """Run an RDM sweep for a single package.

    Parameters
    ----------
    package_code : 'A' through 'G'
    n_scenarios : number of LHS-sampled parameter combinations
    """
    package = get_package(package_code)
    model = build_ema_model(package)
    experiments, outcomes_dict = perform_experiments(model, scenarios=n_scenarios)
    outcomes_df = pd.DataFrame(outcomes_dict)
    # Tag only the experiments DataFrame with package code; outcomes
    # is concatenated index-wise so the package label aligns by row.
    experiments["package"] = package_code
    return RDMResults(experiments=experiments, outcomes=outcomes_df)


def _sample_uncertainties(n: int, seed: int = 20260501) -> pd.DataFrame:
    """Generate Latin Hypercube samples over the uncertainty ranges.

    Same samples used for every package so that policy-regret comparisons
    across packages are valid (each package is evaluated on the same
    counterfactual futures).
    """
    rng = np.random.default_rng(seed)
    n_dims = len(UNCERTAINTY_RANGES)
    # Stratified LHS: divide [0,1] into n bins, sample one point per bin per dim
    base = np.arange(n).reshape(-1, 1).repeat(n_dims, axis=1)
    bins = (base + rng.random((n, n_dims))) / n
    # Shuffle each column independently
    for j in range(n_dims):
        rng.shuffle(bins[:, j])
    samples = {}
    for j, (name, (lo, hi)) in enumerate(UNCERTAINTY_RANGES.items()):
        samples[name] = lo + bins[:, j] * (hi - lo)
    return pd.DataFrame(samples)


def run_rdm_for_all_packages(
    n_scenarios: int = 1000,
    package_codes: tuple[str, ...] | None = None,
    seed: int = 20260501,
) -> RDMResults:
    """Run an RDM sweep across multiple packages on shared parameter draws.

    Parameters
    ----------
    n_scenarios : LHS draws (each evaluated under every package)
    package_codes : subset of packages; default = all 7
    seed : RNG seed for reproducibility
    """
    if package_codes is None:
        package_codes = tuple(p.code for p in ALL_PACKAGES)

    samples = _sample_uncertainties(n_scenarios, seed=seed)
    all_exp = []
    all_out = []

    for code in package_codes:
        package = get_package(code)
        sim_fn = make_simulator_function(package)
        outcomes = []
        for _, row in samples.iterrows():
            kwargs = row.to_dict()
            outcomes.append(sim_fn(**kwargs))
        out_df = pd.DataFrame(outcomes)
        exp_df = samples.copy()
        exp_df["package"] = code
        exp_df["scenario_id"] = np.arange(n_scenarios)
        out_df["scenario_id"] = np.arange(n_scenarios)
        all_exp.append(exp_df)
        all_out.append(out_df)

    return RDMResults(
        experiments=pd.concat(all_exp, ignore_index=True),
        outcomes=pd.concat(all_out, ignore_index=True),
    )


def policy_regret(
    rdm_results: RDMResults,
    metric: str,
    higher_is_better: bool = True,
) -> pd.DataFrame:
    """Compute policy regret per package per draw.

    Regret of package P in draw d = (best metric across packages in draw d)
    - (metric of P in draw d). Lower regret = more robust.

    Returns DataFrame with one row per package and columns:
    mean_regret, max_regret, fraction_best.
    """
    merged = rdm_results.merge()
    # Pivot so that each row is a draw with columns = packages
    # scenario_id is the shared draw identifier set in run_rdm_for_all_packages
    if "scenario_id" not in merged.columns:
        raise ValueError(
            "scenario_id column missing — RDM must be run with shared LHS sampling"
        )
    pivot = merged.pivot_table(
        index="scenario_id", columns="package", values=metric, aggfunc="mean"
    )
    if higher_is_better:
        best_per_draw = pivot.max(axis=1)
        regret = pivot.sub(best_per_draw, axis=0).abs()
    else:
        best_per_draw = pivot.min(axis=1)
        regret = pivot.sub(best_per_draw, axis=0).abs()

    summary = pd.DataFrame(
        {
            "mean_regret": regret.mean(),
            "max_regret": regret.max(),
            "fraction_best": (regret < 1e-9).mean(),
        }
    )
    summary.index.name = "package"
    return summary
