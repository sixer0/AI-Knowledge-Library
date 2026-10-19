# -*- coding: utf-8 -*-
# Ronde 1015r4 tahap-2: vonis kanonis scan() lewat NILAI KEMBALIAN (bukan stdout),
# rincian 8 kandidat blind-spot done-unacked non-tenant, dan 10 blocked non-tenant.
import sqlite3, time, importlib.util

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
spec = importlib.util.spec_from_file_location("ws", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
authors = mod.DEFAULT_AUTHORS
if isinstance(authors, str): authors = authors.split(",")
print("DEFAULT_AUTHORS:", authors)
print("STALLED_MIN:", mod.STALLED_MIN, "| RUN_WINDOW_H:", mod.RUN_WINDOW_H,
      "| FASE_STALL_MIN:", mod.FASE_STALL_MIN, "| DONE_UNACKED_MIN:", mod.DONE_UNACKED_MIN,
      "| WINDOW:", getattr(mod, "DONE_UNACKED_WINDOW", "?"), "| CUTOFF:", getattr(mod, "DONE_UNACKED_CUTOFF", "?"))
rows = mod.scan(DB, NOW, authors)
print("HASIL scan():", len(rows))
from collections import Counter
print("kelas:", dict(Counter(r[1] for r in rows)))
for r in rows[:40]: print(" ", r)

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
def age(ts): return round((NOW-ts)/60.0) if ts else None

CAND = ["t_c6a44d40","t_2b10bac7","t_8439633f","t_dcbc4856","t_ceca2798","t_f1df16f4","t_1264ca56","t_47044688"]
print("\n== 8 KANDIDAT BLIND-SPOT (non-tenant, lap=gspuser02) ==")
for cid in CAND:
    t = con.execute("SELECT id,status,tenant,assignee,created_by,title,completed_at FROM tasks WHERE id=?", (cid,)).fetchone()
    nack_all = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (cid,)).fetchone()["n"]
    ackauth = [a["author"] for a in con.execute("SELECT DISTINCT author FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (cid,)).fetchall()]
    nmark = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (cid,)).fetchone()["n"]
    lapex = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (cid,)).fetchone()["n"]
    tev = con.execute("SELECT kind, MAX(created_at) m FROM task_events WHERE task_id=? AND kind IN ('completed','blocked')", (cid,)).fetchone()
    print(f"{cid} status={t['status']} tenant={t['tenant']!r} assignee={t['assignee']!r} by={t['created_by']}")
    print(f"   title={(t['title'] or '')[:70]}")
    print(f"   completed_ev={tev['kind'] if tev else None}@{age(tev['m']) if tev else '?'}m | LAPOR-SELESAI(exak)={lapex} ACK_total={nack_all}{ackauth} marker={nmark}")

print("\n== 10 BLOCKED NON-TENANT ==")
for r in con.execute("SELECT id,title,created_by FROM tasks WHERE status='blocked' AND (tenant IS NULL OR tenant != 'VIBE-BIBLE-1013')").fetchall():
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    c = con.execute("SELECT author, body FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    print(f"{r['id']} ev={age(ev)}m by={r['created_by']} {(r['title'] or '')[:55]}")
    print(f"   last_comment[{c['author'] if c else '-'}]: {(c['body'] if c else '-')[:90]}")

print("\n== APAKAH gspuser02 author terdaftar / controller? ==")
n = con.execute("SELECT COUNT(*) n FROM task_comments WHERE author='gspuser02'").fetchone()["n"]
print("komentar gspuser02 seumur papan:", n)
