# -*- coding: utf-8 -*-
"""Round sanity 2026-10-15 cron: liveness via MAX events + reconcile empty scan vs loose tools."""
import sqlite3, time, os, importlib.util

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

now = int(time.time())
r = cur.execute("SELECT MAX(created_at) m, COUNT(*) n FROM task_events").fetchone()
print("events_total=%d newest_event_age_min=%.1f" % (r["n"], (now - r["m"]) / 60.0))
r = cur.execute("SELECT MAX(created_at) m, COUNT(*) n FROM task_comments").fetchone()
print("comments_total=%d newest_comment_age_min=%.1f" % (r["n"], (now - r["m"]) / 60.0))
r = cur.execute("SELECT COUNT(*) n FROM tasks WHERE status NOT IN ('done','archived')").fetchone()
print("open_tasks=%d" % r["n"])
for row in cur.execute("SELECT status, COUNT(*) n FROM tasks WHERE status NOT IN ('done','archived') GROUP BY status ORDER BY n DESC"):
    print("  open %s = %d" % (row["status"], row["n"]))

# blocked cards: note + age of last event per card, top by recency of tenant grouping
print("-- blocked cards (status, tenant, title, last_event_age_min, has_fase_token) --")
ids = [x["id"] for x in cur.execute("SELECT id FROM tasks WHERE status='blocked' ORDER BY created_at DESC")]
for tid in ids:
    row = cur.execute("SELECT id,title,tenant,assignee,created_at FROM tasks WHERE id=?", (tid,)).fetchone()
    ev = cur.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    cm = cur.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%[FASE]%'", (tid,)).fetchone()["n"]
    mk = cur.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()["n"]
    print("%s | tenant=%s | ev_age=%s | fase=%d wake_marker=%d | %s" % (
        tid, row["tenant"], ("%.0fm" % ((now - ev) / 60.0)) if ev else "none", cm, mk,
        (row["title"] or "")[:70]))

# running cards blind spot: LAPOR-SELESEI without ACK
print("-- running cards (blind spot check) --")
rows = [dict(x) for x in cur.execute("SELECT id,title,tenant FROM tasks WHERE status='running'")]
if not rows:
    print("  none running")
for row in rows:
    tid = row["id"]
    lap = cur.execute("SELECT COUNT(*) n, MAX(created_at) m FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESEI%')", (tid,)).fetchone()
    ack = cur.execute("SELECT COUNT(*) n, MAX(created_at) m FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()
    print("%s lap=%d ack=%d | %s" % (tid, lap["n"], ack["n"], (row["title"] or "")[:60]))
con.close()
