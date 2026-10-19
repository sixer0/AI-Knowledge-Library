#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bukti penilaian ronde 18-10: status pasangan Digantikan VBCB, sensus ACK done VBCB,
keadaan t_841f18dc (butir sah kemarin), detail 5 kartu khusus, block_kind semua kandidat."""
import os, sqlite3, time, pathlib, re, collections

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
now = int(time.time())
con = sqlite3.connect(str(HOME / 'kanban.db'))
con.row_factory = sqlite3.Row

print("=== A. PASANGAN DIGANTIKAN (33 induk VBCB) ===")
tags = list(con.execute(
    "SELECT task_id FROM task_comments WHERE body LIKE '%ORPHAN-TAG%' AND created_at>?",
    (now - 3*3600,)))
ids = [t['task_id'] for t in tags]
partners = {}
for tid in ids:
    d = con.execute("SELECT body FROM task_comments WHERE task_id=? AND body LIKE '%Digantikan t_%' "
                    "ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    if d:
        m = re.search(r'Digantikan (t_[0-9a-f]{8})', d['body'])
        if m:
            partners[tid] = m.group(1)
st = collections.Counter()
missing = []
for tid, pid in partners.items():
    p = con.execute("SELECT status FROM tasks WHERE id=?", (pid,)).fetchone()
    st[p['status'] if p else 'HILANG'] += 1
    if not p or p['status'] not in ('done', 'archived'):
        missing.append((tid, pid, p['status'] if p else 'HILANG'))
print(f"induk_berpasangan={len(partners)} distribusi_status_pasangan={dict(st)}")
print(f"pasangan_belum_done={missing}")

print("\n=== B. SENSUS DONE VBCB + ACK (serah-terima senyap) ===")
done_vb = list(con.execute(
    "SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'"))
ack0 = 0
for row in done_vb:
    c = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
                    (row['id'],)).fetchone()['n']
    if c == 0:
        ack0 += 1
print(f"done_VBCB={len(done_vb)} tanpa_RANTAI_ACK={ack0}")
vb_open = con.execute("SELECT COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' "
                      "AND status NOT IN ('done','archived')").fetchone()['n']
print(f"terbuka_VBCB={vb_open}")

print("\n=== C. KEADAAN t_841f18dc (butir SAH ronde 17-10) ===")
t = con.execute("SELECT id,status,assignee,tenant,title,completed_at FROM tasks WHERE id='t_841f18dc'").fetchone()
if t:
    print(dict(t))
    le = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id='t_841f18dc'").fetchone()['m']
    print(f"event_terakhir_umur_j={(now-le)/3600:.1f}")
    for c in con.execute("SELECT author, substr(body,1,100) b, created_at FROM task_comments "
                         "WHERE task_id='t_841f18dc' ORDER BY created_at DESC LIMIT 4"):
        print(f"  [{c['author']}] {(now-c['created_at'])/3600:.1f}j: {c['b']}")
else:
    print("tidak ditemukan")

print("\n=== D. DETAIL 5 KARTU KHUSUS (non-VBCB, non-ASSIGNEE) ===")
for tid in ('t_c38a042f', 't_a3378d47', 't_bb725705', 't_6359bba5', 't_66b1a0b2'):
    t = con.execute("SELECT id,status,assignee,tenant,title,block_kind,block_recurrences "
                    "FROM tasks WHERE id=?", (tid,)).fetchone()
    print(f"\n{tid} st={t['status']} asn={t['assignee']} tenant={t['tenant']} "
          f"bk={t['block_kind']} rec={t['block_recurrences']} :: {(t['title'] or '')[:60]}")
    for c in con.execute("SELECT author, substr(body,1,110) b, created_at FROM task_comments "
                         "WHERE task_id=? AND body NOT LIKE '%ORPHAN-TAG%' ORDER BY created_at DESC LIMIT 2", (tid,)):
        print(f"  [{c['author']}] {(now-c['created_at'])/3600:.0f}j: {c['b']}")

print("\n=== E. BLOCK_KIND 44 TERBUKA ===")
for r in con.execute("SELECT block_kind, COUNT(*) n FROM tasks WHERE status NOT IN ('done','archived') GROUP BY block_kind"):
    print(f"  {r['block_kind']}: {r['n']}")
print("\n=== F. APAKAH ADA KOMENTAR BARU (non-tagihan) SEJAK RONDE 17-10 ===")
CUT = now - 30*3600
for tid in ids:
    c = con.execute("SELECT author, substr(body,1,60) b, created_at FROM task_comments WHERE task_id=? "
                    "AND created_at>? AND body NOT LIKE '%ORPHAN-TAG%' AND body NOT LIKE '%SYSMAN-CLEANER%' "
                    "ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    if c:
        print(f"  {tid}: [{c['author']}] {(now-c['created_at'])/3600:.0f}j: {c['b']}")
print("(kosong = tidak ada aktivitas manusia/controller pada kartu tertagih sejak kemarin)")
con.close()
