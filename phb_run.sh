#!/bin/bash
echo "🧠 Starting PHB Neural v2..."
uvicorn main:app --host 0.0.0.0 --port 8000
