# Final 14-10h: bobot turunan t_689662c9 + cek ACK mendarat + re-scan kanonis.
import sqlite3, time, importlib.util
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

tid = "t_689662c9"
# walk turunan transitif via task_links(parent_id, child_id)
seen, frontier = set(), [tid]
while frontier:
    kids = [r["child_id"] for r in con.execute("SELECT child_id FROM task_links WHERE parent_id=?", (frontier.pop(),))]
    for k in kids:
        if k not in seen:
            seen.add(k); frontier.append(k)
print("turunan transitif:", len(seen))
for k in seen:
    r = con.execute("SELECT status,title FROM tasks WHERE id=?", (k,)).fetchone()
    print(f"  {k} [{r['status']}] {r['title'][:60]}")

cs = list(con.execute("SELECT author, substr(replace(body,char(10),' '),1,90) b, created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 4", (tid,)))
print("\nkomentar terakhir:")
for c in cs:
    print(f"  [{c['author']} {(now-c['created_at'])//60}m] {c['b']}")

spec = importlib.util.spec_from_file_location("ws", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rows = m.scan(DB, now, [a.strip() for a in m.DEFAULT_AUTHORS.split(",")])
import collections
cc = collections.Counter(r[1] for r in rows)
cards = len({r[0] for r in rows})
print(f"\nRE-SCAN: baris={len(rows)} kartu={cards} kelas={dict(cc)}")
du = [r for r in rows if r[1] == 'done-unacked']
print("baris done-unacked:", du)
con.close()
