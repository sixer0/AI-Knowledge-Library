# Read-only eval of WAKE ids: status, tenant, links, comments (LAPOR/ACK/marker), events.
import sqlite3, json, time, collections, sys

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
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

def cols(table):
    try:
        return [r["name"] for r in con.execute(f"PRAGMA table_info({table})")]
    except Exception:
        return []

print("== tables ==")
tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print(tables)
for t in ("tasks", "task_events", "task_links", "comments", "task_comments"):
    if t in tables:
        print(t, "->", cols(t))

now = int(time.time())
idset = set(IDS)

# --- census per tenant among wake ids + whole board open cards ---
rows = {}
for i in IDS:
    r = con.execute("SELECT * FROM tasks WHERE id=?", (i,)).fetchone()
    if r:
        rows[i] = dict(r)
print("\n== wake ids found:", len(rows), "of", len(IDS))

def fmt_ts(ts):
    if not ts:
        return "-"
    return time.strftime("%m-%d %H:%M", time.localtime(ts))

groups = collections.defaultdict(list)
for i, r in rows.items():
    groups[r.get("tenant")].append(i)

print("\n== groups by tenant ==")
for ten, ids in sorted(groups.items(), key=lambda kv: str(kv[0])):
    st = collections.Counter(rows[i].get("status") for i in ids)
    print(f"tenant={ten!r} n={len(ids)} status={dict(st)}")

# sample titles per tenant
print("\n== sample titles per tenant ==")
for ten, ids in sorted(groups.items(), key=lambda kv: str(kv[0])):
    for i in ids[:3]:
        r = rows[i]
        print(f"  {i} [{r.get('status')}] {str(r.get('title'))[:80]}")

# --- per-card detail: last event, parents, comments LAPOR/ACK/marker ---
print("\n== per-card detail ==")
out = []
for i in IDS:
    r = rows.get(i)
    if not r:
        print(f"{i} NOT-FOUND")
        continue
    ev = con.execute(
        "SELECT kind, MAX(created_at) mx FROM task_events WHERE task_id=? GROUP BY kind ORDER BY mx DESC LIMIT 3",
        (i,),
    ).fetchall()
    evs = [(e["kind"], e["mx"]) for e in ev]
    parents = [x[0] for x in con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (i,))]
    nchild = con.execute("SELECT COUNT(*) FROM task_links WHERE parent_id=?", (i,)).fetchone()[0]
    laps = acks = marks = 0
    last_lap_author = None
    if "comments" in tables:
        ctab, ccol = "comments", "body"
    elif "task_comments" in tables:
        ctab, ccol = "task_comments", "body"
    else:
        ctab, ccol = None, None
    if ctab:
        for c in con.execute(f"SELECT {ccol} b, author FROM {ctab} WHERE task_id=? ORDER BY created_at", (i,)):
            b = c["b"] or ""
            if "LAPOR-SELESAI" in b or "LAPOR-SELESAI" in b.upper():
                laps += 1
                last_lap_author = c["author"]
            if "RANTAI-ACK" in b:
                acks += 1
            if "RANTAI-WAKE done-unacked" in b:
                marks += 1
    d = {
        "id": i,
        "status": r.get("status"),
        "tenant": r.get("tenant"),
        "title": str(r.get("title"))[:70],
        "assignee": r.get("assignee"),
        "created": fmt_ts(r.get("created_at")),
        "completed": fmt_ts(r.get("completed_at")),
        "last_events": [(k, fmt_ts(m), round((now - (m or 0)) / 60.0)) for k, m in evs],
        "parents": parents,
        "nchild": nchild,
        "lapor": laps,
        "ack": acks,
        "wake_marker": marks,
        "lapor_author": last_lap_author,
    }
    out.append(d)
    print(json.dumps(d, ensure_ascii=False))

# --- board sanity (MAX not MIN!) ---
print("\n== board sanity ==")
print("now:", fmt_ts(now))
try:
    mx = con.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
    print("max event age_min:", round((now - mx) / 60.0))
except Exception as e:
    print("events err", e)
print("tasks total:", con.execute("SELECT COUNT(*) FROM tasks").fetchone()[0])
st_all = collections.Counter(r[0] for r in con.execute("SELECT status FROM tasks"))
print("status census ALL:", dict(st_all))
if ctab if False else ("comments" in tables or "task_comments" in tables):
    t2 = "comments" if "comments" in tables else "task_comments"
    print("comments total:", con.execute(f"SELECT COUNT(*) FROM {t2}").fetchone()[0])
