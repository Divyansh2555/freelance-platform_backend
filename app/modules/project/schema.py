from datetime import datetime

from pydantic import BaseModel, ConfigDict


# Common fields
class ProjectBase(BaseModel):
    title: str
    description: str
    budget: float
    deadline: datetime
    category: str


# Create
class ProjectCreate(ProjectBase):
    pass


# Update
class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    budget: float | None = None
    deadline: datetime | None = None
    category: str | None = None
    status: str | None = None


# Response
class ProjectResponse(ProjectBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
