#!/bin/bash

echo "[PHB AUTOPATCH] Starting automated fix..."

# 1. Create the router override file
cat << 'PYEOF' > phb_api_autofix.py
from fastapi import FastAPI
from phb_engine_router import route_engine

app = FastAPI()

@app.post("/v1/companion")
def companion(payload: dict):
    return route_engine(payload)
PYEOF

echo "[PHB AUTOPATCH] Created phb_api_autofix.py"

# 2. Create a Procfile override (Railway respects this)
cat << 'PFOEF' > Procfile
web: uvicorn phb_api_autofix:app --host 0.0.0.0 --port \$PORT
PFOEF

echo "[PHB AUTOPATCH] Procfile updated to use phb_api_autofix"

# 3. Make the script executable
chmod +x phb_api_autofix.py

echo "[PHB AUTOPATCH] Patch complete. Redeploy your service."
