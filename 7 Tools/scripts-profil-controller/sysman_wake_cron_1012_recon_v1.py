# Rekonsiliasi ronde sunyi 1012: cek marker RANTAI-WAKE pada kandidat detail WAKE=1,
# jendela 6 jam rute-4b, dan event terminal <=6h tanpa syarat tenant (sapuan blind).
import sqlite3, time, os

DB = os.path.join(os.environ["LOCALAPPDATA"], "hermes", "kanban.db")
now = int(time.time())
H6 = now - 6 * 3600

CANDS = ["t_090415ec", "t_f4de0f1f", "t_5d087ab1", "t_e034cb5e", "t_df6a4a8a", "t_a707d4a3"]

con = sqlite3.connect(DB)
cur = con.cursor()

print("== A. Marker/komentar per kandidat detail WAKE=1 ==")
for cid in CANDS:
    row = cur.execute("SELECT status, tenant, completed_at FROM tasks WHERE id=?", (cid,)).fetchone()
    if not row:
        print(f"{cid}: TIDAK ADA DI PAPAN")
        continue
    status, tenant, completed_at = row
    age_h = (now - (completed_at or 0)) / 3600.0
    marks = cur.execute(
        "SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (cid,)
    ).fetchone()[0]
    acks = cur.execute(
        "SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (cid,)
    ).fetchone()[0]
    in_window = "DI-DALAM-6J" if (completed_at or 0) >= H6 else "LUAR-JENDELA"
    print(f"{cid} status={status} tenant={'ADA' if tenant else 'KOSONG'} done_age={age_h:.1f}h {in_window} marker_wake={marks} ack={acks}")

print("\n== B. Event terminal <=6h TANPA syarat tenant (sapuan blind) ==")
rows = cur.execute(
    """SELECT t.id, t.title, t.tenant, t.status, e.kind, e.created_at
       FROM task_events e JOIN tasks t ON t.id=e.task_id
       WHERE e.created_at >= ? AND e.kind IN ('completed','parked','blocked','failed')
       ORDER BY e.created_at DESC LIMIT 40""",
    (H6,),
).fetchall()
if not rows:
    print("(kosong - tidak ada event terminal dalam 6 jam)")
for r in rows:
    print(f"{r[0]} kind={r[4]} status={r[3]} tenant={'ADA' if r[2] else 'KOSONG'} age={(now-r[5])/60:.0f}m | {r[1][:60]}")

print("\n== C. Kartu todo terbuka: umur + orang tua ==")
rows = cur.execute(
    "SELECT id, title, created_at, tenant FROM tasks WHERE status='todo' ORDER BY created_at DESC LIMIT 10"
).fetchall()
for tid, title, created_at, tenant in rows:
    parents = cur.execute(
        "SELECT p.status FROM task_links l JOIN tasks p ON p.id=l.parent_id WHERE l.child_id=?", (tid,)
    ).fetchall()
    pstat = ",".join(p[0] for p in parents) if parents else "TANPA-ORTU"
    print(f"{tid} umur={(now-created_at)/3600:.1f}h ortu={pstat} | {title[:60]}")

print("\n== D. Umur event terakhir papan (detak hidup) ==")
r = cur.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
print(f"last_event_age_min={(now-r)/60:.1f}")
con.close()
