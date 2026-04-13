#!/usr/bin/env python3
import json, math

STATE_PATH = "gcs/runtime/mind_unified_state.json"

def load_state():
    with open(STATE_PATH,"r",encoding="utf-8") as f:
        return json.load(f)

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

# pick a "current" state: lowest coherence, farthest from target
states_sorted_worst = sorted(
    states,
    key=lambda s: (s["coherence"], -s["goal_distance"])
)
current = states_sorted_worst[0]

# best state: highest coherence, closest to target
states_sorted_best = sorted(
    states,
    key=lambda s: (-s["coherence"], s["goal_distance"])
)
best = states_sorted_best[0]

def coords_of(s): return s["coords"]

cur_c = coords_of(current)
best_c = coords_of(best)

print("=== PHB Mind Transition Planner ===")
print("Current (symbolic) state:")
print(f"  coh={current['coherence']:.3f} dist={current['goal_distance']:.3f} coords={cur_c}")
print("\nTarget-like best state:")
print(f"  coh={best['coherence']:.3f} dist={best['goal_distance']:.3f} coords={best_c}")

# simple linear path in 5D space
STEPS = 10
print("\nProposed 10-step path in mind-space (symbolic):")
for i in range(1, STEPS+1):
    t = i / STEPS
    step_coords = {}
    for k in axes:
        step_coords[k] = round(cur_c[k] + t * (best_c[k] - cur_c[k]), 2)
    d = dist_state(step_coords, target, axes)
    print(f"step {i:2d}: coords={step_coords}, dist_to_target={d:.3f}")
