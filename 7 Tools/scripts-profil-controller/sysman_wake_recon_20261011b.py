#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rekonsiliasi selisih replika detail_v2 (WAKE=1) vs scan() kanonis (kosong),
plus cek kartu running tunggal. READ-ONLY."""
import importlib.util
import os
import sqlite3
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
IDS = ["t_9fbba251", "t_dbd77711", "t_478595eb", "t_a4c8b843",
       "t_d7fa5da4", "t_fda23cbb", "t_f3639fb7", "t_6537fbe6",
       "t_bd122a56", "t_91f3d6df", "t_885a4eb8"]
RUNNING = "t_2d7495cc"

spec = importlib.util.spec_from_file_location("wake_scan", os.path.join(HERE, "gsp_mission_wake_scan.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

now = int(time.time())
con = mod.connect_ro(DB)
rows = mod.scan(DB, now, "default,sysmanager-cleaner,mission-wake".split(","))
print("CANONICAL_SCAN findings =", len(rows))
for r in rows:
    print("  WAKE", *r)

for tid in IDS:
    t = con.execute("SELECT id,status,tenant,assignee,title,completed_at FROM tasks WHERE id LIKE ?", (tid + "%",)).fetchone()
    if not t:
        print(f"[{tid}] TIDAK ADA"); continue
    ev = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=? AND kind IN ('completed','blocked')", (t["id"],)).fetchone()[0]
    age = round((now - ev) / 60.0, 1) if ev else None
    lap = con.execute("SELECT author,created_at FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%' ORDER BY id DESC LIMIT 1", (t["id"],)).fetchone()
    acks = con.execute("SELECT author,created_at,body FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY id", (t["id"],)).fetchall()
    wake_marker = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (t["id"],)).fetchone()[0]
    exempt = any((a["author"] or "") != ((lap["author"] if lap else "") or "~") for a in acks)
    print(f"[{t['id'][:12]}] status={t['status']} tenant={t['tenant']!r} assignee={t['assignee']!r} terminal_ev_age_min={age}")
    print(f"    LAPOR_author={lap['author'] if lap else None} | ACK n={len(acks)} authors={[a['author'] for a in acks]} | rute4b_exempt={exempt} | wake_markers={wake_marker}")
    print(f"    title={t['title'][:70]}")

print("-- RUNNING --")
t = con.execute("SELECT id,status,title,started_at,last_heartbeat_at,max_runtime_seconds,current_run_id,tenant,assignee FROM tasks WHERE id=?", (RUNNING,)).fetchone()
if t:
    hb_age = round((now - t["last_heartbeat_at"]) / 60.0, 1) if t["last_heartbeat_at"] else None
    st_age = round((now - t["started_at"]) / 60.0, 1) if t["started_at"] else None
    print(f"[{t['id']}] status={t['status']} tenant={t['tenant']!r} assignee={t['assignee']!r} started_age_min={st_age} heartbeat_age_min={hb_age} max_runtime={t['max_runtime_seconds']}")
    print(f"    title={t['title'][:80]}")
    evs = con.execute("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY id DESC LIMIT 5", (RUNNING,)).fetchall()
    for e in evs:
        print(f"    ev {e['kind']} age_min={round((now-e['created_at'])/60.0,1)}")
    cs = con.execute("SELECT author,substr(body,1,90),created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 3", (RUNNING,)).fetchall()
    for c in cs:
        print(f"    cm {c['author']} age_min={round((now-c['created_at'])/60.0,1)} :: {c[1]!r}")
    runs = con.execute("SELECT outcome,started_at,ended_at FROM task_runs WHERE task_id=? ORDER BY id DESC LIMIT 3", (RUNNING,)).fetchall()
    for r in runs:
        print(f"    run outcome={r['outcome']} ended_age_min={round((now-(r['ended_at'] or r['started_at']))/60.0,1) if (r['ended_at'] or r['started_at']) else None}")
