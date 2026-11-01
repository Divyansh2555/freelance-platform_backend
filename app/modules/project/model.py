from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =========================
    # CLIENT
    # =========================

    client_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # =========================
    # PROJECT INFORMATION
    # =========================

    title = Column(
        String(200),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    # =========================
    # CATEGORY
    # =========================

    category = Column(
        String(100),
        nullable=True,
    )

    # =========================
    # BUDGET
    # =========================

    budget_type = Column(
        String(20),
        nullable=False,
        default="fixed",
    )
    # fixed / hourly

    budget_min = Column(
        Numeric(12, 2),
        nullable=True,
    )

    budget_max = Column(
        Numeric(12, 2),
        nullable=True,
    )

    # =========================
    # EXPERIENCE
    # =========================

    experience_level = Column(
        String(30),
        nullable=True,
    )
    # entry / intermediate / expert

    # =========================
    # DEADLINE
    # =========================

    deadline = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # =========================
    # STATUS
    # =========================

    status = Column(
        String(30),
        nullable=False,
        default="open",
        index=True,
    )
    # draft / open / in_progress / completed / cancelled

    # =========================
    # LOCATION
    # =========================

    location = Column(
        String(100),
        nullable=True,
    )

    # =========================
    # TIMESTAMPS
    # =========================

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # =========================
    # RELATIONSHIP
    # =========================

    client = relationship(
        "User",
        back_populates="projects",
    )
