# Audit Manual Standar Masuk: Uji Klaim-Diri-dokumen terhadap Disk
(validated 2026-10-08, audit Manual Komprehensif DATUM Terpadu 000/GSP/STD/X-2026 RevA, 102 hal, jalur user "tanpa orkestrasi")

Kelas tugas: user menyerahkan PDF/DOCX **manual standar / kitab terpadu** yang mengklaim
menyatukan atau menggantikan aturan skill fleet yang sudah hidup. Beda dari
`inbound-document-text-and-number-forensics.md` (objeknya kebenaran isi laporan pihak lain):
di sini objeknya **status normatif dokumen terhadap mesin dan skill yang ada di disk**, karena
manual semacam itu berpotensi dipromosikan jadi rujukan fleet-wide. Pertanyaan pemandu:
"kalau dokumen ini jadi otoritas, apakah setiap klaimnya bisa dijalankan ulang dari artefak
yang benar-benar ada?"

## 1. Baterai uji klaim-diri (urut yield tertinggi)

1. **Klaim mesin/builder.** Setiap skrip yang disebut dipakai ("dibangun dengan X.py",
   rantai verifikasi V2 "eksekusi ...") -> `find` di kanonik + registry fleet + docs misi.
   NOL hasil = temuan MERAH: hasil gerbang yang dilaporkan dokumen tidak dapat direproduksi
   (pelanggaran SPK-002 pada dokumen itu sendiri; laporkan sebagai tabel modul-vs-status,
   jangan narasi berderet nama file mentah - lihat §4). Preseden: 5 dari 7 mesin yang diklaim
   manual DATUM terpadu tidak ada di disk (pustaka chart, pustaka simbol, pembangun Word
   generik, perender tambahan, auditor Figma).
2. **Folder referensi yang dirujuk.** Manual menyebut "references/01..09" milik skill sumber;
   skill `datum-house-style` v2.0.0 ternyata TANPA folder references sama sekali -> seluruh
   "rumah aturan" menggantung. Selalu uji path rujukan silang ke struktur direktori nyata.
3. **Pin hash standar induk.** Standar fleet mengunci sha256[:16] di skill penunjuk
   (GAYA-AHLI-1005, VISUAL-1005). Hitung `sha256sum` berkas di disk: cocok = pin valid;
   beda = standar sudah direvisi (rotasi pin belum terjadi) -> temuan KUNING "pin basi",
   jangan pakai salinan ingatan. Sesi ini: pin GAYA-AHLI revG masih valid; pin VISUAL revC
   sudah bergeser ke revD di disk.
4. **Hitung aturan dengan parser, bukan mata.** Ekstrak Lampiran indeks aturan, regex ID
   (`\bDT-\d+\b` dsb), bandingkan dengan jumlah yang diklaim tabel ruang nama, termasuk
   rincian per lapis SG (L0=5 L1=10 L2=9 L3=9 L4=10 L5=9 L6=16 = 68). Cocok semua = bukti
   struktur internal konsisten (nilai plus untuk vonis).
5. **Token vs prosa.** Heks palet, nilai grid, ambang lint yang dikutip manual -> cek muncul
   di tokens.json / sumber kanonik. Cek juga statusnya: navy/emas "pensiun" di manual ternyata
   memang tercatat `retired` di tokens = cocok, bukan temuan.
6. **Versi basis.** Manual mengaku berdasar "v1.8 Rev J" padahal vonis GAP-09 05-10 mencatat
   mesin Rev J tidak ada di disk dan v2.0.0 adalah rebuild lini baru (larangan klaim restorasi).
   Uji klaim basis versi terhadap register putusan fleet yang hidup - sumber drift paling mahal
   karena menyangga seluruh otoritas dokumen.

## 2. Tabrakan dengan kontrak fleet yang hidup (pencarian wajib dua arah)

- **Kontrak blok ter-propagasi.** `grep -rl "GSP-DOC-KORIDOR"` menemukan 23 skill pemegang
  blok Module L. Bandingkan butir manual baru vs Module L nyata: DT-12 (tanpa garis bawah,
  spasi boleh) MENIADAKAN L.3 (snake_case tanpa spasi). Tabrakan begini = MERAH, harus ada
  putusan kanal eksplisit; mekanismenya sudah ada: fixer D17 (`d17_koridor_block_fix_*.py`,
  backup+manifest sha) + `check_standar.py` CHECK 4 (hash blok verbatim kanonik==fleet==profil).
- **Denominator ganda antar-misi.** Katalog chart manual (58 jenis kode P/H/K/S/W/G) vs katalog
  VCTL-1007 (99 entri VC-01..VC-99) hidup bersamaan -> satu rumah wajib diputus sebelum
  promosi. Cari preseden kelas serupa dengan grep judul/topik di `docs/`.
- **Letak caption / konvensi kecil.** DT-15 (caption di atas) vs SV-TAB-04 (di bawah): tabrakan
  kecil tapi pasti diperdebatkan verifier; catat di register rekonsiliasi, jangan dibiarkan.

## 3. Bentuk vonis yang diterima user

Vonis umum (layak-terima-dengan-syarat) -> tabel kecocokan verified (klaim | uji | hasil) ->
temuan berjenjang MERAH/KUNING/HIJAU bernomor T-nn dengan bukti terukur -> rencana konsolidasi
per sasaran skill (K-nn, versi naik, apa yang TIDAK disentuh dan kenapa) -> register sumber R-n.
Sertakan penyeimbang: bagian yang jujur menyatakan batasnya sendiri (Bab 17.5) dihitung sebagai
kebaikan. Simpan laporan sebagai doc internal (`docs/<tanggal>-<slug>/`), tautkan via MEDIA.
Akhiri dengan pertanyaan keputusan yang konkret (jalankan konsolidasi vs putus temuan dulu),
bukan tawaran umum.

## 4. Pitfall gerbang naturalisasi yang terbukti berlaku (kanal chat)

`scan_ai_footprint.py --channel chat` CHECK 19 (C-13 kode mesin tanpa label manusia, plafon
2 identifier keras) menembak FAIL saat jawaban menyebut deretan nama modul Python (.py) dalam
prosa. Remedinya BUKAN hapus informasi: pindahkan identifier ke TABEL berlabel manusia
(kolom "Modul yang diklaim" + "Status di disk"), lalu scan ulang sampai VERDICT: PASS.
Selaraskan dengan SG-L4-03/C-30 - aturan yang sama yang ditegakkannya pada dokumen orang lain
berlaku pada jawaban kita sendiri. Simpan draf jawaban di berkas scratch dan scan berkas itu
(jangan scan string dari ingatan), catat jejak VERDICT untuk dilaporkan bersama artefak.

## 5. Peta rujukan cepat

- Ekstraksi PDF 102 hal: `pypdf` per-halaman -> simpan `=== PAGE n ===` ke scratch -> slicing
  per halaman dengan regex split untuk baca selektif (hemat konteks vs dump 209 KB sekaligus).
- Interpreter: `uv run --python 3.11 --with pypdf python ...` (alias `python` Store rawan).
- Laporan contoh hasil kelas ini: `docs/2026-10-08-datum-terpadu-audit/AUDIT-DAN-KONSOLIDASI-MANUAL-DATUM-TERPADU.md`.
