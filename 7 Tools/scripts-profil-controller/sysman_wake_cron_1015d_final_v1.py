#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""15-10 sysman ronde-3: sampel reason kartu blocked VBCB + cek LAPOR/PARKED + re-scan kanonis."""
import os
import sqlite3
import sys
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())
TEN = "VIBE-BIBLE-1013"

print("== Sampel 3 kartu blocked: payload event blocked + komentar terakhir ==")
rows = con.execute("SELECT id, title FROM tasks WHERE tenant=? AND status='blocked' ORDER BY id LIMIT 3", (TEN,)).fetchall()
for r in rows:
    print("-" * 60)
    print(r["id"], "|", r["title"][:60])
    ev = con.execute("SELECT kind, substr(replace(payload, char(10),' '),1,220) AS p, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (r["id"],)).fetchall()
    for e in ev:
        print("  ev[%s @%dmnt]: %s" % (e["kind"], (now - e["created_at"]) // 60, e["p"]))
    cs = con.execute("SELECT author, substr(replace(body, char(10),' '),1,200) AS b, created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 2", (r["id"],)).fetchall()
    for c in cs:
        print("  cmt[%s @%dmnt]: %s" % (c["author"], (now - c["created_at"]) // 60, c["b"]))

print("\n== Kartu blocked ber-LAPOR/PARKED? ==")
n = con.execute("SELECT COUNT(*) AS n FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant=? AND t.status='blocked' AND (c.body LIKE '%LAPOR-SELESAI%' OR c.body LIKE '%PARKED%')", (TEN,)).fetchone()["n"]
print("komentar LAPOR/PARKED pada kartu blocked:", n)

print("\n== Event unblocked sepanjang masa tenan (terakhir kapan) ==")
r = con.execute("SELECT MAX(e.created_at) AS ts, COUNT(*) AS n FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.kind='unblocked'", (TEN,)).fetchone()
print("unblocked_total=%s terakhir_umur=%s mnt" % (r["n"], ((now - r["ts"]) // 60) if r["ts"] else "-"))

print("\n== RE-SCAN KANONIS (importlib scan()) ==")
sys.path.insert(0, os.path.dirname(DB))
import importlib.util
spec = importlib.util.spec_from_file_location("wake_scan", os.path.join(DB.rsplit(os.sep, 1)[0], "scripts", "gsp_mission_wake_scan.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
findings = mod.scan(DB, int(time.time()), mod.DEFAULT_AUTHORS.split(","))
from collections import Counter
cls = Counter(f[1] for f in findings)
print("total_baris=%d kelas=%s" % (len(findings), dict(cls)))
ids_done_unacked = [f[0] for f in findings if f[1] == "done-unacked"]
print("done-unacked ids:", ids_done_unacked if ids_done_unacked else "(kosong)")
con.close()
