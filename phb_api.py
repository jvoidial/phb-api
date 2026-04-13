#!/usr/bin/env python3
import os
import json
import time
import uuid
from typing import Optional, Dict, Any

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from flask import Flask, request, jsonify

# -----------------------------
# Config / keys (env + local)
# -----------------------------

API_NAME = "PHB Universal API"
API_VERSION = "v1"

# Simple in‑memory key store for now (backed by env or later DB)
VALID_KEYS = set()

env_key = os.getenv("PHB_API_KEY")
if env_key:
    VALID_KEYS.add(env_key)


def validate_key(auth_header: Optional[str]) -> None:
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = auth_header.split(" ", 1)[1].strip()
    if token not in VALID_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")


# -----------------------------
# Core PHB engine stub
# (replace with real PHB calls)
# -----------------------------

def run_phb_companion(message: str) -> Dict[str, Any]:
    """
    This is the integration point:
    here you call your real PHB engine
    (scripts, runtime, JSON files, etc.)
    and return a structured JSON payload.
    """
    ts = time.time()
    return {
        "engine": "PHB COMPANION REPLY ORCHESTRATOR v1",
        "id": str(uuid.uuid4()),
        "ts": ts,
        "user_message": message,
        "reply": {
            "text": f"I heard: {message}. This is a placeholder reply from PHB.",
            "mode": "companion",
            "orientation": "growth-directed",
        },
        "meta": {
            "api": API_NAME,
            "version": API_VERSION,
        },
    }


# -----------------------------
# FastAPI (machine / services)
# -----------------------------

fastapi_app = FastAPI(
    title=API_NAME,
    version=API_VERSION,
    description="PHB universal API for robots, apps, and services.",
)

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@fastapi_app.post("/v1/companion")
async def companion_endpoint(
    payload: Dict[str, Any],
    authorization: Optional[str] = Header(default=None),
):
    validate_key(authorization)
    message = payload.get("message", "")
    if not message:
        raise HTTPException(status_code=400, detail="Field 'message' is required")
    result = run_phb_companion(message)
    return JSONResponse(content=result)


@fastapi_app.post("/v1/mindstate")
async def mindstate_endpoint(
    payload: Dict[str, Any],
    authorization: Optional[str] = Header(default=None),
):
    validate_key(authorization)
    message = payload.get("message", "")
    if not message:
        raise HTTPException(status_code=400, detail="Field 'message' is required")
    # For now, reuse same stub; later, call PHB mind dashboard
    result = run_phb_companion(message)
    result["engine"] = "PHB MINDSTATE API v1"
    return JSONResponse(content=result)


# -----------------------------
# Flask (chat / human mode)
# -----------------------------

flask_app = Flask(__name__)


@flask_app.route("/chat", methods=["POST"])
def chat_endpoint():
    auth_header = request.headers.get("Authorization")
    try:
        validate_key(auth_header)
    except HTTPException as e:
        return jsonify({"detail": e.detail}), e.status_code

    data = request.get_json(force=True, silent=True) or {}
    message = data.get("message", "")
    if not message:
        return jsonify({"detail": "Field 'message' is required"}), 400

    result = run_phb_companion(message)
    # For chat, return a slimmer payload
    return jsonify(
        {
            "reply": result["reply"]["text"],
            "id": result["id"],
            "ts": result["ts"],
            "meta": result["meta"],
        }
    )


# -----------------------------
# Combined launcher
# -----------------------------

if __name__ == "__main__":
    mode = os.getenv("PHB_API_MODE", "fastapi").lower()

    if mode == "flask":
        # Human/chat mode
        flask_app.run(host="0.0.0.0", port=int(os.getenv("PHB_FLASK_PORT", "5000")))
    else:
        # Machine/services mode (FastAPI via uvicorn)
        import uvicorn

        uvicorn.run(
            "phb_api:fastapi_app",
            host="0.0.0.0",
            port=int(os.getenv("PHB_FASTAPI_PORT", "8000")),
            reload=False,
        )
