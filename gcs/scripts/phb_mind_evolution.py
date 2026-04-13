#!/usr/bin/env python3
import json, math, random

STATE_PATH = "gcs/runtime/mind_unified_state.json"
CURRENT_PATH = "gcs/runtime/current_state.json"

def load_state():
    with open(STATE_PATH,"r",encoding="utf-8") as f:
        return json.load(f)

def load_current():
    with open(CURRENT_PATH,"r",encoding="utf-8") as f:
        return json.load(f)["coords"]

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

current = load_current()

def step_toward_target(coords, strength=0.1):
    new = {}
    for k in axes:
        delta = target[k] - coords[k]
        new[k] = max(0.0, min(1.0, coords[k] + strength * delta))
    return new

def add_noise(coords, scale=0.05):
    new = {}
    for k in axes:
        new[k] = max(0.0, min(1.0, coords[k] + random.uniform(-scale, scale)))
    return new

timeline = []
steps = 20
coords = current

for t in range(steps):
    # drift toward target + small noise
    coords = step_toward_target(coords, strength=0.15)
    coords = add_noise(coords, scale=0.03)
    d = dist_state(coords, target, axes)
    timeline.append({"t": t, "coords": {k: round(coords[k],2) for k in axes}, "dist_to_target": d})

out = {
  "target": target,
  "start": current,
  "timeline": timeline
}

with open("gcs/runtime/mind_evolution.json","w",encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print("Wrote gcs/runtime/mind_evolution.json")
