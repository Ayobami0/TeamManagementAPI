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
    group_id: int
    assigner_id: int
    assignees_id: List[int] = []


class TaskInDB(TaskBase):
    id: int
    updated_at: Optional[datetime] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    status: TaskStatus


class Task(TaskBase):
    pass
