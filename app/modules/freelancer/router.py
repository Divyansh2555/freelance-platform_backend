from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.modules.auth.models import User
from app.modules.freelancer.schema import FreelancerProfileResponse
from app.modules.freelancer import crud


router = APIRouter(
    prefix="/freelancer/profile",
    tags=["Freelancer Profile"],
)


# =========================================================
# CREATE PROFILE
# =========================================================

@router.post(
    "/",
    response_model=FreelancerProfileResponse,
)
async def create_profile(
    title: str = Form(...),
    bio: Optional[str] = Form(None),
    skills: Optional[str] = Form(None),
    experience: int = Form(0),
    hourly_rate: Optional[float] = Form(None),
    location: Optional[str] = Form(None),
    profile_image: Optional[UploadFile] = File(None),

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = await crud.create_profile(
        db=db,
        user_id=current_user.id,
        title=title,
        bio=bio,
        skills=skills,
        experience=experience,
        hourly_rate=hourly_rate,
        location=location,
        profile_image=profile_image,
    )

    return profile


# =========================================================
# GET ALL PROFILES
# =========================================================

@router.get(
    "/",
    response_model=list[FreelancerProfileResponse],
)
def get_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.get_profiles(
        db=db,
        user_id=current_user.id,
    )


# =========================================================
# GET SINGLE PROFILE
# =========================================================

@router.get(
    "/{profile_id}",
    response_model=FreelancerProfileResponse,
)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = crud.get_profile(
        db=db,
        profile_id=profile_id,
        user_id=current_user.id,
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return profile


# =========================================================
# UPDATE PROFILE
# =========================================================

@router.put(
    "/{profile_id}",
    response_model=FreelancerProfileResponse,
)
async def update_profile(
    profile_id: int,

    title: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    skills: Optional[str] = Form(None),
    experience: Optional[int] = Form(None),
    hourly_rate: Optional[float] = Form(None),
    location: Optional[str] = Form(None),

    profile_image: Optional[UploadFile] = File(None),

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # -----------------------------------------------------
    # Find existing profile
    # -----------------------------------------------------

    existing_profile = crud.get_profile(
        db=db,
        profile_id=profile_id,
        user_id=current_user.id,
    )

    if existing_profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    # -----------------------------------------------------
    # Update profile
    # -----------------------------------------------------

    updated_profile = await crud.update_profile(
        db=db,
        profile_id=profile_id,
        user_id=current_user.id,
        title=title,
        bio=bio,
        skills=skills,
        experience=experience,
        hourly_rate=hourly_rate,
        location=location,
        profile_image=profile_image,
    )

    if updated_profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return updated_profile


# =========================================================
# DELETE PROFILE
# =========================================================

@router.delete("/{profile_id}")
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted_profile = crud.delete_profile(
        db=db,
        profile_id=profile_id,
        user_id=current_user.id,
    )

    if deleted_profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return {
        "message": "Profile deleted successfully"
    }
