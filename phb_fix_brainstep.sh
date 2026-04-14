#!/bin/bash

echo "🧠 PHB AUTO FIX: FORCE BRAINSTEP v4 STARTING..."

MAIN_FILE="phb-api/main.py"

# 1. Fix import
if grep -q "from cognition.core import think" "$MAIN_FILE"; then
    sed -i 's/from cognition.core import think/from phb.cognition.core import think/g' "$MAIN_FILE"
    echo "✔ Fixed cognition import → phb.cognition.core"
else
    echo "✔ Import already correct"
fi

# 2. Ensure phb package exists
if [ ! -f "phb/__init__.py" ]; then
    mkdir -p phb
    touch phb/__init__.py
    echo "✔ Created phb package"
fi

if [ ! -f "phb/cognition/__init__.py" ]; then
    mkdir -p phb/cognition
    touch phb/cognition/__init__.py
    echo "✔ Created cognition package"
fi

# 3. Clear Python cache (VERY IMPORTANT)
find . -name "__pycache__" -type d -exec rm -rf {} +
echo "✔ Cleared Python cache"

# 4. Kill old server
pkill -f uvicorn || true
sleep 1

# 5. Restart system
echo "🔄 Restarting PHB runtime..."
bash phb-api/run.sh &

sleep 3

# 6. Test automatically
echo "🧪 Running test..."

curl -s -X POST http://localhost:8000/message \
  -H "Content-Type: application/json" \
  -d '{"message":"brain test"}'

echo ""
echo "🟢 PHB AUTO FIX COMPLETE"
