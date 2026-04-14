from fastapi import FastAPI
from phb.core.event_bus import EventBus
from phb.core.plugins import PluginManager
from phb.core.memory import Memory

app = FastAPI()

bus = EventBus()
plugins = PluginManager()
memory = Memory()

plugins.load()


@app.get("/")
def home():
    return {
        "status": "PHB UNIFIED OS v3",
        "kernel": "single_control_plane"
    }


@app.post("/message")
def message(data: dict):
    user = data.get("user_id", "anon")
    msg = data.get("message", "")

    memory.save(user, msg)

    bus.emit("message", {"user": user, "msg": msg})

    plugin = plugins.run(msg)
    if plugin:
        return {
            "input": msg,
            "response": plugin,
            "mode": "PLUGIN_LAYER"
        }

    return {
        "input": msg,
        "response": f"PHB unified processed: {msg}",
        "mode": "CORE"
    }
