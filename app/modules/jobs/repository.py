from sqlalchemy import select
from sqlalchemy.orm import Session

from .model import Job
from .schema import JobCreate, JobUpdate


class JobRepository:

    @staticmethod
    def create(
        db: Session,
        job_data: JobCreate,
        client_id: int,
    ) -> Job:
        job = Job(
            **job_data.model_dump(),
            client_id=client_id,
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        return job

    @staticmethod
    def get_by_id(
        db: Session,
        job_id: int,
    ) -> Job | None:
        statement = select(Job).where(Job.id == job_id)

        return db.scalar(statement)

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Job]:
        statement = (
            select(Job)
            .offset(skip)
            .limit(limit)
            .order_by(Job.created_at.desc())
        )

        return list(db.scalars(statement).all())

    @staticmethod
    def update(
        db: Session,
        job: Job,
        job_data: JobUpdate,
    ) -> Job:
        update_data = job_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(job, field, value)

        db.commit()
        db.refresh(job)

        return job

    @staticmethod
    def delete(
        db: Session,
        job: Job,
    ) -> None:
        db.delete(job)
        db.commit()
