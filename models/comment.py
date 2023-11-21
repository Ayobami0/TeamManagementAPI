from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CommentBase(BaseModel):
    message: str
    poster_id: int
    task_id: int


class Comment(CommentBase):
    pass


class CommentInDB(CommentBase):
    posted_at: datetime
    edited_at: Optional[datetime] = None
    id: int
