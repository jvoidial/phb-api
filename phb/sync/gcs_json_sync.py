import os
import json
from datetime import datetime, timezone

GCS_DIR = "gcs"
OUTPUT_FILE = "phb_gcs_state.json"

def scan_folder(path):
    tree = {}

    for root, dirs, files in os.walk(path):
        rel = os.path.relpath(root, path)
        tree[rel] = {
            "files": files,
            "dirs": dirs
        }

    return tree

def build_state():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "gcs_tree": scan_folder(GCS_DIR) if os.path.exists(GCS_DIR) else {},
        "system": "PHB-GCS-SYNC-v1"
    }

def export_json():
    state = build_state()

    with open(OUTPUT_FILE, "w") as f:
        json.dump(state, f, indent=2)

    return state

if __name__ == "__main__":
    print("🧠 Syncing GCS → AI JSON state...")
    state = export_json()
    print("✔ Sync complete:", OUTPUT_FILE)
