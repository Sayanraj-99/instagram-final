import sqlite3
import config

def get_connection():
    conn = sqlite3.connect(config.DATABASE)
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # Accounts table
    c.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            status TEXT DEFAULT 'active'
        )
    """)
    
    # Queue table
    c.execute("""
        CREATE TABLE IF NOT EXISTS queue(
            id INTEGER PRIMARY KEY,
            file_id TEXT,
            caption TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)
    
    # Analytics table
    c.execute("""
        CREATE TABLE IF NOT EXISTS analytics(
            id INTEGER PRIMARY KEY,
            account_id INTEGER,
            post_id TEXT,
            views INTEGER
        )
    """)
    
    conn.commit()
    conn.close()
