from datetime import datetime

from pydantic import BaseModel, ConfigDict


# =========================================================
# CREATE CONVERSATION
# =========================================================

class ConversationCreate(BaseModel):
    user_id: int


# =========================================================
# CONVERSATION RESPONSE
# =========================================================

class ConversationResponse(BaseModel):
    id: int
    user_one_id: int
    user_two_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# SEND MESSAGE
# =========================================================

class MessageCreate(BaseModel):
    conversation_id: int
    message: str


# =========================================================
# MESSAGE RESPONSE
# =========================================================

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    message: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)