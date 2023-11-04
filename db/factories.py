from typing import Tuple
from db.crud.tasks import get_users_assigned_task
from db.crud.users import get_tasks_assigned_user
from models.comment import CommentInDB

from models.task import TaskInDB, TaskStatus
from models.user import UserInDB


def as_TaskDB(db_result: Tuple) -> TaskInDB:
    (
        id,
        title,
        description,
        created_at,
        updated_at,
        completed_at,
        status,
        assigner_id,
    ) = db_result
    assignees_id = [
        user_id[0] for user_id in get_users_assigned_task(id)
        if len(user_id) > 0
    ]
    return TaskInDB(
        id=id,
        title=title,
        description=description,
        created_at=created_at,
        updated_at=updated_at,
        completed_at=completed_at,
        status=TaskStatus(status),
        assigner_id=assigner_id,
        assignees_id=assignees_id,
    )


def as_UserDB(db_result: Tuple) -> UserInDB:
    id, username, hashed_pass, email_addr = db_result

    assigned_tasks = [
        task_id[0] for task_id in get_tasks_assigned_user(id)
        if len(task_id) > 0
    ]
    return UserInDB(
        username=username,
        email=email_addr,
        hashed_password=hashed_pass,
        id=id,
        assigned_tasks=assigned_tasks,
    )


def as_CommentDB(db_result: Tuple) -> CommentInDB:
    id, sent_at, edited_at, task_id, sender_id, message = db_result
    return CommentInDB(
        sent_at=sent_at,
        edited_at=edited_at,
        message=message,
        sender_id=sender_id,
        task_id=task_id,
        id=id,
    )
