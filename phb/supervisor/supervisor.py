import time
import os

SERVICES=["8000","8001","8002"]

while True:
    print("[SUPERVISOR] health check...")

    for port in SERVICES:
        if os.system(f"curl -s http://127.0.0.1:{port} > /dev/null") != 0:
            print(f"[SUPERVISOR] service {port} down -> restart trigger")

    time.sleep(10)
