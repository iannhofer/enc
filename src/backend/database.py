import sqlite3
from pathlib import Path
from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"], deprecated= "auto")


def createDb():
    with sqlite3.connect("storage.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            create table if not exists users (
                id integer primary key autoincrement,
                username text unique not null,
                password text not null
            )""")
        cursor.execute(
            """
            create table if not exists files(
            id integer primary key autoincrement,
            userId integer not null,
            filename text not null
        )""")
        conn.commit()
        print("Database and table created")



def authenticateUser(username, password):
    dbCheck()
    with sqlite3.connect("storage.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            select * from users where username = ?
            """,
            (username,)
        )
        user = cursor.fetchone()
        if user:
            hashedPw = user[2]
            if pwd_context.verify(password, hashedPw):
                return user
        return None

def createUser(username, password):
    dbCheck()
    hashedPw = pwd_context.hash(password)
    with sqlite3.connect("storage.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        select * from users where username = ?""", (username,))
        if not cursor.fetchone():
            cursor.execute("""
            insert into users (username, password) values (?, ?)
            """, (username, hashedPw))
            conn.commit()
            return authenticateUser(username, password)
        return None

def getUserFiles(user_id):
    dbCheck()
    with sqlite3.connect("storage.db") as conn:
        cursor = conn.cursor()
        cursor.execute("select filename from files where userId = ?", (user_id,))
        files = [row[0] for row in cursor.fetchall()]
        return files

def dbCheck():
    if not Path("storage.db").is_file():
        createDb()