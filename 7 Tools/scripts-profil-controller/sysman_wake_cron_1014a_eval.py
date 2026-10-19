# Read-only eval of WAKE ids: group by tenant/status, parents, timeouts, comments.
import sqlite3, json, time, collections

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

wake_ids = ["t_002af121","t_0311d1e4","t_050a75ff","t_0bf0854c","t_0df60358","t_1168e59f","t_14e7030f","t_153594d4","t_1c98456a","t_23f7da05","t_2543fb8f","t_2ae211bb","t_2d32e7c8","t_2e0e92d4","t_30dd071c","t_34bf2edc","t_3782b61a","t_397be920","t_46ff8be6","t_483b2d91","t_4d7a1691","t_4edfcf3a","t_5831a79d","t_60ed37fa","t_64328060","t_674377e1","t_68d1d8be","t_7391c81b","t_760e7792","t_77a9bcd3","t_799a1879","t_8b90e854","t_8d618268","t_93c6bec3","t_95b5b6cb","t_99418ea0","t_9bf75422","t_9e457da5","t_9ebc8fbc","t_a064e4cc","t_a37d190b","t_a3e70bf1","t_a48e52d1","t_a4b6791b","t_a783103d","t_a931e1b1","t_aaab1be9","t_b422fa6d","t_b81fea6a","t_b9500192","t_ba72c512","t_be219ab7","t_c1d55eef","t_c792df45","t_c8784acc","t_cb601d70","t_d3cc135a","t_d4fca8b3","t_d8480778","t_d9f482ab","t_e04bca14","t_e4c7440d","t_e5e2e083","t_e8cac74b","t_ec2342d5","t_edb280b5","t_efb6071f","t_f9ac1ff2"]

# schema check
cols = [r["name"] for r in cur.execute("PRAGMA table_info(tasks)")]
print("TASK_COLS:", ",".join(cols))
tl_cols = [r["name"] for r in cur.execute("PRAGMA table_info(task_links)")]
print("LINK_COLS:", ",".join(tl_cols))

def get(tid):
    return cur.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()

groups = collections.defaultdict(list)
for tid in wake_ids:
    r = get(tid)
    if not r:
        print("MISSING", tid); continue
    d = dict(r)
    tenant = d.get("tenant") or "(null)"
    # parents
    parents = [x["parent_id"] for x in cur.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,))]
    pstat = []
    for p in parents:
        pr = get(p)
        pstat.append(f"{p}:{pr['status'] if pr else '?'}")
    # children open count
    kids = [x["child_id"] for x in cur.execute("SELECT child_id FROM task_links WHERE parent_id=?", (tid,))]
    kid_open = sum(1 for k in kids if (dict(get(k)) if get(k) else {}).get("status") not in ("done","cancelled"))
    # comments
    ncom = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=?", (tid,)).fetchone()["c"]
    nlap = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (tid,)).fetchone()["c"]
    nack = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["c"]
    nwake = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()["c"]
    # runs timeouts
    runs = list(cur.execute("SELECT * FROM task_runs WHERE task_id=? ORDER BY id", (tid,)))
    nto = sum(1 for x in runs if x["outcome"]=="timed_out")
    lastev = cur.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    age = (now - lastev["created_at"])//60 if lastev else -1
    groups[tenant].append({
        "id": tid, "title": (d.get("title") or "")[:70], "status": d.get("status"),
        "assignee": d.get("assignee"), "parents": pstat, "kids_open": kid_open,
        "comments": ncom, "lapor": nlap, "ack": nack, "wake_marker": nwake,
        "runs": len(runs), "timeouts": nto, "last_ev": f"{lastev['kind']}@{age}m" if lastev else "-",
        "age_min_created": (now - (d.get("created_at") or now))//60,
    })

for tenant, rows in sorted(groups.items(), key=lambda kv: -len(kv[1])):
    print(f"\n=== TENANT {tenant} ({len(rows)} cards) ===")
    for r in rows:
        print(json.dumps(r, ensure_ascii=False))
con.close()
