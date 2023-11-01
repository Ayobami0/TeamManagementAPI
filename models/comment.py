from typing import Optional
from pydantic import BaseModel

from models.user import User


class CommentBase(BaseModel):
    message: str
    sender: User
    sent_at: str
    edited_at: Optional[str] = None
    task_id: int


class Comment(CommentBase):
    pass


class CommentInDB(BaseModel):
    id: int
