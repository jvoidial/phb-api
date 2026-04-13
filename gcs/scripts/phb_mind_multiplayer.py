#!/usr/bin/env python3
import json, math

STATE_PATH = "gcs/runtime/mind_unified_state.json"
AGENTS_PATH = "gcs/runtime/agents_config.json"

def load_state():
    with open(STATE_PATH,"r",encoding="utf-8") as f:
        return json.load(f)

def load_agents():
    with open(AGENTS_PATH,"r",encoding="utf-8") as f:
        return json.load(f)["agents"]

def dist_state(a, b, axes):
    s = 0.0
    for k in axes:
        d = a[k] - b[k]
        s += d*d
    return math.sqrt(s / len(axes))

data = load_state()
axes = data["axes"]
target = data["target_state"]
states = data["state_grid"]
agents = load_agents()

# find nearest grid state for each agent
def nearest_state(coords):
    return min(states, key=lambda s: dist_state(s["coords"], coords, axes))

agent_states = []
for ag in agents:
    ns = nearest_state(ag["coords"])
    agent_states.append({
        "id": ag["id"],
        "label": ag["label"],
        "coords": ns["coords"],
        "coherence": ns["coherence"],
        "goal_distance": ns["goal_distance"]
    })

# symbolic interaction: midpoint + amplification toward target
def midpoint(a, b):
    return {k: round((a[k] + b[k]) / 2.0, 2) for k in axes}

mid = midpoint(agent_states[0]["coords"], agent_states[1]["coords"])

def amplify_toward_target(coords, strength=0.2):
    new = {}
    for k in axes:
        delta = target[k] - coords[k]
        new[k] = max(0.0, min(1.0, coords[k] + strength * delta))
    return {k: round(v,2) for k,v in new.items()}

interaction_state = amplify_toward_target(mid, strength=0.25)

out = {
  "engine": "PHB Mind Multiplayer",
  "target": target,
  "agents": agent_states,
  "midpoint_state": mid,
  "interaction_state": interaction_state,
  "note": "Symbolic p2p mind-state interaction; not psychology or neuroscience."
}

with open("gcs/runtime/mind_multiplayer.json","w",encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print("Wrote gcs/runtime/mind_multiplayer.json")
