# -*- coding: utf-8 -*-
"""Penutup ronde senyap 17-10: buktikan 44 kartu blocked seluruhnya sudah ternilai
(token koreksi di komentar TERAKHIR) + saksi kesegaran sistem non-WMI."""
import os, sqlite3, time, glob

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
NOW = int(time.time())

print("DB mtime age_min = %.1f" % ((NOW - os.path.getmtime(DB)) / 60.0))

con = sqlite3.connect("file:%s?mode=ro" % DB.replace("\\", "/"), uri=True)
con.row_factory = sqlite3.Row
cur = con.cursor()
rows = cur.execute("SELECT id, title FROM tasks WHERE status NOT IN ('done','archived')").fetchall()
print("KARTU TERBUKA =", len(rows))
belum = []
for r in rows:
    lc = cur.execute("SELECT body FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1",
                     (r["id"],)).fetchone()
    b = (lc["body"] if lc else "") or ""
    ok = ("[SYSMAN-CLEANER" in b) or ("RANTAI-WAKE" in b) or ("Digantikan" in b)
    if not ok:
        belum.append((r["id"], (r["title"] or "")[:60], b[:70].replace("\n", " ")))
print("TERNILAI di komentar terakhir =", len(rows) - len(belum))
print("BELUM TERNILAI =", len(belum))
for x in belum:
    print("   ", x)

# saksi kesegaran: heartbeat gateway (profil default = root hermes)
print("\n--- HEARTBEAT GATEWAY (saksi non-WMI) ---")
cands = [os.path.join(HOME, "state", "gateway.heartbeat")] + \
        glob.glob(os.path.join(HOME, "profiles", "*", "state", "gateway.heartbeat"))
for p in cands:
    if os.path.exists(p):
        age_h = (NOW - os.path.getmtime(p)) / 3600.0
        prof = "default" if "profiles" not in p else p.split(os.sep + "profiles" + os.sep)[1].split(os.sep)[0]
        print("  %-28s age_jam=%.1f" % (prof, age_h))
con.close()
print("CLOSE-DONE")
