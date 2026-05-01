# Calibration

This directory contains the records of every calibration run. Calibration is the process of finding parameter values that, when run through the model, reproduce observed empirical targets. **All calibration must be reproducible.**

## What goes in this directory

- `grid_searches/` — outputs of automated grid searches over parameter space, one JSON file per run with timestamp
- `sensitivity/` — outputs of sensitivity analyses (one-at-a-time and Sobol-style)
- `baseline_2015.py` — the script that finds parameters reproducing US 2015 baseline
- `baseline_2025.py` — the script that finds parameters reproducing US 2025 baseline (current state)
- `validation_2015_2025.py` — the backtest script: runs `baseline_2015.py` parameters forward and compares to observed 2025 data

## Calibration targets

### US 2015 baseline (the start of backtest)
- Labor share = 58.0% (BLS Q4 2015)
- Top 1% wealth share = 28% (Saez-Zucman)
- Mean markup (sales-weighted) = 1.18 (DLEU 2020)
- AI capital share of total = ~2% (estimated)
- Capital-output ratio K/Y ≈ 4.0 (Penn World Tables)

### US 2025 baseline (current state)
- Labor share = 56% (BLS most recent)
- Top 1% wealth share = 30% (SCF 2022 projected)
- Mean markup = 1.22 (estimated, post-DLEU update)
- AI capital share of total = ~6% (estimated; has grown rapidly since 2020)

### Backtest validation (2015 → 2025 forward)
Running the `baseline_2015` parameters forward 10 years should produce values within ±2pp of the 2025 baseline targets. If the model can't pass this test, no further claims are warranted.

## Output format for calibration runs

Each run produces a JSON file with this structure:

```json
{
  "run_id": "20260427T103000_baseline_2025",
  "timestamp": "2026-04-27T10:30:00Z",
  "purpose": "Find I, sigma, eps that reproduce US 2025 labor/profit/capital shares",
  "search_space": {
    "I": [0.18, 0.42, 25],
    "sigma": [0.7, 1.5, 9],
    "eps": [4.0, 20.0, 17]
  },
  "targets": {
    "labor_share": 0.56,
    "profit_share": 0.18
  },
  "best_fit": {
    "params": {"I": 0.26, "sigma": 1.0, "eps": 9.0},
    "achieved": {"labor_share": 0.560, "profit_share": 0.171},
    "loss": 0.0001
  },
  "sensitivity": {
    "I_sensitivity": [...],
    "sigma_sensitivity": [...],
    "eps_sensitivity": [...]
  },
  "code_version": "git commit hash",
  "data_version": "data/raw/ as of 2026-04-25"
}
```

## Discipline rules

- Re-run calibration whenever (a) the model code changes meaningfully, (b) raw data is updated, or (c) the literature changes (e.g., new DLEU updates).
- Don't manually edit calibration outputs.
- The "official" calibrated parameters are those output by the most recent successful `baseline_2025.py` run, written into `src/scenarios/base.py` via a script.
- If the model can't pass the backtest validation, the parameters are wrong, the model structure is wrong, or both — fix the underlying issue rather than tuning the calibration to mask it.
