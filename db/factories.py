from typing import Tuple

from models.task import TaskInDB, TaskStatus


def as_TaskDB(db_result: Tuple) -> TaskInDB:
    print(db_result)
    id, title, description, \
        created_at, updated_at, completed_at, \
        status, assigner_id = db_result
    return TaskInDB(
        id=id,
        title=title,
        description=description,
        created_at=created_at,
        updated_at=updated_at,
        completed_at=completed_at,
        status=TaskStatus(status),
        assigner_id=assigner_id,
    )
