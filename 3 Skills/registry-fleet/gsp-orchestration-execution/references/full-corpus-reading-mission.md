# Full-Corpus Reading Mission (baca penuh folder proyek + resume pengetahuan)

Kelas misi: "Baca semua file folder X satu per satu, baris per baris, tanpa yang
terlewat - lalu buatkan resume pengetahuan" (preseden: misi baca korpus 1003 03-10,
misi pemahaman korpus 0925 299 berkas, EKASSAPU-0923 254 berkas). Beda dari lajur riset
saturasi ([`saturation-gate-sweep-lanes.md`](saturation-gate-sweep-lanes.md)): populasinya berkas di disk, bukan
klaim eksternal; vonis selesai = MANIFEST selisih-nol, bukan jenuh ber-angka.

## Prosedur (urutan terbukti 03-10)

1. **Inventaris dulu, delegasi kemudian** (satu giliran terminal): jumlah berkas,
   total byte, histogram ekstensi, ukuran teks (md/json/csv) per subfolder. Ini
   menentukan jumlah gelombang dan mana yang butuh parser.
2. **Controller baca sendiri berkas indeks** (bukan didelegasi): Baca_Dulu,
   Catatan Sesi, Catatan Perubahan, REGISTER, Laporan_Pemahaman terakhir,
   ringkasan iterasi kunci. Resume akhir harus bisa dipertanggungjawabkan oleh
   yang menyerahkannya.
3. **Gelombang kartu baca** ke `gsp-document-reader` (atau `gsp-document-analyst`),
   satu kartu per subtree seukuran <=~1 MB teks, output path unik per kartu
   (`work/wN_<slug>.md`). Dispatcher lokal boleh mengklaim >5 sekaligus; kap 5
   adalah norma gelombang promosi - JANGAN pasang edge semu demi kap (pelajaran
   02-09, tetap berlaku).
4. **Kontrak digest wajib di body kartu**, per berkas: path, ukuran/baris nyata,
   struktur seksi, SEMUA angka kunci verbatim (Rupiah/unit/tanggal/sha/pasal),
   keputusan, anomali, status keterbacaan. Penutup = MANIFEST lingkup vs terbaca
   (selisih nol; biner tanpa salinan .md = `BINER-MURNI-TIDAK-DIBACA` + catat
   ukuran/tanggal/sha dari ledger = status 'tercatat'). Anggaran habis =
   `STATUS: partial-handoff` + SISA_KERJA path persis -> kartu resume, bukan restart.
5. **Data besar (>=~200 KB json/csv)**: boleh parser semantik (schema, jumlah
   record, field kunci, agregat, contoh baris), bukan literal-read - catat putusan
   ini di kontrak ("parser = baca penuh secara semantik", D-02 misi baca korpus).
6. **Watcher digest**: loop polling berkas output via
   `terminal(background=true, notify_on_complete=true)`. DILARANG nohup/disown di
   foreground (ditolak runtime). Jangan poll papan buta tiap giliran.
7. **Verifikasi pra-klaim**: controller ukur ulang sendiri artefak keadaan-terakhir
   (sha256[:16] berkas rilis vs sha yang dikutip vonis/memo; `VONIS-AKHIR`,
   `MEMO-SERAH` di folder docs misi sebelumnya). Folder proyek beku sering BERHENTI
   di iterasi N sementara keadaan hidup ada di `workspace/gsp-hermes/workspace/docs/<tanggal>-<slug>/`
   - sensus artefak luar-folder harus jadi lingkup salah satu kartu (W7 pola misi baca korpus).

## Pitfall: ledger ALUR vs nama berkas di disk (sanitasi)

`Sidik_Berkas.csv` (ledger MD5 hasil `alur.py tutup`) menyimpan nama ASLI dengan
spasi dan karakter khusus (`2. [REN] PENDATAAN...xlsx`, `...(Public).pdf`), tetapi
berkas di disk tersanitasi (`2.__REN__PENDATAAN...xlsx`, `..._EN_Public_.pdf`;
kurung/parenthesis dilepas). Uji keberadaan naif `os.path.exists(ledger_path)`
memvonis sebagian besar berkas HILANG - FALSE ALARM (terukur 03-10: 242/282
"HILANG" padahal isi utuh). Resep audit benar:

- cocokkan dengan kunci ternormalisasi: `path.replace('_',' ').lower()` dua sisi;
- laporkan terpisah: SAMA-MD5 / BEDA-MD5 / RENAME-sanitasi / TAK-TERCOCCOKKAN;
- berkas ekstra di disk jelaskan per kategori (salinan `.md` extracted,
  `__pycache__/*.pyc` jejak run pasca-beku, `.DS_Store`, `Claude outputs/`);
- hasil sehat 03-10: 278 SAMA, 0 BEDA, 4 tersanitasi-nama, 21 ekstra terjelaskan.

Resep integritas folder beku: nol BEDA-MD5 = konten tidak bergeser sejak tutup
ALUR; jangan menuntut "rename balik" - itu merusak ledger.

## Pitfall: skrip python inline lewat heredoc bash

String dengan backslash (`p.replace('\','/')`) rusak lewat heredoc/arg quoting
(SyntaxError). Tulis skrip audit ke berkas via write_file (path native
`C:/Users/...`), lalu jalankan `python <path>` - sekaligus meninggalkan bukti
alat yang bisa dipakai ulang. Gunakan `os.sep`, bukan literal backslash.

## Format resume pengetahuan (kanal user)

Serahkan sebagai dokumen sesi: inti proyek, para pihak, dasar hukum, baseline
historis, riwayat iterasi per fase dengan angka kunci, keadaan anggaran/rantai
nilai, arsitektur keadaan akhir, keputusan terbuka (dengan nomor butir), risiko,
vonis pemahaman. Semua angka dari cetakan alat giliran ini (rule 9 SPK-002),
bukan dari ingatan laporan. Tunduk gerbang naturalisasi (U+2014/U+00B7 nol).
