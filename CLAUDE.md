# CLAUDE.md — Project Specification

> **Read this file completely before doing anything else. It contains the project's purpose, architecture, working agreements, and known pitfalls. Most of the failure modes encountered in this project have been documented here. Re-read the relevant section before starting any new task.**
>
> **2026-05-01 ADDENDUM — APPROACH REVISION.** After strategic review, the
> project pivoted from a bespoke 14-session heterogeneous-agent build to a
> multi-model + RDM + comparative-package design. The original spec below
> remains valid as background and as the source of validated prototype
> modules. The active project is now governed by:
>
> - `PREREGISTRATION.md` — pre-registered hypothesis list and test design
>   (locks in methodology before any simulation runs)
> - `BASELINE_2026.md` — refreshed Q1 2026 status-quo baseline (replaces the
>   abstract "Patchwork" baseline assumed in this spec)
> - `src/packages/` — seven candidate policy packages compared in the
>   simulation (Status Quo, Nebulai Six, CERN-AI, Compute-Centric, Direct
>   Redistribution, Build-Different-AI, Game-Theoretic-Derived)
> - `src/stability/` — game-theoretic robustness tests (defection,
>   coalition, time-consistency, cross-class)
>
> The pivot is justified by three observations: (1) the prototype's
> calibration failures (GDP overshoots, top-1% wealth share moves wrong
> direction) suggest building from scratch is wrong methodology, not just
> wrong parameters; (2) treating the framework as the subject of analysis
> is methodologically weaker than treating it as one candidate among
> several; (3) accuracy for policy decisions is best served by counterfactual
> deltas against a refreshed baseline, not absolute predictions from a
> bespoke model. Read the four artifacts above before extending the
> codebase. Sections of the original spec below are retained but should
> be read with the revised framing in mind.

## What this project is

This repository builds a **peer-review-quality macroeconomic simulation** to support a Nebulai Corp white paper titled *"The Participatory AI Economy: A Framework for Accelerated AI Development, Broadly Owned."* The white paper proposes a six-pillar policy architecture for managing the AI economic transition, and the simulation provides empirical justification.

The simulation must be:

- **Methodologically defensible** to peer reviewers at NBER, IMF working paper, or *Foreign Affairs* / *Project Syndicate* policy outlets
- **Backtested** against US 2015–2025 observed data (labor share, top 1% wealth share, mean markup, GDP growth)
- **Calibrated** from documented academic literature, not stipulated parameters
- **Reproducible** — every figure in the paper traceable to specific code and data files
- **Honest about uncertainty** — Monte Carlo over literature-anchored parameter ranges with reported P10/P90 bands
- **Honest about limitations** — what the model captures and what it does not, in a methodology section that pre-empts critique

This is **not** a thought-leadership consulting deck. This is a serious research artifact that, after publication of the white paper, should be releasable as a technical companion paper that a macro economist would engage with critically rather than dismiss.

## Background context

The project began as a chat-based collaboration that produced (a) a complete white paper draft, (b) four iteratively-improved simulation prototypes, and (c) a thorough peer-review critique that identified specific methodological problems. The chat session was the wrong tool for the simulation work; this repository is the right one.

The full chat history and the paper draft are not committed to the repo, but their substance is captured in:
- `paper/draft/` — the existing white paper draft, sectioned for revision
- `prototype/` — the four prototype Python modules from the chat session
- `paper/sections/peer_review_critique.md` — the methodological critique
- This file — the consolidated working agreement

## Architecture

```
nebulai-ai-economy/
├── CLAUDE.md                    # This file
├── README.md                    # Public-facing project overview
├── ROADMAP.md                   # Multi-session work plan
├── pyproject.toml               # Python project config (uv or poetry)
├── .gitignore
│
├── data/
│   ├── raw/                     # Downloaded data, immutable
│   │   ├── bls_labor_share.csv
│   │   ├── scf_wealth_distribution.csv
│   │   ├── dleu_markup_series.csv
│   │   ├── oecd_country_indicators.csv
│   │   ├── piketty_wid_top1.csv
│   │   └── README.md            # provenance, URL, download date for each
│   └── processed/               # Cleaned, model-ready data
│
├── src/
│   ├── production/              # Acemoglu-Restrepo task-based core
│   │   ├── __init__.py
│   │   └── task_based.py
│   ├── firms/                   # Heterogeneous markups (DLEU 2020)
│   │   └── markup_distribution.py
│   ├── labor/                   # Monopsony (Azar et al. 2022)
│   │   └── monopsony.py
│   ├── capital/                 # Investment, flight, depreciation, Piketty r>g
│   │   └── capital_markets.py
│   ├── households/              # SCF-calibrated heterogeneous agents
│   │   └── household_economy.py
│   ├── countries/               # US/EU/CN/IN/BR disaggregation
│   │   └── country_module.py
│   ├── geopolitics/             # Coalition formation, conflict probability
│   │   └── stability_index.py
│   ├── scenarios/               # Each scenario as a typed config
│   │   ├── base.py              # Scenario dataclass
│   │   ├── patchwork.py
│   │   ├── sf_consensus.py
│   │   ├── participatory_universal.py
│   │   ├── participatory_capflight.py
│   │   ├── participatory_frontier_only.py
│   │   ├── coerced_redistribution.py
│   │   └── historical_backtest.py
│   ├── core/                    # Integrated dynamic model
│   │   └── simulator.py
│   └── analysis/                # Aggregation, metrics, charting
│       ├── inequality_metrics.py
│       ├── monte_carlo.py
│       └── chart_builders.py
│
├── tests/                       # pytest test suite
│   ├── test_production.py       # Sanity tests for task-based production
│   ├── test_firms.py
│   ├── test_labor.py
│   ├── test_capital.py
│   ├── test_calibration.py      # Backtest against 2015-2025
│   └── test_scenarios.py
│
├── calibration/
│   ├── grid_searches/           # Output of automated calibration runs
│   ├── sensitivity/             # One-at-a-time and Sobol sensitivity
│   └── README.md                # How calibration was done, what targets
│
├── notebooks/                   # Exploratory analysis (Jupyter)
│   ├── 01_data_exploration.ipynb
│   ├── 02_baseline_calibration.ipynb
│   ├── 03_scenario_comparison.ipynb
│   └── 04_sensitivity_analysis.ipynb
│
├── paper/
│   ├── draft/                   # Existing white paper draft
│   │   └── participatory_ai_economy_v1.md
│   ├── sections/
│   │   ├── 00_executive_summary.md
│   │   ├── 01_status_quo_diagnostic.md
│   │   ├── 02_organic_convergence.md
│   │   ├── 03_architecture.md
│   │   ├── 04_compounding.md
│   │   ├── 05_implementation_by_tier.md
│   │   ├── 06_capitalist_case.md
│   │   ├── 07_global_order.md
│   │   ├── 08_adoption_equilibrium.md
│   │   ├── 09_methodology.md
│   │   ├── 10_limitations.md
│   │   ├── 11_phased_pathway.md
│   │   ├── 12_conclusion.md
│   │   └── peer_review_critique.md
│   └── figures/                 # Final paper-ready charts
│
└── prototype/                   # Original chat-session prototypes (reference only)
    ├── s1_production.py         # Task-based production — works, port to src/production
    ├── s2_firms_labor.py        # Firms+monopsony — works, port to src/firms and src/labor
    ├── s2_calibrate.py          # Grid search — port to calibration/
    ├── s3_capital_markets.py    # Capital markets — partial, needs Piketty additions
    └── s4_integrated.py         # Integrated dynamic — has known calibration failures
```

## Project status as of handoff

### What works (validated)

- **Task-based production module** (`prototype/s1_production.py`)
  - Reproduces all three Acemoglu-Restrepo theoretical predictions:
    - Displacement effect (rising automation threshold I lowers labor share)
    - Reinstatement effect (new tasks N raise labor share)
    - Capital-augmenting productivity effect (with σ > 1)
  - Cobb-Douglas limit (σ ≈ 1) handled correctly
  - Passes all sanity tests
  - **This module is production-ready. Port to `src/production/task_based.py` with minor refactoring.**

- **Heterogeneous firm markup distribution** (`prototype/s2_firms_labor.py`)
  - Calibrated to DLEU 2020: sales-weighted mean markup ~1.22, profit share ~17%
  - Pareto-lognormal mixture with 60% positive correlation between firm size and markup
  - Top firm markup ~2.1 (matches DLEU 99th percentile)
  - **Production-ready. Port to `src/firms/markup_distribution.py`.**

- **Monopsony labor markets** (`prototype/s2_firms_labor.py`)
  - Wage = (ε / (1+ε)) × MRPL formulation, Azar-Marinescu-Steinbaum 2022 specification
  - Calibrated ε ≈ 9 in baseline (modest monopsony, ~10% markdown)
  - Skill-differential monopsony (complement workers face less)
  - **Production-ready. Port to `src/labor/monopsony.py`.**

- **Calibration grid search to US 2025 baseline** (`prototype/s2_calibrate.py`)
  - Found I=0.26, σ=1.0, ε=9.0 yielding labor share 56.0%, profit share 17.1%
  - Matches BLS labor share and DLEU profit share within 1pp
  - **Production-ready, port to `calibration/baseline_calibration.py`.**

### What is partial (needs work)

- **Capital markets module** (`prototype/s3_capital_markets.py`)
  - Has cost-of-equity, capital flight, depreciation parameters all calibrated correctly
  - **MISSING:** Piketty-style r > g feedback for wealth concentration dynamics
  - **MISSING:** Inheritance / wealth transfer mechanism
  - **MISSING:** Asset price (Tobin's q) dynamics
  - These three additions are necessary to reproduce observed wealth concentration trajectory.

- **Integrated dynamic model** (`prototype/s4_integrated.py`)
  - Reproduces labor share trajectory within 2pp of observed (54% vs 56% target)
  - Reproduces mean markup trajectory within 0.05 (1.26 vs 1.22 target)
  - **FAILS:** GDP trajectory wildly overshoots (2.3× growth in 11 years vs observed 0.22×). See "Known calibration failures" below.
  - **FAILS:** Top 1% wealth share moves in wrong direction (falls instead of rising). See "Known calibration failures" below.

### What is not built

- Country disaggregation (US, EU, CN, IN, BR as separate modules with cross-flows)
- Geopolitical stability layer (coalition formation, conflict probability)
- Demographic structure / lifecycle households
- Financial sector / monetary side
- Adversarial coordination game (who joins Participatory, when)
- Real data ingestion pipelines (BLS, SCF, DLEU, OECD)
- Test suite
- Sensitivity analysis framework
- Paper figure generation pipeline

## Known calibration failures (from prototype iteration)

These are documented honestly so they are not repeated.

### Failure 1: GDP trajectory overshoots

**Symptom:** Backtest of 2015–2025 produces ~2.3× cumulative GDP growth, observed is ~0.22×.

**Diagnosis:** Capital deepening is unconstrained. With high savings rates from top decile + low traditional capital depreciation (5%/yr) + AI productivity growth, K accumulates without bound. There's no balanced-growth-path constraint, no labor-force scaling, no diminishing-returns-to-investment mechanism kicking in.

**Likely fix:** One or more of:
- Tighter labor force scaling (population growth + participation rate trends)
- Investment adjustment costs (Caballero-Engel style, partial implementation in `s3_capital_markets.py`)
- Add Tobin's q as a brake — investment falls when q < 1
- Endogenize the depreciation rate of AI capital (it should rise as AI capital share rises)
- Possibly also: don't let σ stay at 1.0 forever — at high K/L, even slight σ > 1 with capital-augmenting productivity matters

**Validation target:** US 2015–2025 cumulative real GDP growth ≈ 22% (BEA).

### Failure 2: Top 1% wealth share moves wrong direction

**Symptom:** Top 1% share falls from 30% to ~11% over 2015–2025 in backtest, observed is 28% → 30%.

**Diagnosis:** With σ=1 (Cobb-Douglas), capital deepening lowers r (diminishing returns), so capital income falls relative to labor income. Combined with AI capital depreciation (~22%/yr) hitting top decile harder than savings replenish, the top decile loses wealth share. **The actual mechanism behind observed wealth concentration is not in the model:**

- Piketty's r > g — top decile earns r on existing wealth, accumulates faster than g
- Inheritance flows preserve concentration across generations
- Asset price appreciation (especially equities owned by top decile)
- Differential returns by wealth tier (top decile gets higher r than bottom — empirically documented but not modeled)

**Likely fix:** Add Piketty-style differential returns (top decile r systematically higher than bottom by ~200bps, calibrated to Saez-Zucman 2016) plus inheritance accumulation. This is the central additional ingredient needed.

**Validation target:** US 2015–2025 top 1% wealth share rises from ~28% to ~30% (Saez-Zucman / SCF).

### Failure 3: Need σ > 1 in some scenarios

The Acemoglu-Restrepo and Humlum (2019) literature suggests σ ≈ 1.5 is more appropriate for AI capital specifically. Cobb-Douglas (σ=1) was chosen in the prototype for tractability and because it hit the labor share target — but this is at odds with the literature. **Re-investigate whether a two-sector model (one with σ=1.5 for AI-relevant tasks, one with σ closer to 1 for everything else) is needed.**

## Working agreements

### Code style
- Python 3.11+; type hints everywhere
- Use `dataclasses` for state and configuration
- Follow PEP 8; format with `ruff format`
- Lint with `ruff check`
- One module per file, one class per module where possible
- Public API in `__init__.py` for each subpackage

### Calibration discipline
**Every parameter must have a literature citation in a code comment.** No "I picked this number because it felt right." If a parameter is genuinely chosen for tractability rather than from the literature, mark it explicitly:

```python
sigma_KL: float = 1.5  # Acemoglu-Restrepo 2022 Table 3, mean estimate
markup_growth: float = 0.005  # DLEU 2020, average annual increase 1980-2016
investment_friction_cost: float = 0.10  # CHOSEN FOR TRACTABILITY — sensitivity test required
```

### Testing discipline
- Every module has a test file in `tests/`
- New mechanism = new test before committing
- Backtest test (`tests/test_calibration.py`) must pass before any results are reported
- Run `pytest` before every commit

### Calibration discipline
- Calibration runs go in `calibration/grid_searches/`, output as JSON with timestamp
- The "official" calibrated parameters live in `src/scenarios/base.py`
- Changes to baseline calibration require updating the backtest validation

### Data discipline
- All raw data goes in `data/raw/` with `data/raw/README.md` documenting:
  - Source URL
  - Download date
  - Citation
  - Description
  - Any preprocessing applied
- Processed data is reproducible from raw via scripts in `src/analysis/data_pipelines/`
- **Never modify files in `data/raw/` after initial download.**

### Scenario discipline
- Each scenario is a `Scenario` dataclass instance (see `src/scenarios/base.py`)
- Scenarios are not parameterized arbitrarily — every parameter difference between scenarios must have a documented mechanism mapping back to one or more pillars of the framework
- Adding a new scenario requires: scenario file in `src/scenarios/`, results notebook in `notebooks/`, and entry in the scenario table in `paper/sections/09_methodology.md`

### Honest reporting discipline
- All published numbers come with confidence intervals from Monte Carlo (P10/P90 minimum)
- Results that fail backtest validation are not published
- The paper's `10_limitations.md` section explicitly lists what the model does not capture
- If a result is sensitive to a parameter not pinned down by the literature, that's reported

## Workflow for a typical session

1. **Start every session by `git pull` and reading the most recent commit messages.** The roadmap evolves.
2. **Run the test suite first.** `pytest tests/`. If anything fails, fix that before building new things.
3. **Pick one task from `ROADMAP.md`.** Don't expand scope.
4. **Write the test before the code where possible.** The integrated dynamic model especially needs careful incremental validation.
5. **Commit early, commit often.** Small commits with clear messages.
6. **End every session by updating `ROADMAP.md`** with what was done and what's next.

## Likely points of failure to watch for

These are not abstract concerns — they actually happened during the prototype phase.

- **Calibration drift across modules.** Module A uses one σ, module B uses another. Always pull from a single source of truth in `src/scenarios/base.py`.
- **Per-household loops blowing up runtime.** With N=10,000 households and T=11 years and 200 Monte Carlo draws, naive nested loops are 22M iterations. Use vectorized numpy operations always.
- **Feedback loops creating runaway dynamics.** The GDP overshoot was caused by uncontrolled K accumulation feedback. When adding new feedback, always test it bounded — what's the steady-state value? If there isn't one, you have a problem.
- **Confusing labor share factor (from production) with labor share realized (after markups + monopsony).** Use the realized share for empirical validation; the factor share is a model intermediate.
- **Confusing markup *level* (~1.22) with markup *change* (~+0.005/yr).** I had a calibration bug here in the prototype phase — the test catches it.
- **Forgetting that wealth and income are different things.** The wealth concentration story requires asset price / inheritance ingredients that don't show up in flow income models.

## What the white paper requires from this simulation

The simulation must produce, with peer-review-defensible methodology:

1. **A status-quo diagnostic** — three or four current-trajectory scenarios (Slow Diffusion, Goldman Base, SF Consensus, Patchwork) showing the empty upper-right quadrant: no current-architecture scenario produces both growth and broad-based welfare improvement.

2. **A Participatory baseline** — the framework with all six pillars active, showing positive marginal welfare for the median household in every income decile while preserving GDP growth within ~2pp of laissez-faire.

3. **Robustness tests** — Participatory + capital flight; Participatory + frontier-only adoption; Participatory + AGI-acceleration. Showing the framework's results survive these stress tests within reasonable parameter bounds.

4. **A coerced-redistribution counterfactual** — the post-crisis 2032 scenario where political backlash imposes 70% windfall tax and capability caps. Used as the "or else" in the adoption argument.

5. **Sensitivity decomposition** — which pillars contribute how much to which outcomes. Specifically: Pillar 1 (sovereign equity) for top-1% concentration; Pillar 4 (reskilling) for substitute-worker wages; Pillar 5 (open-weights) for markup growth; Pillar 6 (AI tax) for funding.

6. **Country-tier results** — Frontier (US/EU/CN), Emerging (BR/IN/ID), Developing (SSA aggregate) showing the framework benefits the median voter in every tier (the adoption equilibrium argument).

7. **A geopolitical stability dimension** — the connection between AI architecture and great-power conflict probability. This is the weakest empirical leg; treat as illustrative rather than predictive, but build it.

## What the simulation should NOT try to do

- **Don't try to forecast.** This is a comparative-statics exercise across architectural alternatives, not a prediction of 2036.
- **Don't claim cardinal precision.** Report ordinal results (A > B on metric X) with confidence; do not over-interpret point estimates.
- **Don't model AGI emergence.** The SF Consensus scenario assumes capability scaling continues; it does not model recursive self-improvement or alignment failure. These belong in a different paper.
- **Don't model financial crises.** The framework is about distribution, not stability of the financial system. A real macro model would, but it's out of scope here.

## Research collaborators to engage at appropriate stages

After the simulation reaches v1.0, the methodology section will be substantially strengthened by review from one or more of:

- **Anton Korinek** (UVA, Brookings) — most directly aligned researcher; engages with policy proposals; has written the foundational papers on AI inequality
- **Daron Acemoglu / Pascual Restrepo** — the task-based framework's authors
- **Joseph Stiglitz** — would be a flagship endorsement if achieved
- **The Convergence Analysis team** — wrote the Sovereign Wealth Funds for Transformative AI paper; closest aligned methodology
- **Collective Intelligence Project** — pre-distribution framing originated with them

Reaching out at the *draft methodology* stage rather than the *finished paper* stage is more likely to produce engagement.

## How to use the prototype modules

The four files in `prototype/` are the head start. Treat them as reference implementations to port and refactor, not finished products.

- `s1_production.py` → port directly to `src/production/task_based.py`, add type hints, write proper tests
- `s2_firms_labor.py` → split into `src/firms/markup_distribution.py` and `src/labor/monopsony.py`
- `s2_calibrate.py` → reorganize into `calibration/baseline_calibration.py` with proper output logging
- `s3_capital_markets.py` → port to `src/capital/capital_markets.py`, **and add the missing Piketty + inheritance + Tobin's q ingredients**
- `s4_integrated.py` → use as reference for the `src/core/simulator.py` design, but **rebuild from scratch** with the calibration fixes documented above

## Final note

The prototype phase identified that the labor-share dynamics work well; the wealth-concentration dynamics need additional ingredients; and country-disaggregation, geopolitical layer, and sensitivity framework all need to be built. Fix these in roughly that order. Each should take 1–2 sessions of 2–4 hours.

Total estimated work to v1.0: 8–15 focused sessions across 2–4 weeks.

The white paper itself is approximately 80% drafted (in `paper/draft/`). After the simulation reaches v0.5 (working backtest, Participatory baseline producing defensible results), revise the paper's empirical sections to reflect actual model output rather than the chat-session simulations.
