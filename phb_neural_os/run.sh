#!/bin/bash

echo "🧠 PHB NEURAL OS MASTER BOOT"

cd /data/data/com.termux/files/home/phb-api

# kill any old servers safely
pkill -f uvicorn

# optional: give system breathing time
sleep 1

# ALWAYS use single stable entrypoint
uvicorn main:app --host 0.0.0.0 --port 8000
