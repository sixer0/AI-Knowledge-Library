---
id: cdex-temuan-duplikat-suffix-file
type: fakta
title: "Korpus china-defence-expo — 375 file ber-suffix (1)/(2)/(3), hash membuktikan salinan identik"
status: active
sumber: docs/2026-08-24_china-defence-expo-crawler/README.md
halaman: Ringkasan baris 17-18
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: china-defence-expo-crawler
domain: defense-intel
writer: gsp-librarian
tags: [china-defence-expo-crawler, data-quality, duplikat, korpus, migrasi, defense-intel]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/china-defence-expo-crawler/2026-08-25_cdex-temuan-duplikat-suffix-file.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Korpus china-defence-expo — 375 file ber-suffix (1)/(2)/(3), hash membuktikan salinan identik

## Ringkasan
Korpus raw china-defence-expo (743 file) memiliki pola duplikat penamaan: 375 file ber-akhiran
(1)/(2)/(3) (mis. file(1).ext, file(2).ext). Verifikasi hash membuktikan sebagian salinan
identik secara byte — duplikat nyata, bukan sekadar nama mirip.

## Implikasi
- Sebelum dedup/analisa lebih lanjut, file ber-suffix (1)/(2)/(3) wajib dicek hash; salinan
  identik cukup disimpan satu.
- Pola ini menjadi kandidat utama untuk pembersihan korpus saat migrasi.

## Bukti
- Sumber: docs/2026-08-24_china-defence-expo-crawler/README.md (Ringkasan, baris 17-18).
- Kelas bukti: sekunder (temuan dari task migrasi; hash diklaim dibuktikan di source).
- Angka 375 dan 743 dikutip dari README Ringkasan; tanpa nomor halaman (dokumen non-paginasi).
