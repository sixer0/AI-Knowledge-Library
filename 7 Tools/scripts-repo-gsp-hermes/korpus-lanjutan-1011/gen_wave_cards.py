#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_wave_cards.py - generik: buat kartu dari baris tabel 02_structured.md per daftar langkah.
Pemakaian: python gen_wave_cards.py "14,18,19,20,22,23,24" '{"14":"t_3a7f8a60","18":"t_4028d9b9",...}'
Estimasi E dibaca dari tabel S5 02 (baris '| N ... | E |'). Deterministik, salinan kolom verbatim."""
import io, re, subprocess, os, sys, json

WS = 'C:/Users/TRIAL/workspace/gsp-hermes/workspace'
BP = WS + '/docs/2026-10-11-korpus-lanjutan-1011/identification/02_structured.md'
LAD = 'C:/Users/TRIAL/AppData/Local/hermes/skills/gsp/gsp-limit-aware-delegation/scripts/lad_card.py'
TENANT = 'KORPUS-LANJUTAN-1011'
ENV = dict(os.environ); ENV.pop('HERMES_DELEGATED_CHILD_CONTEXT', None)

steps = [s.strip() for s in sys.argv[1].split(',')]
parents = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

def split_row(ln):
    ln = ln.strip().strip('|')
    tmp = ln.replace('\\|', '\x00')
    return [c.strip().replace('\x00', '|') for c in tmp.split('|')]

txt = io.open(BP, encoding='utf-8').read()
rows, est = {}, {}
for ln in txt.splitlines():
    m = re.match(r'^\|\s*(\d+)\s*\|', ln.strip())
    if m and m.group(1) in steps:
        rows[m.group(1)] = split_row(ln)
# E dari tabel S5: '| 14 CC1-NUM | 50 | R-1 |' ATAU gabungan '| 30–32 verifikator | 35/45/20 | R-1 |'
for ln in txt.splitlines():
    m = re.match(r'^\|\s*(\d+)(?:[–-](\d+))?\s*[^|]*\|\s*(\d+(?:/\d+)*)\s*\|\s*R-', ln.strip())
    if not m: continue
    a, b, es = int(m.group(1)), int(m.group(2) or m.group(1)), m.group(3).split('/')
    for i, n in enumerate(range(a, b + 1)):
        if str(n) in steps and i < len(es):
            est[str(n)] = es[i]

out = []
for n in steps:
    assert n in rows, f'langkah {n} tidak ketemu di 02'
    r = rows[n]
    while len(r) < 9: r.append('')
    step, desc, agent, exp, deps, verif, phase, wajib, peranlock = r[:9]
    peran = re.search(r'peran\s*=\s*(?:roles/)?(\S+\.md)', peranlock)
    lock = re.search(r'LOCK\s*=\s*(.+)$', peranlock)
    peran_line = (f"BERKAS PERAN: {WS}/roles/{peran.group(1)}" if peran
                  else "BERKAS PERAN: (tidak ada berkas peran — jalankan identitas profil assignee sendiri)")
    body = (f"KELAS: BERAT (dari 01 sha16 a3260e6b4d3be01c; baris langkah {n} di 02_structured.md adalah otoritas kerjamu)\n"
            f"{peran_line}\n"
            f"TUGAS (verbatim 02): {desc}\n"
            f"EXPECTED OUTPUT: {exp}\n"
            f"VERIFIKASI (short check, maks 3 langkah): {verif}\n"
            f"WAJIB-BACA: {wajib}\n"
            f"LOCK (hanya berkas ini yang boleh kamu tulis): {lock.group(1) if lock else '(lihat 02)'}\n"
            f"BATAS: catatan koreksi TERTANGGAL bukan sunting senyap; jangan sentuh berkas di luar LOCK; "
            f"temuan di luar lingkup = komentar ISU-LINTAS-OWNER, jangan ditambal. "
            f"SAT-1010 bila disebut: pakai peta-lokus JSON, DILARANG baca penuh berkas besar ke konteks.\n"
            f"SELESAI: komentar LAPOR-SELESAI + wait-ack (C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_deleg_watch.py) lalu complete hanya jika ACKED/PARKED.\n"
            f"[jejak: blueprint 02 baris {n}, phase {phase}]")
    head, sep, tail = desc.partition(':')
    title = (head if sep else desc[:40]) + f" (langkah {n}/{phase}): " + (tail if sep else desc[40:]).strip()[:70]
    args = [sys.executable, LAD, '--title', title[:110], '--assignee', agent,
            '--est', est.get(n, '40'), '--shape', 'satu', '--tenant', TENANT, '--body', body]
    if n in parents: args += ['--parents', parents[n]]
    p = subprocess.run(args, capture_output=True, text=True, env=ENV)
    line = [l for l in (p.stdout + p.stderr).splitlines() if l.startswith('Created')]
    # LANEE DINAMIS (kebijakan user 11-10): daftar langganan wake per kartu ke kanal
    # rumah ASIGNOR (bukan hardcode). Kanal dibaca dari env WAKE_LANE_* agar portabel;
    # tanpa env, lewati (kartu warisan pola lama).
    if line and os.environ.get('WAKE_LANE_PLATFORM'):
        tid_new = line[0].split()[1]
        sub = subprocess.run(['hermes','kanban','--board','default','notify-subscribe',tid_new,
                              '--platform',os.environ['WAKE_LANE_PLATFORM'],
                              '--chat-id',os.environ['WAKE_LANE_CHAT_ID'],
                              '--chat-type','dm',
                              '--notifier-profile',os.environ.get('WAKE_LANE_PROFILE','gsp-master'),
                              '--delivery-mode','notify+wake'], capture_output=True, text=True, env=ENV)
        if sub.returncode != 0:
            print('WARN wake-subscribe gagal', tid_new, (sub.stdout+sub.stderr)[:80])
    print(n, agent, est.get(n, '?'), '->', line[0] if line else ('ERR ' + (p.stderr or p.stdout)[:150]))
    if line: out.append({'step': n, 'card': line[0].split()[1], 'assignee': agent})
OUTD = WS + '/docs/2026-10-11-korpus-lanjutan-1011/work/waves'
OUTF = os.path.join(OUTD, 'cards_' + '_'.join(steps[:3]) + '.json')
io.open(OUTF, 'w', encoding='utf-8').write(json.dumps(out, indent=1))
print('total dibuat =', len(out), '->', OUTF)
