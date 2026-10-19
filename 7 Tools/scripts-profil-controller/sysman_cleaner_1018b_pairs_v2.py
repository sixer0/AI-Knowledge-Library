#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifikasi pasangan 'Digantikan' 33 induk VBCB: ambil komentar ASLI (author gsp-master01,
body diawali 'Digantikan'), cek status pengganti satu-satu dengan id-list dulu (pitfall nested)."""
import os, sqlite3, time, pathlib, re, collections

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
now = int(time.time())
con = sqlite3.connect(str(HOME / 'kanban.db'))
con.row_factory = sqlite3.Row

CUT = now - 3 * 3600
ids = [r['task_id'] for r in con.execute(
    "SELECT DISTINCT task_id FROM task_comments WHERE body LIKE '%ORPHAN-TAG%' AND created_at>?", (CUT,))]

pairs = []
for tid in ids:
    d = con.execute("SELECT body FROM task_comments WHERE task_id=? AND body LIKE 'Digantikan%' "
                    "AND author NOT IN ('sysmanager-cleaner','board-cleaner') "
                    "ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    if not d:
        continue
    m = re.search(r'(t_[0-9a-f]{8})', d['body'])
    pairs.append((tid, m.group(1) if m else '?'))
print(f"induk_dengan_marker_Digantikan={len(pairs)}")
st = collections.Counter()
belum = []
for tid, pid in pairs:
    p = con.execute("SELECT status FROM tasks WHERE id=?", (pid,)).fetchone()
    s = p['status'] if p else 'HILANG'
    st[s] += 1
    if s not in ('done', 'archived'):
        belum.append((tid, pid, s))
print(f"distribusi_status_pengganti={dict(st)}")
print(f"pengganti_belum_tuntas={belum}")
