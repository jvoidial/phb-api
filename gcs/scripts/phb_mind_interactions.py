#!/usr/bin/env python3
import json

STATE_PATH = "gcs/runtime/mind_unified_state.json"

with open(STATE_PATH,"r",encoding="utf-8") as f:
    data = json.load(f)

states = data["state_grid"]

# focus on states where both knowledge and practice influence are strong
filtered = [s for s in states if s["knowledge_influence"] > 0.5 and s["practice_influence"] > 0.5]
filtered_sorted = sorted(filtered, key=lambda s: (-s["coherence"], s["goal_distance"]))

print("=== PHB Mind Interaction Inspector ===")
print("Top 20 states where knowledge + practice both strongly contribute:\n")

for s in filtered_sorted[:20]:
    c = s["coords"]
    print(
        f"coh={s['coherence']:.3f} dist={s['goal_distance']:.3f} | "
        f"C={c['curiosity']:.2f} F={c['focus']:.2f} "
        f"O={c['openness']:.2f} R={c['rigor']:.2f} Cr={c['creativity']:.2f} "
        f"Ik={s['knowledge_influence']:.3f} Ip={s['practice_influence']:.3f}"
    )
