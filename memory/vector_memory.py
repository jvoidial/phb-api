import json, os, math

DB="memory_store.json"

def load():
    return json.load(open(DB)) if os.path.exists(DB) else {}

def save(db):
    json.dump(db, open(DB,"w"), indent=2)

def vec(text):
    return {w:1 for w in text.lower().split()}

def cosine(a,b):
    keys=set(a)|set(b)
    dot=sum(a.get(k,0)*b.get(k,0) for k in keys)
    ma=math.sqrt(sum(v*v for v in a.values()))
    mb=math.sqrt(sum(v*v for v in b.values()))
    return dot/(ma*mb+1e-9)

def add(user,text):
    db=load()
    db.setdefault(user,[])
    db[user].append({"text":text,"vec":vec(text)})
    save(db)

def search(user,q):
    db=load()
    qv=vec(q)
    mems=db.get(user,[])
    scored=[(m,cosine(qv,m["vec"])) for m in mems]
    scored.sort(key=lambda x:x[1],reverse=True)
    return [m[0] for m in scored[:5]]
