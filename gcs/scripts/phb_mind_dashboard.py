#!/usr/bin/env python3
import json, statistics

STATE_PATH = "gcs/runtime/mind_unified_state.json"

with open(STATE_PATH,"r",encoding="utf-8") as f:
    data = json.load(f)

states = data["state_grid"]

cohs = [s["coherence"] for s in states]
Ik = [s["knowledge_influence"] for s in states]
Ip = [s["practice_influence"] for s in states]
dists = [s["goal_distance"] for s in states]

summary = {
  "coherence": {
    "min": min(cohs),
    "max": max(cohs),
    "mean": statistics.mean(cohs)
  },
  "knowledge_influence": {
    "min": min(Ik),
    "max": max(Ik),
    "mean": statistics.mean(Ik)
  },
  "practice_influence": {
    "min": min(Ip),
    "max": max(Ip),
    "mean": statistics.mean(Ip)
  },
  "goal_distance": {
    "min": min(dists),
    "max": max(dists),
    "mean": statistics.mean(dists)
  }
}

out = {
  "engine": data["engine"],
  "timestamp": data["timestamp"],
  "summary": summary
}

with open("gcs/runtime/mind_dashboard.json","w",encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print("Wrote gcs/runtime/mind_dashboard.json")
