#!/bin/bash

echo "🧠 PHB FULL SYNC PATCH STARTING..."

cd /data/data/com.termux/files/home/phb-api || exit 1

echo "🧹 Stopping old services..."
pkill -f uvicorn
pkill -f python
sleep 1

echo "🧠 Fixing runtime state safety..."

# -----------------------------
# SAFE MAIN.PY PATCH (crash-proof API)
# -----------------------------
cat << 'PY' > main.py
from fastapi import FastAPI, Request
from phb_orchestrator_v4_2 import run_agent
import traceback

app = FastAPI(title="PHB SAFE CORE v5")

STATE = {
    "turns": 0,
    "memory": [],
    "energy": 5.0,
    "mood": "stable"
}

@app.post("/message")
async def message(req: Request):
    try:
        data = await req.json()

        msg = data.get("message", "")
        user_id = data.get("user_id", "default")

        STATE["turns"] += 1

        # SAFE CALL (prevents total crash)
        result = run_agent(msg, STATE)

        # ensure state always exists
        if isinstance(result, dict):
            STATE.update(result.get("state", STATE))

        return result

    except Exception as e:
        traceback.print_exc()
        return {
            "error": str(e),
            "status": "PHB SAFE MODE ACTIVE"
        }

@app.get("/")
def root():
    return {
        "status": "PHB SAFE CORE ONLINE",
        "mode": "stable-runtime"
    }
PY

echo "🧠 Creating safe run script..."

cat << 'RUN' > run.sh
#!/bin/bash

echo "🧠 PHB SAFE CORE BOOTING..."

cd /data/data/com.termux/files/home/phb-api

pkill -f uvicorn
sleep 1

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
RUN

chmod +x run.sh

echo "✅ PATCH COMPLETE"
echo "👉 START WITH: ./run.sh"
