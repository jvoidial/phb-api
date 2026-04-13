#!/usr/bin/env python3
import json, os, statistics

RUNTIME = "gcs/runtime"

def load(path):
    with open(os.path.join(RUNTIME, path), "r", encoding="utf-8") as f:
        return json.load(f)

def safe_load(path, default=None):
    full = os.path.join(RUNTIME, path)
    if not os.path.exists(full):
        return default
    with open(full, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    state = load("mind_unified_state.json")
    current = safe_load("current_state.json", {"coords": state["target_state"]})
    evo3 = safe_load("mind_evolution_v3.json")
    exec_res = safe_load("mind_execute.json")
    dashboard = {}

    axes = state["axes"]
    dashboard["engine"] = "PHB MIND DASHBOARD v2"
    dashboard["axes"] = axes
    dashboard["target"] = state["target_state"]
    dashboard["current"] = current["coords"]

    # evolution v3 summary
    if evo3:
        tl = evo3["timeline"]
        dists = [p["dist_to_target"] for p in tl]
        cohs = [p["coherence"] for p in tl]
        dashboard["evolution_v3"] = {
            "start": evo3["start"],
            "end": evo3["end"],
            "steps": len(tl),
            "dist_min": min(dists),
            "dist_max": max(dists),
            "dist_last": dists[-1],
            "coherence_min": min(cohs),
            "coherence_max": max(cohs),
            "coherence_last": cohs[-1]
        }

    # executor summary
    if exec_res:
        dashboard["last_execute"] = {
            "program_signature": exec_res["program_signature"],
            "start_state": exec_res["start_state"],
            "end_state": exec_res["end_state"],
            "phases_completed": exec_res["phases_completed"],
            "actions_run": exec_res["actions_run"]
        }

    # agent summary (from evo3)
    if evo3 and "agents" in evo3:
        agents_summary = []
        for ag in evo3["agents"]:
            agents_summary.append({
                "id": ag["id"],
                "label": ag.get("label"),
                "start": ag["start"],
                "end": ag["end"],
                "steps": len(ag["timeline"])
            })
        dashboard["agents"] = agents_summary

    with open(os.path.join(RUNTIME, "mind_dashboard_v2.json"), "w", encoding="utf-8") as f:
        json.dump(dashboard, f, indent=2)

    print("[PHB] Wrote gcs/runtime/mind_dashboard_v2.json")

if __name__ == "__main__":
    main()
