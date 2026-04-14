from event_engine.engine import emit
from result_store import write

def handle(message,user_id):

    emit({
        "message":message,
        "user_id":user_id
    })

    return {
        "status":"queued",
        "mode":"PHB_V16_AUTONOMOUS_OS"
    }
