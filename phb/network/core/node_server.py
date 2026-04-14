from fastapi import FastAPI
import time

app = FastAPI()

NODE_ID = "local-node"
NODE_MEMORY = {}
LAST_HEARTBEAT = time.time()

@app.get("/health")
def health():
    return {
        "node": NODE_ID,
        "status": "alive",
        "time": time.time()
    }

@app.post("/heartbeat")
def heartbeat():
    global LAST_HEARTBEAT
    LAST_HEARTBEAT = time.time()
    return {"ok": True}

@app.post("/task")
def run_task(data: dict):
    msg = data.get("msg", "")

    # simple processing
    result = msg.upper()

    return {
        "node": NODE_ID,
        "input": msg,
        "output": result
    }
