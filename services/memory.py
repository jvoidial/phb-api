from fastapi import FastAPI, Request
import json, os, time

app = FastAPI()

DB="memory_store.json"

def load():
    return json.load(open(DB)) if os.path.exists(DB) else {}

def save(db):
    json.dump(db, open(DB,"w"), indent=2)

@app.post("/event")
async def event(req:Request):
    e=await req.json()

    if e["type"] == "memory_add":
        db=load()
        db.setdefault(e["user_id"],[])
        db[e["user_id"]].append({"text":e["text"],"time":time.time()})
        save(db)
        return {"ok":True}

    if e["type"] == "memory_get":
        db=load()
        return db.get(e["user_id"],[])

    return {"ignored":True}
