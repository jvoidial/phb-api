from fastapi import APIRouter
from phb_engine_router import route_engine

router = APIRouter()

@router.post("/v1/companion")
def companion(payload: dict):
    return route_engine(payload)
