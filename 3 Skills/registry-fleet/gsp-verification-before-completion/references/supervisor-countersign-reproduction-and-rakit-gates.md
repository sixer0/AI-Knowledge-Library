# Countersign Reproduksi Dua-Arah & Gerbang Rakit (misi RAFAI/PROMANUAL, 05-10)

Pola teruji dari satu giliran supervisi dua papan (20+ vonis/countersign, nol cacat artefak lolos, empat positif-palsu instrumen pengawas tertangkap sebelum vonis).

## 1. Countersign = reproduksi independen, bukan pembacaan laporan

Ketika memvonis kartu VERIFIER (G-JENUH, G-KUTIP, VERIF-ULANG), jangan cukup membaca laporannya. Metode yang terbukti:

1. **Tulis parser pengawas sendiri** untuk populasi yang sama (URL, tag, caption, marker) — JANGAN menyalin regex verifier.
2. **Bandingkan dua arah**: `milikku MINUS milikverifier` dan sebaliknya. Delta wajib terjelaskan penuh sebagai BEDA DEFINISI (mis. URL pola-brace instruksional dihitung utuh vs dinormalkan ke basis path; baris tabel katalog vs baris VONIS JENUH), bukan diputus sepihak.
3. **Jalankan instrumen verifier langsung** bila ada di workdir (`toc_vs_headings.py`, `run_twice.py`, diff `shasA/shasB`) — exit code alat = bukti, bukan narasi.
4. Aritmetika klaim dikompute ulang (88/88 pecahan persen; impas 2×0,10+4×0,50; 2.000/1M×2+500/1M×10).
5. Verdict NEEDS_REVIEW verifier DITERIMA apa adanya — pengawas dilarang "meloloskan" atas nama kecepatan; gerbang yang menahan rilis adalah gerbang yang bekerja benar.

Sinyal auditor berkualitas yang dicatat saat countersign: self-correction eksplisit di laporan (FAIL instrumen→dibatalkan), OBSERVASI non-blokir atas temuan sendiri, pemisahan peran (menemukan tapi tidak menyunting), dan klaim yang justru KONSERVATIF vs nyata (kartu sebut "5 skrip", disk 7).

## 2. Bug instrumen pengawas = positif-palsu; curigai matcher sebelum vonis cacat

Empat kejadian satu giliran, semua "0 cocok / tidak ada" ternyata bug pengawas sendiri:

| Alarm | Akar bug | Fix |
|---|---|---|
| "0/36 pola GR-22" | caption nyata `FIG-3.1. ...` diuji prefiks `'3.1.'` | prefiks lengkap `FIG-` |
| "TOC fm tidak ada" | regex batas blok berakhir `\n## ` padahal heading `# ` | batas blok longgar + jalankan instrumen pekerja |
| "nol rujukan [Bab-n]" | format nyata `[Bab 1]` dengan spasi | varian notasi += 1 |
| F-2 probe 403 | TEBAKAN URL host (dpr.go.id) — URL nyata di baris b13 | baca baris naskah dulu, baru probe |

Aturan: hasil "0 / tidak ditemukan" dari instrumen SENDIRI adalah dugaan terhadap instrumen dulu, bukan terhadap artefak. Koreksi diri pengawas ditulis TERPISAH di vonis (bukan disembunyikan), sesuai aturan user: koreksi = komentar jejak baru, suntingan komentar lama dilarang.

## 3. Gerbang rakit: struktur PASS ≠ semantik tertutup

Kartu RAKIT (DOCX+PDF) timeout dengan artefak utama SUDAH JADI dan gerbang 11/11 PASS (defect tautan 0/1362, LOF OOXML 36/36, caption manifest 36, font tertanam, halaman COM==PDF). Vonis SAH DITAHAN karena:

- **Daftar TAMBAL figur terbekukan** (fig-2.1 leader-line, fig-3.1 superlatif, fig-17.1 path-bocor) dan `grep 'tambal|cacat|known-defect' = 0` di seluruh workdir — rakit berjalan DI ATAS hutang semantik tanpa satu pun catatan penanganan. Gerbang struktural tidak pernah mengukur semantik figur (preseden vision QA GC2GF/DENDAM/VCDUA).
- Idempotensi build belum dibuktikan (belum ada dua-run diff sha) — standar seluruh jalur figur harus berlaku untuk rakit juga.
- **Prasyarat vonis SAH rakit: putusan controller TERCATAT** — rilis known-defect berlabel di kolofon (rev-2 menyusul) ATAU tambal-dulu-rakit-ulang. Pertanyaan ini ditulis di kartu sebagai bukan-wewenang-worker/pengawas.
- Catatan turun-temurun: parser TOC front matter (`toc_vs_headings.py`) perlu diperluas mengenal KELAS ARTEFAK BARU (5 berkas review) — setiap artefak yang naik ke rakit wajib punya pembanding mesin di daftar isi.

Generalisasi: sebelum vonis SAH kartu RAKIT/PROMOSI, pengawas grep workdir untuk setiap item daftar-tambang terbekukan; item yang tidak ditangani HARUS muncul sebagai label known-defect di artefak atau putusan controller — diam-diam = FAIL.

## 4. Retry timeout idempoten-berbahaya

Kartu suntingan/apply (EDIT, FIX-LINK, RAKIT) yang timeout dengan suntingan SUDAH mendarat sebagian:

- run-2 WAJIB resume dari state disk; **jangan apply ulang replace** (cek disk tiap target dulu — replace ganda merusak baris); jangan timpa arsip_pre bersih dengan arsip pasca-fix.
- Vonis pengawas dua-arah: URL/koreksi baru hidup TERBUKTI probe DAN bentuk lama hilang dari naskah (sisa lama sah hanya bila konteksnya teks riwayat, cek per kemunculan).
- Jejak run dispatcher terbaca dari workdir: nama berkas output run-4559 membuktikan kartu sudah retry sebelum timeout kedua — bukti anomali durasi untuk tiket traceroot, bukan asumsi.
- Kelengkapan run-2 dinilai vs daftar kerja yang ditempel catatan timeout (laporan, baris Riwayat suntingan, status per butir F-x) — dituruti-literal = sinyal rantai sehat.

## 5. Placeholder register-aware (kanal PROMANUAL)

- `{{KL:KL-R3-268|key}}` pola-pipa membuat parser memotong ID jadi fragmen (`L-R3-268`) — normalisasi: ambil segmen setelah `KL:` sampai `|`; fragmen = artefak parser, verifikasi hulu grep manual ke register beku menutupnya.
- Placeholder key ganda per baris (masuk|keluar, cache_write_5m|1h|hit) = disiplin lebih kuat dari angka telanjang: tiap angka tetap tertelusur terpisah. Spot-check 6 ID per bab ke register wajib sebelum vonis.
- Draf vonis wajib diuji KONTRADIKSI internal sebelum kirim ("78 rekor baru" vs rekor sebenarnya B15=133 — dibetulkan pra-kirim, bukan pasca).

## 6. Pengiriman vonis panjang (kanal WhatsApp/CLI)

- Teks vonis ber-apostrof merusak petik bash (`unexpected EOF`, kadang tampak "OK" palsu dari truncasi). Resep baku: `write_file` vonis ke berkas temp → `hermes kanban comment <id> "$(cat berkas)"` → **anti-duplikat: `kanban show | grep -c` SEBELUM kirim ulang** → append kontrak pakai `;` bukan `&&` (grep exit-1 memutus rantai, append hilang senyap).
- Scan glif vonis itu sendiri (U+2014/U+00B7 = 0) sebelum kirim; typo hitung (ketigabelas vs sebelas) dikoreksi di berkas, bukan di kanal.
