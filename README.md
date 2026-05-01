# Nebulai — Participatory AI Economy Simulation

Macroeconomic simulation supporting the white paper *"The Participatory AI Economy: A Framework for Accelerated AI Development, Broadly Owned"* by Nebulai Corp.

## What's in this repo

A heterogeneous-agent macroeconomic model of the AI economic transition, calibrated to documented academic literature and validated against US 2015–2025 observed data, used to compare a range of policy architectures (status-quo "Patchwork," accelerationist "SF Consensus," the proposed Participatory framework, and a coerced-redistribution counterfactual).

The simulation produces the empirical content of the white paper's diagnostic and adoption-equilibrium sections.

## Theoretical foundations

The model integrates four strands of macro literature:

1. **Task-based production** — Acemoglu & Restrepo (2018, 2019, 2022) on automation, displacement, and reinstatement
2. **Heterogeneous firm markups** — De Loecker, Eeckhout & Unger (2020); Autor, Dorn, Katz, Patterson & Van Reenen (2020) on superstar firms and rising profit share
3. **Monopsonistic labor markets** — Azar, Marinescu & Steinbaum (2022); Manning (2003) on wage markdowns
4. **Wealth dynamics** — Piketty (2014); Saez & Zucman (2016) on the r > g mechanism and differential returns by wealth tier

## Quick start

```bash
# Install
uv sync  # or: pip install -e .

# Run tests
pytest

# Run baseline backtest
python -m src.core.simulator --scenario historical --start-year 2015 --years 11

# Run all main scenarios
python -m src.core.simulator --all-scenarios --monte-carlo 500

# Generate paper figures
python -m src.analysis.chart_builders --paper
```

## Project status

This is research-grade code under active development. The labor-share dynamics module is calibrated and validated; the wealth-concentration module is under construction; country disaggregation and geopolitical layers are planned.

See `CLAUDE.md` for the full project specification and `ROADMAP.md` for the work plan.

## License

Code: MIT. Paper drafts and substantive content: All rights reserved by Nebulai Corp pending publication.

## Citation

If using this simulation framework or its results, please cite the forthcoming white paper:

> Nebulai Corp (2026). *The Participatory AI Economy: A Framework for Accelerated AI Development, Broadly Owned.* Miami, FL.

## Contact

For research collaboration inquiries: partnerships@nebulai.com
