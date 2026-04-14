import os
import subprocess
import signal
import time

PORT = "8000"

def kill_existing_uvicorn():
    print("🧹 Checking for existing uvicorn...")

    try:
        result = subprocess.getoutput("pgrep -f uvicorn")
        if result.strip():
            pids = result.strip().split("\n")
            for pid in pids:
                print(f"🔪 Killing PID {pid}")
                os.kill(int(pid), signal.SIGKILL)
    except Exception as e:
        print("No existing process found")

def start_api():
    print("🚀 Starting PHB Safe API...")

    cmd = [
        "bash", "-c",
        "cd /data/data/com.termux/files/home/phb-api && "
        "uvicorn main:app --host 0.0.0.0 --port 8000"
    ]

    subprocess.Popen(cmd)

if __name__ == "__main__":
    kill_existing_uvicorn()
    time.sleep(1)
    start_api()
    print("🧠 PHB SAFE API STARTED")
