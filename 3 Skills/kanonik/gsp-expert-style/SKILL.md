---
name: gsp-expert-style
description: "Skill tipis penunjuk STD-GAYA-AHLI-001 (gaya bahasa, 68 aturan SG) + STD-VISUAL-001 (instrumen visual, 56 aturan SV): cara pakai per kanal + scanner. Muat saat menyusun/menyerahkan keluaran prosa atau keluaran bergambar yang dibaca manusia."
version: 1.2.0
author: GSP (PT. Gemilang Satria Perkasa)
metadata:
  hermes:
    category: gsp
    tags: [gsp, gaya-bahasa, standar, naturalisasi, serah-terima]
---

# GSP Expert Style - Penunjuk STD-GAYA-AHLI-001

Skill ini SENGAJA tipis: ia hanya pointer + cara pakai. Isi normatif 68 aturan SG
tidak pernah diduplikasi di sini; sumber tunggalnya manual di bawah. Bila teks skill
ini dan manual bertentangan, MANUAL yang menang.
Marker adopsi fleet: GAYA-AHLI-1005 (kartu t_567f9f36, 06-10-2026).
Marker adopsi fleet visual: VISUAL-1005 (kartu t_c7f8f27c, 06-10-2026). Seksi
visual adalah PENDEKATAN POINTER yang sama: isi normatif tetap di manual, tidak
diduplikasi.

## Rujukan kanonis (sumber tunggal)

- Manual: `C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-10-05-gaya-bahasa-forensik/manual/STD-GAYA-AHLI-001.md`
- sha256[:16] terkunci saat skill ditulis: `b83e6bca4a4d4d04` (revG = vonis lepas final 06-10, reshoot-3 dua juri 16/16 LULUS-LEPAS rata 4,00 x4 + suntingan backtick konten-kekal ber-assert; era revE 5d449eee sah di eranya; badan aturan identik revD `c317e0fbcafbefb7`).
- Cek drift sebelum pakai: hitung sha256 berkas dan bandingkan. Beda = manual direvisi; baca Lembar Kendali 1.1 dulu, jangan pakai ingatan salinan lama.
- Struktur: tujuh lapis L0 orientasi pembaca, L1 arsitektur dokumen, L2 paragraf, L3 kalimat, L4 kata/identifier, L5 suara ahli, L6 gerbang. 68 aturan SG bernomor dengan enam bidang wajib per aturan (pernyataan, fungsi pembaca, bukti manusia, kontras fleet, predikat verifikasi, instrumen penegak).
- Kitab induk gabungan (bentuk+visual+bahasa): Manual Komprehensif DATUM GSP
  (000/GSP/STD/X/2026 RevA; nomor final menunggu Register Induk ARSIP, putusan 08-10).
  Salinan kerja terpadu untuk penulis; sumber tunggal normatif per bidang tetap: SG dari
  STD-GAYA-AHLI, bentuk dari datum-house-style, visual dari STD-VISUAL-001. Konflik ->
  manual bidangnya menang, kitab menunjuk (satu rumah SG-L1-09).

## Kapan dimuat

Muat sebelum menulis/menyerahkan keluaran prosa yang dibaca manusia pada kanal mana pun
(chat kerja, dokumen/laporan/proposal, deck, etalase, notifikasi). Keluaran antar-agen
(komentar kanban, checkpoint, metadata mesin) dikecualikan dari gerbang serah sesuai
persempitan 03-09, tetapi tetap tidak boleh melanggar A1/A2 bila dibaca user.

## Cara pakai per kanal (register D-TA-05, bobot lapis per manual Seksi Register Kanal)

| Kanal scanner | Register | Yang berlaku |
|---|---|---|
| `chat` | K1 formal-effisien | L3-L5 penuh; tanpa emoji, tanpa basa-basi servil; dokumen panjang (L0/L1) tidak dipaksakan |
| `doc` | K2 formal institusional | Tujuh lapis penuh; kepala dokumen tunduk SG-L0; tabel/angka tunduk SPK-002 (bukan gaya) |
| `deck` | K3 formal institusional | L3/L4 pada teks slide; L1 jadi arsitektur alur deck |
| `etalase` | K6 formal institusional | Tujuh lapis + gerbang L6 penuh pada paket serah |
| `notif` | K4 formal-netral | Ringkas; L4 konsistensi identifier; ISO waktu boleh (metadata) |
| `sosmed` | parsial (D-TA-08, tercatat di `gsp-output-naturalization` SKILL.md seksi kanal, bukan di manual) | Mengikuti brief kampanye; A1/A2 tetap mutlak; jangan rata-ratakan genre |
| `kanban`/`kitab` | dikecualikan / pengecualian tercatat | Bukan gerbang serah; lihat Seksi Register Kanal Berbobot manual |

Kanal ditetapkan SEBELUM penyusunan keluaran dan disebut eksplisit saat menjalankan scanner.

## Gerbang serah (scanner v1.9.1+)

```text
C:/Users/TRIAL/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe ^
  C:/Users/TRIAL/AppData/Local/hermes/skills/gsp/gsp-output-naturalization/scripts/scan_ai_footprint.py ^
  <berkas-atau-dir> --channel <chat|doc|deck|etalase|notif|sosmed>
```

- Keluaran wajib lolos scanner pada kanal yang sesuai SEBELUM diserahkan ke manusia
  (gerbang naturalisasi; FAIL -> naturalisasi ulang -> cek ulang, konten-kekal: angka,
  fakta, satuan, sitasi tidak boleh berubah).
- A1/A2 (em dash, middle dot) nol di semua keluaran user.
- Jejak cek (laporan scanner atau centang-manual berformat) dilaporkan bersama artefak.

## Aturan bukti-manusia (inti yang paling sering dilanggar)

Dasar sebuah aturan gaya adalah kutipan verbatim tulisan manusia ber-path yang dapat
dicek ulang (bidang 3), BUKAN ambang angka. Angka statistik hanya menjadi ambang bantu
berlabel DIAGNOSIS pada bidang 5. Contoh karangan selalu berlabel CONTOH-ILUSTRATIF dan
tidak pernah mengisi bidang bukti. Akar path kutipan (CONTRACT manual 1.4): `work/` =
`docs/2026-10-05-gaya-bahasa-forensik/work/`; `DEM/`, `VAULT/`, `EKAS/` seperti tercetak
di manual; buku ditandai `PDF n`.

## Penunjuk STD-VISUAL-001 (instrumen visual) [VISUAL-1005]

Skill ini juga memegang pointer standar visual karena satu-satunya kelas tugas yang
membutuhkannya (keluaran bergambar dibaca manusia) selalu membawa prosa dan tunduk dua
standar sekaligus; satu berkas tipis = satu unit distribusi ke registry fleet (putusan
perluasan vs sibling baru, alasan lengkap `work/f4_adopsi-notes.md` misi VISUAL-1005).

- Manual: `C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-10-06-visual-instrument/manual/STD-VISUAL-001.md`
- Pin hidup sha256[:16]: `ec6a642024a38e4f` (revD, rotasi 08-10 lewat prosedur Lembar
  Kendali; revD = sajian DOCX+PDF dogfood engine DATUM kanonis, badan aturan identik
  revC `a3503a73`; ledger: era revC `eddb2866f3c79cb8` sah 06-10 s.d. 07-10). Beda hash =
  pedoman direvisi; baca Lembar Kendali dulu, jangan pakai ingatan salinan lama.
- Struktur: 56 aturan SV lima kelompok (SIM 11 simbol/notasi, GRA 15 chart, DIA 7 diagram,
  TAB 10 tabel, LAY 13 layout/anatomi), enam bidang wajib per aturan, register kanal K2+K6.
- Muat sebelum merancang/menyerahkan keluaran bergambar (docx/pptx/xlsx/pdf) pada kanal
  sasaran; VS-12 mewajibkan penetapan kelompok aktif dan alokasi aset sejak outline, bukan finishing.
- Figur hanya dari registri aset `docs/2026-10-06-visual-instrument/assets/aset.json` lewat
  `render_aset.py` kanonis (palet runtime-read); glif rekaan di luar registri dilarang (SV-SIM-04).
- Scanner: kanal resmi naskah standar = `standar` v1.10.0+; kanal keluaran sesuai jenisnya
  (doc/deck/etalase). Perintah sama seperti gerbang serah di atas, ganti `--channel`.
- Batas: bentuk dokumen tetap DATUM/GSP-SDT, akurasi angka SPK-002, bahasa tetap lapis
  SG di atas; seksi ini hanya instrumen visual.

## Batas

- Skill ini tidak menormalkan bentuk dokumen atau akurasi data: DATUM/GSP-SDT memegang
  anatomi, SPK-002 memegang akurasi; manual ini hanya bahasa (gerbang A-F2.7 manual).
- Jangan menyalin isi manual ke profil/SOUL/blueprint; rujuk path + sha.
- Klasifikasi manual TERBATAS internal fleet: memuat kutipan verbatim korpus, tidak untuk
  distribusi luar.
