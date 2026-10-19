# Rekonsilasi ronde cron 12-10: scan() kanonis vs kandidat detail_v2 + marker RANTAI-WAKE
import importlib.util, time, sqlite3, os

HERMES = os.path.expanduser("C:/Users/TRIAL/AppData/Local/hermes")
DB = HERMES + "/kanban.db"
spec = importlib.util.spec_from_file_location(
    "wake_scan", HERMES + "/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

now = int(time.time())
rows = m.scan(DB, now, m.DEFAULT_AUTHORS.split(","))
print("== scan() KANONIS: %d baris WAKE ==" % len(rows))
for r in rows:
    print(r)

cands = ["t_090415ec","t_f4de0f1f","t_5d087ab1","t_e034cb5e","t_df6a4a8a","t_a707d4a3"]
con = sqlite3.connect(DB)
cur = con.cursor()
print("\n== marker RANTAI-WAKE per kandidat ==")
for cid in cands:
    t = cur.execute("SELECT status,completed_at,tenant,created_by,title FROM tasks WHERE id=?", (cid,)).fetchone()
    mk = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (cid,)).fetchone()[0]
    ack = cur.execute("""SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'""", (cid,)).fetchone()[0]
    lap = cur.execute("""SELECT COUNT(*) FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%' OR body LIKE '%LAPOR-SELESAI%')""", (cid,)).fetchone()[0]
    print("%s status=%s done_age_min=%.0f tenant=%s author=%s marker_wake=%d ack=%d lapor=%d | %s" % (
        cid, t[0], (now - (t[1] or now))/60.0, t[2], t[3], mk, ack, lap, (t[4] or "")[:60]))

# blind spot: event terminal <=6h tanpa syarat tenant
print("\n== blind: terminal events <=6h (tanpa filter tenant) ==")
cutoff = now - 6*3600
for row in cur.execute("""
  SELECT e.task_id, e.kind, e.created_at, t.status, t.tenant
  FROM task_events e JOIN tasks t ON t.id=e.task_id
  WHERE e.kind IN ('completed','done','parked') AND e.created_at>=?
  ORDER BY e.created_at DESC LIMIT 40""", (cutoff,)):
    print(row)
con.close()
