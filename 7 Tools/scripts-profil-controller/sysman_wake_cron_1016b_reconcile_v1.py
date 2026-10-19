# Read-only reconciliation: canonical scan() vs loose detail-tool candidates.
import sqlite3, time, os, importlib.util, json

HERMES = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HERMES, "kanban.db")
SCAN = os.path.join(HERMES, "scripts", "gsp_mission_wake_scan.py")

spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

now = int(time.time())
authors = mod.DEFAULT_AUTHORS
if isinstance(authors, str):
    authors = authors.split(",")
findings = mod.scan(DB, now, authors)
print("CANONICAL_SCAN findings =", len(findings))
for f in findings:
    print("  ROW:", tuple(f))

candidates = ["t_aa8ccf54","t_ba9f0bf6","t_8998b559","t_8da71c9f","t_2da2d99f","t_26d8e0dc"]
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
cur = con.cursor()

# thresholds from source
for name in ["STALLED_MIN","RUN_WINDOW_H","FASE_STALL_MIN","DONE_UNACKED_MIN"]:
    print("THRESH", name, getattr(mod, name, "?"))
print("CUTOFF attr:", [a for a in dir(mod) if "CUTOFF" in a.upper()])

print("-- per-candidate --")
for cid in candidates:
    r = cur.execute("SELECT id,status,tenant,assignee,completed_at,created_at FROM tasks WHERE id=?", (cid,)).fetchone()
    if not r:
        print(cid, "NOT FOUND"); continue
    done_age = (now - (r["completed_at"] or 0))/60.0
    comments = cur.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (cid,)).fetchall()
    lap = [c for c in comments if "LAPOR" in (c["body"] or "")]
    ack = [c for c in comments if "RANTAI-ACK" in (c["body"] or "")]
    mark = [c for c in comments if "RANTAI-WAKE" in (c["body"] or "")]
    lap_authors = sorted({c["author"] for c in lap})
    ack_authors = sorted({(c["author"], time.strftime('%m-%d %H:%M', time.localtime(c["created_at"]))) for c in ack})
    print(json.dumps({
        "id": cid, "status": r["status"], "tenant": r["tenant"], "assignee": r["assignee"],
        "done_age_min": round(done_age,1),
        "n_lap": len(lap), "lap_authors": lap_authors,
        "n_ack": len(ack), "ack_detail": ack_authors,
        "markers": [(c["author"], (c["body"] or "")[:60], time.strftime('%m-%d %H:%M', time.localtime(c["created_at"]))) for c in mark],
    }))

# todo census discrepancy check
print("-- todo census --")
for row in cur.execute("SELECT status, COUNT(*) c FROM tasks GROUP BY status"):
    print(row["status"], row["c"])
print("-- running cards (blindspot) --")
rows = cur.execute("SELECT id,title FROM tasks WHERE status='running'").fetchall()
print("running count:", len(rows))
for row in rows:
    print("  RUN:", row["id"], (row["title"] or "")[:50])
