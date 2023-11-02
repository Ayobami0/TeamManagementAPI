from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CommentBase(BaseModel):
    message: str
    sender_id: int
    task_id: int


class Comment(CommentBase):
    pass


class CommentInDB(BaseModel):
    sent_at: datetime
    edited_at: Optional[datetime] = None
    id: int
