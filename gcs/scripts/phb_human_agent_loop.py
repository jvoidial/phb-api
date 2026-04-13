#!/usr/bin/env python3
import json, os, time, uuid, subprocess

RUNTIME = "gcs/runtime"
SESSION_PATH = os.path.join(RUNTIME, "human_agent_session.json")

def load(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def main():
    # 1) Advance mind engine: execute + evolve + dashboard + profiles
    run("python3 gcs/runtime/phb_mind_api.py mind/execute")
    run("python3 gcs/runtime/phb_mind_api.py mind/evolve")
    run("python3 gcs/runtime/phb_mind_api.py mind/dashboard_v2")
    run("python3 gcs/runtime/phb_mind_api.py mind/human_agent")
    run("python3 gcs/runtime/phb_mind_api.py mind/human_agent_behavior")

    # 2) Load latest state
    dashboard = load(os.path.join(RUNTIME, "mind_dashboard_v2.json"), {})
    profile = load(os.path.join(RUNTIME, "human_agent_profile.json"), {})
    behavior = load(os.path.join(RUNTIME, "human_agent_behavior.json"), {})

    # 3) Append to session log
    session = load(SESSION_PATH, {"engine": "PHB HUMAN AGENT LOOP", "ticks": []})
    tick = {
        "id": str(uuid.uuid4()),
        "ts": time.time(),
        "dashboard": dashboard,
        "profile": profile,
        "behavior": behavior
    }
    session["ticks"].append(tick)
    save(SESSION_PATH, session)

    # 4) Return current snapshot
    out = {
        "engine": "PHB HUMAN AGENT LOOP",
        "dashboard": dashboard,
        "profile": profile,
        "behavior": behavior,
        "session_ticks": len(session["ticks"])
    }
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
