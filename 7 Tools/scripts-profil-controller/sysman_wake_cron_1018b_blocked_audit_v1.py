# -*- coding: utf-8 -*-
"""Ronde 18-10b lanjutan: saksi scheduler hidup (mtime cron output) + audit 44 kartu
blocked vs koreksi [SYSMAN-CLEANER] + identifikasi kartu ke-44 di luar set 43 terenal."""
import os, time, sqlite3, glob

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
now = int(time.time())

print("== SAKSI SCHEDULER (mtime cron output terbaru) ==")
for prof_dir in [os.path.join(HOME, "cron", "output"),
                 os.path.join(HOME, "profiles", "gsp-system-manager", "cron", "output")]:
    files = []
    for p in glob.glob(os.path.join(prof_dir, "**", "*"), recursive=True):
        if os.path.isfile(p):
            files.append((os.path.getmtime(p), p))
    files.sort(reverse=True)
    print(f"  [{prof_dir}]")
    for mt, p in files[:3]:
        print(f"    umur {(now-mt)/60.0:.1f} mnt :: {os.path.basename(os.path.dirname(p))}/{os.path.basename(p)}")

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
print("== AUDIT 44 BLOCKED: koreksi SYSMAN-CLEANER / Digantikan / status pengganti ==")
rows = con.execute("""SELECT id, title, tenant, created_by FROM tasks
                      WHERE status='blocked' ORDER BY tenant NULLS LAST, id""").fetchall()
uncorrected = []
for r in rows:
    # komentar asli pertama ber-anchor awal body (hindari menangkap koreksi sendiri)
    dig = con.execute("""SELECT body, author FROM task_comments WHERE task_id=? AND body LIKE 'Digantikan%'
                         ORDER BY created_at ASC LIMIT 1""", (r["id"],)).fetchone()
    cleaner = con.execute("""SELECT COUNT(*) n FROM task_comments WHERE task_id=?
                             AND body LIKE '%[SYSMAN-CLEANER%'""", (r["id"],)).fetchone()["n"]
    lastc = con.execute("""SELECT body, author, created_at FROM task_comments WHERE task_id=?
                           ORDER BY created_at DESC LIMIT 1""", (r["id"],)).fetchone()
    repl_status = ""
    if dig:
        import re
        m = re.search(r"(t_[0-9a-f]{8})", dig["body"])
        if m:
            pr = con.execute("SELECT status FROM tasks WHERE id=?", (m.group(1),)).fetchone()
            repl_status = f"-> {m.group(1)}={pr['status'] if pr else '?'}"
    line = f"  {r['id']} | {r['tenant'] or '-'} | cleaner={cleaner} | {dig['body'][:28]+repl_status if dig else 'TANPA-DIGANTIKAN'}"
    if not cleaner:
        uncorrected.append(r["id"])
        line += "  << TANPA KOREKSI"
        if lastc:
            line += f" | komentar-terakhir({(now-lastc['created_at'])/60:.0f}mnt,{lastc['author']}): {lastc['body'][:70]!r}"
    print(line)
print(f"== RINGKAS: blocked={len(rows)} tanpa-koreksi={len(uncorrected)} ids={uncorrected}")
con.close()
