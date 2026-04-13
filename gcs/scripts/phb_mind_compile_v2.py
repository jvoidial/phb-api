#!/usr/bin/env python3
import json, os

RUNTIME = "gcs/runtime"
REC_PATH = os.path.join(RUNTIME, "mind_recommendations.json")
OUT_PATH = os.path.join(RUNTIME, "mind_program.json")

def load_recommendations():
    if not os.path.exists(REC_PATH):
        raise SystemExit("[PHB] mind_recommendations.json not found. Run recommender JSON script first.")
    with open(REC_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

rec = load_recommendations()
best = rec["best_state"]
best_c = best["coords"]
practices = rec["recommended_practices"]

def state_signature(c):
    return f"C{c['curiosity']}-F{c['focus']}-O{c['openness']}-R{c['rigor']}-Cr{c['creativity']}"

sig = state_signature(best_c)

# Map practices into simple labels
practice_labels = [p["meta"]["name"] for p in practices]

program = [
    {
        "phase": "Activation",
        "focus": "Ignite curiosity + openness",
        "actions": [
            f"Engage in {practice_labels[0]} (if available)",
            "Generate 3 exploratory questions about the current problem",
            "List 2 surprising or non-obvious angles"
        ]
    },
    {
        "phase": "Stabilization",
        "focus": "Increase focus + rigor",
        "actions": [
            "Define the problem in one precise sentence",
            "List constraints, assumptions, and success criteria",
            "Break the task into 3–5 atomic steps"
        ]
    },
    {
        "phase": "Expansion",
        "focus": "Boost creativity",
        "actions": [
            f"Prototype or sketch using {practice_labels[1]} (if relevant)",
            "Produce 5 variations or alternative solutions",
            "Combine two unrelated ideas into a new approach"
        ]
    },
    {
        "phase": "Integration",
        "focus": "Merge knowledge + practice",
        "actions": [
            f"Teach or explain using {practice_labels[0]} or {practice_labels[2]}",
            "Write a structured summary of what you learned",
            "Apply the idea to one concrete real-world example"
        ]
    }
]

# Human-readable routine
human_script_lines = []
human_script_lines.append(f"PHB Mind Program – State {sig}")
human_script_lines.append("")
for i, phase in enumerate(program, start=1):
    human_script_lines.append(f"Phase {i}: {phase['phase']} – {phase['focus']}")
    for j, act in enumerate(phase["actions"], start=1):
        human_script_lines.append(f"  {i}.{j} {act}")
    human_script_lines.append("")
human_script = "\n".join(human_script_lines)

# Tiny DSL
dsl_lines = []
dsl_lines.append(f"STATE {sig}")
dsl_lines.append("PHASE Activation USE curiosity,openness")
dsl_lines.append("  ACT generate_questions count=3")
dsl_lines.append("  ACT list_surprises count=2")
dsl_lines.append("PHASE Stabilization USE focus,rigor")
dsl_lines.append("  ACT define_problem")
dsl_lines.append("  ACT list_constraints")
dsl_lines.append("  ACT break_down steps=3-5")
dsl_lines.append("PHASE Expansion USE creativity")
dsl_lines.append("  ACT prototype")
dsl_lines.append("  ACT generate_variations count=5")
dsl_lines.append("  ACT combine_concepts")
dsl_lines.append("PHASE Integration USE knowledge,practice")
dsl_lines.append("  ACT teach_or_explain")
dsl_lines.append("  ACT write_summary")
dsl_lines.append("  ACT apply_example")
dsl_script = "\n".join(dsl_lines)

out = {
    "engine": "PHB MIND-STATE COMPILER v2",
    "state_signature": sig,
    "best_state": best_c,
    "recommended_practices": practice_labels,
    "program": program,
    "human_routine": human_script,
    "dsl_program": dsl_script
}

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print(f"[PHB] Wrote {OUT_PATH}")
