# -*- coding: utf-8 -*-
# Ronde cron 1015c final: (a) cek ACK mendarat di 4 kartu running; (b) rem CHECKPOINT di kartu gave_up;
# (c) census gave_up per tenant 24 jam; (d) re-scan kanonis via import modul scan().
import sqlite3, time, json, importlib.util, sys

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

def age(ts):
    return round((NOW - ts) / 60.0) if ts else None

print("== 4 RUNNING: komentar terbaru (ACK?) ==")
for tid in ["t_ccfca3b8","t_de326482","t_de73c01d","t_deb670d0"]:
    cmts = con.execute("SELECT author, created_at, substr(body,1,70) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,)).fetchall()
    st = con.execute("SELECT status FROM tasks WHERE id=?", (tid,)).fetchone()
    print("###", tid, "status=", st["status"])
    for c in cmts:
        print("   -", c["author"], age(c["created_at"]), "m |", c["b"].replace("\n"," "))

print("\n== CONTOH KARTU GAVE_UP: komentar terbaru (rem CHECKPOINT?) ==")
for tid in ["t_d3cc135a","t_e5e2e083"]:
    t = con.execute("SELECT title FROM tasks WHERE id=?", (tid,)).fetchone()
    print("###", tid, "|", (t["title"] or "")[:55])
    for c in con.execute("SELECT author, created_at, substr(body,1,200) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (tid,)).fetchall():
        print("   -", c["author"], age(c["created_at"]), "m |", c["b"].replace("\n"," ")[:190])

print("\n== CENSUS gave_up 24 jam per tenant ==")
rows = con.execute("""SELECT t.tenant, COUNT(DISTINCT e.task_id) n FROM task_events e JOIN tasks t ON t.id=e.task_id
WHERE e.kind='gave_up' AND e.created_at > ? GROUP BY t.tenant""", (NOW-86400,)).fetchall()
for r in rows: print(r["tenant"], r["n"])

print("\n== RE-SCAN KANONIS ==")
spec = importlib.util.spec_from_file_location("mws", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
sys.argv = ["gsp_mission_wake_scan.py"]
spec.loader.exec_module(mod)
fn = getattr(mod, "scan", None)
if fn:
    authors = mod.DEFAULT_AUTHORS
    if isinstance(authors, str): authors = authors.split(",")
    out = fn(DB, int(time.time()), authors)
    lines = out if isinstance(out, list) else [out]
    n = 0
    for line in lines:
        s = str(line)
        if s.strip():
            n += 1
            print(s)
    print("total_wake_lines=", n)
else:
    print("scan() tidak ditemukan; nama:", [x for x in dir(mod) if not x.startswith("_")][:20])
