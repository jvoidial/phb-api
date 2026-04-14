from event_store.store import emit
from plugins.loader import load_plugins

plugins = load_plugins()

def handle(message,user_id):

    event = {
        "type":"message",
        "message":message,
        "user_id":user_id
    }

    emit(event)

    results = []
    for p in plugins:
        if hasattr(p,"run"):
            results.append(p.run(event))

    return {
        "input":message,
        "plugins":results,
        "mode":"PHB_v13_CONTROL_PLANE"
    }
