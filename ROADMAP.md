# ROADMAP

> **2026-05-01 — REVISED.** Original 14-session bespoke build superseded
> by 6-phase multi-model + RDM + comparative-package design. Original plan
> retained below for reference; see §"Revised Phase Plan" first.
>
> Read order before extending: `PREREGISTRATION.md` → `BASELINE_2026.md`
> → `SOURCES.md` (including 2026-05-01 addendum) → `src/packages/` →
> this document.

---

## Revised Phase Plan (2026-05-01 → 2026-Q3)

| Phase | Deliverable | Status | Notes |
|---|---|---|---|
| **0. Foundations** | PREREGISTRATION.md, BASELINE_2026.md, packages, sources, scaffolding | ✅ Complete (2026-05-01) | This commit |
| **1. Empirical delta book** | One-page-per-pillar empirical analog with effect-size CI from real-world data (Norway GPFG, Card-Kluve-Weber, OSS markup erosion, OECD digital tax) | ⬜ Not started | ~1.5 weeks |
| **2. Multi-model anchor** | Acemoglu 2024 (NBER WP 32487) replication code running locally; Tier 1 deterministic runs; sanity check vs. Phase 1 deltas | ⬜ Not started | ~1 week |
| **3. Bilateral US-China model** | Two-country extension of Acemoglu 2024 with PWT 11.0 / WID calibration; Tier 1 + Tier 2 runs (54 deterministic) | ⬜ Not started | ~2 weeks |
| **4. RDM scenario discovery** | EMA Workbench wrapping bilateral model; ~25k draws over jointly-sampled parameters; sign-flip identification | ⬜ Not started | ~1 week |
| **5. Synthesis + red team** | Reversibility / lock-in matrix; leading indicators per pillar; stakeholder/coalition map; commissioned hostile critique; final comparison table | ⬜ Not started | ~1.5 weeks |
| **6. Whitepaper integration** | Updated methodology, empirical, and limitations sections; figures regenerated from model output | ⬜ Not started | ~1 week |

Total estimated calendar time: ~6–8 weeks of focused work.

### Phase 0 deliverables (completed 2026-05-01)

- `PREREGISTRATION.md` v1.0 — 10 pre-registered hypotheses with explicit
  validation/falsification criteria, parameter distributions, and decision
  rules. Locked before any simulation run.
- `BASELINE_2026.md` v1.0 — refreshed Q1 2026 baseline reflecting the
  open-weights inversion, Stargate-scale capital, BIS export controls,
  active regulatory regimes (EU AI Act, AISI Network), and the bilateral
  US-China structural environment. Replaces the abstract "Patchwork" of
  the original handoff.
- `src/packages/` — seven typed `PolicyPackage` dataclasses:
  - A. Status Quo (Patchwork)
  - B. Nebulai Six-Pillar Framework (incl. sequential variant for H2)
  - C. CERN-AI Centered (replaces Pillar 5 with public open-frontier lab)
  - D. Compute-Centric (compute tax + access mandates + structural separation)
  - E. Direct Redistribution (UBI + UBC + wealth tax + care economy)
  - F. Build-Different-AI (Acemoglu-Johnson directed AI)
  - G. Game-Theoretic-Derived (eight pillars from robustness constraints)
- `src/stability/` — four stress test classes (DefectionTest,
  CoalitionTest, TimeConsistencyTest, CrossClassTest) — stubs awaiting
  Phase 3 simulator
- `SOURCES.md` 2026-05-01 addendum — Korinek body of work, GovAI/MAGIC
  proposals, compute governance, open-foundation-model literature, Ostrom,
  RDM methodology, Q1 2026 data sources
- `pyproject.toml` updated with `ema-workbench` and
  `sequence-jacobian` dependencies for Phases 4 and 3 respectively
- `tests/test_packages.py` — 16 unit tests over the package registry
  (all passing)

### Phase 0 kill-criteria (do not proceed to Phase 1 unless)

- ✅ All seven packages instantiate and pass unit tests
- ✅ PREREGISTRATION.md committed and dated; not modified after this point
  except via versioned addenda
- ✅ BASELINE_2026.md committed; status-quo trajectory anchored to specific
  citable sources (not subjective)
- ✅ Pre-registration approvals workflow defined (§11 of PREREGISTRATION.md)

### Decisions still required (escalate to project lead)

1. **Confirm pivot from original 14-session plan.** The revised approach
   reframes the simulation's purpose from "validate the framework" to
   "compare candidate packages and report which dominates under what
   conditions." This is a substantive change that may produce findings
   contrary to Nebulai's preferred narrative.
2. **Budget for paid hostile critique** in Phase 5: ~$5–15K for three
   named scholars (libertarian, China-realist, heterodox).
3. **Academic co-authorship** invitation to Anton Korinek (UVA / Brookings)
   at draft-methodology stage. Earlier engagement substantially raises
   achievable peer-review tier.
4. **Pillars 2 and 3 of the Nebulai framework are placeholder-stubbed**
   in `src/packages/nebulai_six.py` pending whitepaper parse. Need
   project lead to either supply specifications or authorize Claude to
   parse the whitepaper draft.
5. **Coalition design**: Phase 3 builds a *bilateral* US-China model,
   not the handoff's three-tier (Frontier / Emerging / Developing) build.
   Three-tier extension deferred to Phase 7 if needed.

---

## Original 14-session plan (retained for reference)

This is the multi-session work plan for taking the simulation from prototype to publishable v1.0. Estimated 8–15 sessions of 2–4 hours each.

## Status summary

| Component | Status | Sessions remaining |
|---|---|---|
| Project scaffolding (this repo) | ✅ done | 0 |
| Real data ingestion | ⬜ not started | 1 |
| Production module port | 🟡 prototype only | 0.5 |
| Firms module port | 🟡 prototype only | 0.5 |
| Labor module port | 🟡 prototype only | 0.5 |
| Capital markets + Piketty additions | 🟡 partial | 1.5 |
| Households module | 🟡 partial | 1 |
| Integrated simulator (fixed calibration) | 🔴 broken | 2 |
| Test suite | ⬜ not started | 1 |
| Backtest validation passing | 🔴 fails | (depends on simulator fix) |
| Country disaggregation | ⬜ not started | 2 |
| Geopolitical layer | ⬜ not started | 1 |
| Monte Carlo + sensitivity framework | ⬜ not started | 1 |
| Scenario library complete | 🟡 prototype only | 1 |
| Paper figure pipeline | ⬜ not started | 1 |
| Methodology section in paper | ⬜ not started | 1 |
| External methodology review | ⬜ not started | (out of scope here) |

**Total estimate to v1.0: ~14 sessions.**

## Session-by-session plan

### Session 1 — Project setup & data ingestion

Goal: get the development environment running and pull in the actual datasets the model will use.

Tasks:
- Set up `pyproject.toml` with `uv` (or `poetry`)
- Add core dependencies: `numpy`, `pandas`, `scipy`, `matplotlib`, `pytest`, `ruff`
- Initialize git, write `.gitignore`
- Download and document each dataset:
  - **BLS labor share** — quarterly nonfarm business sector labor share, 1990–2025 (`https://www.bls.gov/productivity/`)
  - **SCF wealth distribution** — top 1%, top 10%, bottom 50% wealth shares, 1989–2022 (`https://www.federalreserve.gov/econres/scfindex.htm`)
  - **DLEU markup data** — De Loecker, Eeckhout, Unger 2020 replication package (Zenodo)
  - **Saez-Zucman / WID top wealth shares** — `https://wid.world`
  - **Penn World Tables** — country-level capital stocks, labor shares, output (`https://www.rug.nl/ggdc/productivity/pwt/`)
  - **OECD AI indicators** — country-level AI capacity (`https://oecd.ai`)
- Write `data/raw/README.md` with provenance for each
- Stub out a data pipeline in `src/analysis/data_pipelines/` to load each into pandas DataFrames

Deliverable: `pytest` passes (with empty tests); data loadable with `from src.analysis.data_pipelines import load_bls_labor_share`.

### Session 2 — Port production, firms, labor modules

Goal: clean up the three prototype modules that work and put them under the new architecture.

Tasks:
- Port `prototype/s1_production.py` → `src/production/task_based.py` with type hints, proper `__init__.py` export, and `tests/test_production.py` covering the four sanity tests
- Split `prototype/s2_firms_labor.py` → `src/firms/markup_distribution.py` and `src/labor/monopsony.py`, with tests for each
- Move `prototype/s2_calibrate.py` → `calibration/baseline_2015.py` and `calibration/baseline_2025.py`, with output logged as JSON

Deliverable: `pytest tests/test_production.py tests/test_firms.py tests/test_labor.py` all pass.

### Session 3 — Capital markets module with Piketty additions

Goal: build the capital markets module that the prototype skipped.

Tasks:
- Port `prototype/s3_capital_markets.py` → `src/capital/capital_markets.py` with type hints
- Add **differential returns by wealth tier** (Saez-Zucman 2016): top decile r systematically ~150-250 bps higher than bottom, parameterized
- Add **inheritance flow** mechanism: at each year, fraction of top-decile wealth transfers within top decile (preserving concentration); calibrate to documented bequest data
- Add **Tobin's q dynamics** for AI capital: investment slows when q < 1, accelerates when q > 1
- Implement adjustment-cost model on investment (Caballero-Engel friction)
- Test that, in isolation, these three additions produce a Piketty-style steady-state where top 1% share is bounded above 25%

Deliverable: `tests/test_capital.py` passes including a Piketty-style steady-state test.

### Session 4 — Households module

Goal: clean heterogeneous-household population matched to SCF wealth data.

Tasks:
- Port the prototype's `HouseholdEconomy` to `src/households/household_economy.py`
- **Calibrate to SCF 2022 data**, not stylized facts. Top 1% share = 30.4% (SCF 2022), top 10% = 76%, etc.
- Add lifecycle structure: 3 age groups (young, prime, retired) with different MPCs and labor endowments per age
- Demographics: age groups follow a smoothed US-style distribution
- Skill type by decile + age (Frey-Osborne 2017 calibration)

Deliverable: `tests/test_households.py` validates that the initial population matches SCF 2022 within 1pp on every decile share.

### Session 5 — Integrated simulator, attempt 1

Goal: rebuild the integrated dynamic model with the calibration fixes documented in CLAUDE.md.

Critical: **don't repeat the prototype's mistakes.** The two failures to fix:
1. GDP trajectory overshoots — needs labor-force scaling, investment frictions, and possibly endogenous depreciation
2. Top 1% share moves wrong direction — needs Piketty differential returns + inheritance (built in Session 3)

Tasks:
- Build `src/core/simulator.py` integrating production + firms + labor + capital + households
- Run the historical 2015–2025 backtest
- Iterate on calibration *with the test suite as the validator*
- The backtest must pass (within 2pp on each indicator) before declaring victory

Deliverable: `tests/test_calibration.py::test_2015_2025_backtest` passes. This is the critical milestone.

### Session 6 — Scenario library

Goal: implement all seven scenarios needed for the paper.

Tasks:
- Build `src/scenarios/base.py` with the `Scenario` dataclass
- Implement each scenario as a typed config file:
  - `historical_backtest.py` — already done, formalize
  - `slow_diffusion.py`, `goldman_base.py`, `sf_consensus.py`, `patchwork.py` — current trajectories
  - `participatory_universal.py`, `participatory_capflight.py`, `participatory_frontier_only.py`, `participatory_acceleration.py` — framework variants
  - `coerced_redistribution.py` — counterfactual
- Document the parameter-mechanism mapping for each scenario in scenario file docstring
- Add CLI entry: `python -m src.core.simulator --scenario sf_consensus --years 11 --start-year 2025`

Deliverable: All scenarios run without errors; results saved to `calibration/scenario_runs/`.

### Session 7 — Monte Carlo and sensitivity framework

Goal: parameter uncertainty done properly.

Tasks:
- Build `src/analysis/monte_carlo.py` that runs N draws of any scenario from documented parameter distributions
- Each parameter's distribution is anchored to its literature source — e.g., `sigma_KL ~ Normal(1.5, 0.15) clipped [1.1, 2.0]` because Acemoglu-Restrepo 2022 Table 3 reports range
- Build `src/analysis/sensitivity.py` for one-at-a-time and Sobol-style sensitivity decomposition
- Standard output: P10 / P50 / P90 trajectories for every reported metric

Deliverable: `python -m src.analysis.monte_carlo --scenario participatory_universal --draws 500` produces uncertainty bands for all key indicators.

### Session 8 — Country disaggregation

Goal: the three-tier (Frontier / Emerging / Developing) structure with proper country-level state.

Tasks:
- Build `src/countries/country_module.py` representing one country with its own production, wealth distribution, labor force, and policy state
- Frontier tier: US, EU, China, UK, Japan, South Korea (six countries with shared parameters where data permits)
- Emerging tier: India, Brazil, Indonesia, Mexico, South Africa, Turkey
- Developing: aggregate, with regional substructure
- Cross-flows: AI services trade (calibrated to actual hyperscaler revenue from non-Frontier customers), capital flows, technology diffusion
- Country-level state-capacity parameters

Deliverable: Three-tier model produces region-specific results that match observed inequalities (Frontier richer than Emerging richer than Developing) at baseline.

### Session 9 — Geopolitical stability layer

Goal: the international order dimension.

Tasks:
- Build `src/geopolitics/stability_index.py` with the six components from the chat session: interstate conflict, sub-state conflict, info warfare, coercion, AI arms race, governance capacity
- Causal mappings from policy architecture to each component, citing IR literature for each
- Coalition formation: which countries join Participatory under what conditions (game-theoretic, light-touch — illustrative not predictive)
- **Be honest**: this is the weakest leg empirically. Treat as illustrative.

Deliverable: Stability index produces results for each scenario; methodology section explicitly documents that this is illustrative.

### Session 10 — Paper figure pipeline

Goal: every figure in the paper traceable to specific model output.

Tasks:
- `src/analysis/chart_builders.py` with one function per paper figure
- Each function takes simulator output JSON, produces a Matplotlib figure with brand styling (Nebulai purple #7C3AED, indigo #1E1B4B, etc.)
- Save final paper figures to `paper/figures/` as PNG + SVG
- Build a meta-script `python -m src.analysis.chart_builders --paper` that regenerates every figure

Deliverable: All paper figures regenerated from scratch in one command.

### Session 11 — Methodology section in paper

Goal: write the technical companion section.

Tasks:
- Write `paper/sections/09_methodology.md` describing:
  - Theoretical foundations and citations
  - Calibration targets and sources
  - Backtest validation results
  - Monte Carlo design
  - Sensitivity analysis findings
  - **What the model does and does not capture** (explicit limitations)
- This section is what gets cited if the paper is published as a working paper

Deliverable: 6–10 page methodology document, internally cross-linked to the code.

### Session 12 — Limitations section

Goal: pre-empt every methodological critique.

Tasks:
- Write `paper/sections/10_limitations.md` honestly listing:
  - Median voter assumption (not how all polities work)
  - Cherry-picked historical precedents (Bismarck/FDR — but also Russia 1917)
  - State capacity assumed uniform (not realistic)
  - No financial sector / monetary side
  - No AGI alignment dimension
  - Coordination assumed possible at exactly the moment it's collapsing
  - The framework's "voluntary adoption" mechanism is theoretically optimistic
  - Aggregation across heterogeneous countries
- For each, note what would make the result fail and what the model can/cannot say about it

Deliverable: 4–6 page limitations document. The strongest signal of methodological seriousness in the paper.

### Sessions 13–14 — Buffer / iteration

Realistically, calibration issues will require backtracking, scenarios will need refinement, and figures will require redesign. Reserve 2 sessions for iteration before declaring v1.0.

### Session 15 — External methodology review

Out of scope for this repo, but the natural next step. Reach out to:
- Anton Korinek (UVA / Brookings)
- Convergence Analysis team
- Collective Intelligence Project

Send the methodology document, ask for substantive feedback. Iterate based on response. This is what produces a paper that survives peer review.

## Decisions log

Document major architectural decisions here as they're made. Format: date, decision, rationale.

- **2026-04-26** — Decided to bracket wealth-concentration dynamics (Piketty additions) as an explicit module rather than try to derive from production-side. Rationale: prototype phase showed that flow-income models cannot reproduce wealth concentration without separate stock-side mechanisms. Cleaner to model explicitly.

- **2026-04-26** — Decided σ=1 (Cobb-Douglas) for baseline 2025 calibration, despite Acemoglu-Restrepo 2022 suggesting σ ≈ 1.5. Rationale: σ=1 hits the labor share target. **Open question:** revisit whether two-sector model with σ=1.5 in AI sector and σ=1 elsewhere is needed. Flagged for Session 5.

- **2026-04-26** — Decided to use heterogeneous-agent simulation (10,000 households, 1,000 firms) rather than representative-agent. Rationale: distributional questions are the paper's central concern; representative-agent loses what we care about.
