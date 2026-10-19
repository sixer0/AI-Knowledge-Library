# Vision carry-forward + celah "instrumen melapor tanpa memvonis" (pengawas RAFIFUNITY/GAYA-AHLI, 06-10)

Lima teknik/temuan dari gelombang countersign RAFIFUNITY-1004 (fix-batch, QC figur gel-2) dan GAYA-AHLI-1005 (S7) yang terverifikasi dipakai silang dan layak jadi resep tetap pengawas.

## 1. Byte-identity carry-forward untuk re-QC populasi vision (preseden QC-FIGUR-GEL2-ULANG)

Saat vision QA ulang populasi besar setelah gelombang tambal (58 figur, hanya sebagian berubah):
- JANGAN bayar mata-vision untuk semua. Ukur dulu register hash dua siklus (A sebelum rerun, B sesudah, C rerun-ulang): `diff A->B di luar subset yang seharusnya berubah = NONE` + batas gel-1/bawaan = mismatch 0.
- Byte yang TIDAK BERUBAH mewarisi vonis vision lama secara sah; yang berubah SEMUANYA divisus ulang. Vonis terekam sebagai "PASS 55, MISMATCH 3" dengan syarat pembuktian tercetak di laporan.
- Doktrin dua-sumbu yang dipakai bersamaan: **hash membuktikan identitas, vision membuktikan semantik**. Hash stabil + margin hijau TETAP bukan bukti kebenaran visual (preseden fig_12-5: gerbang deterministik lulus, penanda ④ salah-pasang objek).
- Pra-flight wajib: prasyarat promosi diukur RUN ini (ukuran sidecar, koordinat marker, register hash == pin countersign hulu - rantai warisan tersambung byte-per-byte, bukan dikutip dari laporan).

## 2. Protokol countersign "buta vonis" untuk uji tandingan vision

Sebelum membaca vonis pekerja atas figur target, pengawas membuka gambar sendiri dengan pertanyaan netral ("apa yang salah di sini?", bukan "benarkah klaim X?"). Cocokkan temuan independen vs butir pemblokir pekerja setelahnya. Preseden 8-3: vision pengawas mengonfirmasi PULIHNYA cacat lama (grid 5x5 muat penuh) DANcacat residu yang persis sama butarnya dengan laporan (baris Mask di bawah border panel, callout menembus label) - vonis MISMATCH terdukung mata kedua tanpa echoes bias.

## 3. Kelas cacat BARU: glyph-fallback render (di luar jangkauan gerbang geometri)

fig_30-2 pasca-rerun: glif `$` dan spasi HILANG dari teks dalam-gambar ("US111in, US15 store fee...") padahal judul prosa benar ("US$111"). Kelas akar: font/glyph fallback matplotlib, BUKAN geometri - margin_check/uji teks-vs-teks tidak melihat kehilangan karakter per-glyph. Implikasi gerbang: sensor teks dalam-gambar harus membandingkan STRING EKSPETASI vs hasil OCR/caption-sidecar per-token, bukan hanya posisi. Vision QA tetap penangkap terakhir untuk kelas ini.

## 4. Detektor "instrumen melapor tanpa memvonis" (temuan CRLF ch05)

Sensor FIX-BATCH-2 mencetak `CR=430 -> OK`: ia MELAPORKAN jumlah CR tapi tidak menjadikannya syarat gagal, padahal konvensi fleet vonis-per-bab = "CR nol" dan `_pre` berkas CR=0. Akar provabel: tulis ulang berkas mode teks Windows oleh skrip suntingan (newline default \r\n) - konten baris utuh, format regresi + noise diff git + risiko hitung scanner hilir. Aturan turun-temurun: **setiap metrik yang dicetak instrumen harus punya ambang vonis, atau jangan dicetak** (kelas pelajaran FIXA "verify tertinggal konten": instrumen harus memvonis apa yang ia laporkan). Resep pengawas: probe `b.count(b'\r')` vs `b.count(b'\r\n')` pada byte mentah untuk memastikan CRLF penuh; cek `_pre`/backup untuk menentukan warisan vs mutasi suntingan. Tambahan sekelas: CJK tersesat di laporan kanal-adjacent ("Crop决定性" 3x) - CHECK CJK=0 papan lain (s7_check C8) terbukti menangkap kelas yang scanner papan ini lewatkan; tiket lintas papan, bukan blok vonis isi.

## 5. Rantai pin dua-siklus untuk kartu suntingan batch (teknik countersign FIX-BATCH)

Bukti bahwa suntingan batch lahir dari state yang sudah divonis (bukan salinan lepas): workdir kartu menyimpan `_pre_<berkas>.md` = snapshot pra-sunting. Pengawas menghitung sha256[:16] berkas `_pre` dan mencocokkan ke PIN VONIS PENGAWAS LAMA atas berkas yang sama (preseden: ch10 `_pre` == 569d7185 vonis CH10; ch09 == 2f9a2814; ch12 == 6f33f77c). Tiga mata rantai tertutup: worker pin -> pengawas pin -> `_pre` == pin pengawas -> pin pasca-sunting cocok klaim. Urutan waktu ikut diuji: BEFORE/AFTER-VERIFY per berkas, sensor final TERAKHIR (verify 16:27 -> sensor 16:30, berkas statis setelahnya). Pin SHA1 vs SHA256 wajib dilabel algoritma (disiplin NIT-2 fleet).

## 6. FAIL yang diserahkan = jujur, bukan cacat (pola warisan urutan paralel)

AFTER-VERIFY ch12 FAIL(2) saat kartu mengklaim complete: bukan manipulasi ambang oleh pekerja (yang akan jadi FAIL vonis), melainkan dua FAIL DIBUKUKAN + diserahkan ke pemegang objek berikutnya (kartu figur memegang caption-vs-sidecar fig_12-5 + ukuran fig_12-4 vs register hardcoded era pra-rerun). Akar: naskah disunting 16:27, figur direrun 16:00, register verifikasi beku era berbeda - gerbang dua-arah justru bekerja. Vonis pengawas: SAH-as-partial dengan ANTRIAN terukur ke kartu hilang; register verifikasi yang hardcoded ukuran artefak wajib dibaca sebagai snapshot era, dan FAIL-nya memicu refresh register, bukan tambal naskah.
