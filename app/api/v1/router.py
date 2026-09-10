from fastapi import APIRouter

from app.modules.chat.routers import router as chat_router
from app.modules.auth.route import router as auth_router

from app.modules.jobs.route import router as job_router
from app.modules.project.router import router as project_router


router = APIRouter()


router.include_router(auth_router)
router.include_router(job_router)
router.include_router(project_router)


