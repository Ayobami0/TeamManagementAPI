from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter
from models.comment import Comment

from models.task import Task, TaskStatus
from models.user import User

task_router = APIRouter(tags=["Tasks"], prefix="/tasks")


# Tasks
@task_router.get('/', response_model=List[Task])
def get_tasks(tags: Optional[List[str]] = None, ):
    if tags is None:
        return


@task_router.post('/', response_model=Task)
def create_task(task: Task):
    pass


@task_router.patch('/{id}/status', response_model=Task)
def update_task_status(id: int, status: TaskStatus):
    pass


@task_router.patch('/{id}/description', response_model=Task)
def update_task_description(id: int, description: str):
    pass


@task_router.patch('/{id}/title', response_model=Task)
def update_task_title(id: int, title: str):
    pass


@task_router.patch('/{id}/assign', response_model=Task)
def assign_task(id: int, assignees_to_add: List[User]):
    pass


@task_router.delete('/{id}/assign', response_model=Task)
def unasign_task(id: int, assignees_to_remove: List[User]):
    pass


# Delete Task
@task_router.delete('/{id}')
def delete_task(id: int):
    pass


# Tags
@task_router.delete('/{id}/tags', response_model=Task)
def remove_task_tags(id: int, tags: List[str]):
    pass


@task_router.patch('/{id}/tags', response_model=Task)
def add_task_tags(id: int, tags: List[str]):
    pass


# Comments
@task_router.post('/{id}/comments', response_model=Task)
def add_comment(id: int, comment: Comment):
    pass


@task_router.delete('/{id}/comments/{comment_id}')
def delete_comment(id: int, comment_id: int):
    pass


@task_router.patch('/{id}/comments/{comment_id}')
def edit_comment(id: int, comment_id: int, edited_text: str):
    pass
