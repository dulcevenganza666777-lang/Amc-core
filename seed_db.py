import sqlite3
from datetime import datetime, timedelta
db = 'knowledge/knowledge_base.db'
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS internal_videos')
cur.execute('DROP TABLE IF EXISTS learning_events')
cur.execute('DROP TABLE IF EXISTS decision_log')
cur.execute('''CREATE TABLE internal_videos (video_id TEXT PRIMARY KEY, title TEXT, style TEXT, views INTEGER, retention REAL, hour_published INTEGER, status TEXT, published_at TEXT)''')
cur.execute('''CREATE TABLE learning_events (id INTEGER PRIMARY KEY, variable TEXT, result TEXT, confidence REAL, impact INTEGER, timestamp TEXT)''')
now = datetime.now()
videos = [('v1_bounce', 'Particles bounce', 'bounce', 1000, 55.2, 23, 'publico', (now - timedelta(days=10)).isoformat()), ('v3_spiral', 'Spiral loop', 'spiral', 982, 71.4, 2, 'publico', (now - timedelta(days=8)).isoformat()), ('v4_spiral_fail', 'Spiral loop FAIL', 'spiral', 25, 15.0, 2, 'no_listado', (now - timedelta(days=7)).isoformat()), ('v5_spiral', 'Spiral loop 3am', 'spiral', 310, 70.0, 3, 'publico', (now - timedelta(days=1)).isoformat())]
cur.executemany('INSERT INTO internal_videos VALUES (?,?,?,?,?,?,?,?)', videos)
events = [('duplicate_spiral', 'Video 4 repitió estilo = 95% riesgo', 0.95, 1, now.isoformat()), ('bounce_winner', 'Video 1 tuvo 1K views y revivió canal', 0.8, 1, now.isoformat()), ('slot_horario', '11pm > 2am x2 views', 0.85, 1, now.isoformat())]
cur.executemany('INSERT INTO learning_events VALUES (NULL,?,?,?,?,?)', events)
conn.commit()
conn.close()
print('[DB] RESETEADA Y SEMBRADA: 4 videos + 3 learning events. Lista para auditar.')
