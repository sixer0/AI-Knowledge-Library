# Cek komentar terakhir tiap kartu blocked: sudah ternilai penulis terdaftar atau belum
import sqlite3, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
now = int(time.time())
ids = [r[0] for r in cur.execute("SELECT id FROM tasks WHERE status NOT IN ('done','archived') ORDER BY id")]
unjudged = []
for i in ids:
    c = cur.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (i,)).fetchone()
    ev = cur.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (i,)).fetchone()[0]
    if c is None:
        unjudged.append((i, "NO-COMMENT", ev))
        print("UNJUDGED:", i, "| tanpa komentar | evt_umur_mnt=", round((now-ev)/60,1) if ev else None)
        continue
    body = (c["body"] or "").strip().replace("\n", " ")[:90]
    age = round((now - c["created_at"]) / 60, 1)
    ok = ("SYSMAN-CLEANER" in body) or ("RANTAI-WAKE" in body) or ("RANTAI-ACK" in body) or (c["author"] in ("default","sysmanager-cleaner","mission-wake","gsp-master"))
    print(("OK " if ok else "?? "), i, "|", c["author"], "|", age, "mnt |", body)
    if not ok:
        unjudged.append((i, body, ev))
print("TOTAL_BLOCKED =", len(ids), "| TERNILAI =", len(ids)-len(unjudged), "| BELUM =", len(unjudged))
con.close()
