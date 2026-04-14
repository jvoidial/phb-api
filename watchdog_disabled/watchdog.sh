#!/bin/bash

echo "🛡 PHB v9 WATCHDOG ACTIVE"

cd /data/data/com.termux/files/home/phb-api

while true; do
    if ! pgrep -f uvicorn > /dev/null; then
        echo "[WATCHDOG] restarting kernel..."
        nohup uvicorn main:app --host 0.0.0.0 --port 8000 > log.txt 2>&1 &
    fi
    sleep 5
done
