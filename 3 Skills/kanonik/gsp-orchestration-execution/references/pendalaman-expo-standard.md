# Rujukan Standar Pendalaman Expo (STD/PDL/EXPO/IX/2026 v1.0)

Berlaku untuk SETIAP misi pendalaman expo tersendiri yang berangkat sejak 05-IX-2026
(forward-only; GSX/INTEROP = instance historis). Direktif user 05-09: standar dicatat
sebagai ATURAN, konten artefak tidak diubah.

- Dokumen kanonis: `docs/2026-09-05-pendalaman-expo-standard/STANDAR-PENDALAMAN-EXPO.md`
  (shared ws; sha256 3dc4b11db6c2c4d7... saat terbit 05-09; salinan sha-identik di
  `handover/expo2026/` dan `EXPO [2026]/`).
- Instance normatif: Automate26 RevA xlsx sha dc25d7b42634f69c...cce97 + narasi
  sha 22eb536a8dcebee3...3580 (keduanya JANGAN disentuh).
- Isi inti: D1 susunan 13 lembar + kepala DATUM/freeze A6; D2 PD 24 kolom (18 kanonik +
  6 terbit relevansi WAJIB default), VERDIKT-group LARANG; D3 RELEVANSI-GSP 24 kolom satu
  kanal; D5 KENDALI formula hidup + bendera OK TO ISSUE; D6 gerbang rilis (roundtrip 0,
  tampil-tautan defect 0, gate SPK-002 SALAH-TARGET=0, LADDER, determinisme SEL); D7 narasi
  pendamping; D8 rumus relevansi integer TETAP (S=min(100,Lmax+T+B); agregat top-3 berbobot
  floor; kelayakan ukuran kedua; sort tie-break account_key; jejak byte-level; ambang tinjau);
  D9 tata kelola (PRM/VRS, forward-only, modul dilarang disalin-belokkan, uv --with eksplisit).
- Kartu misi pendalaman berikutnya WAJIB menempel Lampiran CHECK B01-B12 / V01-V14 / C01-C05
  dari dokumen standar + mengisi register PRM di kontrak + mencatat versi standar (FS-46).
- Pemetaan ke rantai: kontrak dibuka -> isi PRM -> DAG pipeline kanonis v1 tidak berubah;
  kartu BUILD/VERIFY/CS mendapat CHECK dari lampiran standar, bukan dikarang ulang.
- Jejak gerbang naturalisasi dokumen standar: scanner kanal=doc PASS kecuali CHECK 12
  (paragraf <4 kalimat) - dikecualikan register: dokumen norma berformat butir daftar,
  bukan prosa; A1/A2 nol mutlak (CHECK 2 PASS).
