from db.crud.tags import get_tasks_with_tag
from db.crud.tasks import get_users_assigned_task
from db.crud.users import get_tasks_assigned_user
from models.chats import ChatInDB
from models.comment import CommentInDB
from models.group import GroupInDB
from models.tags import TagInDB

from models.task import TaskInDB
from models.user import UserInDB


def as_TaskDB(db_result: dict) -> TaskInDB:
    id: int = db_result.get("id")

    assignees_id = [
        user_id.get('user_id') for user_id in
        get_users_assigned_task(id)
    ]
    return TaskInDB(
        assignees_id=assignees_id,
        **db_result,
    )


def as_UserDB(db_result: dict) -> UserInDB:
    return UserInDB(
        **db_result,
    )


def as_CommentDB(db_result: dict) -> CommentInDB:
    return CommentInDB(**db_result)


def as_ChatDB(db_result: dict) -> ChatInDB:
    return ChatInDB(**db_result)


def as_GroupDB(db_result: dict) -> GroupInDB:
    return GroupInDB(**db_result)


def as_TagDB(db_result: dict) -> TagInDB:
    id = db_result.get("id")

    tasks = [task_id.get('task_id') for task_id in get_tasks_with_tag(id)]

    return TagInDB(**db_result, tasks=tasks)
