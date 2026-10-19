# Cek: semua kartu blocked punya koreksi terbaru di komentar terakhir?
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE status='blocked'")]
unvalued = []
for tid in ids:
    last = con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    if last is None:
        unvalued.append((tid, "NO-COMMENT", 0))
        continue
    body = last["body"] or ""
    age = (now - last["created_at"]) / 60.0
    ok = ("[SYSMAN-CLEANER" in body) or ("RANTAI-WAKE" in body) or ("RANTAI-ACK" in body) or ("ANCHOR-KONTRAK" in body)
    if not ok:
        unvalued.append((tid, body[:70].replace("\n", " "), age))
print(f"blocked_total={len(ids)} belum_terkoreksi={len(unvalued)}")
for u in unvalued:
    print("  ", u)
# umur komentar terakhir minimum per kartu blocked (sudah ternilai lama?)
mx = con.execute("SELECT MAX(created_at) FROM task_comments").fetchone()[0]
print(f"last_comment_age_min={(now-mx)/60.0:.1f}")
con.close()
