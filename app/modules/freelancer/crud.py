from sqlalchemy.orm import Session

from app.modules.freelancer.model import FreelancerProfile
from app.modules.freelancer.schema import (
    FreelancerProfileCreate,
    FreelancerProfileUpdate,
)


def create_profile(
    db: Session,
    profile: FreelancerProfileCreate,
    user_id: int,
):
    db_profile = FreelancerProfile(
        user_id=user_id,
        title=profile.title,
        bio=profile.bio,
        skills=profile.skills,
        experience=profile.experience,
        hourly_rate=profile.hourly_rate,
        location=profile.location,
    )

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return db_profile


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


def get_profiles(
    db: Session,
    user_id: int,
):
    return (
        db.query(FreelancerProfile)
        .filter(FreelancerProfile.user_id == user_id)
        .all()
    )


def update_profile(
    db: Session,
    profile_id: int,
    profile: FreelancerProfileUpdate,
    user_id: int,
):
    db_profile = get_profile(
        db,
        profile_id,
        user_id,
    )

    if not db_profile:
        return None

    data = profile.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(db_profile, key, value)

    db.commit()
    db.refresh(db_profile)

    return db_profile


def delete_profile(
    db: Session,
    profile_id: int,
    user_id: int,
):
    db_profile = get_profile(
        db,
        profile_id,
        user_id,
    )

    if not db_profile:
        return None

    db.delete(db_profile)
    db.commit()

    return db_profile
