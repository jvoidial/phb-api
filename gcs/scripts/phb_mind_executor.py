#!/usr/bin/env python3
import json, os, subprocess

RUNTIME = "gcs/runtime"

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def execute():
    # 1. Run recommender (JSON version)
    run("python3 gcs/scripts/phb_mind_recommendations_json.py")

    # 2. Compile mind program
    run("python3 gcs/scripts/phb_mind_compile_v2.py")

    # 3. Load state before execution
    start = load(os.path.join(RUNTIME, "current_state.json"))["coords"]

    # 4. Run interpreter
    run("python3 gcs/scripts/phb_mind_interpreter.py")

    # 5. Load updated state + evolution
    end = load(os.path.join(RUNTIME, "current_state.json"))["coords"]
    evo = load(os.path.join(RUNTIME, "mind_evolution.json"))
    prog = load(os.path.join(RUNTIME, "mind_program.json"))

    # 6. Unified response
    out = {
        "engine": "PHB MIND EXECUTOR",
        "program_signature": prog["state_signature"],
        "start_state": start,
        "end_state": end,
        "phases_completed": len(prog["program"]),
        "actions_run": [step["action"] for step in evo["steps"]],
        "steps": evo["steps"]
    }

    save(os.path.join(RUNTIME, "mind_execute.json"), out)
    print("[PHB] Executor complete. Wrote mind_execute.json")

if __name__ == "__main__":
    execute()
