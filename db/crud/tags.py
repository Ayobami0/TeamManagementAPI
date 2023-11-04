from typing import List
from db.database import connect_to_database


def create_new_tag(tag_name: str) -> int:
    with connect_to_database() as con:
        cur = con.cursor()

        SQLTEXT = "INSERT iNTO tags (tag_name) VAlUES (%s)"
        PARAM = (tag_name,)

        cur.execute(SQLTEXT, PARAM)
        con.commit()

        return cur.lastrowid


def read_tag_from_db_by_id(id) -> tuple:
    with connect_to_database() as con:
        cur = con.cursor()

        SQLTEXT = "SELECT * FROM tags WHERE id = %s"
        PARAM = (id,)

        cur.execute(SQLTEXT, PARAM)
        result = cur.fetchone()

        return result


def read_tags_from_db() -> List[tuple]:
    with connect_to_database() as con:
        cur = con.cursor()

        SQLTEXT = "SELECT * FROM tags"

        cur.execute(SQLTEXT)
        results = cur.fetchall()

        return results


def update_tags_in_db(id, tag_name):
    with connect_to_database() as con:
        cur = con.cursor()

        SQLTEXT = "UPDATE tags SET tag_name = %s WHERE id = %s"
        PARAM = (
            tag_name,
            id,
        )

        cur.execute(SQLTEXT, PARAM)

        con.commit()


def delete_tags_from_db(tag_id: int):
    with connect_to_database() as con:
        cur = con.cursor()

        SQLTEXT = "DELETE FROM tags WHERE id = %s"
        PARAMS = (tag_id, )

        cur.execute(SQLTEXT, PARAMS)

        con.commit()


def get_tasks_with_tag(tag_id) -> List[tuple]:
    with connect_to_database() as con:
        cur = con.cursor()

        SQLTEXT = "SELECT task_id FROM task_tag WHERE tag_id = %s"
        PARAM = (tag_id,)

        cur.execute(SQLTEXT, PARAM)
        result = cur.fetchall()

        return result


def add_task_to_tag_db(task_id, tag_id):
    with connect_to_database() as con:
        cur = con.cursor()

        SQLTEXT = "INSERT INTO task_tag (task_id, tag_id) VAlUES (%s, %s)"
        PARAM = (task_id, tag_id)

        cur.execute(SQLTEXT, PARAM)

        con.commit()


def remove_task_from_tag_db(task_id, tag_id):
    with connect_to_database() as con:
        cur = con.cursor()

        SQLTEXT = "DELETE FROM task_tag WHERE tag_id = %s AND task_id = %s"
        PARAM = (tag_id, task_id)

        cur.execute(SQLTEXT, PARAM)

        con.commit()
