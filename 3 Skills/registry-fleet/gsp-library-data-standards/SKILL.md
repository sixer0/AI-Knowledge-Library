---
name: gsp-library-data-standards
description: "Use when creating/proposing library (vault) objects, or defining how GSP knowledge is structured — object format, type taxonomy, provenance rules, status lifecycle."
version: 1.0.4
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
platforms: [macos, linux, windows]
metadata:
  gsp:
    category: library
    tags: [gsp, library, vault, wiki, knowledge, provenance, standards, proposal]
---

# GSP Library Data Standards

Standar data substrat pengetahuan GSP (Information Library): **bagaimana objek
vault ditulis, diklasifikasikan, dan dibuktikan** sebelum layak naik ke wiki/IL.
Dipakai oleh **siapa pun yang mengusulkan** objek (agen, analis, librarian).
Librarian memakai standar ini saat menilai dan meng-attest.

> Prinsip yang tidak dapat ditawar (bersumber dari arsitektur Information Library):
> 1. **Vault adalah sumber kebenaran.** Basis data (wiki/IL) selalu dapat dibangun ulang dari vault.
> 2. **Isolasi adalah berkas, bukan klausa WHERE.** Satu berkas per objek, per perkara.
> 3. **Angka tanpa halaman diperlakukan sebagai tidak ada.** Klaim tanpa provenans bukan fakta.
> 4. **Verifikasi bukan oleh penulisnya sendiri.** Yang meng-attest bukan yang menulis.
> 5. **Skema diamati, tidak dideklarasikan.** Taksonomi tipe boleh tumbuh dari isi, bukan daftar mati.

## Pipeline 3 tingkat

```
RAW (shared workspace)  ──►  VAULT (workspace/vault/)  ──gateway librarian──►  WIKI / IL (~/.hermes/wiki)
  data mentah,              objek usulan terstruktur         hanya yang lolos      entri terbit
  siapa pun boleh menilai   siapa pun boleh MENGUSULKAN       attest + persetujuan  (dimirror ke DB)
```

## Lokasi

- **Vault:** `<SHARED_WORKSPACE>/vault/<perkara>/<YYYY-MM-DD>_<slug>.md`
  (default SHARED_WORKSPACE = `~/workspace/gsp-hermes/workspace`; perkara default `umum`).
- **Wiki (terbit):** `~/.hermes/wiki/<type>s/<slug>.md` — ditulis **hanya oleh librarian**
  lewat proses promote (`gsp-library-workflow`).

## Format objek vault

Satu berkas markdown per objek. Frontmatter YAML + body. Gunakan helper
`vault_propose.py` (scripts/ skill ini) agar format konsisten.

```yaml
---
id: <slug-stabil>                  # stabil; path boleh berubah, id tidak
type: vendor|produk|standar|proyek|dosir|catatan|keputusan|pelajaran|fakta
title: "Judul manusiawi"
status: usulan                     # usulan → ditinjau → menunggu_persetujuan|menunggu_verifikasi → dipromosikan|ditolak|perlu_revisi
sumber: <path relatif di RAW, WAJIB utk klaim/angka>
halaman: <hal. atau rentang, utk dokumen berhalaman>
tanggal_akses: YYYY-MM-DD
kelas_bukti: primer|sekunder|tersier|sintesis
sensitif: tidak|ya                 # ya → wajib persetujuan user sebelum promote
perkara: <folder/kasus>            # bila bagian dari dosir/perkara
tags: [koma, terpisah]
links: [link1, link2]              # referensi silang (wiki/vault/url)
penulis: <profil atau akun>
diajukan: YYYY-MM-DD
---
<body: ringkasan + bukti. Setiap ANGKA/klaim kuat WAJIB membawa kutipan sumber+halaman.>
```

## Taksonomi tipe (skema diamati)

Tipe bukan daftar mati — ia **diamati** dari isi. Nilai awal:
`vendor`, `produk`, `standar`, `proyek`, `dosir`, `catatan`, `keputusan`, `pelajaran`, `fakta`.
Bila korpus menuntut tipe baru (mis. `kontak`), tambahkan di objek — jangan paksa
memasukkan ke tipe lama. Yang salah bukan tipe barunya, melainkan memaksakannya.

## Aturan provenans (prinsip #3)

- **Angka** (harga, kapasitas, tanggal, ukuran) WAJIB menyebut `sumber` + `halaman`.
  Tanpa itu, angka **dianggap tidak ada** — tulis sebagai perkiraan tersurat, bukan fakta.
- **Kelas bukti:** `primer` (dokumen asli/surat), `sekunder` (laporan turunan),
  `tersier` (ringkasan pihak lain), `sintesis` (hasil analisis lintas sumber).
- `tanggal_akses` wajib untuk sumber yang berubah (web, harga pasar).
- Klaim yang tidak bisa dibuktikan: tandai sebagai **asumsi** di body, bukan fakta.

## Status lifecycle

| Status | Arti | Pemegang transisi |
|---|---|---|
| `usulan` | diajukan, belum ditinjau | siapa pun |
| `ditinjau` | sedang dikurasi librarian | librarian |
| `menunggu_persetujuan` | data sensitif — butuh persetujuan user | librarian → user (Approval Inbox) |
| `menunggu_verifikasi` | data dosir — butuh verifikasi manusia | librarian → manusia |
| `perlu_revisi` | ditolak sementara, wajib catatan alasan | librarian |
| `ditolak` | ditolak permanen, wajib catatan alasan | librarian |
| `dipromosikan` | lolos gateway, naik ke wiki | librarian |

Setiap transisi ke `ditolak`/`perlu_revisi` WAJIB mengisi `catatan_keputusan`.
Keputusan tanpa alasan = keputusan yang akan ditafsirkan ulang orang lain.

## Cara mengusulkan

```bash
python3 "${HERMES_SKILL_DIR}/scripts/vault_propose.py" \
  --vault ~/workspace/gsp-hermes/workspace/vault \
  --perkara vendor-katering \
  --title "Vendor Catering Nusantara — profil" \
  --type vendor \
  --sumber "docs/2026_08_21_koleksi_vendor_katering_jabodetabek/data/vendor_nusantara.md" \
  --halaman 3 --kelas-bukti sekunder --sensitif tidak \
  --tags "katering,vendor,jabodetabek" \
  --body "…ringkasan dengan kutipan halaman…"
```

## Aturan pin sumber APPEND-ONLY (terukur kartu t_23320f06 / DDV-STD-1009, 09-10-2026)

Sumber yang terus bertambah (contract doc / Decision Log milik controller) TIDAK BOLEH
dipin langsung sebagai gerbang kesegaran. Terukur nyata: `CONTRACT.md` misi bergerak TIGA
KALI dalam satu giliran kurasi — 40.763 B `59a43c4d220eace7` (ukur penulis objek) ->
41.452 B `c9c6cb8610e1e1f9` (ukur custodian) -> 43.526 B `acf68355f1235780` (ukur saat
pembekuan). Pin apa pun yang ditulis ke berkas hidup akan basi sebelum promosi selesai, dan
prosedur DELTA yang mempinnya akan melaporkan delta palsu tiap kali controller menambah
entri vonis. Jalur sah (putusan controller, sudah dieksekusi dan lolos recheck custodian):

1. **Bekukan salinan byte-identik ke folder perkara** — `vault/<perkara>/contract-snapshot.md`,
   uji `open(a,'rb').read() == open(b,'rb').read()` = True, lalu PIN SIDIK SALINAN itu.
2. **Nyatakan sumber hidup sebagai append-only di prosedur DELTA**: perbedaan dengan berkas
   HIDUP bukan delta yang sah; bandingkan hanya terhadap salinan beku.
3. **Simpan pin lama berlabel "angka saat pengukuran"** (jangan hapus) — ia bukti sejarah
   rantai, bukan cacat muatan.
4. **Rujuk butir lewat anchor TEKS HEADING** ("Decision Log", "Ronde 5", "Disposisi hasil"),
   BUKAN nomor baris — penomoran bergeser tiap entri vonis baru. Nomor baris hanya sah pada
   berkas beku.
5. Bedakan di body mana gerbang DELTA (sumber beku/stabil) dan mana bukan, agar verifier
   tidak memvonis FAIL-palsu. Sumber stabil yang layak dipin langsung pada misi yang sama:
   naskah sumber, docx terbit, register kuantitas, register eksepsi (empat-empatnya terbukti
   tidak berubah sepanjang misi).

## Nomor register lajur TIDAK global: rujukan wajib membawa tag lajur (terukur RAFIF-GAMESKILL-1010 C2, custodian 11-10-2026)

Register per lajur riset memakai namespace sendiri dan nomornya BOLEH bertabrakan: `U-8` hidup di
`L2_domain_map.md` (ambang Android vitals 1,09%/0,47%) sekaligus di `L3_quality_bar.md` (benchmark
retensi GameAnalytics). Konsekuensi penulisan dan vonis:
1. Setiap ID register WAJIB berada di bawah tag sumbernya sendiri (`[R-4 U-4]`, bukan `[R-2 ... U-4]`).
   ID yang menempel di dalam kurung tag rujukan lain = cacat kelas ALAMAT (perlu_revisi ringan, nol angka berubah).
2. Bila satu angka memang hidup di dua lajur, tag GANDA adalah keharusan (`[R-4 T1, R-3 U-8]`) — bukan
   redundansi yang boleh diseragamkan. Verifier yang menyuruh "hapus tag lama" tanpa mengecek tabrakan
   nomor akan membuat alamat jadi ambigu.
3. Perbaikan cukup retag segmen di DALAM kurung (`[R-2 L1-03, B-01]` -> `[R-2 L1-03; R-1 B-01]`), body-only,
   dengan guard: prosa luar-kurung byte-identik + multiset ID keluarga per baris invarian + multiset angka
   prosa grup body identik + EOL CRLF utuh. Bentuk ini memenuhi syarat "terverifikasi tanpa audit ulang muatan".

## Pitfall terverifikasi (custodian 2026-09-01, batch top40-agent-ai)

- **Frontmatter wajib lolos `yaml.safe_load`, dan perkakas library TIDAK memeriksanya.**
  `vault_propose.py`/`vault_promote.py` menulis & membaca frontmatter dengan split baris
  `key: value`, bukan parser YAML — jadi objek ber-frontmatter rusak tetap bisa dibuat DAN
  dipromosikan (lalu kerusakannya tersalin ke wiki). Validasi batch wajib terpisah:
  `uv run --python 3.11 --with pyyaml` + `yaml.safe_load` per berkas + cek `title == H1`.
- **DUA kelas cacat; yang kedua tidak terdeteksi oleh `yaml.safe_load` saja:**
  1. *Gagal parse keras* — `halaman: -` tanpa kutip (dibaca sebagai sequence entry), atau
     nilai berisi `: ` kedua (mis. `catatan_verifikasi: Verdict: x || Alasan: y`).
  2. *Terpotong diam-diam* — nilai tanpa kutip yang memuat `#`, mis.
     `title: … (Top40 #1, L4)` → terparse SUKSES tapi nilainya jadi `… (Top40`. Ini kehilangan
     data tanpa galat apa pun. Terukur di S18b: 212 baris kelas-1 + **88 baris kelas-2**.
- **Cara uji yang benar** (validator yang cuma memanggil `yaml.safe_load` LOLOS pada kelas-2):
  bandingkan nilai hasil parse dengan teks mentah barisnya, setelah kutip luar dilepas:
  `str(parsed[k]) == unquote(raw_value)` → bila beda, nilai terpotong.
  CATATAN (terukur CVLK C1-L2 2026-09-29): `unquote` wajib pakai `json.loads` untuk nilai
  berkutip ganda, BUKAN strip kutip naif — nilai yang ditulis via `json.dumps` memuat escape
  `\"`/`\n`, dan strip naif melaporkan FAIL-palsu "terpotong" padahal nilai utuh.
- **Kutip manual `"{x}"` tidak cukup** — pecah bila `x` memuat `"`. Generator kini memakai
  `_yval()` = `json.dumps` (JSON adalah subset YAML 1.2 → selalu terparse kembali identik).
  **Tetapi jangan kutip menyeluruh:** `status: "active"` merusak grep ekosistem dan self-test.
  Nilai aman tetap plain; hanya nilai bermasalah yang dikutip (`_plain_is_safe()`).
- **Sunting massal frontmatter: cadangkan dulu + buktikan body tidak berubah.** Wiki
  `AppData/Local/hermes/wiki` BUKAN repo git (git di promote diam-diam no-op) → tidak ada
  rollback otomatis. Pola: snapshot berkas + hash md5 body sebelum/sesudah, hard-fail bila
  ada body yang berubah. Perbaikan S18b: 86 berkas / 288 baris, 87/87 hash body tetap cocok.
- **Jangan rekonstruksi frontmatter dengan `join(fm_lines)` saja — baris penutup `---` ikut hilang.** Pola aman untuk suntingan status satu baris: baca teks mentah, tentukan indeks delimiter pembuka/penutup, ganti SATU elemen pada daftar baris mentah di antaranya, lalu tulis ulang daftar penuh. Tiga guard sekaligus: diff tepat 1 baris, jumlah baris total tetap, md5 body tidak berubah (rollback dari backup bila salah satu gagal). Gejala pola lama: fail cepat saat baca-ulang karena delimiter penutup tak ditemukan (L-B3 2026-09-03; berkas dipulihkan byte-identik dari backup, body vault tidak pernah rusak).
- **Konvensi `title == H1 pertama`** dijaga custodian (dimensi metadata). Saat memakai
  `--body-file`, pastikan baris `# ...` pertama SAMA persis dengan `--title`; jika beda,
  sunting salah satu (pola aman: samakan H1 ke title) SEBELUM verifikasi custodian.
- **Jangan dispatch worker/custodian dengan env kartu librarian aktif tanpa peringatan**:
  anak `hermes -p <profil> -z` mewarisi `HERMES_KANBAN_TASK` dan bisa mem-blokir kartu induk.
  Instruksikan eksplisit "JANGAN panggil tool kanban" di prompt dispatch.

## Pitfall terverifikasi (VSSKB-0923 L-3, kartu t_52ddee03, 23-09-2026)

- **Gerbang marker buatan sendiri FAIL-palsu pada provenans per-seksi.** Objek yang menaruh
  `Sumber: <path ekas/...> utuh` di pembuka seksi lalu memberi marker `[R-n]` hanya pada angka
  kunci membuat penyaring "setiap baris berdigit wajib sebaris marker" melaporkan puluhan weak
  hits pada path berkas, nomor bagian, dan baris tabel. Bentuk uji yang benar: (i) saring dulu ke
  ANGKA BERMUATAN satuan teknis (pix/m, mm, Mb/s, GB, f/d, detik, mK, grade N), (ii) terima marker
  dalam konteks +-4 baris, (iii) terima deklarasi `Sumber:` yang meng-cover sub-seksi (reset scope
  hanya pada heading level-2, bukan level-3). PELONGGARAN baru sah setelah angka itu diverifikasi
  silang ke rak (contoh terukur: `30 f/d` cocok di `ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/
  RANTAI-JAMINAN.md:27`) - bukan setelah dokumen diloloskan.
- **Wewenang pemecahan objek (putusan granularitas librarian):** alasan "kelas bukti berbeda tidak
  boleh satu objek" adalah alasan PELABELAN, bukan selalu alasan PEMISAHAN BERKAS. Satu objek master
  sah bila tiap angka membawa marker sendiri + blok BATAS menyatakan kelas bukti per kelompok;
  catat biaya kurasi berlipat (N verifikasi custodian + N promote + N bukti API) saat memutuskan.
- **Verifikasi silang gatekeeper tetap wajib meski custodian lulus/FAIL:** cocokkan minimal 8-12
  angka lintas bagian ke berkas rak (path:baris) pada giliran yang sama. Pada kartu ini gatekeeper
  dan custodian sama-sama menemukan kecocokan, dan custodian menemukan kelas cacat yang lolos
  gerbang deterministik saya: **angka warisan yang konsisten di korpus teks tapi tidak terkonfirmasi
  pada PDF primer** (dua bentuk Tabel 7 di hulu; geometri sel pymupdf + pdftotext merender jumlah
  nilai berbeda). Implikasi SPK-002 butir 1: kesetiaan hulu bukan bukti benar - untuk angka ambang
  yang akan jadi persyaratan uji, tandai status konfirmasi terhadap sumber primer, jangan hanya
  menyalin resume rak.

## Aturan gerbang promosi dari taksonomi IPDR-GLOBAL (AM-G2/G4/G5, disahkan VE5 t_fbfc624b 2026-09-12)

- **AM-G4 - provenans berjenjang wajib untuk objek hasil akuisisi eksternal.** Objek yang memuat klaim dari sumber web WAJIB mencantumkan di body: (i) sha16 registri/pin beku pembilang, (ii) seed rantai merge/ukur, (iii) path ladder ber-timestamp (rung | URL/aksi | status HTTP + ts | hasil). Klaim eksternal tanpa akun ladder = TIDAK promotable - padanan "angka tanpa halaman = tidak ada" untuk sumber web. Preseden terlengkap: `docs/2026-09-12-ipdr-global/` (rantai GB1..M4 + VD1/VD2 + 27 ladder; VD1 SALAH-TARGET 0 atas 273 fetch mandiri).
- **AM-G2 - guard prosedural kelas pertama.** Di samping guard term-level (regex/batas kata/ko-occur), tiga guard prosedural adalah syarat sah objek: eksekusi ekklusi berakun (analog G-3), adjudikasi manusia per hit dengan disposisi ACCEPT/REJECT/JUDGED-OUT (analog G-7), dan eksklusi direktori arsip dari hitungan (analog G-8). Guard prosedural terbukti bekerja lintas bahasa pada sapuan web eksternal, bukan hanya penambangan korpus.
- **AM-G5 - aturan separator nilai warisan bercabang dua.** Transliterasi eksplisit-terhitung di hulu (deklarasi + cacahan di log parser, mis. U+2014 dan U+00B7 dicatat jumlahnya saat build) = SAH dan tercatat. Drift senyap di lapisan turunan (nilai enum berubah karakter tanpa deklarasi) = pelanggaran kesetiaan sumber (KD-1). Gerbang: uji kesetiaan byte nilai enum warisan, bukan hanya hitungan footprint nol.

## Verification

- Helper `vault_propose.py` lulus `python3 scripts/vault_propose.py --self-test`.
- Objek vault hasil output valid (frontmatter lengkap, path `vault/<perkara>/…`).
- **Frontmatter tiap objek lolos `yaml.safe_load` DAN nilainya utuh** (bandingkan parsed vs
  teks mentah — lihat pitfall kelas-2 di atas). Cek ini TIDAK dilakukan perkakas library.
- Proposa tanpa `sumber` utk klaim angka → helper memperingatkan / menolak bila `--require-provenance`.

<!-- Riwayat: 1.0.4 (11-10-2026, DUPSKILL-L3 t_605e5f7c) diserap dari salinan fisik profil gsp-librarian: aturan pin sumber APPEND-ONLY (t_23320f06), catatan unquote json.loads (CVLK C1-L2), pitfall VSSKB-0923 L-3 (gerbang marker sendiri, wewenang pemecahan objek, verifikasi silang gatekeeper). -->
