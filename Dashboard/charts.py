"""
charts.py
Institutional Plotly visualisations with editorial financial styling.
Clean, uncluttered, professional charts with zero overlapping labels, titles, or collisions.
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Editorial Dark Color Palette
BG_COLOR = "#0e1117"
CARD_BG = "#161b22"
GRID_COLOR = "rgba(48, 54, 61, 0.40)"
TEXT_COLOR = "#c9d1d9"
TEXT_BRIGHT = "#f0f6fc"
TEXT_MUTED = "#8b949e"

COLOR_OPTIMAL = "#00b4d8"      # Vibrant cyan for optimal 189d
COLOR_SECONDARY = "#48cae4"    # Soft blue for 252d
COLOR_SENSITIVITY = "#f4a261"  # Burnt orange for sensitivity scenario
COLOR_RED = "#e63946"          # Muted red for drawdowns & negative returns
COLOR_GREEN = "#38b000"        # Muted green for positive returns
COLOR_NEUTRAL = "#6e7681"      # Slate for other lookbacks

def _apply_institutional_theme(fig, title="", subtitle="", x_title="", y_title="", height=410, top_margin=75, bottom_margin=55, right_margin=40):
    """
    Applies custom styling to remove standard Plotly appearance and prevent any clipped headings or overlapping labels.
    """
    full_title = f"<b>{title}</b>"
    if subtitle:
        full_title += f"<br><span style='font-size: 11px; font-weight: normal; color: {TEXT_MUTED};'>{subtitle}</span>"

    fig.update_layout(
        title=dict(
            text=full_title if title else "",
            font=dict(size=14, color=TEXT_BRIGHT, family="Inter, -apple-system, sans-serif"),
            x=0.01,
            y=0.94,
            yanchor="top",
            xanchor="left",
            pad=dict(t=6, b=4)
        ),
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        height=height,
        margin=dict(l=55, r=right_margin, t=top_margin, b=bottom_margin),
        font=dict(family="Inter, -apple-system, sans-serif", color=TEXT_COLOR, size=11),
        hoverlabel=dict(
            bgcolor=CARD_BG,
            bordercolor="#30363d",
            font=dict(family="JetBrains Mono, monospace", size=11, color=TEXT_BRIGHT)
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="center",
            x=0.5,
            font=dict(size=10.5, color=TEXT_MUTED),
            bgcolor="rgba(0,0,0,0)"
        )
    )

    fig.update_xaxes(
        title=dict(text=x_title, font=dict(size=10.5, color=TEXT_MUTED)),
        showgrid=True,
        gridcolor=GRID_COLOR,
        gridwidth=1,
        zeroline=False,
        tickfont=dict(color=TEXT_MUTED, size=10),
        linecolor="#30363d"
    )
    fig.update_yaxes(
        title=dict(text=y_title, font=dict(size=10.5, color=TEXT_MUTED)),
        showgrid=True,
        gridcolor=GRID_COLOR,
        gridwidth=1,
        zeroline=False,
        tickfont=dict(color=TEXT_MUTED, size=10),
        linecolor="#30363d"
    )
    return fig

def create_lookback_comparison_bars(perf_df: pd.DataFrame):
    """
    Ranked horizontal comparison of Sharpe ratios (Original vs Sensitivity).
    Ample margin and range to guarantee zero label clipping.
    Legend placed cleanly at the bottom.
    """
    df = perf_df.sort_values("Original Sharpe", ascending=True).copy()
    
    fig = go.Figure()
    
    bar_colors = [COLOR_OPTIMAL if lb == 189 else COLOR_SECONDARY if lb == 252 else "#38475a" for lb in df["Lookback"]]
    
    # Original Sharpe bars with clean concise label
    fig.add_trace(go.Bar(
        y=[f"{lb} Days" for lb in df["Lookback"]],
        x=df["Original Sharpe"],
        orientation="h",
        name="Original Backtest",
        marker=dict(color=bar_colors, line=dict(color="#161b22", width=1)),
        text=[f"  {val:.4f} (#{r})" for val, r in zip(df["Original Sharpe"], df["Original Sharpe Rank"])],
        textposition="outside",
        textfont=dict(size=10.5, color=TEXT_BRIGHT, family="JetBrains Mono, monospace"),
        cliponaxis=False
    ))
    
    # Sensitivity Sharpe dots
    fig.add_trace(go.Scatter(
        y=[f"{lb} Days" for lb in df["Lookback"]],
        x=df["Sensitivity Sharpe"],
        mode="markers",
        name="Sensitivity Scenario",
        marker=dict(
            symbol="diamond",
            size=11,
            color=COLOR_SENSITIVITY,
            line=dict(color="#ffffff", width=1)
        ),
        hovertemplate="<b>%{y} Lookback</b><br>Sensitivity Sharpe: %{x:.4f}<extra></extra>"
    ))
    
    # Generous range up to 2.45 to ensure zero truncation of text labels
    fig.update_xaxes(range=[0, 2.45], dtick=0.3)
    
    _apply_institutional_theme(
        fig,
        title="Annualised Sharpe Ratio by Lookback Horizon",
        subtitle="Ranked performance: Original Backtest (bars) vs Sensitivity Scenario (diamonds)",
        x_title="Annualised Sharpe Ratio (Rf = 0%)",
        height=400,
        top_margin=75,
        bottom_margin=60,
        right_margin=75
    )
    return fig

def create_sharpe_cagr_dumbbell(perf_df: pd.DataFrame):
    """
    Clean slope comparison of Sharpe and CAGR degradation.
    Short, well-spaced subplot titles and wide horizontal spacing to eliminate collisions.
    """
    df = perf_df.sort_values("Lookback").copy()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Sharpe Ratio", "CAGR (%)"),
        horizontal_spacing=0.28
    )
    
    for idx, row in df.iterrows():
        lb = int(row["Lookback"])
        is_opt = (lb == 189)
        is_252 = (lb == 252)
        
        color = COLOR_OPTIMAL if is_opt else (COLOR_SECONDARY if is_252 else COLOR_NEUTRAL)
        width = 2.8 if is_opt else (2.0 if is_252 else 1.2)
        opacity = 1.0 if (is_opt or is_252) else 0.45
        
        # Col 1: Sharpe
        fig.add_trace(go.Scatter(
            x=["Original", "Sensitivity"],
            y=[row["Original Sharpe"], row["Sensitivity Sharpe"]],
            mode="lines+markers",
            name=f"{lb}d Horizon",
            line=dict(color=color, width=width),
            marker=dict(size=8 if is_opt else 6, color=color),
            opacity=opacity,
            hovertemplate=f"<b>{lb}d Horizon</b><br>%{{x}}: %{{y:.4f}}<extra></extra>",
            showlegend=True
        ), row=1, col=1)
        
        # Col 2: CAGR
        fig.add_trace(go.Scatter(
            x=["Original", "Sensitivity"],
            y=[row["Original CAGR"] * 100, row["Sensitivity CAGR"] * 100],
            mode="lines+markers",
            name=f"{lb}d Horizon",
            line=dict(color=color, width=width),
            marker=dict(size=8 if is_opt else 6, color=color),
            opacity=opacity,
            hovertemplate=f"<b>{lb}d Horizon</b><br>%{{x}}: %{{y:.1f}}%<extra></extra>",
            showlegend=False
        ), row=1, col=2)
        
    _apply_institutional_theme(
        fig,
        title="Impact of Strict Anomaly Exclusion",
        subtitle="189-Day (cyan) retains Rank #1 in both scenarios; 252-Day in soft blue",
        height=400,
        top_margin=85,
        bottom_margin=60,
        right_margin=40
    )
    
    # Subplot titles placed cleanly below main title
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=12, color=TEXT_BRIGHT, family="Inter, -apple-system, sans-serif")
        
    fig.update_yaxes(title_text="Sharpe Ratio", row=1, col=1, gridcolor=GRID_COLOR, zeroline=False)
    fig.update_yaxes(title_text="CAGR (%)", ticksuffix="%", row=1, col=2, gridcolor=GRID_COLOR, zeroline=False)
    fig.update_xaxes(gridcolor=GRID_COLOR)
    return fig

def create_cumulative_growth_chart(cum_df: pd.DataFrame, lookback: int, show_sens: bool = True, is_log: bool = False):
    """
    Cumulative portfolio growth curve ($1 initial investment).
    Range selector buttons positioned cleanly at top-right (x=1.0) to completely avoid subtitle collision.
    """
    fig = go.Figure()
    
    orig_col = f"{lookback}d_orig"
    sens_col = f"{lookback}d_sens"
    
    orig_equity = 1 + cum_df[orig_col]
    
    fig.add_trace(go.Scatter(
        x=cum_df.index,
        y=orig_equity,
        mode="lines",
        name=f"{lookback}d Original",
        line=dict(color=COLOR_OPTIMAL if lookback == 189 else COLOR_SECONDARY, width=2),
        hovertemplate="%{x|%Y-%m-%d}<br>Original Value: $%{y:,.2f}<br>Cumulative: %{customdata:.2%}<extra></extra>",
        customdata=cum_df[orig_col]
    ))
    
    if show_sens and sens_col in cum_df.columns:
        sens_equity = 1 + cum_df[sens_col]
        fig.add_trace(go.Scatter(
            x=cum_df.index,
            y=sens_equity,
            mode="lines",
            name=f"{lookback}d Sensitivity",
            line=dict(color=COLOR_SENSITIVITY, width=1.8, dash="dot"),
            hovertemplate="%{x|%Y-%m-%d}<br>Sensitivity Value: $%{y:,.2f}<br>Cumulative: %{customdata:.2%}<extra></extra>",
            customdata=cum_df[sens_col]
        ))
        
    scale_label = "Logarithmic Scale (Base 10)" if is_log else "Linear Scale"
    sub = f"Growth of $1.00 starting Jan 2006. Displaying {scale_label}."
    
    _apply_institutional_theme(
        fig,
        title=f"Cumulative Portfolio Growth: {lookback}-Day Horizon",
        subtitle=sub,
        x_title="Date",
        y_title="Portfolio Growth ($)" if not is_log else "Portfolio Growth ($ Log)",
        height=460,
        top_margin=85,
        bottom_margin=50,
        right_margin=30
    )
    
    if is_log:
        fig.update_yaxes(type="log")
        
    # Range selector positioned at top right (x=1.0) so it NEVER overlaps subtitle on the left
    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(count=3, label="3Y", step="year", stepmode="backward"),
                dict(count=5, label="5Y", step="year", stepmode="backward"),
                dict(count=10, label="10Y", step="year", stepmode="backward"),
                dict(step="all", label="All 20Y")
            ]),
            bgcolor=CARD_BG,
            font=dict(color=TEXT_MUTED, size=9.5),
            activecolor="#30363d",
            x=1.0,
            xanchor="right",
            y=1.06,
            yanchor="bottom"
        )
    )
    return fig

def create_drawdown_chart(dd_df: pd.DataFrame, lookback: int, show_sens: bool = True):
    """
    Underwater drawdown curve over time.
    """
    fig = go.Figure()
    
    orig_col = f"{lookback}d_orig"
    sens_col = f"{lookback}d_sens"
    
    fig.add_trace(go.Scatter(
        x=dd_df.index,
        y=dd_df[orig_col] * 100,
        mode="lines",
        name="Original Drawdown",
        line=dict(color=COLOR_RED, width=1.5),
        fill="tozeroy",
        fillcolor="rgba(230, 57, 70, 0.15)",
        hovertemplate="%{x|%Y-%m-%d}<br>Original DD: %{y:.2f}%<extra></extra>"
    ))
    
    if show_sens and sens_col in dd_df.columns:
        fig.add_trace(go.Scatter(
            x=dd_df.index,
            y=dd_df[sens_col] * 100,
            mode="lines",
            name="Sensitivity Drawdown",
            line=dict(color=COLOR_SENSITIVITY, width=1.3, dash="dash"),
            hovertemplate="%{x|%Y-%m-%d}<br>Sens DD: %{y:.2f}%<extra></extra>"
        ))
        
    max_dd = dd_df[orig_col].min() * 100
    sens_max_dd = dd_df[sens_col].min() * 100 if sens_col in dd_df.columns else None
    
    sub = f"Historical Maximum Drawdown: {max_dd:.1f}% (Original)" + (f" vs {sens_max_dd:.1f}% (Sensitivity)" if sens_max_dd else "")
    
    _apply_institutional_theme(
        fig,
        title=f"Drawdown Profile: {lookback}-Day Horizon",
        subtitle=sub,
        x_title="Date",
        y_title="Drawdown (%)",
        height=360,
        top_margin=75,
        bottom_margin=50
    )
    fig.update_yaxes(ticksuffix="%")
    return fig

def create_rolling_sharpe_chart(daily_ret: pd.Series, lookback: int, window: int = 252):
    """
    Rolling 252-day annualised Sharpe ratio with zero benchmark line.
    """
    rolling_mean = daily_ret.rolling(window).mean()
    rolling_std = daily_ret.rolling(window).std(ddof=1)
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)
    rolling_sharpe = rolling_sharpe.dropna()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=rolling_sharpe.index,
        y=rolling_sharpe,
        mode="lines",
        name="1Y Rolling Sharpe",
        line=dict(color=COLOR_OPTIMAL if lookback == 189 else COLOR_SECONDARY, width=1.5),
        hovertemplate="%{x|%Y-%m-%d}<br>Rolling Sharpe: %{y:.2f}<extra></extra>"
    ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="#6e7681", line_width=1)
    
    _apply_institutional_theme(
        fig,
        title=f"1-Year Rolling Sharpe Ratio ({lookback}d Horizon)",
        subtitle="252-trading-day rolling Sharpe (Rf = 0%) demonstrating market cycle variability",
        x_title="Date",
        y_title="Rolling Sharpe",
        height=360,
        top_margin=75,
        bottom_margin=50
    )
    return fig

def create_annual_returns_bar(annual_df: pd.DataFrame, lookback: int):
    """
    Calendar year returns bar chart.
    """
    colors = [COLOR_GREEN if r >= 0 else COLOR_RED for r in annual_df["Return"]]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=annual_df["Year"].astype(str),
        y=annual_df["Return"] * 100,
        marker=dict(color=colors, line=dict(color="#161b22", width=1)),
        text=[f"{r*100:+.0f}%" for r in annual_df["Return"]],
        textposition="outside",
        textfont=dict(size=9.5, color=TEXT_BRIGHT, family="JetBrains Mono, monospace"),
        hovertemplate="Year: %{x}<br>Annual Return: %{y:.2f}%<extra></extra>",
        cliponaxis=False
    ))
    
    _apply_institutional_theme(
        fig,
        title=f"Calendar Year Performance ({lookback}d Horizon)",
        subtitle="Annual compound returns across 2006–2026",
        x_title="Year",
        y_title="Return (%)",
        height=360,
        top_margin=75,
        bottom_margin=50,
        right_margin=30
    )
    fig.update_yaxes(ticksuffix="%")
    return fig

def create_return_distribution_chart(daily_ret: pd.Series, lookback: int):
    """
    Daily return histogram with tail quantile callouts.
    """
    clean_ret = daily_ret.dropna() * 100
    
    q01 = clean_ret.quantile(0.01)
    q99 = clean_ret.quantile(0.99)
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=clean_ret,
        nbinsx=120,
        marker=dict(color="rgba(0, 180, 216, 0.75)", line=dict(color="#0e1117", width=0.5)),
        name="Daily Returns",
        hovertemplate="Daily Return: %{x:.1f}%<br>Count: %{y}<extra></extra>"
    ))
    
    fig.add_vline(x=q01, line_dash="dash", line_color=COLOR_RED, line_width=1.5,
                  annotation_text=f"1% VaR: {q01:.1f}%", annotation_position="top left", annotation_font_size=9.5)
    fig.add_vline(x=q99, line_dash="dash", line_color=COLOR_GREEN, line_width=1.5,
                  annotation_text=f"99% Tail: {q99:.1f}%", annotation_position="top right", annotation_font_size=9.5)
    
    _apply_institutional_theme(
        fig,
        title=f"Empirical Daily Return Distribution ({lookback}d)",
        subtitle=f"Total: {len(clean_ret):,} trading days | Fat tails and extreme kurtosis",
        x_title="Daily Portfolio Return (%)",
        y_title="Frequency",
        height=360,
        top_margin=75,
        bottom_margin=50
    )
    fig.update_xaxes(ticksuffix="%")
    return fig

def create_anomaly_timeline_chart(annual_anom_df: pd.DataFrame):
    """
    Annual distribution of extreme observations and temporary 5x/0.2x scale anomalies.
    """
    fig = go.Figure()
    
    years = annual_anom_df["Year"].astype(str)
    
    fig.add_trace(go.Bar(
        x=years,
        y=annual_anom_df["Extreme_Observations"],
        name="Extreme Moves (≥50%)",
        marker=dict(color="#283445")
    ))
    fig.add_trace(go.Bar(
        x=years,
        y=annual_anom_df["Temporary_5x"],
        name="Temporary ~5x Jumps",
        marker=dict(color=COLOR_SENSITIVITY)
    ))
    fig.add_trace(go.Bar(
        x=years,
        y=annual_anom_df["Temporary_0_2x"],
        name="Temporary ~0.2x Drops",
        marker=dict(color="#f39c12")
    ))
    fig.add_trace(go.Scatter(
        x=years,
        y=annual_anom_df["Strong_Candidates"],
        name="Strong Candidates",
        mode="lines+markers",
        line=dict(color=COLOR_RED, width=2),
        marker=dict(size=7, color=COLOR_RED)
    ))
    
    _apply_institutional_theme(
        fig,
        title="Annual Distribution of Constituent Price Anomalies (189d Strategy)",
        subtitle="Persistent occurrence of severe scale distortions across the 20-year backtest",
        x_title="Year",
        y_title="Observations",
        height=400,
        top_margin=75,
        bottom_margin=60
    )
    fig.update_layout(barmode="stack")
    return fig

def create_signal_exposure_chart(exposure_df: pd.DataFrame):
    """
    Shows how longer lookback windows accumulate anomaly exposure.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[f"{lb} Days" for lb in exposure_df["Lookback"]],
        y=exposure_df["Affected_Percentage"],
        marker=dict(
            color=[COLOR_NEUTRAL, COLOR_NEUTRAL, COLOR_NEUTRAL, COLOR_OPTIMAL, COLOR_SECONDARY],
            line=dict(color="#161b22", width=1)
        ),
        text=[f" {p:.1f}% ({aff:,})" for p, aff in zip(exposure_df["Affected_Percentage"], exposure_df["Affected_Signals"])],
        textposition="outside",
        textfont=dict(size=10.5, color=TEXT_BRIGHT, family="JetBrains Mono, monospace"),
        cliponaxis=False
    ))
    
    _apply_institutional_theme(
        fig,
        title="Signal Exposure to Anomaly Events by Horizon",
        subtitle="Percentage of evaluated monthly signals whose historical window spans at least one strong anomaly event",
        x_title="Lookback Horizon",
        y_title="Signals Affected (%)",
        height=400,
        top_margin=75,
        bottom_margin=50,
        right_margin=30
    )
    fig.update_yaxes(ticksuffix="%", range=[0, 26])
    return fig

def create_price_mcap_discrepancy_scatter(discrepancy_df: pd.DataFrame):
    """
    Scatter plot comparing price return vs market cap return.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=discrepancy_df["Market Cap Return"] * 100,
        y=discrepancy_df["Price Return"] * 100,
        mode="markers",
        text=[f"Ticker: {t}<br>Date: {d}<br>Price Ret: {pr*100:+.1f}%<br>Mcap Ret: {mr*100:+.1f}%" 
              for t, d, pr, mr in zip(discrepancy_df["Ticker"], discrepancy_df["date"], discrepancy_df["Price Return"], discrepancy_df["Market Cap Return"])],
        hovertemplate="%{text}<extra></extra>",
        marker=dict(
            size=8,
            color=COLOR_RED,
            opacity=0.85,
            line=dict(color="#ffffff", width=0.5)
        )
    ))
    
    fig.add_trace(go.Scatter(
        x=[-100, 100],
        y=[-100, 100],
        mode="lines",
        name="Parity (1:1)",
        line=dict(color="#6e7681", dash="dash", width=1)
    ))
    
    _apply_institutional_theme(
        fig,
        title="Price vs Market-Cap Return Discrepancy",
        subtitle="Extreme single-day price spikes (>1,000%) with flat market-cap movement",
        x_title="Market Cap Return (%)",
        y_title="Price Return (%)",
        height=400,
        top_margin=75,
        bottom_margin=60
    )
    fig.update_xaxes(ticksuffix="%")
    fig.update_yaxes(ticksuffix="%")
    return fig

def create_case_study_plot(case_item: dict):
    """
    Dual-panel plot showing price spike & subsequent reversal vs stable market cap.
    Ample headroom on price axis so peak star marker never touches subplot title.
    """
    df = pd.DataFrame(case_item["history"])
    p_max = df["price"].max()
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.22,
        subplot_titles=("Closing Price Trajectory (INR)", "Reported Market Capitalisation (INR)")
    )
    
    # Price line
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["price"],
        mode="lines+markers",
        name="Closing Price",
        line=dict(color=COLOR_RED, width=2.2),
        marker=dict(
            size=[12 if ev else 5 for ev in df["is_event"]],
            color=[COLOR_RED if ev else "#ffffff" for ev in df["is_event"]],
            symbol=["star" if ev else "circle" for ev in df["is_event"]]
        ),
        hovertemplate="Date: %{x}<br>Price: ₹%{y:,.2f}<extra></extra>"
    ), row=1, col=1)
    
    # Mcap line
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["mcap"],
        mode="lines+markers",
        name="Market Cap",
        line=dict(color=COLOR_OPTIMAL, width=2),
        marker=dict(size=5, color=COLOR_OPTIMAL),
        hovertemplate="Date: %{x}<br>Market Cap: ₹%{y:,.0f}<extra></extra>"
    ), row=2, col=1)
    
    _apply_institutional_theme(
        fig,
        title=case_item["title"],
        subtitle=case_item["note"],
        height=450,
        top_margin=85,
        bottom_margin=50
    )
    # Add 25% headroom to price y-axis so the peak star marker never reaches the subplot title
    fig.update_yaxes(title_text="Price (₹)", range=[0, p_max * 1.25], row=1, col=1, gridcolor=GRID_COLOR)
    fig.update_yaxes(title_text="Market Cap (₹)", row=2, col=1, gridcolor=GRID_COLOR)
    fig.update_xaxes(gridcolor=GRID_COLOR)
    return fig
