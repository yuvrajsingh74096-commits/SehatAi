from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.state_machine import (
    INDIAN_LANGUAGES,
    SessionState,
    get_key_status,
    get_knowledge_counts,
    process_voice_turn,
)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="SehatAI", version="0.3.0")

static_dir = BASE_DIR / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
session_state = SessionState()


class TurnRequest(BaseModel):
    text: str = ""
    language: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "languages": INDIAN_LANGUAGES,
            "counts": get_knowledge_counts(),
            "keys": get_key_status(),
            "state": session_state,
        },
    )


@app.get("/api/status")
async def status():
    return JSONResponse(
        {
            "ok": True,
            "keys": get_key_status(),
            "counts": get_knowledge_counts(),
            "language": session_state.language,
        }
    )


@app.post("/api/turn")
async def handle_turn(payload: TurnRequest):
    result = process_voice_turn(
        state=session_state,
        transcript=payload.text,
        language=payload.language,
    )
    return JSONResponse(result)


@app.post("/api/reset")
async def reset_session():
    global session_state
    session_state = SessionState()
    return JSONResponse({"ok": True, "keys": get_key_status()})
