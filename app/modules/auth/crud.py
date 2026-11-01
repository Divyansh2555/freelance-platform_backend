from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.modules.auth.models import User
from app.modules.auth.schemas import UserCreate
from app.core.security import hash_password


def create_user(
    db: Session,
    user: UserCreate
):
    hashed_password = hash_password(
        user.password
    )

    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user(
    db: Session,
    user_id: int
):
    return db.query(User).filter(
        User.id == user_id
    ).first()


def get_user_by_email(
    db: Session,
    email: str
):
    return db.query(User).filter(
        User.email == email
    ).first()


def get_users(db: Session):
    return db.query(User).all()


def delete_user(
    db: Session,
    user_id: int
):
    user = get_user(
        db,
        user_id
    )

    if user:
        db.delete(user)
        db.commit()

    return user


# =========================
# Password Reset
# =========================

def save_reset_token(
    db: Session,
    user: User,
    token_hash: str,
    expires_at: datetime
):
    user.reset_token_hash = token_hash
    user.reset_token_expires = expires_at

    db.commit()
    db.refresh(user)

    return user


def get_user_by_reset_token(
    db: Session,
    token_hash: str
):
    user = (
        db.query(User)
        .filter(
            User.reset_token_hash
            == token_hash
        )
        .first()
    )

    if not user:
        return None

    if not user.reset_token_expires:
        return None

    now = datetime.now(timezone.utc)

    expires_at = user.reset_token_expires

    # SQLite / some DB configurations
    # may return naive datetime.
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(
            tzinfo=timezone.utc
        )

    if expires_at <= now:
        return None

    return user


def clear_reset_token(
    db: Session,
    user: User
):
    user.reset_token_hash = None
    user.reset_token_expires = None

    db.commit()
    db.refresh(user)

    return user