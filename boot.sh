#!/bin/bash

echo "🧠 PHB AI OS STARTING..."

pkill -f uvicorn >/dev/null 2>&1
sleep 1

exec uvicorn main:app --host 0.0.0.0 --port 8000
