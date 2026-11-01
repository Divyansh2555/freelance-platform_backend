from datetime import (
    datetime,
    timedelta,
    timezone,
)

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.modules.auth.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)

from app.modules.auth import crud

from app.core.security import (
    verify_password,
    hash_password,
)

from app.core.jwt import create_access_token

from app.core.reset_token import (
    create_reset_token,
    hash_reset_token,
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


# =========================
# Register
# =========================

@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = crud.get_user_by_email(
        db,
        user.email
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return crud.create_user(
        db,
        user
    )


# =========================
# Login
# =========================

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_email(
        db,
        user.email
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": str(db_user.id),
            "role": db_user.role.value,
        }
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email,
            "role": db_user.role.value,
        }
    }


# =========================
# Forgot Password
# =========================

@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(
        db,
        data.email
    )

    # Same response whether email exists
    # or not. This prevents email enumeration.
    if not user:
        return {
            "message": (
                "If the email is registered, "
                "a password reset link has been sent."
            )
        }

    # Generate secure token
    token, token_hash = (
        create_reset_token()
    )

    # Token valid for 30 minutes
    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(minutes=30)
    )

    crud.save_reset_token(
        db,
        user,
        token_hash,
        expires_at
    )

    # ---------------------------------
    # Development only
    # ---------------------------------
    # Later this token will be sent
    # through email.
    #
    # Production me token response
    # me return MAT karna.
    # ---------------------------------

    return {
        "message": (
            "If the email is registered, "
            "a password reset link has been sent."
        ),
        "reset_token": token,
    }


# =========================
# Reset Password
# =========================

@router.post("/reset-password")
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    token_hash = hash_reset_token(
        data.token
    )

    user = crud.get_user_by_reset_token(
        db,
        token_hash
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    # Hash new password
    user.password = hash_password(
        data.new_password
    )

    # Token can only be used once
    crud.clear_reset_token(
        db,
        user
    )

    return {
        "message": "Password reset successful"
    }


# =========================
# Get All Users
# =========================

@router.get(
    "/users",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):
    return crud.get_users(db)


# =========================
# Get User
# =========================

@router.get(
    "/users/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = crud.get_user(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


# =========================
# Delete User
# =========================

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = crud.delete_user(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "message": "User deleted"
    }