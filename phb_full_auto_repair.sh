#!/bin/bash

echo "🧠 PHB FULL AUTO REPAIR STARTING..."

BASE_DIR="$(pwd)"

# -----------------------------
# 1. Ensure Python package roots
# -----------------------------
echo "✔ Setting Python package structure..."
touch phb/__init__.py
touch phb/cognition/__init__.py
touch phb/memory/__init__.py
touch phb/supervisor/__init__.py

# -----------------------------
# 2. Fix PYTHONPATH root
# -----------------------------
echo "✔ Setting PYTHONPATH..."
export PYTHONPATH="$BASE_DIR"

# -----------------------------
# 3. Fix API import alignment
# -----------------------------
echo "✔ Fixing API imports..."

if [ -f phb-api/main.py ]; then
  sed -i 's/from phb\.cognition\.core import think/from phb.cognition.core import think/g' phb-api/main.py
  sed -i 's/from cognition\.core import think/from phb.cognition.core import think/g' phb-api/main.py
fi

# -----------------------------
# 4. Clean Python cache
# -----------------------------
echo "✔ Cleaning cache..."
find . -type d -name "__pycache__" -exec rm -rf {} +

# -----------------------------
# 5. Fix uvicorn launcher
# -----------------------------
echo "✔ Fixing run script..."

cat << 'RUNEOF' > phb-api/run.sh
#!/bin/bash

echo "🧠 PHB AI OS STARTING (FULL AUTO REPAIRED MODE)..."

cd phb-api
export PYTHONPATH=$(pwd)/..

pkill -f "uvicorn main:app" || true
sleep 1

exec uvicorn main:app --host 0.0.0.0 --port 8000
RUNEOF

chmod +x phb-api/run.sh

# -----------------------------
# 6. Validate structure
# -----------------------------
echo "✔ Validating structure..."

if [ ! -f phb/cognition/core.py ]; then
  echo "❌ ERROR: cognition core missing"
else
  echo "✔ cognition core OK"
fi

if [ ! -f phb-api/main.py ]; then
  echo "❌ ERROR: API main missing"
else
  echo "✔ API main OK"
fi

# -----------------------------
# 7. Done
# -----------------------------
echo "🟢 PHB FULL AUTO REPAIR COMPLETE"
echo "👉 Run: bash phb-api/run.sh"
