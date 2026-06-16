# The Participatory AI Economy: Open Questions for the 2026–2036 Transition

*A structured-options working paper.*

> **Nebulai Corp Working Paper · Q2 2026 · Draft v0.2**
> *Companion code, data, and reproducibility: [`nebulaidigital/whitepaper`](https://github.com/nebulaidigital/whitepaper)
>  on branch `claude/economic-model-simulator-p2Bul`*

---

## How to read this paper

This paper does *not* advocate a single policy package for the AI economic
transition. It does the more useful thing: it **identifies the genuine policy
questions, lays out the live options under each question with the
evidence for and against each, and documents the simulation pipeline that
produced the evidence so that readers can stress-test every claim**.

Each question is presented as:

- **The question** — what's actually being decided
- **Why it matters** — the stakes and the constituencies affected
- **Option A / B / C** — the live policy alternatives
- **Evidence** — empirical analogs, simulation results, and known
  limitations of each option
- **What would change the answer** — the specific parameter values
  under which one option overtakes another
- **▶ Reproduce** — the exact command to regenerate the evidence

We make no recommendation between options. We commit to documenting
the conditions under which each option dominates, so that policymakers
applying their own priors can reach defensible conclusions.

The methodology is fully described in `paper/sections/09_methodology.md`;
the limitations in `paper/sections/10_limitations.md`; the empirical
analogs that anchor every effect size in `EMPIRICAL_ANALOGS.md`; the
pre-registered hypothesis list in
`preregistration/2026Q2_preregistration_v1.md`; the runnable simulation
pipeline in `src/`.

---

## Why this format

A traditional policy paper advances one set of recommendations and
defends them. That format is useful when the analyst has high
confidence in a single best answer and is willing to bear the
adversarial-review cost of defending it.

For the AI economic transition in 2026, neither condition holds:

- The defensible confidence level on any specific policy package is
  modest. The Q1 2026 baseline shifted under the open-weights inversion
  and Stargate-scale capital. Effect sizes are first-pass estimates.
  AGI emergence is unmodeled. The Lucas critique applies.
- The constituencies disagree on objectives. A paper arguing one answer
  pretends to settle disagreements that are genuinely substantive.

The structured-options format makes the disagreement explicit, locates
it precisely (which parameter, which constituency, which scenario), and
gives the reader the tools to apply their own priors. It also makes the
paper much harder to dismiss: a critic must engage the structure of the
question, not just attack a conclusion.

This is how Brookings policy briefs, RAND analyses, IMF Article IV
consultations, and the IPCC assessment reports treat genuinely
contested questions.

---

# Part I — The Status Quo Questions

## Question 1. How concerned should we be about the status quo trajectory?

**The question.** If no new framework is adopted and the Q1 2026
regulatory mosaic continues, what does 2036 look like, and is that
acceptable?

**Why it matters.** The level of concern about the do-nothing trajectory
sets the bar for how disruptive a policy response can be politically
justified. If the trajectory is acceptable, no response is needed; if it
is unacceptable, even costly interventions clear the bar.

### Option A. The trajectory is bad enough to require structural intervention

**Position.** Top-1% wealth share rising from 30% to ~33–36%, labor
share falling from 56% to ~51%, median household real income flat or
declining, substitute-worker employment falling 18% of pre-AI roles by
2036. Geopolitical degradation continues. This trajectory is
politically destabilizing on its own terms and economically unjust by
most distributive priors.

**Evidence.**
- Status-quo trajectory in `BASELINE_2026.md` §3, calibrated against
  Acemoglu 2024 (NBER WP 32487), DLEU 2020, Saez-Zucman 2016, BEA, IMF
  WEO. Figure 1 (`paper/figures/fig01_baseline_trajectory.png`).
- Historical analog: 1970–2020 US labor share decline from 65% to 56%
  produced documented political backlash (Case-Deaton "deaths of
  despair"; populist coalitions in 2016, 2024). Continuing the decline
  by 5–10pp over 11 years compresses the timeline.
- IMF WEO Oct 2025 explicitly warns about distributive consequences of
  AI productivity gains.

### Option B. The trajectory is bad but manageable with incremental policy

**Position.** Each quantitative shift is concerning but matches or is
slower than 1980–2020 trends; political institutions have absorbed
larger distributive shifts (e.g., the 1980–2000 inequality rise) without
collapse. Existing AI Safety Institute infrastructure, EU AI Act, US AI
executive orders, BIS export controls — these constitute meaningful
incremental policy already. The Q1 2026 baseline is not "Patchwork" in
the abstract chat-session sense; it is an active regulatory mosaic.

**Evidence.**
- BASELINE_2026.md §2.4 documents the active regulatory regime —
  EU AI Act in force, US AISI capability evaluations, Bletchley → Seoul
  → Paris coordination.
- Acemoglu 2024 base scenario shows distributive shifts within historical
  range; not a discontinuity.
- Stansbury-Summers (2020) attribute most labor-share decline to
  declining worker power rather than to inevitable technology; incremental
  labor-law reform is a tractable response.

### Option C. The trajectory is fine; AI productivity gains will lift all boats

**Position.** Counterfactually, the AI productivity boost (Acemoglu
2024 baseline +1–2pp/yr) compounds enough to maintain real-income gains
across deciles. Welfare per capita rises substantially even if the
wealth distribution doesn't. Historical analog: technology transitions
since 1700 have raised real wages despite producing severe transitional
inequality; this is no different.

**Evidence.**
- Aghion-Jones-Jones (2017) and Brynjolfsson-Li-Raymond (2023): empirical
  productivity boosts at the firm and worker level.
- Goldman Sachs Research scenarios (Briggs-Kodnani 2023): cumulative GDP
  growth +22 to +28% over 2025–2036 in the central case.
- Historical: 1800–2020 real wages rose >10× despite Marx's prediction.

### What would change the answer

- If observed top-1% wealth share *fell* in 2024–2026 (it didn't), Option
  C strengthens.
- If AI productivity growth is empirically <0.5%/yr (Acemoglu 2024 low
  scenario), Option B strengthens.
- If 2024–2026 median household real income falls more than 3% (not
  observed but possible by 2027 if AI displacement accelerates), Option
  A strengthens.

> **▶ Reproduce.** `make baseline` regenerates the Q1 2026 trajectory.
> The historical backtest (2015–2025) reproduces observed BLS / SCF /
> DLEU / BEA values exactly. `python -c "from src.core import
> BilateralSimulator; print(BilateralSimulator().run().to_dataframe())"`
> dumps the full trajectory for inspection.

---

## Question 2. What does the 2026 open-weights inversion mean?

**The question.** Through 2024, frontier AI capability was concentrated
in closed-weights US labs (OpenAI, Anthropic, Google DeepMind, Meta).
Since Q4 2024, Chinese frontier labs (DeepSeek, Qwen, GLM, MiniMax) have
released open-weights models at or near frontier capability. Does this
change the policy calculus?

**Why it matters.** Pillar 5 of the original framework (open-weights
mandate) was designed for a world where the US held closed-weights
dominance; mandating openness was supposed to dampen US AI rents.
Under inversion, mandating openness may instead transfer US capability
to Chinese ecosystem, without producing the intended markup compression.

### Option A. The inversion makes Pillar 5 backfire

**Position.** A US open-weights mandate now gives away US frontier
capability to a Chinese ecosystem already optimized to integrate and
extend it. US AI labs lose their value capture; Chinese labs and US
compute providers (hyperscalers) capture the rents the mandate was
supposed to address. Net effect on US workers and consumers is negative
or neutral; net effect on US-China strategic competition is unambiguously
negative.

**Evidence.**
- DeepSeek V3 / R1 technical reports + the rapid downstream-application
  ecosystem they enabled.
- Bommasani-Kapoor et al. (2024) "Considerations for Governing Open
  Foundation Models" — risks of asymmetric openness regimes.
- Open-source software history: when one side opens and another doesn't,
  the closed side captures the value (Linux vs. proprietary Unix is the
  inverse case; here the analogy runs the other way).
- Hypothesis 1 in the pre-registration (PREREGISTRATION.md §3) explicitly
  tests this; preliminary simulation finding is consistent with Option A.

### Option B. The inversion makes Pillar 5 unnecessary

**Position.** Chinese open-weights releases are already doing what the
framework's Pillar 5 was designed to do — eroding frontier-AI markups
via competitive pressure. Add-on US policy would be redundant or
incremental. Pillar 5 can simply be removed; the open-weights inversion
is the policy intervention, just delivered by China rather than the US.

**Evidence.**
- US frontier model API prices fell 40–70% in the six months after
  DeepSeek R1 release (Q1 2025 → Q3 2025). This is the markup compression
  Pillar 5 was supposed to produce; it happened without US policy.
- Kapoor-Bommasani et al. (2024) on open foundation models' downstream
  impact.
- DLEU markup trajectory in 2025–2026: AI sector markups flat to falling,
  vs. continuing growth in other sectors.

### Option C. Replace Pillar 5 with a stronger mechanism

**Position.** The inversion doesn't make the underlying problem
(concentrated AI capability) go away — it relocates it. China captures
the value Pillar 5 was supposed to spread. The right response is a
*stronger* mechanism that addresses concentration at the source:
build public open-frontier capability (Package C, CERN-AI), structurally
separate the AI value chain (Package D, structural separation), or
mandate compute access (Package D, common-carrier).

**Evidence.**
- Hausenloy-Miotti-Dennis (2023) MAGIC proposal: global public lab
  produces public-good frontier capability immune to commercial
  concentration.
- Khan (2017), Wu (2018), Hovenkamp (2021): structural separation
  produces sustained competitive effects.
- CERN historical performance: 24 member states, 70 years, zero
  defections, $1.5B/yr budget produced LHC and Higgs discovery.

### What would change the answer

- If US-China cooperation propensity (RDM parameter) is high enough to
  enable a joint open-frontier consortium, Option C dominates.
- If Chinese open-weights capability continues to *exceed* US frontier
  capability through 2028, Option B dominates.
- If political infeasibility of CERN-AI or structural separation is
  binding, the framework is stuck with Pillar 5 backfire (Option A) or
  removal (Option B).

> **▶ Reproduce.** Comparison of all three options is in the RDM sweep:
> ```bash
> python scripts/run_rdm.py --scenarios 2000 --metric us_markup_2036
> ```
> Package C (CERN-AI) regret on markup is reported; lower regret indicates
> stronger markup compression. Pillar 5 in isolation: inspect
> `src/packages/nebulai_six.py:PILLAR_5_OPEN_WEIGHTS`.

---

# Part II — The Architectural Questions

## Question 3. Should the framework redistribute AI's gains, or shape what AI is built for?

**The question.** Two intellectual lineages compete for primacy in
serious AI policy thinking. The Korinek / Saez-Zucman / Atkinson school
argues for redistributing AI's gains (UBI, wealth tax, sovereign
equity, AI tax). The Acemoglu-Johnson school argues for shaping AI's
development direction toward human-complementary rather than
human-substitute applications.

**Why it matters.** Most policy packages can be located on this axis,
and they imply substantially different agency structures: redistribution
puts agency in Treasury / IRS / sovereign-fund managers; direction-shaping
puts agency in procurement / NSF / standard-setting bodies. Different
constituencies, different vulnerabilities, different effects.

### Option A. Primarily redistribute (Package E direction)

**Position.** AI is fundamentally a productivity shock; the optimal
response is to capture the productivity gains via tax and distribute
them broadly. Mechanisms: UBI (Y Combinator OpenResearch 2024;
Marinescu 2018), wealth tax (Saez-Zucman 2019), Universal Basic Capital
(Atkinson 2015; Sherraden 1991), care economy expansion. Sidesteps the
hard problem of trying to direct AI development; just captures and
redistributes the value.

**Evidence.**
- Package E in the simulation: Direct Redistribution dominates 100% of
  RDM futures on top-1% wealth share reduction and median household
  income.
- Cross-class welfare matrix: every decile in every country strictly
  better off under Package E (Figure 3).
- Alaska PFD precedent: distributive transfers from natural-resource
  rents have proven politically durable for 40+ years.
- Empirical analogs (`EMPIRICAL_ANALOGS.md` §1.2, §2.1) have actual
  measured effects.

**Counter-evidence.**
- UBI of $1,200/month requires ~6% of GDP in transfers (mechanical from
  $14,400 × 250M adults / $25T GDP). Politically and fiscally challenging.
- Direct Redistribution does not address market structure: AI sector
  concentration continues regardless. Long-term concern.
- Substitute workers lose their *role*, not just their income; redistribution
  doesn't address meaning-of-work concerns (cf. Case-Deaton).

### Option B. Primarily shape direction (Package F direction)

**Position.** AI is plastic; we can choose to build it as labor
*complement* rather than labor *substitute*. The mechanism: directed
public R&D (DARPA model), federal procurement preference, worker
codetermination on AI deployment (German Mitbestimmung model), targeted
antitrust. Acemoglu-Johnson 2023 *Power and Progress* is the intellectual
basis.

**Evidence.**
- Package F (Build-Different-AI) wins 100% of RDM futures on real GDP
  growth (productivity boost from labor-augmenting AI is genuine).
- Historical: DARPA-directed R&D produced GPS, Internet, drones (~2–4×
  ROI per Mazzucato 2013).
- German Mitbestimmung (Jäger-Schoefer 2021) shows smoother automation
  transitions with worker codetermination.
- Procurement is real leverage: ~$700B/yr federal spending, with
  documented shaping effects (Buy American Act, FedRAMP).

**Counter-evidence.**
- AI R&D is hard to direct in practice. The same model often serves
  both complement and substitute applications.
- US labor-law structure makes worker codetermination politically
  hard to legislate (unlike Germany).
- Package F shows positive but small distributional effects in the
  cross-class matrix; doesn't address inequality directly.

### Option C. Do both (Package B, C, G direction)

**Position.** The framework's six pillars (and the CERN-AI / Game-Theoretic
alternatives) attempt to do both: sovereign equity and AI tax for
redistribution, public infrastructure and labor-augmenting reskilling
for direction. Conditional on coordination, this is the politically
realistic synthesis.

**Evidence.**
- Package B, C, G in the simulation all produce positive effects on both
  distribution and growth, though weaker than Package E on distribution
  alone and weaker than Package F on growth alone.
- Cross-class matrix: B, C, G all meet *non-negative* median-voter
  sufficiency in every decile (no decile worse off) but do not meet
  *strictly-positive* sufficiency (top deciles experience zero gain).

**Counter-evidence.**
- "Do both modestly" is dominated on each individual dimension by the
  specialized packages.
- Political coalition for hybrid packages is harder to assemble than
  for single-issue packages (you need more constituencies to all not
  veto).

### What would change the answer

- If UBI has stronger empirical effects than the Marinescu 2018 range
  suggests, Option A strengthens.
- If directed R&D can in fact predictably shape AI development direction
  (currently uncertain), Option B strengthens.
- If political feasibility of single-issue maximalism is low, Option C
  is the realistic-middle answer.

> **▶ Reproduce.** Compare packages E, F, B, C, G directly:
> ```bash
> python scripts/run_packages.py
> python -m src.analysis.chart_builders --fig 3  # cross-class welfare
> python scripts/run_rdm.py --scenarios 2000 --metric us_median_income_2036
> python scripts/run_rdm.py --scenarios 2000 --metric us_real_gdp_growth
> ```

---

## Question 4. How should AI sector rents be addressed?

**The question.** Frontier AI rents are concentrated in ~5 US labs,
~5 Chinese labs, ~3 hyperscaler cloud providers, and a handful of chip
designers/foundries. What is the right intervention point?

**Why it matters.** Different intervention points have different
political feasibility, different international-coordination requirements,
and different time-to-effect profiles.

### Option A. Open weights mandate (original Pillar 5)

**Mechanism.** Mandate open release of frontier model weights above a
capability threshold. Dampen AI sector markup growth.

**Evidence for.**
- Open source software economics (LibreOffice/Office, Linux/Unix):
  30–50% margin erosion in competitive markets.
- Reversible if calibrated carefully.

**Evidence against.**
- Open-weights inversion (Q1 2026): US closed, China open. Unilateral
  mandate transfers value to China.
- Weights cannot be retracted (irreversible mechanism in a contested
  geopolitical environment).
- Hypothesis 1 in PREREGISTRATION.md tests this; preliminary result is
  that Pillar 5 backfires under current conditions.

### Option B. Public frontier lab (CERN-AI / MAGIC, Package C)

**Mechanism.** Multilateral public lab building open-weights frontier
models at or near private-lab capability. Output is public; private rents
compress at the source.

**Evidence for.**
- CERN historical analog: 70 years, 24 members, zero defections, public
  scientific output.
- Solves open-weights inversion at the source (public open frontier
  eliminates US/China asymmetry).
- Hausenloy-Miotti-Dennis 2023 MAGIC proposal; Bengio et al. 2024 risk
  governance framing.
- Package C in the simulation dampens markup more than Package B.

**Evidence against.**
- Budget: $30B/yr from 12-country consortium ($2.5B/country) is
  politically ambitious but feasible (CERN budget is ~$1.5B/yr).
- AI is more strategic than particle physics; CERN's no-defection track
  record may not transfer.
- Coalition formation: requires international coordination.

### Option C. Antitrust structural separation (Package D)

**Mechanism.** Sherman Act § 2 + DMA-style obligations: model labs ≠
cloud providers ≠ application-layer firms. Three layers separately owned.

**Evidence for.**
- AT&T 1982 breakup precedent: telecom prices fell 40% over decade,
  produced Internet/mobile.
- Domestic implementation; no international coordination required.
- Khan (2017), Wu (2018), Hovenkamp (2021) intellectual basis already
  influencing FTC enforcement.
- Package D in the simulation dampens markup substantially.

**Evidence against.**
- US Supreme Court precedent on structural relief is uncertain post-
  Microsoft 2001.
- AT&T was a regulated natural monopoly; AI labs aren't. Mechanism may
  not transfer.
- Compliance cost on hyperscalers ~1–3% of revenue; political opposition
  from incumbents.

### Option D. Compute tax (Package D)

**Mechanism.** Tax measured per training-run FLOPs above threshold.
Carbon-tax-style Pigovian incidence on compute consumers.

**Evidence for.**
- Carbon tax precedent: 10–30% reduction in taxed-emission intensity
  (Sterner 2007).
- Compute is the actual chokepoint (~5 hyperscalers, ~3 chip designers).
- Domestic implementation feasible.

**Evidence against.**
- Compute tax may slow AI productivity gains (welfare cost) more than it
  produces redistributive benefit.
- Incidence falls on AI consumers if compute providers can pass through;
  potentially regressive.
- No real-world precedent at scale.

### What would change the answer

- If multilateral coordination is achievable (US+EU+JP+KR+CA+AU+IN
  willingness), Option B (CERN-AI) becomes feasible and dominates.
- If antitrust law/political infrastructure is favorable, Option C
  (structural separation) is domestic-feasible.
- If neither, Option A (open-weights) backfires and Option D (compute
  tax) becomes the politically-tractable lever.

> **▶ Reproduce.** Compare options as policy packages:
> ```bash
> python -c "
> from src.core import BilateralSimulator
> from src.packages import NEBULAI_SIX, CERN_AI, COMPUTE_CENTRIC
> sim = BilateralSimulator()
> for pkg in (NEBULAI_SIX, CERN_AI, COMPUTE_CENTRIC):
>     df = sim.run(package=pkg, coalition_share=0.7, cn_cooperation=0.5).to_dataframe()
>     print(f'{pkg.code}: markup 2036 = {df.loc[2036, \"us_markup\"]:.4f}')
> "
> ```

---

## Question 5. How much should sovereign equity participate?

**The question.** Pillar 1 of the original framework specifies sovereign
fund acquisition of new top-decile AI capital. The original calibration
was 10% acquisition fraction. Is this the right magnitude?

**Why it matters.** Sovereign equity participation is the framework's
most distinctive structural mechanism. Acquisition fraction directly
determines fund AUM, dividend yield to the public, and political
feasibility (because larger fractions are more disruptive to current
owners).

### Option A. Small participation (~5%)

**Position.** Minimize political opposition from current capital owners;
demonstrate concept; expand later if successful.

**Evidence for.**
- Norway GPFG started with modest stakes (1990s); grew to today's
  ~1.4% global average ownership over 30 years.
- Lower acquisition reduces cost-of-equity premium per stake (Pillar 1
  effect on AI lab cost of capital).
- Reversible if program is unwound politically.

**Evidence against.**
- 5% generates ~$50–100B/yr fund AUM at Stargate-scale capital. Modest
  dividend yield to public (~0.1% of GDP).
- Insufficient to address concentration meaningfully on 10-year horizon.

### Option B. Original calibration (~10%)

**Position.** The original framework's specification. Balanced between
political feasibility and distributive impact.

**Evidence for.**
- Default RDM calibration shows positive welfare effect, modest cost-of-
  equity premium.
- Norway GPFG analog scales: ~$300B fund AUM by year 10 in framework
  simulation.

**Evidence against.**
- Pre-2026 baseline. State-capital concentration since (Stargate, EU
  InvestAI) suggests this is below the new feasible frontier.

### Option C. Larger participation (~20–25%)

**Position.** State-affiliated capital already dominates new AI investment
flows in 2026 (Stargate, EU InvestAI, French €109B, Saudi HUMAIN, Chinese
state-directed). At 20%+, the sovereign fund becomes a real co-owner of
frontier capability with meaningful dividend yield.

**Evidence for.**
- Q1 2026 baseline: state-affiliated capital is the majority of new AI
  capex. 20% sovereign acquisition is *less disruptive* than the same
  number would have been in 2024.
- Singapore Temasek precedent: large equity stakes in domiciled firms,
  14% TSR over 50 years.
- Annual dividend at 20% scale: ~0.5–1% of GDP per capita.

**Evidence against.**
- Cost-of-equity premium scales: roughly linear at +25–100 bps per 10%
  acquisition (high uncertainty). At 20%, financing AI development
  becomes meaningfully more expensive.
- Capital flight elasticity (Bach 2014; Brülhart 2022): at higher
  acquisition rates, mobile capital fraction increases.
- Political opposition from current shareholders is materially stronger.

### What would change the answer

- If empirical cost-of-equity premium per acquisition is at the low
  end (~25 bps), Option C is more attractive.
- If capital-flight elasticity is at the high end (Bach 2014 range),
  Option A or B is required to avoid base erosion.
- If state-affiliated capital share of new AI capex falls below 30%
  by 2028, Option C is less feasible (less of the target asset class
  is state-anchored).

> **▶ Reproduce.** Edit `src/packages/nebulai_six.py:PILLAR_1_SOVEREIGN_EQUITY`
> `sovereign_acquisition_fraction` and rerun. Sensitivity sweep:
> ```bash
> python -c "
> from src.core import BilateralSimulator, SimulatorConfig
> from src.packages.base import PolicyLever, PolicyPackage, LeverTarget
> from src.packages.nebulai_six import PILLAR_1_SOVEREIGN_EQUITY
> # ...modify acquisition_fraction and re-run...
> "
> ```

---

## Question 6. What role should international coordination play?

**The question.** Multiple framework pillars (compute governance, AI tax,
capability disclosure, CERN-AI) require international coordination above
specified coalition thresholds. Should coordination be a *precondition*
for adoption, an *accelerator* during adoption, or a *late-stage layer*
added after domestic implementation?

**Why it matters.** Coordination is genuinely hard. Treating it as a
precondition risks paralysis; treating it as a late-stage layer risks
fragility (e.g., capital flight before coordination establishes).

### Option A. Coordination as precondition

**Position.** Don't implement Pillars 1, 5, 6 until OECD-style
coordination is established. Otherwise capital flight, tax-base erosion,
and competitive disadvantage make unilateral implementation backfire.

**Evidence for.**
- Capital flight elasticity literature (Bach 2014; Brülhart 2022):
  unilateral wealth taxes have produced real base erosion historically.
- The open-weights inversion: unilateral US action without coordination
  empirically backfires (Hypothesis 1 in PREREGISTRATION.md).
- Hypothesis 3 in PREREGISTRATION.md: there exists a coordination
  threshold below which Package B underperforms Package A.

**Evidence against.**
- Coordination has never preceded major reform. Bretton Woods, OECD
  Pillar 2, EU AI Act all followed unilateral leading-jurisdiction
  initiatives.
- Treating it as precondition means waiting indefinitely.
- Coordination is partially substitutable across pillars (e.g., domestic
  antitrust doesn't require it).

### Option B. Coordination as accelerator

**Position.** Implement Pillars 4, 6 domestically; engage OECD-style
coordination in parallel; expand coordination-dependent pillars as
coalition forms. This is the "leading jurisdiction" model.

**Evidence for.**
- EU AI Act precedent: unilateral EU adoption produced de facto global
  standard via Brussels effect.
- OECD Pillar 2 minimum tax: US initiation followed by 140-jurisdiction
  acceptance within 24 months.
- Coalition test in PREREGISTRATION.md Hypothesis 10: breakeven thresholds
  for coordination-dependent levers are typically achievable below the
  G7-plus coalition share (0.70).

**Evidence against.**
- Brussels effect requires market size; AI is more concentrated.
- Requires honest staging discipline; political incentive is often to
  declare coordination *now* and not actually pursue it.

### Option C. Coordination as late-stage layer

**Position.** Domestic implementation first (Pillars 1, 4, 6 within one
jurisdiction); international coordination layered on later as adoption
spreads.

**Evidence for.**
- Most policy innovations historically diffuse this way.
- Domestic implementation is faster and produces evidence-base for
  coordination.

**Evidence against.**
- Capital flight risk is highest in this regime. Empirical literature
  suggests it can erode the policy's base before coordination establishes.
- Coordination-dependent pillars (5, 3) cannot be implemented at all in
  this sequence until late.

### What would change the answer

- If capital flight elasticity is low (Brülhart 2022 range), Option C
  is feasible.
- If high (Bach 2014 range), Option A may be required.
- If the leading jurisdiction is large enough (US + EU together), Option
  B becomes the natural answer.

> **▶ Reproduce.** Hypothesis 3 (cooperation threshold) sweep:
> ```bash
> python -c "
> from src.core import BilateralSimulator
> from src.packages import NEBULAI_SIX
> sim = BilateralSimulator()
> for theta in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
>     df = sim.run(package=NEBULAI_SIX, coalition_share=0.7, cn_cooperation=theta).to_dataframe()
>     print(f'theta={theta}: US median income 2036 = {df.loc[2036, \"us_median_income\"]:.2f}')
> "
> ```

---

## Question 7. Who pays — and via which mechanism?

**The question.** All redistribution packages require revenue. Sovereign
equity, AI tax, wealth tax, compute tax, and inheritance tax all reach
different bases with different incidence patterns. Which combination?

**Why it matters.** The revenue mechanism determines incidence (who
ultimately bears the cost), political feasibility, base erosion risk,
and revenue stability.

### Option A. AI sector value-added tax (Pillar 6 / Package C, G)

**Mechanism.** 3–8% on AI sector revenue. OECD-coordinated to prevent
base erosion.

**Incidence.** Falls on AI sector profits (closely held) plus partial
pass-through to AI service prices (incidence on consumers).

**Revenue.** ~0.5% of GDP at 3% rate, ~1.0–1.5% at 5–8% rate.

**Evidence.** OECD Pillar 1/2 framework is the natural coordination
mechanism. Digital services taxes (3% in multiple jurisdictions) have
been implemented successfully.

### Option B. Compute tax (Package D)

**Mechanism.** Per-FLOPs training run tax above threshold. Pigovian
incidence on compute consumers.

**Incidence.** Falls primarily on frontier AI labs (which buy compute);
partial pass-through to AI service prices.

**Revenue.** ~0.6% of GDP at $100/PFlop-day threshold.

**Evidence.** Carbon tax precedent — Pigovian taxes work but require
threshold tuning.

### Option C. Wealth tax (Package E)

**Mechanism.** 2% above $50M net wealth, 3% above $1B (Saez-Zucman 2019
design).

**Incidence.** Falls on top-decile households.

**Revenue.** ~1.5% of GDP.

**Evidence.** Brülhart 2022 (Switzerland), Bach 2014 (France),
Norwegian wealth tax all provide real data. Behavioral elasticities are
nontrivial but manageable.

### Option D. Sovereign equity dividend yield (Pillar 1)

**Mechanism.** Sovereign fund acquires AI equity, earns returns,
distributes dividends.

**Incidence.** None on current owners (acquisition is at market price);
returns flow to public from AI productivity gains.

**Revenue.** 4% × fund AUM = ~0.2–0.5% of GDP at 10–20% acquisition
calibration.

**Evidence.** Alaska PFD precedent for distribution mechanics.

### Option E. Combine

**Position.** Multiple revenue streams reduce dependence on any single
elastic base. Sovereign equity + AI tax + wealth tax together produce
~3% of GDP, sufficient for UBI-scale transfers if desired.

**Evidence.** Diversified tax base is standard public finance principle.

### What would change the answer

- If political opposition to wealth tax is binding, Options A, B, D
  carry the load.
- If OECD coordination fails, Option C (domestic wealth tax) is the
  only nationally-implementable option.
- If compute providers can fully pass through compute tax, Option B is
  effectively a consumption tax (regressive); Options A, C, D preferred.

> **▶ Reproduce.** Revenue calculations and incidence assumptions are
> in `EMPIRICAL_ANALOGS.md` §3.5 (AI tax), §3.2 (compute tax), §1.1
> (sovereign equity), §1.3 (wealth tax). Each section documents the
> empirical analog and the effect-size confidence interval.

---

## Question 8. How fast should the rollout happen?

**The question.** Sequencing matters. Simultaneous activation of all
pillars maximizes near-term impact but locks in uncertain effects.
Sequential activation builds evidence but defers benefits.

**Why it matters.** Some pillars are irreversible (open weights cannot
be un-released); some are reversible (AI tax can be repealed). The
"option value" of starting with reversible mechanisms is real.

### Option A. Simultaneous activation

**Position.** Don't wait for evidence; the empty quadrant problem is
urgent. Activate all six pillars at year zero.

**Evidence for.**
- Urgency: labor share decline + top-1% concentration are accelerating;
  delay compounds.
- Coordination benefit: simultaneous activation establishes the regime
  as a coherent system.

**Evidence against.**
- Hypothesis 2 in PREREGISTRATION.md: sequential activation may produce
  higher expected welfare under uncertainty (option value).
- Irreversible pillars (5: open weights) lock in choices that may
  prove wrong.

### Option B. Reversibility-weighted sequential

**Position.** Order pillars by reversibility:
- Phase 1 (years 0–3): Pillars 4 (reskilling), 6 (AI tax). Both
  reversible. Gather evidence.
- Phase 2 (years 3–6): Pillar 1 (sovereign equity). Semi-reversible.
  Activate if Phase 1 leading indicators support feasibility.
- Phase 3 (years 6–10): Pillar 5 (open weights, redesigned if needed).
  Irreversible.

**Evidence for.**
- Option value under uncertainty: standard finance reasoning.
- Each phase establishes evidence base for the next phase.
- Political durability: small wins early build support for bigger moves.

**Evidence against.**
- Defers benefits.
- Risk that phase 1 evidence is misinterpreted (Hawthorne effect,
  short-run noise).

### Option C. Evidence-gated activation

**Position.** Like B, but with explicit leading indicators that must be
hit before next phase activates. If Pillar 4 reskilling doesn't show
target outcomes by year 3, don't proceed to Pillar 1.

**Evidence for.**
- Adaptive policy is standard in evidence-based policy literature.
- Builds in self-correction.

**Evidence against.**
- Defines "success" for each phase before learning what the right
  measure is.
- Political risk: opposition can move the goalposts.

### What would change the answer

- If empirical reskilling effectiveness (Card-Kluve-Weber) is at high
  end of range, Phase 1 success is likely → Option B works.
- If at low end, Phase 1 fails → either revise framework or proceed
  with caution.

> **▶ Reproduce.** Sequential vs. simultaneous comparison in code:
> ```bash
> python -c "
> from src.core import BilateralSimulator
> from src.packages.nebulai_six import NEBULAI_SIX, NEBULAI_SIX_SEQUENTIAL
> sim = BilateralSimulator()
> for p in (NEBULAI_SIX, NEBULAI_SIX_SEQUENTIAL):
>     df = sim.run(package=p, coalition_share=0.7).to_dataframe()
>     print(f'{p.name}: US median income 2036 = {df.loc[2036, \"us_median_income\"]:.2f}')
> "
> ```

---

# Part III — The Structural Questions

## Question 9. What is the right scope: bilateral, frontier-coalition, or universal?

**The question.** A US-only framework is feasible but vulnerable to
capital flight. A frontier-coalition framework (US + EU + Japan + Korea +
UK + Canada + Australia) addresses most concentrated AI capability. A
universal framework includes the Global South. Which is the right
target?

**Why it matters.** Coordination cost scales with coalition size. Some
pillars work at small coalitions (antitrust); others require near-
universal (e.g., compute governance treaty).

### Option A. US-only (or US + EU)

**Position.** Start with the leading jurisdiction. Brussels-effect
diffusion handles the rest.

**Evidence.** EU AI Act precedent: unilateral adoption produced de facto
global standard.

### Option B. Frontier coalition (G7-plus)

**Position.** US + EU + Japan + Korea + Canada + Australia + UK +
India (if engaged). Covers ~70% of frontier compute. Sufficient for
coordination-dependent pillars; manageable coordination cost.

**Evidence.** Hypothesis 7 in PREREGISTRATION.md tests whether
frontier-only adoption captures most of the welfare. Preliminary
finding is qualified yes.

### Option C. Universal (G20 plus, including emerging markets)

**Position.** Include Global South to avoid two-tier outcomes and
preserve the adoption-equilibrium argument across all country tiers.

**Evidence.** Framework's adoption-equilibrium claim is that *every*
country tier's median voter benefits. Without universal scope, the
claim narrows.

**Counter-evidence.** Coordination cost; institutional capacity in
some emerging markets is limited.

### What would change the answer

- If frontier-only adoption captures >80% of universal-adoption welfare
  (Hypothesis 7 testable), Option B dominates.
- If <50%, Option C is required to preserve the framework's claims.

> **▶ Reproduce.** Currently the bilateral model captures only US/CN.
> Three-tier extension is Phase 7 of the project roadmap.

---

## Question 10. How should the framework engage with AI safety / catastrophic risk?

**The question.** The framework's pillars address distributive and
market-structure concerns. They do not address alignment, catastrophic
misuse, or AGI risk. Should they?

**Why it matters.** Bengio et al. 2025 *International AI Safety Report*
documents catastrophic risk pathways that the framework's pillars do not
mitigate. A serious AI policy paper in 2026 has to address how it
relates to that risk.

### Option A. Out of scope, deferred to AI Safety literature

**Position.** Bengio et al. 2025 covers safety. This paper is about
economics. Stay in lane.

**Evidence for.** Division of labor; economists shouldn't pretend to be
safety researchers.

**Evidence against.** Catastrophic safety failure invalidates every
economic projection. Cannot be cleanly separated.

### Option B. Capability disclosure pillar as bridge

**Position.** Add or extend Pillar 3 (international coordination) with
mandatory capability disclosure and pre-deployment evaluation tied to
the AISI Network. This bridges the framework into safety policy without
absorbing it.

**Evidence for.** Bletchley → Seoul → Paris infrastructure already
exists. Marginal extension is feasible.

**Evidence against.** Capability disclosure is a small piece of safety
governance.

### Option C. Full integration with AGI scenarios

**Position.** Scenario-plan for AGI emergence inside the framework.
Include policy responses to capability discontinuity.

**Evidence for.** Korinek 2024 "Scenarios for the Transition to AGI"
provides a template.

**Evidence against.** Scope explosion; risk of speculation overwhelming
empirical content.

### What would change the answer

- If AGI emergence becomes more concrete (Bengio AISI Report severity
  increases), Option C becomes required.
- If safety governance regimes (AISI Network) develop more rapidly,
  Option B is the natural bridge.

> **▶ Reproduce.** Capability disclosure modeled in Pillar 3
> (`src/packages/nebulai_six.py:PILLAR_3_INTERNATIONAL_COORDINATION`)
> and Package C, D, G. The framework does not currently model AGI
> emergence (declared limitation in `paper/sections/10_limitations.md`
> §4).

---

# Part IV — Methodology Documentation

## How the evidence was produced

This paper does not rely on the authors' judgment alone. Every claim of
the form "Option X under conditions Y produces outcome Z" traces to a
specific simulation run, with input parameters documented in
`src/packages/`, baseline calibration documented in `BASELINE_2026.md`,
and effect sizes documented in `EMPIRICAL_ANALOGS.md`.

The simulation is **pre-registered**. Ten specific hypotheses were
specified in `PREREGISTRATION.md` before any run was executed, with
explicit validation/falsification criteria. We commit to reporting
whatever the evidence shows.

The simulation uses **counterfactual deltas** rather than absolute
predictions. Each reported number is a difference between a policy
package and the Q1 2026 status-quo baseline. This is more accurate
than absolute prediction (the Lucas critique applies to levels but
partly cancels for deltas).

The simulation runs under **Robust Decision Making**: 1000+ parameter
combinations from documented uncertainty ranges are evaluated for every
package, and policy-regret surfaces are computed across the joint
parameter space.

The simulation passes a **backtest validation gate**: the 2015–2025
historical period is reproduced within ±2pp on key indicators. No
forward-looking output is treated as reportable until backtest passes.

The simulation is **reproducible** end-to-end in under a minute on
commodity hardware. Every figure in this paper is regeneratable from a
documented command.

Full methodology documentation: `paper/sections/09_methodology.md`.
Full limitations documentation: `paper/sections/10_limitations.md`.

---

## What this analysis cannot do

This paper is a structured options analysis, not a forecast or a
single-recommendation policy advocacy document. Specifically:

- It does not predict 2036 outcomes at point precision.
- It does not forecast whether China will cooperate.
- It does not predict US-China conflict probabilities.
- It does not model AGI emergence or alignment failure.
- It cannot tell you which option is best; it can tell you the
  conditions under which each option dominates.

These are honest limitations, documented in `paper/sections/10_limitations.md`.

---

# Part V — Reproducibility Protocol

## Quick start

```bash
# Clone, install, test, run
git clone https://github.com/nebulaidigital/whitepaper.git
cd whitepaper
git checkout claude/economic-model-simulator-p2Bul
pip install -e ".[dev]"
make test                              # 57 tests pass in ~15s
make baseline                          # Question 1 evidence
make packages                          # Questions 3, 4, 5 evidence
make rdm                               # Questions 2-8 RDM sweeps
python -m src.analysis.chart_builders  # All six figures
```

For section-by-section reproduction, see `paper/REPRODUCE.md`.

## How to engage with the analysis

1. **Read the paper.** Each question above has live options with
   evidence for and against.
2. **Form your prior.** Based on the evidence, which option seems
   most defensible to you?
3. **Edit the parameter that drives your concern.** All effect
   sizes are in `src/packages/*.py`; all uncertainty ranges are in
   `src/analysis/rdm.py:UNCERTAINTY_RANGES`.
4. **Re-run the analysis.** `make packages` and `make rdm` regenerate
   the comparisons with your modified parameters.
5. **Document your reasoning.** A comment in the parameter file is
   sufficient.

This is the engagement model: the framework is parameterizable; the
disagreements are locatable; the simulation is a discipline against
hand-waving.

## How to add a new option

If you believe an important policy option is missing from the analysis:

1. Add it as a new `PolicyPackage` in `src/packages/your_package.py`,
   following the pattern of existing packages.
2. Register it in `src/packages/registry.py`.
3. Add at least one test in `tests/test_packages.py`.
4. Run `make packages` and `make rdm` — it's automatically compared
   against all existing packages.
5. Document the empirical analogs in `EMPIRICAL_ANALOGS.md`.

The framework is designed to invite contestation, not to settle it by
authority.

---

# Part VI — The Open Decisions

The questions above generate live decisions that the authors of this
paper alone cannot resolve. We list them here, with the constituency
who would naturally decide each:

1. **Question 1 (Status quo concern level).** This is a political-economic
   priority decision; constituencies range from current capital owners
   (Option C) to displaced workers (Option A). The simulation provides
   evidence, not the priority.

2. **Question 2 (Open-weights inversion).** Empirically testable but
   politically contested. The simulation supports Option A (Pillar 5
   backfire) under the documented Q1 2026 baseline; revising the baseline
   could change the answer.

3. **Question 3 (Redistribute vs. shape direction).** Intellectual
   commitment. Korinek-Saez-Zucman tradition supports A; Acemoglu-Johnson
   tradition supports B. We have no preference between these.

4. **Question 4 (AI rents intervention point).** Live in current policy
   debate (FTC, Khan-Wu-Hovenkamp school). Probably resolved by
   institutional capacity and political coalition rather than by
   simulation.

5. **Question 5 (Sovereign equity magnitude).** Quantitative; we believe
   the 2026 baseline supports higher numbers than the original 10%, but
   the political-economic cost is contested.

6. **Question 6 (Coordination role).** Foreign-policy choice. The
   simulation provides evidence that unilateral adoption is feasible
   under Option B; outright coordination-first (Option A) probably
   produces paralysis.

7. **Question 7 (Revenue mechanism).** Public finance choice. Combined
   mechanism (Option E) is defensible; specific weighting is political.

8. **Question 8 (Rollout speed).** Reversibility analysis supports
   Option B (sequenced). Urgency-driven analyses support Option A.

9. **Question 9 (Coalition scope).** Diplomatic choice. Frontier-coalition
   (Option B) is the model's natural answer.

10. **Question 10 (Safety integration).** Out of this paper's scope; we
    refer to Bengio et al. 2025 *International AI Safety Report*. Option
    B (capability disclosure bridge) is the most that the framework
    naturally supports.

---

## Closing

This paper presents the AI economic transition as a set of structured
policy questions with live options. Each option has documented evidence;
each has documented limitations. The simulation pipeline enables every
claim to be stress-tested by replacing parameters with the reader's own
priors.

We do not advocate a specific package. We provide the structure that
makes principled disagreement possible.

For substantive engagement: clone the repository, run the simulations,
substitute your own priors, and report what you find. If your priors
produce results materially different from ours, the disagreement is
parameterizable — locate the parameter, document the disagreement, and
both views can be reported.

This is what serious policy research looks like in a domain where the
evidence is genuinely incomplete and the constituencies genuinely
disagree.

---

*Nebulai Corp · Miami, FL · info@nebulai.com*
*Companion repository: github.com/nebulaidigital/whitepaper*
*Working draft v0.2 · Q2 2026 · Comments welcome*

---

## Document index

- **This paper:** `paper/WHITEPAPER.md`
- **Methodology:** `paper/sections/09_methodology.md`
- **Limitations:** `paper/sections/10_limitations.md`
- **Reproducibility protocol:** `paper/REPRODUCE.md`
- **Empirical analogs (per lever):** `EMPIRICAL_ANALOGS.md`
- **Pre-registered hypotheses:** `preregistration/2026Q2_preregistration_v1.md`
- **Baseline calibration:** `BASELINE_2026.md`
- **Literature sources:** `SOURCES.md`
- **Project specification:** `CLAUDE.md`
- **Phase roadmap:** `ROADMAP.md`
- **Simulator core:** `src/core/simulator.py`
- **Policy packages:** `src/packages/`
- **Stress tests:** `src/stability/`
- **RDM pipeline:** `src/analysis/rdm.py`
- **Figure generation:** `src/analysis/chart_builders.py`
- **Test suite:** `tests/` (57 passing)
