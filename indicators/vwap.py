def compute_vwap(df):
    typical = (df["High"] + df["Low"] + df["Close"]) / 3
    v = df["Volume"]
    return (typical * v).cumsum() / v.cumsum()
