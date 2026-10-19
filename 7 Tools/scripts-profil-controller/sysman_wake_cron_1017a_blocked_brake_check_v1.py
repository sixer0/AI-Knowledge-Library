# Cek rem triase pada 44 kartu blocked: komentar terakhir per kartu
import sqlite3, time, os

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = int(time.time())

ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE status='blocked'")]
print("blocked:", len(ids))
nofix = []
for cid in ids:
    c = con.execute("SELECT body, author, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (cid,)).fetchone()
    if c is None:
        nofix.append((cid, "NO-COMMENT", ""))
        continue
    body = c["body"] or ""
    age = round((now - c["created_at"]) / 60.0)
    tok = ("SYSMAN-CLEANER" in body) or ("RANTAI-WAKE" in body) or ("[FASE]" in body) or ("ANCHOR-KONTRAK" in body) or ("Digantikan" in body) or ("DITAHAN" in body)
    if not tok:
        nofix.append((cid, f"last={age}m author={c['author']}", body[:90].replace("\n", " ")))

print("tanpa-token-rem:", len(nofix))
for n in nofix:
    print(" -", n)
