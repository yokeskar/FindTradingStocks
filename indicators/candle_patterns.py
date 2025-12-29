# indicators/candle_patterns.py

def detect_candle_pattern(df):
    """
    Detect basic single / two-candle patterns using Yahoo OHLC format:
    Open, High, Low, Close
    """

    if df is None or len(df) < 2:
        return None

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    # Bullish Engulfing
    if (
        curr["Close"] > curr["Open"]
        and prev["Close"] < prev["Open"]
        and curr["Open"] <= prev["Close"]
        and curr["Close"] >= prev["Open"]
    ):
        return "Bullish_Engulfing"

    # Bearish Engulfing
    if (
        curr["Close"] < curr["Open"]
        and prev["Close"] > prev["Open"]
        and curr["Open"] >= prev["Close"]
        and curr["Close"] <= prev["Open"]
    ):
        return "Bearish_Engulfing"

    # Hammer
    body = abs(curr["Close"] - curr["Open"])
    lower_wick = min(curr["Open"], curr["Close"]) - curr["Low"]

    if lower_wick > 2 * body:
        return "Hammer"

    # Shooting Star
    upper_wick = curr["High"] - max(curr["Open"], curr["Close"])

    if upper_wick > 2 * body:
        return "Shooting_Star"

    return None
