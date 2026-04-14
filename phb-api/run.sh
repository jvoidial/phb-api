#!/bin/bash

echo "🧠 PHB AI OS STARTING (PERSISTENT MODE)..."

cd phb-api
export PYTHONPATH=$(pwd)/..

pkill -f uvicorn || true
sleep 1

exec uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --log-level info \
  --access-log
