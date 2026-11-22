"""
analytics.py
Quantitative calculations, time-series transforms, and metric formatting.
"""
import numpy as np
import pandas as pd

TRADING_DAYS = 252

def calculate_rolling_sharpe(returns: pd.Series, window: int = 252) -> pd.Series:
    """
    Calculate rolling annualised Sharpe ratio over a specified trading-day window.
    Assumes zero risk-free rate.
    """
    rolling_mean = returns.rolling(window).mean()
    rolling_std = returns.rolling(window).std(ddof=1)
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(TRADING_DAYS)
    return rolling_sharpe.dropna()

def calculate_annual_returns(returns: pd.Series) -> pd.DataFrame:
    """
    Calculate annual compound return for each calendar year.
    """
    clean_ret = returns.dropna()
    years = clean_ret.index.year.unique()
    records = []
    for y in sorted(years):
        sub = clean_ret[clean_ret.index.year == y]
        if len(sub) > 0:
            ann_ret = np.prod(1 + sub) - 1
            vol = sub.std(ddof=1) * np.sqrt(TRADING_DAYS)
            mean_r = sub.mean()
            sharpe = (mean_r / sub.std(ddof=1)) * np.sqrt(TRADING_DAYS) if sub.std(ddof=1) > 0 else np.nan
            records.append({
                "Year": y,
                "Return": ann_ret,
                "Volatility": vol,
                "Sharpe": sharpe,
                "Trading_Days": len(sub)
            })
    return pd.DataFrame(records)

def calculate_monthly_returns_matrix(returns: pd.Series) -> pd.DataFrame:
    """
    Calculate monthly compound returns in a Year x Month pivot table.
    """
    clean_ret = returns.dropna()
    monthly = clean_ret.groupby([clean_ret.index.year, clean_ret.index.month]).apply(
        lambda s: np.prod(1 + s) - 1
    ).unstack()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly.columns = [month_names[m - 1] for m in monthly.columns]
    return monthly

def calculate_distribution_stats(returns: pd.Series) -> dict:
    """
    Calculate statistical distribution moments and tail characteristics.
    """
    clean_ret = returns.dropna().astype(float)
    pos_days = (clean_ret > 0).sum()
    neg_days = (clean_ret < 0).sum()
    flat_days = (clean_ret == 0).sum()
    win_rate = pos_days / len(clean_ret) if len(clean_ret) > 0 else 0

    return {
        "count": len(clean_ret),
        "mean": clean_ret.mean(),
        "std": clean_ret.std(ddof=1),
        "skew": clean_ret.skew(),
        "kurtosis": clean_ret.kurtosis(),
        "min": clean_ret.min(),
        "max": clean_ret.max(),
        "q01": clean_ret.quantile(0.01),
        "q05": clean_ret.quantile(0.05),
        "median": clean_ret.median(),
        "q95": clean_ret.quantile(0.95),
        "q99": clean_ret.quantile(0.99),
        "pos_days": int(pos_days),
        "neg_days": int(neg_days),
        "flat_days": int(flat_days),
        "win_rate": win_rate,
        "days_above_10pct": int((clean_ret > 0.10).sum()),
        "days_above_25pct": int((clean_ret > 0.25).sum()),
        "days_above_50pct": int((clean_ret > 0.50).sum()),
        "days_below_neg10pct": int((clean_ret < -0.10).sum()),
        "days_below_neg25pct": int((clean_ret < -0.25).sum()),
        "days_below_neg50pct": int((clean_ret < -0.50).sum()),
    }

def format_pct(val, decimals=2, sign=False) -> str:
    if val is None or np.isnan(val):
        return "N/A"
    prefix = "+" if sign and val > 0 else ""
    return f"{prefix}{val * 100:.{decimals}f}%"

def format_mult(val, decimals=2) -> str:
    if val is None or np.isnan(val):
        return "N/A"
    if abs(val) >= 1e6:
        return f"{val / 1e6:.{decimals}f}M×"
    elif abs(val) >= 1e3:
        return f"{val / 1e3:.{decimals}f}k×"
    return f"{val:.{decimals}f}×"

def format_num(val, decimals=4) -> str:
    if val is None or np.isnan(val):
        return "N/A"
    return f"{val:.{decimals}f}"
