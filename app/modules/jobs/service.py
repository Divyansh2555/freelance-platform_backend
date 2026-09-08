from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .model import Job
from .repository import JobRepository
from .schema import JobCreate, JobUpdate


class JobService:

    @staticmethod
    def create_job(
        db: Session,
        job_data: JobCreate,
        client_id: int,
    ) -> Job:
        return JobRepository.create(
            db=db,
            job_data=job_data,
            client_id=client_id,
        )

    @staticmethod
    def get_job(
        db: Session,
        job_id: int,
    ) -> Job:
        job = JobRepository.get_by_id(
            db=db,
            job_id=job_id,
        )

        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found",
            )

        return job

    @staticmethod
    def get_jobs(
        db: Session,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Job]:
        return JobRepository.get_all(
            db=db,
            skip=skip,
            limit=limit,
        )

    @staticmethod
    def update_job(
        db: Session,
        job_id: int,
        job_data: JobUpdate,
        client_id: int,
    ) -> Job:
        job = JobService.get_job(
            db=db,
            job_id=job_id,
        )

        if job.client_id != client_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update this job",
            )

        return JobRepository.update(
            db=db,
            job=job,
            job_data=job_data,
        )

    @staticmethod
    def delete_job(
        db: Session,
        job_id: int,
        client_id: int,
    ) -> None:
        job = JobService.get_job(
            db=db,
            job_id=job_id,
        )

        if job.client_id != client_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this job",
            )

        JobRepository.delete(
            db=db,
            job=job,
        )
