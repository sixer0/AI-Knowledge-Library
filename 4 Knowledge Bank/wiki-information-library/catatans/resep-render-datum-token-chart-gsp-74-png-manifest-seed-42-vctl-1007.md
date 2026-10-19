---
id: resep-render-datum-token-chart-gsp-74-png-manifest-seed-42-vctl-1007
type: catatan
title: Resep Render DATUM-token Chart GSP (74 PNG + manifest, seed 42, VCTL-1007)
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-10-08
catatan_verifikasi: "Verdict: terverifikasi (ITERASI-2, gsp-custodian 2026-10-08) || Uji delta fokus iterasi-2 saja, bukan audit 7 dimensi ulang. (1) Census id sumber docs/2026-10-07-vctl-chart-catalog/assets/manifest.json sha16 4cf5216f5953937b (36.188 B): entries=74, id unik=74 tanpa duplikat; prefix VC- = 61 (seluruhnya kelas K1..K8), prefix AP- = 12 (resep pasangan presisi, tiap caption memuat BENAR/SALAH), sisanya tepat 1 = LEGACY-THRESHOLD kelas WARISAN berkas render/LEGACY-THRESHOLD__datum-chart-buku.png; 61+12+1 = 74 COCOK dengan klaim. (2) Frasa komposisi pembuka body kini menyebut 61 VC famili jenis, 12 AP aparatus benar/salah, 1 aset warisan tunggal LEGACY-THRESHOLD kelas WARISAN - cocok census. (3) Residu frasa lama di GRUP BODY = 0: pola 60 VC = 0 hit, pola 1 WARISAN, 1 LEGACY = 0 hit, token angka 60 berdiri sendiri = 0 hit. Kemunculannya hanya pada catatan iterasi-1 di bawah (jejak temuan, bukan residu). (4) Baris tabel baru Census keluarga (rev-iter1) hadir di seksi 1 dan angkanya terverifikasi ke manifest. (5) Frontmatter utuh pasca-tambalan gatekeeper: yaml.safe_load OK, 18 kunci (tetap, tidak bertambah), nol kunci duplikat, satu baris status, title == H1. Enam dimensi lain tidak diuji ulang pada giliran ini; vonis iterasi-1 atas dimensi itu tetap berlaku. || PUTUSAN: temuan tunggal iterasi-1 tertambal dan terverifikasi mandiri; status naik perlu_revisi -> terverifikasi. Siap vault_promote.py oleh gsp-librarian (non-sensitif, non-dosir, tanpa gate tambahan). || RIWAYAT ITERASI-1 (perlu_revisi, dipertahankan utuh): Verdict: perlu_revisi || Alasan: satu angka komposisi keluarga di paragraf pembuka salah hitung (dimensi g konsistensi internal); enam dimensi lain dan seluruh pin lolos penuh. || Bukti ukur: manifest 4cf5216f5953937b (36.188 B)==pin; 74 entri id unik==ukur; 74 PNG di disk, missing=0, sha256 cocok manifest 74/74; seed=42, dpi=300, matplotlib 3.11.2, numpy 2.4.6, python 3.11.15==ukur; tokens.json disk sha256 da95cb7b...33d9c==manifest; VC-32 sha16 fda8c03a158bc058==disk. TEMUAN: body menyebut '60 VC famili jenis, 12 AP, 1 WARISAN, 1 LEGACY' padahal census manifest+disk = 61 VC + 12 AP + 1 aset tunggal (id LEGACY-THRESHOLD, kelas WARISAN, resep engine datum_chart_buku) = 74; total benar, rincian salah (60 harusnya 61; WARISAN dan LEGACY merujuk berkas yang sama dihitung dua kali). REKOMENDASI: tulis ulang frasa menjadi '61 VC famili jenis, 12 AP aparatus benar/salah, 1 aset warisan (LEGACY-THRESHOLD)' lalu ajukan ulang; dedup vs manifest-aset-kanonis-visual-1005 (64 entri VIS) terbukti berbeda himpunan."
keputusan-promosi: "Promosi t_469ed5fe 2026-10-08 setelah loop revisi 1 iterasi penuh: perlu_revisi (komposisi 60/1/1 salah hitung) -> tambal gatekeeper terverifikasi -> verdict iterasi-2 custodian terverifikasi (61 VC + 12 AP + 1 LEGACY-THRESHOLD). Non-sensitif non-dosir, tanpa gate tambahan."
sumber: docs/2026-10-07-vctl-chart-catalog/assets/manifest.json
halaman: 74 item; pin manifest sha16 4cf5216f5953937b; tokens sha256 da95cb7b..33d9c
tanggal_akses: 2026-10-08
kelas_bukti: primer
sensitif: tidak
perkara: vctl-1007
tags: [vctl-1007, aset-render, datum-token, seed-42, determinisme, terbatas-internal]
links: [docs/2026-10-07-vctl-chart-catalog/verification/VERDICT-V3.md, vault/vctl-1007/2026-10-08_katalog-kanonik-chart-graph-gsp-99-entri-vctl-1007-pin-b860153546765629.md]
penulis: gsp-librarian
diajukan: 2026-10-08
catatan_keputusan: "dipromosikan: VCTL-1007 LIB2: verdict custodian d61925 (katalog/manual iter-1; resep iter-2 pasca-tambal) + keputusan sadar KD-2 terbit-dengan-known-defect; TERBATAS internal saja"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-08
dipromosikan-ke: catatans/resep-render-datum-token-chart-gsp-74-png-manifest-seed-42-vctl-1007.md
---

# Resep Render DATUM-token Chart GSP (74 PNG + manifest, seed 42, VCTL-1007)

Pustaka aset render chart kanonik: 74 PNG 300 dpi (61 VC famili jenis, 12 AP aparatus benar/salah, 1 aset warisan tunggal LEGACY-THRESHOLD kelas WARISAN) dibangkitkan deterministik dengan token gaya DATUM + seed 42; manifest menyimpan resep per aset (lebar_mm, tinggi_mm, font_min, caption, sha256 berkas).

## 1. Pin terukur ulang giliran kurasi ini (08-10-2026, gsp-librarian)

| Field | Nilai |
|---|---|
| Manifest | `docs/2026-10-07-vctl-chart-catalog/assets/manifest.json` sha16 `4cf5216f5953937b` (36.188 B) [R-1, ukur] |
| Item manifest | 74 entri; id unik tanpa duplikat [R-1] |
| Disk | 74 PNG di `assets/render/`; missing=0; sha256 cocok manifest 74/74 (mismatch=0) [R-1] |
| Beku engine | seed=42; dpi=300; matplotlib 3.11.2; numpy 2.4.6; python 3.11.15; tokens `datum-house-style/tokens.json` sha256 `da95cb7b...33d9c` [R-1] |
| VC-32 pasca-FIX-3 | sha16 `fda8c03a158bc058` == klaim driver fix3_d4_regen (73 PNG lain byte-identik) [R-1, cocok disk] |
| Census keluarga (rev-iter1) | 61 VC + 12 AP + 1 LEGACY-THRESHOLD = 74 id unik manifest; WARISAN dan LEGACY pada frasa lama merujuk berkas yang sama dihitung dua kali [R-1, ukur ulang gsp-librarian t_469ed5fe] |

## 2. Rantai provenans

V1 CHECK 4-8 (dua arah manifest<->disk, sha256 100% populasi, render ulang dua-run byte-identik, kanvas+lantai teks+label sintetis) PASS; FIX-3 mengubah hanya VC-32 dengan driver ter-audit; vonis V3 + pengawas SAH (CONTRACT.md ledger V1/V3/FIX-3).

## 3. Nilai guna dan batas

- Semua data pada figur = CONTOH DATA SINTETIS (caption tiap aset menyatakan; jangan dikutip sebagai data riil).
- Resep = pola token rumah DATUM (ramp sekuensial, pasangan presisi, dsb.) - sah dipakai ulang untuk render internal; bukan angka uji.
- Kelas bukti: primer-alat (output eksekusi engine terkunci, determinisme terverifikasi dua-run).
- Dedup: tidak bersinggungan dengan `manifest-aset-kanonis-visual-1005` (64 aset VIS era R12-R15, perkara lain); himpunan berkas dan id berbeda (VC/AP vs VIS).
