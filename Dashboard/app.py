"""
app.py
Executive Quantitative Research Dashboard: Momentum Factor Optimisation
Authoritative reference: Momentum_Factor_Optimization.ipynb
"""
import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Momentum Factor Optimisation | Quantitative Research",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS from the dashboard folder
from pathlib import Path

css_path = Path(__file__).resolve().parent / "styles.css"
with css_path.open("r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Import modular components
from data_loader import (
    load_universe_meta,
    load_performance_comparison,
    load_daily_returns,
    load_cumulative_returns,
    load_drawdowns,
    load_rebalance_holdings,
    load_reversal_classification,
    load_ticker_anomaly_summary,
    load_price_mcap_discrepancy,
    load_annual_anomaly_summary,
    load_strong_anomaly_events,
    load_anomaly_attribution,
    load_signal_exposure,
    load_cross_lookback_anomalies,
    load_residual_anomalies,
    load_broad_scale_candidates,
    load_case_studies
)
from analytics import (
    calculate_annual_returns,
    calculate_distribution_stats,
    format_pct,
    format_mult,
    format_num
)
from charts import (
    create_lookback_comparison_bars,
    create_sharpe_cagr_dumbbell,
    create_cumulative_growth_chart,
    create_drawdown_chart,
    create_rolling_sharpe_chart,
    create_annual_returns_bar,
    create_return_distribution_chart,
    create_anomaly_timeline_chart,
    create_signal_exposure_chart,
    create_price_mcap_discrepancy_scatter,
    create_case_study_plot
)

# Load core datasets
universe = load_universe_meta()
perf_df = load_performance_comparison()
daily_ret_df = load_daily_returns()
cum_ret_df = load_cumulative_returns()
drawdowns_df = load_drawdowns()

# ==============================================================================
# HEADER COMPONENT (Generous breathing room, no cut-off)
# ==============================================================================
st.markdown("""
<div class="research-header">
    <div class="research-meta">
        <span class="research-badge">QUANTITATIVE RESEARCH REPORT</span>
        <span>UNIVERSE: 30 EQUITIES</span>
        <span>PERIOD: 2006 – 2026</span>
        <span>FREQUENCY: MONTHLY REBALANCE</span>
        <span class="research-badge-warning">DATA INTEGRITY AUDIT INCLUDED</span>
    </div>
    <div class="research-title">Momentum Factor Optimisation</div>
    <div class="research-subtitle">
        An empirical investigation into cross-sectional momentum performance, lookback horizon sensitivity, 
        and market-cap portfolio construction across five historical windows (21, 63, 126, 189, and 252 trading days).
    </div>
</div>
""", unsafe_allow_html=True)

# Methodology Spec Strip
st.markdown("""
<div class="spec-strip">
    <div class="spec-cell">
        <div class="spec-label">Research Objective</div>
        <div class="spec-value">Maximise Annualised Sharpe</div>
    </div>
    <div class="spec-cell">
        <div class="spec-label">Optimal Horizon</div>
        <div class="spec-value optimal">189 Trading Days</div>
    </div>
    <div class="spec-cell">
        <div class="spec-label">Portfolio Size</div>
        <div class="spec-value">10 Stocks (Rank-12 Buffer)</div>
    </div>
    <div class="spec-cell">
        <div class="spec-label">Weighting Scheme</div>
        <div class="spec-value">Market Cap (20% Max Cap)</div>
    </div>
    <div class="spec-cell">
        <div class="spec-label">Execution Mechanism</div>
        <div class="spec-value">T_calc Close → T_reb Execution</div>
    </div>
    <div class="spec-cell">
        <div class="spec-label">Risk-Free Rate</div>
        <div class="spec-value">0.0% (Annualised × √252)</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# NAVIGATION (Clean editorial numbering, no '//')
# ==============================================================================
sections = [
    "01. Research Overview",
    "02. Lookback Optimisation",
    "03. Performance Explorer",
    "04. Portfolio Construction",
    "05. Data Quality Investigation",
    "06. Robustness & Sensitivity",
    "07. Final Assessment"
]

selected_section = st.radio(
    "Navigate Research Sections",
    options=sections,
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)


# ==============================================================================
# SECTION 01: RESEARCH OVERVIEW
# ==============================================================================
if selected_section == "01. Research Overview":
    st.markdown("### Executive Summary & Strategy Specification")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        This quantitative project investigates the behaviour and performance of a systematic cross-sectional 
        **momentum strategy** applied to a closed universe of 30 liquid Indian equities across more than two decades 
        (**January 2006 through June 2026**, spanning 5,083 trading days).
        
        The primary quantitative mandate is to test five lookback horizons:
        - **21 Trading Days** (~1 calendar month)
        - **63 Trading Days** (~1 calendar quarter)
        - **126 Trading Days** (~6 calendar months)
        - **189 Trading Days** (~9 calendar months)
        - **252 Trading Days** (~1 calendar year)
        
        The objective is to identify which lookback produces the highest annualised Sharpe ratio under strict, institutional 
        portfolio constraints including turnover dampening buffers, iterative market-capitalisation allocation limits, and realistic execution lag.
        """)
        
        st.markdown("""
        <div class="callout callout-warning">
            <div class="callout-header">Critical Research Integrity Notice</div>
            The underlying historical dataset contains recurring extreme single-day price distortions and scale anomalies 
            (such as temporary 5x price jumps reversing the following day with unchanged market capitalisation). 
            In keeping with institutional research standards, this dashboard presents the exact backtest results as run on the supplied 
            data alongside exhaustive forensic sensitivity analyses. <b>No outliers were arbitrarily deleted or cosmetically smoothed.</b>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="stat-box optimal-highlight">
            <div class="stat-title">Numerical Winner (Original Backtest)</div>
            <div class="stat-number">189 Days</div>
            <div class="stat-desc">Sharpe: <b>1.4532</b> | Vol: 262.5% | CAGR: 104.6%<br>Margin over 252d: <b>+0.0009 Sharpe</b> (negligible)</div>
        </div>
        <div class="stat-box sensitivity-highlight">
            <div class="stat-title">Numerical Winner (Sensitivity Diagnostic)</div>
            <div class="stat-number">189 Days</div>
            <div class="stat-desc">Sharpe: <b>1.2847</b> | Vol: 253.5% | CAGR: 36.7%<br>Margin over 252d: <b>+0.0052 Sharpe</b></div>
        </div>
        <div class="stat-box warning-highlight">
            <div class="stat-title">Forensic Audit Finding</div>
            <div class="stat-number">9,132</div>
            <div class="stat-desc">Constituent price moves ≥ 50% detected; 150 strong scale anomaly candidates identified across 29 stocks.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Quantitative Strategy Blueprint")
    
    st.markdown("""
    <div class="process-flow">
        <div class="process-step">
            <div class="step-num">Rule 1 — Universe & Alignment</div>
            <div class="step-title">30 Aligned Stocks</div>
            <div class="step-desc">Strict calendar date alignment across closing prices and reported market caps. Pre-2006 history used exclusively for signal burn-in.</div>
        </div>
        <div class="process-step">
            <div class="step-num">Rule 2 — Information Barrier</div>
            <div class="step-title">Calculation at T_calc</div>
            <div class="step-desc">Signals and market caps evaluated at the close of trading day immediately preceding the rebalance date to prevent lookahead bias.</div>
        </div>
        <div class="process-step">
            <div class="step-num">Rule 3 — Cross-Sectional Ranking</div>
            <div class="step-title">Relative Momentum</div>
            <div class="step-desc">Momentum defined as P(T_calc) / P(T_calc - Lookback) - 1. Strict rank-ordering from strongest to weakest across the 30 names.</div>
        </div>
        <div class="process-step">
            <div class="step-num">Rule 4 — Turnover Dampening</div>
            <div class="step-title">Rank-12 Buffer</div>
            <div class="step-desc">Portfolio targets exactly 10 holdings. Incumbent positions are retained if rank ≤ 12. Vacancies filled by highest unheld candidates.</div>
        </div>
        <div class="process-step">
            <div class="step-num">Rule 5 — Iterative Weight Capping</div>
            <div class="step-title">20% Maximum Allocation</div>
            <div class="step-desc">Market-cap weighting subject to iterative 20% capping. Excess weight redistributed proportionally among uncapped constituents until convergence.</div>
        </div>
        <div class="process-step">
            <div class="step-num">Rule 6 — Daily Return Engine</div>
            <div class="step-title">End-of-Day Execution & Drift</div>
            <div class="step-desc">Rebalances execute at close of T_reb. Constituent weights drift daily based on asset price changes until the subsequent monthly rebalance.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# SECTION 02: LOOKBACK OPTIMISATION
# ==============================================================================
elif selected_section == "02. Lookback Optimisation":
    st.markdown("### Cross-Horizon Lookback Optimisation")
    st.markdown("""
    The core research mandate is to determine the optimal lookback horizon $L \\in \\{21, 63, 126, 189, 252\\}$ 
    that maximises the annualised Sharpe ratio:
    $$\\text{Sharpe} = \\frac{\\mu_R}{\\sigma_R} \\times \\sqrt{252}$$
    """)

    # Visualizations row
    c1, c2 = st.columns([1, 1])
    with c1:
        fig_bar = create_lookback_comparison_bars(perf_df)
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
    with c2:
        fig_db = create_sharpe_cagr_dumbbell(perf_df)
        st.plotly_chart(fig_db, use_container_width=True, config={'displayModeBar': False})

    st.markdown("#### Consolidated Performance Comparison Table")
    
    # Clean, properly formatted table (NO raw code blocks)
    perf_table = perf_df.sort_values("Original Sharpe", ascending=False).copy()
    perf_display = pd.DataFrame({
        "Lookback Horizon": [f"{int(lb)} Trading Days {'(Optimal ★)' if lb == 189 else ''}" for lb in perf_table["Lookback"]],
        "Original Sharpe": [f"{v:.4f}" for v in perf_table["Original Sharpe"]],
        "Original Rank": [f"#{int(r)}" for r in perf_table["Original Sharpe Rank"]],
        "Original Volatility": [f"{v*100:.2f}%" for v in perf_table["Original Volatility"]],
        "Original CAGR": [f"{v*100:.2f}%" for v in perf_table["Original CAGR"]],
        "Original Cumulative Growth": [f"{v:,.0f}×" for v in perf_table["Original Cumulative Return"]],
        "Original Max Drawdown": [f"{v*100:.2f}%" for v in perf_table["Original Maximum Drawdown"]],
        "Sensitivity Sharpe": [f"{v:.4f}" for v in perf_table["Sensitivity Sharpe"]],
        "Sensitivity Rank": [f"#{int(r)}" for r in perf_table["Sensitivity Sharpe Rank"]],
        "Sensitivity CAGR": [f"{v*100:.2f}%" for v in perf_table["Sensitivity CAGR"]],
        "Sensitivity Max Drawdown": [f"{v*100:.2f}%" for v in perf_table["Sensitivity Maximum Drawdown"]]
    })
    
    st.dataframe(perf_display, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="callout callout-amber">
        <div class="callout-header">Analytical Insight: The Statistical Margin of Victory</div>
        While the <b>189-day lookback is the numerical winner</b> in both the original backtest (Sharpe 1.4532) 
        and the sensitivity scenario (Sharpe 1.2847), its advantage over the <b>252-day lookback (Sharpe 1.4523 / 1.2795)</b> 
        is only <b>0.0009 in the original backtest and 0.0052 in the sensitivity test</b>. 
        In practical portfolio management, this difference is within noise margins and does not establish a statistically significant superiority of 189 days over a full 1-year momentum factor.
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# SECTION 03: PERFORMANCE EXPLORER
# ==============================================================================
elif selected_section == "03. Performance Explorer":
    st.markdown("### Interactive Time-Series Performance Explorer")
    
    # Controls
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 2, 2])
    with ctrl_col1:
        sel_lookback = st.selectbox(
            "Select Momentum Horizon",
            options=[21, 63, 126, 189, 252],
            index=3,
            format_func=lambda x: f"{x} Trading Days {'★ Optimal' if x==189 else ''}"
        )
    with ctrl_col2:
        show_sens = st.checkbox("Overlay Anomaly Sensitivity Scenario", value=True)
    with ctrl_col3:
        is_log = st.checkbox("Logarithmic Value Scale (Base 10)", value=True,
                             help="Recommended when viewing 20-year unadjusted return compounding")

    # Metrics row for selected lookback
    row_data = perf_df[perf_df["Lookback"] == sel_lookback].iloc[0]
    
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    with m_col1:
        st.markdown(f"""
        <div class="stat-box {'optimal-highlight' if sel_lookback==189 else ''}">
            <div class="stat-title">Annualised Sharpe</div>
            <div class="stat-number">{row_data['Original Sharpe']:.4f}</div>
            <div class="stat-desc">Sens: {row_data['Sensitivity Sharpe']:.4f} (Rank #{int(row_data['Sensitivity Sharpe Rank'])})</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-title">Annualised Volatility</div>
            <div class="stat-number">{row_data['Original Volatility']*100:.1f}%</div>
            <div class="stat-desc">Sens: {row_data['Sensitivity Volatility']*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-title">Compound Annual Growth (CAGR)</div>
            <div class="stat-number">{row_data['Original CAGR']*100:.1f}%</div>
            <div class="stat-desc">Sens: {row_data['Sensitivity CAGR']*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col4:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-title">Maximum Drawdown</div>
            <div class="stat-number">{row_data['Original Maximum Drawdown']*100:.1f}%</div>
            <div class="stat-desc">Sens: {row_data['Sensitivity Maximum Drawdown']*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col5:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-title">Cumulative Growth Multiple</div>
            <div class="stat-number">{format_mult(row_data['Original Cumulative Return'])}</div>
            <div class="stat-desc">Sens: {format_mult(row_data['Sensitivity Cumulative Return'])}</div>
        </div>
        """, unsafe_allow_html=True)

    # Cumulative growth chart
    fig_cum = create_cumulative_growth_chart(cum_ret_df, sel_lookback, show_sens=show_sens, is_log=is_log)
    st.plotly_chart(fig_cum, use_container_width=True, config={'displayModeBar': False})

    # Underwater Drawdown & Rolling Sharpe
    dd_col, rs_col = st.columns(2)
    with dd_col:
        fig_dd = create_drawdown_chart(drawdowns_df, sel_lookback, show_sens=show_sens)
        st.plotly_chart(fig_dd, use_container_width=True, config={'displayModeBar': False})
    with rs_col:
        daily_s = daily_ret_df[f"{sel_lookback}d_orig"]
        fig_rs = create_rolling_sharpe_chart(daily_s, sel_lookback)
        st.plotly_chart(fig_rs, use_container_width=True, config={'displayModeBar': False})

    # Annual returns & Distribution
    ann_col, dist_col = st.columns(2)
    with ann_col:
        ann_df = calculate_annual_returns(daily_ret_df[f"{sel_lookback}d_orig"])
        fig_ann = create_annual_returns_bar(ann_df, sel_lookback)
        st.plotly_chart(fig_ann, use_container_width=True, config={'displayModeBar': False})
    with dist_col:
        fig_dist = create_return_distribution_chart(daily_ret_df[f"{sel_lookback}d_orig"], sel_lookback)
        st.plotly_chart(fig_dist, use_container_width=True, config={'displayModeBar': False})

    # Statistical Moments Table
    stats = calculate_distribution_stats(daily_ret_df[f"{sel_lookback}d_orig"])
    st.markdown("#### Empirical Return Moments & Tail Statistics")
    t_c1, t_c2, t_c3, t_c4 = st.columns(4)
    with t_c1:
        st.markdown(f"""
        - **Trading Days:** {stats['count']:,}
        - **Daily Mean:** {stats['mean']*100:.3f}%
        - **Daily Std Dev:** {stats['std']*100:.2f}%
        - **Win Rate:** {stats['win_rate']*100:.1f}%
        """)
    with t_c2:
        st.markdown(f"""
        - **Sample Skewness:** {stats['skew']:.2f}
        - **Excess Kurtosis:** {stats['kurtosis']:.2f}
        - **Median Return:** {stats['median']*100:.3f}%
        - **Flat Days:** {stats['flat_days']}
        """)
    with t_c3:
        st.markdown(f"""
        - **1% Left Tail (VaR):** {stats['q01']*100:.2f}%
        - **5% Left Tail:** {stats['q05']*100:.2f}%
        - **95% Right Tail:** {stats['q95']*100:.2f}%
        - **99% Right Tail:** {stats['q99']*100:.2f}%
        """)
    with t_c4:
        st.markdown(f"""
        - **Days > +10%:** {stats['days_above_10pct']}
        - **Days > +25%:** {stats['days_above_25pct']}
        - **Days < -10%:** {stats['days_below_neg10pct']}
        - **Days < -25%:** {stats['days_below_neg25pct']}
        """)


# ==============================================================================
# SECTION 04: PORTFOLIO CONSTRUCTION
# ==============================================================================
elif selected_section == "04. Portfolio Construction":
    st.markdown("### Portfolio Construction & Rebalance Forensics")
    
    st.markdown("""
    The strategy enforces a realistic multi-stage portfolio allocation protocol. 
    Crucially, it separates the **signal calculation date ($T_{calc}$)** from the **execution date ($T_{reb}$)**:
    """)

    st.markdown("""
    <div class="process-flow">
        <div class="process-step">
            <div class="step-num">Phase A — Information Close (T_calc)</div>
            <div class="step-title">Close on T_calc</div>
            <div class="step-desc">On the trading day immediately preceding the rebalance date, closing prices and reported market caps are gathered. No lookahead data is allowed.</div>
        </div>
        <div class="process-step">
            <div class="step-num">Phase B — Momentum Score & Ranks</div>
            <div class="step-title">Cross-Sectional Ranking</div>
            <div class="step-desc">Momentum is computed over the selected horizon L. The 30 stocks are ranked cross-sectionally from #1 (strongest) to #30 (weakest).</div>
        </div>
        <div class="process-step">
            <div class="step-num">Phase C — Turnover Retention Filter</div>
            <div class="step-title">Rank ≤ 12 Retention</div>
            <div class="step-desc">Incumbent positions from the previous month are retained if they remain within the top 12. This buffer substantially reduces portfolio turnover.</div>
        </div>
        <div class="process-step">
            <div class="step-num">Phase D — Vacancy Allocation</div>
            <div class="step-title">Exactly 10 Holdings</div>
            <div class="step-desc">If retained positions &lt; 10, the highest-ranked eligible stocks not currently held are admitted until exactly 10 stocks are selected.</div>
        </div>
        <div class="process-step">
            <div class="step-num">Phase E — Iterative Weight Capping</div>
            <div class="step-title">20% Maximum Allocation</div>
            <div class="step-desc">Market-cap weights are determined. Any stock breaching 20% is capped at exactly 20%, and excess weight is iteratively redistributed across uncapped names.</div>
        </div>
        <div class="process-step">
            <div class="step-num">Phase F — Execution & Drift</div>
            <div class="step-title">Execution at T_reb Close</div>
            <div class="step-desc">Trades execute at the close of T_reb. From T_reb + 1 day onward, daily weights drift based on asset price paths until next rebalance.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Historical Rebalance Explorer")
    st.markdown("Inspect actual historical holdings, rankings, retention status, and capped target weights for any monthly rebalance:")

    p_col1, p_col2 = st.columns([1, 2])
    with p_col1:
        rebal_lb = st.selectbox(
            "Lookback Scheme",
            options=[21, 63, 126, 189, 252],
            index=3,
            key="rebal_lb_sel"
        )
        holdings_df = load_rebalance_holdings(rebal_lb)
        unique_reb_dates = sorted(list(holdings_df["Rebalance Date"].unique()))
        
        sel_reb_date = st.selectbox(
            "Select Monthly Rebalance Date (T_reb)",
            options=unique_reb_dates,
            index=0,
            help="First trading day of the month"
        )

    # Filter holdings for this date
    sub_holdings = holdings_df[holdings_df["Rebalance Date"] == sel_reb_date].copy()
    calc_date = sub_holdings["Calculation Date"].iloc[0]

    with p_col2:
        retained_cnt = (sub_holdings["Status"] == "Retained").sum()
        new_cnt = (sub_holdings["Status"] == "New Addition").sum()
        max_wt = sub_holdings["Target Weight"].max() * 100
        total_wt = sub_holdings["Target Weight"].sum() * 100

        st.markdown(f"""
        <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
            <div class="stat-box" style="flex: 1;">
                <div class="stat-title">Signal Calculation Date (T_calc)</div>
                <div class="stat-number" style="font-size: 1.25rem;">{calc_date}</div>
                <div class="stat-desc">Execution Date: {sel_reb_date}</div>
            </div>
            <div class="stat-box" style="flex: 1;">
                <div class="stat-title">Turnover Decomposition</div>
                <div class="stat-number" style="font-size: 1.25rem;">{retained_cnt} Retained / {new_cnt} New</div>
                <div class="stat-desc">Target Count: Exactly 10 Holdings</div>
            </div>
            <div class="stat-box" style="flex: 1;">
                <div class="stat-title">Weight Allocation</div>
                <div class="stat-number" style="font-size: 1.25rem;">{max_wt:.1f}% Max / {total_wt:.0f}% Sum</div>
                <div class="stat-desc">Constraint: Max ≤ 20.0%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Render holdings table
    st.markdown(f"**Constituent Holdings & Allocations on {sel_reb_date} ({rebal_lb}-Day Horizon)**")
    
    sub_holdings_display = sub_holdings.sort_values("Target Weight", ascending=False).copy()
    sub_holdings_display["Target Weight (%)"] = (sub_holdings_display["Target Weight"] * 100).map(lambda x: f"{x:.2f}%")
    sub_holdings_display["Momentum Score"] = sub_holdings_display["Momentum Score"].map(lambda x: f"{x*100:+.2f}%")
    sub_holdings_display["Market Cap (Billion INR)"] = (sub_holdings_display["Market Cap"] / 1e9).map(lambda x: f"₹{x:.2f}B")

    st.dataframe(
        sub_holdings_display[[
            "Stock", "Momentum Rank", "Momentum Score", "Status", "Market Cap (Billion INR)", "Target Weight (%)"
        ]],
        use_container_width=True,
        hide_index=True
    )


# ==============================================================================
# SECTION 05: DATA QUALITY INVESTIGATION
# ==============================================================================
elif selected_section == "05. Data Quality Investigation":
    st.markdown("### Forensic Data Quality & Anomaly Investigation")
    
    st.markdown("""
    <div class="callout callout-warning">
        <div class="callout-header">Prominent Institutional Disclosure: Unadjusted Feed Anomalies</div>
        Quantitative rigor demands confronting data imperfections directly rather than smoothing them away.
        The supplied historical price dataset contains severe, recurring single-day price distortions that 
        artificially drive astronomical cumulative compounding. In accordance with the project mandate, 
        <b>these anomalies were meticulously classified and audited rather than silently altered</b>.
    </div>
    """, unsafe_allow_html=True)

    # Anomaly classification summary metrics
    rev_df = load_reversal_classification()
    ticker_anom = load_ticker_anomaly_summary()
    discrepancy_df = load_price_mcap_discrepancy()
    annual_anom = load_annual_anomaly_summary()
    signal_exp = load_signal_exposure()

    a1, a2, a3, a4 = st.columns(4)
    with a1:
        st.markdown("""
        <div class="stat-box warning-highlight">
            <div class="stat-title">Extreme Daily Returns (≥50%)</div>
            <div class="stat-number">9,132</div>
            <div class="stat-desc">Single-day price moves exceeding ±50% (4,236 moves ≥ 100%).</div>
        </div>
        """, unsafe_allow_html=True)
    with a2:
        st.markdown("""
        <div class="stat-box warning-highlight">
            <div class="stat-title">Reversal Candidates</div>
            <div class="stat-number">4,313</div>
            <div class="stat-desc">Extreme movements followed by immediate opposite reversal on day t+1.</div>
        </div>
        """, unsafe_allow_html=True)
    with a3:
        st.markdown("""
        <div class="stat-box warning-highlight">
            <div class="stat-title">Strong Scale Anomalies</div>
            <div class="stat-number">150</div>
            <div class="stat-desc">Confirmed temporary ~5x or ~0.2x jumps with 2-day price & mcap flat (±5%).</div>
        </div>
        """, unsafe_allow_html=True)
    with a4:
        st.markdown("""
        <div class="stat-box warning-highlight">
            <div class="stat-title">Stocks Affected</div>
            <div class="stat-number">29 / 30</div>
            <div class="stat-desc">96.7% of the entire stock universe is contaminated by scale distortions.</div>
        </div>
        """, unsafe_allow_html=True)

    # Visualizations
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        fig_time = create_anomaly_timeline_chart(annual_anom)
        st.plotly_chart(fig_time, use_container_width=True, config={'displayModeBar': False})
    with v_col2:
        fig_exp = create_signal_exposure_chart(signal_exp)
        st.plotly_chart(fig_exp, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")
    st.markdown("#### Price vs Market-Capitalisation Consistency Discrepancy")
    st.markdown("""
    Under normal corporate capital changes, price and market cap move in tandem unless new shares are issued or retired. 
    Here, the data exhibits massive single-day price jumps while reported market capitalization remains entirely stationary:
    """)

    scat_col, table_col = st.columns([1, 1])
    with scat_col:
        fig_scat = create_price_mcap_discrepancy_scatter(discrepancy_df)
        st.plotly_chart(fig_scat, use_container_width=True, config={'displayModeBar': False})
    with table_col:
        st.markdown("**Top Discrepancy Events (Price Spike vs Flat Market Cap)**")
        disc_disp = discrepancy_df.head(10).copy()
        disc_table = pd.DataFrame({
            "Date": disc_disp["date"],
            "Ticker": disc_disp["Ticker"],
            "Price Return": [f"{v*100:+,.1f}%" for v in disc_disp["Price Return"]],
            "Market Cap Return": [f"{v*100:+,.1f}%" for v in disc_disp["Market Cap Return"]],
            "Absolute Divergence": [f"{v*100:,.1f}%" for v in disc_disp["Absolute Difference"]]
        })
        st.dataframe(disc_table, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### Deep-Dive Forensic Case Studies")
    st.markdown("Select a prominent historical anomaly to inspect its daily price and market-cap path:")

    case_studies = load_case_studies()
    case_names = [cs["title"] for cs in case_studies]
    sel_case_name = st.selectbox("Select Anomaly Event", options=case_names, index=0)
    sel_case = next(cs for cs in case_studies if cs["title"] == sel_case_name)

    fig_case = create_case_study_plot(sel_case)
    st.plotly_chart(fig_case, use_container_width=True, config={'displayModeBar': False})

    st.markdown("""
    <div class="callout callout-amber">
        <div class="callout-header">Methodological Distinction: Confirmed Facts vs Anomaly Candidates</div>
        <ul>
            <li><b>Confirmed Quantitative Facts:</b> The mathematical presence of 9,132 extreme moves ≥50%, 150 temporary 5x/0.2x price distortions, and near-zero correlation with market caps on event dates are verified empirical facts of this dataset.</li>
            <li><b>Potential Anomaly Candidates:</b> In the absence of external primary exchange corporate action feeds, these events are classified as <i>strong anomaly candidates</i> rather than proven vendor errors. Unadjusted stock splits, reverse splits, or vendor decimal transposition errors are the most plausible explanations.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# SECTION 06: ROBUSTNESS & SENSITIVITY
# ==============================================================================
elif selected_section == "06. Robustness & Sensitivity":
    st.markdown("### Robustness & Anomaly Sensitivity Analysis")
    
    st.markdown("""
    <div class="callout callout-warning">
        <div class="callout-header">Sensitivity Methodology Definition</div>
        To diagnose the degree of performance distortion caused by the identified price-scale anomalies, 
        a <b>diagnostic sensitivity test</b> was conducted. For each lookback horizon:
        <br>
        <i>The stock-level return contributions of flagged strong anomaly candidates were removed (set to zero) 
        from portfolio returns on identified event dates, without reconstructing the portfolio or reallocating weights.</i>
        <br><br>
        <b>This is explicitly a diagnostic test, not an investable or corrected backtest.</b>
    </div>
    """, unsafe_allow_html=True)

    cross_lb = load_cross_lookback_anomalies()
    resid_df = load_residual_anomalies()
    broad_df = load_broad_scale_candidates()

    st.markdown("#### Diagnostic Impact Across All Five Lookback Horizons")
    
    # Clean formatted DataFrame table (NO raw code blocks)
    diag_rows = []
    for _, row in perf_df.sort_values("Lookback").iterrows():
        lb = int(row["Lookback"])
        s_diff = row["Sensitivity Sharpe"] - row["Original Sharpe"]
        c_diff = (row["Sensitivity CAGR"] - row["Original CAGR"]) * 100
        is_opt = (lb == 189)
        
        cnt = cross_lb[cross_lb["Lookback"] == lb]["Strong_Candidates"].iloc[0]
        dt_cnt = cross_lb[cross_lb["Lookback"] == lb]["Strong_Dates"].iloc[0]
        
        diag_rows.append({
            "Lookback Horizon": f"{lb} Trading Days {'(Optimal ★)' if is_opt else ''}",
            "Original Sharpe": f"{row['Original Sharpe']:.4f}",
            "Sensitivity Sharpe": f"{row['Sensitivity Sharpe']:.4f}",
            "Sharpe Degradation": f"{s_diff:+.4f}",
            "Original CAGR": f"{row['Original CAGR']*100:.2f}%",
            "Sensitivity CAGR": f"{row['Sensitivity CAGR']*100:.2f}%",
            "CAGR Compression": f"{c_diff:+.2f}%",
            "Strong Candidates Excluded": f"{cnt}",
            "Unique Dates Affected": f"{dt_cnt}"
        })
    
    st.dataframe(pd.DataFrame(diag_rows), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### Residual Extreme Return Forensics")
    st.markdown("""
    Does removing the 48 strong anomaly candidates resolve the data quality issue? **No.**
    Thousands of extreme constituent observations remain active in the portfolio:
    """)

    rc1, rc2 = st.columns([1, 1])
    with rc1:
        st.markdown("**Residual Extreme Constituent Observations (Post-Exclusion)**")
        resid_table = pd.DataFrame({
            "Lookback": [f"{lb}d" for lb in resid_df["Lookback"]],
            "Extreme Moves (≥50%)": [f"{v:,}" for v in resid_df["Total_Extreme"]],
            "Excluded Candidates": [f"{v}" for v in resid_df["Strong_Candidates"]],
            "Remaining Extreme Moves": [f"{v:,}" for v in resid_df["Remaining_Extreme"]],
            "Active Extreme Dates": [f"{v:,}" for v in resid_df["Remaining_Dates"]],
            "Gross Extreme Contribution": [f"{v:.1f}" for v in resid_df["Abs_Remaining_Contrib"]]
        })
        st.dataframe(resid_table, use_container_width=True, hide_index=True)

    with rc2:
        st.markdown("**Broader Price-Scale Anomaly Candidates (Ratios ≥ 1.5x / ≤ 0.67x)**")
        broad_table = pd.DataFrame({
            "Lookback": [f"{lb}d" for lb in broad_df["Lookback"]],
            "Broad Anomaly Events": [f"{v:,}" for v in broad_df["Broad_Scale_Candidates"]],
            "Dates Affected": [f"{v:,}" for v in broad_df["Unique_Dates"]],
            "Stocks Affected": [f"{v} / 30" for v in broad_df["Unique_Stocks"]],
            "Median Jump Factor": [f"{v:.2f}×" for v in broad_df["Median_Scale"]]
        })
        st.dataframe(broad_table, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="callout callout-amber">
        <div class="callout-header">Key Diagnostic Conclusion</div>
        Even under the strict exclusion scenario, <b>2,892 extreme held-stock observations remain</b> for the 189-day strategy, 
        and a broader scan reveals <b>925 additional scale distortion candidates across 858 trading days</b>. 
        Crucially, only 2 of these 925 candidates showed consistent movements between price and market cap. 
        This demonstrates that the extreme strategy performance is not driven by momentum factor premia alone, 
        but by persistent, unadjusted scale distortions across the underlying database.
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# SECTION 07: FINAL ASSESSMENT
# ==============================================================================
elif selected_section == "07. Final Assessment":
    st.markdown("### Institutional Research Verdict & Findings")
    
    st.markdown("""
    <div class="research-header" style="border: none; margin-bottom: 1rem;">
        <div class="research-title" style="font-size: 1.75rem;">Summary of Quantitative Findings</div>
    </div>
    """, unsafe_allow_html=True)

    f_col1, f_col2 = st.columns([3, 2])
    with f_col1:
        st.markdown("""
        #### 1. The 189-Day Lookback is the Numerical Winner
        Across the five prescribed lookback horizons (21, 63, 126, 189, and 252 trading days), 
        the **189-day lookback achieves the highest annualised Sharpe ratio**:
        - **Original Backtest:** Sharpe = **1.4532** (Rank #1)
        - **Sensitivity Scenario:** Sharpe = **1.2847** (Rank #1)
        
        #### 2. The Statistical Advantage Over 252 Days is Marginal
        The performance difference between the 189-day strategy and the 252-day strategy is negligible:
        - Original Sharpe gap: **+0.0009** (1.4532 vs 1.4523)
        - Sensitivity Sharpe gap: **+0.0052** (1.2847 vs 1.2795)
        
        In real-world deployment, this difference is far smaller than execution slippage, bid-ask drag, or transaction costs.
        
        #### 3. Data Anomalies Materially Inflate Raw Strategy Metrics
        The sensitivity test demonstrates that strong price-scale distortions heavily inflate strategy performance:
        - 189d CAGR compresses from **104.63% to 36.71%**.
        - Maximum drawdown deepens from **-72.07% to -85.80%**.
        
        #### 4. The Data Limitations Preclude an Investable Conclusion
        Because thousands of residual extreme constituent returns remain even after strict anomaly exclusion, 
        and because price movements frequently diverge completely from reported market capitalisation, 
        **this strategy cannot be certified as investable or optimal for real-world capital allocation**.
        """)

    with f_col2:
        st.markdown("""
        <div class="stat-box optimal-highlight">
            <div class="stat-title">Numerical Status</div>
            <div class="stat-number">189 Days</div>
            <div class="stat-desc">Top-ranked lookback under the challenge rules across both original and sensitivity frameworks.</div>
        </div>
        <div class="stat-box warning-highlight">
            <div class="stat-title">Investable Status</div>
            <div class="stat-number">Unvalidated</div>
            <div class="stat-desc">Underlying price distortions prevent declaring a validated real-world trading strategy.</div>
        </div>
        <div class="stat-box">
            <div class="stat-title">Production Readiness Recommendation</div>
            <div class="stat-desc" style="font-size: 0.88rem; color: var(--text-secondary);">
                1. Re-source prices with point-in-time dividend and split adjustment factors.<br>
                2. Implement exchange-cleared trade prints rather than unverified tick feeds.<br>
                3. Re-estimate turnover impact under explicit slippage and market-impact models.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="callout callout-teal" style="margin-top: 2rem;">
        <div class="callout-header">Researcher's Concluding Declaration</div>
        This research successfully demonstrates the complete quantitative pipeline: 
        cross-sectional momentum signal generation, turnover-dampening retention buffers, 
        iterative constrained market-cap weighting, and point-in-time execution logic. 
        However, quantitative integrity demands acknowledging when backtest gains are artifacts of unadjusted data feeds. 
        <b>The 189-day lookback should be recognized as the numerical winner of the exercise, but not as an investable commercial strategy until the underlying market data has been independently authenticated.</b>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="display: flex; justify-content: space-between; font-size: 0.78rem; color: #8b949e; font-family: 'JetBrains Mono', monospace; padding-bottom: 2rem;">
    <span>QUANTITATIVE RESEARCH REPORT  •  MOMENTUM FACTOR OPTIMISATION</span>
    <span>SOURCE NOTEBOOK: MOMENTUM_FACTOR_OPTIMIZATION.IPYNB</span>
    <span>2006–2026 AUDIT TRAIL</span>
</div>
""", unsafe_allow_html=True)
