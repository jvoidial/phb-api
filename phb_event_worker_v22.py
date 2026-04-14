import time
import queue
import threading

EVENT_QUEUE = queue.Queue()

def push(event):
    EVENT_QUEUE.put(event)

def worker_loop(handler):
    while True:
        event = EVENT_QUEUE.get()

        try:
            handler(event)
        except Exception as e:
            print("❌ Event failed:", e)
            # retry once
            EVENT_QUEUE.put(event)

        time.sleep(0.01)

def start_worker(handler):
    t = threading.Thread(target=worker_loop, args=(handler,), daemon=True)
    t.start()
