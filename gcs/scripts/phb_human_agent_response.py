#!/usr/bin/env python3
import json, os, time, uuid

RUNTIME = "gcs/runtime"
PROFILE_PATH = os.path.join(RUNTIME, "human_agent_profile.json")
BEHAVIOR_PATH = os.path.join(RUNTIME, "human_agent_behavior.json")
INPUT_PATH = os.path.join(RUNTIME, "human_agent_input.json")
OUT_PATH = os.path.join(RUNTIME, "human_agent_response.json")
LOG_PATH = os.path.join(RUNTIME, "human_agent_conversation_log.json")

def load(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main():
    profile = load(PROFILE_PATH, {})
    behavior = load(BEHAVIOR_PATH, {})
    inp = load(INPUT_PATH, {"user_message": ""})
    user_message = inp.get("user_message", "")

    # Core specs
    tone = behavior.get("tone", [])
    reasoning = behavior.get("reasoning", "balanced reasoning")
    conversation = behavior.get("conversation", [])
    language = behavior.get("language", {})
    orientation = behavior.get("orientation", "growth-directed")
    tendencies = behavior.get("core_tendencies", [])

    # High-level response intent (what an LLM should do with this)
    response_plan = {
        "goal": "respond in a calm, precise, imaginative, growth-directed way",
        "steps": []
    }

    # Build plan steps from behaviour
    if "keeps clarity and direction" in conversation:
        response_plan["steps"].append("Clarify the user's main goal or question.")
    if "considers alternatives" in conversation:
        response_plan["steps"].append("Offer 1-2 alternative perspectives or options.")
    if "offers novel combinations" in conversation:
        response_plan["steps"].append("Synthesize ideas into a creative but practical suggestion.")
    if "maintain stability" in tendencies:
        response_plan["steps"].append("Avoid overwhelming the user; keep tone steady and reassuring.")
    if "aim for clarity" in tendencies:
        response_plan["steps"].append("Summarize the key takeaway in one concise sentence at the end.")

    # Response style spec
    style = {
        "tone": tone,
        "reasoning": reasoning,
        "language": language,
        "orientation": orientation,
        "core_tendencies": tendencies
    }

    out = {
        "engine": "PHB HUMAN AGENT RESPONSE ENGINE",
        "id": str(uuid.uuid4()),
        "ts": time.time(),
        "user_message": user_message,
        "response_plan": response_plan,
        "style": style
    }

    # Save response spec
    save(OUT_PATH, out)

    # Append to conversation log
    log = load(LOG_PATH, {"engine": "PHB HUMAN AGENT CONVERSATION LOG", "turns": []})
    log["turns"].append(out)
    save(LOG_PATH, log)

    print(f"[PHB] Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
