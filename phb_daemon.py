import subprocess
import time
import requests
import os
from datetime import datetime

URL = "http://127.0.0.1:8000/message"
LOG_FILE = "phb_daemon.log"
LAST_STATE_FILE = "phb_last_state.txt"

def log(msg):
    line = f"[{datetime.now()}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def is_alive():
    try:
        r = requests.post(URL, json={"message": "ping"}, timeout=2)
        return r.status_code == 200
    except:
        return False

def state_hash():
    try:
        return subprocess.getoutput("git rev-parse HEAD")
    except:
        return "no-git"

def has_changed():
    current = state_hash()

    if not os.path.exists(LAST_STATE_FILE):
        return True, current

    with open(LAST_STATE_FILE, "r") as f:
        old = f.read().strip()

    return old != current, current

def save_state(state):
    with open(LAST_STATE_FILE, "w") as f:
        f.write(state)

def git_snapshot(reason="auto-repair"):
    log("📦 Creating Git snapshot...")

    try:
        subprocess.call(["git", "add", "."])

        msg = f"PHB auto-repair snapshot: {reason}"

        subprocess.call(["git", "commit", "-m", msg])

        subprocess.call(["git", "push", "origin", "main"])

        log("🚀 GitHub sync complete")

    except Exception as e:
        log(f"❌ Git push failed: {e}")

def restart_server():
    log("🔄 Restarting PHB server...")

    subprocess.call(["pkill", "-f", "uvicorn"])
    time.sleep(2)

    subprocess.Popen(["bash", "phb-api/run.sh"])

    log("🚀 Server restarted")

def run_daemon():
    log("🧠 PHB AUTO-REPAIR + GITHUB DAEMON STARTED")

    last_repair = 0

    while True:
        alive = is_alive()

        if not alive:
            log("❌ System failure detected")

            restart_server()

            # rate limit commits (no spam)
            if time.time() - last_repair > 60:
                git_snapshot("system_recovery")
                last_repair = time.time()

        else:
            log("✔ System healthy")

        time.sleep(10)

if __name__ == "__main__":
    run_daemon()
