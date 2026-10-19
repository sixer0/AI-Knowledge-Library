#!/usr/bin/env python3
"""Pembungkus cron safety-net PMODE-DELEG-1010: gsp_deleg_watch dead.
Pola watchdog: DIAM (stdout kosong) saat tidak ada yang perlu dilaporkan;
baru bicara saat ada PID-hilang yang direclaim / auto-block / kuota menumpuk.
Cron no_agent mengirim stdout verbatim -> kosong = tidak ada notifikasi.

RW-TIMEOUT-FIX 14-10 (kartu t_59822db7): probe kena contention tulis DB papan
bisa melewati plafon lama 120s -> TimeoutExpired tak tertangkap -> seluruh
siklus cron crash exit 1 tanpa laporan. Kini: jendela probe diperlebar 240s,
satu retry, dan timeout tetap mencetak satu baris peringatan (exit 0) supaya
pola diam-sehat tetap informatif. Perilaku pada kondisi normal tidak berubah.

WAKE-FIX-1015 15-10: RECLAIMED count=0 ids=[] adalah detak jantung, BUKAN
kejadian. Sebelumnya baris itu selalu tercetak sehingga cron no_agent mengirim
pesan bot-chat tiap 5 menit pada kondisi sehat (terukur 1.212 injeksi ke sesi
controller sejak 10-10, tiap injeksi membangunkan agen = sumber gejala
stuck-berulang). Kini baris detak jantung dibuang; satu-satunya keluaran
sehat adalah DIAM. Kejadian nyata (GRACE/TIMED-OUT/RECLAIMED count>0/
CRASHED/AUTO-BLOCKED/QUOTA-DEFERRED) tetap tercetak apa adanya.
"""
import subprocess, sys, os

env = {k: v for k, v in os.environ.items() if k != 'HERMES_DELEGATED_CHILD_CONTEXT'}
W = os.path.join(os.environ.get('LOCALAPPDATA', r'C:\Users\TRIAL\AppData\Local'),
                 'hermes', 'scripts', 'gsp_deleg_watch.py')
PY = sys.executable
PROBE_TIMEOUT = 240  # RW-TIMEOUT-FIX 14-10: plafon lama 120s terukur jebol 5x di beban puncak

r = None
for _attempt in range(2):
    try:
        r = subprocess.run([PY, W, 'dead'], capture_output=True, text=True,
                           env=env, timeout=PROBE_TIMEOUT)
        break
    except subprocess.TimeoutExpired:
        if _attempt == 0:
            continue
        print(f'RANTAI-WATCH: probe timeout {PROBE_TIMEOUT}s, dilewati; '
              f'ukur ulang ronde berikut')
        sys.exit(0)

lines = [l for l in (r.stdout or '').splitlines() if l.strip()]
events = [l for l in lines if not l.startswith('SUMMARY')]
# WAKE-FIX-1015: buang detak jantung RECLAIMED count=0 ids=[] (bukan kejadian).
events = [l for l in events
          if not (l.startswith('RECLAIMED') and 'count=0' in l and 'ids=[]' in l)]
if not events:
    sys.exit(0)  # sehat: diam
print('RANTAI-WATCH (safety net mati-jembatan, PMODE-DELEG-1010):')
for l in events:
    print(' ', l)
if r.stderr and r.stderr.strip():
    print('stderr:', r.stderr.strip()[:300])
sys.exit(0)
