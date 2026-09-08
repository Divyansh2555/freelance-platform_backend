import enum

from sqlalchemy import Column, Integer, String, Enum
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

    # Store bcrypt hashed password, never plain password
    password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        Enum(UserRole),
        default=UserRole.client,
        nullable=False
    )
