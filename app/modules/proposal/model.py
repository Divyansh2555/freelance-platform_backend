from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    DateTime,
    ForeignKey,
    Enum,
    UniqueConstraint,
)

from app.database.base import Base

import enum


class ProposalStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    freelancer_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    cover_letter = Column(
        Text,
        nullable=False,
    )

    bid_amount = Column(
        Numeric(12, 2),
        nullable=False,
    )

    estimated_days = Column(
        Integer,
        nullable=False,
    )

    status = Column(
        Enum(ProposalStatus),
        default=ProposalStatus.pending,
        nullable=False,
    )

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

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "freelancer_id",
            name="uq_project_freelancer_proposal",
        ),
    )