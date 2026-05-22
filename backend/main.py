"""FastAPI entry point for the Media AI Chatbot."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.catalog import catalog
from app.chatbot import engine
from app.models import ChatRequest, ChatResponse
from app.sessions import store

app = FastAPI(
    title="Media AI Chatbot - Stream Assistant",
    description="Demo conversational AI for the media, entertainment, and content-platform industry. NOT a real streaming service.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status":   "ok",
        "titles":   len(catalog.titles()),
        "plans":    len(catalog.plans()),
        "profiles": len(catalog.profiles()),
        "devices":  len(catalog.devices()),
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    session = store.get_or_create(req.session_id)
    return engine.respond(req.message, session)


@app.get("/titles")
def list_titles():
    return catalog.titles()


@app.get("/titles/{tid}")
def get_title(tid: str):
    t = catalog.title(tid)
    if not t:
        return {"error": "not_found", "id": tid}
    return t


@app.get("/profiles")
def list_profiles():
    return catalog.profiles()


@app.get("/plans")
def list_plans():
    return catalog.plans()


@app.get("/devices")
def list_devices():
    return catalog.devices()


@app.get("/")
def root():
    return {
        "name":       "Media AI Chatbot - Stream Assistant",
        "version":    app.version,
        "docs":       "/docs",
        "disclaimer": "Demo only. Not a real streaming service.",
    }
