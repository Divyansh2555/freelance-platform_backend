from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

from app.modules.proposal.model import ProposalStatus


class ProposalCreate(BaseModel):
    project_id: int = Field(gt=0)

    cover_letter: str = Field(
        min_length=20,
        max_length=5000,
    )

    bid_amount: Decimal = Field(
        gt=0,
    )

    estimated_days: int = Field(
        gt=0,
        le=3650,
    )


class ProposalResponse(BaseModel):
    id: int
    project_id: int
    freelancer_id: int
    cover_letter: str
    bid_amount: Decimal
    estimated_days: int
    status: ProposalStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )