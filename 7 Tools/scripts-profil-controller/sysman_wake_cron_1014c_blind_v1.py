# -*- coding: utf-8 -*-
# Sapuan blind-spot + cek kartu non-VBCB baru + re-scan akhir (ronde 14-10c, read-only)
import importlib.util
import os
import sqlite3
import time

LOCALAPPDATA = os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local")
DB = os.path.join(LOCALAPPDATA, "hermes", "kanban.db")

con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())

# A) semua kartu running: LAPOR vs ACK
run = con.execute("SELECT id,title,tenant,created_by,assignee FROM tasks WHERE status='running'").fetchall()
print("RUNNING cards:", len(run))
for r in run:
    lap = con.execute("SELECT COUNT(*) n, MAX(created_at) m FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (r["id"],)).fetchone()
    ack = con.execute("SELECT COUNT(*) n, MAX(created_at) m FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    hb = int((now - ev) // 60) if ev else -1
    print(r["id"], "|", (r["title"] or "")[:60], "| tenant=", r["tenant"] or "-", "| lap=", lap["n"], "ack=", ack["n"], "| last_ev_min=", hb)

# B) kartu ber-event terminal <=6h tanpa syarat tenant (blind rute-4b)
term = con.execute(
    "SELECT e.task_id id, e.kind, e.created_at, t.status, t.tenant, t.title "
    "FROM task_events e JOIN tasks t ON t.id=e.task_id "
    "WHERE e.kind IN ('completed','blocked') AND e.created_at >= ? AND t.status NOT IN ('running','archived') "
    "ORDER BY e.created_at DESC LIMIT 20", (now - 6 * 3600,)).fetchall()
print("\nTERMINAL events <=6h (tenant-blind):")
seen = set()
for r in term:
    if r["id"] in seen:
        continue
    seen.add(r["id"])
    lap = con.execute("SELECT author, created_at FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%' ORDER BY id DESC LIMIT 1", (r["id"],)).fetchone()
    acks = con.execute("SELECT author, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY id DESC LIMIT 3", (r["id"],)).fetchall()
    mk = con.execute("SELECT 1 FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%' LIMIT 1", (r["id"],)).fetchone()
    print(r["id"], "|", r["kind"], "| st=", r["status"], "| tenant=", r["tenant"] or "-", "| marker=", bool(mk),
          "| lap=", (lap["author"] if lap else "-"), "| ack_authors=", [a["author"] for a in acks])

# C) t_083d8ccf detail (event terbaru papan, tenant NULL)
row = con.execute("SELECT id,title,status,tenant,created_by,assignee FROM tasks WHERE id='t_083d8ccf'").fetchone()
if row:
    print("\nt_083d8ccf:", dict(row))
    cs = con.execute("SELECT author, substr(replace(body,char(10),' '),1,200) s, created_at FROM task_comments WHERE task_id='t_083d8ccf' ORDER BY id DESC LIMIT 4").fetchall()
    for c in cs:
        print("  ", c["author"], "(", int((now - c["created_at"]) // 60), "min):", c["s"])

# D) re-scan kanonis akhir
spec = importlib.util.spec_from_file_location("wake_scan", os.path.join(LOCALAPPDATA, "hermes", "scripts", "gsp_mission_wake_scan.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
f = mod.scan(DB, int(time.time()), mod.DEFAULT_AUTHORS.split(","))
from collections import Counter
cls = Counter(x[1] for x in f)
print("\nRE-SCAN final:", len(f), "rows | classes:", dict(cls))
tn = Counter()
ids = set(x[0] for x in f)
for i in ids:
    r = con.execute("SELECT tenant FROM tasks WHERE id=?", (i,)).fetchone()
    tn[r["tenant"] or "-"] += 1
print("cards by tenant:", dict(tn))
