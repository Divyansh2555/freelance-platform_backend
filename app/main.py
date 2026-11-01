from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import router as api_router

from app.database.base import Base
from app.database.connection import engine

from app.modules.client.router import router as client_router
from app.modules.freelancer.router import router as freelancer_router

from app.modules.chat.routers import router as chat_router
from app.modules.chat.websocket import router as chat_ws_router


# =========================================================
# BASE DIRECTORY
# =========================================================

# main.py:
# C:\Freelancing Platform\bkd\app\main.py
#
# PROJECT_DIR:
# C:\Freelancing Platform\bkd

PROJECT_DIR = Path(__file__).resolve().parent.parent

UPLOADS_DIR = PROJECT_DIR / "uploads"

CLIENT_PROFILE_DIR = (
    UPLOADS_DIR / "client" / "profile"
)

CLIENT_COVER_DIR = (
    UPLOADS_DIR / "client" / "cover"
)

FREELANCER_PROFILE_DIR = (
    UPLOADS_DIR / "freelancer" / "profile"
)


# =========================================================
# CREATE UPLOAD DIRECTORIES
# =========================================================

CLIENT_PROFILE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

CLIENT_COVER_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

FREELANCER_PROFILE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Freelancing Platform API",
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOADS_DIR)),
    name="uploads",
)


# =========================================================
# ROUTERS
# =========================================================


app.include_router(
    client_router,
)

app.include_router(
    freelancer_router,
)

app.include_router(
    chat_router,
)

app.include_router(
    chat_ws_router,
)

app.include_router(
    api_router,
    prefix="/api/v1",
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def read_root():
    return {
        "message": "Freelancing Platform API",
        "status": "running",
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }
