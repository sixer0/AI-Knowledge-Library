# Read-only: final re-scan reconciliation + blind-spot sweep running cards (14-10c)
import sqlite3, time, importlib.util, collections

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
spec = importlib.util.spec_from_file_location(
    "wake_scan", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

now = int(time.time())
f2 = mod.scan(DB, now, ["default", "sysmanager-cleaner", "mission-wake"])
print("RE-SCAN findings:", len(f2), "unique:", len(set(x[0] for x in f2)))
print("classes:", dict(collections.Counter(x[1] for x in f2)))
du = [x for x in f2 if x[1] == "done-unacked"]
print("done-unacked lines:", du)

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
cur = con.cursor()
# Blind spot: any running cards anywhere?
run = cur.execute("SELECT id,title,tenant,last_heartbeat_at FROM tasks WHERE status IN ('running','in_progress','review')").fetchall()
print("\nrunning/in_progress/review cards:", len(run))
for r in run:
    print(r)

# the single comment after newest gave_up on VBCB
gu = cur.execute("""SELECT MAX(e.created_at) FROM task_events e JOIN tasks t ON t.id=e.task_id
                    WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='gave_up'""").fetchone()[0]
cm = cur.execute("""SELECT c.task_id, c.author, substr(replace(replace(c.body,char(13),' '),char(10),' | '),1,160), c.created_at
                    FROM task_comments c JOIN tasks t ON t.id=c.task_id
                    WHERE t.tenant='VIBE-BIBLE-1013' AND c.created_at > ?""", (gu,)).fetchall()
for c in cm:
    print("post-gave_up comment:", c[0], "|", c[1], "|", c[2], "| age_min=%.0f" % ((now-c[3])/60))

# per-wave: how many writers have 2x timed_out vs 1x (gave_up implies 2x)
w = cur.execute("""SELECT t.id, SUM(CASE WHEN e.kind='timed_out' THEN 1 ELSE 0 END) AS n_to,
                          MAX(CASE WHEN e.kind='gave_up' THEN 1 ELSE 0 END) AS gu
                   FROM tasks t JOIN task_events e ON e.task_id=t.id
                   WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked' AND t.title LIKE '%Penulis%'
                   GROUP BY t.id""").fetchall()
print("\nwriter cards blocked:", len(w),
      "with gave_up:", sum(1 for x in w if x[2]),
      "timed_out count distribution:", dict(collections.Counter(x[1] for x in w)))
con.close()
