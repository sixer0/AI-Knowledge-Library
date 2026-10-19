# Blind-spot sweep: cards with terminal/comment activity <=12h, no tenant filter
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
now = time.time()
cutoff = now - 12 * 3600

ids = set()
for r in con.execute("SELECT id FROM tasks WHERE completed_at >= ?", (cutoff,)):
    ids.add(r["id"])
for r in con.execute(
    "SELECT DISTINCT task_id FROM task_events WHERE created_at >= ? AND kind IN "
    "('completed','parked','blocked','status_change','claimed')", (cutoff,)):
    ids.add(r["task_id"])
print("ACTIVE_IDS_12H =", len(ids))
for tid in sorted(ids):
    t = con.execute("SELECT id,title,status,tenant,assignee FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        continue
    laps = con.execute(
        "SELECT author, created_at FROM task_comments WHERE task_id=? AND "
        "(body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%' OR body LIKE '%LAPOR-SELESEI%') "
        "ORDER BY created_at DESC", (tid,)).fetchall()
    acks = con.execute(
        "SELECT author, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' "
        "ORDER BY created_at DESC", (tid,)).fetchall()
    marks = con.execute(
        "SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()["c"]
    if not laps:
        continue  # no completion report -> not a wake candidate
    lap_last = laps[0]["created_at"]; lap_author = laps[0]["author"]
    other_ack = [a for a in acks if a["author"] != lap_author]
    flag = "OK-ACKED" if other_ack else "!! LAPOR-TANPA-ACK-LAIN"
    print(f"{t['id']} [{t['status']}] tenant={t['tenant']!r} lap_by={lap_author} "
          f"lap_age_h={(now-lap_last)/3600:.1f} acks={len(acks)} other_acks={len(other_ack)} "
          f"markers={marks} -> {flag} :: {t['title'][:70]}")
con.close()
