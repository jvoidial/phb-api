from fastapi import APIRouter, Request
from agents.orchestrator import run_orchestrator
from memory.memory_core import MemoryCore

router = APIRouter()
MEMORY = MemoryCore()

@router.post("/v2/message")
async def message(req: Request):
    data = await req.json()
    user_id = data.get("user_id", "default")
    msg = data.get("message", "")

    context = MEMORY.get(user_id)
    result = run_orchestrator(msg, context)

    MEMORY.store(user_id, msg, result)

    return result
