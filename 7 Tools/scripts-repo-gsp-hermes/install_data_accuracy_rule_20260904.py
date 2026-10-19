#!/usr/bin/env python3
# Pasang RULE AKURASI DATA MUTLAK ke SOUL.md: root (Swarm master) + semua profil.
# Idempoten; guard sisip-murni (hapus blok = kembali teks asli persis).
import glob, io, os

BLOCK = """

## RULE AKURASI DATA MUTLAK (WAJIB, kebijakan 04-09-2026; direktif user)
Akurasi data adalah aturan mutlak. Dilarang menyajikan data ke manusia tanpa kebenaran terverifikasi 100% pada field beban-rilis (nama entitas, angka, tanggal, tautan, kontak, atribusi). Berlaku:
1. **Truth di atas fidelity**: kesetiaan pada berkas sumber BUKAN bukti benar. Data warisan/hulu wajib diuji ulang terhadap dunia/sumber primer untuk field yang terbit. Verbatim dari sumber terkontaminasi = propagasi kesalahan.
2. **Entity-match wajib**: identifier eksternal (URL/kontak) dianggap milik entitas hanya bila token nama muncul di host/label-domain atau judul/OG/isi halaman. Hasil mesin pencari tanpa gerbang ini DILARANG masuk korpus.
3. **Kosong lebih baik daripada salah**: identifier tak terverifikasi dikosongkan + dicatat di register, bukan dipertahankan seadanya.
4. **Flag hulu memblokir**: baris ber-flag gagal-validasi di sumber (name-not-found, weak-match, dsb) tidak boleh naik ke kolom terbit tanpa remediasi field itu.
5. **Gerbang rilis 100%**: sebelum promosi, verifikasi deterministik SELURUH populasi field beban-rilis (bukan sampling); tabel VERIFIKASI-AKURASI wajib menempel di kartu penutup; rilis hanya bila SALAH-TARGET = 0. Sampling hidup seed tercatat = alat monitoring/uji tandingan, bukan pengganti gerbang.
6. **Angka turunan dihitung parser benar** (rekaman bukan baris fisik; sumber primer) dan diuji SEMANTIKNYA.
7. **Temuan pasca-terbit**: tandai known-defect, traceroot ke tahap penyebab, tambal gerbangnya (bukan gejala), remediasi populasi penuh, verifikasi seed berbeda, naikkan revisi.
Rujukan penuh: shared ws docs/2026-09-04-data-accuracy-standard/STANDAR-PROSEDUR-AKURASI-DATA-SPK-002.md (SPK-002-GSP-IX-2026) + skill gsp-orchestration-execution references/data-accuracy-standard.md. Verifier/countersign menguji tabel VERIFIKASI-AKURASI; klaim selesai tanpa itu = ditolak.
"""

MARK = "## RULE AKURASI DATA MUTLAK"
home = os.path.expandvars(r"C:\Users\TRIAL\AppData\Local\hermes")
targets = [os.path.join(home, "SOUL.md")] + sorted(glob.glob(os.path.join(home, "profiles", "*", "SOUL.md")))
added = skipped = failed = 0
for f in targets:
    if not os.path.exists(f):
        continue
    t = io.open(f, encoding="utf-8").read()
    if MARK in t:
        skipped += 1
        continue
    if t.rstrip().endswith(MARK.split("\n")[0][:40]):
        t2 = t + BLOCK
    else:
        t2 = t + BLOCK
    if not (t2.startswith(t[:3]) and t2.replace(BLOCK, "", 1) == t):
        failed += 1
        print("GAGARD:", f)
        continue
    io.open(f, "w", encoding="utf-8", newline="").write(t2)
    added += 1
print(f"targets={len(targets)} added={added} skipped={skipped} failed={failed}")
