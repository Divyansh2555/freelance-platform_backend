from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.modules.auth.models import User
from app.modules.freelancer.schema import (
    FreelancerProfileCreate,
    FreelancerProfileUpdate,
    FreelancerProfileResponse,
)
from app.modules.freelancer import crud


router = APIRouter(
    prefix="/freelancer/profile",
    tags=["Freelancer Profile"],
)


@router.post("/", response_model=FreelancerProfileResponse)
def create_profile(
    profile: FreelancerProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.create_profile(
        db,
        profile,
        current_user.id,
    )


@router.get("/", response_model=list[FreelancerProfileResponse])
def get_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.get_profiles(
        db,
        current_user.id,
    )


@router.get("/{profile_id}", response_model=FreelancerProfileResponse)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = crud.get_profile(
        db,
        profile_id,
        current_user.id,
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return profile


@router.put("/{profile_id}", response_model=FreelancerProfileResponse)
def update_profile(
    profile_id: int,
    profile: FreelancerProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = crud.update_profile(
        db,
        profile_id,
        profile,
        current_user.id,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return updated


@router.delete("/{profile_id}")
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = crud.delete_profile(
        db,
        profile_id,
        current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return {"message": "Profile deleted"}
