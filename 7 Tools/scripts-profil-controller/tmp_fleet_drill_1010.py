# -*- coding: utf-8 -*-
"""Drill-down fleet health 10-10: rincian timed_out/crashed per profil & kartu, kartu blocked."""
import sqlite3, os, time, pathlib, json

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
con = sqlite3.connect(HOME / 'kanban.db')
cur = con.cursor()
day = int(time.time()) - 86400

print("== 1) run gagal 24j per profil ==")
try:
    rows = list(cur.execute(
        "SELECT profile,outcome,COUNT(*) FROM task_runs WHERE outcome IN ('timed_out','crashed','blocked','gave_up') AND ended_at>? GROUP BY 1,2 ORDER BY 3 DESC", (day,)))
    for r in rows: print("  ", r)
except Exception as e:
    print("   kolom profile tidak ada:", e)
    cols = [c[1] for c in cur.execute("PRAGMA table_info(task_runs)")]
    print("   kolom task_runs:", cols)

print("== 2) kartu dengan >=2 timed_out dalam 24j (kandidat salah pecah) ==")
try:
    rows = list(cur.execute(
        "SELECT task_id,COUNT(*) FROM task_runs WHERE outcome='timed_out' AND ended_at>? GROUP BY 1 HAVING COUNT(*)>=2 ORDER BY 2 DESC", (day,)))
    for tid, n in rows:
        t = cur.execute("SELECT id,title,status,assignee FROM tasks WHERE id=?", (tid,)).fetchone()
        print(f"   x{n} -> {t}")
except Exception as e:
    print("   err:", e)

print("== 3) kartu blocked hidup (detail) ==")
for r in cur.execute("SELECT id,substr(title,1,70),assignee,updated_at FROM tasks WHERE status='blocked' ORDER BY updated_at"):
    print("  ", r)

print("== 4) umur kartu running tertua ==")
for r in cur.execute("SELECT id,substr(title,1,60),assignee,datetime(updated_at,'unixepoch','localtime') FROM tasks WHERE status='running' ORDER BY updated_at LIMIT 8"):
    print("  ", r)
con.close()
