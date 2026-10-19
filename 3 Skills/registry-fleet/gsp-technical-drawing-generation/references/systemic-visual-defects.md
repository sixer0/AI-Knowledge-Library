# Kelas cacat visual sistemik pada lembar deterministik (preseden CAD-RUMAH1020-0920)

Terekam 2026-09-20. Tiga lane gambar (arsitektur/struktur/MEP) menutup kartu done-L1
dengan QA numerik lane PASS semua, tetapi vision QA controller sebelum serah memvonis
lembar struktur dan MEP belum layak konsultan. Denah arsitektur (A-02) bersih.

## 1. Kop field-shift (title block salah kolom)
Bukti nyata (baca dari PNG lembar S):
- NO LEMBAR terisi "1:150" / "1:20" (seharusnya skala di kolom SKALA)
- JUDUL LEMBAR terisi "gsp-engineering-analyst" (nama profil agen!)
- TANGGAL terisi "PRELIM"; REV terisi tanggal; SKALA/DIGAMBAR/STATUS kosong
Akar: generator menulis LIST nilai ke LIST label tanpa pemetaan named-field; geser satu
elemen = semua kolom salah. Tambal: dict {field: nilai} eksplisit per lembar.
Gerbang: pypdf extract_text per halaman, assert kode lembar ("S-01") muncul di area field
No lembar dan TIDAK ada string "gsp-" (nama profil) di teks lembar.

## 2. Token internal bocor ke muka lembar
Bukti nyata: "[JSON]", "[JSON fp_reinf]", "[PRM-14]", "dibaca langsung dari
HITUNG-STRUKTUR.json", "titik_me", "[SNI 2847 tidak ada di rak]", sub-header
"misi CAD-RUMAH1020-0920 | sumber: MODEL-RUMAH1020.json".
Aturan: token provenance boleh di artefak INTERNAL antar-agen (MD/JSON), DILARANG di
PNG/PDF yang dibaca manusia. Ganti cara rujuk, jangan hapus substansi:
"[JSON]" -> "(lihat Lembar Hitung S-08)"; "titik_me" -> "titik lampu/saklar/kontak";
"[SNI 2847 tidak ada di rak]" -> tulis metode koefisien yang benar-benar dipakai +
catatan verifikasi insinyur.
Gerbang (target 0 temuan) pada extract_text PDF paket:
grep -E "\[JSON\]|\[PRM|\.json|titik_me|tidak ada di rak|gsp-[a-z-]+"

## 3. Tabrakan teks lintas-axes (buta bagi QA per-axes)
Bukti nyata: blok CATATAN S-01 menimpa bubble grid bawah; "PT GEMILANG SATRIA PERKASA"
vertikal menabrak bingkai; label "rel DP-1" tertindih garis busbar; notasi potongan
B-B vs kode jendela Wnn di tepi kanan denah; bubble grid dua digit (10/11) tubruk
sendiri pada band rapat.
Akar: QA lama menarik bbox hanya dari ax.texts SATU axes; teks axes tetangga dan
fig.texts tidak pernah diuji berpasangan lintas komponen.
Tambal alat: scripts/qa_figure_level.py - kumpulkan ax.texts SEMUA axes + fig.texts,
setelah draw() pakai get_window_extent(renderer), uji OUT-PAGE / OUT-AXES /
OVERLAP>25% bbox terkecil antar pasangan. Iterasi GENERATOR (bukan gambarnya) sampai 0.
Teknik posisi yang terbukti: bubble grid dua digit = penempatan greedy anti-tubruk
(offset band selang-seling); label panah vs dimensi dipisah vertikal; teks DUPLIKAT
informasi boleh dihapus, data tidak pernah.

## Gerbang serah kelas tugas ini (urutan wajib)
1. QA level-figure 0 temuan semua lembar (skrip).
2. Uji field-kop via extract_text (skrip).
3. Grep token bocor pada PDF paket (target 0).
4. vision_analyze controller minimal 1 lembar per disiplin; ls folder png dulu agar
   path tepat.
5. Hanya setelah 1-4 bersih: klaim siap-serah / rakit PDF final.
