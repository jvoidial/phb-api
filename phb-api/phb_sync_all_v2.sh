#!/usr/bin/env bash

set -e

echo "[PHB SYNC] Starting sync..."

# Absolute paths to your real repos
API_REPO="/data/data/com.termux/files/home/phb-api"
VORTEX_REPO="/data/data/com.termux/files/home/phb-godcode-vortex"

# Files to sync
FILES=(
  "phb_science_plugin.py"
  "phb_science_registry.py"
  "phb_science_validate.py"
  "phb_api_science_integration.py"
  "phb_godcode_science_bridge.py"
)

sync_files() {
  local repo="$1"
  echo "[PHB SYNC] Syncing to $repo"

  cd "$repo"
  git pull --rebase

  cd -

  for f in "${FILES[@]}"; do
    if [[ -f "$f" ]]; then
      cp "$f" "$repo/"
      echo "[PHB SYNC] Copied $f → $repo/"
    else
      echo "[PHB SYNC] WARNING: $f not found"
    fi
  done

  cd "$repo"
  git add .
  git commit -m "PHB Science Layer Sync: $(date)"
  git push
  cd -
}

sync_files "$API_REPO"
sync_files "$VORTEX_REPO"

echo "[PHB SYNC] Complete."
