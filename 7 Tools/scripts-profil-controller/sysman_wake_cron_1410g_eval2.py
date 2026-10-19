# Read-only: recovery check post-UNBLOCK + blocked-reason census + ACK recheck
import sqlite3, time, json

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

def age(ts):
    return round((NOW - ts) / 60.0, 1) if ts else None

print("== NOW:", NOW)

# PRAGMA task_runs columns
cols = [r["name"] for r in cur.execute("PRAGMA table_info(task_runs)").fetchall()]
print("== task_runs cols:", cols)

# Runs for the parent card
pid = "t_4edfcf3a"
runs = cur.execute("SELECT id,status,outcome,started_at,ended_at,max_runtime_seconds,last_heartbeat_at,error FROM task_runs WHERE task_id=? ORDER BY started_at", (pid,)).fetchall()
print("== RUNS parent %s: %d" % (pid, len(runs)))
for r in runs:
    d = dict(r)
    print("   run status=%s outcome=%s started_age=%s ended_age=%s cap=%s hb_age=%s err=%s" % (
        d["status"], d["outcome"], age(d["started_at"]), age(d["ended_at"]),
        d["max_runtime_seconds"], age(d["last_heartbeat_at"]), (d["error"] or "")[:60]))

# Global active runs census (any status meaning in-flight)
try:
    act = cur.execute("SELECT status, COUNT(*) n FROM task_runs GROUP BY status").fetchall()
    print("== RUN STATUS CENSUS:", {r["status"]: r["n"] for r in act})
except Exception as e:
    print("run census err", e)

# Events for tenant in last 60 min by kind
recent = cur.execute("""
  SELECT e.kind, COUNT(*) n, MIN(e.created_at) mn, MAX(e.created_at) mx
  FROM task_events e JOIN tasks t ON t.id=e.task_id
  WHERE t.tenant='VIBE-BIBLE-1013' AND e.created_at >= ?
  GROUP BY e.kind""", (NOW - 3600,)).fetchall()
print("== EVENTS LAST 60 MIN:", [(r["kind"], r["n"], age(r["mx"])) for r in recent])

# Blocked reason classes
bl = cur.execute("SELECT id,title,body FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'").fetchall()
from collections import Counter
cnt = Counter()
samples = {}
for r in bl:
    b = (r["body"] or "")
    first = b.strip().split("\n")[0][:70]
    key = "DITAHAN-controller" if "DITAHAN" in b.upper() else ("CHECKPOINT" if "CHECKPOINT" in b.upper() else ("NEEDS-INPUT" if "needs_input" in b else first))
    cnt[key] += 1
    samples.setdefault(key, r["id"])
print("== BLOCKED REASON CLASSES (%d):" % len(bl))
for k, v in cnt.most_common(12):
    print("   %-28s %3d  sample=%s" % (k[:28], v, samples[k]))

# blocked cards: last event age distribution
ages = []
for r in bl:
    mx = cur.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    ages.append(age(mx))
ages = [a for a in ages if a is not None]
print("== BLOCKED last-event age min/median/max:", min(ages), sorted(ages)[len(ages)//2], max(ages))

# todo cards: how many have parent running vs blocked
todos = cur.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo'").fetchall()
par_state = Counter()
for r in todos:
    ps = cur.execute("""SELECT t.status FROM task_links l JOIN tasks t ON t.id=l.parent_id
                        WHERE l.child_id=?""", (r["id"],)).fetchall()
    par_state[tuple(sorted(p["status"] for p in ps)) or ("none",)] += 1
print("== TODO parent-state dist:", {str(k): v for k, v in par_state.items()})

# ACK recheck on 11 done cards: any RANTAI-ACK at all, plus marker presence
done = cur.execute("SELECT id,title,completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'").fetchall()
print("== DONE cards ACK/marker:")
for r in done:
    ack = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    mk = cur.execute("SELECT COUNT(*) c, MAX(created_at) mx FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()
    lap = cur.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()["c"]
    print("   ", r["id"], "lapor=%d ack=%d marker=%d(marker_age=%s)" % (lap, ack, mk["c"], age(mk["mx"])), "| done_age=", age(r["completed_at"]))
con.close()
