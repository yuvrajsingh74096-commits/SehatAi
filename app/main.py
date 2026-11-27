"""FastAPI entry point for SehatAI."""

from __future__ import annotations

import uuid
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.data.languages import INDIAN_LANGUAGES
from app.state_machine import SessionState, get_knowledge_counts, process_voice_turn

app = FastAPI(
    title="SehatAI — Voice-First Healthcare Companion (India)",
    version="0.3.0",
    description="Starts with zero external API keys; covers 22 Scheduled Indian languages, 100+ diseases, 1000+ symptoms, and 500+ nutrition entries.",
)

templates = Jinja2Templates(directory="app/templates")

SESSIONS: dict[str, SessionState] = {}


class TurnRequest(BaseModel):
    session_id: str | None = None
    transcript: str = Field(default="", max_length=2000)
    confidence: float = Field(default=0.92, ge=0.0, le=1.0)
    noise_level: Literal["low", "medium", "high"] = "low"
    language: str | None = None


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "app": "SehatAI",
        "status": "ok",
        "offline_mode": True,
        "knowledge_base": get_knowledge_counts(),
        "active_sessions": len(SESSIONS),
    }


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "languages": INDIAN_LANGUAGES,
            "counts": get_knowledge_counts(),
        },
    )


@app.post("/api/session/reset")
def reset_session(session_id: str | None = None) -> dict[str, object]:
    if session_id and session_id in SESSIONS:
        del SESSIONS[session_id]
    new_id = str(uuid.uuid4())
    SESSIONS[new_id] = SessionState(session_id=new_id)
    return {"session_id": new_id, "offline_mode": True}


@app.post("/api/voice/turn")
def voice_turn(payload: TurnRequest) -> dict[str, object]:
    sid = payload.session_id or str(uuid.uuid4())
    if sid not in SESSIONS:
        SESSIONS[sid] = SessionState(session_id=sid)
    state = SESSIONS[sid]

    result = process_voice_turn(
        state=state,
        transcript=payload.transcript,
        confidence=payload.confidence,
        noise_level=payload.noise_level,
        requested_language=payload.language,
    )
    result["offline_mode"] = True
    result["knowledge_base"] = get_knowledge_counts()
    return result
