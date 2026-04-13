#!/usr/bin/env python3
import json, os, math

RUNTIME = "gcs/runtime"
PROGRAM_PATH = os.path.join(RUNTIME, "mind_program.json")
CURRENT_PATH = os.path.join(RUNTIME, "current_state.json")
EVOLUTION_PATH = os.path.join(RUNTIME, "mind_evolution.json")

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def clamp(x):
    return max(0.0, min(1.0, x))

# Apply symbolic action effects
def apply_action(coords, action):
    name = action["type"]

    if name == "generate_questions":
        coords["curiosity"] = clamp(coords["curiosity"] + 0.05)

    elif name == "list_surprises":
        coords["openness"] = clamp(coords["openness"] + 0.04)

    elif name == "define_problem":
        coords["focus"] = clamp(coords["focus"] + 0.05)

    elif name == "list_constraints":
        coords["rigor"] = clamp(coords["rigor"] + 0.05)

    elif name == "break_down":
        coords["rigor"] = clamp(coords["rigor"] + 0.03)
        coords["focus"] = clamp(coords["focus"] + 0.03)

    elif name == "prototype":
        coords["creativity"] = clamp(coords["creativity"] + 0.05)

    elif name == "generate_variations":
        coords["creativity"] = clamp(coords["creativity"] + 0.04)

    elif name == "combine_concepts":
        coords["creativity"] = clamp(coords["creativity"] + 0.03)
        coords["openness"] = clamp(coords["openness"] + 0.02)

    elif name == "teach_or_explain":
        coords["rigor"] = clamp(coords["rigor"] + 0.04)
        coords["curiosity"] = clamp(coords["curiosity"] + 0.02)

    elif name == "write_summary":
        coords["focus"] = clamp(coords["focus"] + 0.04)

    elif name == "apply_example":
        coords["openness"] = clamp(coords["openness"] + 0.03)

    return coords

# Main interpreter
def run_interpreter():
    program = load_json(PROGRAM_PATH)
    current = load_json(CURRENT_PATH)["coords"]

    evolution = {
        "engine": "PHB MIND-STATE INTERPRETER",
        "start": current.copy(),
        "steps": []
    }

    for phase in program["program"]:
        for action in phase["actions"]:
            # Convert human-readable action to DSL type
            # (Compiler v2 already outputs DSL types in dsl_program)
            # Here we map human actions to DSL types
            if "Generate 3 exploratory questions" in action:
                act = {"type": "generate_questions"}
            elif "List 2 surprising" in action:
                act = {"type": "list_surprises"}
            elif "Define the problem" in action:
                act = {"type": "define_problem"}
            elif "List constraints" in action:
                act = {"type": "list_constraints"}
            elif "Break the task" in action:
                act = {"type": "break_down"}
            elif "Prototype" in action:
                act = {"type": "prototype"}
            elif "Produce 5 variations" in action:
                act = {"type": "generate_variations"}
            elif "Combine two unrelated" in action:
                act = {"type": "combine_concepts"}
            elif "Teach or explain" in action:
                act = {"type": "teach_or_explain"}
            elif "Write a structured summary" in action:
                act = {"type": "write_summary"}
            elif "Apply the idea" in action:
                act = {"type": "apply_example"}
            else:
                continue

            current = apply_action(current, act)
            evolution["steps"].append({
                "action": act["type"],
                "coords": current.copy()
            })

    evolution["end"] = current

    # Save updated current state
    save_json(CURRENT_PATH, {"coords": current})

    # Save evolution log
    save_json(EVOLUTION_PATH, evolution)

    print("[PHB] Interpreter executed. Updated current_state.json and mind_evolution.json.")

if __name__ == "__main__":
    run_interpreter()
