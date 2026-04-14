import subprocess, time

print("[PHB SUPERVISOR v7.1] ONLINE")

def start():
    return subprocess.Popen(
        "uvicorn main:app --host 0.0.0.0 --port 8000",
        shell=True
    )

api = start()

while True:
    time.sleep(5)

    if api.poll() is not None:
        print("[SUPERVISOR] restart")
        api = start()
