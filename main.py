from fastapi import FastAPI

app = FastAPI()

MEMORY = {}

@app.get("/")
def home():
    return {"status": "PHB v2.1 ONLINE"}

@app.post("/message")
def message(data: dict):
    user = data.get("user_id", "anon")
    msg = data.get("message", "")

    if user not in MEMORY:
        MEMORY[user] = []

    MEMORY[user].append(msg)

    return {
        "input": msg,
        "response": f"PHB v2.1 received: {msg}",
        "memory_size": len(MEMORY[user]),
        "kernel": "singleton_safe"
    }
