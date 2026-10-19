# Ronde senyap 18-10: validasi census blocked vs koreksi SYSMAN-CLEANER + saksi kesegaran.
import sqlite3, os, time, glob

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

now = int(time.time())

# 1) sensus status lengkap (anti DB basi)
cur.execute("SELECT status, COUNT(*) c FROM tasks GROUP BY status ORDER BY c DESC")
print("-- census status --")
for r in cur.fetchall():
    print(f"{r['status']} = {r['c']}")

# 2) umur event terakhir (MAX, bukan MIN)
cur.execute("SELECT MAX(created_at) m FROM task_events")
m = cur.fetchone()["m"]
print(f"last_task_event age_min = {(now - m)/60:.1f}" if m else "no events")

# 3) kartu blocked: ada koreksi SYSMAN-CLEANER / marker Digantikan / ACK di komentar?
ids = [r["id"] for r in cur.execute("SELECT id FROM tasks WHERE status='blocked'").fetchall()]
print(f"\n-- blocked census ({len(ids)}) --")
uncorrected = []
for tid in ids:
    c2 = con.cursor()
    rows = c2.execute(
        "SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 5",
        (tid,),
    ).fetchall()
    bodies = [r["body"] for r in rows]
    fixed = any("[SYSMAN-CLEANER" in b for b in bodies)
    replaced = any(b.strip().startswith("Digantikan ") for b in bodies)
    acked = any("RANTAI-ACK" in b for b in bodies)
    last_age = (now - rows[-1]["created_at"]) / 60 if False else ((now - rows[0]["created_at"]) / 60 if rows else None)
    if not (fixed or replaced or acked):
        t = con.execute("SELECT title, tenant, created_at FROM tasks WHERE id=?", (tid,)).fetchone()
        uncorrected.append((tid, t["title"], t["tenant"], (now - t["created_at"]) / 86400.0, len(rows)))
print(f"blocked tanpa koreksi SYSMAN-CLEANER/Digantikan/ACK = {len(uncorrected)}")
for tid, title, tenant, age_d, ncom in uncorrected:
    print(f"  {tid} | {title[:60]} | tenant={tenant} | umur={age_d:.1f}h | komentar={ncom}")

# 4) kartu running/todo (blind-spot rute-4b mustahil bila nol)
cur.execute("SELECT status, COUNT(*) c FROM tasks WHERE status IN ('running','todo','in_progress') GROUP BY status")
rw = cur.fetchall()
print("\n-- running/todo/in_progress --")
print("NOL" if not rw else "\n".join(f"{r['status']} = {r['c']}" for r in rw))

# 5) saksi scheduler hidup: mtime cron output sysman + rantai watch
for pat in [
    r"C:/Users/TRIAL/AppData/Local/hermes/profiles/gsp-system-manager/cron/output/*/*.md",
    r"C:/Users/TRIAL/AppData/Local/hermes/profiles/gsp-system-manager/cron/output/*/*",
]:
    files = glob.glob(pat)
    if files:
        newest = max(files, key=os.path.getmtime)
        print(f"newest cron output = {(now - os.path.getmtime(newest))/60:.1f} min -> {os.path.basename(newest)}")
        break

# 6) heartbeat gateway segar (<5 mnt) vs set wajib
hb = []
home = r"C:/Users/TRIAL/AppData/Local/hermes"
cands = glob.glob(home + r"/profiles/*/state/gateway.heartbeat") + [home + r"/state/gateway.heartbeat"]
for p in cands:
    try:
        age = now - os.path.getmtime(p)
        prof = p.split(os.sep)[-3] if "profiles" in p else "default"
        hb.append((prof, age))
    except OSError:
        pass
fresh = sorted([x for x in hb if x[1] < 300], key=lambda x: x[1])
print(f"\ngateway heartbeat fresh(<5m) = {len(fresh)}: " + ", ".join(p for p, _ in fresh))
con.close()
