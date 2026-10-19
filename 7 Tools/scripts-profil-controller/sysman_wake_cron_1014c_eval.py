# -*- coding: utf-8 -*-
"""Evaluasi read-only baris WAKE ronde cron 14-10 (c). DB ro, tanpa tulis."""
import sqlite3, os, time, json, collections

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())

IDS = """t_002af121 t_0311d1e4 t_050a75ff t_0bf0854c t_0df60358 t_1168e59f t_14e7030f
t_153594d4 t_1c98456a t_23f7da05 t_2543fb8f t_2ae211bb t_2d32e7c8 t_2e0e92d4 t_30dd071c
t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_483b2d91 t_4d7a1691 t_4edfcf3a t_5831a79d
t_60ed37fa t_64328060 t_674377e1 t_68d1d8be t_7391c81b t_760e7792 t_77a9bcd3 t_799a1879
t_8b90e854 t_8d618268 t_93c6bec3 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc
t_a064e4cc t_a37d190b t_a3e70bf1 t_a48e52d1 t_a4b6791b t_a783103d t_a931e1b1 t_aaab1be9
t_b422fa6d t_b81fea6a t_b9500192 t_ba72c512 t_bb725705 t_be219ab7 t_c1d55eef t_c792df45
t_c8784acc t_cb601d70 t_d3cc135a t_d4fca8b3 t_d8480778 t_d9f482ab t_e04bca14 t_e4c7440d
t_e5e2e083 t_e8cac74b t_ec2342d5 t_edb280b5 t_efb6071f t_f9ac1ff2""".split()

def age(ts):
    return int((now - ts) / 60) if ts else None

print("== SENSUS PER KARTU ==")
by_tenant = collections.defaultdict(list)
for tid in IDS:
    r = con.execute("SELECT id,title,status,tenant,created_by,assignee,created_at,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    if not r:
        print(tid, "NOT-FOUND"); continue
    ev = con.execute("SELECT kind,MAX(created_at) ts FROM task_events WHERE task_id=? GROUP BY kind ORDER BY ts DESC LIMIT 1", (tid,)).fetchone()
    ncom = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=?", (tid,)).fetchone()["c"]
    lastcom = con.execute("SELECT author,substr(body,1,90) b,created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 1", (tid,)).fetchone()
    par = con.execute("SELECT l.parent_id, t.status FROM task_links l JOIN tasks t ON t.id=l.parent_id WHERE l.child_id=?", (tid,)).fetchall()
    ch_open = con.execute("SELECT COUNT(*) c FROM task_links l JOIN tasks t ON t.id=l.child_id WHERE l.parent_id=? AND t.status NOT IN ('done','archived')", (tid,)).fetchone()["c"]
    runs = con.execute("SELECT outcome,started_at,ended_at FROM task_runs WHERE task_id=? ORDER BY id DESC LIMIT 2", (tid,)).fetchall()
    print(json.dumps({
        "id": tid, "title": (r["title"] or "")[:70], "status": r["status"],
        "tenant": r["tenant"], "by": r["created_by"], "assignee": r["assignee"],
        "age_created_min": age(r["created_at"]),
        "last_ev": (ev["kind"], age(ev["ts"])) if ev else None,
        "ncom": ncom,
        "lastcom": (lastcom["author"], age(lastcom["created_at"]), lastcom["b"]) if lastcom else None,
        "parents": [(p["parent_id"], p["status"]) for p in par],
        "open_children": ch_open,
        "runs": [(x["outcome"], age(x["ended_at"])) for x in runs],
    }, ensure_ascii=False))
    by_tenant[r["tenant"] or "(null)"].append(tid)

print("\n== GROUP TENANT ==")
for tn, ids in sorted(by_tenant.items()):
    st = collections.Counter(con.execute("SELECT status FROM tasks WHERE id=?", (i,)).fetchone()["status"] for i in ids)
    tot = con.execute("SELECT COUNT(*) c FROM tasks WHERE tenant=?", (tn,)).fetchone()["c"] if tn != "(null)" else None
    open_t = con.execute("SELECT COUNT(*) c FROM tasks WHERE tenant=? AND status NOT IN ('done','archived')", (tn,)).fetchone()["c"] if tn != "(null)" else None
    print(tn, "wake=", len(ids), dict(st), "tenant_total=", tot, "tenant_open=", open_t)

print("\n== DETAIL RUN timed_out (cap?) ==")
seen = set()
for tid in IDS:
    rs = con.execute("SELECT id,outcome,started_at,ended_at,max_runtime_seconds,error FROM task_runs WHERE task_id=? AND outcome='timed_out' ORDER BY id DESC", (tid,)).fetchall()
    if rs and tid not in seen:
        seen.add(tid)
        x = rs[0]
        el = int((x["ended_at"] - x["started_at"]) / 60) if x["started_at"] and x["ended_at"] else None
        print(tid, "runs_to=", len(rs), "elapsed_min=", el, "cap_s=", x["max_runtime_seconds"], "err=", (x["error"] or "")[:110].replace("\n", " "))

print("\n== DONE-UNACKED t_d3cc135a ==")
for row in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id='t_d3cc135a' ORDER BY id"):
    print("-", row["author"], age(row["created_at"]), "min ago |", row["body"][:200].replace("\n", " | "))
print("marker?", con.execute("SELECT 1 FROM task_comments WHERE task_id='t_d3cc135a' AND body LIKE '%RANTAI-WAKE done-unacked%' LIMIT 1").fetchone())
con.close()
