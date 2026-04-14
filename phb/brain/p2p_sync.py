import json
import requests
from phb.brain.global_brain import GlobalBrain

BRAIN = GlobalBrain()

PEERS_FILE = "phb/peers/peers.json"

def load_peers():
    try:
        with open(PEERS_FILE) as f:
            return json.load(f)["nodes"]
    except:
        return []

def fetch_peer_state(url):
    try:
        r = requests.get(url + "/brain-state", timeout=3)
        return r.json()
    except:
        return None

def merge_brain(local, remote):
    if not remote:
        return local

    # simple safe merge strategy
    local["memory"].update(remote.get("memory", {}))
    local["timeline"] += remote.get("timeline", [])

    return local

def sync():
    brain = BRAIN.load()
    peers = load_peers()

    for p in peers:
        remote = fetch_peer_state(p)
        brain = merge_brain(brain, remote)

    BRAIN.save(brain)
    return brain
