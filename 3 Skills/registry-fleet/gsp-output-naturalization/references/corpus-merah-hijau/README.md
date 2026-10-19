dokumentasi corpus - bukan deliverable: berkas ini menjelaskan cara memakai corpus, bukan keluaran yang diuji.

# Corpus merah-hijau uji scanner `scan_ai_footprint.py`

Corpus ini adalah bahan uji gerbang naturalisasi keluaran GSP (kartu NAT-S10,
blueprint langkah 10). Scanner yang diuji:
`../../scripts/scan_ai_footprint.py`. Kebijakan yang diuji: `../kebijakan-naturalisasi.md`
dan `../../SKILL.md`.

## Kenapa berkas merah SENGAJA memuat karakter terlarang

Berkas merah WAJIB memuat literal U+2014 dan U+00B7 beserta bentuk escape/entity-nya.
Itu bukan kelalaian penulis dan bukan cacat yang perlu diperbaiki: kanal C-1 dan C-2
hanya bisa dibuktikan mendeteksi kalau ada sasaran deteksinya. Bentuk escape ditulis
sebagai backslash-u-2014, entity desimal delapan-ribu-dua-ratus-dua-belas, entity
heksadesimal dua-ribu-empat-belas, dan entity bernama mdash; keempatnya memang
ditempel mentah ke dalam berkas agar jalur perhitungan `count_forms()` pada lapisan
mentah ikut teruji (kasus emitter pada matriks sweep baris 20-21). Berkas kebijakan
(`../kebijakan-naturalisasi.md`) memilih jalan lain: ia menyebut karakter lewat nama
kode titik supaya bisa lolos gate etalase. Corpus merah punya kontrak sebaliknya,
yaitu HARUS gagal. Karena itu berkas merah diberi penanda baris pertama
`contoh cacat - bukan deliverable`, dan berkas hijau `contoh bersih - bukan deliverable`.

Aturan praktis: JANGAN pernah menyalin isi berkas merah ke dokumen nyata, dan JANGAN
"membersihkan" berkas merah. Kalau sebuah berkas merah tiba-tiba PASS, yang rusak
adalah scannernya, bukan corpusnya.

## Isi folder

| berkas | warna | yang diuji |
| --- | --- | --- |
| `merah-a1-em-dash.md` | merah | A1 / C-1: literal + escape + entity desimal/heksa/bernama |
| `merah-a2-middle-dot.md` | merah | A2 / C-2: U+00B7 tanpa penanda D16 |
| `merah-a3-emoji.md` | merah | A3 / C-3: emoji di kanal formal |
| `merah-a4567-frasa.md` | merah | A4, A6, A7 + agregat C-4: pembuka generik, jejak percakapan, penutup datar |
| `merah-a5-label-ruang-kerja.md` | merah | A5: label ruang kerja / fungsi internal bocor ke narasi |
| `merah-b-agregasi.md` | merah | ambang agregasi D-TA-09: 6 indikator berat sekaligus (B1,B2,B4,B5,B7,B8) |
| `merah-semua-kode.md` | merah | gabungan A1-A7 dalam satu berkas (kontrol "gerbang tidak mati") |
| `merah-sosmed-caption.md` | merah | kanal `sosmed`: caption promo memuat U+2014 dan U+00B7 -> WAJIB FAIL lewat C-1/C-2 meski kanal parsial (D-TA-08 divonis SAH, `contract.md` D-16, kartu `t_b29e4438`) |
| `hijau-doc-laporan.md` | hijau | deliverable kanal doc/deck/etalase: bersih + marker naturalisasi |
| `hijau-kanban-summary.md` | hijau | ringkasan handoff kanal kanban (D-TA-07) |
| `hijau-notif-deploy.txt` | hijau | kanal pendek chat/notif (D-TA-05) |
| `hijau-sosmed-caption.md` | hijau | kanal `sosmed`: caption santai non-formal beremoji -> WAJIB PASS selama bebas A1/A2 (gaya ikut brief kampanye) |

## Cara menjalankan

Interpreter `python`/`python3` di PATH git-bash host ini adalah stub WindowsApps, jadi
pakai jalur uv (atau interpreter nyata cpython-3.11.15):

```
cd C:/Users/TRIAL/workspace/gsp-hermes/skills/gsp-output-naturalization
UV=C:/Users/TRIAL/AppData/Local/hermes/bin/uv
$UV run --python 3.11 python scripts/scan_ai_footprint.py --channel doc "$(cygpath -w references/corpus-merah-hijau/merah-a1-em-dash.md)"
echo $?   # 1 = ada FAIL, sesuai harapan corpus merah
```

Pemetaan kanal untuk tiap fixture ada di kolom ketiga tabel di atas. Fixture pendek
(`hijau-notif-deploy.txt`) sengaja TIDAK diuji pada kanal `doc`: kanal dokumen menuntut
>=25 kata per kalimat dan maksimal satu paragraf <3 kalimat (H.2.1/H.3.1; ambang gerbang direvisi ke 3 pada NAT-C7 27-09), yang memang
bukan aturan untuk pesan singkat.

## Kontrak hasil

- Berkas merah: `VERDICT: FAIL`, exit 1. Gabungan seluruh berkas merah harus memunculkan
  baris FAIL untuk SETIAP kode `C-1`(A1), `C-2`(A2), `C-3`(A3), `A4`, `A5`, `A6`, `A7`.
- Berkas hijau: `VERDICT: PASS`, exit 0 pada kanal yang diujinya.
- `N/A` berarti check tidak berlaku untuk kanal/format itu, BUKAN lolos.
- `INFO` berarti dilaporkan tanpa menghitung pelanggaran (en dash D-TA-04, media sosial
  D-TA-08, catatan ekstraksi).
- Kanal `sosmed` sengaja mengubah hampir semua indikator menjadi INFO (D-TA-08); hanya
  A1/A2 yang tetap mutlak. Corpus hijau lolos di sana, corpus merah hanya tertangkap
  lewat C-1/C-2.

## Batas yang diketahui

- README ini BUKAN fixture: ia dokumentasi, jadi tidak diuji merah maupun hijau.
  Pada kanal `doc` ia memicu FAIL indikator berat (B1/B2/B8 + agregasi D-TA-09) karena
  gaya penulisannya daftar-and-prosa pendek; itu hasil yang DIHARAPKAN dan sudah
  dicatat di sini agar kontrol NAT-S11 tidak salah menafsirkannya. Semua kanal absolut
  (C-1/C-2/C-3/A4/A5/A6/A7) PASS pada README ini. Saat menjalankan kontrol penuh,
  pisahkan berkas `README.md` dari kelompok merah/hijau atau kecualikan dari sapuan.
- Berkas merah tidak pernah dimaksudkan lolos; ia juga TIDAK boleh ikut sapuan gate
  etalase terhadap folder skill. Saat menyapu folder skill, kecualikan folder corpus ini
  atau perlakukan FAIL-nya sebagai hasil yang diharapkan.
- `C-11` (indikator B9) selalu `N/A` karena juri manusia (RT 5.3).
- `C-10` baru FAIL bila `--require-marker` dipakai; kedua fixture hijau `.md` sudah
  memuat marker sehingga tetap PASS pada mode itu.
