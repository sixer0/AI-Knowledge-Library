# Read-only eval of WAKE ids: group by tenant, status, parents, ACK/LAPOR comments.
import sqlite3, json, time, collections, sys

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
IDS = """t_002af121 t_0311d1e4 t_050a75ff t_0bf0854c t_0df60358 t_1168e59f t_14e7030f t_153594d4
t_1c98456a t_23f7da05 t_2543fb8f t_2ae211bb t_2d32e7c8 t_2e0e92d4 t_30dd071c t_34bf2edc t_3782b61a
t_397be920 t_46ff8be6 t_483b2d91 t_4d7a1691 t_4edfcf3a t_5831a79d t_60ed37fa t_64328060 t_674377e1
t_68d1d8be t_7391c81b t_760e7792 t_77a9bcd3 t_799a1879 t_8b90e854 t_8d618268 t_93c6bec3 t_95b5b6cb
t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc t_a064e4cc t_a37d190b t_a3e70bf1 t_a48e52d1 t_a4b6791b
t_a783103d t_a931e1b1 t_aaab1be9 t_b422fa6d t_b81fea6a t_b9500192 t_ba72c512 t_be219ab7 t_c1d55eef
t_c792df45 t_c8784acc t_cb601d70 t_d3cc135a t_d4fca8b3 t_d8480778 t_d9f482ab t_e04bca14 t_e4c7440d
t_e5e2e083 t_e8cac74b t_ec2342d5 t_edb280b5 t_efb6071f t_f9ac1ff2""".split()

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# sanity: board alive
r = con.execute("SELECT MAX(created_at) m, COUNT(*) c FROM task_events").fetchone()
print("SANITY events: max_age_min=%.1f total=%d" % ((NOW - r["m"]) / 60.0, r["c"]))
r = con.execute("SELECT COUNT(*) c FROM tasks").fetchone()
print("SANITY tasks:", r["c"])

def cols(cur):
    return [d[0] for d in cur.description]

tcols = cols(con.execute("SELECT * FROM tasks LIMIT 1"))
print("TASK COLS:", tcols)

groups = collections.defaultdict(list)
for tid in IDS:
    row = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not row:
        print("MISSING", tid)
        continue
    d = dict(row)
    ev = con.execute("SELECT kind, MAX(created_at) m FROM task_events WHERE task_id=? GROUP BY kind ORDER BY m DESC LIMIT 3", (tid,)).fetchall()
    ncom = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=?", (tid,)).fetchone()["c"]
    nack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["c"]
    nlap = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (tid,)).fetchone()["c"]
    par = con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)).fetchall()
    kids = con.execute("SELECT child_id FROM task_links WHERE parent_id=?", (tid,)).fetchall()
    rec = {
        "id": tid,
        "title": (d.get("title") or "")[:70],
        "status": d.get("status"),
        "tenant": d.get("tenant"),
        "assignee": d.get("assignee") or d.get("claimed_by"),
        "created_min": round((NOW - (d.get("created_at") or NOW)) / 60),
        "last_ev": [(e["kind"], round((NOW - e["m"]) / 60)) for e in ev],
        "com": ncom, "ack": nack, "lapor": nlap,
        "parents": [p["parent_id"] for p in par],
        "nkids": len(kids),
    }
    key = d.get("tenant") or "(no-tenant)"
    groups[key].append(rec)

print("\n=== GROUPS ===")
for k, v in sorted(groups.items(), key=lambda x: -len(x[1])):
    st = collections.Counter(r["status"] for r in v)
    print("\nTENANT %s : %d cards %s" % (k, len(v), dict(st)))
    for r in v[:6]:
        print("  ", json.dumps(r, ensure_ascii=False))
    if len(v) > 6:
        print("   ... %d more" % (len(v) - 6))
