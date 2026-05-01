# Raw Data Provenance

Every dataset placed in this directory must be documented here with: source URL, download date, citation, and any preprocessing applied. **Do not modify files in this directory after download.** All cleaning happens via scripts that read from here and write to `data/processed/`.

## Datasets to acquire (Session 1)

### bls_labor_share.csv
- **Source:** US Bureau of Labor Statistics, Productivity Program
- **URL:** https://www.bls.gov/productivity/tables/labor-productivity-major-sectors.xlsx
- **Series:** Nonfarm business sector labor share, quarterly, 1990 Q1 – present
- **Citation:** US Bureau of Labor Statistics, Major Sector Productivity and Costs program.
- **Download date:** TBD
- **Used by:** Session 2 calibration; `tests/test_calibration.py` backtest validation

### scf_wealth_distribution.csv
- **Source:** Federal Reserve Board, Survey of Consumer Finances
- **URL:** https://www.federalreserve.gov/econres/scfindex.htm
- **Series:** Wealth percentile shares, triennial, 1989–2022
- **Specifically needed:** Top 1%, top 10%, top 50%, bottom 50% wealth shares
- **Citation:** Board of Governors of the Federal Reserve System, Survey of Consumer Finances 2022.
- **Download date:** TBD

### dleu_markup_series.csv
- **Source:** De Loecker, Eeckhout & Unger (2020) replication package
- **URL:** https://zenodo.org/records/3635404 (or Janet De Loecker's website)
- **Series:** US sales-weighted average markup, annual, 1955–2016
- **Citation:** De Loecker, J., Eeckhout, J., & Unger, G. (2020). The Rise of Market Power and the Macroeconomic Implications. *The Quarterly Journal of Economics*, 135(2), 561–644.
- **Download date:** TBD
- **Note:** Series ends in 2016; for 2017–2025 use updated estimates from Eeckhout's website or rely on Diez-Leigh-Tambunlertchai (IMF) updates.

### piketty_wid_top1.csv
- **Source:** World Inequality Database
- **URL:** https://wid.world
- **Series:** Top 1% wealth share, US, 1913–present (annual)
- **Citation:** World Inequality Lab, World Inequality Database, accessed [date].

### penn_world_tables.dta or .csv
- **Source:** Penn World Tables 11.0 (Groningen Growth and Development Centre)
- **URL:** https://www.rug.nl/ggdc/productivity/pwt/
- **Series:** Country-level capital stocks, output, labor share, total factor productivity, annual, 1950–present
- **Citation:** Feenstra, R. C., Inklaar, R., & Timmer, M. P. (2015). The Next Generation of the Penn World Table. *American Economic Review*, 105(10), 3150–3182.
- **Used by:** Session 8 country disaggregation

### oecd_ai_indicators.csv
- **Source:** OECD AI Policy Observatory
- **URL:** https://oecd.ai/en/data
- **Series:** Country-level AI investment, AI talent, AI patents, AI startup funding
- **Citation:** OECD AI Policy Observatory, accessed [date].

### saez_zucman_data/
- **Source:** Gabriel Zucman's website
- **URL:** https://gabriel-zucman.eu/usdina/
- **Series:** US distributional national accounts; wealth shares by percentile and asset type
- **Citation:** Saez, E., & Zucman, G. (2016). Wealth Inequality in the United States since 1913: Evidence from Capitalized Income Tax Data. *Quarterly Journal of Economics*, 131(2), 519–578.

### stanford_ai_index_2025.pdf
- **Source:** Stanford Institute for Human-Centered AI
- **URL:** https://aiindex.stanford.edu
- **Used for:** Foundation model counts by country, AI compute investment by country
- **Citation:** Maslej et al. (2025). The AI Index 2025 Annual Report.

## Format conventions

- All `.csv` files: UTF-8, comma-delimited, header row, dates in ISO format (YYYY-MM-DD)
- All numeric values in source units; conversion to model units happens in `data/processed/`
- File names: lowercase, snake_case, `.csv` extension preferred over `.xlsx`

## Refresh schedule

These datasets update at varying frequencies:
- BLS labor share: quarterly
- SCF wealth: triennial (next: 2025)
- DLEU markups: as updated by authors
- WID: annual
- Penn World Tables: ~every 2 years
- OECD AI indicators: annual

Refresh raw data at the start of any calibration revision session. Document update in `ROADMAP.md` decisions log.
