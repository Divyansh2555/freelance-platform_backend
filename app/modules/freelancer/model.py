from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from app.database.base import Base


class FreelancerProfile(Base):
    __tablename__ = "freelancer_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    title = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    skills = Column(String, nullable=True)
    experience = Column(Integer, default=0)
    hourly_rate = Column(Float, nullable=True)
    location = Column(String, nullable=True)