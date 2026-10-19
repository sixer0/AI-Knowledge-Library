# Rekonsiliasi ronde j (cron sysman mission-wake 11-10): pemanggilan scan() kanonis
# + cek marker anti-ulang pada kandidat longgar detail_v2 + sapuan buta-tutup rute-4b
# (event terminal <=6h tanpa syarat tenant).
import importlib.util, sqlite3, time, os, json

HERMES = "C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HERMES, "kanban.db")
SCRIPTS = os.path.join(HERMES, "scripts")

spec = importlib.util.spec_from_file_location(
    "wake_scan", os.path.join(SCRIPTS, "gsp_mission_wake_scan.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

authors = getattr(m, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")

now = int(time.time())
rows = m.scan(DB, now, authors)
print("CANONICAL scan() rows =", len(rows))
for r in rows:
    print("  WAKE:", r)

cands = ["t_090415ec", "t_f4de0f1f", "t_5d087ab1", "t_e034cb5e",
         "t_df6a4a8a", "t_a707d4a3"]
con = sqlite3.connect(DB)
cur = con.cursor()
print("\n-- marker anti-ulang pada kandidat longgar --")
for cid in cands:
    mk = cur.execute(
        "SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'",
        (cid,)).fetchone()[0]
    st, tenant, done_at = cur.execute(
        "SELECT status, tenant, completed_at FROM tasks WHERE id=?", (cid,)).fetchone()
    age = (now - (done_at or 0)) / 60.0 if done_at else -1
    print(f"{cid} status={st} tenant={tenant!r} done_age_min={age:.1f} markers={mk}")

print("\n-- sapuan buta-tutup: event terminal <=6h TANPA syarat tenant --")
cut = now - 6 * 3600
q = """
SELECT t.id, t.status, t.tenant, t.created_by, e.kind, e.created_at
FROM task_events e JOIN tasks t ON t.id=e.task_id
WHERE e.kind IN ('completed','failed','blocked','parked')
  AND e.created_at >= ?
ORDER BY e.created_at DESC
"""
seen = set()
for tid, st, tenant, cb, kind, ts in cur.execute(q, (cut,)):
    if tid in seen:
        continue
    seen.add(tid)
    # LAPOR vs ACK
    comments = cur.execute(
        "SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at",
        (tid,)).fetchall()
    lapor = [c for c in comments if "LAPOR-SELESAI" in c[1] or "LAPOR-SELESEI" in c[1]]
    acks = [c for c in comments if "RANTAI-ACK" in c[1]]
    mk = [c for c in comments if "RANTAI-WAKE" in c[1]]
    lap_authors = {c[0] for c in lapor}
    ack_authors = {c[0] for c in acks}
    ack_lain = bool(ack_authors - lap_authors)
    flag = "BUTA?" if (lapor and not ack_lain and not mk) else "ok"
    print(f"{flag} {tid} status={st} kind={kind} tenant={tenant!r} creator={cb} "
          f"lapor={len(lapor)}/{sorted(lap_authors)} ack={len(acks)}/{sorted(ack_authors)} marker={len(mk)}")
print("total terminal<=6h =", len(seen))
con.close()
