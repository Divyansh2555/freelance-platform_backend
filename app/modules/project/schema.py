from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    model_validator,
)


# ==========================================
# CREATE PROJECT
# ==========================================

class ProjectCreate(BaseModel):

    title: str = Field(
        ...,
        min_length=5,
        max_length=200,
    )

    description: str = Field(
        ...,
        min_length=20,
    )

    category: str | None = Field(
        default=None,
        max_length=100,
    )

    budget_type: str = Field(
        default="fixed",
        pattern="^(fixed|hourly)$",
    )

    budget_min: Decimal | None = Field(
        default=None,
        ge=0,
    )

    budget_max: Decimal | None = Field(
        default=None,
        ge=0,
    )

    experience_level: str | None = Field(
        default=None,
        pattern="^(entry|intermediate|expert)$",
    )

    deadline: datetime | None = None

    location: str | None = Field(
        default=None,
        max_length=100,
    )

    @model_validator(mode="after")
    def validate_budget(self):
        if (
            self.budget_min is not None
            and self.budget_max is not None
            and self.budget_min > self.budget_max
        ):
            raise ValueError(
                "Minimum budget cannot be greater than maximum budget"
            )

        return self


# ==========================================
# UPDATE PROJECT
# ==========================================

class ProjectUpdate(BaseModel):

    title: str | None = Field(
        default=None,
        min_length=5,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        min_length=20,
    )

    category: str | None = Field(
        default=None,
        max_length=100,
    )

    budget_type: str | None = Field(
        default=None,
        pattern="^(fixed|hourly)$",
    )

    budget_min: Decimal | None = Field(
        default=None,
        ge=0,
    )

    budget_max: Decimal | None = Field(
        default=None,
        ge=0,
    )

    experience_level: str | None = Field(
        default=None,
        pattern="^(entry|intermediate|expert)$",
    )

    deadline: datetime | None = None

    location: str | None = Field(
        default=None,
        max_length=100,
    )

    status: str | None = Field(
        default=None,
        pattern="^(draft|open|in_progress|completed|cancelled)$",
    )

    @model_validator(mode="after")
    def validate_budget(self):
        if (
            self.budget_min is not None
            and self.budget_max is not None
            and self.budget_min > self.budget_max
        ):
            raise ValueError(
                "Minimum budget cannot be greater than maximum budget"
            )

        return self


# ==========================================
# PROJECT RESPONSE
# ==========================================

class ProjectResponse(BaseModel):

    id: int

    client_id: int

    title: str
    description: str

    category: str | None

    budget_type: str

    budget_min: Decimal | None
    budget_max: Decimal | None

    experience_level: str | None

    deadline: datetime | None

    location: str | None

    status: str

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
