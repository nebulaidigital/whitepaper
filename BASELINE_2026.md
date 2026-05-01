# Q1 2026 Status-Quo Baseline

**Document version:** 1.0
**Date:** 2026-05-01
**Purpose:** Define the "do-nothing" trajectory against which all policy
package deltas are measured. The simulation does not predict absolute
outcomes; it predicts deltas vs. this baseline.

> The handoff (`CLAUDE.md`, `SOURCES.md`) was written in April 2026 and
> assumes a status quo that is partly already obsolete. The AI policy
> environment has shifted substantially since the handoff was drafted.
> This document establishes the actual Q1 2026 baseline against which
> the framework's marginal contribution must be evaluated.

---

## 1. Why a refreshed baseline matters

The handoff's "Patchwork" baseline implicitly assumes:

1. US AI development is closed-weights, China is catching up on closed-weights
2. International coordination is minimal beyond Bletchley-style declarations
3. AI capital is privately held, sovereign-fund participation absent
4. Capital flight regulation is largely passive
5. Antitrust enforcement against AI firms is dormant

Each of those assumptions has shifted in 2025–2026. If the framework is
evaluated against the original "Patchwork" baseline, it gets credit for
movement that's *already happened* through other channels. To produce
honest counterfactual deltas, the baseline must reflect what's actually
true now.

---

## 2. Major shifts since the handoff was drafted

### 2.1 The open-weights inversion

**Pre-2025 framing (in handoff):** US frontier labs hold the closed-weights
advantage; open-weights are a small-scale competitive fringe. Pillar 5
(open-weights mandate) is a *policy intervention* to break US AI lab rents.

**Q1 2026 reality:** China has decisively become the open-weights leader.
DeepSeek V3 (Dec 2024), DeepSeek R1 (Jan 2025), Qwen 2.5 (Sep 2024), Qwen 3
(2025), GLM-4, Yi-Lightning, MiniMax M1 — frontier-or-near-frontier Chinese
models released openly with weights, training methodology, and (in some
cases) training data. US frontier labs (Anthropic, OpenAI, Google DeepMind)
remain closed-weights for top capability tiers; Meta Llama is partially open
but trails frontier capability.

**Implication for the framework:** Pillar 5 as written has the polarity
backwards. Mandating open-weights for US frontier labs in 2026 doesn't break
US monopoly rents — it gives away US capability to a Chinese ecosystem
that's already optimized to absorb and extend it. The marginal contribution
of Pillar 5 is much smaller than the framework assumes, possibly negative.

**Sources:** Bommasani, Kapoor et al. (2024); DeepSeek V3 / R1 technical
reports; Qwen technical reports; Stanford HAI AI Index 2025.

### 2.2 State-scale capital concentration in compute

**Pre-2025:** Hyperscaler capital expenditure was substantial but private —
$50–80B/yr range across all major cloud + frontier labs combined. Capital
flight risk for sovereign-equity acquisition was the dominant concern in
Pillar 1 design.

**Q1 2026 reality:**
- **Stargate** (Jan 2025): $500B over four years, OpenAI/SoftBank/Oracle/MGX
  consortium. State-affiliated capital flows participating.
- **EU InvestAI**: €200B mobilized
- **French €109B AI investment commitment**: announced at Paris AI Summit
- **Saudi HUMAIN**: state-affiliated AI infrastructure
- **UAE G42 / MGX**: sovereign-affiliated AI capital
- **Chinese state-directed AI capital**: ~$140B 2025–26 across central +
  provincial programs

**Implication for the framework:** Pillar 1 (sovereign equity acquisition)
is *more* feasible in 2026 than in 2024, because the relevant capital is
already state-affiliated or state-adjacent. Capital flight risk is *lower*
because state-anchored capital cannot relocate as freely as private capital.
The framework's design conservatism (10% acquisition fraction) may be too
modest given the changed capital landscape.

**Sources:** Stargate announcement; Stanford HAI AI Index 2025; CSET
sovereign AI tracker; OECD AI Outlook 2025.

### 2.3 Tech decoupling and compute export controls

**Pre-2025:** BIS October 2022 export controls were the active regime, with
imperfect enforcement and observable evasion through Singapore/Malaysia
intermediaries.

**Q1 2026 reality:**
- BIS October 2023, October 2024, January 2025 successive tightenings
- Effective controls on EUV lithography (ASML), advanced packaging, HBM
  memory, and frontier GPUs >$3K
- Chinese countermeasures: gallium, germanium, rare earth export controls
- Bilateral US-China relationship is structurally adversarial on AI specifically
- No multilateral compute governance regime; bilateral controls only

**Implication for the framework:** Bilateral US-China is *the* policy
environment, not a "nice extension." Any pillar that requires China
participation (or that fails under China non-participation) must be
explicitly designed for the decoupled regime. The framework's "global
adoption" framing is underspecified for the bilateral reality.

**Sources:** BIS regulations; CSET Khan/Allen export-control analyses;
Chinese MOFCOM countermeasure announcements.

### 2.4 Active regulatory regimes

**Pre-2025:** Patchwork was descriptively accurate — fragmented voluntary
commitments, draft regulations, no in-force AI-specific law in major
jurisdictions.

**Q1 2026 reality:**
- **EU AI Act** in force; high-risk and prohibited categories enforceable;
  general-purpose AI obligations took effect August 2025
- **US AI Executive Orders** (Oct 2023; subsequent administration-specific
  modifications) creating mandatory reporting for frontier training runs
  above compute threshold
- **UK AI Safety Institute** producing capability evaluations (publicly
  released for several frontier models)
- **US AI Safety Institute** + International AI Safety Institute Network
  (Bletchley → Seoul → Paris → Brussels)
- **China's Cyberspace Administration** generative AI regulation in force;
  state security review for above-threshold deployments
- **NIST AI Risk Management Framework** + sector-specific applications
- Multiple state-level AI laws (Colorado, California SB 1047 successor,
  Texas, NY)

**Implication for the framework:** The status quo is no longer "Patchwork"
in the original sense — it's a partial, fragmented, but active regulatory
mosaic. The framework's pillars should be evaluated against this real
baseline, not the abstract Patchwork. Some pillars (mandatory disclosure,
capability evaluation) are *already partially implemented* and the
framework's claimed contribution must be the marginal additional effect,
not the total.

**Sources:** EU AI Act primary text + implementing acts; US Executive
Orders; UK AISI publications; US AISI publications; Chinese CAC
regulations; NIST AI RMF.

### 2.5 AI safety infrastructure and capability evaluation

**Pre-2025:** AI safety was largely a private-sector concern (Anthropic
Responsible Scaling Policy, OpenAI Preparedness Framework, DeepMind
Frontier Safety Framework — all voluntary).

**Q1 2026 reality:**
- **International AI Safety Report 2025** published (Bengio chair),
  commissioned by AISI Network — formal multilateral assessment of AI risk
- **AISI Network** member institutes in UK, US, Japan, Singapore, Canada,
  India, Korea, France, EU AI Office
- **METR**, **Apollo Research**, **AI Safety Institutes** producing
  capability evaluations for frontier models pre-deployment
- **Responsible Scaling Policies** at Anthropic, OpenAI, DeepMind, Meta,
  Google updated with explicit deployment thresholds

**Implication for the framework:** A proto-CERN-AI capability evaluation
infrastructure already exists. The framework's omission of capability
disclosure / mandatory evaluation as a pillar is a gap — there's a built
substrate to extend, not an empty space to invent.

**Sources:** International AI Safety Report 2025; AISI publications;
Anthropic/OpenAI/DeepMind RSPs.

### 2.6 Antitrust and structural competition policy

**Pre-2025:** Antitrust against Big Tech was active (DOJ vs Google search,
DOJ vs Apple, FTC vs Meta) but pre-AI-specific.

**Q1 2026 reality:**
- DOJ vs Google search remedies phase ongoing (advertising / Chrome
  divestiture proposed)
- FTC active on AI cloud-provider investments (Microsoft-OpenAI,
  Anthropic-Amazon, Anthropic-Google scrutiny)
- EU DMA fully applicable to designated gatekeepers
- UK CMA AI foundation model market investigation
- Active legal precedent for structural separation as remedy

**Implication for the framework:** Aggressive antitrust as a primary lever
(Package D Compute-Centric, Package F Build-Different-AI) is no longer
unprecedented. The legal and political infrastructure for structural
separation of model labs from cloud providers is materially closer than
the framework's current pillar set assumes.

**Sources:** DOJ filings; FTC investigations; EU Commission DMA decisions;
UK CMA AI foundation models report.

---

## 3. Refreshed quantitative baseline

US 2025 → 2036 status-quo trajectory under the Q1 2026 baseline (i.e., the
fragmented-but-active regulatory mosaic continues; no new framework adopted;
no major US-China AI cooperation):

| Indicator | 2025 actual | 2036 status-quo central | Range (P10–P90) | Source |
|---|---|---|---|---|
| US labor share | 56% | 51% | 49–53% | Acemoglu 2024 + DLEU trend |
| US top 1% wealth share | 30.4% | 33.5% | 32–36% | Saez-Zucman trajectory + Piketty r>g |
| US mean markup | 1.22 | 1.28 | 1.25–1.32 | DLEU 2020 growth rate |
| US real GDP cumulative growth (2025–2036) | (base) | +27% | 22–34% | Acemoglu 2024 base + AI productivity |
| US AI sector share of value-added | ~3% | ~12% | 8–17% | Goldman 2023; Stanford AI Index 2025 |
| US substitute-worker employment Δ | — | −18% of pre-AI roles | −10% to −28% | Webb 2020 + Eloundou 2023 |
| US median household real income | (base 100) | 99 | 92–108 | Mixed — depends on AI productivity capture |
| China labor share | ~50% (PWT) | ~47% | 44–50% | PWT extrapolation |
| China real GDP cumulative growth | (base) | +52% | 35–65% | World Bank baseline + AI contribution |
| China top 1% wealth share | ~30% | ~32% | 30–35% | WID + state-mediated dynamics |
| Bilateral cooperation index (0–100) | 25 | 20 | 10–35 | Atlantic Council; SIPRI projections |
| Geopolitical AI stability (0–100, illustrative) | 38 | 30 | 20–45 | SIPRI; Atlantic Council |

**Note.** This is *not* a forecast. It is a "no-policy-change" trajectory
used as the comparison anchor. Every reported policy delta is computed
relative to this baseline.

---

## 4. What this means for delta interpretation

When the simulation reports "Package B reduces US top-1% wealth share by
1.5pp vs. baseline," that means:

- 2036 baseline projection: 33.5% (range 32–36%)
- 2036 under Package B: 32.0% (range 30.5–34.5%)
- Reported delta: −1.5pp (with appropriate uncertainty propagation)

The delta is more reliable than either absolute number, because:

1. Common-mode model errors cancel between baseline and Package B branches
2. The Lucas critique is partially neutralized — calibration shifts affect
   both branches roughly symmetrically
3. The reader can separately assess whether they agree with the baseline
   (using their own priors) and whether they agree with the policy response

If a reader thinks the baseline top-1% trajectory is 35% rather than 33.5%,
they can mentally shift both numbers up by 1.5pp without changing the
package's marginal contribution.

---

## 5. Baseline update protocol

This baseline document is **versioned** and **dated**. When new data shifts
the baseline materially (e.g., a major policy event, new BIS controls, a
significant US-China bilateral development), a `BASELINE_2026Q3.md` (or
later quarter) supersedes this version. Prior baseline versions remain in
the repo for replication.

Material change threshold: any of the indicators in §3 shifts by more than
10% of its P10–P90 range, or a new structural break occurs (e.g., AGI claim
validated, major capability discontinuity, US-China conflict, etc.).

Routine updates without structural break: annual.

---

## 6. Open issues for the baseline

Items where current best estimates are weakest and the simulation should
sweep over the uncertainty:

1. **Chinese AI productivity attribution.** PRC official statistics likely
   underreport AI's contribution to value-added; independent estimates vary
   widely. Baseline range may be too narrow.
2. **Capital-flight elasticity for AI capital specifically.** Empirical
   anchors are wealth-tax responses (Bach, Brülhart) — not directly
   transferable. Treat as deep uncertainty.
3. **AI productivity growth rate going forward.** Goldman, IMF, Acemoglu,
   Brynjolfsson estimates span 0.5%–4.0%/yr. Range is wide; do not anchor.
4. **Substitute-worker re-employment dynamics.** Acemoglu-Restrepo
   reinstatement effect is empirically observed historically but may not
   replicate at LLM-scale displacement velocity.
5. **Information-warfare / political-stability feedback.** Documented
   degradation but quantification is contested.

These are flagged in the pre-registration document as deep-uncertainty
parameters that drive RDM scenario discovery (Hypothesis 9).

---

*End of baseline document v1.0.*
