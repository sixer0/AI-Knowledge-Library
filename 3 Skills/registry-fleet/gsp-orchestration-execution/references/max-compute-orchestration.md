# Resep gelombang MAKS-KOMPUTASI (kebijakan user 07-10; preseden misi editorial 07-10)

Trigger: user meminta "maksimum compute / utilisasi maksimal / full power" pada misi multi-agen,
atau steering lintas sesi "Gunakan Komputasi Maksimal pada Inference Server" (arsip verbatim:
`memory/refs/gsp-master01/2026_10_07_maks_komputasi.md`). Bentuknya = paralelisme selebar kap +
ukur dulu, jangan asumsi; gerbang mutu tidak pernah ditukar kecepatan.

## 1. Ukur sebelum memutuskan (semua angka masuk Decision Log)
- GPU: `nvidia-smi --query-gpu=...`; papan: `hermes kanban list --json` (running global vs per tenant);
  endpoint lokal: probe `/v1/models`, `ollama ps`.
- Inference server fleet (provider GSP-AI, mis. `worker-fast @ http://<host-inferensi>:11400/v1`):
  uji beban paralel nyata dengan `concurrent.futures.ThreadPoolExecutor` (tangga 8 -> 24 request,
  catat ok/n, latensi rata, wall). Preseden 07-10: 24/24 sukses, lat 1,0 s -> server BUKAN leher
  botol; yang membatasi adalah dispatcher papan.
- KUNCI API: baca dari `profiles/<p>/config.yaml` baris `api_key:` DI DALAM proses Python.
  Keluaran terminal TER-REDAKSI oleh sistem: nilai 13-kararakter hasil grep/sed adalah artefak
  redaksi (401 Unauthorized), kunci asli hanya terbaca saat file dibaca in-process. Jangan pernah
  menampilkan kunci.

## 2. Batch-create DAG via skrip generator (norma N1 + fast-lane)
- Satu skrip Python per misi (`gen_lanes.py`) yang merender body dari templat + memanggil
  `lad_card.py --parents id1,id2,...`; seluruh DAG fase berikutnya lahir sekaligus, promosi
  digerbangi edge hulu-data nyata. Preseden: 69 kartu, 5 lajur, 33 worker serentak.
- PITFALL generator (terbakar nyata 07-10):
  (a) `--parents` harus LIST id; string di-iterasi per karakter -> `kanban: unknown parent
      task(s): f, i, r, s, t`.
  (b) Templat body = string biasa dengan `{PLACEHOLDER}` + `.format()`; JANGAN f-string pada
      konstanta modul yang merujuk placeholder (NameError saat import).
  (c) Unpack tuple kartu: `create(*card)` bukan indeks manual per kolom.
- Kartu yang lahir tanpa edge hulu (kekeliruan generator, mis. FG3b tanpa parent FG3a): mitigasi
  wajib di body = "bila input belum ada, `block kind=dependency` jujur" — dan controller memantau;
  vonis jalan buta = kartu fix dengan input lengkap.

## 3. Kap dispatcher: ukur, jangan hafal
- `kanban.max_in_progress: 20` (host+profil) TERNYATA tidak menegakkan plafon pada jalur dispatcher
  07-10: 33 kartu running global serentak. Norma: angka config = advisory; yang mengikat = hasil
  ukur papan tiap gelombang. Praktik aman: tahan pembuatan kartu baru sementara running global > 24,
  laporkan puncak running terukur di kontrak (syarat audit N1).

## 4. Isolasi angka lintas lajur
- Satu kartu "pencipta angka" per domain data (mis. K1-D5) yang menulis `agregat-resmi.json`;
  semua kartu lain HANYA mengambil dari sana (satu-angka-satu-nilai Aturan Emas 7 Panduan Mutu /
  register angka induk SPK-002). Bila lajur lain mengutip angka yang sama, pasang edge data
  hulu->hilir (RAKIT D3 parent K1-D5), bukan salin nilai.

## 5. Ekstraksi PDF (pitfall mingw)
- `pdftotext` bisa menghasilkan 0 kata padahal lapisan teks ADA (verifikasi dengan pypdf
  `len(reader.pages)` + `extract_text()` per halaman) -> fallback wajib pypdf via
  `uv run --with pypdf`, jangan vonis "PDF tanpa teks / butuh OCR" dari pdftotext saja.
- Argumen output program native (pdftotext/curl/git) WAJIB path native `C:/Users/...`;
  `/c/Users/...` gagal dengan I/O Error (perluasan pitfall curl yang sudah tercatat).
- Berkas hasil ekstrak bisa terdeteksi "binary" oleh read_file (mis. misdetect HPGL) ->
  normalisasi encoding via Python (buang NUL/UTF-16) sebelum dibaca.

## 6. Gerbang banding "data hasil kerja sebelumnya" (steering user 07-10)
Bila user mengarahkan memakai hasil misi lama dan membandingkan dengan folder proyek:
1. Hash banding artefak: `certutil -hashfile <f> SHA256` vs pin rilis misi sebelumnya
   (sha256[:16] dari SERAH-L3/kontrak lama). SAMA = byte-identik, sumber sah.
2. Beda hash -> uji kesetiaan ISI, bukan hanya byte: sampel kalimat prosa acak (seed tercatat,
   mis. 1007) dari md sumber vs ekstrak PDF proyek; cocok-persis prefix 70 karakter setelah
   normalisasi NFKC/whitespace. Putusan tipikal: md misi lama = sumber primer (lebih baru/bersih),
   PDF proyek = pembanding layout.
3. Tulis semuanya di Decision Log dengan angka; jangan ubah kartu tanpa bukti.

## 7. Yang tidak pernah dikorbankan demi kecepatan
Verifier akun berbeda dari penulis; partisi berkas satu-kartu-satu-pemilik; SPK-002 field
beban-rilis; satu instance Word COM aktif pada satu waktu (ekspor antar lajur dijajarkan
controller); penutupan sah tetap `STATUS: complete|partial-handoff|needs-review` (aturan 15).
