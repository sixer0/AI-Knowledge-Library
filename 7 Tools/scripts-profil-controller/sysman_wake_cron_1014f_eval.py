#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Evaluasi baris WAKE ronde 14-10 sore (read-only)."""
import os, sqlite3, sys, time, json

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
NOW = int(time.time())

def ro(db):
    con = sqlite3.connect("file:" + db.replace("\\", "/") + "?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA query_only = ON")
    return con

con = ro(DB)

# 1) parse stdin WAKE lines
rows = []
for line in sys.stdin.read().splitlines():
    p = line.split()
    if len(p) == 4 and p[0] == "WAKE":
        rows.append((p[1], p[2], int(p[3])))

ids = sorted(set(r[0] for r in rows))
print("TOTAL_ROWS=%d UNIQUE_CARDS=%d" % (len(rows), len(ids)))

# per-class unique counts
from collections import Counter, defaultdict
cls = Counter(r[1] for r in rows)
print("CLASS_ROWS:", dict(cls))
uniq_by_class = defaultdict(set)
for tid, alasan, umur in rows:
    uniq_by_class[alasan].add(tid)
for k, v in uniq_by_class.items():
    print("UNIQ[%s]=%d" % (k, len(v)))

# 2) card detail
print("\n=== CARD DETAIL ===")
for tid in ids:
    t = con.execute("SELECT id,title,status,tenant,created_by,assignee,max_runtime_seconds FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print("%s | NOT-IN-DB" % tid); continue
    last_ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    ev_age = int((NOW - last_ev) / 60) if last_ev else -1
    nev = con.execute("SELECT COUNT(*) c FROM task_events WHERE task_id=?", (tid,)).fetchone()["c"]
    ncom = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=?", (tid,)).fetchone()["c"]
    # runs summary
    runs = con.execute("SELECT outcome, COUNT(*) c, MAX(COALESCE(ended_at,started_at)) mx FROM task_runs WHERE task_id=? GROUP BY outcome", (tid,)).fetchall()
    rs = ";".join("%s=%s(age%dm)" % (r["outcome"], r["c"], int((NOW-r["mx"])/60) if r["mx"] else -1) for r in runs)
    # parents
    par = con.execute("SELECT p.parent_id, t2.status FROM task_links l JOIN tasks p ON p.id=l.child_id JOIN tasks t2 ON t2.id=p.parent_id WHERE l.child_id=?", (tid,)).fetchall() if False else con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)).fetchall()
    pars = []
    for pr in par:
        pt = con.execute("SELECT status,title FROM tasks WHERE id=?", (pr["parent_id"],)).fetchone()
        pars.append("%s:%s" % (pr["parent_id"], pt["status"] if pt else "?"))
    # children open count
    ch = con.execute("SELECT COUNT(*) c FROM task_links l JOIN tasks t2 ON t2.id=l.child_id WHERE l.parent_id=? AND t2.status NOT IN ('done','archived')", (tid,)).fetchone()["c"]
    print("%s | st=%s | tenant=%s | by=%s | asg=%s | cap=%s | evAge=%dm evN=%d comN=%d | runs[%s] | parents=%s | openKids=%d" % (
        tid, t["status"], t["tenant"], t["created_by"], t["assignee"], t["max_runtime_seconds"], ev_age, nev, ncom, rs, ",".join(pars) or "-", ch))
    print("    TITLE: %s" % (t["title"][:110] if t["title"] else ""))

# 3) last 3 comments per card (author + snippet)
print("\n=== LAST COMMENTS ===")
for tid in ids:
    cs = con.execute("SELECT author, substr(replace(body, char(10),' '),1,160) b, created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 3", (tid,)).fetchall()
    if not cs:
        print("%s | (no comments)" % tid); continue
    for c in cs:
        print("%s | %s | age%dm | %s" % (tid, c["author"], int((NOW-c["created_at"])/60), c["b"]))
    print("---")

# 4) tenant census for tenants seen
print("\n=== TENANT CENSUS ===")
tenants = set()
for tid in ids:
    t = con.execute("SELECT tenant FROM tasks WHERE id=?", (tid,)).fetchone()
    if t and t["tenant"]:
        tenants.add(t["tenant"])
for tn in sorted(tenants):
    st = con.execute("SELECT status, COUNT(*) c FROM tasks WHERE tenant=? GROUP BY status", (tn,)).fetchall()
    print("%s: %s" % (tn, "; ".join("%s=%d" % (r["status"], r["c"]) for r in st)))

con.close()
