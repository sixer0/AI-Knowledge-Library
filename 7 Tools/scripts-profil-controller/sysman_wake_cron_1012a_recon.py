# Rekonsiliasi ronde sunyi 12-10: scan() kanonis vs kandidat longgar detail_v2
import sqlite3, time, os, importlib.util, json

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
SCAN = "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py"

spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

now = int(time.time())
authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")

rows = mod.scan(DB, now, authors)
print("== CANONICAL scan() rows:", len(rows))
for r in rows:
    print("  ", r)

con = sqlite3.connect(DB)
cur = con.cursor()

# 1) umur event terakhir papan (anti DB basi)
q = """
SELECT MAX(x) FROM (
  SELECT MAX(created_at) x FROM task_events
  UNION ALL SELECT MAX(created_at) FROM task_comments
  UNION ALL SELECT MAX(created_at) FROM tasks
)
"""
last = cur.execute(q).fetchone()[0]
print("== last activity epoch:", last, "age_min:", round((now - last) / 60.0, 1))

# 2) kandidat longgar dari detail_v2 (done tanpa ACK lain-author, 24 jam) -> jelaskan kenapa tidak lolos kanonis
ids = ["t_090415ec","t_f4de0f1f","t_5d087ab1","t_e034cb5e","t_df6a4a8a","t_a707d4a3",
       "t_52521c3b","t_c08057c4"]
print("== kandidat longgar: penjelasan ==")
for tid in ids:
    t = cur.execute("SELECT id,status,tenant,assignee,completed_at,title FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print(tid, "TIDAK ADA"); continue
    tid_, status, tenant, assignee, comp, title = t
    age_h = (now - (comp or 0)) / 3600.0 if comp else -1
    coms = cur.execute(
        "SELECT author, substr(body,1,80), created_at FROM task_comments WHERE task_id=? ORDER BY created_at",
        (tid,)
    ).fetchall()
    lapor = [c for c in coms if "LAPOR" in c[1].upper()]
    acks  = [c for c in coms if "RANTAI-ACK" in c[1].upper()]
    mark  = [c for c in coms if "RANTAI-WAKE" in c[1].upper()]
    lap_authors = {c[0] for c in lapor}
    ack_lain = [c for c in acks if c[0] not in lap_authors]
    reasons = []
    if age_h > 6: reasons.append(f"di-luar-jendela-6h ({age_h:.1f}h)")
    if not tenant: reasons.append("tenant-kosong(gerbang rute-4b)")
    if mark: reasons.append(f"marker-RANTAI-WAKE-ada({len(mark)})")
    if ack_lain: reasons.append(f"ACK-author-lain-ada({len(ack_lain)})")
    print(f"{tid} status={status} tenant={tenant!r} done_age_h={age_h:.1f} lapor={len(lapor)} ack_total={len(acks)} ack_lain={len(ack_lain)} marker={len(mark)} alasan_tidak_lolos={reasons}")
    print(f"   judul: {title[:70]}")
con.close()
