#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Drill read-only ronde 14-10: rincian timed_out 24j, kartu blocked berumur,
satu kartu running, sensus status penuh."""
import sqlite3, os, pathlib, time, json

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
con = sqlite3.connect(HOME / 'kanban.db')
con.row_factory = sqlite3.Row
cur = con.cursor()
now = int(time.time())
day = now - 86400

print("== TIMED_OUT runs 24j ==")
for r in cur.execute("""
  SELECT tr.id AS run_id, tr.task_id, t.title, t.assignee,
         datetime(tr.started_at,'unixepoch','localtime') AS started,
         datetime(tr.ended_at,'unixepoch','localtime') AS ended,
         (tr.ended_at-tr.started_at)/60 AS dur_min
  FROM task_runs tr LEFT JOIN tasks t ON t.id=tr.task_id
  WHERE tr.outcome='timed_out' AND tr.ended_at>? ORDER BY tr.ended_at DESC
""", (day,)):
    print(dict(r))

print("\n== BLOCKED/GAVE_UP/CRASHED runs 24j ==")
for r in cur.execute("""
  SELECT tr.outcome, tr.task_id, t.title, t.assignee, t.status AS card_status,
         datetime(tr.ended_at,'unixepoch','localtime') AS ended
  FROM task_runs tr LEFT JOIN tasks t ON t.id=tr.task_id
  WHERE tr.outcome IN ('blocked','gave_up','crashed') AND tr.ended_at>? ORDER BY tr.ended_at DESC
""", (day,)):
    print(dict(r))

print("\n== SENSUS status tasks ==")
print([dict(r) for r in cur.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status")])

print("\n== Kartu hidup detail (blocked/review/todo/running) ==")
for r in cur.execute("""
  SELECT id, substr(title,1,70) title, assignee, status,
         CAST((?-created_at)/3600.0/24 AS REAL) age_days
  FROM tasks WHERE status IN ('todo','running','blocked','review')
  ORDER BY status, created_at
""", (now,)):
    row = dict(r)
    row['age_days'] = round(row['age_days'], 1)
    print(row)

print("\n== Umur event terakhir papan ==")
r = cur.execute("SELECT MAX(created_at) m FROM task_events").fetchone()
print("last event:", (now - r['m']) / 60.0, "menit lalu" if r['m'] else "TIDAK ADA")
