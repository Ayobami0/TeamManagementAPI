from typing import List, Optional
from fastapi import APIRouter
from db.crud.tasks import create_new_task, get_all_task, get_task_by_id
from db.factories import as_TaskDB
from models.comment import Comment

from models.task import Task, TaskInDB, TaskStatus
from models.user import User

task_router = APIRouter(tags=["Tasks"], prefix="/tasks")


# Tasks
@task_router.get("/", response_model=List[TaskInDB])
def get_tasks(
    tags: Optional[str] = None,
    status: Optional[TaskStatus] = None,
    limit: int = 10, offset: int = 0,
):
    return get_all_task(limit, offset, tags, status)


@task_router.post("/", response_model=TaskInDB)
def create_task(task: Task):
    task_id = create_new_task(task)
    return as_TaskDB(get_task_by_id(task_id))


@task_router.patch("/{id}/status", response_model=TaskInDB)
def update_task_status(id: int, status: TaskStatus):
    pass


@task_router.patch("/{id}/description", response_model=TaskInDB)
def update_task_description(id: int, description: str):
    pass


@task_router.patch("/{id}/title", response_model=TaskInDB)
def update_task_title(id: int, title: str):
    pass


@task_router.patch("/{id}/assign", response_model=TaskInDB)
def assign_task(id: int, assignees_to_add: List[User]):
    pass


@task_router.delete("/{id}/assign", response_model=TaskInDB)
def unasign_task(id: int, assignees_to_remove: List[User]):
    pass


# Delete Task
@task_router.delete("/{id}")
def delete_task(id: int):
    pass


# Tags
@task_router.delete(
    "/{id}/tags",
)
def get_task_tags(id: int):
    pass


@task_router.delete("/{id}/tags", response_model=TaskInDB)
def remove_task_tags(id: int, tags: List[str]):
    pass


@task_router.patch("/{id}/tags", response_model=TaskInDB)
def add_task_tags(id: int, tags: List[str]):
    pass


# Comments
@task_router.get("/{id}/comments", response_model=Comment)
def get_comment(id: int, comment: Comment):
    pass


@task_router.post("/{id}/comments", response_model=Comment)
def add_comment(id: int, comment: Comment):
    pass


@task_router.delete("/{id}/comments/{comment_id}")
def delete_comment(id: int, comment_id: int):
    pass


@task_router.patch("/{id}/comments/{comment_id}")
def edit_comment(id: int, comment_id: int, edited_text: str):
    pass
