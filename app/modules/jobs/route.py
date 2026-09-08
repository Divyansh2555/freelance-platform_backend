from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.modules.auth.models import User

from .schema import JobCreate, JobResponse, JobUpdate
from .service import JobService


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


# =========================
# CREATE JOB - JWT REQUIRED
# =========================

@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return JobService.create_job(
        db=db,
        job_data=job_data,
        client_id=current_user.id,
    )


# =========================
# GET ALL JOBS - JWT REQUIRED
# =========================

@router.get(
    "",
    response_model=list[JobResponse],
)
def get_jobs(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return JobService.get_jobs(
        db=db,
        skip=skip,
        limit=limit,
    )


# =========================
# GET SINGLE JOB - JWT REQUIRED
# =========================

@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return JobService.get_job(
        db=db,
        job_id=job_id,
    )


# =========================
# UPDATE JOB - JWT REQUIRED
# =========================

@router.put(
    "/{job_id}",
    response_model=JobResponse,
)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return JobService.update_job(
        db=db,
        job_id=job_id,
        job_data=job_data,
        client_id=current_user.id,
    )


# =========================
# DELETE JOB - JWT REQUIRED
# =========================

@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    JobService.delete_job(
        db=db,
        job_id=job_id,
        client_id=current_user.id,
    )

    return None
