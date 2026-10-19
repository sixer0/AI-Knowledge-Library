# Rinci ronde 14-10h: 11 done ACK census, CHECKPOINT, kelas wake, keflat-an event.
import sqlite3, time, collections

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

trows = list(con.execute("SELECT id,title,status,completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013'"))
ids = [r["id"] for r in trows]
q = ",".join("?" * len(ids))

# A) Kartu done: ACK author-lain vs LAPOR, marker
print("== KARTU DONE (11) : ACK & MARKER ==")
for r in trows:
    if r["status"] != "done":
        continue
    cs = list(con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (r["id"],)))
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "")]
    ack = [c for c in cs if "RANTAI-ACK" in (c["body"] or "")]
    mark = [c for c in cs if "RANTAI-WAKE done-unacked" in (c["body"] or "")]
    lap_a = {c["author"] for c in lapor}
    ack_o = [c for c in ack if c["author"] not in lap_a]
    done_age = int((now - r["completed_at"]) / 60) if r["completed_at"] else -1
    print(f"  {r['id']} doneAge={done_age}m lap={len(lapor)} ack_lain={len(ack_o)} marker={len(mark)} :: {r['title'][:55]}")

# B) Komentar CHECKPOINT pada kartu blocked
print("\n== KOMENTAR CHECKPOINT (kartu blocked) ==")
cp = list(con.execute(
    f"SELECT task_id, author, substr(replace(body,char(10),' '),1,160) b, created_at FROM task_comments WHERE task_id IN ({q}) AND body LIKE '%CHECKPOINT%' ORDER BY created_at DESC LIMIT 8", ids))
for c in cp:
    print(f"  [{c['task_id']} {c['author']} {(now-c['created_at'])//60}m] {c['b']}")
print("  total komentar CHECKPOINT:", len(list(con.execute(f"SELECT 1 FROM task_comments WHERE task_id IN ({q}) AND body LIKE '%CHECKPOINT%'", ids))))

# C) Kelas wake per kartu (dari pemindai kanonis) - agregat
import importlib.util
spec = importlib.util.spec_from_file_location("ws", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rows = m.scan(DB, now, [a.strip() for a in m.DEFAULT_AUTHORS.split(",")])
cls_card = collections.defaultdict(set)
for r in rows:
    cls_card[r[0]].add(r[1])
agg = collections.Counter()
for tid, cl in cls_card.items():
    st = con.execute("SELECT status FROM tasks WHERE id=?", (tid,)).fetchone()["status"]
    agg[(st, tuple(sorted(cl)))] += 1
print("\n== KELAS WAKE x STATUS ==")
for (st, cl), c in sorted(agg.items()):
    print(f"  {st} {cl}: {c} kartu")

# D) Keplat-an: histogram umur event terakhir per kartu tenant
ages = [int((now - e) / 60) for (e,) in con.execute(
    f"SELECT MAX(created_at) FROM task_events WHERE task_id IN ({q}) GROUP BY task_id", ids) if e]
print(f"\numur event terakhir per kartu: n={len(ages)} min={min(ages)} max={max(ages)} mnt")

# E) Apa yang dikatakan LAPOR terakhir di kartu blocked (sample 3) - rem yang ditawarkan
print("\n== SAMPEL LAPOR TERAKHIR KARTU BLOCKED ==")
n = 0
for r in trows:
    if r["status"] != "blocked" or n >= 3:
        continue
    cs = list(con.execute("SELECT author, substr(replace(body,char(10),' '),1,220) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 2", (r["id"],)))
    print(f"  {r['id']} :: {r['title'][:50]}")
    for c in cs:
        print(f"    [{c['author']} {(now-c['created_at'])//60}m] {c['b']}")
    n += 1

# F) reason blocked sample + apakah ada catatan PARKED
print("\n== EVENT 'blocked' reason (3 terbaru) ==")
for r in con.execute(f"SELECT task_id, created_at, payload FROM task_events WHERE task_id IN ({q}) AND kind='blocked' ORDER BY created_at DESC LIMIT 3", ids):
    print(f"  {r['task_id']} {(now-r['created_at'])//60}m :: {str(r['payload'])[:180]}")
con.close()
