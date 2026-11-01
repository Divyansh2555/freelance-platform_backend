from pathlib import Path
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.modules.freelancer.model import FreelancerProfile


# =========================================================
# UPLOAD DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[3]

UPLOAD_DIR = (
    BASE_DIR
    / "uploads"
    / "freelancer"
    / "profile"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =========================================================
# SAVE PROFILE IMAGE
# =========================================================

async def save_profile_image(
    profile_image: UploadFile,
) -> str:

    # Validate content type
    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    if profile_image.content_type not in allowed_types:
        raise ValueError(
            "Only JPG, PNG and WEBP images are allowed"
        )

    # Get extension
    extension = Path(
        profile_image.filename or ""
    ).suffix.lower()

    if extension not in {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }:
        extension = ".jpg"

    # Read file
    contents = await profile_image.read()

    if not contents:
        raise ValueError(
            "Uploaded image is empty"
        )

    # Generate unique filename
    import uuid

    filename = (
        f"profile_{uuid.uuid4().hex}"
        f"{extension}"
    )

    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    # URL saved in database
    return (
        f"/uploads/freelancer/profile/{filename}"
    )


# =========================================================
# CREATE PROFILE
# =========================================================

async def create_profile(
    db: Session,
    user_id: int,
    title: str,
    bio: Optional[str] = None,
    skills: Optional[str] = None,
    experience: int = 0,
    hourly_rate: Optional[float] = None,
    location: Optional[str] = None,
    profile_image: Optional[UploadFile] = None,
):
    image_path = None

    if profile_image is not None:
        image_path = await save_profile_image(
            profile_image
        )

    new_profile = FreelancerProfile(
        user_id=user_id,
        title=title,
        bio=bio,
        skills=skills,
        experience=experience,
        hourly_rate=hourly_rate,
        location=location,
        profile_image=image_path,
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


# =========================================================
# GET ALL PROFILES
# =========================================================

def get_profiles(
    db: Session,
    user_id: int,
):
    return (
        db.query(FreelancerProfile)
        .filter(
            FreelancerProfile.user_id == user_id
        )
        .all()
    )


# =========================================================
# GET SINGLE PROFILE
# =========================================================

def get_profile(
    db: Session,
    profile_id: int,
    user_id: int,
):
    return (
        db.query(FreelancerProfile)
        .filter(
            FreelancerProfile.id == profile_id,
            FreelancerProfile.user_id == user_id,
        )
        .first()
    )


# =========================================================
# UPDATE PROFILE
# =========================================================

async def update_profile(
    db: Session,
    profile_id: int,
    user_id: int,

    title: Optional[str] = None,
    bio: Optional[str] = None,
    skills: Optional[str] = None,
    experience: Optional[int] = None,
    hourly_rate: Optional[float] = None,
    location: Optional[str] = None,

    profile_image: Optional[UploadFile] = None,
):
    profile = (
        db.query(FreelancerProfile)
        .filter(
            FreelancerProfile.id == profile_id,
            FreelancerProfile.user_id == user_id,
        )
        .first()
    )

    if profile is None:
        return None

    # -----------------------------------------------------
    # Update text fields
    # -----------------------------------------------------

    if title is not None:
        profile.title = title

    if bio is not None:
        profile.bio = bio

    if skills is not None:
        profile.skills = skills

    if experience is not None:
        profile.experience = experience

    if hourly_rate is not None:
        profile.hourly_rate = hourly_rate

    if location is not None:
        profile.location = location

    # -----------------------------------------------------
    # Update image ONLY if new image uploaded
    # -----------------------------------------------------

    if profile_image is not None:
        new_image_path = await save_profile_image(
            profile_image
        )

        # Delete old image
        if profile.profile_image:
            old_path = (
                BASE_DIR
                / profile.profile_image.lstrip("/")
            )

            try:
                if old_path.exists():
                    old_path.unlink()
            except OSError:
                pass

        profile.profile_image = new_image_path

    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    db.commit()
    db.refresh(profile)

    return profile


# =========================================================
# DELETE PROFILE
# =========================================================

def delete_profile(
    db: Session,
    profile_id: int,
    user_id: int,
):
    profile = (
        db.query(FreelancerProfile)
        .filter(
            FreelancerProfile.id == profile_id,
            FreelancerProfile.user_id == user_id,
        )
        .first()
    )

    if profile is None:
        return None

    # -----------------------------------------------------
    # Delete image from disk
    # -----------------------------------------------------

    if profile.profile_image:
        image_path = (
            BASE_DIR
            / profile.profile_image.lstrip("/")
        )

        try:
            if image_path.exists():
                image_path.unlink()
        except OSError:
            pass

    # -----------------------------------------------------
    # Delete database record
    # -----------------------------------------------------

    db.delete(profile)
    db.commit()

    return profile
