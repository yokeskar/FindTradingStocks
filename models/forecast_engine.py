# models/forecast_engine.py

from data.spot_data import fetch_spot_data
from data.option_chain import fetch_option_chain
from indicators.vwap import compute_vwap
from indicators.volume_profile import compute_volume_profile
from indicators.trends import compute_trend_indicators
from indicators.momentum import compute_rsi, compute_macd
from indicators.candle_patterns import detect_candle_pattern
from models.probability import implied_move, probability_above
import numpy as np


def generate_forecast(symbol, days, expiry):
    df = fetch_spot_data(symbol)
    if df is None or df.empty:
        raise Exception("No spot data")

    last_price = df["Close"].iloc[-1]

    # ---------------- Indicators ----------------
    trends = compute_trend_indicators(df)
    rsi = compute_rsi(df)
    macd, signal = compute_macd(df)
    vwap = compute_vwap(df)
    vp = compute_volume_profile(df)

    # ---------------- Candle Pattern ----------------
    candle = detect_candle_pattern(df)

    # ---------------- Option chain ----------------
    opt = fetch_option_chain(symbol, expiry)

    # ---------------- Estimated IV (fallback) ----------------
    returns = df["Close"].pct_change().dropna()
    hv = returns.rolling(21).std().iloc[-1] * np.sqrt(252)
    atm_iv = hv * 100

    # ---------------- Expected move ----------------
    exp_move = implied_move(last_price, atm_iv, days)
    up = last_price + exp_move
    down = last_price - exp_move

    levels = {
        "current": last_price,
        "bullish_target": up,
        "bearish_target": down
    }

    probs = {
        "upside_prob": probability_above(last_price, up, atm_iv, days),
        "downside_prob": 1 - probability_above(last_price, down, atm_iv, days)
    }

    # ---------------- Bias scoring (UNCHANGED) ----------------
    bias_score = 0
    if last_price > trends["ema_20"].iloc[-1]:
        bias_score += 1
    if last_price > trends["ema_50"].iloc[-1]:
        bias_score += 1
    if rsi.iloc[-1] > 55:
        bias_score += 1
    if macd.iloc[-1] > signal.iloc[-1]:
        bias_score += 1

    if bias_score >= 3:
        bias = "Bullish"
    elif bias_score <= 1:
        bias = "Bearish"
    else:
        bias = "Neutral"

    # ---------------- Base confidence ----------------
    base_confidence = min(bias_score / 4.0, 1.0)

    # ---------------- NEW: Candle-weighted confidence ----------------
    candle_adjust = 0.0

    bullish_candles = ("Bullish_Engulfing", "Hammer")
    bearish_candles = ("Bearish_Engulfing", "Shooting_Star")

    if bias == "Bullish":
        if candle in bullish_candles:
            candle_adjust = 0.10
        elif candle in bearish_candles:
            candle_adjust = -0.10

    elif bias == "Bearish":
        if candle in bearish_candles:
            candle_adjust = 0.10
        elif candle in bullish_candles:
            candle_adjust = -0.10

    confidence_weighted = round(
        max(0.0, min(base_confidence + candle_adjust, 1.0)),
        2
    )

    # ---------------- Output ----------------
    return {
        "symbol": symbol,
        "last_price": last_price,
        "atm_iv_percent": atm_iv,
        "expected_move_1s": exp_move,
        "levels": levels,
        "probs": probs,
        "bias": bias,
        "candle": candle,

        # ✅ NEW
        "confidence": confidence_weighted,

        "indicators": {
            "rsi": rsi.iloc[-1],
            "macd": macd.iloc[-1],
            "signal": signal.iloc[-1],
            "ema_20": trends["ema_20"].iloc[-1],
            "ema_50": trends["ema_50"].iloc[-1],
            "sma_200": trends["sma_200"].iloc[-1],
            "vwap": vwap.iloc[-1]
        },

        "top_volume_bins": sorted(vp.items(), key=lambda x: x[1], reverse=True)[:3],
        "option_metrics": {}
    }
