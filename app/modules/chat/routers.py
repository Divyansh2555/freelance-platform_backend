from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user

from app.modules.auth.models import User
from app.modules.chat.schema import (
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)
from app.modules.chat.service import (
    get_or_create_conversation,
    create_message,
    get_messages,
    mark_message_as_read,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


# =========================================================
# SEARCH USERS
# =========================================================

@router.get("/users")
def search_users(
    search: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(User)
        .filter(User.id != current_user.id)
    )

    if search.strip():
        keyword = f"%{search.strip()}%"

        query = query.filter(
            or_(
                User.name.ilike(keyword),
                User.email.ilike(keyword),
            )
        )

    users = (
        query
        .order_by(User.name.asc())
        .limit(50)
        .all()
    )

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value,
        }
        for user in users
    ]


# =========================================================
# CREATE / GET ONE-TO-ONE CONVERSATION
# =========================================================

@router.post(
    "/conversation",
    response_model=ConversationResponse,
)
def create_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Khud ke saath chat nahi
    if data.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot create a conversation with yourself",
        )

    # Other user check
    other_user = (
        db.query(User)
        .filter(User.id == data.user_id)
        .first()
    )

    if not other_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    try:
        conversation = get_or_create_conversation(
            db=db,
            current_user_id=current_user.id,
            other_user_id=data.user_id,
        )

        return conversation

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =========================================================
# SEND MESSAGE - REST
# =========================================================
#
# NOTE:
# Real-time chat mein frontend WebSocket use karega.
# Is endpoint ko normal REST message sending/testing ke
# liye rakha gaya hai.
#
# =========================================================

@router.post(
    "/message",
    response_model=MessageResponse,
)
def send_message(
    data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not data.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty",
        )

    try:
        message = create_message(
            db=db,
            conversation_id=data.conversation_id,
            sender_id=current_user.id,
            message_text=data.message.strip(),
        )

        return message

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =========================================================
# GET ALL MESSAGES
# =========================================================

@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        messages = get_messages(
            db=db,
            conversation_id=conversation_id,
            current_user_id=current_user.id,
        )

        return messages

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


# =========================================================
# MARK MESSAGE AS READ
# =========================================================

@router.patch(
    "/message/{message_id}/read",
    response_model=MessageResponse,
)
def read_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        message = mark_message_as_read(
            db=db,
            message_id=message_id,
            current_user_id=current_user.id,
        )

        return message

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
