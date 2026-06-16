# Limitations

This section pre-empts the methodological critiques that any reader of
this paper is entitled to make. Each limitation is stated explicitly,
with what would have to be true for the result to fail, and what the
model can and cannot legitimately say about that limitation.

The discipline is to surface every limitation before a critic does. A
limitation that's named, characterized, and bounded is much less
damaging than the same limitation discovered by a hostile reviewer.

## 1. Reduced-form simulator, not full HANK

The simulator (`src/core/simulator.py`) applies documented effect-size
deltas to a calibrated status-quo baseline, rather than deriving
trajectories from a fully micro-founded heterogeneous-agent New
Keynesian model. This is a deliberate choice, documented in `CLAUDE.md`'s
2026-05-01 addendum: the original structural prototype produced two
known calibration failures (GDP overshooting observed by 10×, top-1%
wealth share moving the wrong direction), and rebuilding the structural
machinery risked repeating those failures with the same parameters.

The reduced-form approach is appropriate for the project's *comparative*
question (which package dominates under what conditions) but is not
appropriate for *level* claims (what GDP, inequality, etc. will literally
be in 2036). Throughout the paper, claims are stated as deltas vs.
status quo with documented uncertainty intervals; no level claim is
made that doesn't trace to a baseline reference.

A future companion paper could rebuild the analysis on top of a HANK
toolkit (HARK, Sequence Space Jacobian) with appropriate calibration.
The expected effect on the comparative conclusions of this paper is
modest because the *deltas* (rather than levels) are what drive the
recommendations.

## 2. The Lucas critique applies

Parameters calibrated to 2015–2025 observed data — saving rates, monopsony
elasticity ε, markup growth, capital flight responsiveness — will shift
under a structurally different regime such as Pillar 1 (sovereign equity
acquisition). The Lucas (1976) critique is real for this class of
analysis. The mitigations are:

- Counterfactual delta framing (Section 9) partially neutralizes the
  critique because Lucas-shifted parameters affect both baseline and
  policy branches roughly symmetrically.
- RDM uncertainty ranges (PREREGISTRATION.md §7) are wide enough to
  absorb modest Lucas drift.
- Comparative ordering across packages is more robust to Lucas drift
  than absolute levels.

But the critique is not eliminated. A reform large enough to produce
its own regime change is not perfectly modeled, and recommendations
should be read as "best estimate under current behavioral parameters"
rather than "structural certainty."

## 3. Pillars 2 and 3 of the Nebulai framework are inferred

The Nebulai whitepaper's full text was not available in the simulation
sandbox; Pillars 2 and 3 of the framework are specified by inference from
the handoff documentation and contextual hints in `SIMULATION.md`
(which references "Pillar 3: regional cooperation" in the geopolitical
state enum). The current specifications — Pillar 2 as public AI
infrastructure (NSF NAIRR-style at scale), Pillar 3 as light-touch
international coordination — are best-guesses from context, flagged as
such in `src/packages/nebulai_six.py`.

If the actual whitepaper specifications differ materially from these
guesses, Package B (Nebulai Six) comparison against the other packages
shifts in proportion. This is a tractable limitation: re-running the
analysis with corrected Pillar 2/3 specifications takes hours, not weeks,
and the comparative ordering of all *other* packages is unaffected.

## 4. No structural model of AGI / ASI

The framework explicitly does not model recursive self-improvement, AGI
emergence, or alignment failure. These are central to AI policy debates
in 2026 but are properly handled in a separate analysis (Bengio et al.
2025 *International AI Safety Report* is the appropriate reference).

The framework's recommendations are conditional on capability scaling
continuing along trajectories near the published Acemoglu 2024 / Goldman
Sachs Research base case. If transformative AI arrives by 2030 with
discontinuously different economic implications, the framework's
quantitative findings become unreliable and the qualitative direction
(the framework's pillars supporting broader prosperity) may or may not
survive. This is honest deep uncertainty, not a known parameter sweep.

## 5. Bilateral US-China only, not three-tier

The model represents the US and China as the two anchor countries.
Emerging-market (India, Brazil, Indonesia, Mexico, South Africa, Turkey)
and developing-tier (sub-Saharan Africa aggregate) dynamics are not
explicitly modeled. The framework's adoption-equilibrium argument —
that the median household in *every* country tier benefits — therefore
rests on inference from US/CN to the other tiers, not direct simulation.

Extension to a three-tier model is planned for Phase 7 of the project
roadmap (`ROADMAP.md`). Until then, the cross-class results in this
paper apply rigorously to US and CN, and inference to other tiers
should be read with appropriate epistemic humility.

## 6. Geopolitical layer is illustrative, not predictive

The geopolitical stability index and arms-race intensity are reported
qualitatively in the methodology section because the underlying causal
mappings — from policy architecture to international stability, conflict
probability, AI arms-race dynamics — draw on IR literature (Allison,
Mearsheimer, Ikenberry, Doshi) that is itself genuinely contested.

The literature on whether bipolar splits produce conflict is not
settled. The literature on whether shared scientific infrastructure
reduces conflict (CERN, ITER, ISS analogs) is suggestive but not
strong evidence for the much more strategic AI context. The geopolitical
layer in our simulation should be read as *one possible* mapping with
explicit citations, not as a calibrated prediction.

## 7. Effect-size confidence intervals are wider than the literature suggests

None of the AI-specific levers — sovereign AI equity acquisition,
open-weights mandate, compute governance treaty, CERN-AI public lab —
have empirical analogs at the proposed scale. The closest analogs
(Norway GPFG for sovereign equity; OSS economics for open weights;
NPT for compute governance) have different mechanisms, different
strategic environments, and different time horizons. Effect-size
intervals in `EMPIRICAL_ANALOGS.md` are widened to reflect analog
imperfection, but real uncertainty is probably larger than even the
widened intervals.

This is the strongest limitation. Hostile reviewers will (correctly)
focus most attention here. The mitigation is the comparative-delta
framing — even substantial error in absolute effect sizes preserves
relative ordering across packages, *if* the errors are common-mode.

## 8. Hostile review not yet completed

The Phase 5 hostile-critique stage of the project plan
(`ROADMAP.md`) — commissioning paid critique from named scholars in the
libertarian (Cowen / Cochrane school), strategic-competition (CSIS /
Hudson school), and heterodox (post-Keynesian / MMT) traditions — has
not been completed at the time of paper drafting. Each of those
perspectives will produce specific objections to specific effect sizes
and assumptions. The current effect-size estimates are first-pass
literature synthesis and should be expected to shift under structured
adversarial critique.

The paper's conclusions are robust to *direction* under most plausible
revisions, but specific quantitative claims may move. Readers should
treat point estimates as preliminary pending hostile-critique-updated
v2.0.

## 9. Pillar-interaction effects are underspecified

The simulator treats each lever's effect as additive (with documented
gating for coordination requirements). In reality, levers interact:
Pillar 1 (sovereign equity) and Pillar 6 (AI tax) target overlapping
rents and may be partial substitutes (Hypothesis 6 in
`PREREGISTRATION.md`); Pillar 4 (reskilling) and Pillar 5 (open weights)
may be complements if open weights expand the surface area where
reskilled workers can apply complement skills. The current simulator
does not model these interactions explicitly.

Hypothesis 6 tests the Pillar 1 × Pillar 6 substitutability claim;
other interactions are deferred. The expected effect on conclusions is
modest because most package comparisons involve different *mechanisms*
rather than different intensities of the same mechanism — the
interaction term primarily affects sub-package design within a
particular mechanism family.

## 10. The framework's own pillars may not be optimal

The seven-package comparison includes the Nebulai framework
(Package B), a CERN-AI-centered alternative (Package C), and a
game-theoretically-derived eight-pillar set (Package G) that explicitly
attempts to fix the framework's structural weaknesses. If the analysis
finds that Package G or C dominates Package B under most parameter
draws, the implication is that the framework as currently designed is
suboptimal — and the appropriate response is to revise the framework
in line with the dominant package, not to defend the framework against
the evidence.

The authors commit, *in advance of seeing final results*, to reporting
honestly whichever package dominates. This commitment is the
pre-registration discipline (PREREGISTRATION.md §10): findings cannot
be retroactively reinterpreted to favor a pre-committed answer. If
this paper concludes with a recommendation for Package C or Package G
rather than Package B, that is a working-as-intended outcome of the
methodology.

## What the analysis cannot legitimately do

For clarity, the following claims are *not* supported by this analysis
and any of them being made about this paper would be a methodological
critique we accept:

- Predicting GDP, inequality, or any other outcome at a specific year
  with point precision
- Forecasting whether China will or will not cooperate on AI policy
- Predicting the probability of US-China conflict
- Resolving the σ task-elasticity debate
- Modeling alignment failure or AGI emergence
- Quantitatively scoring any specific real-world policy proposal
  (the candidates here are stylized representations)
- Claiming peer-review certification before peer review actually
  occurs

The analysis is decision-quality counterfactual delta evidence under
deep uncertainty, anchored to empirical analogs and pre-registered.
That is what it is. Treating it as more (e.g., a structural forecast)
would not be supported; treating it as less (e.g., a stylized
illustration) would understate its methodological discipline.

## Where these limitations leave the policy recommendation

The recommendations the paper makes (forthcoming based on completed
analysis) survive the limitations above if and only if:

- The framework's pillar set produces robust dominance under RDM, or
- The framework's pillars survive adversarial-critique-driven effect-
  size revision, or
- The framework's structural argument is qualitatively unaffected by
  the limitations even when quantitative claims must be hedged.

If none of these conditions hold, the appropriate response is to revise
the framework. The methodological commitment is to publication-quality
defensibility, not to defending a pre-committed answer.
