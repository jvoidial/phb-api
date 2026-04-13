#!/usr/bin/env python3
import json

with open("gcs/runtime/mind_unified_state.json","r",encoding="utf-8") as f:
    data = json.load(f)

states = data["state_grid"]

# sort by coherence descending, then by goal_distance ascending
states_sorted = sorted(
    states,
    key=lambda s: (-s["coherence"], s["goal_distance"])
)

print("Top 20 unified mind states (high coherence, close to target):")
for s in states_sorted[:20]:
    c = s["coords"]
    print(
        f"coh={s['coherence']:.3f} dist={s['goal_distance']:.3f} | "
        f"C={c['curiosity']:.2f} F={c['focus']:.2f} "
        f"O={c['openness']:.2f} R={c['rigor']:.2f} Cr={c['creativity']:.2f} "
        f"Ik={s['knowledge_influence']:.3f} Ip={s['practice_influence']:.3f}"
    )
