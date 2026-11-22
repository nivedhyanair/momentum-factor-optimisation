"""
data_loader.py
Provides cached access to all precomputed datasets, metrics, and anomaly logs.
"""
import os
import json
import pandas as pd
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(__file__), "data_cache")

@st.cache_data
def load_universe_meta():
    with open(os.path.join(DATA_DIR, "universe.json"), "r") as f:
        return json.load(f)

@st.cache_data
def load_performance_comparison():
    path = os.path.join(DATA_DIR, "final_performance_comparison.json")
    with open(path, "r") as f:
        data = json.load(f)
    return pd.DataFrame(data)

@st.cache_data
def load_daily_returns():
    path = os.path.join(DATA_DIR, "daily_returns.parquet")
    return pd.read_parquet(path)

@st.cache_data
def load_cumulative_returns():
    path = os.path.join(DATA_DIR, "cum_returns.parquet")
    return pd.read_parquet(path)

@st.cache_data
def load_drawdowns():
    path = os.path.join(DATA_DIR, "drawdowns.parquet")
    return pd.read_parquet(path)

@st.cache_data
def load_rebalance_holdings(lookback: int):
    path = os.path.join(DATA_DIR, f"rebalance_holdings_{lookback}d.parquet")
    return pd.read_parquet(path)

@st.cache_data
def load_reversal_classification():
    with open(os.path.join(DATA_DIR, "reversal_classification.json"), "r") as f:
        return pd.DataFrame(json.load(f))

@st.cache_data
def load_ticker_anomaly_summary():
    with open(os.path.join(DATA_DIR, "ticker_anomaly_summary.json"), "r") as f:
        return pd.DataFrame(json.load(f))

@st.cache_data
def load_price_mcap_discrepancy():
    with open(os.path.join(DATA_DIR, "price_mcap_discrepancy.json"), "r") as f:
        return pd.DataFrame(json.load(f))

@st.cache_data
def load_annual_anomaly_summary():
    with open(os.path.join(DATA_DIR, "annual_anomaly_summary.json"), "r") as f:
        return pd.DataFrame(json.load(f))

@st.cache_data
def load_strong_anomaly_events():
    with open(os.path.join(DATA_DIR, "strong_anomaly_events.json"), "r") as f:
        return pd.DataFrame(json.load(f))

@st.cache_data
def load_anomaly_attribution():
    with open(os.path.join(DATA_DIR, "anomaly_attribution.json"), "r") as f:
        return pd.DataFrame(json.load(f))

@st.cache_data
def load_signal_exposure():
    with open(os.path.join(DATA_DIR, "signal_exposure.json"), "r") as f:
        return pd.DataFrame(json.load(f))

@st.cache_data
def load_cross_lookback_anomalies():
    with open(os.path.join(DATA_DIR, "cross_lookback_anomalies.json"), "r") as f:
        return pd.DataFrame(json.load(f))

@st.cache_data
def load_residual_anomalies():
    with open(os.path.join(DATA_DIR, "residual_anomalies.json"), "r") as f:
        return pd.DataFrame(json.load(f))

@st.cache_data
def load_broad_scale_candidates():
    with open(os.path.join(DATA_DIR, "broad_scale_candidates.json"), "r") as f:
        return pd.DataFrame(json.load(f))

@st.cache_data
def load_case_studies():
    with open(os.path.join(DATA_DIR, "case_studies.json"), "r") as f:
        return json.load(f)
