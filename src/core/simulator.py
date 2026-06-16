"""Bilateral US/China simulator — reduced-form delta model.

Per the strategic decision documented in CLAUDE.md (2026-05-01 addendum):
this simulator deliberately uses a *reduced-form* approach rather than a
fully-derived structural model. The justification:

    1. The prototype's structural HANK-style build hit two calibration
       failures (GDP overshoot, top-1% wealth share moves wrong direction)
       documented in CLAUDE.md. Re-deriving from first principles risks
       repeating those failures.

    2. The project's actual question is comparative: which policy package
       dominates under what conditions, expressed as deltas vs. status quo.
       Counterfactual deltas are systematically more accurate than absolute
       predictions because common-mode model errors cancel between
       baseline and policy branches (this is how CBO scoring, IMF Article
       IV, and Treasury OBM all work).

    3. The structural Acemoglu-Restrepo task-based production module
       (src/production/task_based.py) is retained as a methodological
       sanity check and for the methodology section's narrative — it
       demonstrates that the displacement / reinstatement / capital-bias
       mechanics are correctly understood. But the policy-comparison runs
       use the reduced-form trajectory below.

What the simulator does:
    - For each indicator (labor share, top 1% wealth, mean markup, GDP
      growth, by-decile income), computes a status-quo trajectory
      calibrated to BLS / SCF / DLEU / BEA observed data 2015-2025
    - Extends the trajectory forward to end_year using a documented
      forward-projection rule (BASELINE_2026.md §3 central values)
    - For each policy package, applies the documented effect-size deltas
      from PolicyLever.parameter_changes
    - For coordination-dependent levers, applies them only if the
      coalition share exceeds the lever's threshold; partial coordination
      produces partial effects

This is honest about its reduced-form nature. The methodology section
of the paper must explicitly state this and explain why it's the right
choice for the project's comparative-policy question.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from src.analysis.baseline_data import (
    BaselineSeries,
    load_cn_baseline,
    load_us_baseline,
)
from src.packages.base import PolicyPackage


# =============================================================================
# Configuration
# =============================================================================


@dataclass
class SimulatorConfig:
    """Configuration parameters with literature anchors.

    Most defaults match BASELINE_2026.md §3 central projections.
    Sweepable parameters (those with distributions in PREREGISTRATION.md
    §7) have explicit RDM sampling support via overrides.
    """

    start_year: int = 2015
    backtest_end_year: int = 2025  # observed data ends here
    end_year: int = 2036  # projection horizon

    # Baseline forward-projection rates (calibrated to hit BASELINE_2026.md §3
    # 2036 central values from 2025 anchor).
    # Labor share 0.56 -> 0.51: 0.911^(1/11) = 0.9915 → 0.85%/yr decay
    us_labor_share_decay_rate: float = 0.0085
    # Top 1% 0.304 -> 0.335: 1.102^(1/11) = 1.0089 → 0.89%/yr growth
    us_top_1pct_growth_rate: float = 0.0089
    # Markup 1.22 -> 1.28: 1.049^(1/11) = 1.0044 → 0.44%/yr growth
    us_markup_growth_rate: float = 0.0044
    # Real GDP +27% cumulative = 2.2%/yr
    us_gdp_growth_rate: float = 0.022
    # Substitute employment 100 -> 82 by 2036 (~18% displacement) = 1.8%/yr decay
    us_substitute_emp_decay: float = 0.0180

    # China forward projections to 2036
    cn_labor_share_decay_rate: float = 0.0080  # 0.49 -> 0.45 by 2036
    cn_top_1pct_growth_rate: float = 0.0040  # 0.305 -> 0.32
    cn_markup_growth_rate: float = 0.0050  # 1.13 -> 1.20
    cn_gdp_growth_rate: float = 0.045  # IMF WEO 2025-2036 ~4.5%

    # Sweep parameters (RDM)
    # v2.0 updates: see EMPIRICAL_ANALOGS.md §7.1, §7.4, §7.5
    sigma_task_elasticity: float = 1.5  # PREREG §7 — Acemoglu-Restrepo 2022
    capital_flight_elasticity: float = 0.004  # v2.0 Jakobsen et al. + Saez-Zucman 2022
    reskilling_earnings_effect: float = 0.08  # v2.0 Brookings Hamilton 2024; was 0.10 v1.0
    open_weights_markup_dampening: float = 0.20  # v2.0 post-DeepSeek; was 0.40 v1.0
    ai_productivity_growth: float = 0.018  # v2.0 Cazzaniga IMF 2024 median
    cn_cooperation_propensity: float = 0.30  # subjective prior — sweep

    # Coalition / coordination
    base_compute_coalition_share: float = 0.70

    # Cross-class welfare (from Hypothesis 4)
    n_deciles: int = 10
    decile_income_share: tuple[float, ...] = (
        0.04, 0.05, 0.07, 0.08, 0.09, 0.10, 0.12, 0.13, 0.15, 0.17,
    )

    # Geopolitical illustrative components (PREREG flags Tier D)
    base_arms_race_intensity: float = 0.70  # SIPRI 2025
    base_geopolitical_stability: float = 38.0  # Atlantic Council
    geopolitical_decay_rate: float = 0.008  # per year under status quo

    # Pre-loaded baseline series (set via load_baselines)
    us_baseline: BaselineSeries | None = None
    cn_baseline: BaselineSeries | None = None


# =============================================================================
# Result types
# =============================================================================


@dataclass(frozen=True)
class CountryResult:
    """One country's full trajectory."""

    code: str
    years: np.ndarray
    labor_share: np.ndarray
    top_1pct_wealth: np.ndarray
    top_10pct_wealth: np.ndarray
    bottom_50pct_wealth: np.ndarray
    mean_markup: np.ndarray
    real_gdp: np.ndarray  # billions, chained 2017 USD
    substitute_employment_idx: np.ndarray
    median_real_income: np.ndarray  # by year
    decile_real_income: np.ndarray  # (n_years, 10) — used in cross-class test


@dataclass(frozen=True)
class SimulationResult:
    """Full simulation output covering both countries plus geopolitical layer."""

    config: SimulatorConfig
    package_code: str
    coalition_share: float
    cn_cooperation: float
    us: CountryResult
    cn: CountryResult
    geopolitical_stability: np.ndarray
    arms_race_intensity: np.ndarray
    audit_trail: list[tuple[str, str, str, float]] = field(default_factory=list)

    @property
    def years(self) -> np.ndarray:
        return self.us.years

    def cumulative_growth(self, country: str = "us", indicator: str = "real_gdp") -> float:
        cr = self.us if country.lower() == "us" else self.cn
        series = getattr(cr, indicator)
        return float(series[-1] / series[0] - 1.0)

    def to_dataframe(self) -> pd.DataFrame:
        rows = []
        for i, y in enumerate(self.years):
            rows.append(
                {
                    "year": int(y),
                    "us_labor_share": self.us.labor_share[i],
                    "us_top_1pct": self.us.top_1pct_wealth[i],
                    "us_top_10pct": self.us.top_10pct_wealth[i],
                    "us_bottom_50pct": self.us.bottom_50pct_wealth[i],
                    "us_markup": self.us.mean_markup[i],
                    "us_real_gdp": self.us.real_gdp[i],
                    "us_sub_emp_idx": self.us.substitute_employment_idx[i],
                    "us_median_income": self.us.median_real_income[i],
                    "cn_labor_share": self.cn.labor_share[i],
                    "cn_top_1pct": self.cn.top_1pct_wealth[i],
                    "cn_markup": self.cn.mean_markup[i],
                    "cn_real_gdp": self.cn.real_gdp[i],
                    "cn_median_income": self.cn.median_real_income[i],
                    "geopolitical_stability": self.geopolitical_stability[i],
                    "arms_race": self.arms_race_intensity[i],
                }
            )
        return pd.DataFrame(rows).set_index("year")


# =============================================================================
# Simulator
# =============================================================================


class BilateralSimulator:
    """Bilateral US-China simulator using reduced-form trajectories.

    Usage
    -----
    >>> sim = BilateralSimulator()
    >>> result = sim.run()  # status quo
    >>> df = result.to_dataframe()

    Or with a policy package:

    >>> from src.packages import CERN_AI
    >>> sim = BilateralSimulator()
    >>> result = sim.run(package=CERN_AI, coalition_share=0.7)
    """

    def __init__(self, config: SimulatorConfig | None = None) -> None:
        self.config = deepcopy(config) if config is not None else SimulatorConfig()
        if self.config.us_baseline is None:
            self.config.us_baseline = load_us_baseline()
        if self.config.cn_baseline is None:
            self.config.cn_baseline = load_cn_baseline()

    def _baseline_trajectory(
        self,
        country: str,
    ) -> CountryResult:
        """Build the status-quo trajectory for one country.

        For 2015-2025 (backtest period), uses observed values from
        baseline_data. For 2026-end_year, projects forward using the
        decay/growth rates calibrated in SimulatorConfig.
        """
        c = self.config
        base = c.us_baseline if country == "US" else c.cn_baseline
        assert base is not None
        years = np.arange(c.start_year, c.end_year + 1)
        n = len(years)

        labor_share = np.zeros(n)
        top_1pct = np.zeros(n)
        top_10pct = np.zeros(n)
        bottom_50pct = np.zeros(n)
        markup = np.zeros(n)
        real_gdp = np.zeros(n)
        sub_emp = np.zeros(n)

        # Backtest period: copy observed values
        for i, y in enumerate(years):
            if y in base.labor_share.index:
                labor_share[i] = base.labor_share[y]
                top_1pct[i] = base.top_1pct_wealth_share[y]
                markup[i] = base.mean_markup_sw[y]
                real_gdp[i] = base.real_gdp_b[y]
                if base.top_10pct_wealth_share is not None:
                    top_10pct[i] = base.top_10pct_wealth_share[y]
                else:
                    top_10pct[i] = 0.70  # CN approximate from WID
                if base.bottom_50pct_wealth_share is not None:
                    bottom_50pct[i] = base.bottom_50pct_wealth_share[y]
                else:
                    bottom_50pct[i] = 0.05
                if base.substitute_employment_idx is not None:
                    sub_emp[i] = base.substitute_employment_idx[y]
                else:
                    sub_emp[i] = 100.0
            else:
                # Forward projection from previous year
                labor_share[i] = labor_share[i - 1] * (
                    1.0 - (
                        c.us_labor_share_decay_rate
                        if country == "US"
                        else c.cn_labor_share_decay_rate
                    )
                )
                top_1pct[i] = top_1pct[i - 1] * (
                    1.0 + (
                        c.us_top_1pct_growth_rate
                        if country == "US"
                        else c.cn_top_1pct_growth_rate
                    )
                )
                top_10pct[i] = min(0.85, top_10pct[i - 1] * 1.001)
                bottom_50pct[i] = max(0.005, bottom_50pct[i - 1] * 0.997)
                markup[i] = markup[i - 1] * (
                    1.0 + (
                        c.us_markup_growth_rate
                        if country == "US"
                        else c.cn_markup_growth_rate
                    )
                )
                real_gdp[i] = real_gdp[i - 1] * (
                    1.0 + (
                        c.us_gdp_growth_rate
                        if country == "US"
                        else c.cn_gdp_growth_rate
                    )
                )
                sub_emp[i] = sub_emp[i - 1] * (
                    1.0 - c.us_substitute_emp_decay
                )

        # Median real income (decile 5 of distribution; indexed to GDP)
        median_real_income = real_gdp / real_gdp[0] * 100.0
        # By-decile real income (matrix)
        decile_real_income = np.outer(real_gdp / real_gdp[0] * 100.0, c.decile_income_share) * 10.0
        # Decile incomes shift toward bottom over time as wealth concentrates
        # (actually they shift toward top; this is the inequality channel)
        for i in range(1, n):
            top_decile_factor = top_10pct[i] / top_10pct[0]
            decile_real_income[i] *= np.array(
                [
                    1.0 / top_decile_factor ** 0.5,  # bottom deciles lose
                    1.0 / top_decile_factor ** 0.4,
                    1.0 / top_decile_factor ** 0.3,
                    1.0 / top_decile_factor ** 0.2,
                    1.0 / top_decile_factor ** 0.1,
                    1.0,  # decile 6 is roughly neutral
                    top_decile_factor ** 0.1,
                    top_decile_factor ** 0.3,
                    top_decile_factor ** 0.6,
                    top_decile_factor ** 1.0,  # top decile gains proportionally
                ]
            )

        return CountryResult(
            code=country,
            years=years,
            labor_share=labor_share,
            top_1pct_wealth=top_1pct,
            top_10pct_wealth=top_10pct,
            bottom_50pct_wealth=bottom_50pct,
            mean_markup=markup,
            real_gdp=real_gdp,
            substitute_employment_idx=sub_emp,
            median_real_income=median_real_income,
            decile_real_income=decile_real_income,
        )

    def _apply_package_deltas(
        self,
        baseline: CountryResult,
        package: PolicyPackage,
        coalition_share: float,
        cn_cooperation: float,
        country: str,
    ) -> tuple[CountryResult, list[tuple[str, str, str, float]]]:
        """Apply package-induced deltas to a baseline trajectory.

        Returns the modified trajectory plus an audit trail of which
        levers modified which indicator and by how much.

        Effect sizes come from each lever's parameter_changes — these are
        anchored to documented empirical analogs (will be expanded in
        EMPIRICAL_ANALOGS.md / Phase 1).
        """
        c = self.config
        audit: list[tuple[str, str, str, float]] = []
        years = baseline.years
        c_year_zero = c.start_year
        package_active = years >= package.activation_year

        # Start from the baseline arrays
        labor_share = baseline.labor_share.copy()
        top_1pct = baseline.top_1pct_wealth.copy()
        top_10pct = baseline.top_10pct_wealth.copy()
        bottom_50pct = baseline.bottom_50pct_wealth.copy()
        markup = baseline.mean_markup.copy()
        real_gdp = baseline.real_gdp.copy()
        sub_emp = baseline.substitute_employment_idx.copy()
        median_income = baseline.median_real_income.copy()
        decile_income = baseline.decile_real_income.copy()

        # If country == 'CN' and CN's cooperation is partial, scale all
        # coordination-dependent lever effects by cooperation propensity
        cn_factor = cn_cooperation if country == "CN" else 1.0

        for lever in package.levers:
            # Coalition gating
            if lever.requires_coordination and coalition_share < lever.coalition_threshold:
                audit.append((lever.name, "<gated>", "skipped", coalition_share))
                continue

            # Effective intensity = (1 if domestic) or (coalition_share / threshold) for coord
            if lever.requires_coordination:
                intensity = min(
                    1.0, coalition_share / max(lever.coalition_threshold, 0.01)
                ) * cn_factor
            else:
                intensity = 1.0

            # Apply lever-specific effects
            for key, value in lever.parameter_changes.items():
                # Effects on markups
                if key == "ai_markup_growth_dampening":
                    # Slow markup growth in years package is active
                    for i in range(len(years)):
                        if package_active[i] and i > 0:
                            additional_dampening = value * intensity
                            base_growth = markup[i] / markup[i - 1] - 1.0
                            damped = base_growth * (1.0 - additional_dampening)
                            markup[i] = markup[i - 1] * (1.0 + damped)
                    audit.append((lever.name, "markup_growth", "dampen", value * intensity))

                elif key == "ai_sector_concentration_shift":
                    # Higher concentration → higher markup; this lever lowers it
                    shift = value * intensity
                    for i in range(len(years)):
                        if package_active[i]:
                            markup[i] = markup[i] * (1.0 + shift * 0.3)
                    audit.append((lever.name, "concentration", "shift", shift))

                elif key in ("epsilon_sub_shift", "skill_mix_complement_shift"):
                    # Reskilling → labor share rises, sub-worker employment recovers
                    boost = value * intensity * 0.01  # convert ε shift to labor-share effect
                    for i in range(len(years)):
                        if package_active[i]:
                            labor_share[i] += boost * 0.10  # 10% pass-through to labor share
                            sub_emp[i] *= (1.0 + boost * 0.005)
                    audit.append((lever.name, "labor_share", "boost", boost))

                elif key == "reskilling_earnings_effect":
                    # Earnings effect for displaced workers → boosts deciles 3-7
                    for i in range(len(years)):
                        if package_active[i]:
                            for d in range(2, 7):  # deciles 3-7
                                decile_income[i, d] *= (1.0 + value * intensity * 0.50)
                    audit.append((lever.name, "decile_3_7", "boost", value * intensity))

                elif key == "ubc_grant_per_capita":
                    # UBC → bottom 50% wealth share rises; top 1% falls slightly
                    grant_effect = value / 50000.0 * intensity  # normalize to UBC unit
                    for i in range(len(years)):
                        if package_active[i]:
                            bottom_50pct[i] = min(0.10, bottom_50pct[i] + grant_effect * 0.01)
                            top_1pct[i] = max(0.20, top_1pct[i] - grant_effect * 0.005)
                    audit.append((lever.name, "wealth_floor", "lift", grant_effect))

                elif key == "ubi_monthly_per_adult":
                    # UBI → median income rises; bottom deciles boosted most
                    ubi_per_year = value * 12 / 30000.0 * intensity  # normalize
                    for i in range(len(years)):
                        if package_active[i]:
                            for d in range(0, 10):
                                weight = max(0, 1.0 - d * 0.10)  # bottom decile gets 100%
                                decile_income[i, d] *= (1.0 + ubi_per_year * weight * 0.20)
                            median_income[i] *= (1.0 + ubi_per_year * 0.05)
                    audit.append((lever.name, "ubi", "transfer", ubi_per_year))

                elif key == "wealth_tax_marginal_top":
                    # Wealth tax → top 1% share falls, bottom 50% rises
                    tax_strength = value / 0.03 * intensity
                    for i in range(len(years)):
                        if package_active[i]:
                            top_1pct[i] = max(0.20, top_1pct[i] - tax_strength * 0.003)
                            bottom_50pct[i] = min(0.10, bottom_50pct[i] + tax_strength * 0.001)
                    audit.append((lever.name, "wealth_concentration", "tax", tax_strength))

                elif key == "ai_sector_tax_rate":
                    # AI tax → small GDP drag, modest distributional shift
                    rate = value * intensity
                    for i in range(len(years)):
                        if package_active[i]:
                            real_gdp[i] *= (1.0 - rate * 0.05)  # ~5% deadweight per pp
                    audit.append((lever.name, "real_gdp", "drag", rate))

                elif key == "transfer_funding_per_gdp":
                    # Transfer funding → boosts median income directly
                    transfer = value * intensity
                    for i in range(len(years)):
                        if package_active[i]:
                            for d in range(0, 6):  # bottom 60% receives
                                decile_income[i, d] *= (1.0 + transfer * 0.50)
                            median_income[i] *= (1.0 + transfer * 0.10)
                    audit.append((lever.name, "transfers", "boost", transfer))

                elif key == "labor_augmenting_productivity_growth":
                    # Directed R&D → faster labor productivity → higher GDP, higher labor share
                    extra = value * intensity
                    for i in range(len(years)):
                        if package_active[i] and i > 0:
                            real_gdp[i] *= (1.0 + extra)
                            labor_share[i] += extra * 0.02
                    audit.append((lever.name, "labor_productivity", "lift", extra))

                elif key == "public_compute_per_gdp":
                    # Public compute infrastructure → small GDP boost from
                    # entry-barrier reduction + diffuse productivity gains
                    boost = value * intensity * 0.5  # 0.5x leverage on GDP
                    for i in range(len(years)):
                        if package_active[i]:
                            real_gdp[i] *= (1.0 + boost)
                            markup[i] *= (1.0 - boost * 0.10)  # slight markup pressure
                    audit.append((lever.name, "public_compute", "lift", boost))

                elif key == "ai_lab_entry_barrier":
                    # Lowered entry barriers → markup pressure, faster diffusion
                    shift = value * intensity
                    for i in range(len(years)):
                        if package_active[i]:
                            markup[i] *= (1.0 + shift * 0.20)  # negative shift → markup falls
                    audit.append((lever.name, "entry_barrier", "shift", shift))

                elif key == "frontier_capability_diffusion":
                    # Capability diffusion → AI sector less concentrated;
                    # markup pressure plus modest GDP boost
                    diff = value * intensity
                    for i in range(len(years)):
                        if package_active[i]:
                            markup[i] *= (1.0 - diff * 0.05)
                            real_gdp[i] *= (1.0 + diff * 0.01)
                    audit.append((lever.name, "diffusion", "lift", diff))

                elif key == "capability_disclosure_compliance":
                    # Pre-deployment evaluation requirements → small markup
                    # compliance cost, modest stability gain (captured in
                    # geopolitical layer)
                    compliance = value * intensity
                    for i in range(len(years)):
                        if package_active[i]:
                            markup[i] *= (1.0 + compliance * 0.01)  # small compliance cost
                    audit.append((lever.name, "disclosure", "raise", compliance))

                elif key == "ai_arms_race_intensity":
                    # Captured below in geopolitical layer
                    audit.append((lever.name, "arms_race", "shift", value * intensity))

                elif key == "geopolitical_stability_index":
                    audit.append((lever.name, "stability", "shift", value * intensity))

                else:
                    # State-only or unmodeled — record but don't modify trajectory
                    audit.append((lever.name, key, "state_only", value))

        # Re-derive median income: tracks GDP growth + cumulative redistribution
        # effects on the median household. Computed as average of decile 5 and 6
        # of the (updated) decile_income matrix, normalized to baseline year.
        median_dollar = (decile_income[:, 4] + decile_income[:, 5]) / 2.0
        median_income = median_dollar / median_dollar[0] * 100.0

        # Median income should also propagate the underlying GDP boost from
        # productivity-side levers (e.g., directed R&D in Package F).
        gdp_relative = real_gdp / baseline.real_gdp
        median_income = median_income * gdp_relative

        # Apply documented lever interactions (substitutability /
        # complementarity). See src/core/interactions.py and
        # PREREGISTRATION.md Hypothesis 6.
        from src.core.interactions import total_correction_for_outcome, interaction_audit

        # Apply interaction corrections to the *delta* (active − baseline),
        # not to the absolute value, so corrections compound only what
        # the package itself caused.
        def _apply_correction(active: np.ndarray, baseline: np.ndarray, outcome: str) -> np.ndarray:
            correction = total_correction_for_outcome(package, outcome)
            if abs(correction - 1.0) < 1e-9:
                return active
            delta = active - baseline
            return baseline + delta * correction

        labor_share = _apply_correction(labor_share, baseline.labor_share, "us_labor_share")
        top_1pct = _apply_correction(top_1pct, baseline.top_1pct_wealth,
                                     "us_top_1pct" if country == "US" else "cn_top_1pct")
        markup = _apply_correction(markup, baseline.mean_markup, "us_markup")
        median_income = _apply_correction(median_income, baseline.median_real_income, "us_median_income")
        sub_emp = _apply_correction(sub_emp, baseline.substitute_employment_idx, "us_substitute_emp")

        # Record interaction audit entries
        for ix_name, outcome, correction in interaction_audit(package):
            audit.append((ix_name, outcome, "interaction", correction))

        return (
            CountryResult(
                code=country,
                years=years,
                labor_share=labor_share,
                top_1pct_wealth=top_1pct,
                top_10pct_wealth=top_10pct,
                bottom_50pct_wealth=bottom_50pct,
                mean_markup=markup,
                real_gdp=real_gdp,
                substitute_employment_idx=sub_emp,
                median_real_income=median_income,
                decile_real_income=decile_income,
            ),
            audit,
        )

    def _geopolitical_trajectory(
        self,
        package: PolicyPackage | None,
        coalition_share: float,
        cn_cooperation: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Compute geopolitical stability + arms race intensity trajectories.

        Per PREREGISTRATION.md Tier D — illustrative, not predictive.
        """
        c = self.config
        years = np.arange(c.start_year, c.end_year + 1)
        n = len(years)
        stability = np.full(n, c.base_geopolitical_stability)
        arms_race = np.full(n, c.base_arms_race_intensity)

        # Status quo decay
        for i in range(1, n):
            stability[i] = stability[i - 1] * (1.0 - c.geopolitical_decay_rate)
            arms_race[i] = arms_race[i - 1] * 1.005  # slight escalation

        if package is None:
            return stability, arms_race

        # Apply package-induced effects
        for lever in package.levers:
            if lever.requires_coordination and coalition_share < lever.coalition_threshold:
                continue
            intensity = (
                min(1.0, coalition_share / max(lever.coalition_threshold, 0.01))
                if lever.requires_coordination
                else 1.0
            ) * cn_cooperation

            for key, value in lever.parameter_changes.items():
                if key == "ai_arms_race_intensity":
                    package_active = years >= package.activation_year
                    arms_race = np.where(
                        package_active,
                        arms_race * (1.0 + value * intensity),
                        arms_race,
                    )
                elif key == "geopolitical_stability_index":
                    package_active = years >= package.activation_year
                    stability = np.where(
                        package_active,
                        stability + value * intensity,
                        stability,
                    )

        return stability, arms_race

    def run(
        self,
        package: PolicyPackage | None = None,
        coalition_share: float | None = None,
        cn_cooperation: float | None = None,
    ) -> SimulationResult:
        """Run the simulator for a package (or status quo if package is None).

        Parameters
        ----------
        package : the policy package; if None, runs status quo (PolicyPackage A)
        coalition_share : fraction of frontier compute participating in
            coordination-dependent levers; defaults to config base
        cn_cooperation : China's cooperation propensity; defaults to config
        """
        c = self.config
        coalition = (
            coalition_share if coalition_share is not None
            else c.base_compute_coalition_share
        )
        cn_coop = cn_cooperation if cn_cooperation is not None else c.cn_cooperation_propensity

        us_baseline = self._baseline_trajectory("US")
        cn_baseline = self._baseline_trajectory("CN")

        if package is None or len(package.levers) == 0:
            # Status quo — return baselines
            stability, arms = self._geopolitical_trajectory(None, coalition, cn_coop)
            return SimulationResult(
                config=c,
                package_code="A",
                coalition_share=coalition,
                cn_cooperation=cn_coop,
                us=us_baseline,
                cn=cn_baseline,
                geopolitical_stability=stability,
                arms_race_intensity=arms,
                audit_trail=[],
            )

        us_trajectory, us_audit = self._apply_package_deltas(
            us_baseline, package, coalition, cn_coop, country="US"
        )
        cn_trajectory, cn_audit = self._apply_package_deltas(
            cn_baseline, package, coalition, cn_coop, country="CN"
        )
        stability, arms = self._geopolitical_trajectory(package, coalition, cn_coop)

        return SimulationResult(
            config=c,
            package_code=package.code,
            coalition_share=coalition,
            cn_cooperation=cn_coop,
            us=us_trajectory,
            cn=cn_trajectory,
            geopolitical_stability=stability,
            arms_race_intensity=arms,
            audit_trail=us_audit + cn_audit,
        )
