import os

from mysql.connector import connect

USERNAME = os.environ.get('AZURE_MYSQL_USER', 'root')
PASSWORD = os.environ.get('AZURE_MYSQL_PASSWORD', 'root')
HOSTNAME = os.environ.get('AZURE_MYSQL_HOST', 'localhost')
DB_NAME = os.environ.get('AZURE_MYSQL_NAME', 'test')


def connect_to_database():
    db = connect(
        host=HOSTNAME,
        user=USERNAME,
        password=PASSWORD,
        database=DB_NAME
    )
    return db


def init_db():
    with connect_to_database() as con:
        cur = con.cursor()

        # Users Table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT,
            username VARCHAR(255),
            password VARCHAR(64),
            email VARCHAR(255),
            PRIMARY KEY (id)
        )
        """)

        # Tasks table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(500) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
            completed_at TIMESTAMP NULL,
            status VARCHAR(255) NOT NULL,
            assigner_id INT,
            PRIMARY KEY (id),
            FOREIGN KEY (assigner_id) REFERENCES users(id)
        )
        """)

        # Comments Table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INT AUTO_INCREMENT,
            posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            edited_at TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
            task_id INT,
            poster_id INT,
            PRIMARY KEY (id),
            FOREIGN KEY(task_id) REFERENCES tasks(id),
            FOREIGN KEY(poster_id) REFERENCES users(id)
        )
        """)

        # Tags table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            id INT PRIMARY KEY AUTO_INCREMENT,
            tag_name VARCHAR(255) NOT NULL
        )
        """)

        # Junction tables
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_task (
            user_id INT,
            task_id INT,
            CONSTRAINT pk_usertask PRIMARY KEY
            (
                user_id,
                task_id
            ),
            FOREIGN KEY(task_id) REFERENCES tasks(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS task_tag (
            tag_id INT,
            task_id INT,
            CONSTRAINT pk_tasktag PRIMARY KEY
            (
                tag_id,
                task_id
            ),
            FOREIGN KEY(task_id) REFERENCES tasks(id),
            FOREIGN KEY(tag_id) REFERENCES tags(id)
        )
        """)

        con.commit()
