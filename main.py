from models.forecast_engine import generate_forecast

if __name__ == "__main__":
    symbol = "BEL.NS"       # Replace with your ticker
    days = 14               # Forecast horizon
    expiry = "2025-12-30"   # Optional: if your option API needs expiry

    result = generate_forecast(symbol, days, expiry)

    print("\n===== Probability-Driven Forecast =====")
    print("Symbol:", result["symbol"])
    print("Last Price:", result["last_price"])
    print("Bias:", result["bias"])
    print("ATM IV:", result["atm_iv_percent"])
    print("Expected Move (±1σ):", result["expected_move_1s"])

    print("\n--- Levels ---")
    for k, v in result["levels"].items():
        print(f"{k}: {v}")

    print("\n--- Probabilities ---")
    for k, v in result["probs"].items():
        if v is not None:
            print(f"P(price > {k}) => {v:.2%}")

    print("\n--- Indicators ---")
    for k, v in result["indicators"].items():
        print(k, ":", v)

    print("\n--- Volume Profile (Top Zones) ---")
    for zone, vol in result["top_volume_bins"]:
        print(zone, "=>", vol)

    print("\n--- Option Chain Metrics ---")
    for k, v in result["option_metrics"].items():
        print(k, ":", v)
