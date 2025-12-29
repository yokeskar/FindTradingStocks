# data/spot_data.py
import time
import yfinance as yf
import pandas as pd

def fetch_spot_data(symbol, period="6mo", interval="1d", max_retries=3, pause=1.0):
    """
    Robust fetcher using yf.Ticker().history() with retries.
    Returns a DataFrame or an empty DataFrame on failure.
    """
    if symbol is None:
        return pd.DataFrame()

    last_exception = None
    for attempt in range(1, max_retries + 1):
        try:
            t = yf.Ticker(symbol)
            df = t.history(period=period, interval=interval, auto_adjust=True, actions=False)

            if df is None:
                df = pd.DataFrame()

            if not df.empty:
                needed = ["Open", "High", "Low", "Close", "Volume"]
                missing = [c for c in needed if c not in df.columns]

                if missing:
                    # Fallback to download once if history missing data
                    tmp = yf.download(symbol, period=period, interval=interval, progress=False, auto_adjust=True)
                    if tmp is not None and not tmp.empty:
                        df = tmp

                if df is not None and not df.empty:
                    return df

            # if empty, retry
            raise ValueError("Empty spot data received")

        except Exception as exc:
            last_exception = exc
            print(f"[fetch_spot_data] Retry {attempt}/{max_retries} for {symbol} due to: {exc}")
            time.sleep(pause * attempt)

    print(f"[fetch_spot_data] FAILED for {symbol}: {last_exception}")
    return pd.DataFrame()
