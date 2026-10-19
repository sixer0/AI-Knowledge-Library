# PDF / cetak-rilis chain verification (preseden RAFIFUNITY Ed3, 06-11/06-12)

Lapisan ukur di atas `document-artifact-verification.md` (DOCX/XML). Semua pola di bawah
terbukti dipakai nyata menutup defect kelas yang lolos gerbang DOCX.

## Gerbang pasangan cetak (screen + print)
- Pasangan rilis Ed-kelas: byte BEDA (delta metadata ±3 B), teks IDENTIK per halaman.
  Uji dua-sumbu: `cmp` byte + loop `page[i].get_text()` PyMuPDF delta-halaman. Satu sumbu
  saja menipu: byte-identik = salinan menipu; teks-identik tapi beda jumlah hal = regresi.
- Yardstick halaman lintas-cetakan: bandingkan `page_count` + ComputeStatistics Word COM
  dengan angka cetakan era sebelumnya; klaim "klausul/sisipan tidak menggeser pagination"
  wajib dari hitung alat, bukan asumsi.
- Proksi halaman (kata/hal) boleh dilaporkan HANYA dua-dasar berangka + vonis pengikat
  milik halaman tercetak alat. Satu dasar proksi = klaim selundupan.

## Gerbang URI/anchor PDF
- `uri terpotong = [u for u in uri if re.search(r'\([^)]*$', u)]` pada semua LINK_URI.
  Hati-hati positif-palsu: DOI sah MEMANG berisi kurung seimbang
  (`10.1002/(SICI)1520-6378(199908)…;2-3`) - filter substring naif menuduh yang utuh;
  uji bentuk lengkap per-butir sebelum menuduh cacat (dua sensor pengawas salah arah di sini).
- Rekonsiliasi anchor: total hyperlink-anchor = TOC + non-TOC (mis. 722 = 463 + 259);
  cocokkan tiga jalur (docx rels, PDF GOTO per wilayah halaman, laporan builder).
  GoTo non-TOC PDF = 0 padahal DOCX anchor 259 = Word regenerasi TOC membuang bookmark
  kustom di paragraf sumber TOC (korelasi 487/487, round-trip simpan permanen) - akar
  known-defect terdiagnosis, bukan regresi cetak.
- Regex atribut XML WAJIB urutan-bebas: `<w:hyperlink\b[^>]*>` lalu cari `w:anchor="…"`
  di dalam elemen. Regex tunggal dengan urutan tetap mencetak selisih palsu (496 vs 722).

## Klausul/register harus TERBIT di artefak cetak
Register known-defect yang "sudah mendarat di naskah" belum tentu terbit: probe teks PDF
per-halaman (`'frasa kunci' in page.get_text()`, catat nomor halaman). Bila artefak cetak
hidup lebih tua dari suntingan naskah (mtime/sha era-lama), rilis BELUM menutup - tagih
re-cetak dari pin baru, lalu verifikasi klausul di PDF sebagai gerbang tiga-arah
(klausul-di-PDF + label-edisi dua-arah + ratifikasi pemilik).

## Konten-kekal lintas-cetak lewat aritmetika delta
Total karakter teks PDF baru − lama harus == delta paragraf bernama yang declared
(+766 B untuk satu klausul). Delta tak terjelaskan = konten bergeser senyap.

## Retrofit 'sumber utuh' terbukti dua-arah
Klaim retrofit pada salinan: pin SUMBER kuprobe di SEMUA lokasinya (sha identik antar-copy),
dan salinan kerja sha-nya BERBEDA dari sumber. Satu arah saja (hanya salinan ada) tidak
membuktikan sumber tak tersentuh.

## Disiplin countersign pengawas (pola lintas papan)
- Redeliver notifikasi = guard `grep -c "Countersign pengawas"` pada `kanban show` SEBELUM
  menulis vonis; sudah ada = tanpa aksi.
- Instrumen beku pihak-kerja dijalan-ulang oleh pengawas atas objek HIDUP (jangan warisi
  cetakan era-lama; pin dua-era declared). Determinisme terkuat = lintas-waktu: hasil
  proses pengawas hari ini byte-identik dengan aset beku pekerja.
- Klaim hasil hanya dari cetakan yang sudah dipetik SEBELUM tayang (koreksi terjadi di
  draf, bukan di komentar-koreksi); koreksi jejak disensor ke TEKS TAYANG.
- Sensus manifest JSON pakai kolom kanon (`path`/`sha256`); kolom opsional per-jenis
  entri (`png`/`sha256_png`) mencetak positif-palsu 'hilang'.
- Sensus 'selesai senyap' vs 'belum terkartu': grep list judul sebelum menyimpulkan
  penutupan; peta berubah antar-sensus dikoreksi via komentar terpisah ber-timestamp.
- Vonis dua-juri menempel byte objek saat vonis: suntingan bernama pasca-vonis (walau
  ber-instrumen-PASS) memindahkan byte - vonis-lepas wajib atas pin baru via reshoot sempit
  zona tersentuh ATAU putusan tercatat eksplisit; dilarang warisi vonis era-lama diam-diam.
