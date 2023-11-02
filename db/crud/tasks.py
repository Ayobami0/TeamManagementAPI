from typing import List, Optional
from db.database import connect_to_database
from db.factories import as_TaskDB
from models.task import Task, TaskInDB, TaskStatus


def create_new_task(task: Task):
    with connect_to_database() as con:
        cur = con.cursor()

        cur.execute(
            """
            INSERT INTO tasks (
                title,
                description,
                status,
                assigner_id
            ) VALUES (%s, %s, %s, %s)
        """,
            (task.title, task.description, task.status.value, task.assigner_id)
        )
        con.commit()
        return cur.lastrowid


def get_task_by_id(id: int) -> TaskInDB:
    with connect_to_database() as con:
        cur = con.cursor()

        cur.execute(
            """
            SELECT * from tasks WHERE id = %s
        """,
            (id,),
        )
        result = as_TaskDB(cur.fetchone())

        return result


def get_all_task(
    limit: int,
    offset: int,
    tags: Optional[str] = None,
    status: Optional[TaskStatus] = None,
):
    with connect_to_database() as con:
        cur = con.cursor()

        cur.execute(
            """
            SELECT * from tasks LIMIT %s OFFSET %s
        """,
            (limit, offset),
        )
        result = [as_TaskDB(task) for task in cur.fetchall()]

        return result
