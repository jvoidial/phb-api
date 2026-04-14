import json, os, time

DB="memory.json"

def load():
    return json.load(open(DB)) if os.path.exists(DB) else {}

def save(db):
    json.dump(db, open(DB,"w"), indent=2)

def write(user_id,text):
    db = load()
    db.setdefault(user_id,[])
    db[user_id].append({"text":text,"time":time.time()})
    save(db)

def read(user_id):
    db = load()
    return db.get(user_id,[])
