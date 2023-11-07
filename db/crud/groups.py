from typing import List
from fastapi.exceptions import HTTPException
from db.crud.admins import promote
from db.database import connect_to_database
from models.group import GroupCreate, GroupInDB, GroupUpdate


def create_new_group(group: GroupCreate) -> int:
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)
        try:
            cur.execute(
                """
                INSERT INTO groups (
                    name,
                    description,
                    created_by
                ) VALUES (%s, %s, %s)
            """,
                (
                    group.name,
                    group.description,
                    group.created_by,
                ),
            )
            con.commit()
            group_id = cur.lastrowid

            promote(group.created_by, group_id)

            return group_id
        except Exception:
            raise HTTPException(500, "An Error Occured")


def get_group_in_db(limit, offset) -> List[dict]:
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)
        try:
            cur.execute(
                """
                SELECT * FROM groups LIMIT %s OFFSET %s
            """,
                (limit, offset),
            )

            return cur.fetchall()
        except Exception:
            raise HTTPException(500, "An Error Occured")


def get_group_by_id_db(group_id: int):
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)
        try:
            cur.execute(
                """
                SELECT * FROM groups WHERE id = %s
            """,
                (group_id,),
            )

            return cur.fetchone()
        except Exception:
            raise HTTPException(500, "An Error Occured")


def update_group_in_db(id, update: GroupUpdate) -> int:
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)
        try:
            cur.execute(
                """
                UPDATE groups
                SET name = %s, description = %s
                WHERE id = %s
            """,
                (update.name, update.description, id),
            )

            con.commit()
            return cur.lastrowid
        except Exception:
            raise HTTPException(500, "An Error Occured")


def remove_group_in_db(group_id: int):
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)
        try:
            cur.execute(
                """
                DELETE from groups
                WHERE id = %s
            """,
                (group_id,),
            )

            con.commit()
        except Exception:
            raise HTTPException(500, "An Error Occured")


def check_user_in_group(group_id, user_id):
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)
        cur.execute(
            """
            SELECT * FROM user_group WHERE user_id = %s AND group_id = %s
        """,
            (user_id, group_id),
        )
        if cur.fetchone():
            return True
        else:
            return False


def add_user_to_group_in_db(group_id, user_id):
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)
        try:
            cur.execute(
                """
                INSERT INTO user_group (user_id, group_id)
                VALUES (name = %s, %s)
            """,
                (user_id, group_id),
            )
        except Exception:
            raise HTTPException(500, "An Error Occured")


def remove_user_from_group_in_db(group_id, user_id):
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)
        try:
            cur.execute(
                """
                DELETE FROM user_group WHERE user_id = %s AND %s = group_id
                """,
                (user_id, group_id),
            )
            con.commit()
        except Exception:
            raise HTTPException(500, "An Error Occured")
