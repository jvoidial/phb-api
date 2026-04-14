from fastapi import FastAPI
from phb_engine_router import route_engine

app = FastAPI()

@app.post("/v1/companion")
def companion(payload: dict):
    return route_engine(payload)
