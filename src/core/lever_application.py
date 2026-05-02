"""Lever application audit trail.

The reduced-form simulator (src/core/simulator.py) applies lever effects
directly to baseline trajectories via documented effect sizes — see
`BilateralSimulator._apply_package_deltas`. This module produces an
audit trail showing which lever was active and what its parameter
changes were, useful for the methodology section's transparency.

Note: in the original structural-build plan, this module mapped lever
keys to simulator config attributes via LEVER_KEY_MAPPING. With the
reduced-form approach, that mapping is implicit in the simulator's
internal _apply_package_deltas function (one canonical place for
effect-size logic). This module is retained for audit purposes only.
"""

from __future__ import annotations

from copy import deepcopy

from src.core.simulator import SimulatorConfig
from src.packages.base import PolicyLever, PolicyPackage


# =============================================================================
# Lever key → simulator parameter mapping
# =============================================================================
#
# Each entry: lever_key -> (config_attribute, operation)
#   operation:
#     'set'      → config.attr = value
#     'add'      → config.attr += value
#     'mul'      → config.attr *= value
#     'dampen'   → config.markup_growth_rate *= (1 - value); used for
#                  open-weights / antitrust dampening of markup growth
#
# Lever keys NOT in this table that ARE valid SimulatorConfig attributes
# are applied directly via setattr. Other keys are silently retained as
# state-only annotations (consumed by stress tests, not by the simulator).
#
LEVER_KEY_MAPPING: dict[str, tuple[str, str]] = {
    # Markup-related — most levers want to dampen markup growth
    "ai_markup_growth_dampening": ("markup_dampening_open_weights", "set"),
    "markup_growth_rate": ("markup_growth_rate", "set"),
    # Reskilling / monopsony
    "epsilon_sub_shift": ("epsilon_sub", "mul"),
    "skill_mix_complement_shift": ("skill_mix_comp", "add"),
    "skill_mix_substitute_shift": ("skill_mix_sub", "add"),
    # Production
    "labor_augmenting_productivity_growth": ("base_productivity_growth_L", "add"),
    "automation_threshold_growth_dampening": ("automation_rate_dI", "mul"),
    # Cross-border / capital flight
    "capital_flight_responsiveness": ("capital_flight_elasticity_per_pp", "add"),
    # Coalition / cooperation parameters
    # (Note: these route through cn_cooperation_propensity at run time)
}


# Lever keys that are state-only — recorded but don't modify simulator config
# directly. Stress tests (e.g., DefectionTest) read these from the package
# specification; the simulator records them but doesn't apply them as numeric
# overrides.
STATE_ONLY_LEVER_KEYS: frozenset[str] = frozenset(
    {
        "sovereign_acquisition_fraction",
        "cost_of_equity_premium",  # already in SimulatorConfig as separate attr
        "dividend_rate",
        "transfer_funding_per_gdp",
        "ai_sector_tax_rate",
        "ubc_grant_per_capita",
        "ubi_monthly_per_adult",
        "wealth_tax_marginal_top",
        "wealth_distribution_floor",
        "ai_arms_race_intensity",
        "geopolitical_stability_index",
        "frontier_capability_diffusion",
        "frontier_compute_concentration",
        "compute_layer_profit_share_cap",
        "ai_lab_concentration",
        "ai_sector_concentration_shift",
        "compute_access_premium_for_independents",
        "public_compute_per_gdp",
        "ai_lab_entry_barrier",
        "compute_tax_per_pflop_day",
        "deployment_risk_pricing",
        "ai_misuse_externality_internalization",
        "capability_disclosure_compliance",
        "ai_safety_audit_coverage",
        "displacement_speed_dampening",
        "labor_supply_elasticity",
        "monopsony_outside_option_strength",
        "inheritance_top_decile_recirculation",
        "care_sector_employment_share",
        "median_wage_floor",
        "ai_market_share_complement_systems",
        "ai_dev_resource_allocation_complement",
        "public_rd_per_gdp",
        "safety_audit_capacity",
        "misuse_proliferation_risk",
        "public_funding_per_gdp",
    }
)


# =============================================================================
# Application functions
# =============================================================================


class LeverApplication:
    """Result of applying a package to a SimulatorConfig.

    Records both the modified config and the per-lever audit trail —
    which lever modified which parameter to what value, for reporting
    and for stress tests.
    """

    def __init__(self, config: SimulatorConfig) -> None:
        self.config: SimulatorConfig = config
        self.audit_trail: list[tuple[str, str, str, float]] = []
        # Each entry: (lever_name, param_key, operation, value)


def parameter_overrides_from_levers(
    package: PolicyPackage,
    coalition_share: float | None = None,
) -> dict[str, float]:
    """Return a flat dict of {config_attr: value} from all levers in package.

    Levers that require coordination only apply if `coalition_share` exceeds
    their `coalition_threshold`. If coalition_share is None, all levers
    are applied (full-coordination assumption).
    """
    overrides: dict[str, float] = {}
    for lever in package.levers:
        # Coalition gating
        if lever.requires_coordination and coalition_share is not None:
            if coalition_share < lever.coalition_threshold:
                continue
        # Apply the lever's parameter_changes
        for key, value in lever.parameter_changes.items():
            if key in STATE_ONLY_LEVER_KEYS:
                continue
            if key in LEVER_KEY_MAPPING:
                attr, op = LEVER_KEY_MAPPING[key]
                if op == "set":
                    overrides[attr] = value
                elif op == "add":
                    overrides[attr] = overrides.get(attr, 0.0) + value
                elif op == "mul":
                    # We need the base value to multiply against; use a sentinel
                    # and resolve in apply_package_to_state where config exists
                    overrides[f"__mul__{attr}"] = (
                        overrides.get(f"__mul__{attr}", 1.0) * value
                    )
                elif op == "dampen":
                    overrides["markup_dampening_open_weights"] = max(
                        overrides.get("markup_dampening_open_weights", 0.0), value
                    )
            elif hasattr(SimulatorConfig, key):
                # Direct attribute override
                overrides[key] = value
            # else: silently ignored — log if needed
    return overrides


def apply_package_to_state(
    package: PolicyPackage,
    config: SimulatorConfig | None = None,
    coalition_share: float | None = None,
) -> LeverApplication:
    """Build a SimulatorConfig with the package's levers applied.

    Returns a LeverApplication wrapping the modified config plus an audit
    trail. Use the audit trail in the methodology section to show exactly
    which lever changed which parameter.
    """
    base = deepcopy(config) if config is not None else SimulatorConfig()
    app = LeverApplication(base)

    for lever in package.levers:
        # Coalition gating
        if lever.requires_coordination and coalition_share is not None:
            if coalition_share < lever.coalition_threshold:
                app.audit_trail.append(
                    (
                        lever.name,
                        "<gated>",
                        "skipped",
                        coalition_share,
                    )
                )
                continue

        for key, value in lever.parameter_changes.items():
            if key in STATE_ONLY_LEVER_KEYS:
                app.audit_trail.append((lever.name, key, "state_only", value))
                continue

            if key in LEVER_KEY_MAPPING:
                attr, op = LEVER_KEY_MAPPING[key]
                # Skip mapping entries for attributes the new reduced-form
                # config doesn't have — those are handled in the simulator's
                # internal _apply_package_deltas instead.
                if not hasattr(app.config, attr):
                    app.audit_trail.append((lever.name, attr, "n/a in reduced-form", value))
                    continue
                if op == "set":
                    setattr(app.config, attr, value)
                elif op == "add":
                    setattr(app.config, attr, getattr(app.config, attr) + value)
                elif op == "mul":
                    setattr(app.config, attr, getattr(app.config, attr) * value)
                elif op == "dampen":
                    if hasattr(app.config, "markup_dampening_open_weights"):
                        new_val = max(app.config.markup_dampening_open_weights, value)
                        app.config.markup_dampening_open_weights = new_val
                app.audit_trail.append((lever.name, attr, op, value))
            elif hasattr(app.config, key):
                setattr(app.config, key, value)
                app.audit_trail.append((lever.name, key, "set", value))
            else:
                app.audit_trail.append((lever.name, key, "n/a in reduced-form", value))

    return app
