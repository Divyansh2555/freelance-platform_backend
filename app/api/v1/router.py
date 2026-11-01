from fastapi import APIRouter

from app.modules.client.router import router as client_router
from app.modules.auth.route import router as auth_router

from app.modules.jobs.route import router as job_router
from app.modules.project.router import router as project_router

from app.modules.proposal.router import router as proposal_router


router = APIRouter()


router.include_router(auth_router)
router.include_router(client_router)
router.include_router(job_router)
router.include_router(project_router)
router.include_router(proposal_router)



