#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sapuan blind-spot: kartu running + LAPOR vs ACK; retry_status VIBE; ronde sebelumnya."""
import os, sqlite3, time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
NOW = int(time.time())
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

print("=== RUNNING CARDS (blind spot) ===")
for t in con.execute("SELECT id,title,status,tenant,created_by,assignee FROM tasks WHERE status='running'"):
    hb = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (t["id"],)).fetchone()["m"]
    nl = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (t["id"],)).fetchone()["c"]
    na = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (t["id"],)).fetchone()["c"]
    lw = con.execute("SELECT author, substr(replace(body,char(10),' '),1,90) b, created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 1", (t["id"],)).fetchone()
    print("%s | %s | tenant=%s | asg=%s | hbAge=%dm | LAPOR=%d ACK=%d" % (
        t["id"], (t["title"] or "")[:70], t["tenant"], t["assignee"], int((NOW-hb)/60) if hb else -1, nl, na))
    if lw:
        print("   lastcom: [%s|%dm] %s" % (lw["author"], int((NOW-lw["created_at"])/60), lw["b"]))

print("\n=== VIBE WRITER RETRY STATE (kolom task_runs) ===")
cols = [r[1] for r in con.execute("PRAGMA table_info(task_runs)")]
print("task_runs cols:", cols)
q = "SELECT ru.task_id, ru.id, ru.outcome, ru.%s FROM task_runs ru JOIN tasks t ON t.id=ru.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND ru.outcome IS NOT NULL ORDER BY ru.task_id, ru.id" % (",".join([c for c in ("retry_status","max_runtime_seconds","ended_at") if c in cols]) or "NULL as x")
rows = con.execute(q).fetchall()
from collections import defaultdict
per = defaultdict(list)
for r in rows:
    per[r["task_id"]].append(r)
print("writer runs per card:", {tid: [(rr["outcome"], rr["retry_status"] if "retry_status" in rr.keys() else "?") for rr in v] for tid, v in list(per.items())[:3]})
tot = defaultdict(int)
for v in per.values():
    for rr in v:
        tot[(rr["outcome"], rr["retry_status"] if "retry_status" in rr.keys() else "?")] += 1
print("VIBE run outcome/retry census:", dict(tot))
print("cards with runs:", len(per))

print("\n=== SCHEDULED STA13-1013 ===")
for t in con.execute("SELECT id,title,status,scheduled_from FROM tasks WHERE status='scheduled'"):
    print(t["id"], t["title"][:60], t["scheduled_from"])
con.close()
