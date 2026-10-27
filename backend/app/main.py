# Patch compatibility between Starlette 1.3.x and FastAPI 0.111.x before importing FastAPI
try:
    import starlette.routing
    if not hasattr(starlette.routing.Router, "_crimevision_patched"):
        _orig_router_init = starlette.routing.Router.__init__
        def _patched_router_init(self, *args, on_startup=None, on_shutdown=None, **kwargs):
            self.on_startup = list(on_startup or [])
            self.on_shutdown = list(on_shutdown or [])
            return _orig_router_init(self, *args, **kwargs)
        starlette.routing.Router.__init__ = _patched_router_init
        starlette.routing.Router._crimevision_patched = True
except Exception:
    pass

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import init_db
from .services.mock_service import ensure_synthetic_keyframes
from .routers import image, audio, video, fusion, chat, report, cases

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite tables and default seed data on startup
    init_db()
    ensure_synthetic_keyframes()
    yield

app = FastAPI(
    title="CrimeVision AI – Intelligent Multimodal Forensic Analysis Platform",
    description="REST backend for multimodal forensic intelligence using FastAPI, SQLite, and Google Gemini AI.",
    version="1.0.0",
    lifespan=lifespan
)

# Export aliases for Vercel Python runtime
application = app
handler = app

# Enable CORS for Streamlit and cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount local upload directory and static keyframes for preview access
keyframes_dir = settings.UPLOAD_DIR / "keyframes"
keyframes_dir.mkdir(parents=True, exist_ok=True)
if settings.UPLOAD_DIR.exists():
    app.mount("/uploads", StaticFiles(directory=str(settings.UPLOAD_DIR)), name="uploads")
if keyframes_dir.exists():
    app.mount("/static", StaticFiles(directory=str(keyframes_dir)), name="static")

# Register API v1 Routers
app.include_router(image.router, prefix=settings.API_V1_PREFIX)
app.include_router(audio.router, prefix=settings.API_V1_PREFIX)
app.include_router(video.router, prefix=settings.API_V1_PREFIX)
app.include_router(fusion.router, prefix=settings.API_V1_PREFIX)
app.include_router(chat.router, prefix=settings.API_V1_PREFIX)
app.include_router(report.router, prefix=settings.API_V1_PREFIX)
app.include_router(cases.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {
        "platform": "CrimeVision AI Forensic Engine",
        "version": "1.0.0",
        "gemini_active": settings.is_gemini_active,
        "active_model": settings.GEMINI_MODEL if settings.is_gemini_active else "Sandbox / Mock Fallback Engine",
        "documentation": "/docs",
        "status": "OPERATIONAL"
    }

@app.get("/api/health")
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "sqlite3 connected",
        "gemini_mode": "live" if settings.is_gemini_active else "mock_sandbox",
        "gemini_api_key_configured": settings.is_gemini_active
    }
