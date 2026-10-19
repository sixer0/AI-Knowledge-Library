# Self-Audit of Deterministic Scoring/Verification Instruments

Preseden MWSKILL-0916 (16-09): controller menjalankan skrip SCORE sendiri; vonis run-1
ganjil (G4 1/6 padahal juri TRAP 6/6). Audit membuktikan PARSER controller yang salah
tafsir klausul spesifikasi, bukan kandidatnya. Run-1 diarsipkan `score_run1_INVALID.json`,
run-2 taat-spec jadi vonis resmi. Lessons tergeneralisasi:

## 1. Audit instrumen sebelum memublikasikan vonisnya
- Untuk tiap gerbang FAIL yang ganjil terhadap sinyal lain (juri 6/6 vs parser 1/6),
  dump interpretasi nyata parser per kasus vs teks klausul spec; bandingkan klausal per
  klausal, bukan aggregate.
- Kalau parser menyimpang dari spec: vonis lama INVALID total, jangan dilunakkan per
  baris. Arsipkan utuh dengan suffix `_INVALID`, jalankan run baru, catat kedua run di
  Decision Log. Rubrik/ambang tidak digeser - hanya parser yang dibetulkan.

## 2. Sidik jari: kunci algoritma sebelum klaim cocok
Pekerji melaporkan "sha16" yang ternyata awalan SHA-1, bukan SHA-256 (konvensi fleet).
Saat menguji klaim hash: hitung ULANG sha1[:16] dan sha256[:16]; kalau cocok ke salah
satu, konten identik dan itu salah LABEL algoritma, bukan cacat data. Footer artefak
wajib menyebut algoritma kanonik (sha256).

## 3. Baca skema dari berkas, bukan dari ingatan
Cek pertama memakai field `status_bukti` padahal skema register memakai `kelas_asal`
-> hasil "semua_TERUKUR: False" palsu. Sebelum menulis skrip uji: cetak
`sorted(keys(row0))` dari baris pertama target. False dari asumsi nama field = artefak
alat, bukan temuan data.

## 4. Bukti urutan konsumsi (mtime ordering)
Klaim "vonis sudah memakai semua input" dibuktikan dengan timestamp: input terakhir
(grade juri final) HARUS lebih muda dari artefak vonis (`score.json` 21:04 > grades
20:57). Kalau input menyusul setelah vonis, vonis wajib diulang.

## 5. Watchdog kanban CLI: urutan flag
`hermes kanban --board default list --json` valid; `--json list` membuat parse gagal
dan watchdog berputar tanpa vonis (silent stall). Symptom: watchdog running terus,
output kosong, padahal kartu sudah terminal. Kalau watchdog tidak melapor sama sekali,
curigai dulu perintah dalamnya, bukan papan.

## 6. Vonis simulasi FAIL -> audit cakupan hulu dulu
Panel buta gagal ambang (G1/G3/G5) padahal juri sepakat penuh (arbiter 0) dan penolakan
jujur berskor baik: indikator kuat cacat di HULU (ekstraksi register melewatkan butir
yang ditagih bank soal), bukan kandidat/kunci. Resep diagnosis:
- join butir kunci soal-gagal vs register (kata kunci nol-cocok = kandidat celah);
- uji tandingan pymupdf terhadap dokumen asli di halaman klaim: angka ADA di sumber +
  TIDAK ADA di register = cacat rakit;
- hasilkan daftar halaman celah deterministik (join skor<3 x key), kartu tambal paralel,
  merge, reverif, lalu simulasi ULANG dari lapis kandidat - lembar jawaban lama tidak
  valid terhadap paket baru.
