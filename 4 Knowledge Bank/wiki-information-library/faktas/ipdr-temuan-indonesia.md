---
id: ipdr-temuan-indonesia
type: fakta
title: "Temuan Indonesia: jejak domestik dan pemasok lokal IPDR/LI"
status: active
sumber: docs/2026-09-12-ipdr-global/registri/REGISTRI-ENTITAS-v8.csv
halaman: kolom jejak-INDONESIA+negara (293 baris)
tanggal_akses: 2026-09-13
kelas_bukti: sintesis
sensitif: ya
perkara: ipdr-global-0912
tags: [ipdr, gsp-global-0912, traffic-intelligence, indonesia, drill]
penulis: gsp-librarian
diajukan: 2026-09-12
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-13
dipromosikan-ke: faktas/ipdr-temuan-indonesia.md
persetujuan-ref: user-webui-2026-09-12T22:3x-D-11a-kartu-t_fbfc624b
catatan_keputusan: "dipromosikan: revisi VE5-B pin v8 b16d91aa880de478 (D-15; riwayat: promosi VE5 persetujuan user D-11a)"
---

# Temuan Indonesia: jejak domestik dan pemasok lokal IPDR/LI

Ringkasan keterlibatan Indonesia dari registri beku definitif v8 IPDR-GLOBAL-0912, hasil drill dua putaran (DRILL-ID-A/B) dan lajur G-C7. Kelas akses: internal-TERBATAS (memuat baris aparat/regulator domestik dan kanal APARAT-DIREKT lokal), mengikuti label sumber.

## 1. Populasi terukur (registri beku v8, diukur ulang giliran revisi ini)

- jejak-INDONESIA = ADA: 66 baris dari total 293 (semua bentuk keterlibatan, termasuk distributor regional).
- Bernegara Indonesia: 15 baris (rinci kelas bentuk di bawah).
- Vendor Indonesia dengan token literal IPDR di bukti: Heksagon (GENT-00016), PT. Artha Inti Prima (GENT-00100, adjudikasi badan hukum AHU nomor registrasi 40530 Kemayoran Jakarta Pusat).

## 2. Tiga kelas bentuk keterlibatan

1. Vendor/integrator domestik penjual langsung: Heksagon (GENT-00016, IPDR literal, DUA-KANAL, VERIFIED-L1), PT. Artha Inti Prima (GENT-00100, IPDR literal + LI patuh ETSI/3GPP/CALEA, VERIFIED-L1), Siberindo (GENT-00101, INTEGRATOR, APARAT-DIREKT, VERIFIED-L1), PT Len Industri (GENT-00102, PARTIAL), PT INTI (GENT-00103, PARTIAL), PT Sasmita Wikrama Nusantara (GENT-00182, ISV, APARAT-DIREKT, VERIFIED-L1), Rokade (GENT-00183), Bounga Solusi Informatika (GENT-00181), SoftwareAsli (GENT-00184).
2. Kerangka regulator domestik sebagai beban kepatuhan sekaligus pencipta pasar: UU 11/2008 ITE jo. UU 19/2016 (GENT-00105), PP 71/2019 PSTE (GENT-00106), BSSN (GENT-00107, PARTIAL), Komdigi (GENT-00108, PARTIAL; situs langsung 403 WAF, bukti lewat cermin arsip + LPSE berakun).
3. Distributor regional dengan bukti dokumen ke institusi Indonesia: ESW Systems Pte Ltd (GENT-00213, VERIFIED-L2), Ataka Enterprises Pte Ltd (GENT-00214, VERIFIED-L1), Omni Integer Pte Ltd (GENT-00185, MITRA-RESELLER, distributor Amped FIVE untuk SG/MY/ID) - ketiganya lewat laporan Amnesty International Security Lab, label L2 dengan korroborasi LSM bukan aparat; baca sebagai indikasi, bukan konfirmasi pengadaan resmi. Dua mitra kanal masuk kelas ini pada v8: VST ECS (Thailand) (GENT-00229, jejak-INDONESIA=ADA level GRUP via PT ECS Indo Jaya - BUKAN badan hukum sama, label wajib) dan TDS (tds-apac) (GENT-00230, jejak-INDONESIA=ADA level KANAL-PARTNER via post resmi LinkedIn TDS 2026-06-25 event Jakarta lewat PT. Binareka Tatamandiri + ASIX, fetch 200 ts 17:26:48Z; domisili badan hukum belum terbukti; adjudikasi level rilis menunggu putusan controller - O-B4).

Catatan: PT Telkom Indonesia (GENT-00104, TELKO-HULU murni, PARTIAL) TIDAK boleh dibaca sebagai solusi aparat tanpa bukti penawaran (TA-D-11). ENT-14290 A10 Networks: klaim emisi IPDR HANYA snippet PROV mirror, status PARTIAL, jangan naik ke kolom terbit tanpa remediasi (SPK-002 butir 4/5). Adjudikasi F-1 (putusan controller D-13, tercatat v8): GENT-00224 'Quality Net Solutions' = ENT-14438 QualityNet Solutions (Jepang) - merged, merge dua arah tercatat di catatan-risiko ENT-14438, gap register tepat 1 (id 224), bukti lama tersimpan utuh; jejak-ID ENT-14438 tetap TIDAK.

## 3. PROVENANS

- Pembilang tunggal: `registri/REGISTRI-ENTITAS-v8.csv` sha256(16) `b16d91aa880de478` (293 baris), diukur ulang giliran revisi ini lewat `process/ve5b_measure.py` (jejak ADA 66, negara Indonesia 15). Riwayat pin gelombang-1: `e1940da5c400f70f` (273 baris; jejak ADA 64).
- Drill: `process/LADDER-DRILL-ID-A.md` (8.411 B), `process/LADDER-DRILL-ID-B.md` (15.894 B); lajur `process/LADDER-GC7*.md`; drill jejak-ID v8 di `process/LADDER-GC1GAP-*.md`.
- Rantai seed GB1..M4 + GC1-GAP..F1 (`registri/SEED-LOG.txt` sha16 `b7b5fdbf39a94ef2`, tumbuh dari `dba7cd3da2920cf0`; blok M4 update jejak-ID A/B + blok F1 drill GENT-00230 tercatat di SEED-LOG).
- Laporan verifikasi: VD1 sha16 `03f7a0598c92d456` (SALAH-TARGET 0), VD2 sha16 `f0dd9dc7c4ae021e`, V-SUSUN v2 sha16 `158e35f710443e11` PASS; VD3 `reports/VERIFIKASI-AKURASI-v3.md` (sha16 `a10d8acb87019a8f`), VD4 `reports/VERIFIKASI-AKURASI-v4.md` (sha16 `b0843be81117384c`), countersign VD2-B2 `reports/COUNTERSIGN-v3.md` (sha16 `c9e42965c30ca200`, VERDICT SETUJU-RILIS, sumber definitif v8).
- Persetujuan promosi: user via WebUI 2026-09-12 22:3x verbatim "1. Masukkan ke Information Library" (kontrak D-11a, kartu t_fbfc624b).

## REV-4 (2026-09-13, kartu t_384058a8, putusan controller D-15)

- Pin pembilang diganti: BEKU M4 sha256(16) `e1940da5c400f70f` (273 baris; riwayat pin gelombang-1, tetap rujukan sejarah, bukan sunting diam) -> BEKU definitif `registri/REGISTRI-ENTITAS-v8.csv` sha256(16) `b16d91aa880de478` (293 baris data; kapabilitas 262). Rantai beku utuh: e1940da5 -> v6 `75a76c5556f5e932` -> v7 `8c62d91b7fd4a00d` -> v8 `b16d91aa880de478` (deklarasi D-14; diverifikasi VD1-B3 CHECK 1 + countersign VD2-B2 SETUJU-RILIS `c9e42965c30ca200`).
- Angka turunan objek ini ditarik ulang dari v8 lewat `process/ve5b_measure.py` (seed `20260913-VE5B-SEED-V1`; cetakan `process/ve5b_measure.json`). Tabel perubahan lama->baru: `reports/PROMOSI-IL-LOG-v2.md`.
- Kelas akses tidak berubah; persetujuan user D-11a tetap berlaku untuk objek TERBATAS.
