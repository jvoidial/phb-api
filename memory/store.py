import json, os, time

DB="memory_store.json"

def load():
    return json.load(open(DB)) if os.path.exists(DB) else {}

def save(db):
    json.dump(db, open(DB,"w"), indent=2)

def add(user,text):
    db=load()
    db.setdefault(user,[])
    db[user].append({"text":text,"time":time.time()})
    save(db)

def get(user):
    db=load()
    return db.get(user,[])
