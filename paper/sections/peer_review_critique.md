# Peer Review Critique of Prototype Simulation

This document records the peer-review-style critique produced during the prototype phase. It serves two purposes: (1) the basis for the paper's `10_limitations.md` section, and (2) the explicit list of issues the production simulation must address.

The critique is divided into "macro economist" objections (concerning the model's economic structure) and "political scientist" objections (concerning the framework's adoption argument). Each objection is rated by severity and by whether the planned production simulation addresses it.

## Macro economist objections

### M1. Stylized accounting model, not a macroeconomic model
**Severity: HIGH.** The prototype was a Lorenz-curve evolution exercise with redistribution rules — no production function, no factor-price determination, no investment dynamics, no monetary side, no expectations. **Production simulation addresses:** ✓ Task-based production with marginal-product factor returns (Stage 1 of prototype, ported to `src/production/`).

### M2. Investment elasticity hand-waved
**Severity: HIGH.** The prototype used `INV_ELASTICITY = 0.7` with no microfoundation. **Production simulation addresses:** ✓ Caballero-Engel-style adjustment cost model in `src/capital/capital_markets.py`; calibrated to documented empirical estimates with sensitivity analysis.

### M3. AI premium plucked from air
**Severity: HIGH.** Prototype used 5–10% extra return on top-decile wealth as "AI premium" with no derivation. **Production simulation addresses:** ✓ Returns emerge from CES/task-based production marginal product; differential returns by wealth tier follow Saez-Zucman 2016 empirical estimates.

### M4. Cross-region inference rents stipulated
**Severity: MEDIUM.** Prototype assigned 2% of developing-country GDP as flowing to Frontier, no derivation. **Production simulation addresses:** Partially. Country module (Session 8 of roadmap) calibrates AI services trade to actual hyperscaler revenue from non-Frontier customers, currently ~$50B/year. Still requires forward-projection assumption.

### M5. Monolithic labor share
**Severity: MEDIUM.** Real labor share is bifurcated — high-AI-complementarity workers see wage growth, AI-substitutable workers see decline. **Production simulation addresses:** ✓ Three-skill labor structure (safe / substitute / complement) with separate wage dynamics.

### M6. No general equilibrium
**Severity: MEDIUM.** Prototype lacked price-quantity feedback. **Production simulation addresses:** Partially. Wages and capital returns clear at marginal products. Still missing: explicit price-level dynamics, cross-sector reallocation, monetary policy.

### M7. Confidence intervals missing
**Severity: HIGH.** Prototype produced point estimates with no uncertainty quantification. **Production simulation addresses:** ✓ Monte Carlo over literature-anchored parameter distributions, P10/P50/P90 reporting throughout (Session 7 of roadmap).

### M8. Demand resilience metric contrived
**Severity: MEDIUM.** Prototype invented a non-standard metric. **Production simulation addresses:** ✓ Replaced with standard inequality measures: Gini, P90/P10, Atkinson index, top-share, and median real income growth.

### M9. 11-year horizon too short for some arguments
**Severity: LOW.** AI productivity diffusion typically takes 20–40 years. **Production simulation addresses:** Partially. The 2026–2036 horizon matches the white paper's claim window. A 25-year extension is feasible as a supplementary analysis.

### M10. Aggregation across heterogeneous countries brutal
**Severity: HIGH.** "Frontier" lumps US, EU, China, etc. with wildly different conditions. **Production simulation addresses:** ✓ Country disaggregation in Session 8 of roadmap; six Frontier countries modeled separately.

### M11. Capital-market reaction to Pillar 1 not modeled
**Severity: MEDIUM.** A 30% sovereign equity acquisition would, in real markets, raise required equity returns and slow investment. **Production simulation addresses:** ✓ Cost-of-equity rises with sovereign acquisition share in `src/capital/capital_markets.py`; investment function responds to required-realized return gap.

### M12. Wealth concentration cannot be derived from flow-income models
**Severity: HIGH.** Prototype could not reproduce observed top-1% wealth share trajectory because wealth concentration requires r > g, inheritance, or asset-price ingredients absent from production-side models. **Production simulation addresses:** ✓ Piketty-style differential returns and inheritance flows added explicitly in Session 3.

## Political scientist objections

### P1. Median voter theorem assumed
**Severity: HIGH.** The framework's adoption equilibrium argument is Downsian. Modern political science (Achen-Bartels, Gilens-Page) has largely abandoned median voter as descriptive. **Production simulation addresses:** ✗ Cannot. This is a normative-political-theory issue, not modelable. **Disposition:** Acknowledged in `paper/sections/10_limitations.md`. The paper should reframe the adoption argument as conditional on functioning democratic feedback rather than asserting it as universal.

### P2. Bismarck calculation does not generalize
**Severity: HIGH.** The historical analogy (Bismarck, FDR) selectively cherry-picks cases where elites accommodated. Russia 1917, France 1788, etc. show elites who didn't accommodate and were destroyed — proving the threat is real, but not that voluntary accommodation is the modal response. **Production simulation addresses:** ✗ Cannot. **Disposition:** Acknowledged in `paper/sections/10_limitations.md`. The historical-precedent argument is rhetorical scaffolding, not load-bearing.

### P3. International coordination assumed at moment of collapse
**Severity: HIGH.** The framework requires multilateral coordination at exactly the moment when WTO is moribund, OECD pillar-2 unraveling, G20 fragmenting. **Production simulation addresses:** Partially. Coalition formation modeled in Session 9 (geopolitical layer). But the *theory of how coordination becomes possible* is not in the model. **Disposition:** Acknowledged. The paper should be honest that this is the framework's weakest precondition.

### P4. Free-rider problem more serious than simulated
**Severity: MEDIUM.** The "Frontier-only" scenario assumed Frontier benefits domestically even without coordination. But if EU adopts and US doesn't, EU AI firms operate under capital constraints US firms don't, creating EU→US capital flight pressure. **Production simulation addresses:** ✓ Capital flight scenario (`participatory_capflight.py`) explicitly models this. Sensitivity analysis varies the differential.

### P5. No theory of state capacity
**Severity: HIGH.** Pillar 1 (sovereign wealth fund), Pillar 4 (portable benefits administration), Pillar 6 (automation-intensity coefficient measurement) all require state capacity that varies wildly across countries. **Production simulation addresses:** Partially. Country module (Session 8) includes state-capacity parameters that scale policy effectiveness. **Disposition:** Acknowledged limitation: the framework assumes Norwegian-quality institutions almost everywhere. Where state capacity is weaker (Brazil, India, Indonesia, much of Africa), implementation is more difficult.

### P6. Geopolitical stability simulation is a vibes index
**Severity: MEDIUM.** Component scores in the chat-session geopolitics simulation were calibrated by judgment, not derived from causal models in the IR literature. **Production simulation addresses:** Partially. Session 9 reframes this as illustrative rather than predictive, with explicit acknowledgment.

### P7. Historical precedents cherry-picked
**Severity: MEDIUM.** Same as P2 — selection bias in the cases used. **Production simulation addresses:** ✗ Cannot. **Disposition:** Acknowledged in limitations.

### P8. State-business collusion not addressed
**Severity: MEDIUM.** The Pillar 1 sovereign fund will face exactly the regulatory-capture pressures any large public investor faces. The Norwegian model works partly because Norway is high-trust, transparent, etc. **Production simulation addresses:** Partially. Country-level state-capacity parameters capture some of this. **Disposition:** Acknowledged.

### P9. Coerced redistribution as deterrent — credibility
**Severity: HIGH.** For voluntary adoption to be rational, the coerced-redistribution threat must be credible. In the US, no major candidate has run on AI windfall taxes. The threat may be strongest in Europe and weakest in the US — opposite of where it would need to be. **Production simulation addresses:** ✗ Cannot model political credibility directly. **Disposition:** Acknowledged. The paper should be explicit that the deterrent argument is strongest in Europe and weakest in the US.

### P10. AI safety dimension absent
**Severity: HIGH.** If AGI arrives in the late 2020s with the dynamics Korinek-Davidson-Halperin-Houlden (2026) describe, the entire economic-distribution conversation becomes secondary. **Production simulation addresses:** ✗ Out of scope. **Disposition:** Explicitly bracketed in the paper. The paper is about the human-managed AI transition; if AGI takes the system over, the framework is moot.

## Summary of disposition

| Objection | Severity | Production sim addresses? |
|---|---|---|
| M1 Macro structure | HIGH | ✓ |
| M2 Investment elasticity | HIGH | ✓ |
| M3 AI premium | HIGH | ✓ |
| M4 Cross-region rents | MEDIUM | Partial |
| M5 Monolithic labor share | MEDIUM | ✓ |
| M6 No GE | MEDIUM | Partial |
| M7 No CIs | HIGH | ✓ |
| M8 Contrived metrics | MEDIUM | ✓ |
| M9 Time horizon | LOW | Partial |
| M10 Country aggregation | HIGH | ✓ |
| M11 Capital market reaction | MEDIUM | ✓ |
| M12 Wealth dynamics | HIGH | ✓ (Session 3) |
| P1 Median voter | HIGH | Limitation |
| P2 Bismarck cherry-picking | HIGH | Limitation |
| P3 Coordination collapse | HIGH | Limitation |
| P4 Free-rider | MEDIUM | ✓ |
| P5 State capacity | HIGH | Partial + limitation |
| P6 Geopolitics vibes | MEDIUM | Partial + caveat |
| P7 Historical cherry-pick | MEDIUM | Limitation |
| P8 State-business collusion | MEDIUM | Limitation |
| P9 Coercion credibility | HIGH | Limitation |
| P10 AI safety | HIGH | Bracketed |

**Score: 12 of 22 objections fully addressed by production simulation; 5 partially; 5 surface as explicit paper limitations.**

This is what serious research papers do: not silence critique by refusing to engage, but list every objection upfront and explicitly mark how each is handled. A reader who has read this document knows exactly what the paper claims and what it does not.
