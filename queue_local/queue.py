import json, os, time

Q_FILE="queue.json"

def load():
    return json.load(open(Q_FILE)) if os.path.exists(Q_FILE) else []

def save(q):
    json.dump(q, open(Q_FILE,"w"), indent=2)

def push(job):
    q = load()
    job["status"]="queued"
    job["time"]=time.time()
    q.append(job)
    save(q)

def pop():
    q = load()
    for j in q:
        if j["status"]=="queued":
            j["status"]="processing"
            save(q)
            return j
    return None
