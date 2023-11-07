from typing import List
from fastapi import APIRouter, HTTPException, Response, status, Depends
from fastapi.responses import JSONResponse

# from fastapi.responses import JSONResponse
from db.crud.tasks import get_task_by_id
from db.crud.users import (
    create_new_user,
    delete_user_from_db,
    get_groups_joined_by_user_in_db,
    read_user_by_email_from_db,
    read_user_by_id_from_db,
    read_users_from_db,
    update_user_from_db,
)
from db.factories import as_GroupDB, as_TaskDB, as_UserDB
from models.task import Task

from models.user import UserCreate, UserInDB
from security.utils import get_current_user

user_create_router = APIRouter(prefix="/users", tags=["Auth"])
user_router = APIRouter(
    tags=["Users"],
    prefix="/users",
    dependencies=[Depends(get_current_user)],
)


@user_router.get("", response_model=List[UserInDB])
async def get_users(limit: int = 10, offset: int = 0):
    users = [as_UserDB(user) for user in read_users_from_db(limit, offset)]
    return users


@user_router.get("/{id}", response_model=UserInDB)
async def get_user_by_id(id: int):
    db_tuple = read_user_by_id_from_db(id)
    if not db_tuple:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist.",
        )

    user = as_UserDB(db_tuple)

    return user


@user_create_router.post(
    "/create",
    response_model=UserInDB,
)
async def create_user(user: UserCreate, response: Response):
    user_exist = read_user_by_email_from_db(user.email)
    if user_exist is not None:
        response.status_code = status.HTTP_302_FOUND
        return user_exist

    new_user_id = create_new_user(user)

    new_user = read_user_by_id_from_db(new_user_id)

    if new_user is None:
        return JSONResponse({"message": "User was not created"}, 500)

    return as_UserDB(new_user)


@user_router.put("/{id}/update", response_model=UserInDB)
async def update_user(id: int, user: UserInDB):
    db_tuple = read_user_by_id_from_db(user.id)
    if not db_tuple:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist.",
        )

    return update_user_from_db(user)


@user_router.delete("/{id}/delete")
async def delete_user(id: int):
    db_tuple = read_user_by_id_from_db(id)
    if not db_tuple:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist.",
        )

    delete_user_from_db(id)


@user_router.get("/{id}/tasks", response_model=List[Task])
async def get_tasks_assigned_to_user(
    id: int,
    limit: int = 10,
    offset: int = 0,
):
    db_tuple = read_user_by_id_from_db(id)
    if db_tuple is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist.",
        )
    user = as_UserDB(db_tuple)
    tasks_len = len(user.assigned_tasks)
    tasks = []

    if not (offset >= tasks_len):
        for i in range(offset, tasks_len if tasks_len < limit else limit):
            tasks.append(as_TaskDB(get_task_by_id(user.assigned_tasks[i])))

    return tasks


@user_router.get("/{id}/groups", response_model=List[Task])
async def get_groups_joined_by_user(
    id: int,
    limit: int = 10,
    offset: int = 0,
):
    db_tuple = read_user_by_id_from_db(id)
    if db_tuple is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist.",
        )
    groups = [
        as_GroupDB(group)
        for group in get_groups_joined_by_user_in_db(id, limit, offset)
    ]

    return groups

