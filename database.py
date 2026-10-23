import sqlite3

DB_NAME = "air_canvas.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drawings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        created_at TEXT,
        color TEXT,
        mode TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_drawing(filename, color, mode, time_str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO drawings (filename, created_at, color, mode) VALUES (?, ?, ?, ?)",
        (filename, time_str, color, mode)
    )

    conn.commit()
    conn.close()

def get_drawings():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM drawings ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()
    return rows
