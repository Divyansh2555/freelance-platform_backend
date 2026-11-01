from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user

from app.modules.auth.models import User

from app.modules.project.schema import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
)

from app.modules.project.service import (
    create_project,
    get_project_by_id,
    get_all_projects,
    get_my_projects,
    get_my_project_by_id,
    update_project,
    delete_project,
)


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


# ==========================================
# CREATE PROJECT
# ==========================================

@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_project(
        db=db,
        project_data=project_data,
        current_user=current_user,
    )


# ==========================================
# PUBLIC - GET ALL OPEN PROJECTS
# ==========================================

@router.get(
    "/",
    response_model=list[ProjectResponse],
    status_code=status.HTTP_200_OK,
)
def get_projects(
    db: Session = Depends(get_db),
):
    return get_all_projects(
        db=db,
    )


# ==========================================
# PRIVATE - GET MY PROJECTS
# ==========================================

@router.get(
    "/my",
    response_model=list[ProjectResponse],
    status_code=status.HTTP_200_OK,
)
def get_my_projects_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_projects(
        db=db,
        current_user=current_user,
    )


# ==========================================
# PRIVATE - GET MY PROJECT BY ID
# ==========================================

@router.get(
    "/my/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
def get_my_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_project_by_id(
        db=db,
        project_id=project_id,
        current_user=current_user,
    )


# ==========================================
# PUBLIC - GET SINGLE OPEN PROJECT
# ==========================================

@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    return get_project_by_id(
        db=db,
        project_id=project_id,
    )


# ==========================================
# UPDATE PROJECT
# ==========================================

@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
def update_existing_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_project(
        db=db,
        project_id=project_id,
        project_data=project_data,
        current_user=current_user,
    )


# ==========================================
# DELETE PROJECT
# ==========================================

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_200_OK,
)
def delete_existing_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_project(
        db=db,
        project_id=project_id,
        current_user=current_user,
    )
