import json
import time
from tool_router import run_tool

MEM_FILE = "memory.json"

def load_memory():
    try:
        with open(MEM_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(mem):
    with open(MEM_FILE, "w") as f:
        json.dump(mem, f, indent=2)

# -------------------
# MEMORY SYSTEM
# -------------------
def run_cognition(user_id: str, message: str):
    mem = load_memory()

    if user_id not in mem:
        mem[user_id] = {"messages": []}

    mem[user_id]["messages"].append({
        "text": message,
        "time": time.time()
    })

    response = process_message(message)

    save_memory(mem)

    return {
        "input": message,
        "response": response["response"],
        "tool_used": response.get("tool"),
        "mode": "PHB_V20_EVENT_KERNEL"
    }

# -------------------
# TOOL ROUTING LOGIC
# -------------------
def process_message(message):
    msg = message.lower()

    # TOOL TRIGGERS
    if msg.startswith("time"):
        return {
            "response": run_tool("time", ""),
            "tool": "time"
        }

    if msg.startswith("calc"):
        expr = message.replace("calc", "").strip()
        return {
            "response": run_tool("calc", expr),
            "tool": "calc"
        }

    if msg.startswith("analyze"):
        text = message.replace("analyze", "").strip()
        return {
            "response": run_tool("analyze", text),
            "tool": "analyze"
        }

    # DEFAULT AI BEHAVIOR
    return {
        "response": "PHB v19 received your message safely.",
        "tool": None
    }
