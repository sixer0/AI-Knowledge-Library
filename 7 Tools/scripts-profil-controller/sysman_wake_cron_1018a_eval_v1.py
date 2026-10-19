# Read-only eval of a single WAKE card (done-unacked) from root kanban.db
import sqlite3, sys, time, os

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
CARD = sys.argv[1] if len(sys.argv) > 1 else "t_d663f001"

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def fmt(ts):
    if ts is None:
        return "-"
    try:
        return time.strftime("%Y-%m-%d %H:%M", time.localtime(float(ts))) + f" ({int(time.time()-float(ts))//60}m lalu)"
    except Exception:
        return str(ts)

t = con.execute("SELECT * FROM tasks WHERE id=?", (CARD,)).fetchone()
if not t:
    print("CARD NOT FOUND", CARD); sys.exit(0)
print("=== TASK ===")
for k in ("id","title","status","tenant","assignee","created_by","created_at","completed_at",
          "current_run_id","last_heartbeat_at","block_kind"):
    if k in t.keys():
        v = t[k]
        if k.endswith("_at"):
            v = fmt(v)
        print(f"{k}: {v}")
print("result:", (t["result"] or "")[:1500] if "result" in t.keys() else "-")

print("\n=== LAST 8 EVENTS ===")
for r in con.execute("SELECT kind, created_at, payload FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 8", (CARD,)):
    p = (r["payload"] or "")[:200]
    print(f"- {r['kind']} @ {fmt(r['created_at'])} | {p}")

print("\n=== COMMENTS (all, asc) ===")
rows = list(con.execute("SELECT id, author, created_at, body FROM task_comments WHERE task_id=? ORDER BY created_at ASC", (CARD,)))
print(f"count={len(rows)}")
for r in rows:
    body = (r["body"] or "").replace("\n", " | ")
    print(f"- [{fmt(r['created_at'])}] {r['author']}: {body[:400]}")

# marker check
mk = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (CARD,)).fetchone()["c"]
ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (CARD,)).fetchone()["c"]
lap = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESEI%')", (CARD,)).fetchone()["c"]
print(f"\nMARKER-done-unacked={mk} ACK={ack} LAPOR={lap}")

# children / parents
par = [x["parent_id"] for x in con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (CARD,))]
chi = [x["child_id"] for x in con.execute("SELECT child_id FROM task_links WHERE parent_id=?", (CARD,))]
print("parents:", par)
if chi:
    ph = ",".join("?"*len(chi))
    for r in con.execute(f"SELECT id,status,title FROM tasks WHERE id IN ({ph})", chi):
        print(f"  child {r['id']} [{r['status']}] {r['title'][:80]}")

# tenant census
tn = t["tenant"]
if tn:
    print(f"\n=== TENANT CENSUS {tn} ===")
    ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE tenant=?", (tn,))]
    st = {}
    for i in ids:
        rr = con.execute("SELECT status FROM tasks WHERE id=?", (i,)).fetchone()
        st[rr["status"]] = st.get(rr["status"], 0) + 1
    print("total cards:", len(ids), "status:", st)
    ack0 = 0
    for i in ids:
        c = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (i,)).fetchone()["c"]
        if c == 0:
            ack0 += 1
    print("cards with zero RANTAI-ACK:", ack0)
