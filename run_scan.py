import concurrent.futures
import time
from models.forecast_engine import generate_forecast
from data.spot_data import fetch_spot_data

# ----- NIFTY 50 ticker list -----
NIFTY50_TICKERS = [
    "RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS",
    "KOTAKBANK.NS","SBIN.NS","ITC.NS","LT.NS","AXISBANK.NS",
    "BAJFINANCE.NS","BHARTIARTL.NS","ASIANPAINT.NS","ULTRACEMCO.NS",
    "ONGC.NS","NTPC.NS","POWERGRID.NS","TITAN.NS","MARUTI.NS",
    "SUNPHARMA.NS","HINDUNILVR.NS","WIPRO.NS","TECHM.NS","ADANIENT.NS"
]

HORIZON_DAYS = 2
MAX_WORKERS = 6


# -------------------------------------------------------
# INTERNAL CORE LOGIC (REUSABLE)
# -------------------------------------------------------
def run_scan_internal():
    results = []

    def process_symbol(sym):
        try:
            df = fetch_spot_data(sym, period="3mo", interval="1d")
            if df is None or df.empty:
                return None

            res = generate_forecast(sym, days=HORIZON_DAYS, expiry=None)

            return {
                "symbol": sym,
                "last_price": res["last_price"],
                "down_prob": res["probs"]["downside_prob"],
                "atm_iv": res["atm_iv_percent"],
                "expected_move_1s": res["expected_move_1s"],
                "confidence": res.get("bias_confidence", 0.0),
                "candle": res.get("candle"),
                "bias": res["bias"]
            }

        except Exception as e:
            print(f"Error processing {sym}: {e}")
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(process_symbol, s) for s in NIFTY50_TICKERS]
        for f in concurrent.futures.as_completed(futures):
            r = f.result()
            if r:
                results.append(r)

    return results


# -------------------------------------------------------
# JSON OUTPUT (FOR API)
# -------------------------------------------------------
def run_scan_json():
    scan_results = run_scan_internal()

    return [
        {
            "symbol": r["symbol"],
            "last": round(r["last_price"], 2),
            "down_prob": round(r["down_prob"], 3),
            "atm_iv": round(r["atm_iv"], 2),
            "exp_move": round(r["expected_move_1s"], 2),
            "conf": round(r["confidence"], 2),
            "candle": r["candle"],
            "bias": r["bias"]
        }
        for r in scan_results
    ]


# -------------------------------------------------------
# CLI OUTPUT (OPTIONAL)
# -------------------------------------------------------
def run_scan():
    start = time.time()
    results = run_scan_internal()

    print("\nTOP PROBABLE TRADES:\n")
    print("symbol | last | down_prob | atm_iv | exp_move | conf | candle | bias")

    for r in results:
        print(
            f"{r['symbol']:10} | "
            f"{r['last_price']:.2f} | "
            f"{r['down_prob']:.2f} | "
            f"{r['atm_iv']:.2f} | "
            f"{r['expected_move_1s']:.2f} | "
            f"{r['confidence']:.2f} | "
            f"{r['candle']} | "
            f"{r['bias']}"
        )

    print(f"\nScan completed in {time.time() - start:.1f}s")


if __name__ == "__main__":
    run_scan()
