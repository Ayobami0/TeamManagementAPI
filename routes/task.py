from typing import List, Optional
from typing_extensions import Annotated
from db.crud.admins import is_admin
from db.crud.groups import get_group_by_id_db
from fastapi import APIRouter, Body, HTTPException, status, Depends
from db.crud.tasks import (
    add_task_comments,
    assign_task_to_user,
    create_new_task,
    delete_task_comments,
    delete_task_from_db,
    edit_task_comments,
    get_all_task,
    get_task_by_id,
    get_task_comments_by_id,
    get_tasks_comments,
    unassign_task_from_user,
    update_task_db_description,
    update_task_db_status,
    update_task_db_title,
)
from db.crud.users import read_user_by_id_from_db
from db.factories import as_CommentDB, as_TaskDB, as_UserDB
from models.comment import Comment, CommentInDB

from models.task import Task, TaskInDB, TaskStatus
from models.user import UserInDB
from routes.user import get_user_by_id
from security.utils import get_current_user

task_router = APIRouter(
    tags=["Tasks"],
    prefix="/tasks",
    dependencies=[Depends(get_current_user)],
)


# Tasks
@task_router.get("", response_model=List[TaskInDB])
async def get_tasks(
    status: Optional[TaskStatus] = None,
    limit: int = 10,
    offset: int = 0,
):
    tasks = [as_TaskDB(task) for task in get_all_task(limit, offset, status)]

    print(tasks)
    return tasks


@task_router.get("/{id}", response_model=TaskInDB)
async def get_task(id: int):
    task = get_task_by_id(id)
    if task is None:
        raise HTTPException(404, f"Task with id {id} not found")

    return as_TaskDB(task)


@task_router.post("", response_model=TaskInDB)
async def create_task(task: Task):
    if get_group_by_id_db(task.group_id) is None:
        raise HTTPException(404, f"Group not found")
    task_id = create_new_task(task)
    task_inDB = get_task_by_id(task_id)

    if task_inDB is None:
        pass

    return as_TaskDB(task_inDB)


@task_router.patch("/{id}/status", response_model=TaskInDB)
async def update_task_status(id: int, status: TaskStatus):
    task = get_task_by_id(id)
    if task is None:
        raise HTTPException(404, f"Task with id {id} not found")

    update_task_db_status(id, status)

    task = as_TaskDB(get_task_by_id(id))

    return task


@task_router.patch("/{id}/description", response_model=TaskInDB)
async def update_task_description(
    id: int,
    description: Annotated[str, Body(embed=True)],
):
    task = get_task_by_id(id)
    if task is None:
        raise HTTPException(404, f"Task with id {id} not found")

    update_task_db_description(id, description)

    task = as_TaskDB(get_task_by_id(id))

    return task


@task_router.patch("/{id}/title", response_model=TaskInDB)
async def update_task_title(title: Annotated[str, Body(embed=True)], id: int):
    task = get_task_by_id(id)
    if task is None:
        raise HTTPException(404, f"Task with id {id} not found")

    update_task_db_title(id, title)

    task = as_TaskDB(get_task_by_id(id))

    return task


@task_router.patch("/{id}/assign", response_model=TaskInDB)
async def assign_task(
    id: int,
    assignees_to_add: Annotated[
        List[int],
        Body(embed=True),
    ],
):
    task = get_task_by_id(id)

    if task is None:
        raise HTTPException(404, f"Task with id {id} not found")

    for user_id in assignees_to_add:
        if get_user_by_id(user_id) is None:
            raise HTTPException(404, f"User with id {id} not found")

    assign_task_to_user(
        task_id=id,
        users_id=assignees_to_add,
    )

    task = as_TaskDB(get_task_by_id(id))

    return task


@task_router.delete("/{id}/unassign", response_model=TaskInDB)
async def unasign_task(
    id: int,
    assignees_to_remove: Annotated[
        List[int],
        Body(embed=True),
    ],
):
    task = get_task_by_id(id)

    if task is None:
        raise HTTPException(404, f"Task with id {id} not found")

    for user_id in assignees_to_remove:
        if read_user_by_id_from_db(user_id) is None:
            raise HTTPException(404, f"User with id {id} not found")

    unassign_task_from_user(
        task_id=id,
        users_id=assignees_to_remove,
    )

    task = as_TaskDB(get_task_by_id(id))

    return task


# Delete Task
@task_router.delete("/{id}")
async def delete_task(id: int):
    task = get_task_by_id(id)

    if task is None:
        raise HTTPException(404, f"Task with id {id} not found")

    delete_task_from_db(id)


# Comments
@task_router.get("/{id}/comments", response_model=List[Comment])
async def get_comment(id: int):
    task = get_task_by_id(id)

    if task is None:
        raise HTTPException(404, f"Task with id {id} not found")

    comments = [as_CommentDB(comment) for comment in get_tasks_comments(id)]

    return comments


@task_router.post("/{id}/comments", response_model=CommentInDB)
async def add_comment(id: int, comment: Comment):
    task = get_task_by_id(id)

    if task is None:
        raise HTTPException(404, f"Task with id {id} not found")

    user = read_user_by_id_from_db(comment.poster_id)

    if user is None:
        raise HTTPException(404, f"User with id {id} not found")

    comment_id = add_task_comments(comment)

    comment_in_DB = get_task_comments_by_id(comment_id)

    return as_CommentDB(comment_in_DB)


@task_router.delete("/{id}/user/{user_id}/comments/{comment_id}")
async def delete_comment(id: int, user_id: int, comment_id: int):
    task = get_task_by_id(id)
    comment = get_task_comments_by_id(comment_id)
    user = read_user_by_id_from_db(user_id)

    if user is None:
        raise HTTPException(404, f"User with id {id} not found")

    if task is None:
        raise HTTPException(404, f"Task with id {id} not found")

    if comment is None:
        raise HTTPException(404, f"Comment with id {id} not found")

    if user_id != as_CommentDB(comment).poster_id or not is_admin(
        user_id, as_TaskDB(task).group_id
    ):
        raise HTTPException(402, f"Not Permitted")

    comment_id_deleted = delete_task_comments(comment_id)

    if comment_id_deleted is None:
        pass


@task_router.patch("/{id}/user/user_id/comments/{comment_id}")
async def edit_comment(id: int, comment_id: int, user_id, edited_text: str):
    task = get_task_by_id(id)
    comment = get_task_comments_by_id(comment_id)
    user = read_user_by_id_from_db(user_id)

    if user is None:
        raise HTTPException(404, f"User with id {id} not found")

    if task is None:
        raise HTTPException(404, f"Task with id {id} not found")

    if comment is None:
        raise HTTPException(404, f"Comment with id {id} not found")

    if user_id != as_CommentDB(comment).poster_id:
        raise HTTPException(402, f"Not Permitted")

    comment_in_DB = edit_task_comments(comment_id, edited_text)

    if comment_in_DB is None:
        return

    return as_CommentDB(comment_in_DB)


@task_router.get("/{id}/users", response_model=List[UserInDB])
async def get_users_assigned_to_task(
    id: int,
    limit: int = 10,
    offset: int = 0,
):
    db_tuple = get_task_by_id(id)
    if db_tuple is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id} does not exist.",
        )
    task = as_TaskDB(db_tuple)
    users_len = len(task.assignees_id)
    users = []

    if not (offset >= users_len):
        for i in range(offset, users_len if users_len < limit else limit):
            users.append(
                as_UserDB(
                    read_user_by_id_from_db(task.assignees_id[i]),
                ),
            )

    return users
