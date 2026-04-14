#!/bin/bash

echo "🧠 PHB AI OS STARTING (STABLE MODE)..."

cd "$(dirname "$0")/.."

export PYTHONPATH=$(pwd)

pkill -f uvicorn || true
sleep 1

uvicorn phb-api.main:app --host 0.0.0.0 --port 8000
