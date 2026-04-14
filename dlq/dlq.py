import json, os

FILE="dlq.json"

def load():
    return json.load(open(FILE)) if os.path.exists(FILE) else []

def save(d):
    json.dump(d, open(FILE,"w"), indent=2)

def add(job):
    d=load()
    d.append(job)
    save(d)
