import threading
import time

running = False

def loop():
    while True:
        print("[PHB OS] autonomous cycle running...")
        time.sleep(60)

def start_supervisor():
    global running
    if running:
        return

    running = True
    t = threading.Thread(target=loop, daemon=True)
    t.start()
