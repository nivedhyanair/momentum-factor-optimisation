# Momentum Factor Optimisation

Quantitative research and a Streamlit dashboard evaluating five market-cap-weighted momentum lookbacks across a 30-stock universe. The repository includes the research notebook, input data, backtest outputs, anomaly diagnostics, an interactive dashboard, and the final research report.

## Interactive Dashboard

[Open the live Streamlit dashboard](https://momentum-factor-optimisation-rjynydupn5n9j5uehftbqz.streamlit.app/)

## Research Overview

The analysis compares lookback periods of **21, 63, 126, 189, and 252 trading days** under a common monthly portfolio-construction and backtesting framework.

- **Universe:** 30 securities, as identified in the supplied data
- **Portfolio:** 10 holdings, with an incumbent retention buffer through rank 12
- **Weighting:** Market-capitalisation weighted, with a 20% target-weight cap
- **Backtest period:** 2006-01-03 to 2026-06-24
- **Return observations:** 5,083 daily observations
- **Rebalances:** 246 monthly rebalances
- **Sharpe convention:** Annualised using 252 trading days and a zero risk-free rate

The ticker labels include `.NS` and `.BO` suffixes. The supplied materials do not include a definitive security master or independently verified corporate-action history, so security identities and price adjustments should be treated as unverified.

## Main Result

The 189-day lookback has the highest measured annualised Sharpe ratio in the supplied backtest:

| Lookback | Original Sharpe | Diagnostic sensitivity Sharpe |
|---|---:|---:|
| 189 days | 1.4532 | 1.2847 |
| 252 days | 1.4523 | 1.2795 |

The advantage over 252 days is small. In the diagnostic sensitivity scenario, selected stock contributions are set to zero without rebuilding holdings or reallocating weights. This scenario is not a corrected or implementable portfolio backtest.

The supplied price history also contains many extreme returns. The report and notebook describe the anomaly checks and their limitations. These results are a research comparison, not verified investment performance or investment advice.

## Repository Contents

```text
.
├── README.md
├── Momentum_Factor_Optimisation_Quantitative_Research_Report.pdf
├── Code/
│   ├── Momentum_Factor_Optimization.ipynb
│   ├── Input/
│   │   ├── Test_price_data.csv
│   │   └── Test_mcap_data.csv
│   └── Output/
│       ├── annual_anomaly_summary_189d.csv
│       ├── anomaly_classification_summary.csv
│       ├── anomaly_event_return_attribution_189d.csv
│       ├── final_performance_comparison.csv
│       ├── full_period_extreme_return_audit_189d.csv
│       ├── price_anomaly_register.csv
│       ├── price_mcap_discrepancy_report.csv
│       ├── reversal_investigation.csv
│       ├── strong_anomaly_events_189d.csv
│       └── ticker_anomaly_summary.csv
└── Dashboard/
    ├── app.py
    ├── analytics.py
    ├── charts.py
    ├── data_loader.py
    ├── styles.css
    ├── requirements.txt
    └── data_cache/
