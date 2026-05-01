"""Package A: Status Quo (Patchwork).

The Q1 2026 baseline. No new framework adopted. The fragmented-but-active
regulatory mosaic continues: EU AI Act in force, US AI executive orders,
AISI Network testing, BIS export controls, no new sovereign equity, no
multilateral compute treaty, no UBI/UBC.

This is the comparison anchor for all other packages. See BASELINE_2026.md
for the full status-quo trajectory.
"""

from src.packages.base import (
    LeverTarget,
    PolicyLever,
    PolicyPackage,
    Reversibility,
)

# Status quo has no active levers — all parameter values follow baseline
# trajectory. This empty-lever package exists to make the comparison
# explicit and enforces that "no policy change" is itself a typed scenario.
STATUS_QUO = PolicyPackage(
    code="A",
    name="Status Quo (Patchwork)",
    description=(
        "The Q1 2026 baseline trajectory: existing regulations remain in force "
        "(EU AI Act, US AI executive orders, AISI Network, BIS export controls) "
        "but no new framework is adopted. Capital flows, AI development, and "
        "wealth dynamics evolve under current trajectories with no additional "
        "intervention. Per BASELINE_2026.md §3."
    ),
    levers=(),
    activation_year=2026,
    sequencing="simultaneous",
)
