import sqlite3
import config


def get_connection():
    return sqlite3.connect(config.DATABASE)


def init_db():

    conn = get_connection()
    c = conn.cursor()

    # Queue table
    c.execute("""
    CREATE TABLE IF NOT EXISTS queue(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_id TEXT,
        caption TEXT,
        status TEXT DEFAULT 'pending'
    )
    """)

    # Accounts table
    c.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        status TEXT DEFAULT 'active'
    )
    """)

    # Proxies table
    c.execute("""
    CREATE TABLE IF NOT EXISTS proxies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT,
        status TEXT DEFAULT 'active'
    )
    """)

    conn.commit()
    conn.close()
