import sqlite3

def create_db():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            create table if not exists users (
                id integer primary key autoincrement,
                username text unique not null,
                password text not null
            )
            """
        )
        conn.commit()
        print("Database and table created")

def authenticate_user(username, password):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            select * from users where username = ? and password = ?
            """,
            (username, password)
        )
        user = cursor.fetchone()
        return user

def create_user(username, password):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        select * from users where username = ?""", (username,))
        if not cursor.fetchone():
            cursor.execute("""
            insert into users (username, password) values (?, ?)
            """, (username, password))
            return authenticate_user(username, password)
        return None