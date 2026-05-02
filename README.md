# Nebulai — Participatory AI Economy Simulation

> Macroeconomic simulation supporting the white paper *"The Participatory AI
> Economy: A Framework for Accelerated AI Development, Broadly Owned"* by
> Nebulai Corp.

This repository compares seven candidate policy packages for managing the
2025–2036 AI economic transition, anchored to a Q1 2026 status-quo baseline.
The simulator produces counterfactual deltas (Δ vs. status quo) for each
package, then uses Robust Decision Making (RDM) scenario discovery to
identify the conditions under which each package's recommendations hold or
fail.

**This is not a forecast.** It is a comparative-policy analysis. The
methodology is described in `PREREGISTRATION.md`; the reasoning behind the
approach is documented in `CLAUDE.md`'s 2026-05-01 addendum.

---

## Quickstart

```bash
# Clone the repo
git clone <your-fork-url> nebulai-ai-economy
cd nebulai-ai-economy

# Install dependencies (Python 3.11+ required)
pip install -e ".[dev]"
# Or with uv:  uv sync

# Run the test suite (~2s, 44 tests)
pytest

# Run the status-quo baseline
python scripts/run_baseline.py

# Compare all 7 policy packages at 2036
python scripts/run_packages.py

# Run RDM scenario discovery (1000 LHS draws × 7 packages = 7000 sims; ~5s)
python scripts/run_rdm.py --scenarios 1000

# Save full RDM results to CSV
python scripts/run_rdm.py --scenarios 5000 --csv results/rdm.csv

# Common operations via Makefile
make test       # pytest
make baseline   # status-quo run
make packages   # all-package comparison
make rdm        # 1000-scenario RDM sweep
make clean      # remove results/
```

---

## What's in this repo

```
nebulai-ai-economy/
├── PREREGISTRATION.md           # Pre-registered hypothesis list (LOCKED)
├── BASELINE_2026.md             # Q1 2026 status-quo baseline reference
├── EMPIRICAL_ANALOGS.md         # Literature delta book per policy lever
├── CLAUDE.md                    # Project specification + 2026 addendum
├── ROADMAP.md                   # 6-phase plan
├── SOURCES.md                   # Literature anchors + 2026-05-01 addendum
├── README.md                    # This file
├── pyproject.toml               # Python project config
├── Makefile                     # Common operations
│
├── src/
│   ├── packages/                # 7 typed PolicyPackage dataclasses
│   │   ├── status_quo.py        # A — Patchwork baseline
│   │   ├── nebulai_six.py       # B — Original framework
│   │   ├── cern_ai.py           # C — Global public lab + compute treaty
│   │   ├── compute_centric.py   # D — Compute tax + access + structural sep
│   │   ├── direct_redistribution.py  # E — UBI + UBC + wealth tax
│   │   ├── build_different.py   # F — Acemoglu directed AI
│   │   ├── game_theoretic.py    # G — 8 pillars from robustness constraints
│   │   ├── base.py              # PolicyPackage / PolicyLever types
│   │   └── registry.py          # Central package lookup
│   ├── stability/               # Game-theoretic stress tests (stubs for Phase 5)
│   ├── production/              # Acemoglu-Restrepo task-based production
│   ├── core/
│   │   ├── simulator.py         # Bilateral US/CN reduced-form simulator
│   │   └── lever_application.py # Lever audit-trail layer
│   └── analysis/
│       ├── baseline_data.py     # Hard-coded BLS/SCF/DLEU/BEA series
│       └── rdm.py               # EMA Workbench RDM wrapper
│
├── scripts/
│   ├── run_baseline.py          # Status-quo trajectory
│   ├── run_packages.py          # 7-package comparison
│   └── run_rdm.py               # RDM scenario discovery
│
├── tests/                       # pytest test suite (44 tests, all passing)
├── prototype/                   # Original chat-session prototype code
├── preregistration/             # Versioned pre-registration documents
├── data/raw/                    # Drop CSVs here to override hard-coded series
├── results/                     # Output directory (gitignored)
├── notebooks/                   # Jupyter notebooks (mostly empty pre-Phase 6)
└── paper/                       # Whitepaper draft + sections
```

---

## Methodology in one screen

1. **Status-quo baseline** (`BASELINE_2026.md`) — Q1 2026 trajectory
   continuation. Backtest period 2015–2025 uses observed values from
   BLS/SCF/DLEU/BEA. Forward projection 2025→2036 uses calibrated rates
   matching the central values from the literature.

2. **Counterfactual deltas, not absolute predictions.** Every reported
   number is a difference between a policy package and the status-quo
   baseline. This is more accurate than absolute prediction — common-mode
   model errors cancel between branches.

3. **Seven candidate policy packages** (`src/packages/`) — the framework
   plus six alternatives. The framework may dominate, may be dominated,
   or may dominate only conditionally. All three outcomes are reportable.

4. **Effect sizes from empirical analogs** (`EMPIRICAL_ANALOGS.md`) —
   each policy lever's effect is anchored to a real-world program where
   similar mechanisms were measured (Norway GPFG, Card-Kluve-Weber 2018,
   AT&T 1982 breakup, etc.).

5. **Robust Decision Making** (`src/analysis/rdm.py`) — Latin Hypercube
   sampling over the literature-anchored uncertainty ranges
   (PREREGISTRATION.md §7). Computes policy-regret surface across all
   packages × all parameter draws, identifying which package wins
   under which conditions.

6. **Pre-registered hypotheses** (`PREREGISTRATION.md`) — 10 specific
   hypotheses with explicit validation/falsification criteria, locked
   before any simulation runs. Reportable findings must trace to a
   pre-registered hypothesis.

---

## Example output

```
$ python scripts/run_packages.py

PACKAGE COMPARISON @ 2036: Δ vs status quo
  coalition_share = 0.7, cn_cooperation = 0.3

code  name                                 us_LS_d_pp  us_T1%_d_pp  us_Mu_d  us_GDP_d%  us_med_d%
A     Status Quo (Patchwork)                   +0.000       +0.000   +0.000     +0.000     +0.000
B     Nebulai Six-Pillar Framework             +0.155       +0.000   -0.023     -0.150     +4.971
C     CERN-AI Centered                         +0.155       -0.250   -0.066     -0.250     +5.023
D     Compute-Centric Package                  +0.000       +0.000   -0.081     +0.000     +0.172
E     Direct Redistribution Package            +0.008       -0.800   +0.000     +0.000     +9.358
F     Build-Different-AI (Acemoglu-Johnson)    +0.184       +0.000   -0.040     +1.500     +1.371
G     Game-Theoretic-Derived Eight Pillars     +0.155       -0.500   -0.141     -0.300     +5.074
```

```
$ python scripts/run_rdm.py --scenarios 1000 --metric us_top_1pct_wealth_2036

POLICY REGRET BY METRIC

  us_top_1pct_wealth_2036  (↓ lower is better)
    E:  mean_regret=+0.0000  fraction_best=100.0%
    G:  mean_regret=+0.0026  fraction_best= 14.0%
    C:  mean_regret=+0.0051  fraction_best=  0.0%
    A:  mean_regret=+0.0076  fraction_best=  0.0%
    ...
```

Read this as: across 1000 plausible futures, Package E (Direct Redistribution)
produces the lowest top-1% wealth concentration in 100% of futures.

---

## Honest limitations (read these)

1. **Reduced-form simulator, not structural HANK.** The prototype's structural
   build hit two calibration failures (GDP overshoot, top-1% wealth share moves
   wrong direction). The reduced-form approach is more honest about what we
   can and can't know. Documented in `CLAUDE.md`'s 2026-05-01 addendum.

2. **No live data fetching.** Baseline series are hard-coded from
   published BLS/SCF/DLEU/BEA tables. To use updated data, drop CSVs
   into `data/raw/` (filenames documented in
   `src/analysis/baseline_data.py`).

3. **Pillars 2 and 3 of the Nebulai framework are placeholder-stubbed.**
   `src/packages/nebulai_six.py` flags this. Their specifications need
   to come from the whitepaper draft parse, deferred.

4. **Effect sizes have wide confidence intervals.** None of the AI-
   specific levers have empirical analogs at the proposed scale. See
   `EMPIRICAL_ANALOGS.md` cross-cutting caveats §1-§5.

5. **Geopolitical stability is illustrative, not predictive.** Per
   `PREREGISTRATION.md` Tier D — the geopolitical layer is reported
   qualitatively in the methodology section.

---

## Status

| Phase | Deliverable | Status |
|---|---|---|
| 0. Foundations | PREREG, BASELINE, packages, sources | ✅ Done |
| 1. Empirical delta book | EMPIRICAL_ANALOGS.md | ✅ Done |
| 2. Multi-model anchor | Acemoglu-Restrepo task-based core | ✅ Done (extended from prototype) |
| 3. Bilateral US-China model | `src/core/simulator.py` | ✅ Done (reduced-form) |
| 4. RDM scenario discovery | `src/analysis/rdm.py` | ✅ Done |
| 5. Synthesis + red team | Reversibility matrix, hostile critique | ⬜ Open |
| 6. Whitepaper integration | Methodology, figures | ⬜ Open |

---

## Contributing / extending

- **New policy package**: add `src/packages/your_package.py` following the
  pattern of `direct_redistribution.py`; register in `registry.py`; add a
  test to `tests/test_packages.py`.
- **New empirical analog for an existing lever**: edit
  `EMPIRICAL_ANALOGS.md`; update effect-size values in the corresponding
  `src/packages/*.py`; verify tests still pass.
- **New simulator capability**: extend `src/core/simulator.py`, add
  tests to `tests/test_simulator.py`, ensure backtest still passes
  (`tests/test_backtest.py` is the canonical gate per PREREGISTRATION
  §8).
- **Refresh data**: drop CSVs into `data/raw/` with the filenames listed
  in `src/analysis/baseline_data.py` `_try_csv` calls. The loader
  preferentially uses files over hard-coded values.

---

## Citation

If using this simulation framework or its results, please cite the
forthcoming white paper:

> Nebulai Corp (2026). *The Participatory AI Economy: A Framework for
> Accelerated AI Development, Broadly Owned.* Miami, FL.

## License

Code: MIT. Paper drafts and substantive content: All rights reserved by
Nebulai Corp pending publication.

## Contact

For research collaboration inquiries: partnerships@nebulai.com
