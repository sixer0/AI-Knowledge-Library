#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sysman cron 15-10d: sensus kartu terbuka per tenant + umur event (read-only)."""
import os, sqlite3, time, pathlib
HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
con = sqlite3.connect(HOME / 'kanban.db')
con.row_factory = sqlite3.Row
now = int(time.time())

print("STATUS_CENSUS:", dict((r['status'], r['n']) for r in con.execute(
    "SELECT status, COUNT(*) n FROM tasks WHERE status IN ('blocked','review','todo','running') GROUP BY status")))

print("\nOPEN_BY_TENANT (>=1 open card):")
q = """SELECT COALESCE(NULLIF(tenant,''),'(null)') ten, status, COUNT(*) n,
       MIN((SELECT MAX(created_at) FROM task_events e WHERE e.task_id=t.id)) mev
       FROM tasks t WHERE status IN ('blocked','review','todo','running') GROUP BY ten, status"""
agg = {}
for r in con.execute(q):
    age_h = (now - (r['mev'] or 0)) / 3600
    d = agg.setdefault(r['ten'], {})
    d[r['status']] = (r['n'], round(age_h))
for ten, d in sorted(agg.items(), key=lambda kv: -sum(v[0] for v in kv[1].values())):
    tot = sum(v[0] for v in d.values())
    print(f"  {ten}: total={tot} " + " ".join(f"{s}={n}(lastev {a}j)" for s, (n, a) in d.items()))

print("\nOPEN_ASSIGNEE_CENSUS:")
for r in con.execute("SELECT COALESCE(NULLIF(assignee,''),'(none)') a, COUNT(*) n FROM tasks WHERE status IN ('blocked','review','todo','running') GROUP BY a ORDER BY n DESC"):
    print(f"  {r['a']}={r['n']}")
