from typing import List, Union
from pydantic import BaseModel


class TagBase(BaseModel):
    tag_name: str


class TagCreate(TagBase):
    pass


class TagInDB(TagBase):
    id: int
    tasks: Union[List[int], None]
