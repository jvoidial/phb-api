#!/bin/bash

echo "🧠 PHB AI OS v7.1 STARTING..."

cd "$(dirname "$0")"

# kill only uvicorn (safe)
pkill -f "uvicorn main:app" || true

sleep 1

uvicorn main:app --host 0.0.0.0 --port 8000
