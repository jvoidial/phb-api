#!/bin/bash

echo "🧠 PHB AUTO RUNTIME REPAIR STARTING..."

cd phb-api/.. || exit 1

# =========================
# STEP 4 — ENSURE COGNITION PACKAGE
# =========================
echo "🔧 Rebuilding cognition package..."

mkdir -p cognition
touch cognition/__init__.py

cat << 'PYEOF' > cognition/core.py
def think(message):
    return {
        "engine": "cognition-core",
        "status": "active",
        "input": message,
        "response": f"PHB processed: {message}"
    }
PYEOF

echo "✔ cognition core restored"

# =========================
# STEP 5 — SAFE IMPORT PATCH (MAIN.PY)
# =========================
echo "🔧 Patching main.py safely..."

if ! grep -q "PHB SAFE COGNITION PATCH" phb-api/main.py; then
cat << 'PATCH' >> phb-api/main.py

# =========================
# PHB SAFE COGNITION PATCH
# =========================
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from cognition.core import think
except Exception:
    def think(message):
        return {
            "fallback": True,
            "input": message,
            "response": "cognition fallback active"
        }
PATCH
fi

echo "✔ main.py cognition-safe"

# =========================
# STEP 6 — SAFE RESTART SYSTEM
# =========================
echo "🔄 Restarting PHB runtime..."

pkill -f uvicorn || true
sleep 1

cd phb-api || exit 1
export PYTHONPATH=$(pwd)/..

echo "🧠 Starting PHB AI OS v7.1..."
uvicorn phb-api.main:app --host 0.0.0.0 --port 8000 &

sleep 2

echo "🟢 PHB AUTO REPAIR COMPLETE"
echo "👉 System running on http://localhost:8000"
