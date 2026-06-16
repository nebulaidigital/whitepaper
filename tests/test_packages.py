"""Tests for the policy package registry.

Validates that all seven packages instantiate correctly, have non-empty
specifications (except Status Quo, which is empty by design), and have
consistent metadata.
"""

import pytest

from src.packages import (
    ALL_PACKAGES,
    BUILD_DIFFERENT,
    CERN_AI,
    COMPUTE_CENTRIC,
    DIRECT_REDISTRIBUTION,
    GAME_THEORETIC,
    KORINEK_SCENARIO,
    NEBULAI_SIX,
    NEBULAI_SIX_SEQUENTIAL,
    PACKAGES_BY_CODE,
    STATUS_QUO,
    PolicyPackage,
    Reversibility,
    get_package,
    list_packages,
)


def test_all_packages_present():
    """Nine packages: A-H plus R (Recommended, v0.3 addition for validation)."""
    assert len(ALL_PACKAGES) == 9
    codes = {pkg.code for pkg in ALL_PACKAGES}
    assert codes == {"A", "B", "C", "D", "E", "F", "G", "H", "R"}


def test_packages_by_code_lookup():
    assert get_package("A") is STATUS_QUO
    assert get_package("B") is NEBULAI_SIX
    assert get_package("C") is CERN_AI
    assert get_package("D") is COMPUTE_CENTRIC
    assert get_package("E") is DIRECT_REDISTRIBUTION
    assert get_package("F") is BUILD_DIFFERENT
    assert get_package("G") is GAME_THEORETIC
    assert get_package("H") is KORINEK_SCENARIO


def test_korinek_scenario_has_seven_levers():
    """Package H operationalizes Korinek (2024) four-scenario taxonomy
    with seven scenario-adaptive levers."""
    assert len(KORINEK_SCENARIO.levers) == 7
    assert KORINEK_SCENARIO.sequencing == "sequential"
    # Every lever should reference 'Korinek-conditional' in the name
    for lever in KORINEK_SCENARIO.levers:
        assert "Korinek" in lever.name or "Scenario-Adaptive" in lever.name


def test_invalid_code_raises():
    with pytest.raises(KeyError):
        get_package("Z")


def test_status_quo_has_no_levers():
    """Status quo is the explicit no-policy-change anchor."""
    assert len(STATUS_QUO.levers) == 0


def test_other_packages_have_levers():
    for pkg in ALL_PACKAGES:
        if pkg.code == "A":
            continue
        assert len(pkg.levers) > 0, f"Package {pkg.code} has no levers"


def test_nebulai_six_has_six_pillars():
    """Pillars 1, 2, 3, 4, 5, 6 — six total even though 2 and 3 are stubbed."""
    assert len(NEBULAI_SIX.levers) == 6


def test_nebulai_six_sequential_variant_exists():
    assert NEBULAI_SIX_SEQUENTIAL.sequencing == "sequential"
    assert NEBULAI_SIX.sequencing == "simultaneous"
    # Same lever set, different sequencing
    assert NEBULAI_SIX_SEQUENTIAL.levers == NEBULAI_SIX.levers


def test_lever_target_consistency():
    """Every lever's parameter_changes keys should be reasonable identifiers."""
    for pkg in ALL_PACKAGES:
        for lever in pkg.levers:
            for param_name in lever.parameter_changes:
                assert isinstance(param_name, str)
                assert len(param_name) > 0
                assert " " not in param_name, (
                    f"Param {param_name!r} in {lever.name} has spaces"
                )


def test_irreversible_levers_flagged():
    """Pillar 5 (open weights) in Nebulai Six is irreversible — released
    weights cannot be retracted."""
    irreversible_in_b = NEBULAI_SIX.irreversible_levers()
    assert any("Open" in lev.name or "open" in lev.name for lev in irreversible_in_b), (
        "Expected Pillar 5 (open weights) to be flagged irreversible"
    )


def test_coordination_dependent_levers_have_thresholds():
    """Any lever marked requires_coordination must have coalition_threshold > 0."""
    for pkg in ALL_PACKAGES:
        for lever in pkg.coordination_dependent_levers():
            assert lever.coalition_threshold > 0, (
                f"{lever.name} in package {pkg.code} requires coordination "
                f"but has zero coalition threshold"
            )


def test_package_codes_unique():
    codes = [pkg.code for pkg in ALL_PACKAGES]
    assert len(codes) == len(set(codes))


def test_list_packages_renders():
    rendered = list_packages()
    assert "Status Quo" in rendered
    assert "Nebulai" in rendered
    assert "CERN" in rendered
    assert "Game-Theoretic" in rendered


def test_package_dataclass_immutable():
    """PolicyPackage is frozen — should not allow mutation."""
    with pytest.raises((AttributeError, TypeError)):
        STATUS_QUO.code = "X"  # type: ignore


def test_reversibility_enum_complete():
    """Every lever's reversibility is one of the three valid enum values."""
    valid = {Reversibility.REVERSIBLE, Reversibility.SEMI_REVERSIBLE, Reversibility.IRREVERSIBLE}
    for pkg in ALL_PACKAGES:
        for lever in pkg.levers:
            assert lever.reversibility in valid


def test_game_theoretic_replaces_pillar_1_with_ubc():
    """Per the package's design intent — UBC instead of sovereign equity."""
    has_ubc = any("Universal Basic Capital" in lev.name for lev in GAME_THEORETIC.levers)
    has_sovereign_equity = any(
        "Sovereign Equity" in lev.name for lev in GAME_THEORETIC.levers
    )
    assert has_ubc and not has_sovereign_equity


def test_game_theoretic_replaces_pillar_5_with_compute_governance():
    """Per design — compute governance + CERN-AI instead of open-weights mandate."""
    has_compute_gov = any("Compute Governance" in lev.name for lev in GAME_THEORETIC.levers)
    has_open_mandate = any(
        "Pillar 5: Open-weights mandate" in lev.name for lev in GAME_THEORETIC.levers
    )
    assert has_compute_gov and not has_open_mandate
