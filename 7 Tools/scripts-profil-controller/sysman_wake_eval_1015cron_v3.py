# Round 3 (read-only): non-VBCB blocked debt + final re-scan check.
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

print("=== BLOCKED NON-VBCB ===")
oth = [dict(r) for r in con.execute(
    "SELECT id,title,tenant,created_at FROM tasks WHERE status='blocked' "
    "AND (tenant IS NULL OR tenant!='VIBE-BIBLE-1013') ORDER BY created_at DESC")]
print("count=", len(oth))
for c in oth:
    le = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (c["id"],)).fetchone()[0]
    la = con.execute("SELECT author, substr(body,1,110) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1",(c["id"],)).fetchone()
    print(c["id"], "|", (c["title"] or "")[:58], "| tenant=", c["tenant"],
          "| age_days=", round((NOW-c["created_at"])/86400,1),
          "| lastev_min=", round((NOW-le)/60) if le else None,
          "| last:", (la["author"]+": "+(la["b"] or "").replace(chr(10)," ")) if la else "-")

print("\n=== TODO NON-VBCB ===")
td = [dict(r) for r in con.execute(
    "SELECT id,title,tenant FROM tasks WHERE status='todo' AND (tenant IS NULL OR tenant!='VIBE-BIBLE-1013')")]
print("count=", len(td))
for c in td[:10]: print(c["id"], (c["title"] or "")[:60], c["tenant"])

# who promoted/linked the 33 todo verification cards, and when (context for controller)
print("\n=== LINK EVENT AGE (sample) ===")
for tid in ["t_002af121","t_153594d4","t_f9ac1ff2"]:
    evs = [dict(r) for r in con.execute("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at",(tid,))]
    print(tid, [(e["kind"], round((NOW-e["created_at"])/60)) for e in evs])
