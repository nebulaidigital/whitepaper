# Methodology

## Overview

The empirical content of this paper rests on a comparative-policy
simulation that evaluates seven candidate policy packages — the
six-pillar framework proposed here plus six structured alternatives —
against a Q1 2026 status-quo baseline, under deep parameter uncertainty.
The simulation is designed for accuracy on the *comparative* question
("which package dominates under what conditions") rather than absolute
prediction, with every reported number expressed as a delta versus the
status quo. This is the standard methodology used by CBO scoring, IMF
Article IV consultations, and Treasury Office of Macroeconomic Analysis,
all of which report counterfactual deltas rather than absolute forecasts
because common-mode model errors cancel between baseline and policy
branches.

## Theoretical foundations

The simulator integrates four well-established theoretical frameworks:

1. **Task-based production** (Acemoglu & Restrepo 2018, 2019, 2022) for
   the production side and labor-share dynamics, with explicit
   displacement / reinstatement / capital-augmenting-productivity
   mechanics implemented in `src/production/task_based.py` and validated
   against the three core comparative statics from Acemoglu-Restrepo 2022
   Section 3.

2. **Heterogeneous firm markups** (De Loecker, Eeckhout & Unger 2020;
   Eggertsson, Robbins & Wold 2021) for the markup channel of labor
   share decline, with sales-weighted aggregate markup calibrated to
   the DLEU 2020 cross-section (μ̄ = 1.22 in US 2020).

3. **Monopsonistic labor markets** (Azar, Marinescu & Steinbaum 2022;
   Manning 2003) for wage markdown and skill-differential effects.

4. **Wealth dynamics with differential returns** (Piketty 2014;
   Saez & Zucman 2016; Fagereng, Guiso, Malacrino & Pistaferri 2020)
   for the r > g mechanism and inheritance recirculation that produce
   the documented top-1% wealth-share trajectory.

A reduced-form simulator integrates these mechanics with policy-lever
deltas anchored to empirical analogs documented in `EMPIRICAL_ANALOGS.md`.
The choice of reduced-form rather than full structural HANK is documented
in `CLAUDE.md` 2026-05-01 addendum: the structural prototype hit two
calibration failures (GDP overshoot, top-1% share moving the wrong
direction), and the comparative-delta framing is more honest about what
can be known from any model of structurally novel policy regimes (Lucas
critique).

## Pre-registration

The analysis is **pre-registered**. Before any simulation was run, ten
specific hypotheses were specified in `PREREGISTRATION.md` with explicit
validation criteria, parameter distributions, and decision rules. The
pre-registration is dated and version-controlled; amendments after
results are observed are stated explicitly and do not retroactively
modify the original. Every reported finding traces to a pre-registered
hypothesis.

This discipline is non-negotiable for the policy-research class this
paper aims to belong to: results not specified ex-ante can always be
attacked as cherry-picked, and the credibility of the comparative claim
depends on commitment to reporting whatever the data show — including
findings that qualify or refute parts of the framework.

## Baseline construction

The Q1 2026 status-quo baseline (`BASELINE_2026.md`) is constructed in
two parts:

- **Backtest period 2015–2025**: observed values from BLS labor share,
  Distributional Financial Accounts top-1% wealth share, DLEU 2020
  sales-weighted markup, BEA chained-2017-dollar real GDP, and
  Webb 2020 / Eloundou et al. 2023 substitute-worker employment index.
  The simulator reproduces these exactly by construction.

- **Forward projection 2025–2036**: literature-anchored decay/growth
  rates calibrated to BASELINE_2026.md §3 central values. The decay rates
  reflect what the existing literature projects for a "no new framework"
  trajectory given current trends (Acemoglu 2024 NBER WP 32487; Saez-
  Zucman 2016/2019; DLEU 2020 markup trend; BEA / IMF WEO GDP).

Importantly, the Q1 2026 baseline reflects the actual policy landscape
as of paper writing — including the EU AI Act in force, US AI executive
orders, AISI Network testing, BIS export controls, and the **open-weights
inversion** in which Chinese frontier models (DeepSeek R1, Qwen 3) lead
in open-weights release while US frontier labs remain closed. This is
materially different from the abstract "Patchwork" baseline assumed in
the project's original specification, and the difference matters for
Pillar 5 (open-weights mandate) interpretation.

## Comparative packages

Seven policy packages are compared, each implemented as a typed
`PolicyPackage` dataclass in `src/packages/`:

| # | Package | Core mechanism |
|---|---|---|
| A | Status Quo (Patchwork) | Current trajectory baseline |
| B | Nebulai Six-Pillar Framework | Sovereign equity + Pillars 2-6 |
| C | CERN-AI Centered | Global public lab + compute treaty + tiered openness |
| D | Compute-Centric | Compute tax + access mandates + structural separation |
| E | Direct Redistribution | UBI + UBC + wealth tax + care economy |
| F | Build-Different-AI | Directed labor-augmenting R&D + procurement + codetermination |
| G | Game-Theoretic-Derived | Eight pillars derived from robustness constraints |

Treating the framework as one of seven candidates rather than as the
subject of analysis is a deliberate methodological choice. The
comparative framing produces stronger evidence for whatever
recommendation emerges than would a "validate the framework" framing,
because dominance against alternatives is more informative than absence
of failure against a null. Packages C through G are specified to test
plausible alternative architectures the existing literature would
propose; their specifications draw on the GovAI / Korinek / Acemoglu /
Mazzucato / Khan-Wu-Hovenkamp literatures documented in `SOURCES.md`.

## Lever effect sizes

Every policy lever's effect size is anchored to a documented empirical
analog in `EMPIRICAL_ANALOGS.md`. For example, Pillar 1 (sovereign equity)
effect sizes derive from the Norway GPFG 30-year track record and Alaska
Permanent Fund analog; Pillar 4 (reskilling) derives from the
Card-Kluve-Weber (2018) meta-analysis of 207 active-labor-market-program
evaluations; CERN-AI parameters scale from CERN's actual budget per
member; antitrust structural separation from the AT&T 1982 breakup
pricing dynamics.

The empirical-analog approach is essential for the project's accuracy
goal because none of the AI-specific policy levers — sovereign-AI-equity
acquisition, open-weights mandate, compute governance treaty — have
historical precedents at the proposed scale. Anchoring to the closest
real-world analog gives a documented effect-size prior with explicit
uncertainty; stipulating effect sizes from scratch would not. Cross-
cutting caveats about the imperfection of each analog are stated in
`EMPIRICAL_ANALOGS.md` §6.

## Uncertainty quantification

Parameter uncertainty is propagated via Latin Hypercube sampling over
seven uncertainty ranges documented in `PREREGISTRATION.md` §7. These
ranges are literature-anchored: σ (task elasticity) ranges over
Acemoglu-Restrepo 2022 Table 3 reported estimates; capital flight
elasticity ranges over Bach 2014 (high) and Brülhart 2022 (low) wealth-
tax behavioral responses; reskilling earnings effect ranges over the
P10-P90 of the Card-Kluve-Weber meta-analysis; and so on.

For each draw, the same parameter vector is applied across all seven
packages — this is essential for valid policy-regret comparison, since
otherwise packages would be evaluated on different "futures" and
relative ordering would be meaningless. The shared-sample design is
implemented in `src/analysis/rdm.py:_sample_uncertainties` and tested
in `tests/test_rdm.py`.

## Robust Decision Making

Following Lempert, Popper & Bankes (2003) and the EMA Workbench
implementation of Kwakkel & Pruyt (2013), the analysis computes a
policy-regret surface across the joint parameter space. For each
outcome metric and each parameter draw, the package producing the best
outcome is identified, and regret is computed as the difference between
each package's outcome and the best in that draw. The reportable
quantities are:

- **Mean regret** per package per metric — lower is more robust
- **Maximum regret** — worst-case underperformance
- **Fraction of futures won** — under how many parameter draws each
  package is best

This identifies *conditional dominance* rather than mean-best dominance,
which is more informative for policy decisions under genuine deep
uncertainty (Walker, Lempert & Kwakkel 2013).

## Stability stress tests

Four stress-test families test the game-theoretic robustness of each
package (`src/stability/`):

1. **Defection test**: for each coordination-dependent lever, simulate
   the most likely defection (CN for compute governance, tax-haven
   jurisdictions for AI tax, frontier-lab jurisdiction for open
   weights) and measure whether the package's welfare under defection
   beats the status quo. A lever is flagged "fragile" if its package
   becomes net negative under documented-likelihood defection.

2. **Coalition formation test**: vary the coalition share of frontier
   compute from 0.30 to 1.00 and identify the breakeven threshold
   at which the package is welfare-positive. Inconsistency between
   declared `coalition_threshold` and actual breakeven indicates
   over-optimistic specification.

3. **Time-consistency test**: simulate stochastic political reversal,
   with per-year reversal probability weighted by the lever's
   `Reversibility` classification (Reversible: 0.50/yr; Semi-reversible:
   0.20/yr; Irreversible: 0.05/yr because released weights cannot
   meaningfully be retracted). Monte Carlo over reversal realizations
   yields expected welfare under political risk.

4. **Cross-class test**: by-decile welfare deltas across 20 cells
   (10 deciles × 2 countries). Tests the framework's
   adoption-equilibrium claim (Hypothesis 4): under the package, the
   median household in every decile in every country tier should be
   better off vs. status quo.

## Backtest validation gate

No simulation result is reported unless the underlying model passes the
2015–2025 backtest within the tolerances declared in
`PREREGISTRATION.md` §8: ±2pp on US labor share and top-1% wealth share,
±0.05 on mean markup, ±5pp on US cumulative real GDP growth, ±3pp on
CN labor share, ±0.05 on CN markup, ±10pp on CN cumulative real GDP
growth. These tolerances are checked automatically in
`tests/test_backtest.py` before any forward-looking output is treated
as reportable. The model must explain observed data before producing
forward-looking policy recommendations.

## Reproducibility

Every figure in this paper is regenerable from a single command:
`python -m src.analysis.chart_builders`. Every numerical claim traces
to a specific `PolicyLever` parameter value in `src/packages/` and an
empirical analog in `EMPIRICAL_ANALOGS.md`. The full RDM sample for
the policy-regret surface is reproducible from the LHS seed declared
in `PREREGISTRATION.md` (seed 20260501) and is preserved as CSV output
from `scripts/run_rdm.py`. The full code is released under MIT license
at the repository accompanying the paper.

The discipline of pre-registration, empirical-analog anchoring,
shared-sample RDM, and code release together make the analysis
defensible against the methodological critiques that typically defeat
corporate-affiliated policy research. They do not eliminate the
substantive limitations documented in §10.
