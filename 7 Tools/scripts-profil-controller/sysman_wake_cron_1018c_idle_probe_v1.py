import sqlite3, time, os
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
now = int(time.time())
# 1) umur event/komentar terbaru secara eksplisit (MAX, bukan MIN)
for tbl in ("task_events","task_comments"):
    r = con.execute(f"SELECT MAX(created_at) m, COUNT(*) c FROM {tbl}").fetchone()
    print(f"{tbl}: total={r['c']} terbaru={(now-r['m'])/60:.1f} mnt")
# 2) kartu butir tingkat-misi 17-10/18-10: aktivitas sejak laporan
for tid in ("t_841f18dc","t_66b1a0b2"):
    ev = con.execute("SELECT COUNT(*) c, MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()
    cm = con.execute("SELECT COUNT(*) c, MAX(created_at) m FROM task_comments WHERE task_id=?", (tid,)).fetchone()
    st = con.execute("SELECT status FROM tasks WHERE id=?", (tid,)).fetchone()
    print(f"{tid}: status={st['status'] if st else 'N/A'} events={ev['c']} (terbaru {(now-ev['m'])/60:.0f} mnt) comments={cm['c']} (terbaru {(now-cm['m'])/60:.0f} mnt)")
# 3) sensus ACK done VIBE-BIBLE-1013 (id-list dulu, hindari nested cur)
ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'")]
acked = 0
for i in ids:
    n = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (i,)).fetchone()["c"]
    if n: acked += 1
print(f"VBCB done={len(ids)} ber-ACK={acked} ack=0={len(ids)-acked}")
