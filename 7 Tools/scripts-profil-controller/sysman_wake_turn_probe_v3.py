# -*- coding: utf-8 -*-
"""Probe terarah read-only: (1) simpul running t_2d7495cc (heartbeat vs plafon),
(2) empat kartu RO01 yang baru menutup senyap tapi tergating tenant kosong
(blind spot rute-4b), (3) kemajuan rantai todo RO01 pasca-penutupan itu."""
import os
import sqlite3
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"),
                  "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = time.time()


def age(ts):
    return "-" if ts is None else f"{(now - float(ts)) / 60:.1f}m"


print("event_cols:", [r[1] for r in con.execute("PRAGMA table_info(task_events)")])
print("run_cols:", [r[1] for r in con.execute("PRAGMA table_info(task_runs)")])

print("\n===== (1) SIMPUL RUNNING =====")
tid = "t_2d7495cc"
t = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
for k in ("id", "status", "assignee", "tenant", "created_by", "started_at",
          "last_heartbeat_at", "current_run_id", "max_runtime_seconds",
          "consecutive_failures", "worker_pid", "block_kind"):
    v = t[k]
    if k.endswith("_at"):
        v = f"{v} (age {age(v)})"
    print(f"   {k} = {v!r}")
print("   -- runs terakhir --")
for r in con.execute("SELECT id,outcome,started_at,ended_at FROM task_runs WHERE task_id=? ORDER BY id DESC LIMIT 4", (tid,)):
    print(f"     run {r['id']} {r['outcome']} start={age(r['started_at'])} lalu end={age(r['ended_at'])} lalu")
print("   -- events terakhir (6) --")
for r in con.execute("SELECT * FROM task_events WHERE task_id=? ORDER BY id DESC LIMIT 6", (tid,)):
    keys = r.keys()
    payload = r["payload"] if "payload" in keys else (r["data"] if "data" in keys else "")
    print(f"     ev {r['id']} kind={r['kind']} {age(r['created_at'])} lalu {str(payload)[:110]}".replace("\n", " "))
print("   -- komentar terakhir (4) --")
for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 4", (tid,)):
    print(f"     c[{c['author']}] {age(c['created_at'])}: {c['body'][:160]}".replace("\n", " "))

print("\n===== (2) KARTU RO01 BARU MENUTUP (tenant kosong) =====")
for tid in ("t_9fbba251", "t_dbd77711", "t_478595eb", "t_a4c8b843"):
    t = con.execute("SELECT id,title,status,tenant,assignee,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    print(f"\n[{tid}] {(t['title'] or '')[:50]} status={t['status']} tenant={t['tenant']!r} assignee={t['assignee']!r} completed={age(t['completed_at'])} lalu")
    for r in con.execute("SELECT * FROM task_events WHERE task_id=? ORDER BY id DESC LIMIT 3", (tid,)):
        keys = r.keys()
        payload = r["payload"] if "payload" in keys else (r["data"] if "data" in keys else "")
        print(f"     ev kind={r['kind']} {age(r['created_at'])} lalu {str(payload)[:100]}".replace("\n", " "))
    for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 2", (tid,)):
        print(f"     c[{c['author']}] {age(c['created_at'])}: {c['body'][:200]}".replace("\n", " "))

print("\n===== (3) RANTAI TODO RO01 =====")
for tid in ("t_fb685c56", "t_52521c3b", "t_414deb88"):
    t = con.execute("SELECT id,title,status,tenant,assignee FROM tasks WHERE id=?", (tid,)).fetchone()
    par = con.execute("SELECT t.id,t.status FROM task_links l JOIN tasks t ON t.id=l.parent_id WHERE l.child_task_id=?", (tid,)).fetchall() if True else []
    st = {}
    for p in par:
        st[p["status"]] = st.get(p["status"], 0) + 1
    print(f"[{tid}] {(t['title'] or '')[:48]} status={t['status']} tenant={t['tenant']!r} parents={len(par)} {st}")
    lastev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    print(f"     last_event age={age(lastest) if False else age(lastev)}")
    for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 2", (tid,)):
        print(f"     c[{c['author']}] {age(c['created_at'])}: {c['body'][:170]}".replace("\n", " "))

print("\n===== (4) CENSUS 24 JAM: event terminal tanpa komentar apa pun =====")
q = """
SELECT t.id, t.status, t.tenant, t.assignee, MAX(e.created_at) ts,
       (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id) nc
FROM task_events e JOIN tasks t ON t.id=e.task_id
WHERE e.kind IN ('completed','blocked') AND e.created_at >= ?
GROUP BY t.id HAVING nc = 0 AND t.status IN ('done','review','blocked')
ORDER BY ts DESC LIMIT 20
"""
for r in con.execute(q, (now - 86400,)):
    print(f"   [{r['id']}] {r['status']} tenant={r['tenant']!r} assignee={r['assignee']!r} terminal_age={age(r['ts'])} komentar=0")
con.close()
