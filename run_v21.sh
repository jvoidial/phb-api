#!/bin/bash

echo "🧠 PHB v21 BOOT SEQUENCE"

# kill old system safely
pkill -f uvicorn
pkill -f main_v21

sleep 1

echo "🚀 Starting PHB v21 API..."

uvicorn main_v21:app --host 0.0.0.0 --port 8000
