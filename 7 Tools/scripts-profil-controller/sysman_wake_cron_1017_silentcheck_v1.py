# Ronde senyap 17-10: replika scan() kanonis + kesegaran event + sensus blocked
import sqlite3, os, time, importlib.util, sys

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
SCAN = os.path.join(HOME, "scripts", "gsp_mission_wake_scan.py")
now = int(time.time())

# 1) panggil scan() kanonis (importlib), tangkap nilai kembaliannya
spec = importlib.util.spec_from_file_location("mws", SCAN)
mws = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mws)
authors = getattr(mws, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")
findings = mws.scan(DB, now, authors)
print("SCAN findings =", len(findings))
for f in findings:
    print("  ROW:", tuple(f))

con = sqlite3.connect(DB)
con.row_factory = None
cur = con.cursor()

# 2) kesegaran papan: MAX per tabel (BUKAN MIN)
for tbl, col in (("task_events","created_at"),("task_comments","created_at"),("task_runs","started_at")):
    try:
        mx = cur.execute(f"SELECT MAX({col}) FROM {tbl}").fetchone()[0]
        age = (now - float(mx))/60.0 if mx else -1
        print(f"FRESH {tbl}: max_age_min = {age:.1f}")
    except Exception as e:
        print(f"FRESH {tbl}: ERR {e}")

# 3) sensus kartu terbuka non-done/archived
rows = cur.execute("SELECT id,title,status,tenant,created_by,created_at,block_kind FROM tasks WHERE status NOT IN ('done','archived') ORDER BY status, created_at").fetchall()
print("OPEN cards =", len(rows))
for r in rows:
    tid, title, status, tenant, cb, created, bk = r
    # komentar terakhir kartu
    c2 = con.cursor()
    lastc = c2.execute("SELECT author, substr(body,1,90), created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    evmax = c2.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (tid,)).fetchone()[0]
    ev_age = (now - float(evmax))/60.0 if evmax else -1
    marker = ""
    if lastc:
        b = lastc[1] or ""
        toks = ["SYSMAN-CLEANER","RANTAI-WAKE","Digantikan","ANCHOR-KONTRAK","antre rilis","DITAHAN"]
        marker = ",".join(t for t in toks if t in b)
    print(f"  {status} | {tid} | {(title or '')[:48]} | tenant={tenant} | by={cb} | blk={bk} | ev_age={ev_age:.0f}m | lastc=[{lastc[0] if lastc else '-'}]{marker} :: {(lastc[1] if lastc else '(no comment)')[:70]}")
con.close()
