#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde 14-Oct pagi: (A) status orang tua GSF-23 + sensus tenant GSF-1012 & AIE26SAT,
(B) sapuan blind-spot: kartu running dengan LAPOR-SELESAI tanpa ACK,
(C) sensus RANTAI-ACK per kartu untuk butir done-unacked. Read-only."""
import os
import sqlite3
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())


def age(ts):
    return round((now - ts) / 60.0, 1)


print("### A. ORANG TUA GSF-23")
for pid in ("t_0178294e", "t_9a813cbb"):
    r = con.execute("SELECT id,status,title,assignee FROM tasks WHERE id=?", (pid,)).fetchone()
    if r:
        print("  %s [%s] %s | %s" % (r["id"], r["status"], (r["title"] or "")[:80], r["assignee"]))
    else:
        print("  %s TIDAK ADA" % pid)

print("\n### B. SENSUS TENANT GSF-1012 (status + jumlah ACK)")
for r in con.execute("SELECT id,status,title,assignee,completed_at FROM tasks WHERE tenant='GSF-1012' ORDER BY id"):
    ack = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
    lap = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()["n"]
    print("  %-12s %-9s ack=%d lapor=%d %-30s %s" % (r["id"], r["status"], ack, lap, (r["title"] or "")[:60], r["assignee"]))

print("\n### C. KARTU BERKAITAN AIE26SAT (judul/isi/tenant)")
seen = set()
for r in con.execute("SELECT id,status,title,assignee,tenant,created_at FROM tasks WHERE title LIKE '%AIE26%' OR tenant LIKE '%AIE26%' ORDER BY created_at"):
    seen.add(r["id"])
    print("  %-12s %-9s tenant=%-14s %-24s %s (%s mnt)" % (
        r["id"], r["status"], r["tenant"], r["assignee"], (r["title"] or "")[:70], age(r["created_at"])))
print("  total kartu = %d" % len(seen))

print("\n### D. BLIND SPOT: kartu running (umur heartbeat vs LAPOR vs ACK)")
rows = list(con.execute("SELECT id,status,title,assignee,tenant,started_at FROM tasks WHERE status='running' ORDER BY started_at"))
print("  jumlah running = %d" % len(rows))
for r in rows:
    hb = con.execute("SELECT MAX(created_at) AS m FROM task_events WHERE task_id=? AND kind='heartbeat'", (r["id"],)).fetchone()["m"]
    lap = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR:%')", (r["id"],)).fetchone()["n"]
    ack = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
    print("  %-12s %-9s hb=%-8s lap=%d ack=%d %-22s %s" % (
        r["id"], r["status"], (str(age(hb)) + "m") if hb else "-", lap, ack, r["assignee"], (r["title"] or "")[:60]))

print("\n### E. SANITASI PAPAN (anti sehat-palsu)")
tot = con.execute("SELECT COUNT(*) AS n FROM tasks").fetchone()["n"]
ev = con.execute("SELECT MAX(created_at) AS m FROM task_events").fetchone()["m"]
cm = con.execute("SELECT COUNT(*) AS n FROM task_comments").fetchone()["n"]
st = dict((r["status"], r["n"]) for r in con.execute("SELECT status, COUNT(*) AS n FROM tasks GROUP BY status"))
print("  tasks=%d comments=%d event_terakhir=%s mnt status=%s" % (tot, cm, age(ev), st))
