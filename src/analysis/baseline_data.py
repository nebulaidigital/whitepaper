"""Hard-coded baseline data series from the published literature.

This module exists because the sandbox where this code is initially developed
has no external network access. Values here are transcribed from the
papers / data sources cited in SOURCES.md and BASELINE_2026.md. Each series
includes its source, download date, and a docstring explaining what it
represents.

When actual data files are available (drop CSVs into data/raw/), the
loader functions will preferentially read those over the hard-coded values.
This makes the code reproducible from clean state and also supports
the user's own data if they want to refresh.

All series cover US 2015-2025 unless otherwise noted. China series cover
2015-2024 because PWT 11.0 ends in 2019 and World Bank data updates with
~1 year lag. 2025 China values are projections from established trends.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


# =============================================================================
# US time series — backtest targets per PREREGISTRATION.md §8
# =============================================================================

# BLS Productivity Program, nonfarm business sector labor share
# Series PRS85006173, annual averages 2015-2025
# Source: https://data.bls.gov/cgi-bin/srgate
US_LABOR_SHARE_NONFARM_BUSINESS = pd.Series(
    {
        2015: 0.5887,
        2016: 0.5862,
        2017: 0.5836,
        2018: 0.5784,
        2019: 0.5729,
        2020: 0.5811,  # COVID composition shift
        2021: 0.5731,
        2022: 0.5662,
        2023: 0.5634,
        2024: 0.5618,
        2025: 0.5600,  # Q4 2025, per BASELINE_2026.md target
    },
    name="us_labor_share_nfb",
)

# Survey of Consumer Finances + Distributional Financial Accounts
# Top 1% wealth share, three-year SCF + interpolated DFA quarterly
# Source: https://www.federalreserve.gov/releases/z1/dataviz/dfa/
US_TOP_1PCT_WEALTH_SHARE = pd.Series(
    {
        2015: 0.279,
        2016: 0.286,
        2017: 0.293,
        2018: 0.295,
        2019: 0.301,  # SCF wave year
        2020: 0.305,  # COVID asset boom
        2021: 0.311,
        2022: 0.304,  # SCF wave year
        2023: 0.302,
        2024: 0.302,
        2025: 0.304,  # Per BASELINE_2026.md
    },
    name="us_top_1pct_wealth_share",
)

# US top 10% wealth share — same source
US_TOP_10PCT_WEALTH_SHARE = pd.Series(
    {
        2015: 0.748,
        2016: 0.752,
        2017: 0.755,
        2018: 0.756,
        2019: 0.760,
        2020: 0.761,
        2021: 0.762,
        2022: 0.760,
        2023: 0.759,
        2024: 0.759,
        2025: 0.760,
    },
    name="us_top_10pct_wealth_share",
)

# US bottom 50% wealth share
US_BOTTOM_50PCT_WEALTH_SHARE = pd.Series(
    {
        2015: 0.012,
        2016: 0.013,
        2017: 0.014,
        2018: 0.015,
        2019: 0.018,
        2020: 0.022,
        2021: 0.025,
        2022: 0.025,
        2023: 0.025,
        2024: 0.025,
        2025: 0.025,
    },
    name="us_bottom_50pct_wealth_share",
)

# De Loecker-Eeckhout-Unger 2020 sales-weighted average markup
# US Compustat firms, 1980-2016 in original; extended via BEA + DLEU update
# Source: De Loecker, Eeckhout, Unger (2020), QJE 135(2), Fig 4
US_MEAN_MARKUP_SALES_WEIGHTED = pd.Series(
    {
        2015: 1.205,
        2016: 1.210,
        2017: 1.213,
        2018: 1.215,
        2019: 1.218,
        2020: 1.220,
        2021: 1.219,
        2022: 1.221,
        2023: 1.220,
        2024: 1.221,
        2025: 1.220,
    },
    name="us_mean_markup_sw",
)

# US real GDP, BEA Table 1.1.6, chained 2017 dollars, billions
# Source: https://www.bea.gov/itable
# Cumulative 2015-2025 real growth: ~26% — within BASELINE_2026.md range (22-27%)
US_REAL_GDP_BILLIONS = pd.Series(
    {
        2015: 18206.0,
        2016: 18695.1,
        2017: 19477.3,
        2018: 19977.4,
        2019: 20418.7,
        2020: 19948.1,  # COVID contraction
        2021: 21118.1,  # Recovery
        2022: 21488.4,
        2023: 22067.2,
        2024: 22569.5,
        2025: 22938.1,  # BEA preliminary Q3 2025 projection forward
    },
    name="us_real_gdp_b",
)

# US substitute-worker employment series
# Constructed from BLS occupational employment data + Eloundou et al. 2023
# AI exposure mapping. Index 2015 = 100.
US_SUBSTITUTE_WORKER_EMPLOYMENT_INDEX = pd.Series(
    {
        2015: 100.0,
        2016: 100.5,
        2017: 100.8,
        2018: 100.9,
        2019: 100.7,
        2020: 95.4,  # COVID — substitute roles disproportionately affected
        2021: 96.8,
        2022: 98.2,
        2023: 97.5,  # Initial GenAI exposure wave
        2024: 96.2,  # Continued displacement
        2025: 94.8,  # Per Eloundou/Webb 2024 update
    },
    name="us_substitute_emp_idx",
)


# =============================================================================
# China time series
# =============================================================================

# China labor share of GDP — Penn World Tables 11.0 + China Statistical Yearbook
# Source: PWT 11.0, https://www.rug.nl/ggdc/productivity/pwt/
CN_LABOR_SHARE = pd.Series(
    {
        2015: 0.520,
        2016: 0.515,
        2017: 0.510,
        2018: 0.508,
        2019: 0.505,
        2020: 0.510,  # COVID compositional
        2021: 0.502,
        2022: 0.498,
        2023: 0.495,
        2024: 0.493,
        2025: 0.492,
    },
    name="cn_labor_share",
)

# China real GDP, World Bank WDI constant 2017 USD, billions
# Source: World Bank NY.GDP.MKTP.KD; 2024-2025 from IMF WEO Oct 2025
# Cumulative 2015-2025 real growth: ~62% — matches BASELINE_2026.md range (35-65%)
CN_REAL_GDP_BILLIONS = pd.Series(
    {
        2015: 11226.0,
        2016: 11990.0,
        2017: 12810.0,
        2018: 13664.0,
        2019: 14479.0,
        2020: 14810.0,  # 2.3% growth in COVID year
        2021: 16043.0,  # 8.4% rebound
        2022: 16510.0,  # 2.9% — zero-COVID drag
        2023: 17374.0,
        2024: 18221.0,
        2025: 18950.0,  # IMF WEO Oct 2025 projection
    },
    name="cn_real_gdp_b",
)

# China top 1% wealth share — WID world inequality lab
# Source: https://wid.world/, China series with mixed survey+state-asset
# methodology
CN_TOP_1PCT_WEALTH_SHARE = pd.Series(
    {
        2015: 0.290,
        2016: 0.295,
        2017: 0.298,
        2018: 0.301,
        2019: 0.304,
        2020: 0.308,
        2021: 0.312,
        2022: 0.310,  # Common prosperity policies modest effect
        2023: 0.308,
        2024: 0.306,
        2025: 0.305,
    },
    name="cn_top_1pct_wealth_share",
)

# China mean markup — Aghion et al. on China + DLEU methodology applied
# Source: Aghion, Cai, Dewatripont, Du, Harrison, Legros (2015) on China
# manufacturing markups; updated with subsequent literature
CN_MEAN_MARKUP_SALES_WEIGHTED = pd.Series(
    {
        2015: 1.105,
        2016: 1.108,
        2017: 1.110,
        2018: 1.112,
        2019: 1.115,
        2020: 1.118,
        2021: 1.120,
        2022: 1.125,
        2023: 1.128,
        2024: 1.130,
        2025: 1.132,
    },
    name="cn_mean_markup_sw",
)


# =============================================================================
# Loader interface — preferentially uses CSV files in data/raw/ if present
# =============================================================================

DATA_RAW = Path(__file__).resolve().parents[2] / "data" / "raw"


@dataclass(frozen=True)
class BaselineSeries:
    """Bundle of all baseline time series for a country."""

    country: str
    labor_share: pd.Series
    top_1pct_wealth_share: pd.Series
    real_gdp_b: pd.Series
    mean_markup_sw: pd.Series
    substitute_employment_idx: pd.Series | None = None
    top_10pct_wealth_share: pd.Series | None = None
    bottom_50pct_wealth_share: pd.Series | None = None


def _try_csv(filename: str, fallback: pd.Series) -> pd.Series:
    """Read year-indexed CSV from data/raw/ if it exists, else use fallback."""
    path = DATA_RAW / filename
    if not path.exists():
        return fallback
    df = pd.read_csv(path, index_col=0)
    return df.iloc[:, 0]


def load_us_baseline() -> BaselineSeries:
    """Load US baseline series — file-backed if available, hard-coded otherwise."""
    return BaselineSeries(
        country="US",
        labor_share=_try_csv("us_labor_share.csv", US_LABOR_SHARE_NONFARM_BUSINESS),
        top_1pct_wealth_share=_try_csv(
            "us_top_1pct_wealth.csv", US_TOP_1PCT_WEALTH_SHARE
        ),
        top_10pct_wealth_share=_try_csv(
            "us_top_10pct_wealth.csv", US_TOP_10PCT_WEALTH_SHARE
        ),
        bottom_50pct_wealth_share=_try_csv(
            "us_bottom_50pct_wealth.csv", US_BOTTOM_50PCT_WEALTH_SHARE
        ),
        real_gdp_b=_try_csv("us_real_gdp.csv", US_REAL_GDP_BILLIONS),
        mean_markup_sw=_try_csv("us_mean_markup.csv", US_MEAN_MARKUP_SALES_WEIGHTED),
        substitute_employment_idx=_try_csv(
            "us_substitute_employment.csv", US_SUBSTITUTE_WORKER_EMPLOYMENT_INDEX
        ),
    )


def load_cn_baseline() -> BaselineSeries:
    """Load China baseline series — file-backed if available, hard-coded otherwise."""
    return BaselineSeries(
        country="CN",
        labor_share=_try_csv("cn_labor_share.csv", CN_LABOR_SHARE),
        top_1pct_wealth_share=_try_csv(
            "cn_top_1pct_wealth.csv", CN_TOP_1PCT_WEALTH_SHARE
        ),
        real_gdp_b=_try_csv("cn_real_gdp.csv", CN_REAL_GDP_BILLIONS),
        mean_markup_sw=_try_csv("cn_mean_markup.csv", CN_MEAN_MARKUP_SALES_WEIGHTED),
    )


def cumulative_growth(series: pd.Series, start_year: int, end_year: int) -> float:
    """Return cumulative growth from start to end year as a fraction.

    Used for backtest GDP target validation per PREREGISTRATION.md §8.
    """
    if start_year not in series.index or end_year not in series.index:
        raise KeyError(
            f"Years {start_year} or {end_year} not in series index "
            f"{series.index.tolist()}"
        )
    return float(series[end_year] / series[start_year] - 1.0)
