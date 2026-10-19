#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Umur penanda RANTAI-WAKE pada 4 kartu RO01 tenant-kosong + re-scan final."""
import importlib.util, os, sqlite3, time
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
spec = importlib.util.spec_from_file_location("wake_scan", os.path.join(HERE, "gsp_mission_wake_scan.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
now = int(time.time())
con = mod.connect_ro(DB)
for tid in ["t_9fbba251","t_dbd77711","t_478595eb","t_a4c8b843"]:
    r = con.execute("SELECT author,created_at,body FROM task_comments WHERE task_id LIKE ? AND body LIKE '%RANTAI-WAKE%' ORDER BY id DESC LIMIT 1", (tid+"%",)).fetchone()
    comp = con.execute("SELECT completed_at FROM tasks WHERE id LIKE ?", (tid+"%",)).fetchone()[0]
    print(f"{tid}: marker author={r['author']} age_min={round((now-r['created_at'])/60,1)} :: {r['body'][:60]!r} | completed_age_min={round((now-comp)/60,1) if comp else None}")
print("FINAL_SCAN rows =", len(mod.scan(DB, now, "default,sysmanager-cleaner,mission-wake".split(","))))
