# Ronde cron 16-10: kenapa 34 kartu terbuka VIBE-BIBLE-1013 tidak ditagih (gerbang dedup vs buta-tutup)
import sqlite3, time
HOME = "C:/Users/TRIAL/AppData/Local/hermes"
now = int(time.time())
con = sqlite3.connect(HOME + "/kanban.db")
con.row_factory = sqlite3.Row
BASE = ["default", "sysmanager-cleaner", "mission-wake"]

rows = con.execute("SELECT id,status,created_by FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status NOT IN ('done','archived')").fetchall()
print("open cards =", len(rows))
stall_worthy = 0
for r in rows:
    cid = r["id"]
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (cid,)).fetchone()["m"]
    if ev is None:
        continue
    age = int((now - ev) // 60)
    authors = BASE + ([r["created_by"]] if r["created_by"] and r["created_by"] not in BASE else [])
    ph = ",".join("?" * len(authors))
    ctrl = con.execute(f"SELECT 1 FROM task_comments c WHERE c.task_id=? AND c.author IN ({ph}) AND c.created_at>=? LIMIT 1", [cid]+authors+[ev]).fetchone()
    mk = con.execute("SELECT 1 FROM task_comments c WHERE c.task_id=? AND c.body LIKE '%RANTAI-WAKE stalled%' AND c.created_at>=? LIMIT 1", (cid, ev)).fetchone()
    if age > 30 and not ctrl and not mk:
        stall_worthy += 1
        print("  TIDAK TERGATEN:", cid, "age=", age)
print("stall-worthy tanpa gerbang =", stall_worthy)

# sample alasan blocked + jejak triase terakhir per tenant
print("\n-- penahan: marker vs komentar controller (per kartu) --")
mk_only = ctrl_only = both = 0
ids = [r["id"] for r in rows]
for cid in ids:
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (cid,)).fetchone()["m"]
    r = con.execute("SELECT created_by,status FROM tasks WHERE id=?", (cid,)).fetchone()
    authors = BASE + ([r["created_by"]] if r["created_by"] and r["created_by"] not in BASE else [])
    ph = ",".join("?" * len(authors))
    ctrl = con.execute(f"SELECT author FROM task_comments c WHERE c.task_id=? AND c.author IN ({ph}) AND c.created_at>=? LIMIT 1", [cid]+authors+[ev]).fetchone()
    mk = con.execute("SELECT 1 FROM task_comments c WHERE c.task_id=? AND c.body LIKE '%RANTAI-WAKE stalled%' AND c.created_at>=? LIMIT 1", (cid, ev)).fetchone()
    if mk and not ctrl: mk_only += 1
    elif ctrl and not mk: ctrl_only += 1
    else: both += 1
print("  hanya_marker_sysman=%d hanya_komentar_controller=%d keduanya/lain=%d" % (mk_only, ctrl_only, both))
print("\n-- status terbuka --")
for r in con.execute("SELECT status,COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status NOT IN ('done','archived') GROUP BY status"):
    print("  ", r["status"], r["n"])
print("\n-- komentar triase terbaru tenant ini --")
for r in con.execute("SELECT t.id,c.author,substr(c.body,1,70) b,c.created_at FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant='VIBE-BIBLE-1013' ORDER BY c.created_at DESC LIMIT 5"):
    print("  ", r["id"], r["author"], round((now-r["created_at"])/60.0), "mnt |", r["b"])
print("\n-- lepas-blokir (unblocked) 24 jam terakhir --")
n = con.execute("SELECT COUNT(*) n FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='unblocked' AND e.created_at >= ?", (now-86400,)).fetchone()["n"]
print("  unblocked_24h =", n)
con.close()
