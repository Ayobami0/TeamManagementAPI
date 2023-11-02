from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel


class TaskStatus(Enum):
    COMPLETED = "COMPLETED"
    OPEN = "OPEN"
    PROCESSING = "PROCESSING"


class TaskBase(BaseModel):
    title: str
    description: str
    tags: Optional[List[str]] = None
    status: TaskStatus
    assigner_id: int


class TaskInDB(TaskBase):
    id: int
    updated_at: Optional[datetime] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    assignees_id: Optional[List[int]] = None


class Task(TaskBase):
    pass
