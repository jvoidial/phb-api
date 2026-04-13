#!/usr/bin/env python3
import json, math

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
current_coords = load_current()

# find nearest grid state to current
nearest = min(
    states,
    key=lambda s: dist_state(s["coords"], current_coords, axes)
)

# best state (as before)
best = min(
    states,
    key=lambda s: (-s["coherence"], s["goal_distance"])
)

def coords_of(s): return s["coords"]

cur_c = coords_of(nearest)
best_c = coords_of(best)

print("=== PHB Personal Transition ===")
print("Current (approx) grid state:", cur_c)
print("Best target-like state:", best_c)

STEPS = 10
path = []
for i in range(1, STEPS+1):
    t = i / STEPS
    step_coords = {}
    for k in axes:
        step_coords[k] = round(cur_c[k] + t * (best_c[k] - cur_c[k]), 2)
    d = dist_state(step_coords, target, axes)
    path.append({"step": i, "coords": step_coords, "dist_to_target": d})

out = {
  "current": cur_c,
  "best": best_c,
  "target": target,
  "path": path
}

with open("gcs/runtime/personal_transition.json","w",encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print("Wrote gcs/runtime/personal_transition.json")
