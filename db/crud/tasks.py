from typing import Any, List, Optional, Tuple
from db.database import connect_to_database
from models.comment import Comment
from models.task import Task, TaskStatus


############################
# TASK                     #
###########################
def create_new_task(task: Task) -> int:
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
            (
                task.title,
                task.description,
                task.status.value,
                task.assigner_id,
            ),
        )
        con.commit()
        task_id = cur.lastrowid

        if task.assignees_id is not None:
            assign_task(task_id, task.assignees_id)

        return task_id


def get_task_by_id(id: int) -> Tuple:
    with connect_to_database() as con:
        cur = con.cursor()

        cur.execute(
            """
            SELECT * FROM tasks WHERE id = %s
        """,
            (id,),
        )
        result = cur.fetchone()

        return result


def get_all_task(
    limit: int,
    offset: int,
    status: Optional[TaskStatus] = None,
) -> List[Tuple]:
    with connect_to_database() as con:
        SQLTEXT = """SELECT * from tasks """
        PARAM: List[Any] = [limit, offset]

        if status is not None:
            SQLTEXT += """WHERE status = %s """
            PARAM.insert(0, status.value)

        SQLTEXT += """LIMIT %s OFFSET %s"""
        cur = con.cursor()

        cur.execute(SQLTEXT, tuple(PARAM))
        result = cur.fetchall()

        return result


def delete_task_from_db(task_id: int) -> int:
    with connect_to_database() as con:
        SQLTEXT = """DELETE FROM tasks WHERE id = %s"""
        PARAM = (task_id,)

        cur = con.cursor()

        cur.execute(SQLTEXT, tuple(PARAM))
        con.commit()
        return task_id


def update_task_db_status(task_id: int, status: TaskStatus):
    with connect_to_database() as con:
        SQLTEXT = """UPDATE tasks SET status = %s WHERE id = %s"""
        PARAM = (status, task_id)

        cur = con.cursor()
        cur.execute(SQLTEXT, tuple(PARAM))

        con.commit()


def update_task_db_description(task_id: int, description: str):
    with connect_to_database() as con:
        SQLTEXT = """UPDATE tasks SET description = %s WHERE id = %s"""
        PARAM = (description, task_id)

        cur = con.cursor()
        cur.execute(SQLTEXT, tuple(PARAM))

        con.commit()


def update_task_db_title(task_id: int, title: str):
    with connect_to_database() as con:
        SQLTEXT = """UPDATE tasks SET title = %s WHERE id = %s"""
        PARAM = (title, task_id)

        cur = con.cursor()
        cur.execute(SQLTEXT, tuple(PARAM))

        con.commit()


############################
# TASK ASSIGNS            #
###########################
def assign_task_to_user(task_id: int, users_id: List[int]) -> int:
    with connect_to_database() as con:
        SQLTEXT = """
        INSERT INTO user_task (user_id, task_id) VALUES (%s, %s)
        """
        PARAMS = tuple(zip(users_id, [task_id for _ in range(len(users_id))]))

        cur = con.cursor()
        cur.executemany(SQLTEXT, PARAMS)

        con.commit()
        return cur.lastrowid


def unassign_task_from_user(task_id: int, users_id: List[int]) -> int:
    with connect_to_database() as con:
        SQLTEXT = """
        DELETE FROM user_task WHERE users_id = %s AND task_id = %s
        """
        PARAMS = tuple(zip(users_id, [task_id for _ in range(len(users_id))]))

        cur = con.cursor()
        cur.executemany(SQLTEXT, PARAMS)

        con.commit()
        return cur.lastrowid


def get_users_assigned_task(task_id: int) -> List[Tuple]:
    with connect_to_database() as con:
        SQLTEXT = """
            SELECT user_id FROM user_task WHERE task_id = %s
        """
        PARAM = (task_id,)

        cur = con.cursor()
        cur.execute(SQLTEXT, PARAM)

        result = cur.fetchall()

        return result


############################
# TASK COMMENTS            #
###########################
def get_tasks_comments(task_id: int) -> List[Tuple]:
    with connect_to_database() as con:
        SQLTEXT = """
        SELECT * FROM comments WHERE task_id = %s
        """
        PARAM = (task_id,)

        cur = con.cursor()
        cur.execute(SQLTEXT, PARAM)

        result = cur.fetchall()

        return result


def get_task_comments_by_id(comment_id: int) -> Tuple:
    with connect_to_database() as con:
        SQLTEXT = """
        SELECT * FROM comments WHERE id = %s
        """
        PARAM = (comment_id,)

        cur = con.cursor()
        cur.execute(SQLTEXT, PARAM)

        result = cur.fetchone()

        return result


def add_task_comments(comment: Comment) -> int:
    with connect_to_database() as con:
        SQLTEXT = """
        INSERT INTO comments (message, poster_id, task_id) VALUES
        (%s, %s, %s)
        """
        PARAM = (comment.message, comment.sender_id, comment.task_id,)

        cur = con.cursor()
        cur.execute(SQLTEXT, PARAM)

        con.commit()

        return cur.lastrowid


def delete_task_comments(comment_id: int) -> int:
    with connect_to_database() as con:
        SQLTEXT = """
        DELETE FROM comments WHERE id = %s
        """
        PARAM = (comment_id,)

        cur = con.cursor()
        cur.execute(SQLTEXT, PARAM)

        con.commit()

        return cur.lastrowid


def edit_task_comments(comment_id: int, message: str) -> Tuple:
    with connect_to_database() as con:
        SQLTEXT = """
        UPDATE comments SET message = %s WHERE id = comment_id
        """
        PARAM = (message, comment_id,)

        cur = con.cursor()
        cur.execute(SQLTEXT, PARAM)

        con.commit()
        result = cur.fetchone()
        return result
