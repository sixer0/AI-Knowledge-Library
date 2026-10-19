#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Drill ronde 2: status akhir kartu timed_out + komentar terakhir + umur run cron."""
import sqlite3, os, pathlib, time

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
con = sqlite3.connect(HOME / 'kanban.db')
con.row_factory = sqlite3.Row
cur = con.cursor()
now = int(time.time())

ids = ['t_dee16014','t_8e5e944b','t_9013fbb0','t_5380e510','t_c30bce13','t_4197bb1e']
print("== Status akhir kartu timed_out ==")
for i in ids:
    r = cur.execute("SELECT id,status,assignee,completed_at FROM tasks WHERE id=?", (i,)).fetchone()
    d = dict(r) if r else {'id': i, 'status': 'TIDAK-DITEMUKAN'}
    if d.get('completed_at'):
        d['completed'] = time.strftime('%d-%m %H:%M', time.localtime(d['completed_at']))
    print(d)

print("\n== Run terakhir per kartu timed_out (semua outcome) ==")
for r in cur.execute("""
  SELECT task_id, outcome, datetime(ended_at,'unixepoch','localtime') ended
  FROM task_runs WHERE task_id IN (%s) ORDER BY ended_at DESC LIMIT 14
""" % ",".join("?"*len(ids)), ids):
    print(dict(r))

print("\n== Umur event terminal kartu running t_9dcf333d ==")
for r in cur.execute("SELECT kind, datetime(created_at,'unixepoch','localtime') ts FROM task_events WHERE task_id='t_9dcf333d' ORDER BY created_at DESC LIMIT 6"):
    print(dict(r))
