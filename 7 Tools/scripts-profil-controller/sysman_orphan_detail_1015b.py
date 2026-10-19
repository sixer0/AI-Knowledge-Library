#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sysman cron 15-10b: vonis mendalam 5 kandidat + blind spot running (read-only)."""
import json, os, sqlite3, time, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
con = sqlite3.connect(HOME / 'kanban.db')
con.row_factory = sqlite3.Row
now = int(time.time())

IDS = ["t_ff13e0e6", "t_87058aef", "t_2a3b78f9", "t_425f4e08", "t_309a2522"]

for tid in IDS:
    r = con.execute("SELECT id,title,status,assignee,tenant,created_by,created_at,block_kind,body FROM tasks WHERE id=?", (tid,)).fetchone()
    print("=" * 100)
    print(f"CARD {tid} status={r['status']} assignee={r['assignee']} tenant={r['tenant']} created_by={r['created_by']} created={time.strftime('%Y-%m-%d %H:%M', time.localtime(r['created_at']))} block_kind={r['block_kind']}")
    body = (r['body'] or '').replace('\n', ' ')
    print(f"BODY[:300]: {body[:300]}")
    # exact order of tag vs correction
    cs = list(con.execute("SELECT author, created_at, substr(replace(body, char(10),' '),1,200) b FROM task_comments WHERE task_id=? ORDER BY created_at ASC", (tid,)))
    for c in cs:
        print(f"  COMMENT [{time.strftime('%m-%d %H:%M', time.localtime(c['created_at']))}] {c['author']}: {c['b']}")
    # tenant census
    ten = r['tenant']
    if ten:
        cen = list(con.execute("SELECT status, COUNT(*) n FROM tasks WHERE tenant=? GROUP BY status", (ten,)))
        print(f"  TENANT_CENSUS {ten}: " + ", ".join(f"{x['status']}={x['n']}" for x in cen))

print("=" * 100)
# Blind spot: running cards heartbeat check
print("\nRUNNING_CARDS:")
for r in con.execute("SELECT id,title,assignee,tenant,last_heartbeat_at,current_run_id FROM tasks WHERE status='running'"):
    tid = r['id']
    le = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (tid,)).fetchone()[0] or 0
    hb = r['last_heartbeat_at'] or 0
    nl = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (tid,)).fetchone()[0]
    na = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()[0]
    print(f"  {tid} ev_age_min={(now-le)/60:.0f} hb_age_min={(now-hb)/60:.0f} lap={nl} ack={na} t={(r['title'] or '')[:50]}")

print("\nOPEN_BY_STATUS (blocked/review/todo idle>24h BEFORE any comment reset, using last NON-comment event):")
for r in con.execute("SELECT id,title,status,assignee,tenant FROM tasks WHERE status IN ('blocked','review','todo')"):
    tid = r['id']
    le_nc = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=? AND kind != 'commented'", (tid,)).fetchone()[0] or 0
    idle_nc_h = (now - le_nc) / 3600
    if idle_nc_h >= 24:
        ntag = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%ORPHAN-TAG%'", (tid,)).fetchone()[0]
        nsys = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND author='sysmanager-cleaner'", (tid,)).fetchone()[0]
        print(f"  {tid} {r['status']} idle_noCommentEv={idle_nc_h:.0f}h tags={ntag} sysman={nsys} assignee={r['assignee']} t={(r['title'] or '')[:45]}")
