from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ChatBase(BaseModel):
    content: str
    sender_id: int
    group_id: int


class Chat(ChatBase):
    pass


class ChatInDB(ChatBase):
    date_sent: datetime
    date_edited: Optional[datetime] = None
    id: int
