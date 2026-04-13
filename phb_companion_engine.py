import os
import time
import sqlite3
from pathlib import Path
from typing import Optional, Literal

from phb_intelligence_core import run_intelligence_core

DB_PATH = Path(os.getenv("PHB_COMPANION_DB", "phb_companion.db"))

EMOTIONS = ("neutral", "focused", "stressed", "curious", "encouraging")
Tone = Literal["warm", "direct", "analytical"]

def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        created_ts REAL,
        last_ts REAL,
        label TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        ts REAL,
        role TEXT,
        content TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS state (
        session_id TEXT PRIMARY KEY,
        emotion TEXT,
        tone TEXT,
        notes TEXT
    )
    """)
    conn.commit()
    conn.close()

def ensure_session(session_id: str) -> None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM sessions WHERE id = ?", (session_id,))
    row = cur.fetchone()
    now = time.time()
    if row is None:
        cur.execute(
            "INSERT INTO sessions (id, created_ts, last_ts, label) VALUES (?, ?, ?, ?)",
            (session_id, now, now, "default"),
        )
        cur.execute(
            "INSERT OR REPLACE INTO state (session_id, emotion, tone, notes) VALUES (?, ?, ?, ?)",
            (session_id, "neutral", "warm", ""),
        )
    else:
        cur.execute(
            "UPDATE sessions SET last_ts = ? WHERE id = ?",
            (now, session_id),
        )
    conn.commit()
    conn.close()

def append_message(session_id: str, role: str, content: str) -> None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (session_id, ts, role, content) VALUES (?, ?, ?, ?)",
        (session_id, time.time(), role, content),
    )
    conn.commit()
    conn.close()

def load_recent_context(session_id: str, limit: int = 8) -> list[dict]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT ts, role, content FROM messages WHERE session_id = ? ORDER BY ts DESC LIMIT ?",
        (session_id, limit),
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in reversed(rows)]

def load_state(session_id: str) -> dict:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT emotion, tone, notes FROM state WHERE session_id = ?",
        (session_id,),
    )
    row = cur.fetchone()
    conn.close()
    if row is None:
        return {"emotion": "neutral", "tone": "warm", "notes": ""}
    return dict(row)

def save_state(session_id: str, emotion: str, tone: str, notes: str) -> None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO state (session_id, emotion, tone, notes) VALUES (?, ?, ?, ?)",
        (session_id, emotion, tone, notes),
    )
    conn.commit()
    conn.close()

def _infer_emotion(user_message: str, prev_emotion: str) -> str:
    msg = user_message.lower()
    if any(k in msg for k in ("stuck", "overwhelmed", "tired", "burnt")):
        return "stressed"
    if any(k in msg for k in ("idea", "curious", "wonder", "explore")):
        return "curious"
    if any(k in msg for k in ("let's go", "ready", "focus", "plan", "design a better flow")):
        return "focused"
    if prev_emotion in EMOTIONS:
        return prev_emotion
    return "neutral"

def _select_tone(emotion: str) -> Tone:
    if emotion in ("stressed",):
        return "warm"
    if emotion in ("focused",):
        return "direct"
    if emotion in ("curious",):
        return "analytical"
    return "warm"

def generate_companion_reply(
    session_id: str,
    user_message: str,
) -> dict:
    ensure_session(session_id)
    append_message(session_id, "user", user_message)

    state = load_state(session_id)
    prev_emotion = state.get("emotion", "neutral")
    emotion = _infer_emotion(user_message, prev_emotion)
    tone = _select_tone(emotion)

    context = load_recent_context(session_id, limit=6)

    msg = user_message.strip()
    lower = msg.lower()

    if not msg:
        base = "I’m here. Tell me what’s on your mind and we’ll unpack it step by step."
    elif "help" in lower and "plan" in lower:
        base = "Walk me through what you’re trying to do, and I’ll help you structure it clearly."
    elif "plan" in lower or "next step" in lower or "design a better flow" in lower:
        base = "Let’s pin down where you are now, then we’ll define one concrete next step."
    elif "hello" in lower or "hi" in lower:
        base = "Hey — I’m with you. What are you actually wrestling with right now."
    elif "why" in lower or "keeps happening" in lower:
        base = "I’m following you. Give me one layer deeper so I can respond with precision."
    else:
        base = "I’m following you. Give me one layer deeper so I can respond with precision."

    if tone == "warm":
        style = "I’ll keep it grounded and steady with you."
    elif tone == "direct":
        style = "I’m going to be clear and to the point so you can move."
    else:  # analytical
        style = "I’ll look at the structure of what you’re saying and reflect it back cleanly."

    if context:
        last_user_msgs = [c for c in context if c["role"] == "user"]
        if last_user_msgs:
            last_user = last_user_msgs[-1]["content"]
            ctx_line = f" I remember you said: “{last_user}”."
        else:
            ctx_line = ""
    else:
        ctx_line = ""

    intel = run_intelligence_core(
        session_id=session_id,
        user_message=user_message,
        recent_context=context,
        emotion=emotion,
        tone=tone,
    )

    reply_text = f"{base} {style}{ctx_line}"

    if intel["plan"]["mode"] in ("strategic", "analytical"):
        reply_text += " " + intel["summary"]

        skel = intel["plan"].get("planning_skeleton", {})
        next_moves = skel.get("next_moves") or []
        if next_moves:
            # Mini‑plan: short, human, not overwhelming
            moves_str = " ".join(
                f"{i+1}) {m}" for i, m in enumerate(next_moves[:2])
            )
            reply_text += f" Here’s a simple way to move from here: {moves_str}"

    notes = state.get("notes", "") or ""
    notes = notes[:2000]
    save_state(session_id, emotion=emotion, tone=tone, notes=notes)

    append_message(session_id, "companion", reply_text)

    return {
        "reply_text": reply_text,
        "emotion": emotion,
        "tone": tone,
        "context_used": context,
        "intelligence": {
            "mode": intel["mode"],
            "plan": intel["plan"],
            "summary": intel["summary"],
        },
    }

def presence_ping(session_id: str, note: Optional[str] = None) -> None:
    ensure_session(session_id)
    state = load_state(session_id)
    notes = state.get("notes", "") or ""
    if note:
        notes = (notes + "\n" + note).strip()[:4000]
    save_state(
        session_id,
        emotion=state.get("emotion", "neutral"),
        tone=state.get("tone", "warm"),
        notes=notes,
    )

init_db()
