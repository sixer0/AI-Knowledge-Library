# Verifikasi ronde senyap: koreksi SYSMAN-CLEANER per kartu blocked + status butir SAH kemarin
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
now = int(time.time())

# Kesegaran komentar terbaru (saksi kedua selain events)
r = cur.execute("SELECT MAX(created_at) mx FROM task_comments").fetchone()
print(f"komentar_terbaru_umur_menit={(now - r['mx'])/60:.0f}")

ids = [x["id"] for x in cur.execute("SELECT id FROM tasks WHERE status='blocked'").fetchall()]
print(f"blocked={len(ids)}")
uncorrected = []
for tid in ids:
    c2 = con.cursor()
    last = c2.execute("SELECT body, author, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    body = (last["body"] if last else "") or ""
    has_cleaner = "[SYSMAN-CLEANER" in body
    has_digantikan = "Digantikan t_" in body
    # cek pengganti done utk pola Digantikan
    repl_done = None
    if has_digantikan:
        import re
        m = re.search(r"Digantikan (t_[0-9a-f]{4,}) ", body)
        if m:
            rep = c2.execute("SELECT status FROM tasks WHERE id=?", (m.group(1),)).fetchone()
            repl_done = rep["status"] if rep else "TIDAK-KETEMU"
    marker = c2.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()["c"]
    tag = "CLEANER" if has_cleaner else ("DIGANTIKAN->"+str(repl_done) if has_digantikan else "TANPA-KOREKSI")
    if tag == "TANPA-KOREKSI":
        uncorrected.append((tid, (last["author"] if last else "-"), body[:90].replace("\n", " ")))
    print(f"{tid} | {tag} | marker_wake={marker} | last_author={last['author'] if last else '-'}")

print("== TANPA KOREKSI ==")
for u in uncorrected:
    print("  ", u)

# Butir SAH kemarin: t_841f18dc - cek komentar & event terakhir
print("== t_841f18dc detail ==")
for r in cur.execute("SELECT author, substr(body,1,140) b, datetime(created_at,'unixepoch','+7 hours') ts FROM task_comments WHERE task_id='t_841f18dc' ORDER BY created_at DESC LIMIT 5"):
    print(f"  [{r['ts']}] {r['author']}: {r['b']}")
con.close()
