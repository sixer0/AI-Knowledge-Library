"""Ronde senja 17-10: vonis kanonis scan() + sensus kartu terbuka + marker per kartu."""
import importlib.util, os, sqlite3, time, sys

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
SCAN = os.path.join(HOME, "scripts", "gsp_mission_wake_scan.py")

spec = importlib.util.spec_from_file_location("mws", SCAN)
mws = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mws)

authors = getattr(mws, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")

findings = mws.scan(DB, int(time.time()), authors)
print("CANONICAL_SCAN_FINDINGS =", len(findings))
for f in findings:
    print("  ROW:", tuple(f))

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("\n-- open cards (status NOT IN done/archived) --")
ids = [r["id"] for r in con.execute(
    "SELECT id FROM tasks WHERE status NOT IN ('done','archived') ORDER BY status, created_at")]
print("open_count =", len(ids))
cur = con.cursor()
for tid in ids:
    r = cur.execute(
        "SELECT id,title,status,tenant,assignee,created_by,created_at,completed_at,"
        "block_kind,current_run_id,last_heartbeat_at FROM tasks WHERE id=?", (tid,)).fetchone()
    ev = cur.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    cm = cur.execute(
        "SELECT author, body, created_at FROM task_comments WHERE task_id=? "
        "ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    nack = cur.execute(
        "SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["c"]
    nwake = cur.execute(
        "SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()["c"]
    last_body = (cm["body"] or "").replace("\n", " ")[:110] if cm else "(no comment)"
    last_auth = cm["author"] if cm else "-"
    print("CARD %s | st=%s | tenant=%s | assignee=%s | blk=%s | run=%s | hb_age_min=%s | ev_age_min=%s | ack=%s wake=%s" % (
        r["id"], r["status"], r["tenant"], r["assignee"], r["block_kind"], r["current_run_id"],
        round((time.time() - r["last_heartbeat_at"]) / 60, 1) if r["last_heartbeat_at"] else "None",
        round((time.time() - ev) / 60, 1) if ev else "None", nack, nwake))
    print("     title:", (r["title"] or "")[:90])
    print("     last[%s]: %s" % (last_auth, last_body))

print("\n-- board life --")
for tbl, col in (("task_events", "created_at"), ("task_comments", "created_at"), ("tasks", "created_at")):
    row = con.execute("SELECT MAX(%s) m, COUNT(*) c FROM %s" % (col, tbl)).fetchone()
    print("%s: max_age_min=%.1f rows=%s" % (tbl, (time.time() - row["m"]) / 60.0, row["c"]))
con.close()
