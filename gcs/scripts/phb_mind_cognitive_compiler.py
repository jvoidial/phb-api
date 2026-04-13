#!/usr/bin/env python3
import json

PERSONAL_PATH = "gcs/runtime/personal_transition.json"
RECOMMENDER_PATH = "gcs/runtime/mind_unified_state.json"  # for axes/target reference

def load_personal():
    with open(PERSONAL_PATH,"r",encoding="utf-8") as f:
        return json.load(f)

def load_axes_target():
    with open(RECOMMENDER_PATH,"r",encoding="utf-8") as f:
        d = json.load(f)
        return d["axes"], d["target_state"]

personal = load_personal()
axes, target = load_axes_target()

current = personal["current"]
best = personal["best"]
path = personal["path"]

# simple symbolic compiler:
# - for each step, infer which axes need boosting
# - map axes to generic math/science routines

AXIS_TO_ACTIONS = {
  "curiosity": [
    "Pose 3 new questions about the topic",
    "Scan a new paper or article and extract 5 key ideas"
  ],
  "focus": [
    "Do a 25-minute deep work block on a single problem",
    "Remove distractions and work with a timer"
  ],
  "openness": [
    "Compare 2 different explanations of the same concept",
    "List alternative models or interpretations"
  ],
  "rigor": [
    "Write out all assumptions and check each step of a derivation",
    "Verify results with a second method or source"
  ],
  "creativity": [
    "Generate 3 alternative solution paths",
    "Draw or sketch the concept as a diagram or metaphor"
  ]
}

compiled_steps = []

for step in path:
    coords = step["coords"]
    actions = []
    for axis in axes:
        # if this axis is still below target, suggest actions
        if coords[axis] < target[axis]:
            actions.extend(AXIS_TO_ACTIONS.get(axis, []))
    compiled_steps.append({
        "step": step["step"],
        "coords": coords,
        "dist_to_target": step["dist_to_target"],
        "actions": actions
    })

program = {
  "engine": "PHB Cognitive Compiler",
  "domain_focus": ["mathematics","physics","science reasoning"],
  "current": current,
  "best": best,
  "target": target,
  "compiled_routine": compiled_steps,
  "note": "Symbolic compiler: turns mind-state transitions into math/science study/work routines."
}

with open("gcs/runtime/mind_cognitive_program.json","w",encoding="utf-8") as f:
    json.dump(program, f, indent=2)

print("Wrote gcs/runtime/mind_cognitive_program.json")
