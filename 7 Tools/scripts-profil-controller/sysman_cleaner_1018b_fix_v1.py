#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde 18-10: tempel koreksi [SYSMAN-CLEANER 18-10] pada 43 kartu tertagih ORPHAN-TAG v1.
Idempoten: lewati kartu yang sudah punya token tanggal ini. Author = sysmanager-cleaner."""
import os, sqlite3, subprocess, pathlib, time

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
HERMES = str(HOME / 'hermes-agent' / 'venv' / 'Scripts' / 'hermes.exe')
con = sqlite3.connect(str(HOME / 'kanban.db'))
con.row_factory = sqlite3.Row
now = int(time.time())

CLASS_A = {  # ASSIGNEE-DI-LUAR-REGISTRI
 't_ff13e0e6': "POSITIF-PALSU (vonis sama 11-10/14-10/16-10/17-10). Kartu terminal era pra-PROF-MERGE: diblok prasyarat eksternal tercatat (API Smart WMS nyata + environment test + izin tertulis pemilik sistem); assignee gsp-engineering-analyst sudah diarsipkan PROF-MERGE-1010 sehingga kelas yatim-penghuni ini muncul selamanya. Rem permanen: arsip/tutup oleh controller pemilik misi SWMS, bukan tagihan harian.",
 't_87058aef': "POSITIF-PALSU (vonis sama 11-10/14-10/16-10/17-10). Laju lajur CCTV-DP-0923 DIBATALKAN OLEH USER 23-09 (catatan eksplisit di kartu: scope turun ke jawaban langsung); assignee gsp-vss-specialist profil arsip PROF-MERGE-1010. Rem: arsipkan kartu terminal ini.",
 't_2a3b78f9': "POSITIF-PALSU (vonis sama 11-10/14-10/16-10/17-10). Sekandung L1/L3/L6: dibatalkan user 23-09, alasan tercatat di event blocked; assignee profil arsip. Rem: arsipkan.",
 't_425f4e08': "POSITIF-PALSU (vonis sama 11-10/14-10/16-10/17-10). Sekandung L1/L2/L6: dibatalkan user 23-09, alasan tercatat di event blocked; assignee profil arsip. Rem: arsipkan.",
 't_309a2522': "POSITIF-PALSU (vonis sama 11-10/14-10/16-10/17-10). Sekandung L1/L2/L3: dibatalkan user 23-09, alasan tercatat di event blocked; assignee profil arsip. Rem: arsipkan.",
}
CLASS_B_NOTE = "POSITIF-PALSU kelas parent-tersingkir (pola identik 16-10/17-10). Pengganti M4 rebuild diverifikasi ulang ronde 18-10: 33/33 pasangan DONE. Induk sengaja dibiarkan blocked setelah rebuild. Isu nyata berada di tingkat misi VIBE-BIBLE-1013 (serah-terima senyap: 117 kartu done tanpa RANTAI-ACK; gerbang W7 t_841f18dc masih blocked tanpa aksi sejak eskalasi 17-10), bukan pada kartu ini. Rem mekanis agar daur berhenti: tutup/archive induk tersingkir oleh controller gsp-master01."
CLASS_C = {
 't_c38a042f': "POSITIF-PALSU kelas menunggu-keputusan-user (vonis sama 11-10 s.d. 17-10): gerbang L3 uji piksel dua akun adalah putusan insan, keadaan tercatat. Tagihan berulang = artefak jendela anti-spam alat, bukan pekerjaan tertunda.",
 't_a3378d47': "POSITIF-PALSU: sudah ternilai D-PAYUNG-05 (wewenang insan; guard AGENTS.md headless memblokir jalur otomatis). Vonis konsisten 11-10 s.d. 17-10.",
 't_bb725705': "POSITIF-PALSU: sasaran tercapai oleh aksi insan 13-10; vonis controller wake-lane 15-10 sudah menempel. Tidak ada kerja tertunda di kartu ini.",
 't_6359bba5': "BUTUH-MASUKAN sah yang SUDAH ternilai dua kali (triase wake-lane 15-10 + token [FASE] dari user). Tagihan harian = temuan instrumen (rute stalled tidak diredam triase author tak terdaftar), bukan butir kerja baru.",
 't_66b1a0b2': "POSITIF-PALSU kelas kartu-jangkar-kontrak (ANCHOR-KONTRAK jangan-dispatch): tidak akan pernah dapat komentar controller, jadi baris ditagih selamanya. Vonis konsisten sejak 14-10; isu sebenarnya tingkat-misi AIE26SAT.",
}

def post(tid, text):
    dup = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%[SYSMAN-CLEANER 18-10]%'",
                      (tid,)).fetchone()['c']
    if dup:
        return 'SKIP_IDEMPOTEN'
    msg = f"[SYSMAN-CLEANER 18-10] Koreksi tagihan ORPHAN-TAG v1: {text}"
    r = subprocess.run([HERMES, 'kanban', '--board', 'default', 'comment', tid, msg,
                        '--author', 'sysmanager-cleaner'], capture_output=True, text=True, timeout=90)
    return 'OK' if r.returncode == 0 else f'GALAT:{r.stderr[:120]}'

# kumpulkan 33 induk VBCB tertagih (punya marker Digantikan, tanpa komentar koreksi hari ini)
tagged = [r['task_id'] for r in con.execute(
    "SELECT DISTINCT task_id FROM task_comments WHERE body LIKE '%ORPHAN-TAG%' AND created_at>?",
    (now - 3 * 3600,))]
class_b = [t for t in tagged if t not in CLASS_A and t not in CLASS_C]
print(f"tertagih={len(tagged)} A={len(CLASS_A)} B={len(class_b)} C={len(CLASS_C)}")
assert len(class_b) == 33, f"kelas B harus 33, dapat {len(class_b)}"

hasil = {}
for tid, txt in list(CLASS_A.items()) + [(t, CLASS_B_NOTE) for t in class_b] + list(CLASS_C.items()):
    hasil[tid] = post(tid, txt)
    print(f"{tid}: {hasil[tid]}")
ok = sum(1 for v in hasil.values() if v == 'OK')
skip = sum(1 for v in hasil.values() if v == 'SKIP_IDEMPOTEN')
galat = {k: v for k, v in hasil.items() if v.startswith('GALAT')}
print(f"\nRINGKASAN OK={ok} SKIP={skip} GALAT={len(galat)} {galat}")
