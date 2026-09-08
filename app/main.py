from pathlib import Path


from app.api.v1.router import router as api_router


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database.base import Base
from app.database.connection import engine

from app.modules.auth.route import router as auth_router
from app.modules.client.router import router as client_router
from app.modules.freelancer.router import router as freelancer_router

from app.modules.chat.routers import router as chat_router
from app.modules.chat.websocket import router as chat_ws_router
# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# APP
# =========================================================

app = FastAPI()


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

Path("uploads/client/profile").mkdir(
    parents=True,
    exist_ok=True,
)

Path("uploads/client/cover").mkdir(
    parents=True,
    exist_ok=True,
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)


# =========================================================
# ROUTERS
# =========================================================


app.include_router(auth_router)
app.include_router(client_router)
app.include_router(freelancer_router)


app.include_router(chat_router)
app.include_router(chat_ws_router)




app.include_router(api_router,prefix="/api/v1")


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def read_root():
    return {
        "message": "Freelancing Platform API"
    }




