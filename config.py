import sqlite3
import config


def get_connection():
    return sqlite3.connect(config.DATABASE)


def init_db():

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS queue(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id TEXT,
        caption TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS proxies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proxy TEXT
    )
    """)

    conn.commit()
    conn.close()
