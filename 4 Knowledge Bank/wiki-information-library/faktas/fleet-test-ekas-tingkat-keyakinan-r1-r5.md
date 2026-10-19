---
id: fleet-test-ekas-tingkat-keyakinan-r1-r5
type: fakta
title: "Tingkat keyakinan sumber EKAS R1-R5 dan keadaan rak (2026-08-24)"
status: active
sumber: docs/2026-08-24_fleet_test/gsp-data-collector/collection_report.md
halaman: hal. 1 (README EKAS baris 18-27, 33-43, 79-80, 93-96)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: fleet-test-2026-08-24
domain: engineering
writer: gsp-librarian
tags: [ekas, sumber, r1-r5, provenans, engineering]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/fleet-test-2026-08-24/2026-08-25_fleet-test-ekas-tingkat-keyakinan-r1-r5.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Tingkat keyakinan sumber EKAS R1-R5 dan keadaan rak (2026-08-24)


Sistem EKAS menetapkan 5 tingkat keyakinan sumber R1-R5 [sumber — README.md baris 18-27, 79-80 via gsp-data-collector]:
- R1 regulasi Indonesia/SNI/standar normatif nasional — mengikat hukum untuk ambang terima;
- R2 standar internasional (IEC/IEEE/BS EN/ANSI-NETA) — sah bila diadopsi kontrak;
- R3 buku teks/handbook — hanya bila kontrak mengadopsi tertulis;
- R4 dokumentasi teknis OEM — wajib untuk angka melekat produk;
- R5 sumber sekunder — penunjuk saja, tidak pernah menjadi sandaran akhir.

Keadaan rak 2026-08-24 [sumber — README.md baris 33-43]: R1 = 0, R2 = 5, R3 = 24, R4 = 0, R5 = 8.
Implikasi: GSP dapat merancang/menghitung dan menetapkan ambang untuk lima jenis pengujian, tetapi TIDAK dapat menyatakan kepatuhan hukum Indonesia (R1 kosong) dan tidak boleh menyebut angka produk tanpa bahan pabrikan (R4 kosong).

Batas sistem [sumber — README.md baris 93-96]: nomor halaman merujuk halaman PDF (bukan cetak); Diesel Generator Handbook kehilangan ±55 halaman (Bab 11 emergency & standby seluruhnya tidak tersedia); tiga buku catu daya terbit 2000-2004 — kerangka hitung sahih tetapi angka produknya tidak.

Kelas bukti: sekunder (sintesis laporan smoke-test dari sumber primer EKAS README; kanonik tetap ekas/00_START-HERE/README.md).
