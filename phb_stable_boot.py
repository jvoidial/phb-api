import os
import signal
import subprocess
import time

PORT = 8000
LOCK_FILE = "/tmp/phb_stable.lock"

def kill_existing_uvicorn():
    try:
        output = subprocess.getoutput("ps -A | grep uvicorn | grep -v grep")
        for line in output.splitlines():
            parts = line.split()
            pid = int(parts[0])
            print(f"🔪 Killing old uvicorn PID {pid}")
            os.kill(pid, 9)
    except:
        pass

def free_port():
    try:
        pid = subprocess.getoutput(f"lsof -t -i:{PORT}")
        if pid:
            print(f"🔪 Freeing port {PORT} PID {pid}")
            os.system(f"kill -9 {pid}")
    except:
        pass

def create_lock():
    try:
        if os.path.exists(LOCK_FILE):
            old = open(LOCK_FILE).read().strip()
            try:
                os.kill(int(old), 0)
                print("❌ PHB already running")
                exit()
            except:
                pass

        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))
    except:
        pass

def start_api():
    print("🚀 Starting PHB Stable API...")

    os.system(
        "uvicorn main:app --host 0.0.0.0 --port 8000"
    )

if __name__ == "__main__":
    print("🧠 PHB STABLE CORE BOOT")

    kill_existing_uvicorn()
    free_port()
    create_lock()

    time.sleep(1)

    start_api()
