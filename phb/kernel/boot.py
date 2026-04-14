import os
import time
import signal
import uvicorn

PORT = 8000

BASE = os.path.expanduser("~/.phb")
os.makedirs(BASE, exist_ok=True)

LOCK = os.path.join(BASE, "lock.pid")


# -------------------------
# SINGLE INSTANCE LOCK
# -------------------------
def acquire_lock():
    if os.path.exists(LOCK):
        try:
            pid = int(open(LOCK).read())
            os.kill(pid, 0)
            os.kill(pid, signal.SIGKILL)
        except:
            pass

    with open(LOCK, "w") as f:
        f.write(str(os.getpid()))


# -------------------------
# CLEAN START
# -------------------------
def cleanup():
    os.system("pkill -f uvicorn >/dev/null 2>&1")
    os.system("fuser -k 8000/tcp >/dev/null 2>&1")


# -------------------------
# START API
# -------------------------
def start():
    uvicorn.run("phb.main:app", host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    print("🧠 PHB UNIFIED OS BOOT")

    acquire_lock()
    cleanup()

    time.sleep(1)

    print("🚀 Starting kernel...")
    start()
