import sqlite3

DB = "v14_ceo_brain.db"


def save_cycle(state):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cycles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        )
    """)

    cur.execute("INSERT INTO cycles (data) VALUES (?)", (str(state),))

    conn.commit()
    conn.close()
