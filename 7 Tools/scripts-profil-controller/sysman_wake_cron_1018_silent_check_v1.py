#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde senyap 18-10: saksi hidup + sensus kartu blocked (read-only)."""
import os, sqlite3, time, glob

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

def age(ts):
    return round((now - ts) / 60.0, 1) if ts else None

print("-- umur event terbaru (MAX, bukan MIN) --")
for tbl, col in (("task_events", "created_at"), ("task_comments", "created_at")):
    mx = con.execute("SELECT MAX(%s) m FROM %s" % (col, tbl)).fetchone()["m"]
    print("%s max_age_min=%s" % (tbl, age(mx)))

print("-- sensus status buka --")
for r in con.execute("SELECT status, COUNT(*) n FROM tasks WHERE status NOT IN ('done','archived') GROUP BY status"):
    print("%s = %d" % (r["status"], r["n"]))

print("-- kartu blocked: umur event terakhir + rem penutup --")
ids = [r["id"] for r in con.execute(
    "SELECT id FROM tasks WHERE status='blocked' ORDER BY id")]
for tid in ids:
    le = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    lastc = con.execute("SELECT author, substr(replace(body, char(10),' '),1,70) b, created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 1", (tid,)).fetchone()
    mk = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND (body LIKE '%RANTAI-WAKE%' OR body LIKE '%[SYSMAN-CLEANER%')", (tid,)).fetchone()["n"]
    print("%s ev_age=%s marker=%d last=[%s] %s" % (
        tid, age(le), mk,
        (lastc["author"] if lastc else "-"),
        (lastc["b"] if lastc else "(tanpa komentar)")))

print("-- saksi scheduler: mtime cron output --")
base = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes")
for profdir in ("profiles/gsp-system-manager/cron/output", "cron/output"):
    root = os.path.join(base, profdir)
    files = []
    for p in glob.glob(os.path.join(root, "**", "*"), recursive=True):
        if os.path.isfile(p):
            files.append((os.path.getmtime(p), p))
    files.sort(reverse=True)
    for mt, p in files[:3]:
        print("%s min_ago=%.1f" % (p.replace(base, "<H>"), (now - mt) / 60.0))
con.close()
