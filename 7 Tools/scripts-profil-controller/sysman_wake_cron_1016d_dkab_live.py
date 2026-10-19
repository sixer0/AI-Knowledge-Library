"""Cek apakah rantai DKAB masih hidup (kartu terbuka / aktivitas controller) atau senyap."""
import os, sqlite3, time

DB = os.path.join(os.environ["LOCALAPPDATA"], "hermes", "kanban.db")
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = int(time.time())

print("== kartu terbuka (todo/blocked/running/in_progress) judul ber-DKAB ==")
rows = list(con.execute(
    "SELECT id,status,title,created_at FROM tasks "
    "WHERE status NOT IN ('done','archived') AND (title LIKE '%DKA%' OR title LIKE '%Adint%' OR tenant LIKE 'DKA%')"))
print(f"  jumlah: {len(rows)}")
for r in rows:
    print(f"  {r['id']} {r['status']:10s} | {r['title'][:70]}")

print("\n== 44 kartu terbuka fleet-wide (judul ringkas) ==")
for r in con.execute("SELECT id,status,substr(title,1,60) t FROM tasks WHERE status NOT IN ('done','archived') ORDER BY status"):
    print(f"  {r['id']} {r['status']:10s} | {r['t']}")

print("\n== aktivitas komentar terbaru pada rantai DKAB (24 jam) ==")
ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE title LIKE 'DKAB%'")]
print(f"  kartu DKAB*: {len(ids)}")
q = ",".join("?" * len(ids))
for c in con.execute(
        f"SELECT task_id,author,created_at,substr(body,1,90) b FROM task_comments "
        f"WHERE task_id IN ({q}) ORDER BY created_at DESC LIMIT 15", ids):
    print(f"  [{(now-c['created_at'])/60:6.1f}m] {c['task_id']} {c['author']}: {c['b']}")

print("\n== event terbaru pada kartu DKAB ==")
for e in con.execute(
        f"SELECT task_id,kind,created_at FROM task_events WHERE task_id IN ({q}) "
        f"ORDER BY created_at DESC LIMIT 12", ids):
    print(f"  [{(now-e['created_at'])/60:6.1f}m] {e['task_id']} {e['kind']}")
con.close()
