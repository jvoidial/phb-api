#!/bin/bash

echo "🧠 PHB AI OS INSTALLER STARTING..."

if [ ! -d "phb-api" ]; then
  git clone https://github.com/jvoidial/phb-api.git
fi

cd phb-api || exit 1

mkdir -p phb/{cognition,memory,bridge,supervisor,world_model,sync}

touch phb/__init__.py
touch phb/cognition/__init__.py
touch phb/memory/__init__.py
touch phb/bridge/__init__.py
touch phb/supervisor/__init__.py

export PYTHONPATH=$PWD

pip install -r requirements.txt 2>/dev/null

pkill -f uvicorn || true

echo "🚀 Starting PHB..."
bash phb-api/run.sh &

sleep 3

curl -s http://localhost:8000/ || echo "⚠ Not ready yet"

echo "🟢 INSTALL COMPLETE"
