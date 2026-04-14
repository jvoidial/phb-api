#!/bin/bash

echo "🧠 PHB v22 DISTRIBUTED EVENT OS STARTING..."

pkill -f uvicorn
pkill -f phb

sleep 1

echo "🚀 Starting API..."

uvicorn main_v22:app --host 0.0.0.0 --port 8000
