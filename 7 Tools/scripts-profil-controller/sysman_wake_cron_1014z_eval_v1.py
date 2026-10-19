# Sensus kartu WAKE ronde cron 14-10-z: kelompok per tenant, status, umur event, ACK.
import sqlite3, time, json, sys

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
IDS = """t_002af121 t_0311d1e4 t_050a75ff t_0bf0854c t_1168e59f t_14e7030f t_153594d4
t_1c98456a t_23f7da05 t_2543fb8f t_2ae211bb t_2d32e7c8 t_2e0e92d4 t_30dd071c t_34bf2edc
t_3782b61a t_397be920 t_46ff8be6 t_483b2d91 t_4d7a1691 t_4edfcf3a t_5831a79d t_60ed37fa
t_64328060 t_674377e1 t_68d1d8be t_7391c81b t_760e7792 t_77a9bcd3 t_799a1879 t_8b90e854
t_8d618268 t_93c6bec3 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc t_a064e4cc
t_a37d190b t_a3e70bf1 t_a48e52d1 t_a4b6791b t_a783103d t_a931e1b1 t_aaab1be9 t_b422fa6d
t_b81fea6a t_b9500192 t_ba72c512 t_be219ab7 t_c1d55eef t_c792df45 t_c8784acc t_cb601d70
t_d3cc135a t_d4fca8b3 t_d8480778 t_d9f482ab t_e04bca14 t_e4c7440d t_e5e2e083 t_e8cac74b
t_ec2342d5 t_edb280b5 t_efb6071f t_f9ac1ff2""".split()

now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def cols(table):
    return [r["name"] for r in con.execute(f"PRAGMA table_info({table})")]

tc = cols("tasks")
print("tasks cols:", tc)
ec = cols("task_events")
print("events cols:", ec)
cc = cols("task_comments")
print("comments cols:", cc)

# per-WAKE detail
rows = []
for tid in IDS:
    t = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print("MISSING", tid); continue
    d = dict(t)
    ev = con.execute("SELECT MAX(created_at) m, COUNT(*) n FROM task_events WHERE task_id=?", (tid,)).fetchone()
    cm = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=?", (tid,)).fetchone()["n"]
    kinds = [r["kind"] for r in con.execute("SELECT kind FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (tid,))]
    marker = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["n"]
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
    lapor = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%' OR body LIKE '%LAPOR-SELESAI%')", (tid,)).fetchone()["n"]
    rows.append({
        "id": tid, "status": d.get("status"), "tenant": d.get("tenant"),
        "title": (d.get("title") or "")[:70],
        "assignee": d.get("assignee"),
        "last_ev_age_min": round((now - (ev["m"] or 0)) / 60, 1) if ev["m"] else None,
        "ev_n": ev["n"], "cm_n": cm, "marker": marker, "ack": ack, "lapor": lapor,
        "recent_kinds": kinds,
    })

# group by tenant
from collections import defaultdict
g = defaultdict(list)
for r in rows:
    g[r["tenant"]].append(r)

print("\n=== GROUP BY TENANT ===")
for ten, items in sorted(g.items(), key=lambda kv: -len(kv[1])):
    ages = [i["last_ev_age_min"] for i in items if i["last_ev_age_min"] is not None]
    st = defaultdict(int)
    for i in items: st[i["status"]] += 1
    print(f"\nTENANT={ten!r} n={len(items)} status={dict(st)} age_min[{min(ages) if ages else '-'}..{max(ages) if ages else '-'}]")
    print("  sample titles:", [i["title"][:48] for i in items[:3]])

# whole-board census
print("\n=== BOARD CENSUS ===")
tot = con.execute("SELECT COUNT(*) n FROM tasks").fetchone()["n"]
print("total tasks:", tot)
for r in con.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status"):
    print(" ", r["status"], r["n"])
mx = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
print("last event age min:", round((now - mx) / 60, 1))
print("gave_up events total:", con.execute("SELECT COUNT(*) n FROM task_events WHERE kind='gave_up'").fetchone()["n"])
print("timed_out events total:", con.execute("SELECT COUNT(*) n FROM task_events WHERE kind='timed_out'").fetchone()["n"])

# running cards w/ LAPOR (blind spot)
print("\n=== RUNNING CARDS (blind spot sweep) ===")
q = con.execute("SELECT id, title, tenant FROM tasks WHERE status='running'").fetchall()
print("running count:", len(q))
for r in q:
    lp = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (r["id"],)).fetchone()["n"]
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    hb = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%heartbeat%'", (r["id"],)).fetchone()["n"]
    print(f"  {r['id']} lap={lp} hb={hb} ev_age={(now-ev)/60:.0f}m {r['title'][:50]!r}")
