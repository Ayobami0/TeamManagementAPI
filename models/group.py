from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class GroupBase(BaseModel):
    name: str
    description: str
    created_by: Optional[int]


class GroupInDB(GroupBase):
    id: int
    date_created: datetime


class GroupCreate(GroupBase):
    created_by: int


class GroupUpdate(GroupBase):
    pass
