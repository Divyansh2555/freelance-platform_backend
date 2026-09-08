from pydantic import BaseModel
from typing import Optional


class FreelancerProfileCreate(BaseModel):
    title: str
    bio: Optional[str] = None
    skills: Optional[str] = None
    experience: int = 0
    hourly_rate: Optional[float] = None
    location: Optional[str] = None


class FreelancerProfileUpdate(BaseModel):
    title: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[int] = None
    hourly_rate: Optional[float] = None
    location: Optional[str] = None


class FreelancerProfileResponse(BaseModel):
    id: int
    user_id: int
    title: str
    bio: Optional[str] = None
    skills: Optional[str] = None
    experience: int
    hourly_rate: Optional[float] = None
    location: Optional[str] = None

    class Config:
        from_attributes = True
