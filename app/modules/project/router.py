from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.modules.project.schema import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
)

from app.modules.project import service


router = APIRouter(
    prefix="/project",
    tags=["Project"],
)


# =========================================================
# CREATE PROJECT
# =========================================================

@router.post(
    "/create",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    data: ProjectCreate,
    user_id: int,
    db: Session = Depends(get_db),
):
    return service.create_project(
        db=db,
        project_data=data,
        user_id=user_id,
    )


# =========================================================
# GET SINGLE PROJECT
# =========================================================

@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = service.get_project(
        db=db,
        project_id=project_id,
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


# =========================================================
# GET USER PROJECTS
# =========================================================

@router.get(
    "/user/{user_id}",
    response_model=list[ProjectResponse],
)
def get_user_projects(
    user_id: int,
    db: Session = Depends(get_db),
):
    return service.get_user_projects(
        db=db,
        user_id=user_id,
    )


# =========================================================
# UPDATE PROJECT
# =========================================================

@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
):
    project = service.get_project(
        db=db,
        project_id=project_id,
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return service.update_project(
        db=db,
        project=project,
        project_data=data,
    )


# =========================================================
# DELETE PROJECT
# =========================================================

@router.delete(
    "/{project_id}",
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = service.get_project(
        db=db,
        project_id=project_id,
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    service.delete_project(
        db=db,
        project=project,
    )

    return {
        "status": "success",
        "message": "Project deleted successfully",
    }



@router.post("/",
             status_code=status.HTTP_200_OK,)



def create_projectas(age:int):
    return{
        "status": "success",
        "message": "Project created successfully",

        "age": age


    }

