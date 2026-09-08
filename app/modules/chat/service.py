from sqlalchemy.orm import Session

from app.modules.chat.model import Conversation, Message


# =========================================================
# GET OR CREATE ONE-TO-ONE CONVERSATION
# =========================================================

def get_or_create_conversation(
    db: Session,
    current_user_id: int,
    other_user_id: int,
):
    # Khud se chat nahi
    if current_user_id == other_user_id:
        raise ValueError("You cannot create a conversation with yourself")

    # Existing conversation check
    conversation = (
        db.query(Conversation)
        .filter(
            (
                (Conversation.user_one_id == current_user_id)
                & (Conversation.user_two_id == other_user_id)
            )
            |
            (
                (Conversation.user_one_id == other_user_id)
                & (Conversation.user_two_id == current_user_id)
            )
        )
        .first()
    )

    if conversation:
        return conversation

    # New conversation
    conversation = Conversation(
        user_one_id=current_user_id,
        user_two_id=other_user_id,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


# =========================================================
# SEND MESSAGE
# =========================================================

def create_message(
    db: Session,
    conversation_id: int,
    sender_id: int,
    message_text: str,
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id
        )
        .first()
    )

    if not conversation:
        raise ValueError("Conversation not found")

    # Check sender conversation ka participant hai
    if sender_id not in (
        conversation.user_one_id,
        conversation.user_two_id,
    ):
        raise ValueError(
            "You are not a participant of this conversation"
        )

    message = Message(
        conversation_id=conversation_id,
        sender_id=sender_id,
        message=message_text,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


# =========================================================
# GET CONVERSATION MESSAGES
# =========================================================

def get_messages(
    db: Session,
    conversation_id: int,
    current_user_id: int,
):
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id
        )
        .first()
    )

    if not conversation:
        raise ValueError("Conversation not found")

    # Sirf participants messages dekh sakte hain
    if current_user_id not in (
        conversation.user_one_id,
        conversation.user_two_id,
    ):
        raise ValueError(
            "You are not a participant of this conversation"
        )

    return (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(Message.created_at.asc())
        .all()
    )


# =========================================================
# MARK MESSAGE AS READ
# =========================================================

def mark_message_as_read(
    db: Session,
    message_id: int,
    current_user_id: int,
):
    message = (
        db.query(Message)
        .filter(Message.id == message_id)
        .first()
    )

    if not message:
        raise ValueError("Message not found")

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == message.conversation_id
        )
        .first()
    )

    if not conversation:
        raise ValueError("Conversation not found")

    # Sirf receiver/read karne wala participant
    if current_user_id not in (
        conversation.user_one_id,
        conversation.user_two_id,
    ):
        raise ValueError(
            "You are not a participant of this conversation"
        )

    # Sender apna message read mark na kare
    if message.sender_id == current_user_id:
        return message

    message.is_read = True

    db.commit()
    db.refresh(message)

    return message
