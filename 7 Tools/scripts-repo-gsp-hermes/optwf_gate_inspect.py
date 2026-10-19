#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""optwf_gate_inspect.py — OPT-WF-F1: inspeksi hanya-baca struktur DB utk gerbang-ekalasi."""
import sqlite3

db = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect('file:' + db.replace('\\', '/') + '?mode=ro', uri=True)
cur = con.cursor()
print('TABLES:', [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")])
try:
    print('subs cols:', [d[1] for d in cur.execute('PRAGMA table_info(kanban_notify_subs)')])
    print('subs count:', cur.execute('SELECT COUNT(*) FROM kanban_notify_subs').fetchone()[0])
    for r in cur.execute('SELECT * FROM kanban_notify_subs LIMIT 5'):
        print('SUB:', r)
except Exception as e:
    print('subs err:', e)
print('tasks cols:', [d[1] for d in cur.execute('PRAGMA table_info(tasks)')])
print('events cols:', [d[1] for d in cur.execute('PRAGMA table_info(task_events)')])
print('event kinds:', list(cur.execute("SELECT kind, COUNT(*) FROM task_events GROUP BY kind")))
for r in cur.execute("SELECT task_id, run_id, payload FROM task_events WHERE kind='blocked' ORDER BY created_at DESC LIMIT 3"):
    print('BLOCKED SAMPLE:', r)
print('review-ish kinds:', list(cur.execute("SELECT DISTINCT kind FROM task_events WHERE kind LIKE '%review%' OR kind LIKE '%request%'")))
has_c = cur.execute("SELECT name FROM sqlite_master WHERE name='task_comments'").fetchone()
print('comments cols:', [d[1] for d in cur.execute('PRAGMA table_info(task_comments)')] if has_c else 'NO task_comments')
# status values used
print('task statuses:', list(cur.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")))
con.close()
