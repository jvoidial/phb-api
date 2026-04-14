import os
import time
import json
import subprocess
from datetime import datetime, timezone

GCS_DIR = "gcs"
STATE_FILE = "phb_gcs_state.json"
LAST_HASH_FILE = ".phb_last_hash"

SYNC_INTERVAL = 10  # seconds

def scan(path):
    tree = {}
    for root, dirs, files in os.walk(path):
        rel = os.path.relpath(root, path)
        tree[rel] = {"files": files, "dirs": dirs}
    return tree

def build_state():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "gcs_tree": scan(GCS_DIR) if os.path.exists(GCS_DIR) else {},
        "system": "PHB-GLOBAL-SYNC-v1"
    }

def hash_state(state):
    return str(hash(json.dumps(state, sort_keys=True)))

def load_last_hash():
    if os.path.exists(LAST_HASH_FILE):
        return open(LAST_HASH_FILE).read().strip()
    return None

def save_hash(h):
    with open(LAST_HASH_FILE, "w") as f:
        f.write(h)

def write_json(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def git_holy_commit(msg):
    try:
        subprocess.call(["git", "add", "-A"])
        subprocess.call(["git", "commit", "-m", msg])
        subprocess.call(["git", "push", "origin", "main"])
        print("🔥 HOLY COMMIT PUSHED")
    except Exception as e:
        print("⚠️ Git error:", e)

def run():
    print("🧠 PHB GLOBAL SYNC DAEMON STARTED")

    while True:
        state = build_state()
        state_hash = hash_state(state)

        last = load_last_hash()

        # Only act if state changed
        if state_hash != last:
            print("🔄 State change detected")

            write_json(state)
            save_hash(state_hash)

            # “Holy commit” snapshot
            git_holy_commit("PHB HOLY SYNC CHECKPOINT")

        else:
            print("✔ No changes")

        time.sleep(SYNC_INTERVAL)

if __name__ == "__main__":
    run()
