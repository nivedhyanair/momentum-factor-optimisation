# Momentum Factor Optimisation: Interactive Quantitative Research Dashboard

An institutional-grade interactive research dashboard investigating the performance, lookback horizon sensitivity, and portfolio construction mechanics of a cross-sectional, market-cap-weighted momentum strategy across 30 equities over a 20-year backtest horizon (2006–2026).

---

## 1. Executive Summary

This project evaluates momentum factor dynamics across five historical lookback horizons (**21, 63, 126, 189, and 252 trading days**) to identify the horizon that maximises annualised Sharpe ratio under institutional portfolio constraints:
- **Universe:** 30 Indian equities (NSE/BSE).
- **Backtest Period:** January 2, 2006 to June 24, 2026 (5,083 trading days; pre-2006 used exclusively for signal initialization).
- **Portfolio Construction:** Exactly 10 holdings selected by relative momentum rank.
- **Turnover Dampening Buffer:** Rank-12 retention buffer (incumbent holdings retained if their cross-sectional rank $\le 12$).
- **Allocation Rules:** Market-capitalisation weighting subject to an iterative 20% maximum target allocation cap.
- **Execution Barrier:** Information close at $T_{calc}$ (preceding trading day close) with trade execution at $T_{reb}$ close, after which weights drift daily.
- **Risk-Free Rate:** Assumed 0.0% for annualised Sharpe calculation ($\sqrt{252}$ scaling factor).

### Authoritative Reference
The primary source of truth is `Momentum_Factor_Optimization.ipynb`. All figures, metrics, holdings, rankings, and anomaly classifications displayed in the dashboard replicate the notebook's exact code and outputs down to $10^{-16}$ float precision.

---

## 2. Key Quantitative Findings

| Lookback Horizon | Original Sharpe | Sharpe Rank | Original Volatility | Original CAGR | Sensitivity Sharpe | Sensitivity Rank | Sensitivity CAGR | Max Drawdown (Orig / Sens) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **21 Trading Days** | 1.3530 | #5 | 260.52% | 62.87% | 1.2351 | #3 | 22.78% | -76.21% / -97.71% |
| **63 Trading Days** | 1.3946 | #4 | 266.55% | 69.33% | 1.2286 | #5 | 13.67% | -73.12% / -96.57% |
| **126 Trading Days** | 1.3972 | #3 | 265.33% | 71.68% | 1.2334 | #4 | 15.92% | -71.04% / -89.20% |
| **189 Trading Days (★ Winner)** | **1.4532** | **#1** | **262.47%** | **104.63%** | **1.2847** | **#1** | **36.71%** | **-72.07% / -85.80%** |
| **252 Trading Days** | **1.4523** | **#2** | **262.92%** | **101.30%** | **1.2795** | **#2** | **33.59%** | **-69.18% / -85.81%** |

### Crucial Analytical Insights:
1. **189 Days is the Numerical Winner:** Under the specified Sharpe objective, the 189-day lookback achieves the highest score in both the original backtest (1.4532) and the anomaly sensitivity scenario (1.2847).
2. **Marginal Advantage Over 252 Days:** The difference between 189 days and 252 days is merely **+0.0009 Sharpe in the original backtest and +0.0052 Sharpe in the sensitivity test**. In institutional portfolio management, this difference is within noise margins.
3. **Data Quality & Anomaly Impact:** 
   - 9,132 constituent daily returns $\ge 50\%$ were audited.
   - 150 strong price-scale distortion candidates (temporary ~5x or ~0.2x jumps that reverse the next day with flat market cap) were confirmed across 29 of the 30 stocks.
   - Longer lookback horizons mechanically accumulate anomaly exposure: 21.0% of evaluated monthly signals for the 252-day horizon span an anomaly event (vs 2.0% at 21 days).
4. **Diagnostic Sensitivity Findings:** Excluding strong anomaly contributions from portfolio returns compresses the 189-day CAGR from 104.63% to 36.71%, yet 2,892 extreme held-stock observations still remain.
5. **Intellectual Honesty:** The data-quality limitations prevent certifying the strategy as an investable commercial alpha. The 189-day horizon is reported as the **numerical winner** of the exercise, not as a validated production strategy.

---

## 3. Project Architecture

The application is structured modularly:

```text
├── app.py                   # Streamlit multi-section editorial research application
├── data_loader.py           # Cached dataset accessors with @st.cache_data
├── analytics.py             # Time-series analytics, rolling Sharpe, moments, and formatters
├── charts.py                # Institutional Plotly charts with custom dark financial styling
├── styles.css               # Editorial CSS, typography, spec strips, and callouts
├── requirements.txt         # Production dependencies
├── README.md                # Quantitative research documentation
├── data_cache/              # High-performance Parquet & JSON precomputed series (zero-latency UI)
└── Momentum_Factor_Optimization.ipynb # Primary source of truth notebook
```

---

## 4. How to Run the Dashboard Locally

Ensure Python 3.10+ is installed with the required libraries:

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the Streamlit research dashboard
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## 5. Dashboard Sections

1. **01 // Research Overview:** Comprehensive quantitative executive summary, universe specs, strategy parameters, and execution rules.
2. **02 // Lookback Optimisation:** Cross-horizon Sharpe rankings, dumbbell sensitivity slope chart, and consolidated metrics table.
3. **03 // Performance Explorer:** Interactive time-series performance explorer with lookback selection, linear/logarithmic toggles, underwater drawdowns, rolling 252-day Sharpe curves, and empirical return distribution moments.
4. **04 // Portfolio Construction:** Multi-stage methodology breakdown (separating $T_{calc}$ and $T_{reb}$) and historical rebalance explorer across all 246 rebalances.
5. **05 // Data Quality Investigation:** Forensic audit displaying extreme price moves, price vs market-cap divergences, signal exposure scaling, and interactive case study trajectories.
6. **06 // Robustness & Sensitivity:** Deep-dive into the diagnostic sensitivity scenario, residual extreme return analysis, and broad-scale distortion detection.
7. **07 // Final Assessment:** Balanced, institutional research verdict acknowledging both the quantitative execution and data limitations.
