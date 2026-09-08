from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    Boolean,
    DateTime,
)
from sqlalchemy.sql import func

from app.database.base import Base


class ClientProfile(Base):
    __tablename__ = "client_profiles"

    # =========================================================
    # PRIMARY
    # =========================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
        index=True,
    )

    # =========================================================
    # BASIC PROFILE
    # =========================================================

    company_name = Column(
        String(150),
        nullable=True,
    )

    bio = Column(
        Text,
        nullable=True,
    )

    location = Column(
        String(150),
        nullable=True,
    )

    # =========================================================
    # PROFILE IMAGES
    # =========================================================

    # Profile photo ka URL/path
    # Example:
    # https://your-domain.com/uploads/client/profile/abc123.jpg
    profile_image_url = Column(
        String(1000),
        nullable=True,
    )

    # Cover/banner photo ka URL/path
    # Example:
    # https://your-domain.com/uploads/client/cover/xyz456.jpg
    cover_image_url = Column(
        String(1000),
        nullable=True,
    )

    # =========================================================
    # CLIENT DETAILS
    # =========================================================

    website = Column(
        String(255),
        nullable=True,
    )

    industry = Column(
        String(150),
        nullable=True,
    )

    company_size = Column(
        String(100),
        nullable=True,
    )

    founded_year = Column(
        Integer,
        nullable=True,
    )

    # =========================================================
    # CONTACT / BUSINESS
    # =========================================================

    phone = Column(
        String(50),
        nullable=True,
    )

    country = Column(
        String(100),
        nullable=True,
    )

    timezone = Column(
        String(100),
        nullable=True,
    )

    # =========================================================
    # FREELANCING CLIENT STATS
    # =========================================================

    jobs_posted = Column(
        Integer,
        default=0,
        nullable=False,
    )

    hires = Column(
        Integer,
        default=0,
        nullable=False,
    )

    active_jobs = Column(
        Integer,
        default=0,
        nullable=False,
    )

    reviews_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    rating = Column(
        Integer,
        default=0,
        nullable=False,
    )

    # =========================================================
    # VERIFICATION
    # =========================================================

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # =========================================================
    # TIMESTAMPS
    # =========================================================

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
