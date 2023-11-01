from typing import List, Optional
from enum import Enum
from pydantic import BaseModel

from models.comment import Comment
from models.user import User


class TaskStatus(Enum):
    COMPLETED = "COMPLETED"
    OPEN = "OPEN"
    PROCESSING = "PROCESSING"


class TaskBase(BaseModel):
    title: str
    description: str
    created_at: str
    updated_at: Optional[str] = None
    completed_at: Optional[str] = None
    tags: Optional[List[str]] = None
    status: TaskStatus
    assigner: User
    assignees: Optional[List[User]] = None
    comments: Optional[List[Comment]] = None


class TaskInDB(BaseModel):
    id: int


class Task(TaskBase):
    pass
