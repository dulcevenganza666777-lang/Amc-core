import sqlite3, json, os
DB = "v14_ceo_brain.db"

def get_own_history():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS videos (id TEXT PRIMARY KEY, title TEXT, style TEXT, retention REAL, views INTEGER, tags TEXT, status TEXT, created_at TIMESTAMP)")
    cur.execute("SELECT style, retention, views, tags FROM videos WHERE status='publicado' LIMIT 10")
    rows = [{"style": r["style"], "retention": r["retention"], "views": r["views"], "tags": json.loads(r["tags"])} for r in cur.fetchall()]
    conn.close()
    return rows

def get_last_7_styles():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT style FROM videos ORDER BY created_at DESC LIMIT 7")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows

def update_hypothesis(hid, confidence, status):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS hypotheses (id TEXT PRIMARY KEY, confidence REAL, status TEXT)")
    cur.execute("INSERT OR REPLACE INTO hypotheses VALUES (?,?,?)", (hid, confidence, status))
    conn.commit()
    conn.close()
