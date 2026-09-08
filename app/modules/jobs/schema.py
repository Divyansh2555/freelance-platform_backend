from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class JobBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10)
    category: Optional[str] = Field(default=None, max_length=100)
    budget: Optional[Decimal] = Field(default=None, ge=0)
    skills: Optional[str] = None


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=255,
    )

    description: Optional[str] = Field(
        default=None,
        min_length=10,
    )

    category: Optional[str] = Field(
        default=None,
        max_length=100,
    )

    budget: Optional[Decimal] = Field(
        default=None,
        ge=0,
    )

    skills: Optional[str] = None

    status: Optional[str] = Field(
        default=None,
        max_length=50,
    )


class JobResponse(JobBase):
    id: int
    status: str
    client_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
