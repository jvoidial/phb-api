import json
import os
import time

DB_FILE = "phb_memory_v22.json"

def load_memory():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def write(user_id, msg, response):
    db = load_memory()

    if user_id not in db:
        db[user_id] = []

    db[user_id].append({
        "input": msg,
        "output": response,
        "ts": time.time()
    })

    save_memory(db)

def read(user_id):
    db = load_memory()
    return db.get(user_id, [])
