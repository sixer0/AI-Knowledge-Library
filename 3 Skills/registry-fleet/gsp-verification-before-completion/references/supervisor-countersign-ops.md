# Supervisor countersign ops — mengukur klaim dan memeriksa laporan secara langsung

Dipakai sepanjang enam papan (06-10 s.d. 06-11/12): PROMANUAL, GAYA-AHLI, buku Unity, EKASLAP, PROMANUAL-V2, VISUAL-1005. Vonis `SAH / NEEDS_REVIEW / FAIL` hanya sah dari artefak yang dibuka dan diukur pada giliran itu; `completed` dari judul/notifikasi bukan bukti.

## Aturan inti

1. **Angka = cetakan alat pada giliran ini.** Setiap field beban-rilis diuji ulang dengan instrumen sendiri (sha16, byte, hitungan parser, probe hidup). Dilarang mengutip angka dari result kartu, laporan pihak lain, atau ingatan. Bila klaim pekerja cocok digit-per-digit dengan cetakan-ku: vonis; bila beda: rekonsiliasi DEFINISI dulu (mis. anchor 722 = 463 TOC + 259 badan; bookmark 487 nama-kustom vs 511 pasca-regenerasi Word) sebelum menyebut cacat.
2. **Guard redeliver sebelum pasang jejak.** Notifikasi kanban bisa datang dua kali untuk kartu yang sudah divonis:
   `hermes kanban show <id> | grep -c "Countersign pengawas"` — bila >=1 dan isi result identik butir-per-butir dengan yang kuukur: TANPA komentar baru, laporkan sebagai redeliver-tanpa-aksi.
3. **Koreksi diri lewat komentar terpisah, dan sensor ke TEKS TAYANG.** Mengoreksi draf lokal bukan koreksi: grep komentar yang sudah tayang untuk membuktikan frasa cacat benar-benar hilang. Berlaku juga untuk angka peta: sensus final `kanban list | awk ...` kupetik SEBELUM vonis dikirim (bukan ditulis dari ingatan lalu dikoreksi setelah tayang).
4. **Sensor-dulu-vonis-kemudian.** Bila probe-ku membantah artefak, curigai probe. Katalog positif-palsu yang benar-benar terjadi dan cara benernya:
   - regex path terpotong di SPASI (nama berkas berisi spasi, mis. "James F. Kurose ... .pdf") -> potong pada `|`, baris, backtick; jangan spasi
   - backtick penutup menempel path -> `.strip('`')` sebelum uji `os.path.exists`
   - regex XML sensitif urutan atribut (`w:anchor=` bisa muncul sebelum/sesudah atribut lain) -> ambil seluruh tag hyperlink lalu cari atribut per elemen
   - filter substring "URL terpotong" salah tuduh -> DOI sah memang berkurung: `10.1002/(SICI)...CO;2-3`; uji BENTUK UTUH
   - scanner dijalankan `--text <path>` mengukur STRING path, bukan isi berkas (kelas F-25-1, membatalkan klaim "PASS" sebuah vonis-lepas) -> selalu argumen posisi berkas
   - byte disk mentah != konten LF (CRLF): sha cocok-konten-LF + selisih byte == jumlah CR = konsisten; catat dua konvensi
   - flag `--out` bisa berarti DIREKTORI: probe awal "semua berkas BEDA" ternyata salah baca struktur; daftar isi dulu, bandingkan file-per-file
5. **Pin era dan rantai byte.** "Vonis menempel byte." Pin sah = result kartu TERAKHIR atas artefak hidup; komentar lama boleh men-pin era lain (jejak dua/tiga-era sah, bukan cacat) tetapi hilir WAJIB jalankan ulang instrumen atas pin hidup sebelum mewarisi vonis (kelas "pin-komentar vs artefak-hidup": SERAH run-1, outline VISUAL 7a9866ff->84415982, typo digit pin dibetulkan via postflight parent). Ledger era dicatat, artefak era dilumpuhkan `*.stale*`/`_arsip/`, tidak dihapus.
6. **Dua arah untuk remedi:** token target == jumlah diharapkan DAN token lama == 0, di SEMUA lapis terbit (teks-docx `w:t`, teks-PDF, companion). Contoh baku: `'(Edition 3)'=1 / '(Edition 2)'=0` di docx+PDF+companion; sisa "(Edition 2)" di lapis-audit declared sah, bukan regresi.
7. **Gerbang OPC DOCX keras** (preseden 54C; zipfile/python-docx toleran, Word menolak): keunikan Id rels (`collections.Counter` pada `Id="rId\d+"`), tiap `Override PartName` menunjuk part yang ada di namelist, dan probe buka nyata (Word COM `pages=N`). Build idempoten: dua build `cmp` byte-identik.
8. **Pasangan cetak PDF:** teks identik per-halaman (delta halaman 0) SEMENTARA byte beda (serialisasi/timestamp) = pasangan sah; ukuran byte sama + char sama + predikat "delta-metadata-saja" koheren = klaim terverifikasi.
9. **Laporkan instrumen yang mati.** Sensor gagal (AttributeError properti COM, salah interpreter uv) dibuka di jejak + ditutup uji lebih kuat; dilarang sensor-palsu atau diam-diam tambal allow-list.
10. **Batas peran pengawas:** tidak membuat/membuka ulang kartu, tidak dispatch, tidak promosi, tidak menyentuh target promosi. Rekomendasi = tagihan di komentar/kontrak; putusan tetap milik controller/user.

## Resep sensor cepat (zip/PDF)

```python
# docx: census anchor urutan-bebas
hl = re.findall(r'<w:hyperlink\b[^>]*/>|<w:hyperlink\b[^>]*>', doc)
anch = [re.search(r'w:anchor="([^"]+)"', h).group(1) for h in hl if 'w:anchor=' in h]
# rel eksternal + terpotong-kurung
uri = re.findall(r'Target="(https?://[^"]+)" TargetMode="External"', rels)
trunc = [u for u in uri if re.search(r'\([^)]*$', u)]  # kurung tak tertutup
# PDF: GoTo di luar wilayah TOC (deteksi anchor-prosa-polos kelas F-58B-1)
for pg in d:
    for lk in pg.get_links():
        if lk.get('kind') == pymupdf.LINK_GOTO and not (3 <= pg.number <= 13): nontoc += 1
```

## Redaksi laporan vonis

Struktur komentar: status eksekusi -> UKUR mandiriku (angka) -> cokok vs klaim -> temuan/ anomali (dengan dasar) -> tagihan hilir bernama -> peta dari sensus final. Glif U+2014/U+00B7 nol pada teks tayang; kutipan verbatim cacat (mis. em-dash di artefak yang kudaftarkan) boleh di kanal internal dan wajib dibukukan eksplisit agar tak tampak misterius.