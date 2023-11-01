import sqlite3


def create_connection():
    con = sqlite3.connect("test.db")
    return con


def init_db():
    cur = create_connection()

    cur.execute(
        """
        CREATE TABLE IF NOT EXIST user(
            id INT PRIMARY KEY AUTO_INCREMENT,
            username,
            email,
            hashed_password
        )
        """
    )
