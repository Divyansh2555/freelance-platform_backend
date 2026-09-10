from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.auth.models import User
from app.modules.project.model import Project
from app.modules.project.schema import ProjectCreate, ProjectUpdate


# =========================================================
# CREATE PROJECT
# =========================================================

def create_project(
    db: Session,
    project_data: ProjectCreate,
    user_id: int,
) -> Project:

    # Check if user exists
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    project = Project(
        user_id=user_id,
        title=project_data.title,
        description=project_data.description,
        budget=project_data.budget,
        deadline=project_data.deadline,
        category=project_data.category,
        status="open",
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


# =========================================================
# GET SINGLE PROJECT
# =========================================================

def get_project(
    db: Session,
    project_id: int,
) -> Project | None:

    return (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )


# =========================================================
# GET ALL PROJECTS
# =========================================================

def get_projects(
    db: Session,
) -> list[Project]:

    return (
        db.query(Project)
        .order_by(Project.created_at.desc())
        .all()
    )


# =========================================================
# GET USER'S PROJECTS
# =========================================================

def get_user_projects(
    db: Session,
    user_id: int,
) -> list[Project]:

    # Check if user exists
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    return (
        db.query(Project)
        .filter(Project.user_id == user_id)
        .order_by(Project.created_at.desc())
        .all()
    )


# =========================================================
# UPDATE PROJECT
# =========================================================

def update_project(
    db: Session,
    project: Project,
    project_data: ProjectUpdate,
) -> Project:

    update_data = project_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


# =========================================================
# DELETE PROJECT
# =========================================================

def delete_project(
    db: Session,
    project: Project,
) -> None:

    db.delete(project)
    db.commit()
