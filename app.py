from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from run_scan import run_scan_json

app = FastAPI(title="Market Scan API")

# -----------------------------
# CORS (for Android / Web)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# HEALTH CHECK ENDPOINT
# -----------------------------
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "market-scan-api"
    }

# -----------------------------
# MAIN SCAN ENDPOINT
# -----------------------------
@app.get("/scan")
def scan_market():
    return run_scan_json()
