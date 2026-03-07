import sqlite3
import config

def get_connection():
    return sqlite3.connect(config.DATABASE)

def init_db():
