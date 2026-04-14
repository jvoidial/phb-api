import os, time, subprocess, signal

API_CMD = "uvicorn main:app --host 0.0.0.0 --port 8000"

def start_api():
    return subprocess.Popen(API_CMD, shell=True)

def memory_tick():
    # placeholder for future GC / decay
    pass

def run_forever():
    print("[PHB SUPERVISOR] ONLINE")

    api = start_api()

    while True:
        try:
            # health check
            if api.poll() is not None:
                print("[SUPERVISOR] API crashed → restarting")
                api = start_api()

            memory_tick()
            time.sleep(5)

        except Exception as e:
            print("[SUPERVISOR ERROR]", e)
            time.sleep(2)

if __name__ == "__main__":
    run_forever()
