import sqlite3
import config

def get_connection():
    """Create database connection"""
    conn = sqlite3.connect(config.DATABASE)
    return conn

def init_db():
    """Initialize database with all required tables"""
    conn = get_connection()
    c = conn.cursor()
    
    # Accounts table
    c.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            posts_count INTEGER DEFAULT 0,
            total_views INTEGER DEFAULT 0
        )
    """)
    
    # Content queue table
 # One more thing (very important)
# Your database must support status.
#Make sure your queue table has:
status TEXT DEFAULT 'pending'
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            uploaded_at TIMESTAMP,
            account_id INTEGER REFERENCES accounts(id)
        )
    """)
    
    # Analytics table
    c.execute("""
        CREATE TABLE IF NOT EXISTS analytics(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER REFERENCES accounts(id),
            post_id TEXT,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
