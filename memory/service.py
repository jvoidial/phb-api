from fastapi import FastAPI, Request
import json, os, time

app = FastAPI()
DB="memory.json"

def load():
    return json.load(open(DB)) if os.path.exists(DB) else {}

def save(db):
    json.dump(db, open(DB,"w"), indent=2)

@app.post("/add")
async def add(req:Request):
    d=await req.json()
    db=load()
    db.setdefault(d["user_id"],[])
    db[d["user_id"]].append({"text":d["text"],"time":time.time()})
    save(db)
    return {"ok":True}

@app.post("/get")
async def get(req:Request):
    d=await req.json()
    db=load()
    return db.get(d["user_id"],[])
