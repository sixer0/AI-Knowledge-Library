#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde cron 15-10b langkah-2: bukti kelas parent-tersingkir + buta-tutup papan + re-scan.
Read-only."""
import os
import re
import sqlite3
import sys
import time
import importlib.util

LOCALAPPDATA = os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local")
DB = os.path.join(LOCALAPPDATA, "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())

PARENTS_BLOCKED = ["t_64328060","t_30dd071c","t_d8480778","t_8b90e854","t_93c6bec3","t_d9f482ab",
"t_4d7a1691","t_ec2342d5","t_c1d55eef","t_674377e1","t_68d1d8be","t_b422fa6d","t_2d32e7c8",
"t_760e7792","t_ba72c512","t_2ae211bb","t_050a75ff","t_483b2d91","t_e8cac74b","t_e5e2e083",
"t_a783103d","t_d3cc135a","t_8d618268","t_c792df45","t_0df60358","t_a3e70bf1","t_be219ab7",
"t_b9500192","t_a931e1b1","t_2543fb8f","t_b81fea6a","t_aaab1be9","t_e4c7440d"]

print("== ORANG TUA BLOCKED (33) ==")
n_digantikan = 0
repl_ids = []
for pid in PARENTS_BLOCKED:
    t = con.execute("SELECT id,status,created_by FROM tasks WHERE id=?", (pid,)).fetchone()
    evs = [e["kind"] for e in con.execute("SELECT kind FROM task_events WHERE task_id=? ORDER BY created_at", (pid,))]
    dig = None
    for c in con.execute("SELECT body FROM task_comments WHERE task_id=? ORDER BY created_at", (pid,)):
        m = re.search(r"Digantikan (t_[0-9a-f]{8})", c["body"])
        if m:
            dig = m.group(1)
    if dig:
        n_digantikan += 1
        repl_ids.append(dig)
    print("%s by=%s kinds=%s digantikan=%s" % (pid, t["created_by"] if t else "?", ",".join(evs[-3:]), dig))
print("TOTAL digantikan-bukti=%s/33" % n_digantikan)

if repl_ids:
    qm = ",".join("?" * len(repl_ids))
    rows = con.execute("SELECT status, COUNT(*) AS n FROM tasks WHERE id IN (%s) GROUP BY status" % qm, repl_ids).fetchall()
    print("STATUS PASANGAN PENGGANTI:", {r["status"]: r["n"] for r in rows})

print("\n== BLIND SPOT PAPAN: running ber-LAPOR tanpa ACK (semua tenant) ==")
ids_run = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE status='running'")]
for rid in ids_run:
    lap = con.execute("SELECT author, MAX(created_at) AS mx FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%' GROUP BY 1", (rid,)).fetchone()
    if not lap:
        continue
    ack = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (rid,)).fetchone()["n"]
    if ack == 0:
        evm = con.execute("SELECT MAX(created_at) AS mx FROM task_events WHERE task_id=?", (rid,)).fetchone()["mx"]
        tt = con.execute("SELECT title, tenant FROM tasks WHERE id=?", (rid,)).fetchone()
        print("CANDIDAT %s tenant=%s hb_age=%smin judul=%.60s" % (rid, tt["tenant"], int((now-evm)//60) if evm else -1, tt["title"]))
print("running_total=%s" % len(ids_run))

print("\n== DONE-UNACKED BARU (rute-4b, tanpa marker) ==")
# kandidat done <6 jam tanpa RANTAI-ACK dan tanpa marker
cands = con.execute(
    "SELECT id, tenant, completed_at FROM tasks WHERE status='done' AND completed_at >= ? AND completed_at <= ?",
    (now - 6*3600, now - 5*60)).fetchall()
for c in cands:
    ack = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (c["id"],)).fetchone()["n"]
    mk = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (c["id"],)).fetchone()["n"]
    if ack == 0 and mk == 0:
        print("DONE-UNACKED %s tenant=%s age=%smin" % (c["id"], c["tenant"], int((now-c["completed_at"])//60)))

print("\n== RE-SCAN KANONIS ==")
spec = importlib.util.spec_from_file_location("wake_scan", os.path.join(LOCALAPPDATA, "hermes", "scripts", "gsp_mission_wake_scan.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
findings = mod.scan(DB, now, mod.DEFAULT_AUTHORS.split(","))
from collections import Counter
print("total_baris=%s per_kelas=%s" % (len(findings), dict(Counter(k for _, k, _ in findings))))
