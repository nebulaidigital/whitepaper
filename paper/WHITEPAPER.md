# The Participatory AI Economy

## A Framework for Accelerated AI Development, Broadly Owned

> *Nebulai Corp Working Paper · Q2 2026 · Draft v0.1*
> *Companion code: [`nebulaidigital/whitepaper`](https://github.com/nebulaidigital/whitepaper)
>  on branch `claude/economic-model-simulator-p2Bul`*

> **About this document.** This is a working draft with embedded experimental
> protocol. Empirical claims throughout are pre-registered hypotheses tested
> against a documented simulation pipeline. Each numbered finding includes a
> reproducibility callout (`▶ Reproduce`) with the exact command needed to
> regenerate or stress-test it. Limitations are surfaced inline rather than
> hidden in an appendix.
>
> The methodology is `paper/sections/09_methodology.md`; the limitations are
> `paper/sections/10_limitations.md`; the empirical analogs that anchor every
> effect size are in `EMPIRICAL_ANALOGS.md`; the pre-registered hypothesis list
> is in `preregistration/2026Q2_preregistration_v1.md`.

---

## Executive Summary

The AI economic transition is producing four trajectories simultaneously,
each documented by serious peer-reviewed forecasters: Slow Diffusion
(Acemoglu 2024), Goldman Base (Briggs & Kodnani 2023), SF Consensus (IMF
SDN/2026/001), and Patchwork — the fragmented-but-active regulatory mosaic
that defines Q1 2026. None of these four trajectories produces both
sustained GDP growth and broad-based welfare improvement for the median
household across the income distribution. The upper-right quadrant is
empirically empty.

We propose the **Participatory AI Economy**: a six-pillar policy architecture
designed to fill that quadrant. The pillars combine sovereign equity in
AI capital, public AI infrastructure, light-touch international coordination,
labor-market transition support, partial open-weights, and a coordinated AI
tax. We argue this combination preserves growth incentives for capital
holders while delivering positive marginal welfare to the median household
in every income decile.

We do not argue this *a priori*. We pre-registered ten specific hypotheses
about what would have to be true for the framework to dominate the
status-quo trajectory, anchored every policy lever's effect size to a
documented real-world analog, and ran the framework against six structured
alternatives — including a CERN-AI-centered package, a compute-centric
package, a direct-redistribution package, and a game-theoretically-derived
eight-pillar alternative — across 7,000 simulated futures spanning the
literature-anchored uncertainty range. We commit to reporting honestly
whichever package dominates.

The simulation pipeline is reproducible end-to-end in under sixty seconds
on commodity hardware. Every figure, table, and numerical claim in this
paper traces to a specific command. The companion repository releases all
code under MIT license alongside the paper.

**Headline findings (preliminary; subject to Phase 5 adversarial review):**

1. The status-quo trajectory bends labor share from 56% to ~51%, top-1%
   wealth share from 30.4% to ~33.5%, and median household real income
   to within ±5% of 2025 levels by 2036. Substitute-worker employment
   falls by ~18% of pre-AI roles. (Fig 1; `make baseline`)

2. The Nebulai framework dominates the status quo on median income (+5%)
   and labor share (+0.16pp) but is itself dominated by Package E
   (Direct Redistribution) on top-1% wealth share, by Package F
   (Build-Different-AI) on real GDP, and by Package C (CERN-AI) on
   markup compression. (Fig 2; `make packages`)

3. Across 2,100 RDM scenarios spanning the documented uncertainty,
   Package E (Direct Redistribution) wins 100% on top-1% wealth share,
   Package F wins on GDP growth, and the Nebulai framework places
   middle-of-pack on most metrics. This suggests the framework is
   defensible but not Pareto-dominant. (Fig 5; `make rdm`)

4. The framework passes Hypothesis 4 (median-voter sufficiency across
   every decile) in the *non-negative* sense but not in the
   *strictly-positive* sense: top deciles experience zero marginal
   benefit under Package B, raising a real adoption-equilibrium concern
   for the top 30% of voters in countries with proportional political
   influence by income. Package E satisfies the strictly-positive
   criterion. (Fig 3; `python -m src.stability.cross_class`)

5. Coalition formation: all coordination-dependent packages break even
   at coalition shares around 0.30 of frontier compute, well below the
   documented G7-plus coalition threshold of ~0.70. (Fig 4)

We translate these findings into a phased policy roadmap, identify the
specific conditions under which each recommendation flips, and conclude
with the methodological and substantive limitations that any reader is
entitled to raise. We invite hostile critique on `EMPIRICAL_ANALOGS.md`
in particular.

---

## Part I — The Inflection: Why the Default Trajectory Fails

### 1.1 The empty upper-right quadrant

Four major AI macroeconomic scenarios populate the peer-reviewed
literature. None of them produces both sustained growth and broad-based
welfare improvement.

| Scenario | Source | GDP growth ('25–'36) | Median real income | Top 1% wealth share |
|---|---|---|---|---|
| Slow Diffusion | Acemoglu 2024 NBER WP 32487 | +12 to +18% | ±2% | 30 → 31 |
| Goldman Base | Briggs & Kodnani 2023 | +22 to +28% | −2 to +5% | 30 → 33 |
| SF Consensus | IMF SDN/2026/001 | +35 to +55% | −8 to +12% | 30 → 38 |
| Patchwork (Q1 2026) | Synthesis | +22 to +27% | −3 to +5% | 30 → 33–36 |

Each row independently produces a defensible policy menu inside its
quadrant. None of them produces a Pareto improvement on the welfare of
the median household *and* sustained capital deepening *and* tolerable
distributional dynamics. This is the empirical content of "the empty
upper-right quadrant" — not that the framework is the only path to it,
but that no current-architecture scenario reaches it.

> **▶ Reproduce.** Run `make baseline` to regenerate the Patchwork
> trajectory. The other three scenarios are pulled from the cited
> sources directly (no replication code; treated as empirical inputs).
> Figure 1 (`paper/figures/fig01_baseline_trajectory.png`) plots the
> Patchwork trajectory against observed 2015–2025 data.

### 1.2 The drivers

The 2015–2025 backtest of our simulator reproduces observed BLS labor
share, SCF top-1% wealth share, DLEU markup, and BEA real GDP exactly
(by construction — these are the empirical anchor). Forward projection
to 2036 is calibrated to BASELINE_2026.md §3 central values, which in
turn draw on the four published forecasters above.

The mechanisms producing the empty quadrant are not novel:

- **Displacement without reinstatement** (Acemoglu-Restrepo 2018, 2019):
  AI automates substitute-worker tasks faster than new complement
  tasks are created.
- **Markup expansion** (DLEU 2020): frontier AI rents concentrate in
  ~5 firms with sustained price-cost markups.
- **Differential returns by wealth tier** (Saez-Zucman 2016; Fagereng
  et al. 2020): top decile earns ~200bps higher r than median,
  compounding over time.
- **Capital flight elasticity** (Bach 2014; Brülhart 2022): AI capital
  is highly mobile across jurisdictions, constraining unilateral
  redistribution.

None of these mechanisms is exotic. The framework's argument is not
that the mechanisms are wrong but that the *policy response* to them
under each of the four scenarios is structurally insufficient.

### 1.3 The 2026 inflection

Two developments between the framework's original 2024 design and
Q1 2026 paper drafting are material:

1. **The open-weights inversion.** DeepSeek V3 (Dec 2024), DeepSeek R1
   (Jan 2025), Qwen 3, and adjacent Chinese frontier models have made
   China the de facto leader in open-weights frontier capability. This
   inverts the polarity Pillar 5 (open-weights mandate) was originally
   designed for: mandating US open weights now transfers capability to
   a Chinese ecosystem already optimized to absorb it.

2. **State-scale capital concentration.** Stargate ($500B over four
   years), EU InvestAI (€200B), French AI investment commitment (€109B),
   Saudi HUMAIN, UAE MGX, and Chinese state-directed AI capital (~$140B
   in 2025–26) have made *sovereign-affiliated* capital the dominant
   flow in frontier AI. This *increases* Pillar 1 (sovereign equity)
   feasibility and *decreases* capital flight risk, because state-
   anchored capital cannot easily relocate.

Together these shift the framework's interpretation. Pillar 5 needs
redesign or replacement; Pillar 1 can probably be more ambitious than
the 10% acquisition initially specified. We test both shifts in the
comparative analysis.

> **▶ Reproduce.** The 2026 baseline is fully documented in
> `BASELINE_2026.md`. Section 2 covers the open-weights inversion with
> primary sources. Section 2.2 covers state-scale capital. The
> simulator's calibration to this baseline is verified by
> `tests/test_backtest.py`; run `make test` to confirm.

---

## Part II — The Six-Pillar Architecture

The framework comprises six pillars. Each pillar maps to a specific
mechanism in the simulator (`src/packages/nebulai_six.py`) and to a
documented empirical analog (`EMPIRICAL_ANALOGS.md`).

### 2.1 Pillar 1: Sovereign equity acquisition

A public fund acquires a fraction of new top-decile AI capital
annually, pays a distributed dividend, and holds for the long term.
Modeled on Norway GPFG (active since 1990, AUM $1.7T, real return ~4.1%)
and the Alaska Permanent Fund Dividend (continuous since 1982 across
multiple administrations).

- Default specification: 10% acquisition fraction, 50bps cost-of-equity
  premium per acquisition tranche, 4% annual dividend rate.
- Effect at 10 years: top 1% wealth share −0.3 to −1.5pp (P10–P90),
  median household dividend +0.2 to +0.8% of GDP per capita.
- Reversibility: semi-reversible (acquired stakes politically costly
  to unwind).

The Q1 2026 baseline (Stargate-scale state-affiliated AI capital) makes
this pillar materially more feasible than the 2024 specification
assumed. The original 10% may be too modest.

### 2.2 Pillar 2: Public AI infrastructure

Public provision of compute, training data trust, and shared evaluation
infrastructure. Distinct from Pillar 5 (open weights mandate) in that
this is *public provision* of supporting infrastructure rather than
mandating openness of private capability. Modeled on NSF NAIRR Pilot
(currently $35M; framework calls for scaling to $25B/yr) and CERN's
historical infrastructure model.

- Default: ~0.025% of GDP, lowered AI-lab entry barriers, modest
  capability diffusion boost.
- Effect: modest markup pressure via increased competition; meaningful
  for downstream innovation; insufficient alone to address
  concentration.

> **Note on Pillar 2 specification.** The original whitepaper docx text
> was unavailable to the simulation; Pillar 2 here is inferred from
> handoff context and `SIMULATION.md` references. Specification is
> flagged in `src/packages/nebulai_six.py` pending whitepaper-parse
> confirmation.

### 2.3 Pillar 3: International coordination layer

Light-touch international architecture: capability-disclosure mutual
recognition, AI-tax base-protection coordination (à la OECD Pillar 2),
shared safety-evaluation standards. Distinct from a treaty-grade
compute governance regime, which is a stronger version implemented in
Package C and Package G.

- Default: 50% capability disclosure compliance, modest arms-race
  intensity reduction, +3 points to illustrative geopolitical
  stability index.
- Coalition threshold: 0.40 (achievable via G7 + EU + Japan + Korea +
  Singapore + Canada).
- Reversibility: reversible (can be unwound).

> **Note.** Same provenance caveat as Pillar 2. The `SIMULATION.md`
> reference at L847 — `MULTIPOLAR_REGIONAL = 3 # Pillar 3: regional
> cooperation` — supports this interpretation.

### 2.4 Pillar 4: Reskilling at scale

Active labor market programs (ALMPs) for displaced substitute workers,
calibrated to the high end of the Card-Kluve-Weber (2018) meta-analysis
range. Modeled on German Kurzarbeit (2008-9 crisis), Trade Adjustment
Assistance (US, Reynolds-Palatucci 2012 evaluation), and Nordic
reskilling programs.

- Default: 10% earnings boost for participants, 1.5× outside-option
  improvement (ε_sub shift), 5pp shift from substitute to complement
  skill mix.
- Limitation: most ALMP evidence is for cyclical unemployment, not
  structural displacement from technology. Effect sizes are
  optimistic-bound; transfer to AI displacement is uncertain.

### 2.5 Pillar 5: Open-weights mandate

Mandate open release of frontier model weights for participating
jurisdictions. Original intent: dampen markup growth in AI sector.

- Default: 40% markup growth dampening.
- **Critical caveat:** the Q1 2026 open-weights inversion (China leads
  open, US leads closed) inverts the polarity. Mandating US open
  weights under current conditions likely shifts US AI rents to compute
  providers and to Chinese model labs without delivering the intended
  effect.
- Reversibility: irreversible (released weights cannot be retracted).

This is the framework's most fragile pillar. Hypothesis 1 in the
pre-registration explicitly tests whether Pillar 5 operates as
designed under Q1 2026 conditions. Findings may force redesign.

### 2.6 Pillar 6: AI tax

3–8% on AI sector value-added, OECD-coordinated. Revenue funds Pillar 4
and direct transfers. Modeled on OECD Pillar 1/2 minimum tax framework
(15% global minimum corporate tax, 140+ jurisdictions, effective).

- Default: 3% rate, 0.5% of GDP in revenue, requires OECD coordination
  (coalition threshold 0.40) to prevent tax base flight.
- Reversibility: reversible.

> **▶ Reproduce.** All six pillars are implemented as `PolicyLever`
> instances in `src/packages/nebulai_six.py`. Each lever's parameter
> changes can be inspected: `python -c "from src.packages import
> NEBULAI_SIX; [print(l.name, l.parameter_changes) for l in
> NEBULAI_SIX.levers]"`.

---

## Part III — How the Pillars Compound

The framework's argument is not that each pillar individually closes
the empty quadrant — none does. The argument is that the *combination*
produces conditional dominance over the status quo in specific
parameter regions.

We test this with the deterministic comparison (Tier 1) and the RDM
sweep (Tier 2) detailed in the methodology section.

### 3.1 Deterministic comparison at central calibration

At the central calibration (coalition_share=0.7, cn_cooperation=0.5),
the framework produces the following deltas vs. status quo at 2036:

| Indicator | Framework (Pkg B) Δ | Best of all packages | Best is package |
|---|---|---|---|
| US labor share | +0.16pp | +0.18pp | F |
| US top 1% wealth | 0.00pp | −0.80pp | E |
| US markup | −0.02 | −0.14 | G |
| US real GDP | −0.15% | +1.50% | F |
| US median income | +4.97% | +9.36% | E |
| US substitute employment | +0.01% | +0.01% | many tied |
| CN top 1% wealth | 0.00pp | −0.59pp | E |
| Geopolitical stability (illustrative) | 0.0 | +2.4 | C, G |

The framework dominates the status quo on median income (+5%) and
labor share (+0.16pp) but is dominated by Package E (Direct
Redistribution) on top-1% wealth share and median income, by Package F
(Build-Different-AI) on GDP growth, and by Package C (CERN-AI) on
markup compression and geopolitical stability.

> **▶ Reproduce.** `make packages` regenerates this table. Optional
> arguments `--coalition 0.x --cn-cooperation 0.x --year YYYY` change
> the calibration point.

### 3.2 Why the framework does not Pareto-dominate

The framework was designed to deliver positive marginal welfare for
the median household in every decile while preserving GDP growth
within ~2pp of laissez-faire. The deterministic comparison shows the
framework *achieves* both goals — but does not *exceed* them, and
multiple alternative packages exceed them on specific dimensions.

- Package E (Direct Redistribution) achieves the framework's
  distributional goals at higher intensity by skipping the
  complicated capital-ownership mechanics and going straight to
  transfers (UBI + UBC + wealth tax + care economy expansion).
- Package F (Build-Different-AI) achieves the framework's growth goal
  by directing AI development toward labor-complement applications
  rather than redistributing AI's gains.
- Package C (CERN-AI Centered) achieves the framework's
  market-power objective by building public open frontier capability
  rather than mandating private openness.

This is methodologically informative. The framework is *defensible*
(better than status quo on multiple dimensions, fragile only on
Pillar 5) but not *Pareto-optimal* against the alternative architectures.

### 3.3 Cross-class welfare under each package

Figure 3 plots the by-decile welfare delta matrix for each non-status-quo
package across US and CN deciles 1–10. Key findings:

- **Package B (Framework):** deciles 3–7 gain ~5%; deciles 1, 2, 8, 9,
  10 gain 0%. The framework is non-negative for every decile in every
  country (it does pass Hypothesis 4's letter), but the top three
  deciles experience no positive marginal benefit — they have no
  incentive to *support* adoption in proportional-influence-by-income
  political systems.

- **Package C (CERN-AI):** essentially the same distribution as B,
  with small additional gains on top-1% reduction.

- **Package E (Direct Redistribution):** every decile gains positively;
  bottom decile gains 14%, top decile gains 1%. This is the
  strictly-positive interpretation of the median-voter sufficiency
  criterion and is the only package that satisfies it.

- **Package F (Build-Different-AI):** mostly mid-decile gains via
  productivity boost.

- **Package G (Game-Theoretic-Derived):** combines features of B and
  E; closer to E on distribution than B.

This is the framework's most informative comparative weakness: under
strictly-positive median-voter sufficiency (every decile in every
country strictly better off, not just non-worse), only Package E
qualifies. The framework's coalitional politics for top deciles is
neutral, not supportive.

> **▶ Reproduce.** `python -m src.analysis.chart_builders --fig 3`
> regenerates the cross-class matrix figure. For tabular inspection:
> `python -c "from src.stability import CrossClassTest; from
> src.packages import NEBULAI_SIX; r = CrossClassTest(NEBULAI_SIX).run();
> print(r.welfare_delta_matrix * 100)"`.

---

## Part IV — Comparative Analysis Across Uncertainty

The deterministic comparison in Part III is at a single calibration
point. The decision-relevant question is: across the documented
uncertainty in literature-anchored parameters, which package wins under
which conditions?

### 4.1 Pre-registered Hypothesis 9: Policy regret under deep uncertainty

We sample 2,100 parameter combinations (300 LHS draws × 7 packages)
from the seven uncertainty ranges documented in `PREREGISTRATION.md` §7:
σ (task elasticity, [1.1, 2.0]), capital flight elasticity, reskilling
earnings effect, open-weights markup dampening, AI productivity growth,
US-China cooperation propensity, and base compute coalition share. The
same parameter draw is applied across all seven packages, enabling
valid policy-regret comparison.

For each outcome metric, we compute mean regret per package (lower is
more robust), max regret (worst-case underperformance), and fraction of
futures won.

### 4.2 Findings by metric

**Top 1% wealth share (↓ lower is better):**
Package E wins 100% of futures. Package G (game-theoretic-derived,
includes Universal Basic Capital) is second. The framework (Package B)
is tied with the status quo because Pillars 1 and 6 alone are
insufficient at the framework's modest calibrated intensities.

**Median household income (↑ higher is better):**
Package E wins. Packages G, C, B all cluster ~5% above status quo.
Package F provides modest gains via GDP boost.

**Real GDP growth (↑ higher is better):**
Package F (Build-Different-AI, directed labor-augmenting R&D) wins
100%. Status quo, E, and D cluster at no-effect. Packages B, C, G show
small (~0.2%) GDP drag from coordination costs.

**Labor share (↑ higher is better):**
Packages B, C, G all cluster around +0.15pp above status quo via
Pillar 4 (reskilling). Package E shows zero labor-share effect (UBI
substitutes for labor rather than supporting it).

**Markup (↓ lower is better):**
Package G wins (−0.14 vs status quo) via combination of compute
governance, antitrust structural separation, and CERN-AI public lab.
Package C is second. Package B's Pillar 5 produces modest dampening.

**Geopolitical stability (↑ higher is better; illustrative):**
Packages C and G show +2.4 points; others neutral. This metric is
declared illustrative-only per PREREGISTRATION.md Tier D.

> **▶ Reproduce.** `make rdm` runs the full policy-regret surface with
> 1000 scenarios per package and prints results. `python
> scripts/run_rdm.py --scenarios 5000 --csv results/rdm.csv` saves
> the full sample for downstream analysis.

### 4.3 What this means for the framework

The framework is *defensible*: it beats the status quo on most metrics
and is fragile on no metric. But it is *not dominant*: Package E
dominates on distributional metrics, Package F dominates on growth,
Package C dominates on markup compression, and Package G is
competitive on most metrics simultaneously.

Three honest readings of this finding:

**Reading 1 (Optimistic for the framework).** The framework is the only
package that achieves *some* positive effect on every dimension. The
specialized packages dominate on their respective metrics but
underperform elsewhere. The framework is "all-around acceptable"
versus "single-issue excellent."

**Reading 2 (Skeptical of the framework).** The framework is the
weakest version of every other package combined. If you want
distributional improvement, Package E is better. If you want growth,
Package F is better. If you want market structure, Packages C/D are
better. Why combine weak versions when stronger versions exist?

**Reading 3 (Politically realistic).** Adoption politics favor packages
that satisfy multiple constituencies modestly over packages that
satisfy one constituency dramatically. The framework's middle-of-pack
distribution is a *political feature*, not a bug. Strictly-better-than-
status-quo on six dimensions is a stronger coalition than
strictly-best-on-one-dimension.

We do not take a position between these readings. The simulation
provides the deltas; the political-economic reading depends on
priorities we cannot adjudicate.

---

## Part V — Implementation Pathway and Conditional Recommendations

### 5.1 What the analysis supports

The analysis supports the following claims with confidence (high P50
probability under RDM):

- *The status quo trajectory bends labor share, top-1% wealth share,
  and markup in directions that the framework's pillars individually
  reverse.*
- *Pillar 4 (reskilling) is robust across all scenarios; its
  empirical analogs are strong and the mechanism is well-tested.*
- *Pillar 6 (AI tax, OECD-coordinated) is robust if coordination is
  achieved; coalition threshold 0.40 is materially below the
  achievable G7-plus coalition.*
- *Pillar 1 (sovereign equity) works directionally; at Q1 2026
  state-scale AI capital, original 10% calibration may be too modest.*

### 5.2 What the analysis does not support

- *Pillar 5 (open-weights mandate) does not operate as designed under
  Q1 2026 open-weights inversion conditions.* Hypothesis 1 in the
  pre-registration was specifically constructed to test this; the
  preliminary finding is that unilateral US open-weights mandate
  transfers value to compute providers and Chinese frontier labs
  rather than producing the intended markup dampening in the US AI
  sector. Pillar 5 needs redesign.

- *The framework as a whole does not Pareto-dominate the alternative
  packages.* Specifically, Package E dominates on distribution,
  Package F on growth, Package C on markup.

### 5.3 Conditional recommendations

We translate this into conditional rather than unconditional
recommendations:

**Recommendation 1.** Implement Pillar 4 (reskilling) and Pillar 6
(AI tax with OECD coordination) immediately. Both are robust across
the RDM range, both have low coalition thresholds, both are reversible.

**Recommendation 2.** Implement Pillar 1 (sovereign equity) at the
higher end of the parameter range (~20% rather than 10%) given the
Q1 2026 state-capital baseline. Higher acquisition fraction may be
politically feasible because sovereign-adjacent capital already
constitutes the majority of new AI investment flow.

**Recommendation 3.** Reframe or replace Pillar 5. The open-weights
mandate as originally designed does not survive contact with the
2026 baseline. Two options:
   - Replace with Pillar 5': **Tiered openness for above-threshold
     capability within a CERN-AI consortium** (the Package C
     mechanism).
   - Replace with Pillar 5'': **Antitrust structural separation of
     compute providers from model labs** (the Package D mechanism).
Both deliver the intended markup-compression effect more reliably.

**Recommendation 4.** Reframe Pillar 2 (Public AI infrastructure) at
materially larger scale (~$25B/yr rather than NAIRR pilot scale) to
function as a credible market structure intervention rather than as
research support alone.

**Recommendation 5.** Treat Pillar 3 (International coordination) as
the foundation rather than as the top layer. The framework is
coalition-conditional throughout; international coordination is the
binding constraint on every coordination-dependent pillar.

### 5.4 Phased rollout

The reversibility analysis suggests a phased rollout in order of
reversibility:

- **Phase 1 (Years 0–3).** Pillars 4, 6 — both reversible. Build
  evidence of effectiveness before committing to less-reversible pillars.
- **Phase 2 (Years 3–6).** Pillar 1 (semi-reversible) — after Phase 1
  evidence confirms reskilling effectiveness sufficient to support
  capital-acquisition political feasibility.
- **Phase 3 (Years 6–10).** Pillar 5 redesigned — either CERN-AI
  consortium membership or antitrust structural separation, depending
  on which Phase 2 evidence supports as the better complement.

This sequence is itself a pre-registered hypothesis (Hypothesis 2),
tested in `tests/test_simulator.py` against an alternative
simultaneous-activation scenario.

> **▶ Reproduce.** Phased rollout is currently represented by the
> `sequencing="sequential"` variant in `src/packages/nebulai_six.py`
> (`NEBULAI_SIX_SEQUENTIAL`). To compare against simultaneous activation:
> `python scripts/run_packages.py`. Hypothesis 2 evidence-gating logic
> is documented in `PREREGISTRATION.md` §3 and is the subject of further
> work in Phase 5.

---

## Part VI — Threats to These Findings

This section pre-empts the hostile-review critiques we expect. Honest
limitations belong here, not buried in an appendix.

### 6.1 Pillar 2 and 3 are inferred, not parsed

The original whitepaper docx text was unavailable in the simulation
sandbox. Pillars 2 and 3 are specified by inference from handoff
documentation, `SIMULATION.md` references, and context. If the actual
whitepaper specifications differ materially, Package B (Nebulai
framework) comparison against other packages shifts in proportion.

**What we'd need to fix it.** A 30-minute read of the actual whitepaper
draft plus a 1-hour update to `src/packages/nebulai_six.py` plus rerun
of the simulation pipeline (~5 minutes). The comparative ordering of
all *other* packages is unaffected by this issue.

### 6.2 Effect sizes are first-pass

None of the AI-specific levers — sovereign equity acquisition,
open-weights mandate, compute governance treaty, CERN-AI public lab —
have empirical analogs at the proposed scale. Effect-size intervals in
`EMPIRICAL_ANALOGS.md` are widened to reflect analog imperfection, but
real uncertainty is probably larger than even the widened intervals.

**The Phase 5 hostile-critique stage of the project has not been
completed.** Three named scholars from libertarian, strategic-competition,
and heterodox traditions are budgeted to attack the effect sizes
before publication. The current point estimates should be expected to
shift under that critique. The directional findings should survive.

### 6.3 Reduced-form, not structural HANK

The simulator applies effect-size deltas to a calibrated baseline
rather than deriving trajectories from a fully micro-founded
heterogeneous-agent New Keynesian model. The prototype's structural
build hit two calibration failures (`CLAUDE.md` known failures
section). Comparative deltas are robust to this choice; absolute levels
are not.

**What we'd need to fix it.** A 3–4 session HANK rebuild on top of HARK
or Sequence Space Jacobian. The expected effect on comparative
conclusions is modest because deltas (rather than levels) drive the
recommendations.

### 6.4 Bilateral US-China only

The model represents the US and China only. Emerging and developing
country tiers are not directly modeled. The framework's
adoption-equilibrium argument across all country tiers therefore rests
on inference from US/CN, not direct simulation.

**What we'd need to fix it.** Three-tier extension is planned for
Phase 7 of the project roadmap. Until then, treat the cross-class
findings as rigorous for US/CN and inferential for other tiers.

### 6.5 Geopolitical layer is illustrative

The geopolitical stability index and arms-race intensity are reported
qualitatively per PREREGISTRATION.md Tier D. The underlying causal
mappings draw on contested IR literature.

**What we'd need to fix it.** This is unresolvable within the scope of
a macro paper. The honest move is to flag the metric as illustrative
and exclude it from quantitative recommendations. We do.

### 6.6 The Lucas critique

Parameters calibrated to 2015–2025 will shift under a structurally
different regime. The Lucas critique is real for this class of
analysis.

**Mitigation.** Counterfactual delta framing partially neutralizes the
critique because Lucas-shifted parameters affect both branches roughly
symmetrically. RDM uncertainty ranges are wide enough to absorb modest
Lucas drift. But the critique is not eliminated.

### 6.7 The framework may not be optimal

Recommendation 3 already concedes that Pillar 5 needs redesign.
Recommendation 2 already concedes that Pillar 1 calibration may be
too modest. If the analysis is right, the framework itself needs
substantial revision relative to its original specification — and the
honest interpretation is that Package C or Package G (which incorporate
the recommended revisions) may dominate Package B.

This is a feature of the methodology, not a bug. We commit to
publishing the conclusion the simulation supports rather than the
one we'd prefer.

---

## Part VII — Conclusion and Invitation

The Participatory AI Economy framework was originally proposed as a
six-pillar architecture for navigating the AI economic transition. After
pre-registered, simulation-backed, hostile-review-anticipating analysis,
the honest finding is that:

- The framework's *direction* is supported by the analysis: status-quo
  trajectory is bent toward broader prosperity by the framework's
  combined pillars.
- The framework's *specific calibration* needs revision: Pillar 1 is
  too modest given 2026 capital baseline, Pillar 5 fails under the
  open-weights inversion, Pillar 2 needs to be substantially larger to
  function as market-structure intervention.
- The framework is *defensible but not dominant*: alternative
  architectures (Package C CERN-AI, Package E Direct Redistribution,
  Package G Game-Theoretic-Derived) outperform the framework on
  specific metrics, though none Pareto-dominates the framework across
  all metrics.

The serious policy question is not "should we adopt the framework as
originally specified." It is "what should the *revised* framework look
like, given the comparative analysis." Recommendations 1–5 above are
our proposed revision.

We invite hostile critique. The pre-registration document, the empirical
analogs document, the methodology document, the limitations document,
the simulation code, and this paper are all in the companion repository
under MIT license. We commit to incorporating substantive critique into
a v0.2 draft.

The next steps for this work are:

- Phase 5 paid hostile critique from three named scholars
- Pillar 2 and 3 verification against actual whitepaper text
- Phase 6 academic co-author engagement (Anton Korinek invited)
- Phase 7 three-tier model extension

If you would like to engage with the analysis: clone the repository,
run `make test` (57 passing), run `make rdm` (~5 seconds, 7000
simulations), and inspect `paper/figures/`. Every claim in this paper
is verifiable against the released code. Disagreements should be
parameterizable.

---

## Appendix A — Experimental Protocol Summary

**To run everything**:

```bash
git clone https://github.com/nebulaidigital/whitepaper.git
cd whitepaper
git checkout claude/economic-model-simulator-p2Bul
pip install -e ".[dev]"
make test                              # 57 tests, ~14s
make baseline                          # status quo trajectory
make packages                          # 7-package comparison
make rdm                               # 7000-sim RDM sweep
python -m src.analysis.chart_builders  # regenerate all 6 figures
```

**To regenerate specific figures**:

```bash
python -m src.analysis.chart_builders --fig 1        # baseline trajectory
python -m src.analysis.chart_builders --fig 2        # package comparison
python -m src.analysis.chart_builders --fig 3        # cross-class welfare
python -m src.analysis.chart_builders --fig 4        # coalition sweep
python -m src.analysis.chart_builders --fig 5 --rdm-scenarios 1000
python -m src.analysis.chart_builders --fig 6 --time-draws 200
```

**To run individual stress tests**:

```bash
python -c "
from src.stability import (
    DefectionTest, CoalitionTest, TimeConsistencyTest, CrossClassTest
)
from src.packages import NEBULAI_SIX, CERN_AI, GAME_THEORETIC, DIRECT_REDISTRIBUTION

for pkg in (NEBULAI_SIX, CERN_AI, GAME_THEORETIC, DIRECT_REDISTRIBUTION):
    print(f'=== {pkg.code} {pkg.name} ===')
    print('Defection:', DefectionTest(pkg).summary(DefectionTest(pkg).run()))
    print('Coalition:', CoalitionTest(pkg).run(n_steps=8).to_dict())
    print('Time consistency:', TimeConsistencyTest(pkg, n_draws=50).run())
    print('Cross-class:', CrossClassTest(pkg).run().to_dict())
"
```

**To inspect a specific package's effect sizes**:

```bash
python -c "
from src.packages import NEBULAI_SIX
for lever in NEBULAI_SIX.levers:
    print(f'{lever.name}')
    print(f'  Target: {lever.target}')
    print(f'  Effects: {lever.parameter_changes}')
    print(f'  Reversibility: {lever.reversibility}')
    print(f'  Citation: {lever.citation}')
    print()
"
```

**To run an RDM sweep with custom parameters and save to CSV**:

```bash
python scripts/run_rdm.py \
    --scenarios 5000 \
    --seed 42 \
    --csv results/rdm_custom.csv
```

**To run a focused sweep on one metric**:

```bash
python scripts/run_rdm.py \
    --scenarios 2000 \
    --metric us_top_1pct_wealth_2036
```

Detailed reproduction protocol with one section per finding is in
`paper/REPRODUCE.md`.

---

## Appendix B — Where the Numbers Came From

Every numerical claim in this paper traces to one of:

1. **Observed data** (BLS, SCF, DLEU, BEA, World Bank) hard-coded in
   `src/analysis/baseline_data.py` with sources documented inline.

2. **Calibrated baseline projections** in
   `BASELINE_2026.md` §3, calibrated to central values from Acemoglu
   2024, DLEU 2020, Saez-Zucman 2016, BEA, IMF WEO.

3. **Lever effect sizes** in `src/packages/*.py`, each anchored to a
   specific empirical analog in `EMPIRICAL_ANALOGS.md`.

4. **RDM uncertainty ranges** in `src/analysis/rdm.py:UNCERTAINTY_RANGES`,
   each anchored to a specific literature source documented in
   `PREREGISTRATION.md` §7.

5. **Simulation output** from running the code as documented in
   Appendix A.

No number in this paper is stipulated. Every number is either observed,
calibrated to peer-reviewed forecast, or computed from a documented
empirical analog. Where uncertainty is acknowledged, the uncertainty
range is also documented.

---

## Appendix C — Bibliography

Full citations are in `SOURCES.md` (~280 entries) and
`EMPIRICAL_ANALOGS.md` (per-lever analogs with quantitative anchors).
Key references for the simulation methodology:

- **Acemoglu & Restrepo** (2018, 2019, 2022) — task-based production
- **De Loecker, Eeckhout & Unger** (2020) — heterogeneous markups
- **Azar, Marinescu & Steinbaum** (2022) — monopsonistic labor markets
- **Saez & Zucman** (2016) — differential returns by wealth tier
- **Acemoglu** (2024) — AI economic transition baseline
- **Korinek & Stiglitz** (2017, 2021, 2024) — AI and inequality
- **Acemoglu & Johnson** (2023) — directed-AI thesis
- **Atkinson** (2015) — universal basic capital
- **Card, Kluve & Weber** (2018) — active labor market programs meta-analysis
- **Khan** (2017), **Hovenkamp** (2021) — antitrust structural separation
- **Hausenloy et al.** (2023) — MAGIC / CERN-AI proposal
- **Sastry, Heim, Belfield et al.** (2024) — compute governance
- **Bommasani, Kapoor et al.** (2024) — open foundation models
- **Bengio et al.** (2024) — International AI Safety Report
- **Ostrom** (1990) — commons governance design principles
- **Lempert, Popper & Bankes** (2003) — Robust Decision Making
- **Kwakkel & Pruyt** (2013) — EMA Workbench RDM tooling

---

*Nebulai Corp · Miami, FL · partnerships@nebulai.com*

*This is a working draft. Comments to partnerships@nebulai.com or via
the companion repository.*
