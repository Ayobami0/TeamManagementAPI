from typing import List
from typing_extensions import Annotated
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from mysql.connector.errors import IntegrityError
from db.crud.tags import (
    add_task_to_tag_db,
    create_new_tag,
    delete_tags_from_db,
    read_tag_from_db_by_id,
    read_tags_from_db,
    remove_task_from_tag_db,
)
from db.crud.tasks import get_task_by_id
from db.factories import as_TagDB

from models.tags import TagCreate, TagInDB

tag_router = APIRouter(prefix="/tags", tags=["Tags"])


@tag_router.get("/", response_model=List[TagInDB])
async def get_tags():
    tags = [as_TagDB(tag) for tag in read_tags_from_db()]
    return tags


@tag_router.get("/{id}")
async def get_tag_by_id(id: int):
    tag = read_tag_from_db_by_id(id)

    if tag is not None:
        return as_TagDB(tag)
    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        f"Tag with id {id} not found",
    )


@tag_router.post("/",)
async def add_tag(tag: TagCreate):
    tag_in_db_id = create_new_tag(tag.tag_name)

    if tag_in_db_id is not None:
        tag_in_db = read_tag_from_db_by_id(tag_in_db_id)

        if tag_in_db is not None:
            return as_TagDB(tag_in_db)
    raise HTTPException(
        500,
        f"An error occured in the server",
    )


@tag_router.delete("/")
async def remove_tag(
    tag_ids: Annotated[
        List[int],
        Body(
            embed=True,
            description="List of tags to remove (Max 10)",
        ),
    ],
):
    if len(tag_ids) > 10:
        return JSONResponse(
            {"title": "Provided tags > 10. Limit tags to a maximum of 10"},
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )
    for idx, tag_id in enumerate(tag_ids):
        if read_tag_from_db_by_id(id) is not None:
            delete_tags_from_db(tag_id)
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "title": f"Tag with id {tag_id} not found.",
                    "message": f"The following tags were not added \
{[id for id in tag_ids[idx:]]}",
                },
            )


@tag_router.post("/{tag_id}/tasks/{task_id}")
async def add_task_to_tag(task_id, tag_id):
    if read_tag_from_db_by_id(tag_id) is not None:
        if get_task_by_id(task_id) is not None:
            try:
                add_task_to_tag_db(task_id, tag_id)
            except IntegrityError:
                pass
            return as_TagDB(read_tag_from_db_by_id(tag_id))
        else:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"Tag with id {task_id} not found",
            )
    else:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Tag with id {tag_id} not found",
        )


@tag_router.delete("/{tag_id}/tasks/{task_id}")
async def remove_task_from_tag(task_id, tag_id):
    if read_tag_from_db_by_id(tag_id) is not None:
        if get_task_by_id(task_id) is not None:
            remove_task_from_tag_db(task_id, tag_id)
            return as_TagDB(read_tag_from_db_by_id(tag_id))
        else:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"Tag with id {task_id} not found",
            )
    else:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Tag with id {tag_id} not found",
        )
