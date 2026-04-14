import json, os, time, math
from collections import Counter

DB_PATH = "phb_memory.json"


def _load():
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH,"r") as f:
        return json.load(f)


def _save(db):
    with open(DB_PATH,"w") as f:
        json.dump(db,f,indent=2)


def _vec(text):
    return Counter(text.lower().split())


def _cos(a,b):
    keys = set(a)|set(b)
    dot = sum(a.get(k,0)*b.get(k,0) for k in keys)
    ma = math.sqrt(sum(v*v for v in a.values()))
    mb = math.sqrt(sum(v*v for v in b.values()))
    if ma==0 or mb==0:
        return 0
    return dot/(ma*mb)


def add_memory(user_id,text,mood="neutral"):
    db=_load()
    db.setdefault(user_id,[])

    db[user_id].append({
        "text":text,
        "mood":mood,
        "time":time.time(),
        "weight":1.0,
        "vector":_vec(text)
    })

    _save(db)
    return db[user_id][-1]


def search_memory(user_id,query,top_k=5):
    db=_load()
    mem=db.get(user_id,[])

    q=_vec(query)
    out=[]

    for m in mem:
        score=_cos(q,m.get("vector",{}))*m.get("weight",1.0)
        out.append({**m,"score":score})

    out.sort(key=lambda x:x["score"],reverse=True)
    return out[:top_k]


def reinforce(user_id,text):
    db=_load()
    for m in db.get(user_id,[]):
        if text.lower() in m["text"].lower():
            m["weight"]=m.get("weight",1.0)+0.1
    _save(db)


def decay():
    db=_load()
    for u in db:
        for m in db[u]:
            m["weight"]=max(0.1,m.get("weight",1.0)*0.999)
    _save(db)
