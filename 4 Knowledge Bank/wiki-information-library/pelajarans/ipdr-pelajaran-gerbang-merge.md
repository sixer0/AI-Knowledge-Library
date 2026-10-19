---
id: ipdr-pelajaran-gerbang-merge
type: pelajaran
title: Pelajaran gerbang perkakas dari rantai merge registri IPDR-GLOBAL
status: active
sumber: docs/2026-09-12-ipdr-global/reports/ARUS-BALIK-KEMHAN-v1.md
halaman: bagian 2c
tanggal_akses: 2026-09-13
kelas_bukti: sintesis
sensitif: tidak
perkara: ipdr-global-0912
tags: [ipdr, gsp-global-0912, traffic-intelligence, pelajaran, pipeline, merge]
penulis: gsp-librarian
diajukan: 2026-09-12
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-13
dipromosikan-ke: pelajarans/ipdr-pelajaran-gerbang-merge.md
catatan_keputusan: "dipromosikan: revisi VE5-B pin v8 b16d91aa880de478 (D-15; riwayat: promosi VE5 persetujuan user D-11a)"
---

# Pelajaran gerbang perkakas dari rantai merge registri IPDR-GLOBAL

Enam pelajaran terdokumentasi dari pipeline merge misi IPDR-GLOBAL-0912 (GB1..M4), layak jadi preseden library untuk pipeline registri lain (termasuk KEMHAN yang memakai normalizer sekerabat), plus dua pelajaran lapisan pengikatan angka dari reverifikasi V-SUSUN. Kelas akses: internal nonsensitif.

## 1. Pelajaran perkakas gerbang merge

1. PSEUDO_TLD: `com.sa` terpotong jadi root (kasus interkey.com.sa) - daftar root pseudo-TLD harus memuat ccSLD dua segmen. Remediasi tercatat MERGE-M2b-NOTES bagian 3.
2. UMBRELLA_HOSTS perlu `ietf.org`: OPSAWG vs IPFIX WG = badan berbeda di penerbit sama; dedup berbasis host penerbit saja salah-lebur (adjudikasi A-36).
3. PLATFORM_ROOTS perlu `justice.gov`: root institusional pemerintah sah sebagai penerbit bukti identitas (adjudikasi A-29).
4. Normalizer yang membuang titik memicu FAIL-NOMATCH palsu (`fd.io` -> `fd io`); remediasi yang sah = uji host strip-tanda-baca berakun, BUKAN pelolosan buta (M2b-GATE bagian 2).
5. Invarian GENT sequential: placeholder lajur (GENT-30101..30105) dibuang saat merge; nomor master hanya terbit di kartu single-writer (CHECK 7 merge).
6. HTTP 200 bukan bukti entitas bila body stub: thales.co.id 1041-1050 B tanpa token (M2b-GATE, reject berakun); host-token pada stub kosong BUKAN bukti entity-match.

## 2. Pelajaran pengikatan angka (dari V-SUSUN)

1. Cermin beku yang diwarisi verbatim bisa membekukan predikat basi saat hitungan segar naik: ekspor-kontrol persis `BELUM-DIKAJI` 254 vs berawalan 272 (18 varian berpenanda kurung secara semantik masih belum dikaji). Putusan kanonis REV 1 = awalan 272 (pada v8 pola sama terukur: persis 274 vs awalan 292, varian kurung 18); binder wajib menarik hitung ulang, bukan cermin verbatim.
2. Frasa prosa manual wajib ditokenisasi agar terikat panjang tabel: "Enam belas teratas" vs tabel 18 baris (T-2); uji generik `X belas teratas` terhadap jumlah baris nyata kini menjadi CHECK 13 v2.

## 3. PROVENANS

- Akun lengkap: `reports/ARUS-BALIK-KEMHAN-v1.md` (sha16 `2e23f2dc6d4143d8`) bagian 2c; `process/MERGE-M2b-NOTES.md`; `process/M2b-GATE*.json`; `reports/V-SUSUN-003-v1.md` dan `reports/V-SUSUN-003-v2.md` (sha16 `158e35f710443e11`, VERDICT PASS 20 CHECK, seed tercatat `20260912-VS3R-SEED-V2`).
- Registri hasil: beku definitif `registri/REGISTRI-ENTITAS-v8.csv` sha256(16) `b16d91aa880de478` (293 baris; rantai append-only e1940da5 -> v6 -> v7 -> v8, riwayat pin gelombang-1 `e1940da5c400f70f`); rantai seed `registri/SEED-LOG.txt` (sha16 `b7b5fdbf39a94ef2`, tumbuh dari `dba7cd3da2920cf0`).
- Kelas bukti sintesis lintas sumber primer internal misi; seluruh butir menunjuk berkas yang ada di disk.

## REV-4 (2026-09-13, kartu t_384058a8, putusan controller D-15)

- Pin pembilang diganti: BEKU M4 sha256(16) `e1940da5c400f70f` (273 baris; riwayat pin gelombang-1, tetap rujukan sejarah, bukan sunting diam) -> BEKU definitif `registri/REGISTRI-ENTITAS-v8.csv` sha256(16) `b16d91aa880de478` (293 baris data; kapabilitas 262). Rantai beku utuh: e1940da5 -> v6 `75a76c5556f5e932` -> v7 `8c62d91b7fd4a00d` -> v8 `b16d91aa880de478` (deklarasi D-14; diverifikasi VD1-B3 CHECK 1 + countersign VD2-B2 SETUJU-RILIS `c9e42965c30ca200`).
- Angka turunan objek ini ditarik ulang dari v8 lewat `process/ve5b_measure.py` (seed `20260913-VE5B-SEED-V1`; cetakan `process/ve5b_measure.json`). Tabel perubahan lama->baru: `reports/PROMOSI-IL-LOG-v2.md`.
- Kelas akses tidak berubah; persetujuan user D-11a tetap berlaku untuk objek TERBATAS.
