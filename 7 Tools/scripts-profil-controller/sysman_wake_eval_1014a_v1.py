# Read-only evaluation of WAKE lines for cron mission-wake round 14-10 (sysman).
import sqlite3, json, time, os, sys

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())

IDS = """t_002af121 t_0311d1e4 t_050a75ff t_0bf0854c t_0df60358 t_1168e59f t_14e7030f
t_153594d4 t_1c98456a t_23f7da05 t_2543fb8f t_2ae211bb t_2d32e7c8 t_2e0e92d4 t_30dd071c
t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_483b2d91 t_4d7a1691 t_4edfcf3a t_5831a79d
t_60ed37fa t_64328060 t_674377e1 t_68d1d8be t_7391c81b t_760e7792 t_77a9bcd3 t_799a1879
t_8b90e854 t_8d618268 t_93c6bec3 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc
t_a064e4cc t_a37d190b t_a3e70bf1 t_a48e52d1 t_a4b6791b t_a783103d t_a931e1b1 t_aaab1be9
t_b422fa6d t_b81fea6a t_b9500192 t_ba72c512 t_be219ab7 t_c1d55eef t_c792df45 t_c8784acc
t_cb601d70 t_d3cc135a t_d4fca8b3 t_d8480778 t_d9f482ab t_e04bca14 t_e4c7440d t_e5e2e083
t_e8cac74b t_ec2342d5 t_edb280b5 t_efb6071f t_f9ac1ff2""".split()

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

def cols(table):
    return [r[1] for r in cur.execute(f"PRAGMA table_info({table})")]

tc = cols("tasks")
print("TASK_COLS:", ",".join(tc))
print("LINK_COLS:", ",".join(cols("task_links")))
print()

def age(ts):
    if ts is None: return None
    return round((NOW - int(ts)) / 60.0, 1)

rows = {}
for tid in IDS:
    r = cur.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if r is None:
        print(f"MISSING {tid}")
        continue
    d = dict(r)
    rows[tid] = d

# group by tenant
from collections import defaultdict
bytenant = defaultdict(list)
for tid, d in rows.items():
    bytenant[d.get("tenant") or "(null)"].append(tid)

for tenant, tids in sorted(bytenant.items()):
    print(f"===== TENANT {tenant} ({len(tids)} cards) =====")
    for tid in sorted(tids):
        d = rows[tid]
        title = (d.get("title") or "")[:90].replace("\n", " ")
        status = d.get("status")
        assignee = d.get("assignee") or d.get("agent") or ""
        created_age = age(d.get("created_at"))
        # last event
        ev = cur.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
        evk = ev["kind"] if ev else "-"
        evage = age(ev["created_at"]) if ev else None
        # parents
        parents = [x[0] for x in cur.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)).fetchall()]
        pstat = []
        for p in parents:
            pr = cur.execute("SELECT status FROM tasks WHERE id=?", (p,)).fetchone()
            pstat.append(f"{p}:{pr['status'] if pr else '?'}")
        # children open count
        kids = [x[0] for x in cur.execute("SELECT child_id FROM task_links WHERE parent_id=?", (tid,)).fetchall()]
        kids_open = sum(1 for k in kids if (cur.execute("SELECT status FROM tasks WHERE id=?", (k,)).fetchone() or {"status":"done"})["status"] not in ("done","cancelled"))
        # comments
        ncmt = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=?", (tid,)).fetchone()["c"]
        lastc = cur.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
        lc = ""
        if lastc:
            lc = f"[{lastc['author']} {age(lastc['created_at'])}m] {(lastc['body'] or '')[:110].replace(chr(10),' ')}"
        mrs = d.get("max_runtime_seconds")
        reason = (d.get("blocked_reason") or d.get("reason") or "")[:100].replace("\n"," ")
        print(f"- {tid} | {status} | {title}")
        print(f"    assignee={assignee} created={created_age}m lastev={evk}@{evage}m parents={pstat} kids_open={kids_open} ncomments={ncms if False else ncmt} maxruntime={mrs} reason={reason}")
        if lc:
            print(f"    lastcomment: {lc}")
    print()
