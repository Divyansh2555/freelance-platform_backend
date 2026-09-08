
from sqlalchemy.orm import Session

from app.modules.client.model import ClientProfile
from app.modules.client.schema import ClientProfileUpdate


# =========================================================
# CREATE PROFILE
# =========================================================

def create_profile(
    db: Session,
    user_id: int,
    company_name: str | None = None,
    bio: str | None = None,
    location: str | None = None,
    profile_image_url: str | None = None,
    cover_image_url: str | None = None,
    website: str | None = None,
    industry: str | None = None,
    company_size: str | None = None,
    founded_year: int | None = None,
    phone: str | None = None,
    country: str | None = None,
    timezone: str | None = None,
):
    # Check existing profile
    existing_profile = (
        db.query(ClientProfile)
        .filter(
            ClientProfile.user_id == user_id
        )
        .first()
    )

    if existing_profile:
        return existing_profile

    # Create profile
    db_profile = ClientProfile(
        user_id=user_id,

        # Basic Profile
        company_name=company_name,
        bio=bio,
        location=location,

        # Profile Images
        profile_image_url=profile_image_url,
        cover_image_url=cover_image_url,

        # Business
        website=website,
        industry=industry,
        company_size=company_size,
        founded_year=founded_year,

        # Contact
        phone=phone,
        country=country,
        timezone=timezone,

        # Stats
        jobs_posted=0,
        hires=0,
        active_jobs=0,
        reviews_count=0,
        rating=0,

        # Verification
        is_verified=False,
    )

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return db_profile


# =========================================================
# GET ALL PROFILES
# =========================================================

def get_profiles(
    db: Session,
):
    return (
        db.query(ClientProfile)
        .order_by(ClientProfile.id.desc())
        .all()
    )


# =========================================================
# GET PROFILE BY ID
# =========================================================

def get_profile(
    db: Session,
    profile_id: int,
):
    return (
        db.query(ClientProfile)
        .filter(
            ClientProfile.id == profile_id
        )
        .first()
    )


# =========================================================
# GET PROFILE BY USER ID
# =========================================================

def get_profile_by_user_id(
    db: Session,
    user_id: int,
):
    return (
        db.query(ClientProfile)
        .filter(
            ClientProfile.user_id == user_id
        )
        .first()
    )


# =========================================================
# UPDATE PROFILE
# =========================================================

def update_profile(
    db: Session,
    profile_id: int,
    profile: ClientProfileUpdate,
):
    db_profile = get_profile(
        db=db,
        profile_id=profile_id,
    )

    if not db_profile:
        return None

    update_data = profile.model_dump(
        exclude_unset=True
    )

    allowed_fields = {
        "company_name",
        "bio",
        "location",

        # Profile Images
        "profile_image_url",
        "cover_image_url",

        # Business
        "website",
        "industry",
        "company_size",
        "founded_year",

        # Contact
        "phone",
        "country",
        "timezone",
    }

    for key, value in update_data.items():
        if key in allowed_fields:
            setattr(
                db_profile,
                key,
                value,
            )

    db.commit()
    db.refresh(db_profile)

    return db_profile


# =========================================================
# DELETE PROFILE
# =========================================================

def delete_profile(
    db: Session,
    profile_id: int,
):
    db_profile = get_profile(
        db=db,
        profile_id=profile_id,
    )

    if not db_profile:
        return None

    db.delete(db_profile)
    db.commit()

    return db_profile
