import sqlite3

def get_connection():
    conn = sqlite3.connect("event.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            college TEXT,
            registered_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()