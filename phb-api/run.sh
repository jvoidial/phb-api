#!/bin/bash

echo "🧠 PHB AI OS STARTING (CLEAN ROOT MODE)..."

cd "$(dirname "$0")"

export PYTHONPATH=$PWD

pkill -f "uvicorn main:app" || true
sleep 1

exec uvicorn main:app --host 0.0.0.0 --port 8000
