---
id: ipdr-value-chain-taxonomy-r1-r7
type: standar
title: Taksonomi rantai nilai IPDR R1..R7 + demarkasi PASIF/AKTIF (versi GLOBAL)
status: active
sumber: docs/2026-09-12-ipdr-global/identification/02_structured.md
halaman: baris 80-89
tanggal_akses: 2026-09-13
kelas_bukti: sintesis
sensitif: tidak
perkara: ipdr-global-0912
tags: [ipdr, gsp-global-0912, traffic-intelligence, taksonomi, rantai-nilai]
penulis: gsp-librarian
diajukan: 2026-09-12
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-13
dipromosikan-ke: standars/ipdr-value-chain-taxonomy-r1-r7.md
catatan_keputusan: "dipromosikan: revisi VE5-B pin v8 b16d91aa880de478 (D-15; riwayat: promosi VE5 persetujuan user D-11a)"
---

# Taksonomi rantai nilai IPDR R1..R7 + demarkasi PASIF/AKTIF (versi GLOBAL)

Kerangka tujuh lapis untuk penjodohan kapabilitas IPDR/traffic-intelligence, diwarisi UTUH dari misi IPDR-KEMHAN (sumber kanonis `docs/2026-09-12-ipdr-kemhan/identification/02_structured.md` baris 126-138; salin-silang keputusan D-05) lalu divalidasi dan diadaptasi oleh sapuan eksternal IPDR-GLOBAL-0912. Kelas akses: internal nonsensitif.

## 1. Ketujuh lapis (definisi ringkas)

| Lapis | Nama | Cakupan | Jalur tata kelola |
|---|---|---|---|
| R1 | Probe dan pengumpulan | tap/mirror, packet capture, network recorder, probe inline/out-of-band | PASIF |
| R2 | DPI dan parsing protokol | deep packet inspection, application recognition, parsing protokol | PASIF-AKTIF (demarkasi TA-D-09) |
| R3 | Pembangkit dan agregasi record | IPDR/CDR generation, mediation, enrichment identitas pelanggan | PASIF (metadata) |
| R4 | Penyimpanan dan retensi | retensi metadata, penyimpanan massal arsip trafik, tiering | AKTIF bila retensi konten |
| R5 | Analitik dan visualisasi | analitik trafik, UEBA, dashboard, kueri rekaman | PASIF |
| R6 | Kepatuhan dan intersepsi sah | lawful interception/lawful access, handoff ke otoritas | AKTIF (wajib landasan hukum) |
| R7 | Integrasi SOC/tata kelola | antarmuka SIEM/SOC/command center, manajemen kasus, RBAC, audit trail | Lintas jalur |

## 2. Dua adaptasi GLOBAL terbukti

1. Badan standar/regulator menjadi KELAS ENTITAS tersendiri (SDO-REGULATOR, non-kapabilitas, di luar pembilang jenuh) alih-alih lapis R8 tambahan (putusan Q-4a; populasi terukur 22 baris).
2. Validasi pengisian: ketujuh lapis terisi tanpa lapis hilang diam-diam. Terukur atas registri beku definitif v8 giliran revisi ini: lapis terbukti (utama+sekunder) R1 71, R2 42, R3 72, R4 19, R5 81, R6 57, R7 35; lapis utama R4 milik gap bernama seed KEMHAN tetap terisi 9 utama + 19 terbukti; KOSONG-beralasan 13.

## 3. Aturan pakai

- Sumbu kapabilitas (R1..R7) berbeda dari sumbu klaster taksonomi solusi RevC; keduanya tidak boleh saling menggantikan (dasar butir AM-G1).
- Demarkasi PASIF/AKTIF ikut TA-D-09 KEMHAN; fungsi AKTIF wajib tertambat baris register risiko kepatuhan.
- Lapis bukan label pemasaran: tiap label wajib bukti per baris registri (kolom bukti-sumber + URL-bukti lolos entity-match).

## 4. PROVENANS

- Pin registri beku definitif: sha256(16) `b16d91aa880de478` (356.251 B, 293 baris), diukur ulang giliran revisi ini. Riwayat pin gelombang-1: `e1940da5c400f70f` (273 baris).
- Blueprint: `docs/2026-09-12-ipdr-global/identification/02_structured.md` (sha16 `1c5a0062092996ab`, baris 80-89 tabel R + guard); kanon KEMHAN `docs/2026-09-12-ipdr-kemhan/identification/02_structured.md` baris 126-138.
- Skema kolom: `registri/SKEMA-REGISTRI-v1.md` (sha16 `d3cee2b490c1da06`; revisi v1.1 append-only, riwayat v1.0 `9c32f0237c441688`).
- Rantai seed GB1..M4 + GC1-GAP..F1 (`registri/SEED-LOG.txt` sha16 `b7b5fdbf39a94ef2`, tumbuh append-only dari `dba7cd3da2920cf0`); 33 ladder `process/LADDER-*.md`; VD1 `03f7a0598c92d456`, VD2 `f0dd9dc7c4ae021e`, V-SUSUN v2 `158e35f710443e11` PASS; VD3 `reports/VERIFIKASI-AKURASI-v3.md` (sha16 `a10d8acb87019a8f`), VD4 `reports/VERIFIKASI-AKURASI-v4.md` (sha16 `b0843be81117384c`), countersign VD2-B2 `reports/COUNTERSIGN-v3.md` (sha16 `c9e42965c30ca200`, VERDICT SETUJU-RILIS, sumber definitif v8).
- Temuan pengisi gap R4: `reports/ARUS-BALIK-KEMHAN-v1.md` (sha16 `2e23f2dc6d4143d8`) bagian 1a/1b.

## REV-5 (2026-09-13, kartu t_384058a8, putusan controller D-15)

- Pin pembilang diganti: BEKU M4 sha256(16) `e1940da5c400f70f` (273 baris; riwayat pin gelombang-1, tetap rujukan sejarah, bukan sunting diam) -> BEKU definitif `registri/REGISTRI-ENTITAS-v8.csv` sha256(16) `b16d91aa880de478` (293 baris data; kapabilitas 262). Rantai beku utuh: e1940da5 -> v6 `75a76c5556f5e932` -> v7 `8c62d91b7fd4a00d` -> v8 `b16d91aa880de478` (deklarasi D-14; diverifikasi VD1-B3 CHECK 1 + countersign VD2-B2 SETUJU-RILIS `c9e42965c30ca200`).
- Angka turunan objek ini ditarik ulang dari v8 lewat `process/ve5b_measure.py` (seed `20260913-VE5B-SEED-V1`; cetakan `process/ve5b_measure.json`). Tabel perubahan lama->baru: `reports/PROMOSI-IL-LOG-v2.md`.
- Kelas akses tidak berubah; persetujuan user D-11a tetap berlaku untuk objek TERBATAS.
