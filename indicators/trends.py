import pandas as pd

def compute_trend_indicators(df):
    out = pd.DataFrame(index=df.index)

    out["close"] = df["Close"]
    out["ema_20"] = df["Close"].ewm(span=20).mean()
    out["ema_50"] = df["Close"].ewm(span=50).mean()
    out["sma_200"] = df["Close"].rolling(200).mean()

    return out
