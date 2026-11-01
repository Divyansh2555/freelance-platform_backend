import enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    DateTime,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class UserRole(str, enum.Enum):
    client = "client"
    freelancer = "freelancer"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        Enum(UserRole),
        default=UserRole.client,
        nullable=False
    )

    # =========================
    # Password Reset
    # =========================

    reset_token_hash = Column(
        String(64),
        nullable=True,
        index=True
    )

    reset_token_expires = Column(
        DateTime(timezone=True),
        nullable=True
    )

    # =========================
    # Client Projects
    # =========================

    projects = relationship(
        "Project",
        back_populates="client",
        cascade="all, delete-orphan",
    )