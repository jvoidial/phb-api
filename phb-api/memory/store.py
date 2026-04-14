import json, os, time

DB = "phb_memory.json"

def load():
    if not os.path.exists(DB):
        return {}
    try:
        return json.load(open(DB))
    except:
        return {}

def save(db):
    json.dump(db, open(DB,"w"), indent=2)

def add(user_id, text, mood):
    db = load()
    db.setdefault(user_id, [])

    db[user_id].append({
        "text": text,
        "mood": mood,
        "time": time.time()
    })

    save(db)

def get(user_id):
    db = load()
    return db.get(user_id, [])
