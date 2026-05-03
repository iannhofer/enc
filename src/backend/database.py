import sqlite3
from pathlib import Path

def createDb():
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
    with sqlite3.connect("files.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            create table if not exists files(
                id integer primary key autoincrement,
                userId integer not null,
                filename text not null
            )
            """
        )
def authenticateUser(username, password):
    dbCheck()
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

def createUser(username, password):
    dbCheck()
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        select * from users where username = ?""", (username,))
        if not cursor.fetchone():
            cursor.execute("""
            insert into users (username, password) values (?, ?)
            """, (username, password))
            conn.commit()
            return authenticateUser(username, password)
        return None

def getUserFiles(user_id):
    dbCheck()
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("select filename from files where user_id = ?", (user_id,))
        files = [row[0] for row in cursor.fetchall()]
        return files

def dbCheck():
    if not Path("users.db").is_file():
        createDb()