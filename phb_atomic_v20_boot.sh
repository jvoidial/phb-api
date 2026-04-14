#!/bin/bash

echo "🧠 PHB ATOMIC v20 SAFE BOOT (PID CONTROL MODE)"

# -----------------------------
# 1. STOP ONLY UVICORN SAFELY
# -----------------------------
echo "🧹 Finding uvicorn process..."

UVICORN_PIDS=$(pgrep -f "uvicorn main:app")

if [ ! -z "$UVICORN_PIDS" ]; then
    echo "🔪 Stopping uvicorn: $UVICORN_PIDS"
    kill -9 $UVICORN_PIDS
else
    echo "✅ No uvicorn running"
fi

# -----------------------------
# 2. STOP KERNEL SAFELY
# -----------------------------
KERNEL_PIDS=$(pgrep -f "start_kernel.py")

if [ ! -z "$KERNEL_PIDS" ]; then
    echo "🔪 Stopping kernel: $KERNEL_PIDS"
    kill -9 $KERNEL_PIDS
else
    echo "✅ No kernel running"
fi

sleep 1

# -----------------------------
# 3. CLEAN CACHE
# -----------------------------
echo "🧽 Cleaning cache..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

# -----------------------------
# 4. VERIFY FILES
# -----------------------------
echo "🔍 Verifying v20 system..."

for f in main.py event_bus.py kernel_worker.py start_kernel.py; do
    if [ ! -f "$f" ]; then
        echo "❌ Missing $f"
        exit 1
    fi
done

echo "✅ System OK"

# -----------------------------
# 5. START KERNEL
# -----------------------------
echo "⚙️ Starting kernel..."
nohup python start_kernel.py > kernel.log 2>&1 &

sleep 2

# -----------------------------
# 6. START API (SAFE)
# -----------------------------
echo "🚀 Starting API..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
