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
        user_id[0] for user_id in
        get_users_assigned_task(id) if len(user_id) > 0
    ]
    return TaskInDB(
        **db_result,
        assignees_id=assignees_id,
    )


def as_UserDB(db_result: dict) -> UserInDB:
    id: int = db_result.get("id")

    assigned_tasks = [
        task_id[0] for task_id in
        get_tasks_assigned_user(id) if len(task_id) > 0
    ]
    return UserInDB(
        **db_result,
        hashed_password=db_result.get("password"),
        assigned_tasks=assigned_tasks,
    )


def as_CommentDB(db_result: dict) -> CommentInDB:
    return CommentInDB(**db_result)


def as_ChatDB(db_result: dict) -> ChatInDB:
    return ChatInDB(**db_result)


def as_GroupDB(db_result: dict) -> GroupInDB:
    return GroupInDB(**db_result)


def as_TagDB(db_result: dict) -> TagInDB:
    id = db_result.get("id")

    tasks = [task_id[0] for task_id in get_tasks_with_tag(id)]

    return TagInDB(**db_result, tasks=tasks)
