# -*- coding: utf-8 -*-
"""Evaluasi baris WAKE ronde cron 14-10 (read-only): agregasi per tenant/kelas."""
import sqlite3, time, json, collections, sys

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())

WAKE_IDS = """t_002af121 t_0311d1e4 t_050a75ff t_0bf0854c t_0df60358 t_1168e59f t_14e7030f
t_153594d4 t_1c98456a t_23f7da05 t_2543fb8f t_2ae211bb t_2d32e7c8 t_2e0e92d4 t_30dd071c
t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_483b2d91 t_4d7a1691 t_4edfcf3a t_5831a79d
t_60ed37fa t_64328060 t_674377e1 t_68d1d8be t_7391c81b t_760e7792 t_77a9bcd3 t_799a1879
t_8b90e854 t_8d618268 t_93c6bec3 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc
t_a064e4cc t_a37d190b t_a3e70bf1 t_a48e52d1 t_a4b6791b t_a783103d t_a931e1b1 t_aaab1be9
t_b422fa6d t_b81fea6a t_b9500192 t_ba72c512 t_be219ab7 t_c1d55eef t_c792df45 t_c8784acc
t_cb601d70 t_d3cc135a t_d4fca8b3 t_d8480778 t_d9f482ab t_e04bca14 t_e4c7440d t_e5e2e083
t_e8cac74b t_ec2342d5 t_edb280b5 t_efb6071f t_f9ac1ff2""".split()

db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

def evs(tid):
    return db.execute("SELECT kind,payload,created_at FROM task_events WHERE task_id=? ORDER BY created_at", (tid,)).fetchall()

out = {}
for tid in WAKE_IDS:
    t = db.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        out[tid] = {"missing": True}
        continue
    e = evs(tid)
    last_ev = e[-1] if e else None
    comments = [x for x in e if x["kind"] == "commented"]
    def cbody(x):
        try:
            p = json.loads(x["payload"]) if x["payload"] else {}
        except Exception:
            p = {}
        return (p.get("author") or p.get("created_by") or "?", p.get("body") or p.get("text") or "")
    clist = [cbody(x) for x in comments]
    lap = [i for i,(a,b) in enumerate(clist) if "LAPOR-SELE" in b.upper()]
    ack = [i for i,(a,b) in enumerate(clist) if "RANTAI-ACK" in b.upper()]
    mark = [i for i,(a,b) in enumerate(clist) if "RANTAI-WAKE" in b.upper()]
    parents = db.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)).fetchall()
    pstat = []
    for pr in parents:
        pt = db.execute("SELECT status,title FROM tasks WHERE id=?", (pr["parent_id"],)).fetchone()
        pstat.append((pr["parent_id"], pt["status"] if pt else "?"))
    nchild_open = db.execute("""SELECT COUNT(*) c FROM task_links l JOIN tasks ch ON ch.id=l.child_id
                                WHERE l.parent_id=? AND ch.status NOT IN ('done','cancelled')""", (tid,)).fetchone()["c"]
    nchild_all = db.execute("SELECT COUNT(*) c FROM task_links WHERE parent_id=?", (tid,)).fetchone()["c"]
    runs = db.execute("SELECT id,status,outcome,max_runtime_seconds,last_heartbeat_at,started_at,ended_at,error FROM task_runs WHERE task_id=? ORDER BY started_at DESC LIMIT 3", (tid,)).fetchall()
    out[tid] = {
        "title": t["title"], "status": t["status"], "tenant": t["tenant"],
        "assignee": t["assignee"], "created_by": t["created_by"],
        "created_age_min": round((NOW - (t["created_at"] or NOW))/60),
        "last_ev": (last_ev["kind"], round((NOW-last_ev["created_at"])/60)) if last_ev else None,
        "n_comments": len(clist),
        "last_comments": [(a, b[:110].replace("\n"," ")) for a,b in clist[-3:]],
        "lap_idx": lap, "ack_idx": ack, "marker": bool(mark),
        "parents": pstat, "children": (nchild_all, nchild_open),
        "runs": [(r["status"], r["outcome"], r["max_runtime_seconds"],
                  round((NOW-(r["last_heartbeat_at"] or 0))/60) if r["last_heartbeat_at"] else None,
                  (r["error"] or "")[:80]) for r in runs],
    }

# ringkas per tenant
by_tenant = collections.defaultdict(list)
for tid, d in out.items():
    by_tenant[d.get("tenant") or "(NULL)"].append(tid)

print("=== TENSUS WAKE PER TENANT ===")
for ten, ids in sorted(by_tenant.items(), key=lambda kv:-len(kv[1])):
    st = collections.Counter(out[i]["status"] for i in ids)
    print(f"{ten}: {len(ids)} kartu | status {dict(st)}")
print()
print("=== DETAIL PER KARTU ===")
for tid, d in out.items():
    print(json.dumps({tid: d}, ensure_ascii=False))
