# Ronde cron 15-10r: nilai kartu blind-spot t_26d8e0dc (running + LAPOR tanpa ACK)
import sqlite3, time, os, sys

DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
now = int(time.time())
tid = sys.argv[1] if len(sys.argv) > 1 else "t_26d8e0dc"

t = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
if not t:
    print("TIDAK ADA:", tid); sys.exit(0)
print(f"[{t['id']}] {t['title']}")
print(f"  status={t['status']} assignee={t['assignee']} created_by={t['created_by']} tenant={t['tenant']}")
print(f"  block_kind={t['block_kind']} block_recurrences={t['block_recurrences']} consecutive_failures={t['consecutive_failures']}")
hb = t["last_heartbeat_at"]
if hb:
    try:
        hbn = int(hb) if str(hb).isdigit() else int(time.mktime(time.strptime(str(hb)[:19], "%Y-%m-%d %H:%M:%S")))
        print(f"  heartbeat_age_min = {(now - hbn)/60:.1f} (raw={hb})")
    except Exception as e:
        print(f"  heartbeat raw={hb} parse-err={e}")
else:
    print("  heartbeat = None")

print("-- parents/children --")
for r in con.execute("SELECT parent_id, child_id FROM task_links WHERE parent_id=? OR child_id=?", (tid, tid)):
    other = r["child_id"] if r["parent_id"] == tid else r["parent_id"]
    st = con.execute("SELECT status FROM tasks WHERE id=?", (other,)).fetchone()
    rel = "child" if r["parent_id"] == tid else "parent"
    print(f"  {rel}: {other} status={st['status'] if st else '?'}")

print("-- last 8 events --")
for r in con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 8", (tid,)):
    print(f"  {int((now - r['created_at'])/60)}m {r['kind']}")

print("-- comments (last 12, full body) --")
for r in con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 12", (tid,)):
    print(f"  [{int((now - r['created_at'])/60)}m] {r['author']}: {r['body'][:400]}")

# ACK setelah LAPOR-SELESAI terakhir?
lap = con.execute("SELECT MAX(created_at) m FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%' AND author != 'gsp-system-manager'", (tid,)).fetchone()["m"]
ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' AND created_at >= ?", (tid, lap or 0)).fetchone()["c"]
mk = con.execute("SELECT MAX(created_at) m FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()["m"]
print(f"-- lap_age_min={None if not lap else round((now-lap)/60,1)} ack_after_lap={ack} marker_last_age_min={None if not mk else round((now-mk)/60,1)}")
con.close()
