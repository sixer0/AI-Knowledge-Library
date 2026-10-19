# -*- coding: utf-8 -*-
"""Ronde sysman 16-10: tempel koreksi author sysmanager-cleaner (idempoten, hemat giliran)."""
import os, sqlite3, subprocess, time, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
HERMES = str(HOME / 'hermes-agent' / 'venv' / 'Scripts' / 'hermes.exe')
con = sqlite3.connect(str(HOME / 'kanban.db'))
con.row_factory = sqlite3.Row
tc = con.cursor()

TOKEN = '[SYSMAN-CLEANER 16-10]'

MSG_VBCB = (TOKEN + " Koreksi tagihan ORPHAN-TAG v1: POSITIF-PALSU kelas parent-tersingkir. "
            "Run penulis lama timed_out(3600s) x2 lalu gave_up; kartu sudah digantikan jalur M4 rebuild "
            "(lihat komentar 'Digantikan t_...' di kartu ini) dan SELURUH pasangan pengganti done. "
            "Induk tersingkir ini dibiarkan blocked permanen: bukan butir kerja, jangan ditagih ulang. "
            "Rem mekanis (tutup/relink induk tersingkir) = satu butir tingkat-misi VIBE-BIBLE-1013 "
            "ke controller pemilik tenant.")

MSG_NONVBCB = {
    't_ff13e0e6': (TOKEN + " Koreksi: POSITIF-PALSU berulang (vonis sama 11-10 dan 14-10). Kartu terminal atas "
                   "putusan user tercatat 'BLOCK permanen - lupakan WMS' (TRIASE-0912); assignee gsp-engineering-analyst "
                   "dilebur PROF-MERGE-1010. Jangan ditagih ulang."),
    't_c38a042f': (TOKEN + " Koreksi: POSITIF-PALSU kelas menunggu-keputusan-user. Gerbang L3 uji piksel dua akun ada di "
                   "tangan user sejak WAKE-TRIAGE 10-10; vonis 11-10/14-10 identik. Jangan ditagih ulang."),
    't_87058aef': (TOKEN + " Koreksi: POSITIF-PALSU (vonis 11-10/14-10). Event blocked beralasan 'dibatalkan user - scope "
                   "turun ke jawaban langsung'; kartu terminal. Jangan ditagih ulang."),
    't_2a3b78f9': (TOKEN + " Koreksi: POSITIF-PALSU (vonis 11-10/14-10). Sekandung L1/L3/L6: dibatalkan user, kartu terminal. Jangan ditagih ulang."),
    't_425f4e08': (TOKEN + " Koreksi: POSITIF-PALSU (vonis 11-10/14-10). Sekandung L1/L2/L6: dibatalkan user, kartu terminal. Jangan ditagih ulang."),
    't_309a2522': (TOKEN + " Koreksi: POSITIF-PALSU (vonis 11-10/14-10). Sekandung L1/L2/L3: dibatalkan user, kartu terminal. Jangan ditagih ulang."),
    't_a3378d47': (TOKEN + " Koreksi: POSITIF-PALSU, sudah ternilai D-PAYUNG-05 (wewenang insan, guard AGENTS.md headless); "
                   "triase default+gsp-master 15-10 melarang lapor ulang sebelum consent mendarat. Jangan ditagih ulang."),
    't_bb725705': (TOKEN + " Koreksi: POSITIF-PALSU, sasaran tercapai oleh aksi insan 13-10 (setara opsi B); vonis controller "
                   "wake-lane 15-10 mendarat, penutupan final menunggu kata user. Jangan ditagih ulang."),
    't_6359bba5': (TOKEN + " Koreksi: BUTUH-MASUKAN sah yang sudah ternilai dua kali (triase wake-lane 15-10 + token [FASE]); "
                   "naskah hulu divonis TIDAK LAYAK RILIS, GSF-23 dilarang jalan. Menunggu putusan user, bukan macet. Jangan ditagih ulang."),
    't_66b1a0b2': (TOKEN + " Koreksi: POSITIF-PALSU kelas kartu-jangkar-kontrak (ANCHOR-KONTRAK jangan-dispatch, vonis sysman "
                   "14-10 + sepakat wake-lane 15-10). Isu nyata = penerimaan akhir misi AIE26SAT, tingkat-misi. Jangan ditagih ulang."),
}

# kumpulkan id target
vpcb = [r['id'] for r in tc.execute(
    "SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' AND title LIKE '%Penulis bab%'")]
targets = [(i, MSG_VBCB) for i in vpcb] + list(MSG_NONVBCB.items())

done, skipped, failed = [], [], []
for tid, msg in targets:
    have = tc.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE ?",
                      (tid, '%' + TOKEN + '%')).fetchone()['c']
    if have:
        skipped.append(tid); continue
    r = subprocess.run([HERMES, 'kanban', '--board', 'default', 'comment', tid, msg,
                        '--author', 'sysmanager-cleaner'], capture_output=True, text=True, timeout=90)
    if r.returncode == 0:
        done.append(tid)
    else:
        failed.append((tid, (r.stderr or r.stdout)[:120]))

print(f"TEMPEL={len(done)} SKIP={len(skipped)} GAGAL={len(failed)}")
if failed:
    print("GAGAL:", failed)
