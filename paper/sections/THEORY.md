# Formal Theoretical Specification

This document specifies the theoretical structure of the simulation
in equations. Every quantity in the simulator traces to a labeled
equation here, with calibration source and uncertainty interval.

The structure responds to the PhD-level critique that the v0.2 paper
moves too quickly from theory to projection without separating
mechanisms and documenting equations. Reviewers can compare equations
here against the code in `src/`; calibration sources can be cross-
checked against `EMPIRICAL_ANALOGS.md`.

## 1. Production: task-based model

Following Acemoglu & Restrepo (2018, 2019, 2022), production occurs
across a continuum of tasks indexed by z ∈ [0, 1+N]. Tasks z < I are
performed by capital; tasks z ≥ I by labor.

### 1.1 Output

Output Y is a CES aggregate over the task continuum:

```
Y = B · [ ∫₀ᴵ q_K(z)^((σ-1)/σ) dz + ∫_I^(1+N) q_L(z)^((σ-1)/σ) dz ]^(σ/(σ-1))
```

where:
- I ∈ [0, 1+N] — automation threshold (tasks below performed by capital)
- N ≥ 0 — new tasks added at the labor-eligible end (reinstatement effect)
- σ > 0 — task elasticity of substitution
- q_K(z), q_L(z) — productivities at task z
- B — TFP scaling parameter

For tractability, productivities are uniform within each region:
q_K(z) = A_K for z < I; q_L(z) = A_L for z ≥ I. Capital is allocated
equally across [0, I]; labor across [I, 1+N]:

```
Y = [ I^(1/σ) · (A_K K)^((σ-1)/σ) + (1+N-I)^(1/σ) · (A_L L)^((σ-1)/σ) ]^(σ/(σ-1))
```

### 1.2 Cobb-Douglas limit (σ → 1)

```
Y = (A_K K)^α · (A_L L)^(1-α)   where α = I / (1+N)
r = α · Y / K
w = (1-α) · Y / L
labor share = 1 - α = (1+N-I) / (1+N)
```

### 1.3 General CES branch (σ ≠ 1)

```
K_eff = I^(1/σ) · (A_K K)^((σ-1)/σ)
L_eff = (1+N-I)^(1/σ) · (A_L L)^((σ-1)/σ)
Y = (K_eff + L_eff)^(σ/(σ-1))
r = (Y/K) · K_eff / (K_eff + L_eff)
w = (Y/L) · L_eff / (K_eff + L_eff)
labor share factor = L_eff / (K_eff + L_eff)
```

### 1.4 The three core comparative statics

Acemoglu-Restrepo (2022) identify three effects of AI on the labor share:

1. **Displacement effect.**
   ∂(labor share) / ∂I < 0
   Automating tasks (raising I) lowers labor share.

2. **Reinstatement effect.**
   ∂(labor share) / ∂N > 0
   New tasks created at labor-end (raising N) raise labor share.

3. **Capital-augmenting productivity bias.**
   ∂(labor share) / ∂A_K < 0 when σ > 1
   With elastic task substitution, productivity gains in capital lower
   labor share.

All three are validated in `tests/test_production.py` via the prototype
module.

### 1.5 Calibration

| Parameter | Default | Range | Source |
|---|---|---|---|
| σ | 1.5 | [1.1, 2.0] | Acemoglu-Restrepo 2022 Table 3 |
| I (US 2025) | 0.41 | [0.35, 0.50] | Calibrated to BLS labor share 56% |
| N (US 2025) | 0.00 | [0.00, 0.25] | Reinstatement absent in baseline |
| dI/dt | 0.012/yr | [0.005, 0.030] | Acemoglu 2024 + AR 2014 calibration |
| dN/dt | 0.005/yr | [0.000, 0.020] | AR 2019 historical reinstatement rate |
| A_K growth | 0.020/yr | [0.005, 0.055] | v2.0 Cazzaniga IMF 2024 |
| A_L growth | 0.005/yr | [0.000, 0.015] | Historical labor-augmenting trend |

## 2. Firm markups (DLEU 2020)

Each firm i charges price p_i = μ_i · mc_i where μ_i ≥ 1 is the firm-
specific markup. Aggregate (sales-weighted) markup:

```
μ̄ = Σ_i s_i · μ_i
```

where s_i is firm i's revenue share. Profit share of value-added:

```
π / Y = Σ_i s_i · (μ_i - 1) / μ_i
```

Markups distributed Pareto-lognormal with positive size-markup
correlation (DLEU 2020 §4).

### 2.1 Realized vs factor labor share

The simulator distinguishes:

```
labor_share_factor = L_eff / (K_eff + L_eff)            [production model]
labor_share_realized = labor_share_factor · (1/μ̄) · monopsony_markdown
```

The realized share is what BLS reports. The factor share is the
production-side intermediate. Confusing them is the documented
failure mode in `CLAUDE.md`.

### 2.2 Calibration

| Parameter | Default 2025 | 2036 projection | Source |
|---|---|---|---|
| μ̄ (US) | 1.220 | 1.280 | DLEU 2020 + post-DeepSeek update |
| μ̄ growth rate | 0.0044/yr | (v2.0: 0.0020/yr) | DLEU trend + 2025 update |
| Pareto-lognormal std | 0.30 | — | DLEU 2020 Fig 6 |
| Top firm markup | 2.14 | — | DLEU 99th percentile |

## 3. Monopsonistic labor markets (Azar-Marinescu-Steinbaum 2022)

Wage paid by a monopsonistic employer:

```
w = (ε / (ε + 1)) · MRPL
```

where ε is firm-specific labor supply elasticity. Wage markdown =
1/(ε+1). Lower ε = stronger monopsony power.

### 3.1 Skill differential

Wages and markdowns differ by skill type:

- AI-safe labor (manual, personal services): ε_safe
- AI-substitute labor (clerical, cognitive routine): ε_sub
- AI-complement labor (high-skill cognitive): ε_comp

Webber (2015) finds higher-skill workers face less monopsony, so
ε_comp > ε_safe > ε_sub typically.

### 3.2 Calibration

| Parameter | Default | Source |
|---|---|---|
| ε_safe | 9.0 | Azar-Marinescu-Steinbaum 2022 calibrated to 56% labor share |
| ε_sub | 9.0 | Same baseline; degrades over time |
| ε_comp | 13.5 | Webber 2015 (1.5 × ε_safe) |
| ε_sub decay | 0.20/yr | Worsening outside options under AI displacement |

## 4. Wealth dynamics (Piketty 2014; Saez-Zucman 2016; Fagereng et al. 2020)

The fundamental wealth concentration mechanism is r > g with
differential returns by wealth tier. For household h:

```
W_{h,t+1} = (1 + r_h) · W_{h,t} + S_h - C_h + B_h
```

where:
- r_h — household's realized return
- S_h — labor income
- C_h — consumption
- B_h — net inheritance flow

Top decile households earn a differential return:

```
r_top = r_baseline + δ_top
```

where δ_top is the documented top-decile premium.

### 4.1 Inheritance flow

Top decile households additionally receive inheritance flows
recirculating within the top decile, preserving concentration across
generations:

```
B_top,t = ρ_inherit · W_top,t-1
```

where ρ_inherit is the inheritance recirculation rate
(Piketty-Postel-Vinay-Rosenthal 2014).

### 4.2 Calibration

| Parameter | Default | Source |
|---|---|---|
| r_baseline | 0.04/yr | Risk-free + equity premium baseline |
| δ_top | 0.020/yr | Saez-Zucman 2016 |
| ρ_inherit | 0.015/yr | Piketty-Postel-Vinay-Rosenthal 2014 |

## 5. Aggregate equilibrium

Each period t resolves in this sequence (per SIMULATION.md §1.5):

1. **Update productivity:** A_K, A_L grow per scenario rates.
2. **Update automation:** I rises by dI, N by dN.
3. **Update markups:** μ_i shifts per scenario; Pillar 5 dampens if active.
4. **Update monopsony:** ε_sub falls; Pillar 4 buffers if active.
5. **Aggregate factor supplies:** L_eff (by skill), K_productive.
6. **Production yields Y, r, w_unit via §1 equations.**
7. **Markups extract profit share π = Y · markup_share.**
8. **Monopsony extracts further rents from labor payments.**
9. **Sovereign fund (Pillar 1) acquires fraction of new top-decile AI capital.**
10. **Household incomes determined: wage by skill × markdown, capital × (r + premium),
    dividend, less AI tax.**
11. **Households consume per MPC; save residual.**
12. **Wealth updates per §4 with differential returns.**
13. **Capital flight responds to bilateral tax/policy differential.**
14. **Depreciation: K_T at δ_T, K_AI at δ_AI.**
15. **Inheritance recirculates within top decile.**

## 6. Reduced-form trajectory mechanism (simulator implementation)

The v0.2 simulator implements a *reduced-form* approximation of the
above structural model. Instead of solving the full equilibrium per
period, it applies calibrated rate equations:

```
labor_share(t) = labor_share(t-1) · (1 - decay_rate)
top_1pct(t) = top_1pct(t-1) · (1 + growth_rate)
markup(t) = markup(t-1) · (1 + markup_growth_rate)
real_gdp(t) = real_gdp(t-1) · (1 + gdp_growth_rate)
sub_emp(t) = sub_emp(t-1) · (1 - sub_emp_decay)
```

The decay/growth rates are calibrated to BASELINE_2026.md §3 central
values. This trades structural derivation for tractability — see
`CLAUDE.md` 2026-05-01 addendum for the justification.

A full structural rebuild on HARK or Sequence Space Jacobian is
Phase 9 of the project roadmap. The reduced-form approach is
appropriate for *comparative* claims (Δ vs. status quo) but not for
*level* claims.

## 7. Out-of-sample validation

The trajectory mechanism is validated out-of-sample via
`src/analysis/out_of_sample.py`:

- Fit decay/growth rates from 2015–2019 observed data.
- Project forward to 2020–2025.
- Compare predictions to actual observed values.

Result: 8/9 indicators predict within documented tolerance from a
2015–2019 training window. Substitute-worker employment fails
tolerance due to COVID-era disruption (2020 shock). See OOS report.

## 8. Lever effect specification

Each policy lever modifies one or more trajectory rates or applies an
additive shift to a final-year value. The specifications are in
`src/packages/*.py`. Lever interactions
(`src/core/interactions.py`) apply multiplicative corrections to the
policy-induced delta to capture substitutability and complementarity.

## 9. Welfare aggregation

The Atkinson-Sen social welfare function aggregates decile incomes
under a parameterized inequality aversion ε:

```
W(ε) = [(1/N) Σ y_i^(1-ε)]^(1/(1-ε))   for ε ≠ 1
W(1) = exp[(1/N) Σ ln(y_i)]              for ε = 1
W(∞) = min_i y_i                          (Rawlsian)
```

See `src/analysis/welfare.py`. The paper reports rankings across
ε ∈ {0, 0.5, 1, 2, 5} so reviewers can apply their own prior on
inequality aversion.

## 10. RDM uncertainty propagation

Latin Hypercube samples are drawn from the parameter ranges in
`src/analysis/rdm.py:UNCERTAINTY_RANGES` (literature-anchored per
`PREREGISTRATION.md` §7 and v2.0 updates in `EMPIRICAL_ANALOGS.md`
§7.1, §7.4):

| Parameter | Range | Source |
|---|---|---|
| σ | [1.1, 2.0] | Acemoglu-Restrepo 2022 |
| ε_flight | [0.002, 0.012] | v2.0 Jakobsen + Saez-Zucman |
| Reskilling effect | [0.05, 0.20] | Card-Kluve-Weber 2018 + Brookings 2024 |
| Open-weights dampening | [0.05, 0.35] | v2.0 post-DeepSeek |
| AI productivity growth | [0.005, 0.055] | v2.0 Cazzaniga IMF 2024 |
| US-China cooperation θ | [0.05, 0.95] | Declared subjective |
| Coalition share | [0.30, 1.00] | Coalition formation test |

Shared-sample LHS ensures valid policy-regret comparison across packages.

## 11. Causal attribution (mechanism decomposition)

The simulator's projected change in any indicator can be decomposed
across mechanisms by toggling each channel on/off in isolation
(`src/analysis/mechanism_decomposition.py`):

- Automation
- Markup expansion
- Worker bargaining decline
- Wealth concentration dynamics
- AI productivity boost

For 2025→2036 US labor-share decline at default calibration:
- Automation: ~67% of decline
- Worker bargaining decline: ~33%
- Markup, wealth-concentration, productivity: small or counter-acting

This is approximate (channels interact); a Shapley decomposition would
be more rigorous. Reported as a methodological aid rather than as a
settled causal claim.

## 12. Limitations of the formal specification

- The reduced-form trajectory bypasses the full structural model.
  Level claims are not directly validated; comparative deltas are.
- Lucas critique applies to all rate parameters under regime change.
  Mitigation via RDM uncertainty propagation is partial.
- AI productivity is treated as exogenous to policy in most levers;
  Package F (Build-Different-AI) is the exception.
- Geopolitical layer is illustrative per PREREGISTRATION.md Tier D.

See `paper/sections/10_limitations.md` for full limitations document.
