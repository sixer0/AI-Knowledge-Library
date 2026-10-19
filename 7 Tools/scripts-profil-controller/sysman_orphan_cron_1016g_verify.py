# -*- coding: utf-8 -*-
"""Ronde sysman 16-10: verifikasi koreksi mendarat + rekap akhir."""
import os, sqlite3, time, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
con = sqlite3.connect(str(HOME / 'kanban.db'))
con.row_factory = sqlite3.Row
tc = con.cursor()
now = int(time.time())

n = tc.execute("SELECT COUNT(*) c FROM task_comments WHERE body LIKE '%[SYSMAN-CLEANER 16-10]%' AND author='sysmanager-cleaner'").fetchone()['c']
print(f"VERIFIKASI: komentar koreksi 16-10 di DB = {n}")
ids = [r['task_id'] for r in tc.execute("SELECT DISTINCT task_id FROM task_comments WHERE body LIKE '%[SYSMAN-CLEANER 16-10]%'")]
vpcb = [i for i in ids if tc.execute("SELECT tenant FROM tasks WHERE id=?", (i,)).fetchone()['tenant'] == 'VIBE-BIBLE-1013']
print(f"  cakupan: {len(ids)} kartu (VBCB={len(vpcb)}, non-VBCB={len(ids)-len(vpcb)})")

# tagihan ronde ini yang TIDAK dikoreksi (harus 0)
tagih = [r['task_id'] for r in tc.execute(
    "SELECT DISTINCT task_id FROM task_comments WHERE body LIKE '%ORPHAN-TAG v1%' AND created_at > ?", (now - 7200,))]
uncorr = [i for i in tagih if i not in ids]
print(f"  tertagih={len(tagih)} tanpa-koreksi={len(uncorr)} {uncorr}")

# umur kartu jangkar & W7 utk laporan
for tid in ('t_841f18dc',):
    le = tc.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()['m']
    print(f"  W7 {tid}: event terakhir {int((now-le)/3600)}j lalu")
