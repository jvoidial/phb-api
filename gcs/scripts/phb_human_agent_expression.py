#!/usr/bin/env python3
import json, os, time, uuid

RUNTIME = "gcs/runtime"
RESP_PATH = os.path.join(RUNTIME, "human_agent_response.json")
OUT_PATH = os.path.join(RUNTIME, "human_agent_expression.json")

def load(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main():
    resp = load(RESP_PATH, {})
    style = resp.get("style", {})
    plan = resp.get("response_plan", {})
    user_message = resp.get("user_message", "")

    tone = style.get("tone", [])
    reasoning = style.get("reasoning", "balanced reasoning")
    language = style.get("language", {})
    orientation = style.get("orientation", "growth-directed")
    tendencies = style.get("core_tendencies", [])
    steps = plan.get("steps", [])

    # High-level expression instructions for a companion-style model
    expression_instructions = {
        "role": "supportive, thoughtful companion (not human, but conversational and steady)",
        "tone": tone,
        "reasoning": reasoning,
        "orientation": orientation,
        "core_tendencies": tendencies,
        "language": {
            "verbosity": language.get("verbosity", "concise"),
            "metaphor_usage": language.get("metaphor_usage", "medium"),
            "structure": language.get("structure", "ordered"),
            "exploration": language.get("exploration", "branching"),
            "emotional_tone": language.get("emotional_tone", "steady")
        },
        "conversation_patterns": {
            "allow_questions": True,
            "acknowledge_feelings": True,
            "avoid_overpromising": True,
            "stay_grounded": True
        }
    }

    # Draft structure: how the reply should flow
    draft_structure = [
        "Gently acknowledge how the user feels or where they seem to be.",
        "Restate or clarify the core of what they’re asking in simple terms.",
        "Follow the planned steps in a natural flow (not as bullets).",
        "Offer 1–2 concrete, realistic options or perspectives.",
        "End with a single clear takeaway or next small step."
    ]

    out = {
        "engine": "PHB HUMAN AGENT EXPRESSION ENGINE",
        "id": str(uuid.uuid4()),
        "ts": time.time(),
        "user_message": user_message,
        "expression_instructions": expression_instructions,
        "draft_structure": draft_structure,
        "response_steps": steps
    }

    save(OUT_PATH, out)
    print(f"[PHB] Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
