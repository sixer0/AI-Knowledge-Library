# Supervisor lessons wave 07-10 malam (papan GAYAMANUAL-1007 + misi paralel 1007)

Sumber: countersign pengawas GM-L1..L7/L6b, VCTL RT/TA/R1/R1b/R2/R3/R4/C1, JWB1-8/GCERPOP-C/D/REGATED/G8SYNC/SERAH-B (PROMANUAL-V2 closeout), FIX-SA3B/3C/3D + L11/L12B/L12C-D/L13 (INDUK).

## 1. Canon-source inversion audit (kelas baru, GM-L2 -> L5 -> L6b -> L7)

Saat dokumen hilir memilih SATU sumber kanonis di antara DUA VARIAN aturan yang sama (mis. indeks = cermin outline terkunci vs badan = pernyataan pasca-revisi):
- Probe byte kedua varian dari SUMBER primer (baris indeks vs baris badan dari inventaris), lalu grep kedua potongan khas ke artefak hilir. Kalau hilir mengutip varian PRA-REVISI untuk entri ber-delta: itu BUKAN salah pekerja (faithful ke outline = jalur benar) - pertanyaan desain milik controller.
- Escalate berantai tiap kartu berikutnya sampai terbukti di ARTIFAK RAKIT (PDF final memuat kata lama). Setelah terbit, biaya naik dari "re-kutip mekanis" jadi "re-rakit penuh". Vonis pengawas: sajikan dua jalur sah (sahkan-varian + register delta ATAU ganti-sumber + re-rakit lewat pipeline idempoten yang sudah ada), jangan putuskan sendiri.
- Deteksi dini di lapis inventaris: field `verbatim_indeks_vs_badan` / `catatan_mismatch` dalam register = bahan pertanyaan yang HARUS diajukan sebelum blok tulis jalan (GM-L1 sudahvonis delta 17 substantif; outline yang memilih indeks tanpa menjawab = tagihan naik).

## 2. Pin-freeze-before-repair check (register gabungan, REG-D3)

Kartu konsolidasi/register gabungan yang dipromosikan <= beberapa menit setelah kartu sumber tutup `partial-handoff` dengan cacat bernama = risiko membekukan byte pra-tambal sebagai "siap":
- Cek: mtime promosi vs daftar cacat named di laporan sumber; grep kata-kata cacat ("margin", "cacat", "pra-tambal") ke register gabungan - nol temuan = anotasi hilang.
- Rekomendasi baku: jalankan kartu repair dulu, lalu jalankan ULANG skrip konsolidasi idempoten (murah), ATAU anotasi baris terdampak. Jangan promosi rakit hilir dari snapshot basi-by-construction.
- Aturan umur-pin yang dipuji: pekerja yang menulis sendiri "sha kini mencerminkan artefak PRA-TAMBAL, jangan dipakai sebagai pin final, regenerasi setelah bersih" = hash jujur-umur > hash tampak-final (pelajaran-ke-13 bentuk terbaik).

## 3. Scanner genre-mismatch + zona kutipan manusia (FAIL yang tidak boleh ditambal)

- Scanner prosa (C-7 rasio paragraf pendek, C-8b pengakuan-batasan, C-13 identifier) atas dokumen GENRE TABEL/REGISTER (outline, katalog, lampiran) menghasilkan FAIL struktural yang sah tapi salah-sasaran: vonis pengawas = register known-defect genre ATAU uji level-buku saat rakit; JANGAN paksa outline jadi prosa demi hijau.
- Temuan A4/C-4 berupa frasa percakapan ("let me know if") WAJIB dibedah konteksnya dulu: kalau ia hidup di dalam KUTIPAN SURAT MANUSIA ASLI yang justru DIADILI dokumen sebagai contoh tersangkal = positif-palsu kelas self-reference; zona pengecualian kutipan ber-path adalah tagihan fitur R-1. Jangan laporkan sebagai pelanggaran agen.
- Kanal pemindaian harus dikunci eksplisit saat dua kanal punya ambang beda (kanal standar 20% vs kanal doc <=1): laporan tanpa kunci kanal = risk tambal ke angka salah-sasaran (F-GAKUR-01 versi kanal). GM-L6b mencontohkan penutupan benar: kunci kanal acuan + residual kanal lain dibiarkan TERDOKUMENTASI, bukan dipaksa.

## 4. Parser-blindness catalog (pelajaran-ke-11, enam kasus satu wave)

Sebelum mengklaim cacat artefak, setiap sensor gagal harus dibedah sampai penyebabnya alat-atau-artefak:
1. JSON: pilih array lewat试探 nama key -> AttributeError/'str'; baca `keys atas` dulu, pakai key kanon (`entri`, `figur`).
2. Nama berkas: id `FIG-01` vs berkas `fig-01.png` -> "sha 0/5"; `.lower()` dulu (cocok 5/5).
3. YAML bertingkat: regex `^\w+:` melewatkan kelanjutan indentasi -> "sidecar cacat 29/29" padahal 14 field lengkap; baca isi satu berkas utuh.
4. Notasi rentang: `SG-L0-01..05` -> regex id penuh mencetak 7; bentangkan rentang dulu (baru 68/68 valid).
5. Kolom vs global: hitung token `[H]` lintas seluruh CSV = 12; di KOLOM kanon-nya saja = 9 == klaim. Selisih definisi, bukan kontradiksi.
6. Path dengan spasi/glob `{svg,png}` terpotong regex -> "3 path TAK-ADA" semu; verifier ber-`root_map` pekerja lebih benar dari probe cepat.
Aturan: klaim cacat hilir hanya boleh tayang setelah sensor sendiri survive minimal satu bedah format; kalau alat pengawas yang cacat, nyatakan declared (kelas N-2 yang dibukukan B4-INDUK, kini dipraktikkan terhadap diri sendiri).

## 5. Cross-board semantic spread

Pertanyaan semantik tak terputus di satu papan menyebar lewat standar turunan: `kanvas_target` (125/176) vs `nominal_mm` render (128/166) lahir di PV-1007 (P-08), belum putus, lalu menjalar ke rak GM-L3 (dua kisi hidup bersamaan 166x22+176x4+128x2+125x1). Putusan controller wajib dinyatakan BERLAKU SEMUA PAPAN; pengawas menghitung spread-nya (distribusi lebar per rak) supaya re-render massal tidak terjadi dua kali. Field ganda yang disimpan terpisah = reversibel murah; puji dan tagih pola ini.

## 6. Arithmetic-label dan selisih-kecil audit

- Total byte label "N gambar" bisa diam-diam memasukkan manifest: 1.175.552 = 30 gambar (1.149.910) + manifest (25.642). Koheren-total, label-kurang-teliti: non-blokir declared, jangan vonis salah-klaim.
- Garis vs EOF: klaim "237 baris" vs probe 238 = pola EOF berulang; byte +5 B = state tulis-menengah declared - pin hilir SELALU sha16, bukan angka byte/garis.
- Sensus nomor inline kehilangan satu (79 dari 80, no.77 bolong) karena satu item tanpa nomor: hilir wajib pakai angka dari cache/parse resmi, bukan dari sensus-nomor dokumen.

## 7. Mekanika jejak yang terbukti

- Redeliver notifikasi kartu yang sudah kubevonis: guard `grep -c` komentar pengawas TERLEBIH DAHULU; kalau >=1, tanpa aksi (state boleh bergeser gave-up->done, cukup dicatat konsisten).
- Klaim alat pekerja tanpa log persisten: pengawas menjalankan scanner sendiri + menyimpan `.log` hasil (mis. `gm_l6b_scan_standar_pengawas.log`) - vonis menempel byte termasuk byte alat vonis.
- Pola self-describing-ledger (validasi-14 tersimpan TERSTRUKTUR dalam JSON register; verifier-generator terpisah tanpa impor data = C1) = bentuk tertinggi ledger audit-able; puji dan jadikan tagihan papan lain.
- Steer mid-run vs steer-sebelum-run: komentar controller yang diterima DI TENGAH run wajib dicek terserap via token konten (grep kata kunci butir steer); yang diterima SEBELUM promosi lebih murah - catat kronologinya sebagai observasi proses.
- Terminal menolak perintah panjang secara berulang ('expected string, got NoneType', rusak saat pengiriman, BUKAN kegagalan perintah): jalur sah = execute_code `subprocess.run(['hermes','kanban','comment', tid, teks])` dari berkas temp; verifikasi guard post-tayang. Pecah perintah gabungan panjang jadi pendek, dan jangan pakai ulang bentuk yang gagal 2x.
