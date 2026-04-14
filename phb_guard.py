import os
import psutil

LOCK_FILE = "/tmp/phb_v21.lock"

def acquire_lock():
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "r") as f:
            pid = int(f.read().strip())

        # kill stale process if exists
        if psutil.pid_exists(pid):
            os.system(f"kill -9 {pid}")

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))


def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
