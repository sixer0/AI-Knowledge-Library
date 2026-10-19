#!/usr/bin/env python3
# Pasang RULE KONTRAK DESAIN (anti-drift template) ke SOUL.md: root + semua profil.
# Idempoten; guard sisip-murni (preseden 21-08: jangan pernah tulis-ulang SOUL).
# Preseden: INT-EXPO-2026 RevC dicabut user 06-09 - drift dari Template Hi-Tech v1.1
# lolos gerbang karena verifier menguji ke speks controller, bukan ke sumber desain.
import glob, io, os

BLOCK = """## RULE KONTRAK DESAIN ANTI-DRIFT (WAJIB, kebijakan 06-09-2026; direktif user pasca-pencabutan RevC)
Setiap tugas yang menginstruksikan keluaran 'mengikuti' sumber desain tertentu (template, prototipe, exemplar, master design):
1. SEBELUM blueprint: dump struktur sumber desain (read-only; sheet/dims/freeze/lebar/isi kepala/token gaya). Blueprint WAJIB memuat KONTRAK-DESAIN: daftar butir anatomi sumber dengan status per butir PERSIS / ADAPTASI-alasan / DIBUANG-putusan-user. Deviasi dari kata kerja eksplisit user butuh putusan user tercatat - controller dilarang mensahkan deviasinya sendiri.
2. SAAT build: mekanisme boleh disesuaikan (statis vs formula demi performa), KEBERADAAN dan BENTUK elemen kontrak tidak boleh hilang. Mengganti sistem token gaya (glif peran, palet, separator, struktur seksi) = pelanggaran kontrak; pulihkan sistem sumber, jangan ciptakan padanan lokal.
3. SEBELUM serah: verifier menguji artefak akhir terhadap DUMP sumber desain, butir per butir, dengan predikat terukur. Speks controller BUKAN alat ukur desain. Daftar delta-terizinkan pada gerbang fidelity dilarang memuat elemen kontrak desain tanpa putusan user.
4. KELUHAN VISUAL user ('beda dengan template', 'pita salah', 'drift dari konteks awal') = sinyal vonis: diff artefak vs sumber desain dulu, temukan elemen sistem yang hilang, pulihkan sistemnya - dilarang menambal gejala dengan kosakata/format baru.
5. Pencabutan artefak oleh user: hapus dari SEMUA lokasi data (verifikasi sisa 0), catat hash jejak, komentar REVOKE di kartu, konfirmasi rilis sebelumnya utuh, traceroot ke tahap penyebab, tambal gerangnya, naikkan aturan.
Rujukan penuh: skill gsp-orchestration-execution references/design-contract-drift.md (D-INT-11).

"""

def target_files():
    home = os.path.expandvars(r"C:\Users\TRIAL\AppData\Local\hermes")
    files = [os.path.join(home, "SOUL.md")]
    files += sorted(glob.glob(os.path.join(home, "profiles", "*", "SOUL.md")))
    return files

changed, skipped, failed = [], [], []
for f in target_files():
    try:
        t = io.open(f, encoding="utf-8").read()
    except Exception as e:
        failed.append((f, "read: %s" % e)); continue
    if "RULE KONTRAK DESAIN ANTI-DRIFT" in t:
        skipped.append(f); continue
    anchor = None
    for a in ("## GATE NATURALISASI", "## RULE AKURASI DATA MUTLAK", "## RULE PENCARIAN OFENSIF",
              "## GATE ENFORCEMENT", "## Aturan Kerja", "## Memori & Dokumentasi"):
        if a in t:
            anchor = a; break
    if anchor:
        t2 = t.replace(anchor, BLOCK + anchor, 1)
    else:
        t2 = t.rstrip() + "\n\n" + BLOCK
    try:
        io.open(f, "w", encoding="utf-8").write(t2)
        changed.append(f)
    except Exception as e:
        failed.append((f, "write: %s" % e))

print("changed=%d skipped=%d failed=%d" % (len(changed), len(skipped), len(failed)))
for f, e in failed: print("FAIL", f, e)
