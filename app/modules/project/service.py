from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.auth.models import User
from app.modules.project.model import Project
from app.modules.project.schema import (
    ProjectCreate,
    ProjectUpdate,
)


# ==========================================
# CREATE PROJECT
# ==========================================

def create_project(
    db: Session,
    project_data: ProjectCreate,
    current_user: User,
) -> Project:

    # Only client can create project
    if current_user.role != "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only clients can create projects",
        )

    project = Project(
        client_id=current_user.id,
        title=project_data.title,
        description=project_data.description,
        category=project_data.category,
        budget_type=project_data.budget_type,
        budget_min=project_data.budget_min,
        budget_max=project_data.budget_max,
        experience_level=project_data.experience_level,
        deadline=project_data.deadline,
        location=project_data.location,
        status="open",
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


# ==========================================
# PUBLIC
# GET SINGLE PROJECT BY ID
# ==========================================

def get_project_by_id(
    db: Session,
    project_id: int,
) -> Project:

    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.status == "open",
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


# ==========================================
# PUBLIC
# GET ALL OPEN PROJECTS
# ==========================================

def get_all_projects(
    db: Session,
):
    return (
        db.query(Project)
        .filter(
            Project.status == "open",
        )
        .order_by(
            Project.created_at.desc()
        )
        .all()
    )


# ==========================================
# PRIVATE
# GET MY PROJECTS
# ==========================================

def get_my_projects(
    db: Session,
    current_user: User,
):
    return (
        db.query(Project)
        .filter(
            Project.client_id == current_user.id,
        )
        .order_by(
            Project.created_at.desc()
        )
        .all()
    )


# ==========================================
# PRIVATE
# GET MY PROJECT BY ID
# ==========================================

def get_my_project_by_id(
    db: Session,
    project_id: int,
    current_user: User,
) -> Project:

    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.client_id == current_user.id,
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


# ==========================================
# UPDATE PROJECT
# ==========================================

def update_project(
    db: Session,
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User,
) -> Project:

    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.client_id == current_user.id,
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    # Current values + new values
    budget_min = (
        project_data.budget_min
        if project_data.budget_min is not None
        else project.budget_min
    )

    budget_max = (
        project_data.budget_max
        if project_data.budget_max is not None
        else project.budget_max
    )

    if (
        budget_min is not None
        and budget_max is not None
        and budget_min > budget_max
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Minimum budget cannot be greater than maximum budget",
        )

    # Only update provided fields
    update_data = project_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return project


# ==========================================
# DELETE PROJECT
# ==========================================

def delete_project(
    db: Session,
    project_id: int,
    current_user: User,
):

    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.client_id == current_user.id,
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }
