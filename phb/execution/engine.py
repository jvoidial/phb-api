
from datetime import datetime, timezone

EXECUTION_QUEUE = {
    "pending": [],
    "active": [],
    "completed": []
}

def add_task(plan):
    EXECUTION_QUEUE["pending"].append(plan)

def next_task():
    if EXECUTION_QUEUE["pending"]:
        task = EXECUTION_QUEUE["pending"].pop(0)
        EXECUTION_QUEUE["active"].append(task)
        return task
    return None

def complete_task(task):
    EXECUTION_QUEUE["active"].remove(task)
    task["status"] = "done"
    task["completed_at"] = datetime.now(timezone.utc).isoformat()
    EXECUTION_QUEUE["completed"].append(task)

def get_state():
    return EXECUTION_QUEUE
