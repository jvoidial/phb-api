import os
import signal

LOCK_DIR = os.path.expanduser("~/.phb/locks")
LOCK_FILE = os.path.join(LOCK_DIR, "phb_v23.lock")

def acquire_lock():
    os.makedirs(LOCK_DIR, exist_ok=True)

    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                old_pid = int(f.read().strip())

            os.kill(old_pid, 0)
            print("❌ PHB already running (PID:", old_pid, ")")
            exit(1)

        except:
            print("🧹 Stale lock removed")

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))

def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
