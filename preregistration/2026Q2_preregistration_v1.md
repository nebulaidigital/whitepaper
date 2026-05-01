# Pre-Registration: Participatory AI Economy Simulation

**Document version:** 1.0
**Date:** 2026-05-01
**Author:** Nebulai Corp + Claude Code
**Branch:** `claude/economic-model-simulator-p2Bul`
**Status:** Draft — locked before any simulation run

> **Purpose.** This document specifies — *before any simulation is run* — the
> hypotheses to be tested, the validation criteria for each, the parameter
> ranges to be swept, the policy packages to be compared, and the decision rules
> for what counts as a "validated" insight versus a "refuted" one. Every
> simulation result reported in the eventual paper or policy document must trace
> to a hypothesis and test design specified here. Modifications to this document
> after simulation runs begin require an addendum (`v2.md`, `v3.md`, ...) that
> explains what changed and why.
>
> **The discipline this enforces.** Without pre-registration, parameter ranges
> and reported metrics are chosen post-hoc to support pre-committed conclusions.
> With pre-registration, the analysis is unattackable on that axis: the
> hypotheses are fixed, the tests are fixed, and the results — whether they
> validate or refute — are reported as specified.

---

## 1. Project framing

### 1.1 The question being answered

> **Across plausible policy packages for managing the 2025–2036 AI economic
> transition, which produces the highest expected welfare under deep parameter
> uncertainty, which is most robust to defection by major actors, and under
> what conditions do recommendations flip?**

This is *not* a question about whether the Nebulai six-pillar framework
"works." It is a comparative question across multiple candidate packages,
including the framework. The framework may dominate, may be dominated, or may
dominate only in specific conditions. All three outcomes are reportable.

### 1.2 What "accuracy" means here

The priority is decision-quality output for policy recommendations. This
implies:

1. **Counterfactual deltas, not absolute predictions.** Every reported number
   is a difference between a policy package and the Q1 2026 status-quo
   baseline (`BASELINE_2026.md`). Levels are not the deliverable.
2. **Honest uncertainty.** P10/P50/P90 trajectories from Monte Carlo / RDM
   over literature-anchored parameter distributions. No point estimates
   reported without intervals.
3. **Sign-flip identification.** Where in parameter space does each
   recommendation reverse? This is more decision-relevant than mean outcomes.
4. **Game-theoretic robustness.** A package that produces the highest mean
   welfare but fails under defection by a major actor is *not* the best
   package for actual policy. Stability tests are first-class deliverables.

### 1.3 What this analysis cannot do (declared in advance)

- Predict 2036 absolute outcomes
- Resolve the σ debate (Cobb-Douglas vs σ ≈ 1.5)
- Model AGI emergence or recursive self-improvement
- Quantitatively model conflict probability (geopolitical stability index is
  illustrative)
- Settle whether AI is fundamentally different from past automation

These limitations are stated up front and must remain in the paper's
limitations section.

---

## 2. Policy packages compared

Six packages run side-by-side. Specifications in `src/packages/*.py`.

| Package | Core mechanism | Source |
|---|---|---|
| **A. Status Quo (Patchwork)** | Current trajectory, no new framework | Baseline anchor — Acemoglu 2024 NBER WP 32487 |
| **B. Nebulai Six-Pillar Framework** | Sovereign equity + Pillar 2 + Pillar 3 + Reskilling + Open weights + AI tax | `paper/draft/` (Nebulai whitepaper v2) |
| **C. CERN-AI Centered** | Global public frontier lab + compute governance treaty + tiered openness + supporting transfers | Hausenloy et al. 2023 (MAGIC); Bengio et al. 2024 |
| **D. Compute-Centric** | Compute tax + access mandates + structural separation of compute providers from model labs | Sastry, Heim, Belfield et al. 2024 |
| **E. Direct Redistribution** | UBI + wealth tax + Universal Basic Capital + care-economy expansion | Atkinson 2015; Saez-Zucman 2019; Korinek-Juelfs 2023 |
| **F. Build-Different-AI (Acemoglu-Johnson)** | Directed R&D for human-complementary AI + procurement preference + worker codetermination + targeted antitrust | Acemoglu & Johnson 2023 *Power and Progress*; Mazzucato 2021 |
| **G. Game-Theoretic-Derived** | Eight pillars derived from individual rationality + coalition stability + verifiability tests | Derived in this work; Ostrom 1990 design principles |

Each package is implemented as a typed `PolicyPackage` dataclass
(`src/packages/base.py`) with a documented mapping from each policy lever to
its target mechanism in the simulation.

---

## 3. Primary hypotheses (Tier A — recommendation-altering if validated/refuted)

For each hypothesis: claim, test design, validation criteria, falsification
criteria, decision implication.

### Hypothesis 1: Open-Weights Inversion

**Claim.** In the post-DeepSeek bilateral world (China leads in open-weights,
US leads in closed-weights as of Q1 2026), the Nebulai framework's Pillar 5
(open-weights mandate) implemented unilaterally by the US does *not* dampen US
AI markups. Instead, it shifts US AI rents to (a) US compute providers and (b)
Chinese frontier model labs.

**Test design.** Run Package B with Pillar 5 active in the bilateral US-China
simulator under the empirically-observed Q1 2026 open/closed asymmetry.
Compare to Package B with Pillar 5 inactive.

**Metrics measured.**
- Δ(US mean AI-sector markup) from 2025 → 2036
- Δ(US compute-layer profit share) from 2025 → 2036
- Δ(Chinese AI sector revenue share) from 2025 → 2036
- Δ(US labor share)

**Validates if.** US AI markup falls by ≥0.02 *and* compute-layer profit share
rises by less than 50% of the markup decline *and* Chinese AI revenue does not
rise by more than 30% relative to baseline.

**Falsifies if.** Any of: US markup unchanged; compute layer captures >50% of
foregone rents; Chinese revenue rises >30%.

**Decision implication.** If falsified, Pillar 5 must be redesigned —
candidate replacements: tiered openness within CERN-AI consortium framework
(Package C), or paired with infrastructure-layer antitrust (Package D's
structural separation).

---

### Hypothesis 2: Reversibility-Weighted Optimal Sequence

**Claim.** Implementing pillars in reversibility-weighted order — reversible
pillars (4: reskilling, 6: AI tax) first, evidence-gated; semi-reversible
pillars (1: sovereign equity) second; near-irreversible pillars (5: open
weights) last or never — produces strictly higher expected welfare than
simultaneous activation, once honest uncertainty over pillar effectiveness is
included.

**Test design.** Two RDM runs of Package B with identical parameter
distributions:

1. Simultaneous activation: all pillars on at year 0
2. Sequential activation: Pillar 4+6 at year 0; Pillar 1 at year 3 *if*
   Pillar 4 leading indicator hits target; Pillar 5 at year 6 *if* Pillar 1
   leading indicator hits target

5,000 RDM draws each.

**Metrics measured.**
- E[Δ(median welfare)] across draws
- 10th-percentile Δ(median welfare) across draws
- E[Δ(GDP)] across draws
- Probability of Pareto improvement vs. status quo

**Validates if.** Sequential E[welfare] ≥ simultaneous E[welfare] *and*
sequential 10th-percentile welfare > simultaneous 10th-percentile welfare.

**Falsifies if.** Simultaneous outperforms on either measure (e.g., because
displacement urgency dominates option value).

**Decision implication.** If validated, framework recommendation is for
staged rollout, not all-at-once. If falsified, the urgency case for
simultaneous activation overrides reversibility considerations.

---

### Hypothesis 3: US-China Cooperation Threshold

**Claim.** There exists a quantifiable level of US-China policy cooperation
(probability θ that China adopts framework-aligned policies) below which
Package B underperforms Package A on global welfare. The framework's
recommendations are conditional on θ ≥ θ*.

**Test design.** Bilateral US-China simulator, parameterize China cooperation
propensity θ ∈ [0, 1] in steps of 0.1. Run Package B at each θ. Measure
welfare delta vs. Package A.

**Metrics measured.**
- θ* such that welfare(B; θ < θ*) < welfare(A) and welfare(B; θ ≥ θ*) > welfare(A)
- Confidence interval on θ* from RDM uncertainty
- Comparison: where does Q1 2026 best-estimate θ fall relative to θ*?

**Validates if.** A clear θ* exists in [0, 1] *and* Q1 2026 best-estimate θ
falls within ±0.2 of θ*.

**Falsifies if.** Package B dominates Package A at all θ ≥ 0 (framework is
robust to defection — strong claim) *or* Package B fails to dominate at any
θ < 1 (framework requires unattainable cooperation — also strong, negative).

**Decision implication.** If θ* lies in plausible cooperation range,
framework's pitch shifts from "the right policy" to "the right policy *if*
US-China coordination achievable" — which is a different political program.

---

### Hypothesis 4: Median-Voter Sufficiency Across All Deciles

**Claim.** Under Package B, the median household in every income decile in
every country tier (Frontier / Emerging / Developing) is better off vs.
Package A. (This is the framework's core adoption-equilibrium claim.)

**Test design.** Compute Δ(real income) for the median household in each of
10 deciles × 3 country tiers = 30 cells. Pass if all 30 cells are positive at
P50 *and* >25 cells are positive at P10.

**Metrics measured.** For each of 30 cells: P10, P50, P90 of Δ(real income)
from RDM ensemble.

**Validates if.** All 30 P50 deltas positive *and* ≥25 P10 deltas positive.

**Falsifies if.** Any P50 delta negative, *or* >5 P10 deltas negative.

**Decision implication.** If falsified, the adoption-equilibrium argument
needs revision — typically by adding compensating mechanisms for the failing
deciles (e.g., direct cash transfer for substitute workers in deciles 3–6 of
frontier countries). This changes the policy package itself.

---

## 4. Secondary hypotheses (Tier B — sharpen but don't reshape recommendations)

### Hypothesis 5: Capital Flight Threshold for Unilateral Action

**Claim.** There exists a capital-flight elasticity ε* below which unilateral
US Pillar 1 implementation is net welfare-improving. Above ε*, multilateral
coordination is required.

**Test.** Vary AI capital flight elasticity over [0.003, 0.015] /yr/pp.
Identify ε* where unilateral Pillar 1 crosses break-even.

**Decision-relevant output.** Where does ε* fall relative to current best
empirical estimate (~0.005, Bach et al. 2014; Brülhart et al. 2022)?

---

### Hypothesis 6: Sovereign Equity / AI Tax Substitutability

**Claim.** Pillars 1 and 6 are partial substitutes — combined activation
produces less marginal welfare than the sum of independent activations
because they target overlapping rents.

**Test.** Run Pillar 1 alone, Pillar 6 alone, Pillar 1+6 combined. Check
sub-additivity: Δ(combined) < Δ(Pillar 1) + Δ(Pillar 6).

**Decision-relevant output.** If substitutable, framework should pick one at
high intensity rather than both at moderate intensity.

---

### Hypothesis 7: Frontier-Country Sufficiency

**Claim.** Frontier-country-only adoption (US + EU + China + UK + Japan +
Korea) captures ≥80% of the welfare gain of universal adoption.

**Test.** Frontier-only run vs. universal run. Compare welfare deltas
globally and by country tier.

**Decision-relevant output.** Shapes whether Phase-1 advocacy targets G7+
or invests in Global South coordination.

---

### Hypothesis 8: Coerced Redistribution Counterfactual

**Claim.** The 2032 coerced-redistribution counterfactual (70% windfall tax +
capability caps imposed post-crisis) produces lower welfare than Package A
(Patchwork), establishing the "voluntary now or coerced later" framing.

**Test.** Stylized counterfactual scenario; compare welfare to Package A.

**Honest limitation.** Highly stylized; depends on assumed political-economy
responses. Treat result as illustrative; methodology section explicitly flags.

---

## 5. Tier C hypotheses (cross-package comparative)

### Hypothesis 9: Package Dominance Under Deep Uncertainty

**Claim.** Across packages A–G, no single package Pareto-dominates all
others under all parameter draws; instead, dominance is conditional on
parameter regime.

**Test.** RDM scenario discovery (PRIM / Patient Rule Induction Method) on
the joint output of all packages × ~10,000 parameter draws. For each metric,
identify the parameter region where each package is best.

**Output.** A "policy regret surface" per metric. The decision-relevant
artifact is *not* "package X is best" but "package X is best under
conditions Y, package Z is best under conditions W."

**This is the central deliverable of the project.** Hypotheses 1–8 are
sub-questions; Hypothesis 9 is the integrating analysis.

---

### Hypothesis 10: Game-Theoretic Robustness Ordering

**Claim.** Package G (game-theoretically derived) is more stable under
defection, coalition formation, and time-inconsistency stress tests than
Package B (Nebulai original).

**Tests.**
- *Defection test.* For each pillar, simulate the most likely defection
  (capital flight, jurisdiction shopping, weight non-release, treaty exit).
  Measure whether welfare under defection beats baseline.
- *Coalition test.* Vary participating coalition from 30% to 100% of global
  AI compute. Identify minimum threshold for each pillar to be welfare-positive.
- *Time-consistency test.* Introduce stochastic policy reversal (50%
  probability per pillar in years 5–10). Compare expected welfare.
- *Cross-class test.* By-decile welfare delta across 30 cells. Count cells
  with positive welfare under each package.

**Validates if.** Package G outperforms Package B on at least 3 of 4 stress
tests at P50.

**Falsifies if.** Package B outperforms G on ≥2 of 4 stress tests.

**Decision implication.** If Package G is more robust, framework should
adopt its pillar set. If B is more robust, framework's design choices are
vindicated by stress-testing.

---

## 6. Tier D — declared not-testable

The following claims appear in the paper but are *not* testable in this
simulation. They will be reported qualitatively only, with explicit
limitation notes:

- The probability that China cooperates with framework adoption (political
  question, not a macro one)
- Long-run AGI/ASI emergence dynamics
- Specific conflict probabilities under each scenario (geopolitical
  stability index is illustrative)
- Optimal AI safety / alignment policy

Quantitative claims about these dimensions in the paper would be
methodologically unsupported and must be flagged as such.

---

## 7. Parameter ranges and distributions

All parameters drawn from `SOURCES.md` literature anchors. RDM samples from
joint distributions over the following:

| Parameter | Distribution | Range | Source |
|---|---|---|---|
| σ (task elasticity) | Truncated normal | μ=1.5, σ=0.15, [1.1, 2.0] | Acemoglu-Restrepo 2022 Table 3 |
| Capital flight elasticity | Beta-shaped on log scale | [0.003, 0.015] /yr/pp | Bach 2014; Brülhart 2022 |
| Reskilling earnings effect | Truncated normal | μ=0.10, σ=0.04, [0.05, 0.20] | Card-Kluve-Weber 2018 |
| Open-weights markup dampening | Uniform | [0.10, 0.50] | Inferred from OSS economics |
| AI productivity growth | Truncated normal | μ=0.020, σ=0.010, [0.005, 0.05] | Acemoglu 2024; Goldman 2023 |
| US-China cooperation θ | Beta(2, 5) | [0, 1] | Subjective prior — declared |
| Top-decile differential return | Truncated normal | μ=0.020, σ=0.005, [0.010, 0.030] | Saez-Zucman 2016; Fagereng 2020 |
| Capability disclosure compliance | Uniform | [0.5, 1.0] | Subjective — declared |
| Compute coalition share | Truncated normal | μ=0.7, σ=0.10, [0.5, 1.0] | US+EU+JP+KR+TW = ~0.7 of frontier compute |

Joint distribution: parameters drawn independently except where literature
documents correlation (σ and AI productivity growth are positively correlated
per Acemoglu-Restrepo 2022 estimates; correlation = 0.3 imposed).

RDM sample size: 10,000 draws per package = 70,000 total runs. Computational
budget ~10–20 hours on one workstation; tractable.

---

## 8. Backtest validation gates

No simulation result is published unless the underlying model passes the
2015–2025 backtest within these tolerances:

| Indicator (US) | 2025 actual | Model tolerance |
|---|---|---|
| Labor share | 56% | ±2pp |
| Top 1% wealth share | 30.4% | ±2pp |
| Mean markup (sales-weighted) | 1.22 | ±0.05 |
| Real GDP growth (cumulative 2015–2025) | 22% | ±5pp |
| Substitute-worker employment Δ | (calibrated to BLS) | ±3pp |

| Indicator (China) | 2025 actual | Model tolerance |
|---|---|---|
| Labor share | ~50% (PWT) | ±3pp |
| Mean markup | ~1.13 | ±0.05 |
| Real GDP growth (cumulative 2015–2025) | ~62% | ±10pp |

If the bilateral model fails to backtest both countries within tolerance,
RDM analysis is not run. The model must explain past observed data before
producing forward-looking policy recommendations.

---

## 9. Decision rules for reporting

### 9.1 What gets reported

- **Validated hypotheses** → reported as primary findings with confidence
  intervals
- **Falsified hypotheses** → reported as refutations with the same prominence
- **Mixed results** (validates on some metrics, falsifies on others) →
  reported with explicit decomposition; no cherry-picking
- **Untestable claims** → declared and not made

### 9.2 What does not get reported

- Hypotheses not in this document (pre-registration enforcement)
- Results outside the parameter ranges declared in §7
- Point estimates without P10/P90 intervals
- Recommendations not traceable to a hypothesis test

### 9.3 Sensitivity and robustness disclosures

For every primary finding, the paper reports:
- Which parameters most affected the result (Sobol indices)
- Under what parameter combinations the result reverses
- The single most important caveat to the finding

This is non-negotiable for the methodology section.

---

## 10. Versioning and amendments

This document is `v1.0`, dated 2026-05-01. Any amendment after the first
simulation run produces a new version (`v2.md`, `v3.md`, ...) explaining:

1. What changed
2. Why
3. Whether the change was prompted by data observed in earlier runs
4. How prior results are or are not affected

Amendments after results are observed are stated explicitly as such; they
are not retroactive modifications. The original `v1.md` remains the
publication-eligible standard.

---

## 11. Approvals and accountability

| Role | Name | Approval |
|---|---|---|
| Project lead | (Nebulai Corp) | Pending |
| Methodological reviewer | (TBD — Korinek invited) | Pending |
| Adversarial reviewer (libertarian) | (TBD) | Pending |
| Adversarial reviewer (China-realist) | (TBD) | Pending |
| Adversarial reviewer (heterodox) | (TBD) | Pending |

Signed approvals required before primary RDM analysis (Phase 4) commences.
Phases 1–3 (empirical analogs, multi-model anchor, bilateral build) may
proceed before all approvals secured.

---

*End of pre-registration v1.0.*
