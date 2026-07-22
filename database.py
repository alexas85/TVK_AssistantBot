import sqlite3
from pathlib import Path

DB_PATH = Path("tvk_objects.db")  # отдельное имя БД под проект

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('current', 'completed')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_object(name: str, status: str = "current"):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO objects (name, status) VALUES (?, ?)",
        (name, status)
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id

def get_objects(status: str | None = None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if status:
        cur.execute("SELECT id, name, status FROM objects WHERE status = ?", (status,))
    else:
        cur.execute("SELECT id, name, status FROM objects")
    rows = cur.fetchall()
    conn.close()
    return rows
