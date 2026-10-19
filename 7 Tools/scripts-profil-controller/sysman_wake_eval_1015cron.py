# Read-only eval of WAKE done-unacked ids from root kanban.db (cron-safe, no CLI show).
import sqlite3, time, json, sys

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
IDS = ["t_02f42f42","t_18720708","t_22eb6962","t_3f4d4d81","t_46a35ff9","t_5adc3df2",
       "t_847af2bf","t_937692a6","t_b02ed4db","t_b4d6303d","t_d86dcc82","t_ee1517ea"]

now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def one(cur, q, args=()):
    cur.execute(q, args)
    return cur.fetchall()

out = []
for tid in IDS:
    r = {}
    r["id"] = tid
    rows = one(con.cursor(), "SELECT * FROM tasks WHERE id=?", (tid,))
    if not rows:
        r["missing"] = True
        out.append(r); continue
    t = dict(rows[0])
    r["status"] = t.get("status")
    r["title"] = (t.get("title") or "")[:110]
    r["tenant"] = t.get("tenant")
    r["assignee"] = t.get("assignee") or t.get("profile") or t.get("claimed_by")
    r["completed_at"] = t.get("completed_at")
    r["age_done_min"] = round((now - t["completed_at"]) / 60) if t.get("completed_at") else None
    evs = one(con.cursor(), "SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,))
    r["last_events"] = [(e["kind"], round((now - e["created_at"]) / 60)) for e in evs]
    # LAPOR comments (latest)
    laps = one(con.cursor(), "SELECT author, created_at, substr(body,1,160) b FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%' ORDER BY created_at DESC LIMIT 2", (tid,))
    r["lapor"] = [(l["author"], round((now - l["created_at"]) / 60), l["b"].replace("\n", " ")[:120]) for l in laps]
    acks = one(con.cursor(), "SELECT author, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY created_at DESC LIMIT 3", (tid,))
    r["acks"] = [(a["author"], round((now - a["created_at"]) / 60)) for a in acks]
    mk = one(con.cursor(), "SELECT created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%' ORDER BY created_at DESC LIMIT 1", (tid,))
    r["marker_age_min"] = round((now - mk[0]["created_at"]) / 60) if mk else None
    ncom = one(con.cursor(), "SELECT COUNT(*) c FROM task_comments WHERE task_id=?", (tid,))[0]["c"]
    r["n_comments"] = ncom
    lastcom = one(con.cursor(), "SELECT author, created_at, substr(body,1,200) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,))
    r["last_comment"] = [(c["author"], round((now - c["created_at"]) / 60), c["b"].replace("\n", " ")[:150]) for c in lastcom]
    out.append(r)

print(json.dumps({"now": now, "rows": out}, ensure_ascii=False, indent=1))

# tenant census for context
tenants = sorted({r.get("tenant") for r in out if r.get("tenant")})
for tn in tenants:
    cs = one(con.cursor(), "SELECT status, COUNT(*) c FROM tasks WHERE tenant=? GROUP BY status", (tn,))
    print("TENANT", tn, {c["status"]: c["c"] for c in cs})
