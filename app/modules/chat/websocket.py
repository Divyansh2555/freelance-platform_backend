from typing import Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.session import SessionLocal
from app.modules.chat.model import Conversation, Message


router = APIRouter(
    prefix="/chat",
    tags=["Chat WebSocket"],
)


# =========================================================
# CONNECTED USERS
# =========================================================

# user_id -> websocket connection
active_connections: Dict[int, WebSocket] = {}


# =========================================================
# JWT USER ID
# =========================================================

def get_user_id_from_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise ValueError("Invalid token")

        return int(user_id)

    except (JWTError, ValueError):
        raise ValueError("Invalid or expired token")


# =========================================================
# WEBSOCKET CHAT
# =========================================================

@router.websocket("/ws/{token}")
async def websocket_chat(
    websocket: WebSocket,
    token: str,
):
    await websocket.accept()

    # -----------------------------------------------------
    # AUTHENTICATION
    # -----------------------------------------------------

    try:
        user_id = get_user_id_from_token(token)

    except ValueError:
        await websocket.send_json({
            "type": "error",
            "message": "Invalid or expired token",
        })

        await websocket.close(code=1008)
        return

    # -----------------------------------------------------
    # SAVE CONNECTION
    # -----------------------------------------------------

    active_connections[user_id] = websocket

    try:
        while True:

            # Receive message
            data = await websocket.receive_json()

            receiver_id = data.get("receiver_id")
            message_text = data.get("message")

            if not receiver_id or not message_text:
                await websocket.send_json({
                    "type": "error",
                    "message": "receiver_id and message are required",
                })
                continue

            receiver_id = int(receiver_id)

            # -------------------------------------------------
            # DATABASE
            # -------------------------------------------------

            db: Session = SessionLocal()

            try:
                # Find existing conversation
                conversation = (
                    db.query(Conversation)
                    .filter(
                        (
                            (Conversation.user_one_id == user_id)
                            & (
                                Conversation.user_two_id
                                == receiver_id
                            )
                        )
                        |
                        (
                            (Conversation.user_one_id == receiver_id)
                            & (
                                Conversation.user_two_id
                                == user_id
                            )
                        )
                    )
                    .first()
                )

                # Create conversation if not exists
                if not conversation:
                    conversation = Conversation(
                        user_one_id=user_id,
                        user_two_id=receiver_id,
                    )

                    db.add(conversation)
                    db.commit()
                    db.refresh(conversation)

                # -------------------------------------------------
                # SAVE MESSAGE
                # -------------------------------------------------

                message = Message(
                    conversation_id=conversation.id,
                    sender_id=user_id,
                    message=message_text,
                )

                db.add(message)
                db.commit()
                db.refresh(message)

                response = {
                    "type": "message",
                    "message_id": message.id,
                    "conversation_id": conversation.id,
                    "sender_id": user_id,
                    "receiver_id": receiver_id,
                    "message": message.message,
                    "is_read": message.is_read,
                    "created_at": (
                        message.created_at.isoformat()
                        if message.created_at
                        else None
                    ),
                }

            finally:
                db.close()

            # -------------------------------------------------
            # SEND TO RECEIVER
            # -------------------------------------------------

            receiver_socket = active_connections.get(
                receiver_id
            )

            if receiver_socket:
                await receiver_socket.send_json(response)

            # -------------------------------------------------
            # SEND BACK TO SENDER
            # -------------------------------------------------

            await websocket.send_json(response)

    except WebSocketDisconnect:
        active_connections.pop(user_id, None)

    except Exception:
        active_connections.pop(user_id, None)

        try:
            await websocket.close()
        except Exception:
            pass
