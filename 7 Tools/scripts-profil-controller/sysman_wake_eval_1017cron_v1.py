# Read-only eval of a WAKE card id from root kanban.db (cron-safe, no CLI show)
import sqlite3, sys, time, os

db = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
tid = sys.argv[1] if len(sys.argv) > 1 else "t_7878017f"
now = int(time.time())
con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

t = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
if not t:
    print("NOT-FOUND", tid); sys.exit(0)
print("== TASK ==")
for k in t.keys():
    v = t[k]
    if k == "result":
        v = (str(v)[:1200] + ("...[TRUNC]" if v and len(str(v)) > 1200 else "")) if v else v
    print(f"  {k} = {v}")
for col in ("created_at", "completed_at"):
    v = t[col] if col in t.keys() else None
    if v:
        print(f"  AGE {col}: {round((now-int(v))/60)} min")

print("== EVENTS (last 15) ==")
for e in con.execute("SELECT kind, created_at, payload FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 15", (tid,)):
    age = round((now - int(e["created_at"])) / 60)
    p = (str(e["payload"])[:200]) if e["payload"] else ""
    print(f"  [{age}m] {e['kind']} :: {p}")

print("== COMMENTS (all, newest first) ==")
for c in con.execute("SELECT author, created_at, body FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 30", (tid,)):
    age = round((now - int(c["created_at"])) / 60)
    body = str(c["body"]).replace("\n", " | ")[:400]
    print(f"  [{age}m] {c['author']}: {body}")

print("== MARKER CHECK ==")
mk = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["n"]
print("  existing RANTAI-WAKE done-unacked markers:", mk)

print("== TENANT CENSUS ==")
ten = t["tenant"] if "tenant" in t.keys() else None
if ten:
    rows = con.execute("SELECT id, title, status, tenant, created_by FROM tasks WHERE tenant=?", (ten,)).fetchall()
    print(f"  tenant={ten}: {len(rows)} cards")
    ackq = con.cursor()
    for r in rows:
        nack = ackq.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
        nlap = ackq.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESEI%' OR body LIKE '%LAPOR-SELESAI%')", (r["id"],)).fetchone()["n"]
        nwk = ackq.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (r["id"],)).fetchone()["n"]
        print(f"    {r['id']} [{r['status']}] ack={nack} lapor={nlap} wake={nwk} :: {str(r['title'])[:70]}")
con.close()
