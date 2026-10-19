# Read-only eval of WAKE ids from mission-wake scan (cron ronde 14-10-2026).
import sqlite3, time, json, sys, collections

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
IDS = sys.argv[1:]
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def d(sql, args=()):
    cur = con.cursor()  # separate cursor per query (nested-cursor pitfall)
    cur.execute(sql, args)
    return cur.fetchall()

out = {}
for tid in IDS:
    r = d("SELECT * FROM tasks WHERE id=?", (tid,))
    if not r:
        out[tid] = {"error": "not-found"}
        continue
    t = dict(r[0])
    ev = d("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (tid,))
    coms = d("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 30", (tid,))
    parents = d("SELECT l.parent_id FROM task_links l WHERE l.child_id=?", (tid,))
    pstat = []
    for p in parents:
        pr = d("SELECT status FROM tasks WHERE id=?", (p["parent_id"],))
        pstat.append((p["parent_id"], pr[0]["status"] if pr else "?"))
    kids = d("SELECT c.id, c.status FROM task_links l JOIN tasks c ON c.id=l.child_id WHERE l.parent_id=?", (tid,))
    lap = [c for c in coms if "LAPOR" in (c["body"] or "")]
    ack = [c for c in coms if "RANTAI-ACK" in (c["body"] or "")]
    mk = [c for c in coms if "RANTAI-WAKE" in (c["body"] or "")]
    lastev = ev[0]["created_at"] if ev else None
    out[tid] = {
        "title": (t.get("title") or "")[:90],
        "status": t.get("status"),
        "tenant": t.get("tenant"),
        "creator": t.get("created_by"),
        "assignee": t.get("assignee"),
        "age_min_created": round((now - (t.get("created_at") or now)) / 60),
        "last_ev_kind": ev[0]["kind"] if ev else None,
        "last_ev_age_min": round((now - lastev) / 60) if lastev else None,
        "n_comments": len(coms),
        "lap_authors": sorted({c["author"] for c in lap}),
        "lap_age_min": [round((now - c["created_at"]) / 60) for c in lap][:3],
        "ack_n": len(ack),
        "ack_authors": sorted({c["author"] for c in ack}),
        "marker_n": len(mk),
        "parents": pstat,
        "kids_open": sum(1 for k in kids if k["status"] not in ("done", "cancelled")),
        "kids_total": len(kids),
    }

# census per tenant across whole board (context for mission-level verdict)
cen = d("""SELECT tenant, status, COUNT(*) n FROM tasks
           WHERE tenant IS NOT NULL AND tenant != '' GROUP BY tenant, status""")
tenant_census = collections.defaultdict(dict)
for row in cen:
    tenant_census[row["tenant"]][row["status"]] = row["n"]

alive = d("SELECT MAX(created_at) m, COUNT(*) n FROM task_events")[0]
print(json.dumps({
    "board_alive_last_event_min": round((now - alive["m"]) / 60) if alive["m"] else None,
    "total_events": alive["n"],
    "wake_cards": out,
    "tenant_census": {k: v for k, v in tenant_census.items()},
}, indent=1, ensure_ascii=False))
