#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe perbaikan 18-10: pasangan Digantikan (spasi non-ASCII!), bukti blok 5 kartu assignee-lama."""
import os, sqlite3, time, pathlib, re, collections

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
now = int(time.time())
con = sqlite3.connect(str(HOME / 'kanban.db'))
con.row_factory = sqlite3.Row

CUT = now - 3 * 3600
ids = [r['task_id'] for r in con.execute(
    "SELECT DISTINCT task_id FROM task_comments WHERE body LIKE '%ORPHAN-TAG%' AND created_at>?", (CUT,))]
print(f"kartu_tertagih_ronde_ini={len(ids)}")

print("\n=== A. PASANGAN DIGANTIKAN (polanya tanpa ' t_') ===")
st = collections.Counter()
belum = []
npair = 0
for tid in ids:
    d = con.execute("SELECT body FROM task_comments WHERE task_id=? AND body LIKE '%Digantikan%' "
                    "ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    if not d:
        continue
    m = re.search(r'Digantikan\s+(t_[0-9a-f]{8})', d['body'])
    if not m:
        belum.append((tid, 'REGEX-GALAT', repr(d['body'][:40])))
        continue
    npair += 1
    p = con.execute("SELECT status FROM tasks WHERE id=?", (m.group(1),)).fetchone()
    s = p['status'] if p else 'HILANG'
    st[s] += 1
    if s not in ('done', 'archived'):
        belum.append((tid, m.group(1), s))
print(f"berpasangan={npair} distribusi={dict(st)} belum_done={belum}")

print("\n=== B. BUKTI ASAL-BLOK 5 KARTU ASSIGNEE-LAMA ===")
for tid in ('t_ff13e0e6', 't_87058aef', 't_2a3b78f9', 't_425f4e08', 't_309a2522'):
    print(f"\n{tid}:")
    ev = list(con.execute(
        "SELECT kind, created_at, substr(COALESCE(payload,''),1,120) p FROM task_events "
        "WHERE task_id=? AND kind IN ('blocked','created') ORDER BY created_at LIMIT 3", (tid,)))
    for e in ev:
        print(f"  ev[{e['kind']}] {(now-e['created_at'])/86400:.0f}h: {e['p']}")
    c = con.execute("SELECT author, substr(body,1,140) b, created_at FROM task_comments WHERE task_id=? "
                    "AND body NOT LIKE '%ORPHAN-TAG%' AND body NOT LIKE '%SYSMAN-CLEANER%' "
                    "AND body NOT LIKE '%RANTAI-WAKE%' ORDER BY created_at ASC LIMIT 2", (tid,)).fetchall()
    for x in c:
        print(f"  kmt_pertama[{x['author']}]: {x['b']}")

print("\n=== C. STATUS TERAKHIR tenant VBCB ringkas ===")
for r in con.execute("SELECT status, COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status"):
    print(f"  {r['status']}: {r['n']}")
con.close()
