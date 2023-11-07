from typing import Any, List
from db.database import connect_to_database
from models.user import UserCreate, UserInDB
import importlib


def create_new_user(user: UserCreate) -> int:
    with connect_to_database() as con:
        SQLTEXT = """
            INSERT INTO users (username, password, email)
            VALUES (%s, %s, %s)"""
        get_password_hash = importlib.import_module(
            "security.utils",
        ).get_password_hash

        PARAM = (user.username, get_password_hash(user.password), user.email)

        cur = con.cursor(dictionary=True)

        cur.execute(SQLTEXT, tuple(PARAM))
        con.commit()
        user_id = cur.lastrowid

        return user_id


def read_users_from_db(limit, offset) -> List[dict]:
    with connect_to_database() as con:
        SQLTEXT = """SELECT * from users LIMIT %s OFFSET %s"""
        PARAM: List[Any] = [limit, offset]

        cur = con.cursor(dictionary=True)

        cur.execute(SQLTEXT, tuple(PARAM))
        result = cur.fetchall()

        return result


def read_user_by_id_from_db(user_id: int) -> dict:
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)

        SQLTEXT = """SELECT * FROM users WHERE id = %s"""
        PARAM = (user_id,)

        cur.execute(SQLTEXT, PARAM)

        result = cur.fetchone()

        return result


def read_user_by_email_from_db(email_address: str) -> dict:
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)

        SQLTEXT = """SELECT * FROM users WHERE email = %s"""
        PARAM = (email_address,)

        cur.execute(SQLTEXT, PARAM)

        result = cur.fetchone()

        return result


def delete_user_from_db(user_id: int) -> int:
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)

        SQLTEXT = """DELETE FROM users WHERE id = %s"""
        PARAM = (user_id,)
        cur.execute(SQLTEXT, PARAM)
        con.commit()

        return cur.lastrowid()


def update_user_from_db(user: UserInDB) -> UserInDB:
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)

        SQLTEXT = """
        UPDATE users
        SET username = %s, password = %s, email = %s WHERE id = %s"""
        PARAM = (user.username, user.hashed_password, user.email, user.id)

        cur.execute(SQLTEXT, PARAM)

        con.commit()

        return user


def get_tasks_assigned_user(
    user_id: int,
) -> List[dict]:
    with connect_to_database() as con:
        SQLTEXT = """
            SELECT task_id FROM user_task WHERE user_id = %s LIMIT %s OFFSET %s
        """
        PARAM = (user_id,)

        cur = con.cursor(dictionary=True)
        cur.execute(SQLTEXT, PARAM)

        result = cur.fetchall()

        return result


def get_groups_joined_by_user_in_db(
    user_id: int, limit: int, offset: int
) -> List[dict]:
    with connect_to_database() as con:
        SQLTEXT = """
            SELECT group_id
            FROM user_group
            WHERE user_id = %s
            LIMIT %s OFFSET %s
        """
        PARAM = (user_id, limit, offset)

        cur = con.cursor(dictionary=True)
        cur.execute(SQLTEXT, PARAM)

        result = cur.fetchall()

        return result
