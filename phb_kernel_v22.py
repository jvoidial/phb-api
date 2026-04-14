import time
from phb_memory_v22 import write
from phb_event_worker_v22 import push, start_worker

SYSTEM_MODE = "PHB_V22_DISTRIBUTED_EVENT_OS"

# -------------------------
# TOOL SAFE LAYER
# -------------------------
def tool_exec(tool, data):
    if tool == "time":
        return time.ctime()

    if tool == "calc":
        try:
            return str(eval(data, {"__builtins__": {}}))
        except:
            return "error"

    if tool == "analyze":
        return {
            "chars": len(str(data)),
            "type": str(type(data))
        }

    return "unknown"

# -------------------------
# EVENT HANDLER
# -------------------------
def handle_event(event):
    data = event["data"]

    user = data["user_id"]
    msg = data["message"]

    if msg.startswith("time"):
        response = tool_exec("time", None)
    elif msg.startswith("calc"):
        response = tool_exec("calc", msg.replace("calc", "").strip())
    elif msg.startswith("analyze"):
        response = tool_exec("analyze", msg)
    else:
        response = f"PHB v22 processed: {msg}"

    write(user, msg, response)

    print("🧠 EVENT PROCESSED:", response)

# -------------------------
# START KERNEL
# -------------------------
def start_kernel():
    print("🧠 PHB v22 KERNEL STARTING...")

    start_worker(handle_event)

    print("🟢 EVENT WORKER ACTIVE")
    print("🧠 MEMORY PERSISTENCE ACTIVE")

    while True:
        time.sleep(10)
