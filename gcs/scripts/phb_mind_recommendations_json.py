#!/usr/bin/env python3
import json, math, os

STATE_PATH = "gcs/runtime/mind_unified_state.json"
PRACT_DIR = "gcs/data/practice_nodes"
OUT_PATH = "gcs/runtime/mind_recommendations.json"

def load_state():
    with open(STATE_PATH,"r",encoding="utf-8") as f:
        return json.load(f)

def load_nodes(dirpath):
    import glob
    nodes = []
    for path in glob.glob(os.path.join(dirpath, "*.json")):
        try:
            with open(path,"r",encoding="utf-8") as f:
                nodes.append(json.load(f))
        except:
            continue
    return nodes

def dist_state(a, b, axes):
    s = 0.0
    for k in axes:
        d = a[k] - b[k]
        s += d*d
    return math.sqrt(s / len(axes))

data = load_state()
axes = data["axes"]
states = data["state_grid"]

# sort by coherence desc, then goal_distance asc
states_sorted = sorted(
    states,
    key=lambda s: (-s["coherence"], s["goal_distance"])
)

top_states = states_sorted[:10]
best = top_states[0]
best_coords = best["coords"]

practice_nodes = load_nodes(PRACT_DIR)

ranked_practices = sorted(
    practice_nodes,
    key=lambda n: dist_state(n["coords"], best_coords, axes)
)

out = {
    "engine": "PHB MIND RECOMMENDER",
    "top_states": top_states,
    "best_state": best,
    "recommended_practices": ranked_practices[:5]
}

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print(f"[PHB] Wrote {OUT_PATH}")
