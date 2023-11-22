from mysql.connector import connect
import config


def connect_to_database():
    db = connect(
        host=config.HOSTNAME,
        user=config.USERNAME,
        password=config.PASSWORD,
        database=config.DB_NAME,
        port=config.PORT,
    )
    return db


def init_db():
    with connect_to_database() as con:
        cur = con.cursor()

        # Users Table
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT,
            username VARCHAR(255),
            password VARCHAR(64),
            email VARCHAR(255),
            PRIMARY KEY (id),
            UNIQUE (email)
        )
        """
        )

        # Tasks table
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(500) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            completed_at TIMESTAMP NULL,
            status ENUM('OPEN', 'PROCESSING', 'COMPLETED')
                DEFAULT 'OPEN',
            assigner_id INT,
            group_id INT NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY (assigner_id) REFERENCES users(id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
            FOREIGN KEY (group_id) REFERENCES users(id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        )
        """
        )

        # Comments Table
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS comments (
            id INT AUTO_INCREMENT,
            posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            edited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP,
            task_id INT,
            poster_id INT,
            message VARCHAR(255),
            PRIMARY KEY (id),
            FOREIGN KEY(task_id) REFERENCES tasks(id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
            FOREIGN KEY(poster_id) REFERENCES users(id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        )
        """
        )

        # Tags table
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS tags (
            id INT PRIMARY KEY AUTO_INCREMENT,
            tag_name VARCHAR(255) NOT NULL
        )
        """
        )
        # Groups table
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS `groups` (
            id INT AUTO_INCREMENT,
            name VARCHAR(255),
            description VARCHAR(255),
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INT,
            PRIMARY KEY (id),
            FOREIGN KEY(created_by) REFERENCES users(id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        )
            """
        )

        # TeamChats table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS chats (
                id INT AUTO_INCREMENT,
                group_id INT,
                sender_id INT,
                content VARCHAR(255),
                date_sent TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_edited TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(id),
                FOREIGN KEY (group_id) REFERENCES `groups` (id)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
                FOREIGN KEY (sender_id) REFERENCES users (id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
            )
            """
        )

        # Admin table
        # Contains users with admin rights and the groups where
        # they have those rights.
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS group_admins (
                group_id INT,
                user_id INT,
                CONSTRAINT pk_adminuser PRIMARY KEY
                (
                    user_id,
                    group_id
                ),
                FOREIGN KEY (group_id) REFERENCES `groups` (id)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users (id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
            )
            """
        )

        # Junction tables
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS user_group (
            user_id INT,
            group_id INT,
            CONSTRAINT pk_usertask PRIMARY KEY
            (
                user_id,
                group_id
            ),
            FOREIGN KEY(group_id) REFERENCES `groups`(id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
            FOREIGN KEY(user_id) REFERENCES users(id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        )
        """
        )

        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_task (
            user_id INT,
            task_id INT,
            CONSTRAINT pk_usertask PRIMARY KEY
            (
                user_id,
                task_id
            ),
            FOREIGN KEY(task_id) REFERENCES tasks(id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
            FOREIGN KEY(user_id) REFERENCES users(id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        )
        """)

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS task_tag (
            tag_id INT,
            task_id INT,
            CONSTRAINT pk_tasktag PRIMARY KEY
            (
                tag_id,
                task_id
            ),
            FOREIGN KEY(task_id) REFERENCES tasks(id)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
            FOREIGN KEY(tag_id) REFERENCES tags(id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        )
        """
        )

        con.commit()
