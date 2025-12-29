import numpy as np

def compute_volume_profile(df, bins=20):
    prices = df["Close"]
    volumes = df["Volume"]

    edges = np.linspace(prices.min(), prices.max(), bins + 1)
    profile = {}

    for i in range(bins):
        mask = (prices >= edges[i]) & (prices < edges[i+1])
        profile[(edges[i], edges[i+1])] = volumes[mask].sum()

    return profile
