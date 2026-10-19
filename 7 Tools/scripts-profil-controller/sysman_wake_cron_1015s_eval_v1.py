# Round 15-10s (cron mission-wake): evaluate WAKE t_841f18dc class=stalled age=34min, read-only.
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
CARD = "t_841f18dc"
now = int(time.time())

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def age(ts):
    return round((now - int(ts)) / 60.0, 1) if ts else None

r = con.execute("SELECT * FROM tasks WHERE id=?", (CARD,)).fetchone()
if not r:
    print("CARD NOT FOUND")
    raise SystemExit(1)
d = dict(r)
print("=== CARD ===")
for k in ("id","title","status","tenant","assignee","created_by","created_at","started_at","completed_at"):
    if k in d:
        v = d[k]
        if k.endswith("_at") and v:
            print(f"{k}: {v} (age {age(v)} min)")
        else:
            print(f"{k}: {v}")
# body preview
body = d.get("body") or ""
print("BODY[:700]:", body[:700].replace(chr(10), " | "))

print("\n=== LAST EVENTS ===")
for e in con.execute("SELECT kind, created_at, substr(COALESCE(payload,''),1,200) p FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 15", (CARD,)):
    print(f"- {e['kind']} @ age {age(e['created_at'])} min | {e['p']}")

print("\n=== COMMENTS (all) ===")
for c in con.execute("SELECT author, created_at, substr(body,1,400) b FROM task_comments WHERE task_id=? ORDER BY created_at ASC", (CARD,)):
    print(f"- [{c['author']}] age {age(c['created_at'])} min :: {c['b'].replace(chr(10),' | ')[:380]}")

print("\n=== LINKS ===")
cc = con.cursor()
for l in cc.execute("SELECT parent_id, child_id FROM task_links WHERE parent_id=? OR child_id=?", (CARD, CARD)):
    pid, cid = l["parent_id"], l["child_id"]
    other = cid if pid == CARD else pid
    st = cc.execute("SELECT status, title FROM tasks WHERE id=?", (other,)).fetchone()
    role = "PARENT" if pid == CARD else "CHILD"
    print(f"- {role} {other} status={st['status'] if st else '?'} title={(st['title'][:80] if st else '')}")

tenant = d.get("tenant")
if tenant:
    print(f"\n=== TENANT CENSUS ({tenant}) ===")
    rows = [dict(row) for row in cc.execute("SELECT id, status, title, assignee FROM tasks WHERE tenant=? ORDER BY created_at", (tenant,))]
    st = {}
    for row in rows:
        st.setdefault(row["status"], []).append(row)
    for s, lst in sorted(st.items()):
        print(f"- {s}: {len(lst)}")
    print("\n--- open cards detail (todo/blocked/in_progress/running/parked) ---")
    for row in rows:
        if row["status"] not in ("done","cancelled","archived"):
            le = cc.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (row["id"],)).fetchone()["m"]
            ncom = cc.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=?", (row["id"],)).fetchone()[0]
            print(f"- {row['id']} [{row['status']}] lastev={age(le)}m com={ncom} assignee={row['assignee']} :: {row['title'][:90]}")

print("\n=== BOARD SANITY ===")
mx = con.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
print(f"last board event age: {age(mx)} min")
print("status census:", dict((row[0], row[1]) for row in con.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")))
con.close()
