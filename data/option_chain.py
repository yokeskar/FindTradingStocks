# data/option_chain.py
import pandas as pd

def fetch_option_chain(symbol, expiry=None):
    """
    Placeholder function.
    Must return a DataFrame with columns:
    strike, call_oi, put_oi, call_iv, put_iv
    Currently returning empty DF so forecast engine falls back to hist-vol.
    """
    return pd.DataFrame()
