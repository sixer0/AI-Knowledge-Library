# -*- coding: utf-8 -*-
"""Ronde sysman 16-10: cek skema kanban.db + sensus status (read-only)."""
import os, sqlite3, time, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
con = sqlite3.connect(str(HOME / 'kanban.db'))
con.row_factory = sqlite3.Row
cur = con.cursor()

print("TABLES:", [r[0] for r in cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")])
for t in ('tasks', 'task_events', 'task_comments', 'task_runs', 'task_links'):
    try:
        cols = [r[1] for r in cur.execute(f"PRAGMA table_info({t})")]
        print(f"COLS {t}: {cols}")
    except Exception as e:
        print(f"COLS {t}: ERR {e}")

now = int(time.time())
print("\nSTATUS SENSUS:")
for r in cur.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"  {r['status']}: {r['n']}")
print("OPEN BY BOARD:")
for r in cur.execute("SELECT board, COUNT(*) n FROM tasks WHERE status IN ('todo','blocked','review','running') GROUP BY board"):
    print(f"  {r['board']}: {r['n']}")
try:
    mx = cur.execute("SELECT MAX(created_at) m FROM task_events").fetchone()['m']
    print(f"\nBOARD ALIVE: event terakhir {int((now-mx)/60)} menit lalu; total events={cur.execute('SELECT COUNT(*) c FROM task_events').fetchone()['c']}")
except Exception as e:
    print("EVENT QUERY ERR", e)
