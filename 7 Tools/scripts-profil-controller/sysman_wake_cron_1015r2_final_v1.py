# -*- coding: utf-8 -*-
# Ronde 1015r2 final: pecah 46 done VBCB (M4 vs lain), cek sisa M4 terbuka, cek anak dari
# orang-tua yang sudah selesai penuh, lalu re-scan kanonis scan().
import sqlite3, time, importlib.util
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
def age(ts): return round((NOW-ts)/60.0) if ts else None

print("== PECAH 46 DONE VBCB ==")
rows = con.execute("""SELECT substr(title,1,10) pref, COUNT(*) n FROM tasks
 WHERE tenant='VIBE-BIBLE-1013' AND status='done' GROUP BY pref""").fetchall()
for r in rows: print(" ", r["pref"], r["n"])
m4open = con.execute("""SELECT COUNT(*) FROM tasks WHERE tenant='VIBE-BIBLE-1013'
 AND title LIKE '%(resume)%' AND status != 'done'""").fetchone()[0]
print("kartu M4 (resume) belum done:", m4open)

print("\n== ANAK TODO: semua orang tua done? ==")
ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo'").fetchall()]
all_done_parents = 0
for tid in ids:
    par = [r["parent_id"] for r in con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,)).fetchall()]
    st = [con.execute("SELECT status FROM tasks WHERE id=?", (p,)).fetchone()[0] for p in par]
    if st and all(s == "done" for s in st): all_done_parents += 1
print(f"anak todo={len(ids)} | yang SEMUA orang tuanya done={all_done_parents} (sisanya tertahan orang tua blocked)")

print("\n== RE-SCAN KANONIS ==")
spec = importlib.util.spec_from_file_location("ws", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
import sys, io, contextlib
sys.argv = ["scan"]
spec.loader.exec_module(mod)
auth = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(auth, str): auth = auth.split(",")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    try: mod.scan(DB, int(time.time()), auth)
    except SystemExit: pass
out = buf.getvalue().strip().splitlines()
print("baris WAKE re-scan:", len(out))
from collections import Counter
print(Counter(l.split()[2] for l in out if l.startswith("WAKE")))
