from fastapi import APIRouter

from app.modules.chat.routers import router as chat_router
from app.modules.auth.route import router as auth_router



router = APIRouter()


router.include_router(auth_router)



