from fastapi import FastAPI, Request
import json, os

app=FastAPI()

DB="memory.json"

def load():
    return json.load(open(DB)) if os.path.exists(DB) else {}

def save(d):
    json.dump(d, open(DB,"w"), indent=2)

@app.post("/write")
async def write(req:Request):
    d=await req.json()
    db=load()
    db.setdefault(d["user_id"],[])
    db[d["user_id"]].append(d["text"])
    save(db)
    return {"ok":True}

@app.post("/read")
async def read(req:Request):
    d=await req.json()
    db=load()
    return db.get(d["user_id"],[])
