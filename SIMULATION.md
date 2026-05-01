# SIMULATION.md — Technical Specification

> **Purpose:** This document specifies the simulation in enough detail that any module can be implemented, tested, and validated independently. It is the technical contract between the project's intent (`CLAUDE.md`), schedule (`ROADMAP.md`), parameter sources (`SOURCES.md`), and the actual code.
>
> **Audience:** Claude Code instances executing the roadmap, plus any future macro economist reviewing the methodology.
>
> **Maintenance:** When implementation diverges from this spec, update the spec. Do not let the code and spec drift apart.

---

## Table of contents

1. [Mathematical foundations](#1-mathematical-foundations)
2. [Module: Production (`src/production/`)](#2-module-production)
3. [Module: Firms (`src/firms/`)](#3-module-firms)
4. [Module: Labor (`src/labor/`)](#4-module-labor)
5. [Module: Capital markets (`src/capital/`)](#5-module-capital-markets)
6. [Module: Households (`src/households/`)](#6-module-households)
7. [Module: Countries (`src/countries/`)](#7-module-countries)
8. [Module: Geopolitics (`src/geopolitics/`)](#8-module-geopolitics)
9. [Module: Scenarios (`src/scenarios/`)](#9-module-scenarios)
10. [Module: Core simulator (`src/core/`)](#10-module-core-simulator)
11. [Module: Analysis (`src/analysis/`)](#11-module-analysis)
12. [Test suite (`tests/`)](#12-test-suite)
13. [Calibration protocol](#13-calibration-protocol)
14. [Validation targets](#14-validation-targets)
15. [Output artifacts](#15-output-artifacts)

---

## 1. Mathematical foundations

The simulation integrates four theoretical frameworks. Their formal relationships are:

### 1.1 Task-based production (Acemoglu-Restrepo 2018, 2019, 2022)

Output Y is produced from a continuum of tasks indexed z ∈ [0, 1+N]:

```
Y = B · [∫₀ᴵ q_K(z)^((σ-1)/σ) dz + ∫_I^(1+N) q_L(z)^((σ-1)/σ) dz]^(σ/(σ-1))
```

where:
- **I** ∈ [0, 1+N] is the automation threshold; tasks z < I performed by capital, z ≥ I by labor
- **N** ≥ 0 is new tasks added at the labor-eligible end
- **σ > 0** is task elasticity of substitution
- **q_K(z), q_L(z)** are productivity at task z

For tractability, productivities are uniform within each region: q_K = A_K, q_L = A_L. Capital allocated equally across [0, I], labor across [I, 1+N]:

```
Y = [I^(1/σ) · (A_K K)^((σ-1)/σ) + (1+N-I)^(1/σ) · (A_L L)^((σ-1)/σ)]^(σ/(σ-1))
```

Cobb-Douglas limit (σ → 1):

```
Y = (A_K K)^α · (A_L L)^(1-α)   where α = I/(1+N)
```

**Three core comparative statics (validation tests):**
1. **Displacement:** ∂(labor share)/∂I < 0 — automating tasks lowers labor share
2. **Reinstatement:** ∂(labor share)/∂N > 0 — new tasks raise labor share
3. **Productivity bias:** ∂(labor share)/∂A_K < 0 when σ > 1 — capital-augmenting tech with σ > 1 lowers labor share

### 1.2 Heterogeneous firm markups (De Loecker-Eeckhout-Unger 2020)

Each firm i charges price p_i = μ_i · mc_i where μ_i ≥ 1 is its markup. Aggregate (sales-weighted) markup:

```
μ̄ = Σ_i s_i · μ_i   where s_i is firm i's revenue share
```

Profit (rents above competitive returns) as share of value-added:

```
π/Y = Σ_i s_i · (μ_i - 1)/μ_i
```

Markups distributed Pareto-lognormal with positive size-markup correlation (DLEU 2020, Section 4).

### 1.3 Monopsonistic labor markets (Azar-Marinescu-Steinbaum 2022)

Wage paid by monopsonistic employer:

```
w = ε/(ε+1) · MRPL
```

where ε is the firm-specific labor supply elasticity. Wage markdown = 1/(ε+1). Lower ε = more monopsony power.

Wages and markdowns differ by skill type:
- AI-safe labor: ε_safe (manual occupations, moderate monopsony)
- AI-substitute labor: ε_sub (clerical/cognitive routine, high monopsony exposure as AI-displaceability worsens outside options)
- AI-complement labor: ε_comp (high-skill cognitive, low monopsony — high mobility)

### 1.4 Wealth dynamics (Piketty 2014, Saez-Zucman 2016, Fagereng et al. 2020)

The fundamental wealth concentration mechanism is r > g with differential returns by wealth tier. For household h:

```
W_{h,t+1} = (1 + r_h) · W_{h,t} + S_h - C_h + B_h
```

where:
- **r_h** is the household's realized return, with r_top > r_median (Saez-Zucman estimates ~150-250 bps differential)
- **S_h** is labor income, **C_h** consumption, **B_h** net inheritance flow
- **r_h** decomposes into r_safe (risk-free) + r_premium (risk premium scaled by portfolio composition)

Top decile households additionally receive **inheritance flows** that recirculate within the top decile, preserving concentration across generations (Piketty-Postel-Vinay-Rosenthal 2014).

### 1.5 General equilibrium

Each period t resolves in this sequence:

1. **Update productivity:** A_K, A_L grow per scenario
2. **Update automation:** I rises (displacement), N rises (reinstatement)
3. **Update markups:** μ_i shifts per scenario; Pillar 5 dampens
4. **Update monopsony:** ε_sub falls (worse outside options); Pillar 4 buffers
5. **Aggregate factor supplies:** L_eff (by skill), K_productive (excluding fled capital)
6. **Production yields Y, r, w_unit per task-based formula**
7. **Markups extract π = Y · profit_share as rents to capital owners**
8. **Monopsony extracts further rents from labor payments**
9. **Sovereign fund (Pillar 1) acquires fraction of new top-decile AI capital; pays dividend**
10. **Household incomes determined: wage by skill × markdown, capital × (r + premium for top), dividend, less AI tax (Pillar 6)**
11. **Households consume per MPC; save residual**
12. **Wealth updates: K_T and K_AI by household, with differential returns**
13. **Capital flight: fraction of top-1% mobile AI capital responds to tax differential**
14. **Depreciation: K_T at δ_T, K_AI at δ_AI**
15. **Inheritance recirculates within top decile**

---

## 2. Module: Production (`src/production/`)

### 2.1 File: `src/production/__init__.py`

```python
from src.production.task_based import TaskBasedProduction

__all__ = ["TaskBasedProduction"]
```

### 2.2 File: `src/production/task_based.py`

Implements §1.1 above.

**Class signature:**

```python
@dataclass
class TaskBasedProduction:
    I: float = 0.50           # automation threshold
    N: float = 0.00           # new tasks
    A_K: float = 1.0          # capital-augmenting productivity
    A_L: float = 1.0          # labor-augmenting productivity
    sigma: float = 1.5        # task elasticity
    
    def output(self, K: float, L: float) -> ProductionResult:
        """Returns Y, r (marginal product of capital), w_unit (per effective L), labor_share."""
    
    def update_automation(self, dI: float, dN: float) -> None:
        """Apply automation expansion and reinstatement."""
        self.I = min(0.95, self.I + dI)
        self.N = self.N + dN
    
    def update_productivity(self, gK: float, gL: float) -> None:
        """Apply growth rates to A_K and A_L."""
        self.A_K *= (1 + gK)
        self.A_L *= (1 + gL)
```

**Return type:**

```python
@dataclass
class ProductionResult:
    Y: float
    r: float                  # marginal product of capital
    w_unit: float             # marginal product per unit effective labor
    labor_share_factor: float # before markups/monopsony
```

**Cobb-Douglas branch:** when |σ - 1| < 0.02, use closed-form:

```python
alpha = self.I / (1.0 + self.N)
Y = (self.A_K * K) ** alpha * (self.A_L * L) ** (1.0 - alpha)
r = alpha * Y / K
w_unit = (1.0 - alpha) * Y / L
labor_share = 1.0 - alpha
```

**General CES branch:** σ ≠ 1:

```python
rho = (self.sigma - 1) / self.sigma
K_term = (self.I ** (1.0 / self.sigma)) * (self.A_K * K) ** rho
L_share_tasks = 1.0 + self.N - self.I
L_term = (L_share_tasks ** (1.0 / self.sigma)) * (self.A_L * L) ** rho
bracket = K_term + L_term
Y = bracket ** (self.sigma / (self.sigma - 1))
# Factor shares = term / bracket; r = (Y/K) * K_share, w = (Y/L) * L_share
```

**Edge cases to handle:**
- K ≤ 0 or L ≤ 0: return ProductionResult(0, 0, 0, 0)
- I ≥ 1+N (no labor tasks): degenerate, raise ValueError
- bracket ≤ 0 from numerical issues: return ProductionResult(0, 0.05, 1.0, 0)

### 2.3 Tests: `tests/test_production.py`

Required tests:
1. `test_symmetric`: I=0.5, N=0, A=1, K=L=1 → labor share ≈ 0.5
2. `test_displacement`: increasing I lowers labor share
3. `test_reinstatement`: increasing N raises labor share
4. `test_capital_augmenting_sigma_above_1`: A_K↑ with σ=1.5 lowers labor share
5. `test_capital_augmenting_sigma_below_1`: A_K↑ with σ=0.7 raises labor share (theoretically opposite)
6. `test_cobb_douglas_limit`: σ=0.99 vs σ=1.01 produce labor shares within 0.005 of each other
7. `test_zero_inputs`: K=0 returns Y=0, r=0
8. `test_calibration_target`: I=0.26, σ=1.0 produces labor_share_factor ≈ 0.74 (then markups+monopsony bring to ~0.56)

---

## 3. Module: Firms (`src/firms/`)

### 3.1 File: `src/firms/markup_distribution.py`

Implements §1.2 above.

**Class signature:**

```python
@dataclass
class FirmDistribution:
    n_firms: int = 1000
    markup_mean: float = 1.22
    markup_dispersion: float = 0.30
    correlation_size_markup: float = 0.6  # DLEU 2020 documented positive corr
    
    markups: np.ndarray = field(default_factory=lambda: np.array([]))
    sizes: np.ndarray = field(default_factory=lambda: np.array([]))
    ai_intensity: np.ndarray = field(default_factory=lambda: np.array([]))
    
    def initialize(self, seed: int = 42) -> None:
        """Sample firm distribution from calibrated parameters."""
    
    def aggregate_markup(self) -> float:
        """Sales-weighted average markup."""
        return float(np.sum(self.markups * self.sizes))
    
    def profit_share(self) -> float:
        """Aggregate pure profit share of value-added."""
        return float(np.sum((self.markups - 1.0) / self.markups * self.sizes))
    
    def update_markups(
        self, 
        growth_rate: float, 
        ai_concentration_factor: float = 1.5,
        open_weights_dampening: float = 0.0
    ) -> None:
        """
        Markups grow over time. Top quintile (frontier AI firms) get amplified growth.
        Pillar 5 (open_weights_dampening > 0) suppresses growth in top quintile.
        """
    
    def top_quintile_indices(self) -> np.ndarray:
        """Indices of firms in top markup quintile (frontier AI)."""
```

**Initialization algorithm:**

```
1. Draw raw markups: log-normal, std = markup_dispersion
2. Draw raw sizes: Pareto, shape = 2.0
3. Sort sizes descending; assign top (correlation_size_markup × n_firms) sizes 
   to top markup firms (positive correlation), shuffle the rest
4. Scale raw markups so SALES-WEIGHTED mean equals markup_mean
5. Set markups = max(markups, 1.01)
6. Sort by markup descending so index 0 = largest markup firm
7. Assign ai_intensity: top quintile = 1.0, next quintile = 0.5, rest = 0.1
```

**Validation:** after initialization with markup_mean=1.22, dispersion=0.30:
- aggregate_markup() should return value in [1.20, 1.27]
- profit_share() should return value in [0.15, 0.20]
- 99th percentile markup should be in [1.6, 2.5]

### 3.2 Tests: `tests/test_firms.py`

Required tests:
1. `test_initialization_hits_target_mean`: target ~1.22, achieved within ±0.05
2. `test_size_markup_correlation`: Pearson correlation between size and markup ≥ 0.4
3. `test_markup_floor`: all markups ≥ 1.01
4. `test_growth_concentrates_in_top`: after `update_markups(0.005, ai_concentration_factor=1.5)`, top quintile mean grew faster than rest
5. `test_open_weights_dampening`: with dampening=1.0, top quintile growth = bottom quintile growth
6. `test_dleu_99th_percentile`: P99 markup in calibrated baseline matches DLEU 2020 (~2.0)

---

## 4. Module: Labor (`src/labor/`)

### 4.1 File: `src/labor/monopsony.py`

Implements §1.3 above.

**Class signature:**

```python
@dataclass
class MonopsonyLabor:
    eps_safe: float = 10.0    # AI-safe workers
    eps_sub: float = 9.0      # AI-substitute workers (most exposed)
    eps_comp: float = 15.0    # AI-complement workers (high mobility)
    
    def wage_markdown(self, skill_type: SkillType) -> float:
        """Returns ε/(ε+1) for the given skill type."""
    
    def update_for_ai_displacement(
        self, 
        ai_displacement_intensity: float,
        reskilling_buffer: float = 0.0,
    ) -> None:
        """
        AI displacement worsens outside options for substitute workers.
        Pillar 4 reskilling_buffer ∈ [0, 1] dampens this effect.
        """
        shock = ai_displacement_intensity * (1 - reskilling_buffer)
        self.eps_sub = max(2.0, self.eps_sub * (1 - shock))
        self.eps_safe = max(2.5, self.eps_safe * (1 - shock * 0.5))
        # eps_comp unchanged (complement workers gain options as AI augments their work)
```

**Skill type:**

```python
class SkillType(IntEnum):
    SAFE = 0       # manual, personal services (Frey-Osborne low-risk)
    SUBSTITUTE = 1 # clerical, cognitive routine (Frey-Osborne high-risk)
    COMPLEMENT = 2 # high-skill cognitive (AI-augmented)
```

**Aggregation function:**

```python
def aggregate_economy(
    K: float,
    L_safe: float, L_sub: float, L_comp: float,
    production: TaskBasedProduction,
    firms: FirmDistribution,
    monopsony: MonopsonyLabor,
    skill_productivity: dict[SkillType, float] | None = None,
) -> EconomyAggregate:
    """
    Returns:
        Y, factor returns by skill, profit share, monopsony rents, 
        capital return with rents, realized labor share.
    """
```

**Algorithm:**

```
1. L_eff = φ_safe·L_safe + φ_sub·L_sub + φ_comp·L_comp
   (skill_productivity defaults: φ_safe=0.7, φ_sub=1.0, φ_comp=1.6)
2. ProductionResult = production.output(K, L_eff)
3. profit_rents = Y * firms.profit_share()
4. Y_factor = Y - profit_rents (paid to factors at marginal product)
5. capital_payment = Y_factor * (1 - labor_share_factor)
6. labor_payment_total = Y_factor * labor_share_factor
7. Distribute labor payment by skill share of L_eff:
     pay_safe = labor_payment_total * (φ_safe·L_safe / L_eff)
     pay_sub  = labor_payment_total * (φ_sub·L_sub / L_eff)
     pay_comp = labor_payment_total * (φ_comp·L_comp / L_eff)
8. Apply monopsony markdowns:
     realized_safe = pay_safe * monopsony.wage_markdown(SAFE)
     realized_sub  = pay_sub * monopsony.wage_markdown(SUBSTITUTE)
     realized_comp = pay_comp * monopsony.wage_markdown(COMPLEMENT)
9. monopsony_rents = (pay - realized) summed across skills
10. total_capital_income = capital_payment + profit_rents + monopsony_rents
11. realized_labor_share = (realized_safe + sub + comp) / Y
12. wage_per_unit by skill = realized_X / L_X
```

### 4.2 Tests: `tests/test_labor.py`

Required tests:
1. `test_wage_markdown_formula`: ε=3 → markdown = 0.75
2. `test_high_eps_no_monopsony`: ε=100 → markdown ≈ 1.0
3. `test_displacement_worsens_substitute`: applying displacement shock lowers eps_sub
4. `test_reskilling_buffer`: with buffer=1.0, eps_sub unchanged after shock
5. `test_complement_unaffected`: eps_comp unchanged across all displacement scenarios
6. `test_aggregate_economy_calibration`: with US 2025 parameters (I=0.26, σ=1.0, eps=9, markup_mean=1.22), realized labor share = 0.56 ± 0.02

---

## 5. Module: Capital markets (`src/capital/`)

### 5.1 File: `src/capital/capital_markets.py`

Implements §1.4 wealth dynamics plus investment dynamics and capital flight.

**This is the module that requires the most new work** — the prototype version lacked the Piketty mechanism.

**Class signatures:**

```python
@dataclass
class CapitalMarkets:
    # Cost of equity
    cost_of_equity_baseline: float = 0.07
    cost_of_equity_premium_per_decile_acquired: float = 0.005  # 50bps per 10% sov
    
    # Investment dynamics (Caballero-Engel adjustment costs)
    beta_q: float = 0.05
    beta_y: float = 0.4
    beta_r: float = 0.08
    
    # Capital flight (Bach-Bourdier-Bozio 2014)
    flight_responsiveness: float = 0.008  # per pp tax differential
    flight_baseline: float = 0.005
    
    # Depreciation
    depreciation_AI: float = 0.22       # IEEE ComSoc 2025
    depreciation_T: float = 0.05        # BLS MFP series
    
    # Differential returns (Saez-Zucman 2016, Fagereng et al. 2020)
    return_premium_top_decile: float = 0.020   # 200 bps
    return_premium_top_1pct: float = 0.035     # 350 bps over baseline
    
    def cost_of_equity(self, sov_acquisition_share: float) -> float:
        """Required equity return rises with sovereign concentration."""
    
    def investment_demand(
        self, K: float, Y: float, Y_growth: float,
        r_realized: float, r_required: float, q: float = 1.0
    ) -> float:
        """Net new investment (before depreciation replacement)."""
    
    def capital_flight_rate(self, domestic_tax: float, foreign_tax: float) -> float:
        """Annual flight rate as function of tax differential."""
    
    def returns_by_decile(self, base_r: float) -> np.ndarray:
        """
        Differential returns by wealth decile (10 entries; top 1% as 11th).
        Implements Saez-Zucman: top decile gets baseline + premium, top 1% 
        gets baseline + larger premium.
        """
        returns = np.full(11, base_r)  # index 10 = top 1%
        returns[9] = base_r + self.return_premium_top_decile  # top decile ex top 1%
        returns[10] = base_r + self.return_premium_top_1pct
        return returns
```

```python
@dataclass
class InheritanceFlow:
    """
    Piketty-Postel-Vinay-Rosenthal 2014.
    Each year, fraction of top-decile wealth transfers within top decile,
    preserving concentration.
    """
    annual_transfer_rate: float = 0.015  # 1.5% of top-decile wealth recirculates
    
    def apply(self, wealth: np.ndarray, top_decile_indices: np.ndarray) -> np.ndarray:
        """Mutates wealth array to reflect inheritance recirculation."""
        # Transfer from younger top-decile to next-generation top-decile
        # In aggregate effect: redistributes within top decile, preserving total
        # Mechanism: each year, transfer_rate × top_decile_wealth gets reshuffled
        # among top_decile_indices with random recipient pattern
```

```python
@dataclass
class TobinsQ:
    """
    Asset price dynamics for AI capital. q = market_value / replacement_cost.
    When q > 1, investment accelerates; q < 1, slows.
    """
    q_current: float = 1.0
    momentum_factor: float = 0.7  # AR(1) coefficient
    fundamentals_weight: float = 0.3
    
    def update(self, Y_growth: float, ai_capital_share: float) -> None:
        """Update q based on growth expectations and AI hype/bust dynamics."""
```

**Capital flight mechanics:**

```python
def execute_capital_flight(
    K_AI_top1: float,
    domestic_tax: float, foreign_tax: float,
    cm: CapitalMarkets,
    cumulative_flight: float = 0.0,
) -> tuple[float, float]:
    """
    Returns (K_AI_remaining, K_AI_fled_this_period).
    Only top 1% AI capital is mobile (institutional / personal complexity barriers).
    Once fled, capital does not return within the simulation horizon.
    """
    rate = cm.capital_flight_rate(domestic_tax, foreign_tax)
    fled = K_AI_top1 * rate
    return K_AI_top1 - fled, fled
```

### 5.2 Tests: `tests/test_capital.py`

Required tests:
1. `test_cost_of_equity_rises_with_sov`: 0% sov → 7.0%; 30% sov → 8.5%
2. `test_flight_zero_at_no_differential`: domestic = foreign → flight rate = 0.5% (baseline only)
3. `test_flight_calibration_bach_2014`: 5pp differential → ~4.5%/yr flight
4. `test_returns_by_decile_monotone`: returns[9] > returns[5] > returns[0]
5. `test_top_1pct_premium`: returns[10] - returns[9] = 150 bps
6. `test_inheritance_preserves_top_decile_total`: applying inheritance does not change sum of top-decile wealth (only reshuffles)
7. `test_piketty_steady_state`: in isolation (no production, no labor income), Piketty differential returns produce steady-state top-1% share that grows over time, validating the r > g mechanism
8. `test_depreciation_rates`: AI capital halves in ~3 years (consistent with 22%/yr); traditional capital halves in ~14 years

---

## 6. Module: Households (`src/households/`)

### 6.1 File: `src/households/household_economy.py`

Heterogeneous household population calibrated to SCF 2022.

**Class signature:**

```python
@dataclass
class HouseholdEconomy:
    n_per_decile: int = 1000      # 10,000 total + 100 for top 1%
    
    # SCF 2022 wealth distribution
    wealth_decile: list = field(default_factory=lambda: [
        0.001, 0.003, 0.005, 0.008, 0.013, 0.020, 0.033, 0.060, 0.097, 0.760
    ])
    top1_wealth_share: float = 0.304  # SCF 2022
    
    # Labor endowment (units of effective labor) by decile
    labor_endow_decile: list = field(default_factory=lambda: [
        0.5, 0.7, 0.9, 1.0, 1.2, 1.5, 1.9, 2.5, 3.5, 6.0
    ])
    top1_labor_endow: float = 15.0
    
    # MPC by decile (Saez-Zucman, Mian-Straub-Sufi)
    mpc_decile: list = field(default_factory=lambda: [
        0.95, 0.95, 0.95, 0.93, 0.91, 0.87, 0.83, 0.78, 0.70, 0.55
    ])
    top1_mpc: float = 0.40
    
    # Saving rates (negative for bottom deciles in steady state)
    saving_decile: list = field(default_factory=lambda: [
        -0.02, 0.00, 0.01, 0.02, 0.04, 0.06, 0.10, 0.15, 0.22, 0.30
    ])
    top1_saving: float = 0.40
    
    # Skill type by decile (Frey-Osborne 2017 + BLS occupation-decile mapping)
    skill_decile: list = field(default_factory=lambda: [
        SkillType.SAFE, SkillType.SAFE,  # bottom 20%
        SkillType.SUBSTITUTE, SkillType.SUBSTITUTE, SkillType.SUBSTITUTE,
        SkillType.SUBSTITUTE, SkillType.SUBSTITUTE,  # middle 50%
        SkillType.COMPLEMENT, SkillType.COMPLEMENT, SkillType.COMPLEMENT  # top 30%
    ])
    
    def initialize(self, total_wealth: float = 4000.0) -> HouseholdState:
        """Create N=10,100 household state arrays. Total wealth calibrated to K/Y ~ 4."""

@dataclass
class HouseholdState:
    wealth_T: np.ndarray          # traditional capital per household
    wealth_AI: np.ndarray         # AI capital per household
    labor_endow: np.ndarray
    mpc: np.ndarray
    saving_rate: np.ndarray
    skill: np.ndarray             # SkillType values
    decile_index: np.ndarray      # 0-9 for normal, 10 for top 1%
    
    def total_wealth(self) -> np.ndarray:
        return self.wealth_T + self.wealth_AI
```

**Initialization algorithm:**

```
N_normal = 10 * n_per_decile  (e.g. 10,000)
N_top1   = n_per_decile // 100  (e.g. 100, representing 1% of pop)
N_total  = N_normal              (top 1% are last 100 of D10)

For each decile d in 0..9:
    wealth[d*n10:(d+1)*n10] = wealth_decile[d] * total_wealth / n_per_decile
    labor_endow[d*n10:(d+1)*n10] = labor_endow_decile[d]
    mpc, saving, skill similarly

For top 1% (last 100 of D10):
    next_99_share = wealth_decile[9] - top1_wealth_share
    wealth[9*n10:N-100] = next_99_share * total_wealth / (N-100 - 9*n10)
    wealth[N-100:] = top1_wealth_share * total_wealth / 100
    labor_endow[N-100:] = top1_labor_endow
    mpc[N-100:] = top1_mpc
    saving[N-100:] = top1_saving
    skill[N-100:] = COMPLEMENT
    decile_index[N-100:] = 10  # special index for top 1%

Initial split between K_T and K_AI:
    Top decile (incl. top 1%): 90% T, 10% AI (will drift toward AI)
    All other deciles: 98% T, 2% AI
```

### 6.2 Tests: `tests/test_households.py`

Required tests:
1. `test_initialization_matches_scf`: top 1% share within 0.5pp of 0.304
2. `test_top_10_percent_share`: top 10% share within 1pp of 0.760
3. `test_population_count`: total N = 10,000 households
4. `test_top_1_pct_count`: 100 households in top 1%
5. `test_skill_distribution`: 20% SAFE, 50% SUBSTITUTE, 30% COMPLEMENT (within 1%)
6. `test_capital_split_initial`: top decile holds ≥60% of K_AI; bottom 50% holds ≤2% of K_AI

---

## 7. Module: Countries (`src/countries/`)

### 7.1 File: `src/countries/country.py`

Each country is a self-contained economy plus a set of cross-border flows.

**Class signature:**

```python
@dataclass
class Country:
    name: str
    tier: Tier                          # FRONTIER / EMERGING / DEVELOPING
    population: float                   # millions
    pop_growth_rate: float              # annual, may be negative
    
    # Initial conditions (2025)
    gdp_pc: float                       # USD
    K_per_Y: float                      # capital-output ratio
    labor_share_t0: float
    top1_wealth_share_t0: float
    ai_capital_share_t0: float          # K_AI / K_total
    
    # Country-specific calibrated parameters
    state_capacity: float = 1.0         # 0..1, scales policy effectiveness
    
    # State at runtime
    households: HouseholdState
    production: TaskBasedProduction
    firms: FirmDistribution
    monopsony: MonopsonyLabor
    capital_markets: CapitalMarkets
    sov_K_AI: float = 0.0
    fled_K_AI: float = 0.0
    
    # Cross-border state
    inference_rents_received: float = 0.0   # net per period
    inference_rents_paid: float = 0.0

class Tier(IntEnum):
    FRONTIER = 0
    EMERGING = 1
    DEVELOPING = 2
```

**Country library:**

```python
COUNTRIES = {
    "USA": Country(
        name="USA", tier=Tier.FRONTIER, population=340, pop_growth_rate=0.005,
        gdp_pc=80000, K_per_Y=4.0, labor_share_t0=0.56, 
        top1_wealth_share_t0=0.304, ai_capital_share_t0=0.06,
        state_capacity=0.85,  # high but not Norwegian
    ),
    "EU": Country(
        name="EU", tier=Tier.FRONTIER, population=450, pop_growth_rate=0.001,
        gdp_pc=42000, K_per_Y=4.5, labor_share_t0=0.58,
        top1_wealth_share_t0=0.25, ai_capital_share_t0=0.03,
        state_capacity=0.90,
    ),
    "China": Country(
        name="China", tier=Tier.FRONTIER, population=1410, pop_growth_rate=-0.002,
        gdp_pc=15000, K_per_Y=5.0, labor_share_t0=0.51,
        top1_wealth_share_t0=0.31, ai_capital_share_t0=0.04,
        state_capacity=0.80,
    ),
    "UK": Country(
        name="UK", tier=Tier.FRONTIER, population=68, pop_growth_rate=0.005,
        gdp_pc=55000, K_per_Y=4.0, labor_share_t0=0.57,
        top1_wealth_share_t0=0.23, ai_capital_share_t0=0.02,
        state_capacity=0.82,
    ),
    "Japan": Country(
        name="Japan", tier=Tier.FRONTIER, population=124, pop_growth_rate=-0.005,
        gdp_pc=42000, K_per_Y=5.5, labor_share_t0=0.58,
        top1_wealth_share_t0=0.18, ai_capital_share_t0=0.03,
        state_capacity=0.88,
    ),
    "India": Country(
        name="India", tier=Tier.EMERGING, population=1430, pop_growth_rate=0.008,
        gdp_pc=2900, K_per_Y=3.5, labor_share_t0=0.50,
        top1_wealth_share_t0=0.40, ai_capital_share_t0=0.005,
        state_capacity=0.55,
    ),
    "Brazil": Country(
        name="Brazil", tier=Tier.EMERGING, population=216, pop_growth_rate=0.003,
        gdp_pc=10000, K_per_Y=3.0, labor_share_t0=0.45,
        top1_wealth_share_t0=0.49, ai_capital_share_t0=0.005,
        state_capacity=0.60,
    ),
    "Indonesia": Country(
        name="Indonesia", tier=Tier.EMERGING, population=280, pop_growth_rate=0.007,
        gdp_pc=5000, K_per_Y=3.0, labor_share_t0=0.48,
        top1_wealth_share_t0=0.45, ai_capital_share_t0=0.003,
        state_capacity=0.50,
    ),
    "Mexico": Country(
        name="Mexico", tier=Tier.EMERGING, population=130, pop_growth_rate=0.006,
        gdp_pc=11000, K_per_Y=3.0, labor_share_t0=0.42,
        top1_wealth_share_t0=0.43, ai_capital_share_t0=0.003,
        state_capacity=0.55,
    ),
    "Nigeria": Country(
        name="Nigeria", tier=Tier.DEVELOPING, population=225, pop_growth_rate=0.024,
        gdp_pc=2200, K_per_Y=2.5, labor_share_t0=0.42,
        top1_wealth_share_t0=0.45, ai_capital_share_t0=0.001,
        state_capacity=0.35,
    ),
    "SSA_other": Country(  # aggregate sub-Saharan Africa ex-Nigeria/SA
        name="SSA_other", tier=Tier.DEVELOPING, population=900, pop_growth_rate=0.025,
        gdp_pc=1500, K_per_Y=2.0, labor_share_t0=0.38,
        top1_wealth_share_t0=0.50, ai_capital_share_t0=0.001,
        state_capacity=0.30,
    ),
}
```

**Cross-border flows:**

```python
@dataclass
class TradeFlows:
    """
    Cross-border flows of AI services (inference, model rental).
    
    Calibrated to actual hyperscaler cross-border revenue (~$50B/yr in 2024,
    growing rapidly), normalized to per-capita basis.
    
    Inference fees flow from Emerging/Developing to Frontier;
    the Open-Weights pillar (Pillar 5) reduces this flow by providing
    accessible alternatives.
    """
    base_rent_emerging_to_frontier_pc: float = 50.0   # USD per capita per year, 2025
    base_rent_developing_to_frontier_pc: float = 15.0
    
    growth_rate_no_pillar5: float = 0.10              # 10%/yr growth as AI dependency deepens
    pillar5_reduction: float = 0.0                    # 0 = no Pillar 5, 1 = full open-weights
    
    def compute_flows(self, t: int, countries: dict[str, Country]) -> dict:
        """Returns per-country net inference rent flow."""
```

**Coalition formation (light-touch):**

```python
@dataclass
class Coalition:
    """
    Tracks which countries have adopted the Participatory framework.
    
    Adoption is a binary state per country. Joining is rational when
    expected benefit (median voter welfare) exceeds expected cost
    (top decile pushback).
    
    This is illustrative, not a fully derived game-theoretic equilibrium.
    """
    members: set[str] = field(default_factory=set)
    
    def evaluate_joining(
        self, country: Country, 
        domestic_outcome_difference: float,
        coalition_size_effect: float,
    ) -> bool:
        """Returns True if country should join given current state."""
```

### 7.2 Tests: `tests/test_countries.py`

Required tests:
1. `test_country_initialization`: USA initial state matches inputs
2. `test_population_weights_sum`: total modeled population ~ 5.6B (covers most of world)
3. `test_tier_assignments`: all FRONTIER countries have GDP/cap > $15K
4. `test_state_capacity_ranges`: all in [0, 1]; FRONTIER avg > EMERGING avg > DEVELOPING avg
5. `test_inference_flow_direction`: Emerging/Developing pay; Frontier receives
6. `test_pillar5_reduces_flow`: with pillar5_reduction=1.0, flows drop by ≥80%

---

## 8. Module: Geopolitics (`src/geopolitics/`)

### 8.1 File: `src/geopolitics/stability_index.py`

**Caveat: this layer is illustrative, not predictive.** The IR literature on whether bipolar splits produce conflict is contested (Mearsheimer says yes, Ikenberry says not necessarily, Allison says only at power-transition moments). Component scores and weights are calibrated to recent observed events.

**Class signature:**

```python
@dataclass
class StabilityIndex:
    """
    Six-component aggregate index, 0-100 scale (higher = more unstable).
    
    Components calibrated from documented 2024-2026 events:
    - Ukraine/Gaza/Iran AI warfare deployment (interstate)
    - Election interference in 15+ countries (info warfare)
    - US-China chip export controls / Stargate / HUMAIN (arms race)
    """
    
    interstate_conflict: float       # weight 0.25
    substate_conflict: float         # weight 0.15
    info_warfare: float              # weight 0.15
    coercion: float                  # weight 0.15
    arms_race: float                 # weight 0.20
    governance_capacity: float       # weight 0.10 (inverse: high score reduces instability)
    
    def aggregate(self) -> float:
        """Weighted aggregate, 0-100."""
    
    def update_from_configuration(
        self, 
        coalition_size: int,
        cross_border_cooperation: float,
        ai_arms_race_intensity: float,
    ) -> None:
        """Updates components based on world configuration."""
```

**World configurations:**

```python
class WorldConfiguration(IntEnum):
    UNIPOLAR_US = 0           # US dominance, others client states
    BIPOLAR_SPLIT = 1         # Hard US-China bifurcation (current)
    MULTIPOLAR_FRAGMENTED = 2 # Patchwork: 50+ national stacks
    MULTIPOLAR_REGIONAL = 3   # Pillar 3: regional cooperation
    COOPERATIVE = 4           # Full Participatory
```

**Component update rules** (illustrative):

```
INTERSTATE_CONFLICT:
  base = 70 (current Ukraine/Iran level)
  + 10 if BIPOLAR_SPLIT or MULTIPOLAR_FRAGMENTED
  - 25 if cooperative_participatory
  drift over time: +1.5/yr in bipolar, -1.5/yr in cooperative

ARMS_RACE:
  base = 70
  + 10 if zero coalition members
  - 30 if coalition includes US, EU, China simultaneously
  
GOVERNANCE_CAPACITY:
  base = 25 (post-2025 multilateral atrophy)
  + 50 × (coalition_size / 10)
  + 20 × cross_border_cooperation
```

### 8.2 Tests: `tests/test_geopolitics.py`

Required tests:
1. `test_aggregate_in_range`: aggregate always in [0, 100]
2. `test_cooperative_lower_than_bipolar`: cooperative_participatory aggregate < bipolar_split aggregate
3. `test_governance_inversion`: high governance reduces aggregate
4. `test_component_clipping`: components clipped to [0, 100]
5. `test_baseline_calibration`: 2026 baseline aggregate matches "current world" estimate (~67-72)

---

## 9. Module: Scenarios (`src/scenarios/`)

### 9.1 File: `src/scenarios/base.py`

**The single source of truth for all scenario parameters.**

```python
@dataclass(frozen=True)
class Scenario:
    name: str
    description: str
    
    # AI productivity & automation
    ai_tfp_growth: float                  # annual TFP growth from AI
    automation_rate: float                # dI/dt
    reinstatement_rate: float             # dN/dt
    
    # Markups & monopsony
    markup_growth: float                  # mean markup growth per year
    monopsony_tightening: float           # eps_sub decline rate per year
    
    # AI productivity ramp (for SF Consensus-style scenarios)
    ai_tfp_growth_end: float | None = None  # if set, linear ramp from start to end
    automation_rate_end: float | None = None
    
    # Pillar 1: sovereign equity fund
    sov_acquisition_rate: float = 0.0
    sov_acquisition_cap: float = 0.30
    
    # Pillar 4: portable benefits / reskilling
    reskilling_buffer: float = 0.0        # 0..1
    
    # Pillar 5: open-weights public infrastructure
    open_weights_markup_dampening: float = 0.0   # 0..1
    open_weights_inference_rent_reduction: float = 0.0  # 0..1
    
    # Pillar 6: progressive AI taxation
    ai_tax_rate_top1: float = 0.0
    ai_tax_rate_top10: float = 0.0
    
    # Foreign jurisdiction tax (for capital flight)
    foreign_tax_rate: float = 0.0
    
    # Coalition state
    participating_countries: tuple[str, ...] = ()
    
    def get_param_at_t(self, param: str, t: int, T: int) -> float:
        """If param has start/end, linearly interpolate; else return constant."""
```

### 9.2 File: `src/scenarios/historical_backtest.py`

```python
HISTORICAL_BACKTEST = Scenario(
    name="historical_2015_2025",
    description="US 2015-2025 backtest. Calibration target: reproduce labor share, top 1% wealth share, mean markup, GDP growth within 2pp.",
    ai_tfp_growth=0.012,         # observed productivity slowdown
    automation_rate=0.010,
    reinstatement_rate=0.005,
    markup_growth=0.0035,        # DLEU pace
    monopsony_tightening=0.02,
)
```

### 9.3 Other scenario files

```
src/scenarios/slow_diffusion.py      # Acemoglu 2024: 0.7% TFP over decade
src/scenarios/goldman_base.py         # Briggs-Kodnani: 1.5%/yr AI productivity
src/scenarios/sf_consensus.py         # IMF 2026: AGI-adjacent ramp
src/scenarios/patchwork.py            # current organic trajectory
src/scenarios/participatory_universal.py  # full framework, all countries
src/scenarios/participatory_capflight.py  # framework + 5pp tax differential
src/scenarios/participatory_frontier_only.py  # only Frontier countries adopt
src/scenarios/participatory_acceleration.py   # framework + SF Consensus speed
src/scenarios/coerced_redistribution.py       # post-2032 70% windfall tax
```

Each defines a Scenario instance and exports it. The CLI loads scenarios by name.

### 9.4 Parameter table (reference)

| Param | Patchwork | SF Consensus | Participatory Univ. | Coerced |
|---|---|---|---|---|
| ai_tfp_growth | 0.018 | 0.030→0.050 (ramp) | 0.018 | 0.005 |
| automation_rate | 0.018 | 0.030 | 0.018 | 0.008 |
| reinstatement_rate | 0.004 | 0.003 | 0.012 | 0.003 |
| markup_growth | 0.005 | 0.008 | 0.005 | 0.0 |
| monopsony_tightening | 0.04 | 0.06 | 0.04 | -0.02 |
| sov_acquisition_rate | 0 | 0 | 0.05 | 0 |
| reskilling_buffer | 0 | 0 | 0.50 | 0 |
| open_weights_markup_damp | 0 | 0 | 0.40 | 0 |
| open_weights_rent_reduction | 0 | 0 | 0.70 | 0 |
| ai_tax_rate_top1 | 0 | 0 | 0.40 | 0.70 |
| foreign_tax_rate | 0 | 0 | 0.10 | 0 |

### 9.5 Tests: `tests/test_scenarios.py`

Required tests:
1. `test_scenario_immutable`: Scenario instances are frozen dataclasses
2. `test_all_scenarios_loadable`: every scenario file exports a valid Scenario
3. `test_pillar_consistency`: participatory scenarios have non-zero pillar 1, 4, 5, 6 parameters; non-participatory have zero
4. `test_ramp_interpolation`: SF Consensus get_param_at_t at t=0 returns start, at t=T-1 returns end

---

## 10. Module: Core simulator (`src/core/`)

### 10.1 File: `src/core/simulator.py`

**The integrated dynamic model.** Brings together all modules into an annual time-step simulation.

**Top-level API:**

```python
def run_simulation(
    scenario: Scenario,
    n_years: int = 11,
    start_year: int = 2025,
    seed: int = 42,
    countries: list[str] | None = None,  # None = single-country US
) -> SimulationResult:
    """
    Run integrated dynamic simulation.
    
    Returns time series of all key indicators for each country and aggregate.
    """

@dataclass
class SimulationResult:
    scenario_name: str
    years: np.ndarray
    
    # Aggregate (per country)
    by_country: dict[str, CountryResult]
    
    # World aggregate
    world: WorldResult
    
    # Geopolitical (if multi-country)
    stability: StabilityResult | None
    
    # Metadata
    seed: int
    git_commit: str
    runtime_seconds: float
```

```python
@dataclass
class CountryResult:
    Y: np.ndarray
    gdp_pc: np.ndarray
    labor_share_realized: np.ndarray
    profit_share: np.ndarray
    monopsony_rents_share: np.ndarray
    top1_wealth_share: np.ndarray
    top10_wealth_share: np.ndarray
    bot50_wealth_share: np.ndarray
    gini_wealth: np.ndarray
    gini_income: np.ndarray
    p90_p10_income: np.ndarray
    poverty_headcount: np.ndarray  # below 50% of 2025 median
    median_real_income: np.ndarray
    
    consumption_by_decile: np.ndarray  # shape (T, 10)
    income_by_decile: np.ndarray
    wage_by_skill: dict[SkillType, np.ndarray]
    
    sov_share_AI: np.ndarray
    fled_share_AI: np.ndarray
    
    K_per_Y: np.ndarray
    r_capital: np.ndarray
    
    I_threshold: np.ndarray   # automation threshold trajectory
    N_new_tasks: np.ndarray
    mean_markup: np.ndarray
```

### 10.2 Annual time step (the master loop)

```python
def step_year(
    state: SimulationState,
    scenario: Scenario,
    t: int, T: int,
) -> SimulationState:
    """One year of simulation. Mutates state, returns updated."""
    
    # 1. Update production parameters
    for country in state.countries.values():
        net_disp = scenario.get_param_at_t('automation_rate', t, T) * (1 - 0.5 * scenario.reskilling_buffer)
        net_reinst = scenario.reinstatement_rate + scenario.automation_rate * 0.5 * scenario.reskilling_buffer
        country.production.update_automation(dI=net_disp, dN=net_reinst)
        country.production.update_productivity(
            gK=scenario.get_param_at_t('ai_tfp_growth', t, T),
            gL=scenario.get_param_at_t('ai_tfp_growth', t, T) * 0.2,
        )
    
    # 2. Update markups
    for country in state.countries.values():
        eff_markup_growth = scenario.markup_growth * (1 - scenario.open_weights_markup_dampening)
        country.firms.update_markups(eff_markup_growth, ai_concentration_factor=1.5)
    
    # 3. Update monopsony
    for country in state.countries.values():
        country.monopsony.update_for_ai_displacement(
            ai_displacement_intensity=scenario.monopsony_tightening,
            reskilling_buffer=scenario.reskilling_buffer,
        )
    
    # 4. Compute cross-border inference rent flows
    flows = state.trade_flows.compute_flows(t, state.countries)
    for name, country in state.countries.items():
        country.inference_rents_received = flows[name]['received']
        country.inference_rents_paid = flows[name]['paid']
    
    # 5. Aggregate per country
    for country in state.countries.values():
        country_step(country, scenario, t)
    
    # 6. Update geopolitics
    if state.stability is not None:
        state.stability.update_from_configuration(
            coalition_size=len(scenario.participating_countries),
            cross_border_cooperation=...,
            ai_arms_race_intensity=...,
        )
    
    return state


def country_step(country: Country, scenario: Scenario, t: int) -> None:
    """One year of dynamics for a single country."""
    
    # 1. Aggregate labor by skill
    L_safe = sum(country.households.labor_endow[country.households.skill == SkillType.SAFE])
    L_sub  = sum(country.households.labor_endow[country.households.skill == SkillType.SUBSTITUTE])
    L_comp = sum(country.households.labor_endow[country.households.skill == SkillType.COMPLEMENT])
    
    # Apply effective labor adjustments per scenario
    if not country.is_participating(scenario):
        L_sub *= max(0.4, 1 - 0.045 * t)  # cumulative sub-worker displacement
    else:
        L_sub *= max(0.6, 1 - 0.020 * t)  # Pillar 4 reskilling
    
    # 2. Aggregate capital
    K_total = country.households.total_wealth().sum() + country.sov_K_AI
    K_productive = K_total  # fled capital already excluded
    
    # 3. Production aggregation
    agg = aggregate_economy(
        K=K_productive, L_safe=L_safe, L_sub=L_sub, L_comp=L_comp,
        production=country.production,
        firms=country.firms,
        monopsony=country.monopsony,
    )
    
    # 4. Compute incomes
    incomes = compute_household_incomes(country, agg)
    
    # 5. Apply cross-border rents
    if country.tier == Tier.FRONTIER and country.inference_rents_received > 0:
        # Distribute rents to top decile (frontier-AI capital owners)
        top10_idx = country.households.decile_index >= 9
        incomes[top10_idx] += country.inference_rents_received / top10_idx.sum()
    elif country.tier in (Tier.EMERGING, Tier.DEVELOPING):
        # Outflow reduces aggregate income proportionally
        incomes *= (1 - country.inference_rents_paid / max(agg.Y, 1e-9))
    
    # 6. Apply taxes
    if country.is_participating(scenario):
        top1_idx = country.households.decile_index == 10
        top10_idx = (country.households.decile_index == 9)
        cap_income = compute_capital_income(country, agg)
        incomes[top1_idx] -= cap_income[top1_idx] * scenario.ai_tax_rate_top1
        incomes[top10_idx] -= cap_income[top10_idx] * scenario.ai_tax_rate_top10
    
    # 7. Consumption and saving
    consumption = np.maximum(incomes * country.households.mpc, country.subsistence_floor())
    saving = incomes - consumption
    
    # 8. Update wealth (with differential returns by decile)
    base_r = agg.capital_return_with_rents
    returns = country.capital_markets.returns_by_decile(base_r)
    for d in range(11):
        decile_mask = country.households.decile_index == d
        # Wealth grows at decile-specific rate
        country.households.wealth_T[decile_mask] *= (1 + returns[d] - country.capital_markets.depreciation_T)
        country.households.wealth_AI[decile_mask] *= (1 + returns[d] - country.capital_markets.depreciation_AI)
        # Add saving to wealth (allocated K_T vs K_AI per current proportions)
        wealth_T_share = country.households.wealth_T[decile_mask] / np.maximum(
            country.households.total_wealth()[decile_mask], 1e-9
        )
        country.households.wealth_T[decile_mask] += saving[decile_mask] * wealth_T_share
        country.households.wealth_AI[decile_mask] += saving[decile_mask] * (1 - wealth_T_share)
    
    # 9. Pillar 1: sovereign acquisition
    if scenario.sov_acquisition_rate > 0:
        top10_K_AI = country.households.wealth_AI[country.households.decile_index >= 9].sum()
        if country.sov_K_AI / max(top10_K_AI + country.sov_K_AI, 1e-9) < scenario.sov_acquisition_cap:
            acquire = top10_K_AI * scenario.sov_acquisition_rate
            country.sov_K_AI += acquire
            country.households.wealth_AI[country.households.decile_index >= 9] *= (1 - scenario.sov_acquisition_rate)
    
    # 10. Capital flight
    if scenario.ai_tax_rate_top1 > scenario.foreign_tax_rate:
        rate = country.capital_markets.capital_flight_rate(
            scenario.ai_tax_rate_top1, scenario.foreign_tax_rate
        )
        top1_idx = country.households.decile_index == 10
        flight = country.households.wealth_AI[top1_idx].sum() * rate
        country.households.wealth_AI[top1_idx] *= (1 - rate)
        country.fled_K_AI += flight
    
    # 11. Inheritance recirculation
    inheritance = InheritanceFlow(annual_transfer_rate=0.015)
    inheritance.apply(
        country.households.wealth_T + country.households.wealth_AI,
        top_decile_indices=np.where(country.households.decile_index >= 9)[0]
    )
    
    # 12. Record results
    record_country_metrics(country, agg, incomes, consumption, t)
```

### 10.3 CLI

```python
# src/core/cli.py
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scenario', required=True)
    parser.add_argument('--years', type=int, default=11)
    parser.add_argument('--start-year', type=int, default=2025)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--countries', nargs='+', default=['USA'])
    parser.add_argument('--monte-carlo', type=int, default=1)
    parser.add_argument('--output', type=str, default='calibration/scenario_runs/')
    args = parser.parse_args()
    
    if args.monte_carlo == 1:
        result = run_simulation(...)
    else:
        result = run_monte_carlo(..., n_draws=args.monte_carlo)
    
    save_result(result, args.output)
```

### 10.4 Tests: `tests/test_simulator.py`

Required tests:
1. `test_runs_to_completion`: every scenario runs without crashing for 11 years
2. `test_deterministic`: same seed produces identical results
3. `test_aggregate_constraints`: total wealth per country = household sum + sov + fled
4. `test_no_negative_consumption`: consumption ≥ subsistence floor for all households at all times
5. `test_top1_share_bounded`: top 1% wealth share ∈ [0.05, 0.60] across all scenarios
6. `test_labor_share_bounded`: labor share ∈ [0.20, 0.80] across all scenarios

---

## 11. Module: Analysis (`src/analysis/`)

### 11.1 File: `src/analysis/inequality_metrics.py`

```python
def gini(x: np.ndarray) -> float: ...
def p90_p10(x: np.ndarray) -> float: ...
def top_share(x: np.ndarray, fraction: float) -> float: ...
def atkinson_index(x: np.ndarray, epsilon: float = 0.5) -> float: ...
def poverty_headcount(consumption: np.ndarray, poverty_line: float) -> float: ...
```

### 11.2 File: `src/analysis/monte_carlo.py`

Parameter uncertainty done properly.

```python
def sample_param_set(seed: int) -> dict[str, float]:
    """
    Draw one parameter set from literature-anchored distributions.
    Each distribution traces to SOURCES.md.
    """
    rng = np.random.default_rng(seed)
    return {
        'sigma_KL': float(np.clip(rng.normal(1.5, 0.15), 1.1, 2.0)),  # AR 2022
        'ai_tfp_growth': float(np.clip(rng.lognormal(np.log(0.015), 0.45), 0.003, 0.040)),
        'depreciation_AI': float(np.clip(rng.normal(0.22, 0.04), 0.10, 0.30)),
        'inv_elasticity': float(np.clip(rng.normal(0.40, 0.15), 0.10, 0.80)),
        'cap_flight_rate': float(np.clip(rng.normal(0.008, 0.003), 0.002, 0.020)),
        'return_premium_top_decile': float(np.clip(rng.normal(0.020, 0.005), 0.010, 0.030)),
        # ...
    }


def run_monte_carlo(
    scenario: Scenario, 
    n_draws: int = 500,
    n_years: int = 11,
    countries: list[str] | None = None,
) -> MonteCarloResult:
    """Returns P10/P50/P90 trajectories for every metric."""


@dataclass
class MonteCarloResult:
    """Same shape as SimulationResult, but each metric is a tuple (p10, p50, p90)."""
```

### 11.3 File: `src/analysis/sensitivity.py`

```python
def one_at_a_time_sensitivity(
    base_scenario: Scenario,
    parameter_ranges: dict[str, tuple[float, float]],
    metric: str = 'top1_wealth_share',
) -> pd.DataFrame:
    """For each parameter, vary across range; record metric sensitivity."""


def sobol_sensitivity(
    base_scenario: Scenario,
    parameter_ranges: dict[str, tuple[float, float]],
    n_samples: int = 1024,
) -> dict[str, float]:
    """Total-effect Sobol indices via SALib."""
```

### 11.4 File: `src/analysis/chart_builders.py`

Each function in this file produces one figure for the white paper. All figures use Nebulai brand styling.

```python
NEBULAI_COLORS = {
    'purple': '#7C3AED',
    'indigo': '#1E1B4B',
    'lavender': '#F5F3FF',
    'body': '#374151',
    'meta': '#6B7280',
}

def fig_1_status_quo_diagnostic(results: dict) -> Figure: ...
def fig_2_organic_convergence(...) -> Figure: ...
def fig_3_six_pillars_compounding(...) -> Figure: ...
def fig_4_adoption_equilibrium_by_region(...) -> Figure: ...
def fig_5_decile_consumption_change(...) -> Figure: ...
def fig_6_capital_flight_sensitivity(...) -> Figure: ...
def fig_7_geopolitical_stability(...) -> Figure: ...
def fig_8_pillar_decomposition(...) -> Figure: ...
def fig_9_coerced_counterfactual(...) -> Figure: ...
def fig_10_backtest_validation(...) -> Figure: ...

def generate_all_paper_figures(output_dir: Path) -> None:
    """Run all simulations and produce all figures. The reproducibility entry point."""
```

### 11.5 File: `src/analysis/data_pipelines/`

One file per dataset:
- `bls_loader.py` — load BLS labor share series, return cleaned DataFrame
- `scf_loader.py` — load SCF wealth distribution
- `dleu_loader.py` — load DLEU markup series
- `wid_loader.py` — load World Inequality Database top wealth shares
- `pwt_loader.py` — load Penn World Tables
- `oecd_ai_loader.py` — load OECD AI indicators

Each provides a `load_*` function that returns a properly-typed pandas DataFrame, and a `load_all()` aggregator.

### 11.6 Tests: `tests/test_analysis.py`

Required tests:
1. `test_gini_known_values`: gini([1,1,1,1,1]) = 0; gini([0,0,0,0,1]) ≈ 0.8
2. `test_p90_p10_calculation`
3. `test_monte_carlo_runs`: 50 draws complete without errors
4. `test_param_distributions_within_ranges`: 1000 samples all within clipping bounds
5. `test_data_loaders_return_dataframes`: each loader returns pandas DataFrame with expected columns

---

## 12. Test suite (`tests/`)

### 12.1 Test organization

```
tests/
├── conftest.py                     # shared fixtures (seeded RNG, calibrated baseline)
├── test_production.py
├── test_firms.py
├── test_labor.py
├── test_capital.py
├── test_households.py
├── test_countries.py
├── test_geopolitics.py
├── test_scenarios.py
├── test_simulator.py
├── test_analysis.py
└── test_calibration.py             # the master backtest test
```

### 12.2 Critical: `test_calibration.py::test_2015_2025_backtest`

**This is the test that determines whether the model is publishable.**

```python
def test_2015_2025_backtest():
    """
    Run baseline_2015 parameters forward 10 years, validate against US 2025 observed.
    
    All targets must be within ±2pp on percentage measures and ±10% on level measures.
    If any fail, the model is not publication-ready.
    """
    scenario = HISTORICAL_BACKTEST
    result = run_simulation(scenario, n_years=11, start_year=2015, countries=['USA'])
    
    usa = result.by_country['USA']
    
    # Labor share: BLS 2025
    assert abs(usa.labor_share_realized[-1] - 0.56) < 0.02, \
        f"Labor share: model {usa.labor_share_realized[-1]:.3f}, target 0.56"
    
    # Top 1% wealth share: SCF 2022 projected
    assert abs(usa.top1_wealth_share[-1] - 0.30) < 0.02, \
        f"Top 1% wealth: model {usa.top1_wealth_share[-1]:.3f}, target 0.30"
    
    # Mean markup: DLEU 2020 + extension
    assert abs(usa.mean_markup[-1] - 1.22) < 0.05, \
        f"Mean markup: model {usa.mean_markup[-1]:.3f}, target 1.22"
    
    # Cumulative GDP growth: BEA, real
    cumulative_growth = usa.gdp_pc[-1] / usa.gdp_pc[0] - 1.0
    assert abs(cumulative_growth - 0.22) < 0.05, \
        f"Cumulative GDP: model {cumulative_growth:.3f}, target 0.22"
```

### 12.3 Continuous integration

```yaml
# .github/workflows/test.yml (or equivalent)
- run pytest with --cov
- run ruff check
- fail if calibration backtest fails
- fail if test coverage < 80%
```

---

## 13. Calibration protocol

### 13.1 Order of calibration

**Calibrate from inside out:**

1. **Production module** — fix σ, find I that hits target labor share factor (step in isolation)
2. **Firm distribution** — fix dispersion, find scale that hits target sales-weighted markup
3. **Monopsony** — find ε that, given production + firms calibration, hits target realized labor share
4. **Capital markets** — find return_premium values that match Saez-Zucman top-decile differential
5. **Integrated baseline 2015** — find combination of all above that reproduces 2015 state
6. **Integrated baseline 2025** — same for 2025
7. **Forward dynamics** — set scenario parameters so backtest 2015→2025 passes

### 13.2 Calibration targets (US, primary)

| Target | 2015 | 2025 | Source |
|---|---|---|---|
| Labor share | 0.58 | 0.56 | BLS |
| Top 1% wealth | 0.28 | 0.30 | SCF/Saez-Zucman |
| Top 10% wealth | 0.74 | 0.76 | SCF |
| Bottom 50% wealth | 0.025 | 0.025 | SCF |
| Mean markup (sales-weighted) | 1.18 | 1.22 | DLEU |
| Profit share | 0.13 | 0.17 | Barkai 2020 |
| K/Y | 4.0 | 4.0 | Penn World Tables |
| Cumulative real GDP growth | — | 0.22 | BEA |

### 13.3 Calibration script template

```python
# calibration/baseline_2025.py
def calibrate_2025() -> dict:
    """Find parameters reproducing US 2025 baseline."""
    
    targets = {
        'labor_share': 0.56,
        'top1_wealth_share': 0.30,
        'mean_markup': 1.22,
        'K_per_Y': 4.0,
    }
    
    best_params = None
    best_loss = float('inf')
    
    for I in np.linspace(0.18, 0.42, 25):
        for sigma in np.linspace(0.7, 1.5, 9):
            for eps in np.linspace(4.0, 20.0, 17):
                for markup_mean in [1.20, 1.22, 1.25]:
                    params = {'I': I, 'sigma': sigma, 'eps': eps, 'markup_mean': markup_mean}
                    achieved = evaluate_baseline(params)
                    loss = sum((achieved[k] - targets[k])**2 for k in targets)
                    if loss < best_loss:
                        best_loss = loss
                        best_params = params
    
    log_calibration_run(best_params, achieved, targets)
    return best_params
```

### 13.4 Sensitivity protocol

After baseline calibration:
1. Vary each parameter ±20% from calibrated value
2. Record effect on each target
3. Document elasticities in `calibration/sensitivity/baseline_2025_elasticities.csv`
4. If any elasticity exceeds 2.0 (highly sensitive), flag for sensitivity analysis in paper

---

## 14. Validation targets

### 14.1 Backtest validation (must pass before publication)

See §12.2.

### 14.2 Out-of-sample sanity checks

- Pre-2015 trajectory: model should produce 1990-2015 trends consistent with observed (labor share decline, markup rise)
- Cross-country: USA model parameters applied to Germany should produce labor share trajectory broadly similar to German actual (within 5pp)

### 14.3 Theoretical sanity checks (per-module)

Each module's tests cover its theoretical predictions. The full list is in §2.3, §3.2, §4.2, §5.2, §6.2, §7.2, §8.2, §9.5, §10.4, §11.6.

### 14.4 What the model is NOT validated for

- AGI emergence dynamics (not modeled; SF Consensus is parametric ramp, not derived)
- Financial crises / monetary instability (not modeled)
- Country-specific institutional details (state capacity is a single parameter)
- Fully-derived game-theoretic coalition formation (illustrative only)

These limitations are explicitly listed in the paper's `paper/sections/10_limitations.md`.

---

## 15. Output artifacts

### 15.1 Per-run outputs

Each simulation run produces:

```
calibration/scenario_runs/
└── {scenario_name}_{timestamp}/
    ├── meta.json                    # scenario, params, git commit, runtime
    ├── world_aggregate.parquet      # T × N_metrics
    ├── by_country/
    │   ├── USA.parquet
    │   ├── EU.parquet
    │   └── ...
    └── decile_panel.parquet         # T × N_countries × 10 deciles × N_metrics
```

### 15.2 Monte Carlo outputs

```
calibration/monte_carlo/
└── {scenario_name}_{timestamp}/
    ├── meta.json
    ├── parameter_draws.parquet      # n_draws × n_params
    ├── trajectories.parquet         # n_draws × T × N_metrics × N_countries
    └── summary_p10_p50_p90.parquet
```

### 15.3 Paper figures

```
paper/figures/
├── fig_01_status_quo_diagnostic.png
├── fig_01_status_quo_diagnostic.svg
├── fig_02_organic_convergence.png
├── ...
└── data/                            # JSON/CSV of underlying data per figure
    ├── fig_01_data.json
    └── ...
```

Each figure is regenerable via `python -m src.analysis.chart_builders --figure fig_01`.

### 15.4 Reproducibility manifest

After every paper version commit, regenerate:

```
paper/reproducibility/
├── manifest.yaml                    # git commits of code + data
├── parameters.yaml                  # all calibrated parameters
├── results_summary.yaml             # all numbers cited in paper
└── regenerate.sh                    # script that produces every figure from scratch
```

---

## Appendix A: Glossary

- **Pillar 1**: Universal AI Equity (sovereign equity fund + citizen dividend)
- **Pillar 2**: Tokenized Compute and Data Ownership
- **Pillar 3**: Sovereign AI Zones / Interoperable National Stacks
- **Pillar 4**: Reskilling and Portable Benefits
- **Pillar 5**: Open-Weights and Public AI Infrastructure
- **Pillar 6**: Progressive AI Taxation
- **Frontier**: high-capacity AI nations (US, EU, UK, China, Japan, Korea)
- **Emerging**: middle-tier (India, Brazil, Indonesia, Mexico, Turkey, South Africa)
- **Developing**: aggregate sub-Saharan Africa, smaller LATAM, parts of SE Asia
- **AI-safe labor**: low risk of AI displacement (manual, personal services)
- **AI-substitute labor**: high risk (clerical, cognitive routine)
- **AI-complement labor**: AI-augmented (high-skill cognitive)

## Appendix B: Notation summary

| Symbol | Meaning |
|---|---|
| Y | output (real GDP) |
| K | aggregate capital |
| K_T | traditional capital |
| K_AI | AI-specific capital |
| L | aggregate labor |
| L_safe, L_sub, L_comp | labor by skill type |
| I | automation threshold (Acemoglu-Restrepo) |
| N | new tasks added |
| σ | task elasticity of substitution |
| A_K, A_L | factor-augmenting productivity |
| μ | firm markup |
| ε | firm-specific labor supply elasticity (monopsony) |
| r | gross capital return |
| w | wage rate per unit effective labor |
| φ_skill | skill productivity multiplier |

## Appendix C: Implementation order

When starting a new session, check what's done by running `pytest`. Implement in this order:

1. ✅ Production module (`prototype/s1_production.py` ready to port)
2. ✅ Firms module (`prototype/s2_firms_labor.py` ready to port)
3. ✅ Labor module (`prototype/s2_firms_labor.py` ready to port)
4. ⬜ Households module (`prototype/s4_integrated.py` partial)
5. ⬜ Capital markets module (must add Piketty + Tobin's q)
6. ⬜ Single-country integrated simulator + 2015-2025 backtest
7. ⬜ Scenario library
8. ⬜ Monte Carlo + sensitivity
9. ⬜ Country disaggregation
10. ⬜ Geopolitics
11. ⬜ Chart builders + paper figures

Each step's exit criterion: tests pass, including any backtest validation that depends on it.

## Appendix D: Honest limitations

This simulation does NOT capture, by design:

1. **Financial sector dynamics** — no banks, no credit, no monetary policy. The framework treats the economy as a real-side phenomenon.
2. **AGI alignment risks** — if AGI arrives with recursive self-improvement, alignment failure dominates everything; that's a different paper.
3. **Sectoral / industry detail** — production is aggregate; no industry-by-industry analysis.
4. **Lifecycle / demographic structure** — households are time-invariant; no aging, no retirement, no entry/exit.
5. **Stochastic individual returns** — capital returns are decile-deterministic; idiosyncratic risk not modeled.
6. **Endogenous coalition formation** — countries' decisions to join Participatory are stipulated, not derived from a game-theoretic equilibrium.
7. **Trade in goods** — only AI services trade is modeled; rest of trade is exogenous.
8. **Labor market matching frictions** — wages clear at marginal product (with monopsony markdown); no unemployment beyond what's implied by displacement.
9. **Asset price bubbles in AI capital** — Tobin's q is included but its dynamics are simplified.
10. **Country-specific institutional detail** — state capacity is a single parameter; in reality, the institutional landscape varies enormously even within tiers.

Each of these is explicitly noted in the paper's limitations section. None of them are catastrophic for the paper's core claims, but each constrains what the simulation can be cited for.

## End of specification

This document is the technical contract. When in doubt, return here. When the implementation deviates, update the document. When something proves wrong, fix the document and the code together.
