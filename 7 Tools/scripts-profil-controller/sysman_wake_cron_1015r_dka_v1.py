# Ronde cron 15-10r lanjutan: census keluarga DKA + WEBLOC + jejak ACK/komentar per kartu
import sqlite3, time, os

WS = os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local") + "/hermes"
con = sqlite3.connect(f"file:{WS}/kanban.db?mode=ro", uri=True)
con.row_factory = sqlite3.Row
now = int(time.time())

for pref in ("DKA", "WEBLOC"):
    rows = con.execute("SELECT id,title,status,tenant,created_by,assignee,completed_at,created_at FROM tasks WHERE title LIKE ? ORDER BY created_at", (pref + "%",)).fetchall()
    print(f"\n===== KELUARGA {pref}: {len(rows)} kartu =====")
    for r in rows:
        cid = r["id"]
        cs = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=?", (cid,)).fetchone()["c"]
        acks = [a["author"] for a in con.execute("SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (cid,))]
        laps = [a["author"] for a in con.execute("SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (cid,))]
        wk = [a["author"] for a in con.execute("SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (cid,))]
        ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (cid,)).fetchone()["m"]
        ca = f"{(now - r['completed_at'])/60:.0f}m" if r["completed_at"] else "-"
        ea = f"{(now - ev)/60:.0f}m" if ev else "-"
        print(f"  {cid} {r['status']:8s} tenant={str(r['tenant']):22s} by={r['created_by']:16s} asg={str(r['assignee']):16s} done={ca:>6s} ev={ea:>6s} cmts={cs} lap={len(laps)} ack={len(acks)} wake={len(wk)} | {r['title'][:40]}")

# contoh isi komentar 3 kartu DKA done ack=0
print("\n===== SAMPEL KOMENTAR DKA =====")
for cid in ("t_8998b559", "t_fb910478", "t_96332f33"):
    print(f"\n-- {cid} --")
    for c in con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (cid,)):
        print(f"  [{int((now-c['created_at'])/60)}m] {c['author']}: {c['body'][:280]}")

# siapa controller aktif untuk DKA? cek created_by & author komentar terbanyak per keluarga
print("\n===== AUTHOR KOMENTAR DKA (top) =====")
for a in con.execute("SELECT c.author, COUNT(*) n FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.title LIKE 'DKA%' GROUP BY c.author ORDER BY n DESC"):
    print(f"  {a['author']} = {a['n']}")
con.close()
