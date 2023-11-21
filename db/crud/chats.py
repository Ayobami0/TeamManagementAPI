
from fastapi import HTTPException
from db.database import connect_to_database
from models.chats import Chat, ChatInDB


def get_chat_by_id_in_db(chat_id: int):
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)
        cur.execute(
            """
            SELECT * FROM chats WHERE id = %s
            """,
            (chat_id,),
        )
        return cur.fetchone()


def get_all_chats_by_user_id_in_db(user_id: int, limit: int, offset: int):
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)
        cur.execute(
            """
            SELECT * FROM chats WHERE sender_id = %s LIMIT %s OFFSET %s
            """,
            (user_id, limit, offset),
        )
        return cur.fetchall()


def send_chat_to_group_in_db(chat: Chat):
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)
        try:
            cur.execute(
                """
                INSERT INTO chats (sender_id, group_id, content)
                VALUES (%s, %s, %s)
                """,
                (chat.sender_id, chat.group_id, chat.content),
            )
            con.commit()
        except Exception:
            raise HTTPException(500, "An Error Occured")


def update_chat_in_group_in_db(chat: Chat):
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)
        try:
            cur.execute(
                """
                UPDATE chats SET content = %s
                WHERE sender_id = %s AND group_id = %s
                """,
                (chat.content, chat.sender_id, chat.group_id),
            )
            con.commit()
        except Exception:
            raise HTTPException(500, "An Error Occured")


def delete_chat_from_group_in_db(chat: ChatInDB):
    with connect_to_database() as con:
        cur = con.cursor()
        try:
            cur.execute(
                """
                DELETE FROM chats
                WHERE sender_id = %s AND %s = group_id
                """,
                (chat.sender_id, chat.group_id),
            )
            con.commit()
        except Exception:
            raise HTTPException(500, "An Error Occured")


def get_all_chats_in_db(
    group_id: int,
    limit: int,
    offset: int,
):
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)
        cur.execute(
            """
                SELECT * from chats WHERE group_id = %s LIMIT %s OFFSET %s
            """,
            (group_id, limit, offset),
        )
        return cur.fetchall()
