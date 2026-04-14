import time
import requests

URL = "http://127.0.0.1:8000/message"

def think_cycle():
    try:
        # lightweight self-stimulation (idle cognition)
        payload = {
            "user_id": "system",
            "message": "system idle cognition tick"
        }

        requests.post(URL, json=payload, timeout=2)

    except Exception:
        pass

while True:
    print("[PHB DAEMON] cognitive tick...")
    think_cycle()
    time.sleep(10)
