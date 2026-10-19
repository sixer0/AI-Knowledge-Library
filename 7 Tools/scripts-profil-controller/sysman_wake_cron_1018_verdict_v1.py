# Ringkasan vonis: semua kartu terbuka ber-koreksi? ada running/todo? blind-spot rute-4b?
import json, sqlite3, subprocess, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

rows = cur.execute("""
    SELECT id, title, status, tenant FROM tasks
    WHERE status NOT IN ('done','archived')
""").fetchall()
ids = [r["id"] for r in rows]

by_status = {}
missing = []
for r in rows:
    by_status[r["status"]] = by_status.get(r["status"], 0) + 1
    lc = cur.execute(
        "SELECT author, body FROM task_comments WHERE task_id=? "
        "ORDER BY created_at DESC LIMIT 1", (r["id"],)
    ).fetchone()
    ok = lc is not None and "[SYSMAN-CLEANER" in lc["body"]
    if not ok:
        missing.append({"id": r["id"], "tenant": r["tenant"], "status": r["status"],
                        "title": (r["title"] or "")[:70],
                        "last_author": (lc["author"] if lc else None),
                        "last_body": (lc["body"][:100].replace("\n", " ") if lc else None)})

print("STATUS CENSUS OPEN:", json.dumps(by_status))
print("OPEN WITHOUT [SYSMAN-CLEANER last-comment:", len(missing))
print(json.dumps(missing, ensure_ascii=False, indent=1))

# Blind spot: kartu running dengan LAPOR tanpa ACK author-lain
run = cur.execute("SELECT id,title,tenant,last_heartbeat_at FROM tasks WHERE status='running'").fetchall()
print("RUNNING cards =", len(run))
for r in run:
    hb = r["last_heartbeat_at"]
    age = round((time.time() - hb) / 60.0, 1) if hb else None
    laps = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (r["id"],)).fetchone()["c"]
    acks = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    print("  RUN", r["id"], "hb_age_min=", age, "lapor=", laps, "ack=", acks, "|", (r["title"] or "")[:60])

# done <=6 jam tanpa ACK (cek rute-4b manual ringan)
cut = int(time.time()) - 6 * 3600
recent_done = cur.execute(
    "SELECT id,title,tenant,completed_at FROM tasks WHERE status='done' AND completed_at>=? ORDER BY completed_at DESC",
    (cut,)).fetchall()
print("DONE last 6h =", len(recent_done))
for r in recent_done:
    acks = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    mark = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()["c"]
    print("  DONE", r["id"], "ack=", acks, "wake_marker=", mark, "|", (r["title"] or "")[:60], "| tenant=", r["tenant"])
