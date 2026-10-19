# Verifikasi Aktivasi Knowledge Lintas Profil (preseden VSSKB-0923, 23-09)

Kelas tugas: knowledge/korpus didaftarkan permanen lalu dirutekan ke memori banyak
profil; pengguna menuntut bukti bahwa rute itu AKTIF dan TERPAKAI oleh agen-agen
target, bukan hanya tertulis di berkas memori.

## Resep 1: pemetaan target dari sumber otoritatif, bukan asumsi
- Bila user menyempitkan cakupan ke "profil yang punya akun X" (mis. akun RBAC WebUI):
  tarik daftar dari API/registry resmi penyelenggara (mis. endpoint rbac HQ dengan
  token internal dari .env — nilai rahasia SELALU [REDACTED] di laporan/jejak), lalu
  petakan akun -> profil Hermes via config profil. Jangan mengarang daftar dari ingatan.
- Ukur per berkas dengan grep token rute (mis. `INDEX #<slug>`): angka "N/N" harus dari
  cetakan alat giliran itu. Rollout superset (semua profil) tidak perlu dikecilkan bila
  user tidak memerintahkan pencabutan — cukup laporkan irisan target ⊆ terpasang.
- Cek jalur automasi warisan: bila signup profil mengklon dari root default, rute di
  root otomatis menjangkau akun masa depan — catat sebagai properti, bukan kebetulan.

## Resep 2: sampling acak beku untuk verifikasi
- User boleh membatasi: "verifikasi ke random 3 dari 8". Bekukan undian SEBELUM eksekusi:
  `python random.Random(seed=int(time.time())).sample(pool, k)` dan catat seed + waktu UTC +
  pool + hasil di Decision Log kontrak. Ini membuat undian dapat diulang/diaudit dan
  menutup celuh "pilih yang lulus saja" (goalpost-moving).
- Vonis hanya sah atas 3 terpilih; jangan mengutip "fleet-wide 0/100%" dari sampel
  (D-TA-10 analog).

## Resep 3: probe tanya-jawab lintas profil (menguji rute TERPAKAI, bukan ada)
- Dispatch `hermes -p <profil> -z "<prompt>"` dengan env-strip `HERMES_KANBAN_*` agar anak
  tidak mewarisi identitas kartu verifier (pitfall warisan S18b) + kalimat wajib di prompt:
  "JAWAB HANYA dari korpus/memory yang tersedia; sebutkan jalur rujukannya (berkas/baris).
  JANGAN panggil tool kanban."
- Simpan transkrip MENTAH per agen (`verif/...probe-N-<profil>.md` + `.rc`).
- Skor dengan skorer deterministik tiga syarat, bukan kesan:
  (a) menunjuk jalur nyata (token rute memori / berkas rak + baris),
  (b) menyebut angka ground truth persis,
  (c) menyebut penanda batas/known-defect bila butir berstatus defect.
  Cetak `CHECK n: LULUS|FAIL` + `VERDICT:`. Controller UKUR ULANG transkrip dengan grep
  independen sebelum menerima vonis verifier (artefak menang atas summary).
- Gagal-ronde pertama yang berakar lapis sumber (marker hanya di hilir, agen membaca hulu)
  = temuan traceroot SPK-002 butir 7: tambal GERANG/lapis yang dibaca agen, beri marker di
  SEMUA lapis hidup, baru re-probe. Vonis FAIL atas agen karena rak belum ditambal = cacat
  misi, bukan cacat agen.

## Resep 4: sapuan propagasi defect = grep pola ANGKA, bukan daftar berkas
Setelah menandai known-defect pada berkas-berkas yang ditemukan, jalankan sapuan penuh:
`grep -rln -E "<pola angka defect>" --include='*.md' <korpus>` -> setiap berkas yang memuat
angka WAJIB ikut membawa token penanda, atau dibiaran SAH dengan alasan tertulis (mis.
rekaman historis CHANGELOG bukan lapis pakai). Laporan BOCOR=0 dihitung dari sapuan ini.
Bukti kuat resep ini: probe-3 menemukan sendiri berkas ambang-induk yang lolos dari daftar
fix pertama; tanpa sapuan pola angka, dokumen serah-terima tetap membawa klaim mentah.
Tambal lanjutan pakai skrip hanya-tambah dengan penjaga subsequence vs cadangan
(`all(c in iter(new) for c in old)`), cadangan penuh sebelum sunting, uji ulang pasca-apply.

## Resep 5: gerbang rilis pesan siap-pakai ke kanal
- Urutan keras: vonis PASS 3/3 dulu, baru kirim pernyataan kesiapan. "Terkirim-bukti" =
  `hermes send -t <platform:chat_id> -f naskah.md` mencetak `sent` rc 0 (jalur gateway,
  tanpa LLM). Tes gerbang dulu: satu pesan pendek bertanda `TES GERBANG <ID-MISI>`, bukti
  ack di kartu, baru naskah final.
- Cron one-shot hanya perlu bila kirim harus MENUNGGU gerbang; bila gerbang sudah hijau saat
  kirim, `hermes send` langsung lebih benar (cron hanya duplikasi) — catat deviasi di
  Decision Log.
- Scanner naturalisasi untuk notifikasi pendek WAJIB `--channel notif` (K4 formal-netral):
  kanal default `doc` memberlakukan metrik prosa panjang (C-6 rata-rata >= 25 kata/kalimat,
  C-8b, agregasi D-TA-09) yang FAIL pada pesan ringkas yang justru sudah patuh. Kanal benar
  membuat C-6/C-7/C-8b/C-10/D-TA-09 jadi N/A; A1/A2 (U+2014, U+00B7) tetap diuji — cek
  mandiri `grep -c $'\u2014\|\u00b7'` = 0.
- Isi naskah kesiapan wajib memuat: status verifikasi + metode sampling, cara pakai di sesi
  baru (pemicu topik + jalur rute), dan BATAS diketahui (defect, cakupan, gap rak).

## Pitfall alat yang muncul di jalur ini
- `lad_card.py` adalah CLI flag-only: TANPA subcommand `create`, tanpa `--priority/--json`;
  argumen bentuk: `--title --assignee --parents --body-file --est --shape` (shape:
  satu|rantai-N|paralel-Kx). Pemanggilan lewat python butuh path native
  `C:/Users/...` (MSYS `/c/...` tidak diterjemahkan -> can't open file).
- Kartu controller `--interaktif` tetap bisa diklaim gateway (varian pitfall 09-09): gejala
  `cannot complete ... live worker claim (run NNNN)` -> `reclaim` lalu `complete --force`
  dengan bukti; cek mtime artefak untuk memastikan nol suntingan kembar.
- Watchdog lama yang kedaluwarsa mengirim notifikasi "belum selesai" dengan parser grep kolom
  salah — jangan laporkan apa pun darinya; status selalu dari ukur segar `show --json`.
