import os
import time
import signal
import uvicorn

PORT = 8000

# -------------------------
# SAFE LOCK PATH (ANDROID)
# -------------------------
BASE_DIR = os.path.expanduser("~/.phb")
os.makedirs(BASE_DIR, exist_ok=True)

LOCK_FILE = os.path.join(BASE_DIR, "phb_v21.lock")


# -------------------------
# KILL OLD PROCESSES
# -------------------------
def kill_uvicorn():
    print("🧹 Killing uvicorn processes...")
    os.system("pkill -f uvicorn >/dev/null 2>&1")


def free_port():
    print("🔓 Freeing port...")
    os.system("fuser -k 8000/tcp >/dev/null 2>&1")


# -------------------------
# SINGLETON LOCK (SAFE)
# -------------------------
def acquire_lock():
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                old_pid = int(f.read().strip())

            # check if process exists
            os.kill(old_pid, 0)
            print("⚠️ Old kernel found → killing it")
            os.kill(old_pid, signal.SIGKILL)

        except:
            pass

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))


def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)


# -------------------------
# START SERVER
# -------------------------
def start_api():
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)


# -------------------------
# BOOT SEQUENCE
# -------------------------
if __name__ == "__main__":
    print("🧠 PHB v2.1 SINGLETON KERNEL BOOT")

    acquire_lock()
    kill_uvicorn()
    free_port()

    time.sleep(1)

    print("🚀 Starting API...")
    start_api()
