from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# =========================================================
# CREATE
# =========================================================

class ClientProfileCreate(BaseModel):
    company_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None

    # Profile Images
    profile_image_url: Optional[str] = None
    cover_image_url: Optional[str] = None

    # Business
    website: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    founded_year: Optional[int] = None

    # Contact
    phone: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None


# =========================================================
# UPDATE
# =========================================================

class ClientProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None

    # Profile Images
    profile_image_url: Optional[str] = None
    cover_image_url: Optional[str] = None

    # Business
    website: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    founded_year: Optional[int] = None

    # Contact
    phone: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None


# =========================================================
# RESPONSE
# =========================================================

class ClientProfileResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    # Primary
    id: int
    user_id: int

    # =========================================================
    # BASIC PROFILE
    # =========================================================

    company_name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None

    # =========================================================
    # PROFILE IMAGES
    # =========================================================

    profile_image_url: Optional[str] = None
    cover_image_url: Optional[str] = None

    # =========================================================
    # BUSINESS
    # =========================================================

    website: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    founded_year: Optional[int] = None

    # =========================================================
    # CONTACT
    # =========================================================

    phone: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None

    # =========================================================
    # FREELANCING STATS
    # =========================================================

    jobs_posted: int = 0
    hires: int = 0
    active_jobs: int = 0
    reviews_count: int = 0
    rating: int = 0

    # =========================================================
    # VERIFICATION
    # =========================================================

    is_verified: bool = False

    # =========================================================
    # TIMESTAMPS
    # =========================================================

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
