from db.database import connect_to_database


def is_admin(user_id: int, group_id: int):
    with connect_to_database() as con:
        cur = con.cursor()

        SQLQUERY = """
        SELECT * FROM group_admins
        WHERE user_id = %s and group_id = %s
        """
        PARAM = (user_id, group_id)

        cur.execute(SQLQUERY, PARAM)

        if (cur.fetchone() is not None):
            return True

        return False


def promote(user_id: int, group_id: int):
    with connect_to_database() as con:
        cur = con.cursor()

        SQLQUERY = """
        INSERT INTO group_admins (user_id, group_id)
        VALUES(%s,%s)
        """
        PARAM = (user_id, group_id)

        cur.execute(SQLQUERY, PARAM)
        con.commit()


def demote(user_id: int, group_id: int):
    with connect_to_database() as con:
        cur = con.cursor()

        SQLQUERY = """
        DELETE FROM group_admins
        WHERE user_id = %s AND group_id = %s
        """
        PARAM = (user_id, group_id)

        cur.execute(SQLQUERY, PARAM)
        con.commit()


def show_all_admins(group_id: int, limit: int, offset: int):
    with connect_to_database() as con:
        cur = con.cursor(dictionary=True)

        SQLQUERY = """
        SELECT * FROM users
        WHERE id = ANY ( SELECT user_id FROM group_admins WHERE group_id = %s )
        LIMIT %s
        OFFSET %s
        """
        PARAM = (group_id, limit, offset)

        cur.execute(SQLQUERY, PARAM)

        return cur.fetchall()
