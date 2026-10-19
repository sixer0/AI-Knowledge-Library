# Rekonsiliasi ronde cron 12-10: scan() kanonis + cek jendela waktu kandidat longgar
import importlib.util, sqlite3, time, os, json

HERMES = os.path.expandvars(r"C:/Users/TRIAL/AppData/Local/hermes")
DB = os.path.join(HERMES, "kanban.db")
SCAN = os.path.join(HERMES, "scripts", "gsp_mission_wake_scan.py")

spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

now = int(time.time())
authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")

rows = mod.scan(DB, now, authors)
print("CANONICAL_SCAN rows =", len(rows))
for r in rows:
    print("WAKE:", r)

con = sqlite3.connect(DB)
cur = con.cursor()

# ambang yang dibaca dari sumber skrip
for name in ("STALLED_MIN", "RUN_WINDOW_H", "FASE_STALL_MIN", "DONE_UNACKED_MIN"):
    print("THRESH", name, "=", getattr(mod, name, "?"))

# kandidat longgar dari detail_v2: cek umur vs jendela
cands = ["t_090415ec","t_f4de0f1f","t_5d087ab1","t_e034cb5e","t_df6a4a8a","t_a707d4a3"]
q = ("select id,status,completed_at,tenant from tasks where id in (%s)" % ",".join("?"*len(cands)))
for tid, st, comp, tenant in cur.execute(q, cands).fetchall():
    age_h = (now - comp)/3600.0 if comp else -1
    print("CAND", tid, "status=", st, "done_age_h=%.1f" % age_h, "tenant=", repr(tenant))

# event terminal <=6 jam tanpa syarat tenant (sapuan buta-tutup rute-4b)
cut = now - 6*3600
n = cur.execute("select count(*) from task_events where created_at >= ?", (cut,)).fetchone()[0]
print("EVENTS_last6h =", n)
term = cur.execute(
    "select e.task_id, e.kind, e.created_at, t.status, t.tenant "
    "from task_events e join tasks t on t.id=e.task_id "
    "where e.created_at >= ? and e.kind in ('completed','done','parked','blocked') "
    "order by e.created_at desc limit 20", (cut,)).fetchall()
print("TERMINAL_EVENTS_last6h =", len(term))
for row in term:
    print("TERM:", row[0], row[1], "%.1fh" % ((now-row[2])/3600.0), row[3], repr(row[4]))
con.close()
