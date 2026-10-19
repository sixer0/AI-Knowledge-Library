# Ronde 17-10c: baca rute-4b utuh + marker lama + runs/outcome + jejak LAPOR/ACK per kartu
import importlib.util, sqlite3, time, os, re

HERMES = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HERMES, "kanban.db")
SCAN = os.path.join(HERMES, "scripts", "gsp_mission_wake_scan.py")
spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
src = importlib.util.open_ifo = open(SCAN, encoding="utf-8").read()

i = src.find("DONE_UNACKED_MIN")
j = src.find("# (e", i)
if j == -1:
    j = i + 4000
print("-- sumber rute done-unacked --")
k = src.find("done-unacked", src.find("def scan"))
print(src[k-200:k+3200] if k != -1 else "(token tidak ditemukan pasca scan(); cari 'unacked')")

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = time.time()
ids = ["t_6f9b7b1e","t_4352ee5a","t_c789eed1","t_9c02c6ed","t_0ae80997","t_bdfea029","t_c02f6244","t_e749792d","t_a8fdb9f6","t_ce103d8a"]

print("\n-- semua komentar (author, umur jam, awal body) per kandidat --")
for tid in ids:
    t = con.execute("SELECT title FROM tasks WHERE id=?", (tid,)).fetchone()
    print(f"\n### {tid} | {t['title'][:70]}")
    for c in con.execute("SELECT author, created_at, body FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)):
        print(f"   [{(now-c['created_at'])/3600:.1f}h] {c['author']}: {c['body'][:110].replace(chr(10),' | ')}")
    for r in con.execute("SELECT kind, created_at, substr(COALESCE(payload,''),1,80) p FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (tid,)):
        print(f"   ev[{(now-r['created_at'])/3600:.1f}h] {r['kind']} {r['p']}")
con.close()
