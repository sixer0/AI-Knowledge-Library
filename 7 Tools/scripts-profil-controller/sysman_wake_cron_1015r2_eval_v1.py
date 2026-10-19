#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde cron 15-10b: nilai 33 baris stalled umur-seragam + census tenant + sanity papan.
Read-only (mode=ro, query_only). Tidak menulis apa pun ke DB."""
import json
import os
import re
import sqlite3
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())

IDS = ["t_002af121","t_0311d1e4","t_0bf0854c","t_1168e59f","t_14e7030f","t_153594d4",
"t_1c98456a","t_23f7da05","t_2e0e92d4","t_34bf2edc","t_3782b61a","t_397be920","t_46ff8be6",
"t_5831a79d","t_60ed37fa","t_7391c81b","t_77a9bcd3","t_799a1879","t_95b5b6cb","t_99418ea0",
"t_9bf75422","t_9e457da5","t_9ebc8fbc","t_a064e4cc","t_a37d190b","t_a48e52d1","t_a4b6791b",
"t_c8784acc","t_cb601d70","t_d4fca8b3","t_e04bca14","t_efb6071f","t_f9ac1ff2"]

print("== SANITY PAPAN ==")
r = con.execute("SELECT MAX(created_at) AS mx, COUNT(*) AS n FROM task_events").fetchone()
print("events_total=%s last_event_age_min=%s" % (r["n"], int((now - r["mx"]) // 60)))
r = con.execute("SELECT COUNT(*) AS n FROM tasks").fetchone()
print("tasks_total=%s" % r["n"])

print("\n== PER-KARTU WAKE ==")
tenants = {}
for tid in IDS:
    t = con.execute("SELECT id,title,status,tenant,created_by,created_at FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print("%s MISSING" % tid); continue
    ev = con.execute("SELECT kind, MAX(created_at) AS mx FROM task_events WHERE task_id=?", (tid,)).fetchone()
    parents = [p["parent_id"] for p in con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,))]
    # status orang tua
    pstat = []
    for pid in parents:
        pt = con.execute("SELECT status FROM tasks WHERE id=?", (pid,)).fetchone()
        pstat.append((pid, pt["status"] if pt else "?"))
    # komentar 'Digantikan'
    repl = None
    for c in con.execute("SELECT body FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (tid,)):
        m = re.search(r"Digantikan (t_[0-9a-f]{8})", c["body"])
        if m:
            repl = m.group(1); break
    repl_status = None
    if repl:
        rt = con.execute("SELECT status FROM tasks WHERE id=?", (repl,)).fetchone()
        repl_status = rt["status"] if rt else "?"
    ncom = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=?", (tid,)).fetchone()["n"]
    print("%s | %s | tenant=%s | by=%s | last_ev=%s@%smin | parents=%s | replaced_by=%s(%s) | comments=%s" % (
        tid, t["status"], t["tenant"], t["created_by"], ev["kind"] if ev else "?",
        int((now - ev["mx"]) // 60) if ev and ev["mx"] else -1,
        pstat, repl, repl_status, ncom))
    tenants[t["tenant"]] = tenants.get(t["tenant"], 0) + 1

print("\n== CENSUS TENANT ==")
for ten, n in sorted(tenants.items(), key=lambda kv: -kv[1]):
    rows = con.execute("SELECT status, COUNT(*) AS n FROM tasks WHERE tenant=? GROUP BY status", (ten,)).fetchall()
    dist = {rr["status"]: rr["n"] for rr in rows}
    tot = sum(dist.values())
    # ACK census untuk kartu done
    ack_done = 0; done_n = dist.get("done", 0)
    ids_done = [rr["id"] for rr in con.execute("SELECT id FROM tasks WHERE tenant=? AND status='done'", (ten,))]
    for did in ids_done:
        a = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (did,)).fetchone()["n"]
        if a > 0:
            ack_done += 1
    print("tenant=%s wake_rows=%s total=%s dist=%s done_ack=%s/%s" % (ten, n, tot, dist, ack_done, done_n))

print("\n== EVENT TERMINAL RANDE GAGAL (kind timed_out/gave_up/crashed, 24 jam) ==")
rows = con.execute(
    "SELECT kind, COUNT(*) AS n FROM task_events WHERE kind IN ('timed_out','gave_up','crashed') "
    "AND created_at >= ? GROUP BY kind", (now - 24*3600,)).fetchall()
for rr in rows:
    print("kind=%s n=%s" % (rr["kind"], rr["n"]))

print("\n== KARTU RUNNING TENANT-TERPILIH (blind spot) ==")
for ten in tenants:
    for rr in con.execute("SELECT id,status FROM tasks WHERE tenant=? AND status='running'", (ten,)):
        lc = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (rr["id"],)).fetchone()["n"]
        la = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (rr["id"],)).fetchone()["n"]
        evm = con.execute("SELECT MAX(created_at) AS mx FROM task_events WHERE task_id=?", (rr["id"],)).fetchone()["mx"]
        print("running %s tenant=%s lapor=%s ack=%s hb_age_min=%s" % (rr["id"], ten, lc, la, int((now-evm)//60) if evm else -1))
