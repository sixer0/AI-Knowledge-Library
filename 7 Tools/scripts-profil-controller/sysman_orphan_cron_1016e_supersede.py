# -*- coding: utf-8 -*-
"""Ronde sysman 16-10: uji kelas parent-tersingkir pada 33 kartu penulis VBCB."""
import os, re, sqlite3, time, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
con = sqlite3.connect(str(HOME / 'kanban.db'))
con.row_factory = sqlite3.Row
tc = con.cursor()
now = int(time.time())

ids = [r['id'] for r in tc.execute(
    "SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' AND title LIKE '%Penulis bab%'")]
print(f"kartu penulis blocked: {len(ids)}")

superseded = {}
for i in ids:
    m = tc.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? AND body LIKE '%Digantikan%' ORDER BY created_at DESC LIMIT 1", (i,)).fetchone()
    if m:
        rep = re.search(r'(t_[0-9a-f]{8})', m['body'])
        st = None
        if rep:
            r2 = tc.execute("SELECT status,title FROM tasks WHERE id=?", (rep.group(1),)).fetchone()
            st = f"{rep.group(1)}:{r2['status']}" if r2 else f"{rep.group(1)}:?"
        superseded[i] = (m['author'], st)
print(f"ber-komentar Digantikan: {len(superseded)}")
from collections import Counter
print("status pengganti:", Counter(v[1] for v in superseded.values()))

# sampel satu kartu utuh
sample = ids[0]
print(f"\nSAMPEL {sample}:")
for e in tc.execute("SELECT kind,substr(payload,1,160) p,created_at FROM task_events WHERE task_id=? ORDER BY created_at", (sample,)):
    print(f"  {e['kind']}@{int((now-e['created_at'])/3600)}j {(e['p'] or '')[:120]}")
for c in tc.execute("SELECT author,substr(body,1,200) b,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (sample,)):
    print(f"  kom {c['author']}@{int((now-c['created_at'])/3600)}j: {c['b']}")

# anak dari kartu penulis ini (verifikasi) — status?
kids_open = 0
for i in ids:
    for k in tc.execute("SELECT child_id FROM task_links WHERE parent_id=?", (i,)):
        r = tc.execute("SELECT status FROM tasks WHERE id=?", (k['child_id'],)).fetchone()
        if r and r['status'] != 'done':
            kids_open += 1
print(f"\nanak-open dari 33 penulis: {kids_open}")

# W7 gate-close: masih butuh aksi?
w7 = tc.execute("SELECT id,status FROM tasks WHERE id='t_841f18dc'").fetchone()
print(f"W7: {w7['status']}")
for c in tc.execute("SELECT author,substr(body,1,180) b,created_at FROM task_comments WHERE task_id='t_841f18dc' ORDER BY created_at DESC LIMIT 4"):
    print(f"  kom {c['author']}@{int((now-c['created_at'])/3600)}j: {c['b']}")
