
from fastapi import HTTPException
from db.database import connect_to_database
from models.chats import Chat, ChatInDB


def get_chat_by_id_in_db(chat_id: int):
    with connect_to_database() as con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT * FROM chats WHERE id = %s
            """,
            (chat_id,),
        )
        return cur.fetchone()


def send_chat_to_group_in_db(chat: Chat):
    with connect_to_database() as con:
        cur = con.cursor()
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
    limit: int,
    offset: int,
):
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)
        try:
            cur.execute(
                """
                    SELECT * from chats LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            return cur.fetchall()
        except Exception:
            con.rollback()
            raise HTTPException(500, "An Error Occured")
