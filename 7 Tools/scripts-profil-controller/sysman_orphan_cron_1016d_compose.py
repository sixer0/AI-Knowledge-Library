# -*- coding: utf-8 -*-
"""Ronde sysman 16-10: verifikasi komposisi tagihan hari ini + umur pra-tagihan (loop aman)."""
import os, sqlite3, time, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
con = sqlite3.connect(str(HOME / 'kanban.db'))
con.row_factory = sqlite3.Row
now = int(time.time())

# 1) semua komentar ORPHAN-TAG hari ini (<= 2 jam terakhir)
today = list(con.execute(
    "SELECT task_id, author, created_at FROM task_comments WHERE body LIKE '%ORPHAN-TAG v1%' AND created_at > ? ORDER BY created_at",
    (now - 7200,)).fetchall())
print(f"TAGIH HARI INI: {len(today)}")
ids = [r['task_id'] for r in today]
# 2) status+tenant per id (id-list dulu, hindari nested-cursor)
info = {}
for r in con.execute(f"SELECT id,status,tenant,assignee,title FROM tasks WHERE id IN ({','.join('?'*len(ids))})", ids):
    info[r['id']] = r
from collections import Counter
cnt = Counter((info[i]['status'], info[i]['tenant'] or '-') for i in ids if i in info)
for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
    print(f"  {k[0]} / {k[1]}: {v}")
vpcb = [i for i in ids if info.get(i) and info[i]['tenant'] == 'VIBE-BIBLE-1013']
nonv = [i for i in ids if info.get(i) and info[i]['tenant'] != 'VIBE-BIBLE-1013']
print(f"VBCB={len(vpcb)} non-VBCB={len(nonv)}")
print("non-VBCB:", [(i, info[i]['tenant']) for i in nonv])

# 3) umur event kedua-terakhir (pra-komentar cleaner) per kartu tertagih
print("\nPRA-TAGIH idle (jam, event ke-2 terakhir):")
for i in ids:
    rows = [r['created_at'] for r in con.execute(
        "SELECT created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 2", (i,))]
    pre = rows[1] if len(rows) > 1 else (rows[0] if rows else now)
    print(f"  {i} ({info[i]['tenant'] or '-'}): {(now-pre)/3600:.0f}j")

# 4) apakah sudah ada vonis sysmanager-cleaner/TRIASE sebelum ronde ini?
print("\nSUDAHTERNILAI SEBELUM RONDE:")
for i in ids:
    c = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND created_at<? AND (author='sysmanager-cleaner' OR body LIKE '%POSITIF-PALSU%' OR body LIKE '%ternilai%')",
                    (i, now - 7200)).fetchone()['c']
    if c:
        print(f"  {i}: {c} komentar vonis lama")

# 5) VBCB: kartu jangkar W7 + umur blokir asli gelombang penulis
print("\nVBCB detail:")
for r in con.execute("SELECT id,title,status FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status!='done'"):
    evs = [x['created_at'] for x in con.execute(
        "SELECT created_at FROM task_events WHERE task_id=? AND kind!='commented' ORDER BY created_at DESC LIMIT 2", (r['id'],))]
    blk = con.execute("SELECT COUNT(*) c FROM task_events WHERE task_id=? AND kind='blocked'", (r['id'],)).fetchone()['c']
    print(f"  {r['id']} [{r['status']}] blocked_ev={blk} ev_terakhir_nonkom={int((now-(evs[0] if evs else now))/60)}m :: {r['title'][:48]}")
