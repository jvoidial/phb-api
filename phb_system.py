import os
import time
import uuid
import requests

API_URL = os.getenv("PHB_API_URL", "http://localhost:8000")
API_KEY = os.getenv("PHB_API_KEY", "my-phb-master-key")

def phb_companion(message: str) -> dict:
    r = requests.post(
        f"{API_URL}/v1/companion",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        json={"message": message},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()

def phb_engine(input_text: str, mode: str = "robot") -> dict:
    r = requests.post(
        f"{API_URL}/v1/engine",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        json={"input": input_text, "mode": mode},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()

# --- Robot adapter stub ---

def robot_apply_action(action: str):
    # Placeholder: wire this to real hardware later
    print(f"[ROBOT] would execute: {action}")

# --- Multi-agent loop ---

def agent_loop(initial_message: str, steps: int = 5, delay: float = 1.0):
    state = {"last_message": initial_message}
    for i in range(steps):
        print(f"\n[STEP {i+1}]")
        # Companion reflects on state
        msg = f"State: {state}. Respond briefly."
        comp = phb_companion(msg)
        reply_text = comp["reply"]["text"]
        print(f"[COMPANION] {reply_text}")

        # Engine interprets reply as an action command
        eng = phb_engine(reply_text, mode="robot")
        intent = eng["result"]["intent"]
        action = eng["result"]["action"]
        conf = eng["result"]["confidence"]
        print(f"[ENGINE] intent={intent} action={action} conf={conf}")

        # Robot adapter
        robot_apply_action(action)

        # Update state
        state = {
            "last_message": reply_text,
            "last_intent": intent,
            "last_action": action,
            "step": i + 1,
        }
        time.sleep(delay)

# --- P2P-style node shell (local only for now) ---

def run_node(node_id: str | None = None):
    node_id = node_id or str(uuid.uuid4())
    print(f"[PHB NODE] starting node {node_id}")
    print("[PHB NODE] type 'quit' to exit")
    while True:
        try:
            line = input("node> ").strip()
        except EOFError:
            break
        if line.lower() in ("quit", "exit"):
            break
        if not line:
            continue
        # For now: treat as engine command
        eng = phb_engine(line, mode="robot")
        print(eng)

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == "loop":
        msg = sys.argv[2] if len(sys.argv) >= 3 else "begin"
        agent_loop(msg, steps=5, delay=1.0)
    elif len(sys.argv) >= 2 and sys.argv[1] == "node":
        run_node()
    else:
        print("Usage:")
        print("  python3 phb_system.py loop \"start message\"")
        print("  python3 phb_system.py node")
