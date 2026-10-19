# Census tenant BLENDER-MCP-SKILL-1016: status counts + ACK per done card (read-only).
import sqlite3, time, os

DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
TEN = "BLENDER-MCP-SKILL-1016"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

rows = con.execute(
    "SELECT id, status, title, completed_at FROM tasks WHERE tenant=? ORDER BY created_at", (TEN,)
).fetchall()
print(f"TOTAL kartu tenant {TEN}: {len(rows)}")
from collections import Counter
c = Counter(r["status"] for r in rows)
print("sensus status:", dict(c))

ids = [r["id"] for r in rows]  # id-list dulu, hindari nested cursor (pitfall 14-10b)
print("\n-- kartu DONE tanpa RANTAI-ACK --")
n_noack = 0
for tid in ids:
    st = con.execute("SELECT status FROM tasks WHERE id=?", (tid,)).fetchone()["status"]
    if st != "done":
        continue
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
    mk = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["n"]
    if ack == 0:
        n_noack += 1
        ttl = con.execute("SELECT title, completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
        age = (now - int(ttl["completed_at"])) / 60.0 if ttl["completed_at"] else -1
        print(f"  {tid} marker={mk} umur_done={age:.0f}m :: {ttl['title'][:70]}")
print(f"done tanpa ACK: {n_noack}")

print("\n-- kartu RUNNING saat ini --")
for r in rows:
    if r["status"] == "running":
        ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
        print(f"  {r['id']} :: {r['title'][:60]} :: event terakhir umur {(now-int(ev))/60:.0f}m" if ev else f"  {r['id']} :: {r['title'][:60]} :: tanpa event")

print("\n-- kartu BLOCKED/TODO terbuka --")
for r in rows:
    if r["status"] in ("blocked", "todo"):
        print(f"  {r['id']} [{r['status']}] :: {r['title'][:70]}")
