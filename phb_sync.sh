#!/bin/bash

echo "🧬 PHB FULL ORCHESTRATOR SYNC START"

cd ~/phb-api || exit

echo "📦 Adding all files..."
git add .

echo "🧠 Committing unified PHB system..."
git commit -m "PHB ORCHESTRATOR: unified brain + state system + Railway safe architecture"

echo "🚀 Pushing to GitHub..."
git push origin main

echo "✅ Sync complete. Railway will auto-redeploy."
