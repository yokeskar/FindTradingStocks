from fastapi import FastAPI
from run_scan import run_scan_json

# 🚨 REQUIRED for Railway / Uvicorn
app = FastAPI(title="Probability Forecast API")

# -----------------------------
# Health check (Railway needs this)
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------
# Main scan endpoint (Android uses this)
# -----------------------------
@app.get("/scan")
def scan():
    """
    Returns top bullish & bearish trades as JSON
    """
    return run_scan_json()
