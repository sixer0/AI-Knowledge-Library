# -*- coding: utf-8 -*-
"""Ronde sysman 16-10: bukti penilaian — alasan blokir + komentar substantif + sensus tenant."""
import os, sqlite3, time, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
con = sqlite3.connect(str(HOME / 'kanban.db'))
con.row_factory = sqlite3.Row
now = int(time.time())
tc = con.cursor()

TAGGED = ['t_ff13e0e6','t_c38a042f','t_87058aef','t_2a3b78f9','t_425f4e08','t_309a2522',
          't_a3378d47','t_bb725705','t_6359bba5','t_66b1a0b2']

print("=== BLOKIR-REASON + KOMENTAR SUBSTANTIF (kartu non-VBCB) ===")
for tid in TAGGED:
    r = tc.execute("SELECT id,title,assignee,status,tenant FROM tasks WHERE id=?", (tid,)).fetchone()
    if not r:
        print(f"{tid}: TIDAK ADA"); continue
    print(f"\n--- {tid} [{r['status']}] asg={r['assignee']} tenant={r['tenant']}")
    print(f"    {r['title'][:90]}")
    ev = tc.execute("SELECT kind,payload,created_at FROM task_events WHERE task_id=? AND kind IN ('blocked','unblocked','needs_input') ORDER BY created_at DESC LIMIT 2", (tid,)).fetchall()
    for e in ev:
        p = (e['payload'] or '')[:300].replace('\n', ' ')
        print(f"    ev {e['kind']}@{int((now-e['created_at'])/3600)}j: {p}")
    coms = tc.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? AND author NOT IN ('board-cleaner') AND body NOT LIKE '%RANTAI-WAKE%' ORDER BY created_at DESC LIMIT 3", (tid,)).fetchall()
    for c in coms:
        print(f"    kom {c['author']}@{int((now-c['created_at'])/3600)}j: {c['body'][:220].replace(chr(10),' | ')}")

print("\n\n=== SENSUS TENANT VIBE-BIBLE-1013 ===")
tot = tc.execute("SELECT COUNT(*) c FROM tasks WHERE tenant='VIBE-BIBLE-1013'").fetchone()['c']
print(f"total kartu: {tot}")
for r in tc.execute("SELECT status, COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' GROUP BY status"):
    print(f"  {r['status']}: {r['n']}")
print("event kinds (terakhir 7 hari):")
for r in tc.execute("SELECT e.kind, COUNT(*) n FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND e.created_at>? GROUP BY e.kind ORDER BY n DESC", (now-7*86400,)):
    print(f"  {r['kind']}: {r['n']}")
print("umur event terakhir kartu blocked VBCB (menit): ")
ages = [int((now - (tc.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (x['id'],)).fetchone()['m'] or now))/60)
        for x in tc.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'")]
if ages:
    print(f"  n={len(ages)} min={min(ages)} max={max(ages)}")
print("contoh alasan blokir VBCB:")
for r in tc.execute("SELECT t.id, e.payload, e.created_at FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='blocked' ORDER BY e.created_at DESC LIMIT 3"):
    print(f"  {r['id']} @{int((now-r['created_at'])/3600)}j: {(r['payload'] or '')[:280]}")
print("unblocked terakhir VBCB:")
ub = tc.execute("SELECT MAX(e.created_at) m FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='unblocked'").fetchone()['m']
print(f"  {'-' if not ub else str(int((now-ub)/3600))+' jam lalu'}")

print("\n=== VBCB done: sensus ACK (RANTAI-ACK) ===")
ids = [x['id'] for x in tc.execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'")]
ack = 0
for i in ids:
    c = tc.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (i,)).fetchone()['c']
    if c: ack += 1
print(f"done={len(ids)} ber-ACK={ack} tanpa-ACK={len(ids)-ack}")

print("\n=== KARTU VBCB blocked: cek LAPOR-SELESEI tanpa ACK (butir nyata?) ===")
for x in tc.execute("SELECT id,title,assignee FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' LIMIT 40"):
    lap = tc.execute("SELECT author,created_at FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESEI%' OR body LIKE '%LAPOR-SELESAI%' OR body LIKE '%CHECKPOINT%') ORDER BY created_at DESC LIMIT 1", (x['id'],)).fetchall()
    if lap:
        print(f"  {x['id']} {x['title'][:40]}: LAPOR/CHECKPOINT oleh {[l['author'] for l in lap][:2]} @{[int((now-l['created_at'])/3600) for l in lap][:1]}j")
