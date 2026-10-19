# Read-only deep probe: retry-loop depth, tenant census, blind-spot sweep (cron 14-10)
import sqlite3, json, time, collections

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

out = {}

# 1) Run-count census for VBCB blocked writer cards
rows = cur.execute("""
 SELECT t.id, t.status, t.consecutive_failures, t.max_retries, t.current_run_id,
        COUNT(r.id) AS n_runs,
        SUM(CASE WHEN r.status='timed_out' THEN 1 ELSE 0 END) AS n_to,
        MAX(r.started_at) AS last_start
 FROM tasks t LEFT JOIN task_runs r ON r.task_id=t.id
 WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked'
 GROUP BY t.id ORDER BY n_runs DESC LIMIT 5
""").fetchall()
out["writer_run_depth_sample"] = [dict(r) | {"last_start_age_min": round((NOW-r["last_start"])/60) if r["last_start"] else None} for r in rows]

tot = cur.execute("""
 SELECT COUNT(*) c, MIN(n) mn, MAX(n) mx, AVG(n) av FROM (
  SELECT t.id, COUNT(r.id) n FROM tasks t LEFT JOIN task_runs r ON r.task_id=t.id
  WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked' GROUP BY t.id)
""").fetchone()
out["writer_run_depth_all"] = dict(tot)

# total runs across tenant (work burned)
burn = cur.execute("""
 SELECT COUNT(*) n_runs, SUM(CASE WHEN r.status='timed_out' THEN 1 ELSE 0 END) n_to
 FROM task_runs r JOIN tasks t ON t.id=r.task_id
 WHERE t.tenant='VIBE-BIBLE-1013'
""").fetchone()
out["tenant_run_burn"] = dict(burn)

# 2) Tenant census
cen = cur.execute("SELECT status, COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status").fetchall()
out["tenant_census"] = {r["status"]: r["c"] for r in cen}
out["tenant_total"] = sum(r["c"] for r in cen)

# anchor/blueprint cards (tenant null) referencing VBCB in title
anch = cur.execute("SELECT id,status,title FROM tasks WHERE tenant IS NULL AND title LIKE '%VBCB%' LIMIT 10").fetchall()
out["vbcb_null_tenant"] = [dict(r) for r in anch]

# 3) Any controller triage on VBCB cards in last 6h? (authors default/gsp-master etc.)
tri = cur.execute("""
 SELECT c.author, COUNT(*) n, MAX(c.created_at) latest
 FROM task_comments c JOIN tasks t ON t.id=c.task_id
 WHERE t.tenant='VIBE-BIBLE-1013' AND c.created_at > ?
 GROUP BY c.author
""", (NOW-6*3600,)).fetchall()
out["comments_last6h_by_author"] = [{**dict(r), "latest_age_min": round((NOW-r["latest"])/60)} for r in tri]

# sample of worker checkpoint proposal (one full body)
cp = cur.execute("""
 SELECT c.task_id, c.author, c.body, c.created_at
 FROM task_comments c JOIN tasks t ON t.id=c.task_id
 WHERE t.tenant='VIBE-BIBLE-1013' AND c.author='gsp-worker'
 ORDER BY c.created_at DESC LIMIT 1
""").fetchone()
if cp:
    out["checkpoint_proposal_sample"] = {"task": cp["task_id"], "age_min": round((NOW-cp["created_at"])/60), "body": cp["body"][:1200]}

# 4) Blind spot: ALL running cards fleet-wide with LAPOR-SELESAI/PARKED and ACK census
run_cards = cur.execute("SELECT id,title,tenant,assignee,last_heartbeat_at FROM tasks WHERE status='running'").fetchall()
bs = []
for rc in run_cards:
    coms = cur.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 30", (rc["id"],)).fetchall()
    lapor = [c for c in coms if ("LAPOR-SELESAI" in (c["body"] or "").upper() or "LAPOR SELESAI" in (c["body"] or "").upper())]
    ack = [c for c in coms if "RANTAI-ACK" in (c["body"] or "")]
    bs.append({"id": rc["id"], "title": rc["title"][:70], "tenant": rc["tenant"],
               "hb_age_min": round((NOW-rc["last_heartbeat_at"])/60) if rc["last_heartbeat_at"] else None,
               "n_lapor": len(lapor), "n_ack": len(ack)})
out["blindspot_running"] = bs

# 5) sanity: board alive
ev = cur.execute("SELECT MAX(created_at) m, COUNT(*) c FROM task_events").fetchone()
out["sanity_last_event_age_min"] = round((NOW-ev["m"])/60)
out["sanity_events_total"] = ev["c"]

print(json.dumps(out, indent=1, default=str))
