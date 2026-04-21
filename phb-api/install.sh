#!/bin/bash

echo "🧠 PHB AI OS INSTALLER STARTING..."

# Clone if needed
if [ ! -d "phb-api" ]; then
  git clone https://github.com/jvoidial/phb-api.git
fi

cd phb-api || exit 1

echo "✔ Repo loaded"

# Fix package structure
mkdir -p phb/{cognition,memory,bridge,supervisor,world_model,sync}

touch phb/__init__.py
touch phb/cognition/__init__.py
touch phb/memory/__init__.py
touch phb/bridge/__init__.py
touch phb/supervisor/__init__.py

echo "✔ Structure ready"

# Set import path
export PYTHONPATH=$PWD

echo "✔ PYTHONPATH set"

# Install dependencies
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi

echo "✔ Dependencies installed"

# Clean old processes
pkill -f uvicorn || true

echo "✔ Runtime cleaned"

# Start system
echo "🚀 Starting PHB OS..."
bash phb-api/run.sh &

sleep 3

# Health check
curl -s http://localhost:8000/ || echo "⚠ Server starting..."

echo ""
echo "🟢 PHB INSTALL COMPLETE"
echo "👉 Running at http://localhost:8000"
