# Ronde senyap 18-10: saksi scheduler + sensus blocked + keadaan kartu beku t_841f18dc
import sqlite3, os, time, json
from datetime import datetime

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
now = time.time()

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def age_min(ts):
    return round((now - ts) / 60.0, 1) if ts else None

# 1) kesegaran papan: MAX event & MAX komentar (JANGAN MIN)
r = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()
print("last_task_event_age_min =", age_min(r["m"]))
r = con.execute("SELECT MAX(created_at) m FROM task_comments").fetchone()
print("last_comment_age_min =", age_min(r["m"]))

# 2) sensus status lengkap
print("-- census --")
for row in con.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(row["status"], "=", row["n"])

# 3) blocked: koreksi terakhir? kelas?
print("-- blocked detail --")
ids = [row["id"] for row in con.execute("SELECT id FROM tasks WHERE status='blocked' ORDER BY id")]
uncorrected = []
for tid in ids:
    c = con.execute(
        "SELECT body, author, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1",
        (tid,)
    ).fetchone()
    body = (c["body"] if c else "") or ""
    head = body[:70].replace("\n", " ")
    ok = ("SYSMAN-CLEANER" in body) or body.startswith("Digantikan")
    if not ok:
        uncorrected.append((tid, head))
print("blocked_total =", len(ids), "| tanpa_koreksi_bersih =", len(uncorrected))
for tid, head in uncorrected:
    print("  UNC:", tid, "|", head)

# 4) kartu beku t_841f18dc: status, event terakhir, komentar terakhir
print("-- t_841f18dc --")
t = con.execute("SELECT id,status,title,created_at,completed_at FROM tasks WHERE id LIKE 't_841f18dc%'").fetchone()
if t:
    print("status =", t["status"], "| title =", (t["title"] or "")[:80])
    e = con.execute("SELECT kind, MAX(created_at) m FROM task_events WHERE task_id=?", (t["id"],)).fetchone()
    print("last_event =", e["kind"], "age_min =", age_min(e["m"]))
    c = con.execute("SELECT author, substr(body,1,90) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (t["id"],)).fetchall()
    for row in c:
        print("  cmt:", row["author"], "|", age_min(row["created_at"]), "mnt |", row["b"].replace("\n", " "))
else:
    print("TIDAK DITEMUKAN")

# 5) saksi scheduler hidup: mtime berkas cron output terbaru (sysman + rantai watch)
print("-- cron output mtime --")
for jobdir in ["d4d2ccf55163"]:
    p = os.path.join(HOME, "profiles/gsp-system-manager/cron/output", jobdir)
    if os.path.isdir(p):
        files = sorted(os.listdir(p), key=lambda f: os.path.getmtime(os.path.join(p, f)), reverse=True)[:3]
        for f in files:
            mt = os.path.getmtime(os.path.join(p, f))
            print(jobdir, f, "age_min =", age_min(mt))

# 6) heartbeat gateway segar (<300 dtk) pada set wajib monitor
print("-- gateway heartbeat --")
import glob
hb_paths = glob.glob(os.path.join(HOME, "profiles/*/state/gateway.heartbeat"))
hb_paths.append(os.path.join(HOME, "state/gateway.heartbeat"))  # default = root
fresh = 0
for hp in hb_paths:
    try:
        mt = os.path.getmtime(hp)
        prof = hp.split(os.sep)
        name = prof[-3] if "profiles" in prof else "default"
        a = age_min(mt)
        if a is not None and a < 5:
            fresh += 1
        print(name, "hb_age_min =", a)
    except Exception as ex:
        print(hp, "ERR", ex)
print("fresh_lt5min =", fresh)
con.close()
