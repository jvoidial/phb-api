#!/usr/bin/env python3
import json, math

STATE_PATH = "gcs/runtime/mind_unified_state.json"
KNOW_DIR = "gcs/data/mind_nodes"
PRACT_DIR = "gcs/data/practice_nodes"

def load_state():
    with open(STATE_PATH,"r",encoding="utf-8") as f:
        return json.load(f)

def dist_state(a, b, axes):
    s = 0.0
    for k in axes:
        d = a[k] - b[k]
        s += d*d
    return math.sqrt(s / len(axes))

def load_nodes(dirpath):
    import os, glob
    nodes = []
    for path in glob.glob(os.path.join(dirpath, "*.json")):
        try:
            with open(path,"r",encoding="utf-8") as f:
                nodes.append(json.load(f))
        except Exception:
            continue
    return nodes

data = load_state()
axes = data["axes"]
target = data["target_state"]
states = data["state_grid"]

# sort by coherence desc, then goal_distance asc
states_sorted = sorted(
    states,
    key=lambda s: (-s["coherence"], s["goal_distance"])
)

top_states = states_sorted[:20]

print("=== PHB Mind Recommender ===")
print("Top 10 states near target (high coherence, low distance):\n")

for i, s in enumerate(top_states[:10], start=1):
    c = s["coords"]
    print(
        f"#{i} coh={s['coherence']:.3f} dist={s['goal_distance']:.3f} | "
        f"C={c['curiosity']:.2f} F={c['focus']:.2f} "
        f"O={c['openness']:.2f} R={c['rigor']:.2f} Cr={c['creativity']:.2f} "
        f"Ik={s['knowledge_influence']:.3f} Ip={s['practice_influence']:.3f}"
    )

# Recommend practices for the single best state
best = top_states[0]
best_coords = best["coords"]

practice_nodes = load_nodes(PRACT_DIR)

def node_dist_to_state(node, coords):
    return dist_state(node["coords"], coords, axes)

ranked_practices = sorted(
    practice_nodes,
    key=lambda n: node_dist_to_state(n, best_coords)
)

print("\nSuggested practices for BEST state:")
for n in ranked_practices[:5]:
    d = node_dist_to_state(n, best_coords)
    print(f"- {n['meta']['name']} (dist={d:.3f}, tags={','.join(n['meta'].get('tags',[]))})")
