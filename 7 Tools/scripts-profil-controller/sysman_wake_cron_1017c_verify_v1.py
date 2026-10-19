# Verifikasi ronde senyap: koreksi per kartu blocked + census done 12 jam tanpa ACK
import sqlite3, time, os

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def age_min(ts):
    return round((now - ts) / 60.0, 1) if ts else None

print("== KARTU BLOCKED: komentar terakhir + token rem ==")
missing = []
ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE status='blocked' ORDER BY id")]
for tid in ids:
    row = con.execute("SELECT title, tenant, created_by FROM tasks WHERE id=?", (tid,)).fetchone()
    lc = con.execute("SELECT body, author, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    body = (lc["body"] if lc else "") or ""
    toks = []
    for tok in ("[SYSMAN-CLEANER", "RANTAI-WAKE", "RANTAI-ACK", "ANCHOR-KONTRAK", "Digantikan", "DITAHAN"):
        if tok in body:
            toks.append(tok)
    # cek juga seluruh komentar (bukan hanya terakhir) untuk token koreksi
    allc = con.execute("SELECT body FROM task_comments WHERE task_id=?", (tid,)).fetchall()
    ever = set()
    for c in allc:
        for tok in ("[SYSMAN-CLEANER", "RANTAI-WAKE", "ANCHOR-KONTRAK", "Digantikan"):
            if tok in (c["body"] or ""):
                ever.add(tok)
    mark = ",".join(sorted(toks)) or ",".join(sorted(ever)) or "TANPA-REM"
    print(f"  {tid} author_last={lc['author'] if lc else '-'} umur_kom={age_min(lc['created_at']) if lc else '-'} rem=[{mark}] :: {(row['title'] or '')[:45]}")
    if not toks and not ever:
        missing.append(tid)
print("  tanpa rem sama sekali:", len(missing), missing)

print("== DONE 12 JAM TERAKHIR: census ACK ==")
cut = now - 12*3600
rows = con.execute("SELECT id, title, completed_at, tenant FROM tasks WHERE status='done' AND completed_at >= ? ORDER BY completed_at DESC", (cut,)).fetchall()
print("  jumlah done <=12 jam:", len(rows))
for r in rows:
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
    lap = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (r["id"],)).fetchone()["n"]
    mk = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (r["id"],)).fetchone()["n"]
    flag = "" if (ack > 0 or mk > 0 or r["tenant"] is None) else " <-- TANPA ACK"
    print(f"  {r['id']} tenant={r['tenant']} ack={ack} lap={lap} marker={mk} umur_done={age_min(r['completed_at'])}m :: {(r['title'] or '')[:45]}{flag}")

print("== EVENT 6 JAM TERAKHIR (kelas terminal) ==")
cut6 = now - 6*3600
for r in con.execute("SELECT kind, COUNT(*) n FROM task_events WHERE created_at >= ? GROUP BY kind ORDER BY n DESC", (cut6,)):
    print(f"  {r['kind']}: {r['n']}")
con.close()
