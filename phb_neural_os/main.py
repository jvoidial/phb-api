from fastapi import FastAPI
from api.routes.message import router
from runtime.supervisor import start_supervisor

app = FastAPI(title="PHB Neural OS")

app.include_router(router)

@app.on_event("startup")
def boot():
    start_supervisor()

@app.get("/")
def root():
    return {"status": "PHB NEURAL OS ACTIVE"}
