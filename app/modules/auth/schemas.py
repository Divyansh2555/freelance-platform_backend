from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict,
    Field,
)

from app.modules.auth.models import UserRole


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================
# Forgot Password
# =========================

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


# =========================
# Reset Password
# =========================

class ResetPasswordRequest(BaseModel):
    token: str = Field(
        min_length=20
    )

    new_password: str = Field(
        min_length=6,
        max_length=128
    )