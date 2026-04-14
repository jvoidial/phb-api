#!/bin/bash

echo "🧠 PHB v23 BOOT (CONTROL PLANE MODE)"

LOCK="/tmp/phb_v23.lock"

# HARD CLEAN OLD PROCESSES
echo "🧹 Cleaning old uvicorn instances..."
pkill -f uvicorn
pkill -f main_v23

sleep 1

# CHECK LOCK
if [ -f "$LOCK" ]; then
    OLD_PID=$(cat $LOCK)
    echo "🔒 Existing PHB detected PID=$OLD_PID"

    if kill -0 $OLD_PID 2>/dev/null; then
        echo "❌ Already running. Exit."
        exit 1
    else
        echo "🧹 Removing stale lock"
        rm $LOCK
    fi
fi

echo "🚀 Starting PHB v23 API..."

uvicorn main_v23:app --host 0.0.0.0 --port 8000
