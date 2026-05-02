# Empirical Analogs — Effect Sizes for Each Policy Lever

**Document version:** 1.0
**Date:** 2026-05-01
**Phase:** 1 (literature delta book)
**Cross-references:** `PREREGISTRATION.md`, `BASELINE_2026.md`, `SOURCES.md` addendum
**Status:** First-pass synthesis. Sections marked **needs deeper review** are
flagged for Phase 5 hostile-critique stage.

> **Purpose.** Every policy lever in `src/packages/` claims an effect size
> (the `parameter_changes` dict). For the simulation's results to be
> defensible, each effect size must trace to an empirical analog —
> a real-world program where similar mechanisms were measured. This
> document is the master reference for those analogs.
>
> **The discipline this enforces.** Without empirical anchoring, lever
> effect sizes are stipulated, not measured. With it, every reported
> simulation finding can be defended by pointing to the underlying
> empirical evidence. Where no empirical analog exists, that's stated
> explicitly so reviewers know the analysis is theoretical at that point.

---

## How to read this document

For each policy lever, this document provides:

1. **Lever specification** — exactly what the policy proposes
2. **Empirical analog(s)** — the closest real-world programs with measured outcomes
3. **Effect-size estimate with confidence interval** — central value plus P10/P90 from the empirical literature
4. **Mapping to simulator parameters** — how the effect size translates to the values in `src/packages/*.py`
5. **Limitations of the analogy** — where the transfer from analog to AI policy is imperfect

Effect-size values in `src/packages/*.py` should match the central values
documented here. Where they don't, that's a calibration drift to be fixed
or documented.

---

## Section 1: Capital and Wealth Distribution Levers

### 1.1 Sovereign Equity Acquisition (Pillar 1, Package B)

**Specification:** Public fund acquires 10% of new top-decile AI capital
annually; pays distributed dividend.

**Empirical analogs:**

- **Norway Government Pension Fund Global (GPFG)** — established 1990,
  current AUM ~$1.7T (Q1 2025), holds equity in ~9,000 firms globally
  with average ownership stake 1.4%. Annual real return 2014-2024:
  4.1% (target was 3%). Distributes 3% of fund value to government
  budget annually.
- **Alaska Permanent Fund** — established 1976, current AUM ~$80B,
  pays Permanent Fund Dividend (PFD) of $1,200-2,000 to every Alaska
  resident annually. PFD has been continuously paid since 1982 with
  political durability across multiple administrations.
- **Singapore Temasek Holdings** — sovereign wealth fund founded 1974,
  $389B AUM, takes large equity stakes in Singapore-domiciled firms.
  Annual TSR 1974-2024: 14% in SGD terms.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| Cost-of-equity premium per 10% acquisition | +50 bps | +25 bps | +100 bps | Sundaresan-Sushko 2014 (Norway GPFG); calibrated from listed-firm valuation studies |
| Annual real return on captured base | 3.5% | 2.0% | 5.0% | GPFG 30-year track record |
| Effect on top 1% wealth share over 10 years | -1.0pp | -0.3pp | -1.5pp | Inferred — requires structural model |
| Median household dividend (% of GDP/capita) | 0.5% | 0.2% | 0.8% | Alaska PFD ratio scaled to global GPFG-style |

**Mapping to simulator:** `sovereign_acquisition_fraction=0.10`,
`cost_of_equity_premium=0.005`, `dividend_rate=0.04` in
`src/packages/nebulai_six.py:PILLAR_1_SOVEREIGN_EQUITY`.

**Limitations of analog:**
- Norway GPFG holds *foreign* equities; the framework's Pillar 1 is for
  *domestic* AI capital. The political economy is meaningfully different —
  domestic acquisition triggers takings-clause concerns absent in foreign
  holdings.
- AI capital depreciates much faster (~22%/yr per McKinsey 2025) than
  the diversified equity portfolio GPFG holds. Fund returns may erode
  faster than the GPFG analog suggests.
- **Needs deeper review:** Saudi PIF and UAE MGX recent AI-specific
  acquisitions provide closer analogs but are too recent (2023-2025) for
  multi-year track records.

---

### 1.2 Universal Basic Capital (Package E, G)

**Specification:** $50K capital grant to every citizen at age 18 (or
$25K in Package C variant). Distributed via sovereign-managed portfolio
with vesting.

**Empirical analogs:**

- **UK Child Trust Fund (2002-2011)** — every UK child born 2002-2011
  received £250-500 government deposit at birth, with parental top-ups.
  ~6.3M accounts, average value at maturity ~£1,500. Discontinued in 2011
  for fiscal reasons; Conservative government argued cost-ineffective.
- **Singapore Baby Bonus** — cash grants and matched savings for parents
  of newborns. SGD 8,000-10,000 per child; integrated with Child
  Development Account.
- **Atkinson (2015) capital endowment proposal** — theoretical, but
  drawn from analysis of inheritance flow data and proposed at €10K per
  18-year-old, funded by inheritance tax reform.
- **Sherraden (1991) IDA programs** — Individual Development Accounts
  at small scale (Tulsa Saves, Saving for Education, Entrepreneurship,
  and Downpayment) showed 5-10% downstream wealth-building effect for
  participants vs. controls.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| Bottom 50% wealth share lift over 10 years | +1.2pp | +0.5pp | +2.0pp | Atkinson 2015 modeling + Sherraden IDA evidence |
| Top 1% wealth share reduction over 10 years | -0.5pp | -0.1pp | -0.8pp | Mechanical — small relative to total wealth |
| Cost as % of GDP (annual) | 0.4% | 0.2% | 0.7% | $50K × ~4M 18-year-olds × population share |

**Mapping to simulator:** `ubc_grant_per_capita=50000.0`,
`wealth_distribution_floor=0.012` in
`src/packages/direct_redistribution.py:UNIVERSAL_BASIC_CAPITAL`.

**Limitations of analog:**
- UK Child Trust Fund was small (£500), short-lived (8 years), and not
  designed as wealth-distribution policy. Effect sizes are not directly
  comparable to a $50K UBC.
- Sherraden IDA evidence is for participating families, not universal
  population. Selection effects may inflate effect estimates.
- **Genuinely novel proposal at $50K scale.** No existing program is
  close in magnitude.

---

### 1.3 Progressive Wealth Tax (Package E)

**Specification:** 2% on net wealth above $50M, 3% above $1B
(Saez-Zucman 2019 design).

**Empirical analogs:**

- **Norwegian wealth tax** — 0.85% on wealth above ~$170K; pre-2023
  rate was 1.1%. Has existed continuously since 1892. Behavioral elasticity
  estimate from administrative data: −0.3 to −0.6 (10% rate increase →
  3-6% reduction in declared taxable wealth).
- **Swiss wealth tax** — varies by canton (0.1%-1.0%); long history.
  Brülhart, Gruber, Krapf, Schmidheiny (2022) AEJ:Pol: behavioral
  elasticity ≈ −34, which is much larger than Norwegian estimates due to
  cross-canton mobility.
- **French ISF (1981-2017)** — 0.5%-1.5% on wealth above €800K-€1.3M.
  Bach, Bourdier, Bozio (2014) IPP: ~0.8% of taxable assets per year per
  pp of effective rate differential.
- **Spanish wealth tax** — 0.2%-3.5% on wealth above €700K, with regional
  variation. Recent reform (2022) added solidarity surcharge.
- **U.S. estate tax** — 40% above $13.6M exemption (2024). Different
  mechanism (one-time at death) but addresses same wealth-distribution goal.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| Tax base flight per pp differential | 0.005-0.008 /yr | 0.003 | 0.015 | Bach 2014 / Brülhart 2022 |
| Top 1% wealth share reduction (10 yr at 2%) | -1.5pp | -0.5pp | -2.5pp | Saez-Zucman 2019 modeling |
| Revenue as % of GDP | 1.5% | 0.8% | 2.2% | Saez-Zucman 2019 (US-specific) |

**Mapping to simulator:** `wealth_tax_marginal_top=0.03`,
`capital_flight_responsiveness=0.005` in
`src/packages/direct_redistribution.py:WEALTH_TAX_PROGRESSIVE`.

**Limitations of analog:**
- Cross-jurisdictional mobility for the US is much lower than for Switzerland
  (federal system, citizenship-based taxation). Brülhart estimates likely
  upper-bound for US.
- AI capital is more mobile than diversified portfolios — Hayek-style
  capital can flee to Singapore / UAE / Switzerland with low frictions.
- **Needs deeper review:** behavioral response specifically to wealth
  taxes on AI assets vs. diversified portfolios is unstudied.

---

### 1.4 Inheritance / Estate Tax Reform (Package E)

**Specification:** 50% above $5M, 70% above $50M; eliminate step-up
basis at death.

**Empirical analogs:**

- **U.S. estate tax pre-2001** — top rate 55% above $675K, raised
  modest revenue (~0.3% of federal receipts) but considered effective at
  reducing dynastic wealth.
- **U.K. inheritance tax** — flat 40% above £325K. Behavioral response:
  significant lifetime gifting and trust use; effective rate well below
  statutory.
- **Japanese inheritance tax** — top rate 55% above ¥600M. Has produced
  substantial estate-fragmentation effects across generations.
- **French succession tax** — graduated up to 60%, with significant
  lineage-based discounts.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| Top decile inheritance recirculation reduction | -40% | -20% | -55% | Piketty-Postel-Vinay-Rosenthal 2014 |
| Revenue as % of GDP | 0.5% | 0.2% | 0.8% | Historical U.S. + JEC analysis |
| Top 1% wealth share reduction (long-run, 25+ yr) | -2pp to -5pp | -1pp | -7pp | Piketty 2014 modeling; multi-generational |

**Limitations:** Most effects materialize over 25+ year horizons —
inheritance is intergenerational. The simulation's 2025-2036 window
captures only the leading edge of effects.

---

## Section 2: Labor and Income Levers

### 2.1 Universal Basic Income (Package E)

**Specification:** $1,200/month to all adults, unconditional.

**Empirical analogs:**

- **Y Combinator OpenResearch UBI Study (2024)** — first large-N US RCT.
  3,000 participants, 21 US states, $1,000/month for 3 years. Findings:
  modest reductions in labor supply (~2-4%), large improvements in
  reported wellbeing, no change in education enrollment, mixed financial
  health outcomes.
- **Stockton SEED (2019-2021)** — 125 residents, $500/month for 24
  months. Findings: full-time employment rose 12%; wellbeing and
  financial volatility improved markedly.
- **Kenya GiveDirectly** — long-term UBI ($22.50/month) in 295 villages.
  12-year program; ongoing. Findings: substantial business formation,
  income gains, no displacement of work effort.
- **Alaska Permanent Fund Dividend** — closest real-world analog.
  $1,000-2,000/yr to every Alaska resident since 1982. Jones-Marinescu
  (2022) NBER: no detectable employment reduction.
- **Finland Basic Income Experiment (2017-2018)** — 2,000 unemployed
  Finns received €560/month. Modest employment effects (+0.5% relative
  to control); large wellbeing improvements.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| Bottom decile income boost | +50% | +30% | +70% | Mechanical from $14,400/yr |
| Median household income boost | +10% | +5% | +15% | Mechanical, smaller relative |
| Labor supply reduction | -3% | -1% | -8% | Marinescu 2018 review |
| Cost as % of GDP | 6% | 5% | 8% | $1,200/mo × ~250M adults |

**Mapping to simulator:** `ubi_monthly_per_adult=1200.0`,
`transfer_funding_per_gdp=0.060`, `labor_supply_elasticity=-0.05` in
`src/packages/direct_redistribution.py:UBI`.

**Limitations of analog:**
- All large-N evidence is from finite-duration trials. Permanent UBI
  effects on labor supply could differ — Friedman/Hayek conjecture is
  larger reductions; behavioral economics suggests smaller. Open question.
- US-scale UBI ($14,400 × 250M adults = $3.6T/yr) requires funding
  mechanism — package combines wealth tax + AI tax + payroll tax base
  expansion. Funding feasibility is a separate analysis.

---

### 2.2 Active Labor Market Programs / Reskilling (Pillar 4)

**Specification:** Reskilling at scale for displaced substitute workers.

**Empirical analogs:**

- **Card, Kluve & Weber (2018)** — meta-analysis of 207 ALMP evaluations
  across 31 countries. Central finding: average effect on employment ~+5%
  in short run, +10% in medium run (2-3 years post-program). Large
  variation: training programs +5-15%, public employment programs ~0.
- **Trade Adjustment Assistance (US)** — Reynolds-Palatucci (2012)
  evaluation: +12% earnings effect for participants vs. matched controls.
- **German Kurzarbeit (short-time work)** — saved ~500K jobs in
  2008-2009 crisis per Brenke-Rinne-Zimmermann. Different mechanism
  (wage subsidy during downturn), useful as analog for displacement
  mitigation.
- **Heckman, LaLonde, Smith (1999)** — handbook chapter, foundational.
  Notes that average effects mask large heterogeneity; targeted programs
  (vs. universal eligibility) consistently outperform.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| Earnings boost for displaced substitute workers | +10% | +5% | +20% | Card-Kluve-Weber 2018 medium-run |
| Substitute-worker employment rate boost | +8% | +3% | +15% | CKW 2018 medium-run |
| Cost per participant | $8K | $4K | $20K | Heckman-LaLonde-Smith range |
| Substitute → complement skill conversion rate | 5% | 2% | 12% | Inferred from CKW participant tracking |

**Mapping to simulator:** `reskilling_earnings_effect=0.10`,
`epsilon_sub_shift=1.5`, `skill_mix_complement_shift=0.05` in
`src/packages/nebulai_six.py:PILLAR_4_RESKILLING`.

**Limitations of analog:**
- Most ALMP evidence is for cyclical unemployment, not structural
  displacement from technology. AI displacement is fundamentally different
  (skill-targeted, durable).
- Eloundou et al. (2023) suggests AI-substitute roles may not have nearby
  complement-substitute pairs to retrain into. CKW effect sizes may not
  transfer.
- **Needs deeper review:** GenAI-specific reskilling programs (e.g.,
  Anthropic Economic Index, Microsoft AI Skills Initiative) are too
  new for evaluation.

---

### 2.3 Care Economy Expansion (Package E, F)

**Specification:** Direct public investment to grow childcare, elder
care, mental health, education sectors.

**Empirical analogs:**

- **Quebec universal childcare** (1997-) — $7/day childcare. Lefebvre-
  Merrigan 2008: mothers' labor force participation +14pp; modest fiscal
  cost recovery via tax revenue from new workers.
- **Norway/Sweden universal eldercare** — public provision; Kjaer-Soerbye
  2017: fiscal cost ~3% of GDP, but sustained labor force participation
  for caregivers (mostly women).
- **U.S. expanded EITC** — Hoynes-Patel 2018: each $1K EITC raises
  pretax earnings of bottom-quintile families by ~$1.50.
- **NHS England care worker programs** — modest wage floor effects.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| Care-sector employment share boost over 10 yr | +5pp | +2pp | +8pp | Quebec + Nordic experience |
| Median wage in care sector | +10% | +5% | +18% | Sector-specific minimum + public funding |
| Cost as % of GDP | 3% | 1.5% | 4.5% | Nordic comparators |
| Substitute → complement skill shift | +8pp | +3pp | +15pp | Care work is AI-complement |

**Mapping to simulator:** `care_sector_employment_share=0.05`,
`median_wage_floor=0.10`, `skill_mix_complement_shift=0.08` in
`src/packages/direct_redistribution.py:CARE_ECONOMY_EXPANSION`.

---

### 2.4 Worker Codetermination (Package F)

**Specification:** German Mitbestimmung-style codetermination on AI
deployment in firms above 1,000 employees.

**Empirical analogs:**

- **German Mitbestimmungsgesetz (1976)** — board-level codetermination
  in firms above 2,000 employees. Jäger-Schoefer-Heining (2021) QJE:
  causal evidence of small effects on wages, modest reductions in
  managerial turnover, no measurable effects on profitability.
- **Nordic union representation** — substantial workplace voice with
  documented effects on automation adoption pace (Aghion-Antonin-Bunel
  2023): codetermined firms adopt automation more gradually with smoother
  workforce transitions.
- **U.S. UAW collective bargaining on EV transition (2023)** —
  contractual provisions governing automation deployment; too recent
  for outcomes evidence.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| Displacement speed dampening | -30% | -15% | -45% | Aghion et al. 2023 German evidence |
| Worker outside-option strength (ε_sub shift) | +1.4× | +1.1× | +1.7× | Mitbestimmung analyses |
| Effect on firm productivity | -2% | -5% | +2% | Jäger-Schoefer 2021 — null/small |

**Mapping to simulator:** `displacement_speed_dampening=0.30`,
`epsilon_sub_shift=1.4` in
`src/packages/build_different.py:WORKER_CODETERMINATION_AI_DEPLOYMENT`.

**Limitations of analog:**
- US labor law is structurally different from German — no formal works
  council requirement, no board-level worker representation. Implementation
  would require new legislation; effect sizes from Germany may not transfer.
- The AI-deployment-specific dimension is novel — even German Mitbestimmung
  doesn't have specific provisions for algorithmic decision-making.

---

## Section 3: AI Sector and Market Structure Levers

### 3.1 Open-Weights Mandate (Pillar 5, Package B)

**Specification:** Mandate open release of frontier model weights for
participating jurisdictions.

**Empirical analogs:**

- **Open source software economics** — Linux, LibreOffice, Apache,
  Postgres displaced commercial alternatives. Effect on commercial
  pricing: 30-50% margin erosion in directly-competitive markets
  (Lerner-Tirole 2002 review; updated literature).
- **DeepSeek V3 / R1 (2024-2025)** — Chinese-released open-weights
  models reaching GPT-4-class performance. Estimated effect on US
  frontier pricing: API prices fell 40-70% in 6 months following R1
  release.
- **Llama 2/3 (2023-2024)** — Meta's open-weight releases shifted
  market dynamics toward downstream-application competition.
- **Wikipedia vs. Encarta** — open-source displaced commercial
  encyclopedia entirely (~25 years).

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| AI markup growth dampening (universal mandate) | 40% | 20% | 60% | OSS literature midpoint |
| Open-weights inversion factor (Q1 2026) | 60% of dampening goes to compute layer / China | 40% | 80% | Speculative — Hypothesis 1 tests this |
| Markup compression on US frontier labs | -5 to -15% over 5 yr | -2% | -25% | Inferred from DeepSeek-API pricing |

**Mapping to simulator:** `ai_markup_growth_dampening=0.40` in
`src/packages/nebulai_six.py:PILLAR_5_OPEN_WEIGHTS`.

**Limitations of analog:**
- The open-weights inversion (China leads, US closed) is a 2025-2026
  phenomenon with no historical precedent. Pillar 5's effect under this
  configuration may be backwards from intent. **This is exactly what
  Hypothesis 1 tests** — see PREREGISTRATION.md.
- OSS analogs are for products with low marginal cost (software). AI
  inference has substantial marginal cost (compute), changing the
  competition dynamics.

---

### 3.2 Compute Tax (Package D)

**Specification:** Tax measured per training-run FLOPs above threshold.

**Empirical analogs:**

- **Carbon tax** — closest analog. Sweden, BC, EU ETS. Effect: 10-30%
  reduction in taxed-emission intensity per Sterner 2007 review. Tax
  incidence varies — energy-intensive industries pass-through to
  consumers.
- **Tobacco excise tax** — World Bank 2015 review: 10% price increase
  → 4-8% consumption reduction. High-income elasticity higher.
- **Norwegian petroleum special tax** — 78% above ordinary corporate
  rate. Industry-specific extraction tax, has not destroyed industry.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| Compute consumption reduction at $100/PFlop-day | -15% | -5% | -30% | Carbon tax elasticity analog |
| Revenue as % of GDP | 0.6% | 0.3% | 1.0% | Mechanical from $100/PFlop-day × global compute |
| Pass-through to AI service prices | 60% | 30% | 90% | Carbon tax pass-through estimates |

**Mapping to simulator:** `compute_tax_per_pflop_day=100.0` in
`src/packages/compute_centric.py:COMPUTE_TAX`.

**Limitations of analog:**
- Carbon tax is on a continuous-flow externality. Compute tax is on a
  discrete-event input (training run). Mechanism differs.
- AI productivity gains may dominate tax-induced compute reduction in the
  net welfare calculation. Compute tax could be net positive (Pigovian)
  rather than net negative (deadweight).

---

### 3.3 Compute Access Mandate / Common Carrier (Package D)

**Specification:** Hyperscalers must provide compute on non-discriminatory
terms; no bundled-equity deals.

**Empirical analogs:**

- **Telecom common-carrier regulation** (U.S. Title II, EU equivalent)
  — long history. AT&T 1934-1984 era, Computer Inquiries (1971-1986).
  Reduced exclusionary pricing; increased downstream innovation.
- **EU Digital Markets Act (2022)** — gatekeeper obligations including
  non-discriminatory access. Too early for effect estimates but
  documented compliance costs ~1-3% of revenue.
- **Open Internet / Net Neutrality** — Title II reclassification 2015,
  reversed 2018, reinstated 2024. Mixed evidence on investment effects.
- **Banking / financial market access** — Glass-Steagall structural
  separation produced clear competitive effects.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| Independent-lab compute access cost reduction | -40% | -20% | -60% | Common-carrier pricing analogs |
| AI lab market concentration (HHI) reduction | -10% | -5% | -20% | DMA early effects |
| Compliance cost on hyperscalers (% revenue) | 2% | 1% | 4% | DMA documented |

**Mapping to simulator:** `compute_access_premium_for_independents=-0.40`,
`ai_lab_concentration=-0.10` in
`src/packages/compute_centric.py:COMPUTE_ACCESS_MANDATE`.

---

### 3.4 Structural Separation of AI Value Chain (Package D, G)

**Specification:** Antitrust action: model labs ≠ cloud providers ≠
application layers. Three layers must be separately owned.

**Empirical analogs:**

- **AT&T 1982 breakup** — Modified Final Judgment; structural separation
  of long-distance from local. Effect: telecom prices fell 40% over
  decade; entry of MCI/Sprint/etc. Long-run innovation effects positive
  (Internet, mobile).
- **Microsoft 2001 antitrust settlement** — behavioral remedies, not
  structural. Less effective than AT&T precedent suggests.
- **Standard Oil 1911** — structural breakup. Largely successful at
  introducing competition.
- **Glass-Steagall (1933-1999)** — structural separation of investment
  and commercial banking. Effects mixed; repeal coincided with 2008
  financial crisis.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| AI markup growth dampening | 45% | 25% | 65% | AT&T post-divestiture pricing dynamics |
| AI sector HHI reduction | -20% | -10% | -35% | AT&T HHI changes 1984-1995 |
| Compute layer profit share cap | 15% | 10% | 20% | Common-carrier rate-of-return analogs |
| Innovation-rate effect | +10% downstream | +0% | +25% | AT&T Internet/mobile evidence |

**Mapping to simulator:** `ai_markup_growth_dampening=0.45`,
`ai_sector_concentration_shift=-0.20` in
`src/packages/compute_centric.py:STRUCTURAL_SEPARATION_AI_VALUE_CHAIN`.

**Limitations:** AT&T was a regulated natural monopoly; AI labs aren't.
Different starting structure. But the structural-separation principle
applies — the question is whether AI value chain has the same
modularity AT&T did (analysts disagree).

---

### 3.5 AI Tax (Pillar 6, Package C, G)

**Specification:** 3-8% on AI sector value-added, OECD-coordinated.

**Empirical analogs:**

- **OECD Pillar 1/2 minimum tax (2021-)** — global minimum corporate
  tax of 15%; effective for 140+ jurisdictions. Coordination mechanism
  works at scale. Revenue projections ~$150-200B globally.
- **Digital Services Taxes (DSTs)** — France (3%), UK (2%), Spain (3%),
  Italy (3%). Generally repealed under OECD agreement. Demonstrated
  feasibility of sector-specific taxation. Revenue ~0.05-0.10% of GDP
  per pp of rate.
- **Financial Transaction Tax (Tobin tax)** — proposed; partial
  implementation (UK stamp duty 0.5%; France 0.3%). Revenue collection
  feasible but base shrinks via avoidance.
- **Norwegian petroleum special tax** — analog above.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| Revenue as % of GDP at 3% AI tax rate | 0.5% | 0.3% | 0.8% | DST analogs scaled |
| Revenue as % of GDP at 6% AI tax rate | 0.8% | 0.5% | 1.5% | DST + scaling |
| Tax base flight (no coordination) | 30-50% | 20% | 60% | DST experience |
| Tax base flight (OECD coordination) | 5-10% | 2% | 15% | OECD Pillar 2 evidence |
| GDP drag (deadweight loss) | -0.05pp per pp tax | -0.02pp | -0.15pp | Standard tax efficiency literature |

**Mapping to simulator:** `ai_sector_tax_rate=0.03` (B) or `0.05` (C) or
`0.06` (G) across packages; `transfer_funding_per_gdp` set proportionally.

---

### 3.6 AI Liability + Mandatory Insurance (Package D, G)

**Specification:** Strict liability for harms from above-threshold AI
deployment; mandatory liability insurance.

**Empirical analogs:**

- **Price-Anderson Act (1957-)** — US nuclear operator liability +
  mandatory insurance. Has functioned for 70 years; combined private
  insurance pool ($16B) + federal backstop.
- **Environmental Superfund (CERCLA, 1980)** — strict, joint, and several
  liability for hazardous waste cleanup. Created multi-billion-dollar
  insurance market.
- **Auto liability insurance** — universal in 49 US states. Premium
  ~$1,200/yr per driver; reduces uninsured driving externality.
- **Medical malpractice insurance** — sector-specific, mandatory in many
  jurisdictions.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| Misuse/harm externality internalization | 60% | 40% | 80% | Price-Anderson + environmental Superfund |
| Insurance premium as % of training cost | 2% | 1% | 5% | Nuclear/environmental analogs |
| Effect on deployment decisions | Significant for risky systems; minimal for safe systems | — | — | Theoretical / qualitative |

**Mapping to simulator:** `ai_misuse_externality_internalization=0.60`
in `src/packages/compute_centric.py:AI_LIABILITY_INSURANCE` (and Package G).

**Limitations:** Defining the harm function for AI is much harder than
for nuclear (well-understood radiation) or environmental (well-understood
contamination). Insurance pricing requires actuarial models that don't
yet exist for AI.

---

## Section 4: International Governance Levers

### 4.1 CERN-AI Global Public Frontier Lab (Package C, G)

**Specification:** Multilateral public lab building open-weights frontier
models at or near private-lab capability. ~$30B/yr funding.

**Empirical analogs:**

- **CERN** (1954-) — 24 member states, current annual budget ~$1.5B.
  Produced Higgs boson discovery, LHC, World Wide Web. No defections in
  70 years. Per-capita member contribution ~$2/citizen.
- **ITER** (2006-) — international fusion reactor consortium. Budget
  ~$25B over 20 years, slow progress, demonstrates difficulty of large
  multilateral scientific projects.
- **International Space Station** (1998-) — survived US-Russia
  geopolitical breakdowns. Budget ~$3B/yr.
- **NIH** (US, but instructive scale) — $48B/yr budget; produces majority
  of basic biomedical research worldwide.
- **NSF NAIRR Pilot (2024-)** — $35M pilot of public AI compute
  infrastructure. Too small to be a direct analog; demonstrates concept.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| AI markup growth dampening (with parity capability) | 55% | 35% | 75% | CERN spillover effects + OSS analogs |
| Frontier capability diffusion rate | +20% | +10% | +35% | Open-source software diffusion analogs |
| Member-state participation rate | 70% (US, EU, JP, KR, CA, AU, UK, IN if engaged) | 50% | 90% | CERN historical participation rate |
| Annual budget feasibility | $30B/yr from 12-country consortium = $2.5B/country | — | — | NIH/CERN per-capita scaling |

**Mapping to simulator:** `ai_markup_growth_dampening=0.55`,
`frontier_capability_diffusion=0.20`, `public_funding_per_gdp=0.0015` in
`src/packages/cern_ai.py:CERN_AI_PUBLIC_LAB` (and Package G).

**Limitations:** CERN works because particle physics is non-strategic;
AI is highly strategic. Closer analog set: ITER (slow), ISS (survived
geopolitical breakdown), IAEA (verification regime). Mixed track records.

---

### 4.2 Compute Governance Treaty (Package C, G)

**Specification:** Treaty-grade compute monitoring + capability-threshold
agreements modeled on NPT + Wassenaar.

**Empirical analogs:**

- **Nuclear Non-Proliferation Treaty (1968-)** — 191 members. Works
  imperfectly (NK, Iran, Israel, India, Pakistan defected) but
  substantially limited proliferation. IAEA verification regime.
- **Wassenaar Arrangement (1996-)** — export controls on dual-use tech.
  42 members. Mixed enforcement.
- **Chemical Weapons Convention (1997-)** — OPCW verification with
  on-site inspections. Strong compliance.
- **Comprehensive Test Ban Treaty (1996-)** — never fully ratified
  (US, China, Iran, Israel, Egypt). Verification works for tests but
  not capability development.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| AI arms race intensity reduction | 30% | 15% | 50% | NPT-era nuclear arms race comparisons |
| Geopolitical stability index lift | +8 points | +3 | +15 | Theoretical / qualitative — Tier D in PREREG |
| Frontier compute concentration reduction | 10% | 5% | 20% | Wassenaar export-control effects |
| Verification feasibility | Achievable via fab inspection + power monitoring + customs | — | — | Heim, Sastry, Belfield et al. 2024 |

**Mapping to simulator:** `ai_arms_race_intensity=-0.30`,
`geopolitical_stability_index=8.0` in
`src/packages/cern_ai.py:COMPUTE_GOVERNANCE_TREATY`.

---

### 4.3 Mandatory Capability Disclosure + Pre-Deployment Eval (Package C, D, G)

**Specification:** Frontier training runs above compute threshold
register with AISI Network; pre-deployment evals required.

**Empirical analogs:**

- **FDA drug approval process** — pre-market clinical trial requirements.
  Substantially raises costs but improves safety. Time to market: 10-15
  years, $1-2B per approved drug. Has worked for 80+ years.
- **SEC public-company disclosure** — quarterly + annual reports.
  Functions despite incentive to obscure.
- **EU AI Act high-risk / GPAI obligations** (2024-) — already-implemented
  partial disclosure regime. Compliance cost estimates 1-3% of relevant
  revenue.
- **AISI Network publications** (UK, US, JP, etc.) — early evidence
  of voluntary cooperation; many frontier labs (Anthropic, OpenAI,
  Google DeepMind, Meta) participate.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| Capability disclosure compliance rate | 85% | 60% | 95% | FDA/SEC compliance rates |
| AI safety audit coverage | 80% of above-threshold systems | 50% | 95% | EU AI Act / AISI projections |
| Compliance cost (% of training run cost) | 3% | 1% | 8% | FDA/SEC compliance cost analogs |

**Mapping to simulator:** `capability_disclosure_compliance=0.85`,
`ai_safety_audit_coverage=0.80` in
`src/packages/cern_ai.py:CAPABILITY_DISCLOSURE_AND_EVAL`.

---

## Section 5: Production / R&D Levers

### 5.1 Directed R&D for Human-Complementary AI (Package F)

**Specification:** Public R&D funding ($30B/yr) directed at AI that
augments rather than substitutes for labor.

**Empirical analogs:**

- **DARPA program model** — directed R&D produced GPS, Internet, drones,
  autonomous vehicles. Effect: ~2-4× ROI on directed research
  (Mazzucato 2013).
- **NIH biomedical R&D** — $48B/yr. Productivity gains from public R&D
  shown in Azoulay-Graff Zivin et al. (2019).
- **NSF NAIRR Pilot (2024-)** — early days; $35M too small to estimate
  effects.
- **Federal R&D historical** — Mazzucato-Penna 2018 review: substantial
  spillovers from public R&D into private innovation.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| Labor-augmenting productivity growth boost | +1.5%/yr | +0.5% | +3.0% | Mazzucato 2013/2021 ROI estimates |
| Automation rate dampening | -40% | -20% | -55% | Acemoglu/Restrepo directed-tech effects |
| Skill-mix shift toward complement | +10pp | +5pp | +15pp | Cumulative over 10 yr |
| Public R&D as % of GDP | 0.12% | 0.08% | 0.20% | $30B / $25T US GDP |

**Mapping to simulator:** `labor_augmenting_productivity_growth=0.015`,
`automation_threshold_growth_dampening=0.40`,
`skill_mix_complement_shift=0.10` in
`src/packages/build_different.py:DIRECTED_RD_FOR_COMPLEMENT_AI`.

**Limitations:** "Direction" of R&D is hard to enforce. NIH grants get
directed toward specific disease areas successfully; whether AI R&D
can be successfully directed toward complement-rather-than-substitute
applications is genuinely uncertain. Acemoglu-Johnson 2023 argue yes.

---

### 5.2 Federal Procurement Preference for Non-Displacing AI (Package F)

**Specification:** US federal procurement preferentially purchases AI
tools that augment public-sector workers.

**Empirical analogs:**

- **U.S. Buy American Act (1933)** — directed procurement preference for
  domestic suppliers. Has shaped industrial structure.
- **Federal procurement of cloud services (2010s)** — FedRAMP
  certification effectively shaped cloud security standards industry-wide.
- **EU Green Public Procurement** — sustainability criteria in
  procurement; documented effects on supplier choices.

**Effect-size estimate:**

| Outcome | Central | P10 | P90 | Source |
|---|---|---|---|---|
| AI market share shift toward complement systems | +15pp | +8pp | +25pp | EU GPP analogs scaled |
| Private R&D following federal procurement | +20pp toward complement | +10pp | +35pp | Industrial-policy literature |
| Federal procurement leverage (% of total demand) | 5-10% of AI services | — | — | Federal IT spending ratios |

**Mapping to simulator:** `ai_market_share_complement_systems=0.15`,
`ai_dev_resource_allocation_complement=0.20` in
`src/packages/build_different.py:PROCUREMENT_PREFERENCE_NON_DISPLACING`.

---

## Cross-Cutting Caveats

**1. None of the AI-specific levers have analogs at the scale being
proposed.** Norway GPFG is much smaller than a 10% AI capital sovereign
fund would be. UBI trials are finite-duration and small-N. CERN is non-
strategic. Compute governance is theoretical. **Effect-size confidence
intervals here are wider than the literature suggests because of analog
imperfection.**

**2. Effect sizes assume implementation as designed.** Real implementations
face political compromise, capture, and enforcement gaps. Reported effects
are upper-bound for ideal implementation; actual effects likely 50-80%
of the central values.

**3. Interaction effects are not in this document.** Each lever's
empirical analog gives its standalone effect. When packages combine
levers, sub-additivity (substitutability) and super-additivity (complementarity)
are real but not characterized in the analog literature. Hypothesis 6
in PREREGISTRATION.md tests this for Pillar 1 + Pillar 6 specifically.

**4. The biggest gap: open-weights inversion.** The framework's Pillar 5
assumes open-weights mandate dampens markups. Q1 2026 reality (Chinese
open-weights leadership) inverts the polarity. Hypothesis 1 in
PREREGISTRATION.md is the explicit test of this gap.

**5. Effect sizes here will be refined in Phase 5.** The hostile-critique
review (libertarian, China-realist, heterodox) will surface objections
to specific effect sizes. Document version v2.0+ will incorporate those.

---

## How this document is used

- **By the simulator (`src/core/simulator.py`):** consumed indirectly via
  the `parameter_changes` dict in each `PolicyLever` (`src/packages/*.py`).
  Effect-size values in those dicts must match the central values
  documented here.
- **By the methodology section of the white paper:** every reported
  finding traces back to one or more analog estimates here.
- **By the hostile-critique reviewers (Phase 5):** the analog selection
  and effect-size estimation are the most attackable parts of the
  analysis. Review of this document is the highest-leverage red-team
  exercise.

---

*Document version 1.0. To be revised after Phase 5 hostile critique.*
