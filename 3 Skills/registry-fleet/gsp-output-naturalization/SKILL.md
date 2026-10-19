---
name: gsp-output-naturalization
description: "Gate naturalisasi keluaran GSP: register formal dan cek jejak AI."
version: 1.11.0
author: Swarm GSP (gsp-skill-creator)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [gsp, naturalisasi, anti-ai, quality-gate, writing]
    category: gsp
    related_skills: [gsp-document-quality-standards, humanizer, gsp-verification-before-completion]
---

# GSP Output Naturalization Skill

Skill TIPIS sesuai D-TA-01: reference-don't-duplicate. Aturan lengkap tinggal di rumah
asalnya (Module H, humanizer, matriks sweep); skill ini merangkai definisi operasional,
default register, ambang agregasi, prosedur gerbang, dan cara panggil scanner. Detail
kanal penuh, daftar pengecualian, format catatan override, dan resolusi en dash ada di
`references/kebijakan-naturalisasi.md` (dibangun kartu NAT-S8); empat pelajaran misi
GAYA-AHLI-1005 (kanal resmi 'standar', worker-mati-setelah-artefak, pin-komentar-vs-artefak,
reshoot-sempit dua juri) ada di `references/pelajaran-gaya-ahli-1005.md`. Engine
`creative/humanizer` read-only (D14): dikutip, tidak disalin, tidak diedit (D-TA-03).

## When to Use
- (Cakupan dipersempit 03-09-2026, kebijakan user) Hanya keluaran yang BENAR-BENAR
  diserahkan ke user: jawaban chat, dokumen, deck, notifikasi cron untuk user,
  artefak etalase (kanal K1-K4, K6). Artefak antar-agen dan jejak orkestrasi
  TIDAK lagi wajib memenuhi gerbang (lihat pengecualian) agar orkestrasi tidak melambat.
- Saat menjalankan gerbang pra-terbit atau audit sampel oleh verifier.
- Cakupan gate etalase K6 (putusan controller `nat-s9hil-putusan.md` butir 1,
  koreksi cakupan): `--channel etalase --require-marker` hanya untuk artefak
  deliverable sesuai definisi RT 3.1 (file final di `docs/`, `HASIL-PROJECT-*`,
  ZIP serah terima). Berkas skill/references = artefak internal: tetap dipindai
  pada kanal doc, tidak diwajibkan memiliki marker C-10 maupun ambang kerapatan prosa khas
  K6; C-1/C-2/C-3 tetap mutlak padanya tanpa penanda baru.
- Don't use for: markdown antar-agen & jejak orkestrasi (kecualian 03-09):
  contract doc `docs/<kontrak>/`, kartu/komentar/summary kanban,
  `identification/*` (01_translated, 02_structured, SPEC), checkpoint,
  PHASE-REPORTS internal, laporan worker antar-agen; juga isi `metadata`
  mesin kanban, log/event/build, kode sumber, arsip lossless `memory/refs/**`,
  kutipan verbatim eksternal, blok berpenanda D16, SKILL.md engine (read-only).
  Batas tegas (klarifikasi user 03-09): berkas antar-agen BEBAS jejak AI (pola
  A/B tidak diperiksa sebagai kewajiban; konsumennya sesama agen). Keluaran yang sampai ke manusia
  WAJIB naturalisasi penuh karena berpotensi dibawa ke direksi/klien.
  Daftar pengecualian penuh: seksi 3.2 spesifikasi RT
  (`docs/2026-09-02-naturalisasi-output/identification/01_translated.md`, salin ke
  `references/kebijakan-naturalisasi.md` di NAT-S8).

## Sumber rujukan kanonik (pointer, jangan disalin)
| Rumah | Isi | Lokasi |
|---|---|---|
| Module H | Standar anti-AI writing GSP (voice, kalimat, paragraf, kosakata, angka) | `$LOCALAPPDATA/hermes/skills/gsp/gsp-document-quality-standards/SKILL.md` baris 594-923 |
| Humanizer | Taksonomi 34 pola jejak AI, v2.5.1, MIT @blader (dikutip, engine read-only) | `$LOCALAPPDATA/hermes/skills/creative/humanizer/SKILL.md` |
| Matriks sweep | Metode scan per format + aturan penggantian + laporan wajib | `$LOCALAPPDATA/hermes/skills/gsp/gsp-verification-before-completion/references/ai-footprint-sweep.md` |
| Spesifikasi RT | Definisi operasional, kanal K1-K6, A1-A7/B1-B9, override | `workspace/docs/2026-09-02-naturalisasi-output/identification/01_translated.md` |
| Keputusan | D-TA-01..D-TA-10 (adopt), basis profil 53 | `workspace/docs/2026-09-02-naturalisasi-output/contract.md` seksi 4b |

## Default register per kanal (D-TA-05; detail di references/kebijakan-naturalisasi.md)
| Kanal | Register default | Acuan |
|---|---|---|
| K2 Dokumen/laporan/proposal, K3 deck | Formal institusional GSP: sapaan `Kami`, kalimat 21-32 kata rata-rata (revisi 30-09; lama 25-45), paragraf 4-7 kalimat (lama 5-10), klaim spesifik, batasan diakui | Module H.1-H.3 (`:606-753`) |
| K1 Chat kerja / CLI | Formal-effisien: tanpa emoji, tanpa basa-basi servil, istilah teknis utuh tidak di-*italic*; target panjang H.2.1 TIDAK berlaku di chat | H.4.3 + daftar A1-A7; D-TA-05 |
| K4 Notifikasi cron / gateway | Formal-netral, informatif, tanpa dekorasi | Daftar A1-A5; D-TA-05 |
| K5 Ringkasan handoff & komentar kanban | DIKECUALIKAN dari gerbang sejak 03-09 (jejak orkestrasi antar-agen; sebelumnya tunduk via D-TA-07). `metadata` mesin tetap dikecualikan | Kebijakan user 03-09 (kartu t_ed3489c6) |
| K6 Artefak etalase (docs/, ZIP serah terima) | Formal institusional, lolos scanner saat gate pra-terbit; gate marker hanya untuk deliverable sesuai definisi RT 3.1, berkas skill/references = artefak internal (kanal doc, tanpa C-10) | Matriks sweep; putusan `nat-s9hil-putusan.md` butir 1 |
| K7 Naskah panjang gaya kitab (audiens remaja) | Gaya kitab pelajaran remaja; BUKAN kanal pendek. C-6/C-16 dibalik jadi plafon atas FAIL hanya bila rata-rata > 20,0 kata/kalimat (plafon P1a AMBANG-MUTU terkunci); C-7/B2, C-8/B6, C-12/B10, C-13/B11, C-15/B13 dilaporkan sebagai INFO beralasan eksplisit 'kanal kitab' tanpa masuk agregasi D-TA-09; komentar HTML baris provenansi bukan identifier keras; mutlak C-1/C-2/C-3/C-4/C-5/A4-A7/C-8b/C-9a/C-9b/C-9/C-10 tidak berubah; C-17..C-25 ikut perilaku doc | PUTUSAN gerbang t_77fd88c3 (30-09, docs/2026-09-30-sm-c6e02-kitab-channel/PUTUSAN.md seksi 3) |
| Media sosial / konten kreatif | Mengikuti brief kampanye; A1/A2 tetap mutlak (parsial) | D-TA-08 divonis SAH sebagai kebijakan tetap oleh pemilik 02-09 (`contract.md` D-16; kartu `t_b29e4438`) |
| K8 Naskah standar normatif rumah | Kanal ADITIF untuk dokumen normatif yang badan aturannya MENDEFINISIKAN namespace kode sendiri dan MENEGAKKAN standar lain (kelas STD-*/SOP/KAK); BUKAN kanal pendek. Delta terhadap doc HANYA dua: C-7/B2 ambang jadi rasio paragraf <3 kalimat <= 20% total (nama check mencetak '(kanal standar: aparatus navigasi)'); C-8/B6 tebal yang persis sama enam label bidang S-2 (konstanta tertutup `STANDAR_FIELD_LABELS` di scanner, TIDAK dibaca dari dokumen) dikeluarkan dari pembilang dan ambang 6/1000 kata berlaku atas residu dengan jumlah dikecualikan tercetak di detail. Tanpa demosi ala kitab: C-6 tetap floor doc >= 18 (plafon hanya milik kitab), C-12/C-13/C-15 vonis penuh, A4/A7/C-4/C-5 mutlak, tidak ada whitelist identifier baru. Eligibilitas ditegakkan controller SEBELUM sapuan (norma I-4) dan kanal tercetak di CHECK 1; pekerja dilarang memilih `standar` untuk laporan biasa | PUTUSAN t_eec55819 (06-10-2026, work/f4_putusan-kanal-standar.md seksi 2(a); implementasi kartu t_334c0a44) |

Catatan pembagian kerja (RT seksi 4.1, J.6.4 `:1603-1610`): tidak ada humanizer komunitas
yang menargetkan bahasa Indonesia, sehingga Module H/H.6 adalah sumber aturan ID dan
`creative/humanizer` hanya menyumbang mekanika bahasa-agnostik plus taksonomi pola.
Hormati pembagian ini: jangan menuntut humanizer mendefinisikan kosakata AI-typical ID.

## Definisi naturalisasi (RT seksi 2.1; empat sifat, konten-kekal)
Naturalisasi = satu tahap penyuntingan WAJIB setelah konten faktual selesai dan sebelum
konten diserahkan ke kanal yang dibaca manusia, dengan empat sifat:
1. **Konten-kekal.** Fakta, angka, satuan, sitasi, rujukan berkas, dan struktur data
   TIDAK boleh berubah. Naturalisasi mengubah cara bicara, bukan apa yang dikatakan.
2. **Penghapusan pola mesin.** Menanggulangi ciri konkret daftar A1-A7/B1-B9, bukan
   "membaguskan bahasa" secara umum.
3. **Penyesuaian register** ke nilai aktif kanal (formal bila tidak ada override),
   mengikuti suara institusional GSP.
4. **Berbukti.** Meninggalkan jejak yang bisa diaudit: laporan skrip scanner, atau
   deklarasi centang-manual berformat di artefak kontrak. Tanpa jejak, tahap dianggap
   tidak dijalankan.

Batas definisi (RT seksi 2.1): menambah basa-basi, pujian ke user, pertanyaan retoris,
metafora paksa, atau tanda seru berlebih BUKAN naturalisasi melainkan pelanggaran
(humanizer pola 22, 30, 32, 34 di `SKILL.md:379,485,511,537`). Naturalisasi GSP = bersih
dan formal, bukan ramah dan berbunga.

## Definisi gaya mesin (RT seksi 2.2; ambang dua lapis)
Teks keluaran tergolong gaya mesin bila memuat minimal SATU pelanggaran absolut (A1-A7,
ambang 0), ATAU minimal DUA indikator berat (B1-B9) pada artefak final, ATAU terpicu
aturan agregasi D-TA-09 di bawah.

## Pelanggaran absolut A1-A7 (ambang 0; ringkasan ber-rujukan, definisi penuh di RT seksi 2.2 tabel A)
| Kode | Ciri (ringkas) | Rujukan sumber |
|---|---|---|
| A1 | Em dash U+2014, termasuk bentuk escape backslash-u-empat-digit-heks dan entity HTML (desimal, heksadesimal, maupun nama entitas) | D17 mutlak; `ai-footprint-sweep.md:5-7`; resolusi en dash D-TA-04: hanya pola en dash di antara dua digit (pola penuh di references/kebijakan-naturalisasi.md) |
| A2 | Middle dot U+00B7 di luar blok berpenanda `> Penanda D16:` / `# D16:` | D16; `ai-footprint-sweep.md:8-10` |
| A3 | Emoji di konten formal non-media-sosial | humanizer pola 18 (`SKILL.md:327`) |
| A4 | Jejak kolaboratif/percakapan agen: `Hope this helps`, `As an AI`, `Let me know if...`, `Berikut adalah rangkuman yang Anda minta`, sapaan servil | humanizer pola 20-22 (`:353-389`) |
| A5 | Label ruang kerja bocor ke narasi: `scratchpad`, `TODO for me`, nama variabel/tool internal, nama fungsi kanban (`kanban_complete`, `dispatch HQ`) sebagai isi bukan rujukan teknis | interpretasi RT M-5; diperkuat `contract.md:16` |
| A6 | Penutup datar generik: `Demikianlah pembahasan mengenai...`, `Dengan demikian dapat disimpulkan bahwa...` | Module H.3.3 (`:960-966`), H.6.1 (`:871-880`) |
| A7 | Pembuka generik: `Di era digital yang berkembang pesat...`, `Seiring perkembangan teknologi...`, `Tidak dapat dipungkiri bahwa...` | Module H.3.2 (`:716-721`), H.4.4 (`:792-806`) |

Contoh negatif siap-pakai (sumber RT seksi 2.3; ditulis dengan nama kode titik, bukan
literal, agar artefak ini sendiri lolos sapuan):
| Kode | Sebelum (cacat) | Sesudah (formal) |
|---|---|---|
| A1 | `Hasil audit <U+2014> 12 temuan kritis.` | `Hasil audit: 12 temuan kritis.` |
| A2 | `Ringkasan Eksekutif <U+00B7> Triwulan III` | `Ringkasan Eksekutif, Triwulan III` |
| A3 | emoji roket + centang untuk melaporkan deploy | `Deploy selesai.` |
| A4 | `Semoga membantu! Jangan ragu bertanya.` | `Kami siapkan rincian tambahan bila diperlukan.` |
| A5 | `Saya memanggil kanban_complete dulu.` | `Laporan diserahkan melalui kartu tugas.` |
| A6 | `Demikianlah pembahasan di atas.` | `Implikasinya pada TA 2027 kami uraikan di bab 4.` |
| A7 | `Di era digital ini, aset digital...` | `Aset produksi 2024 tersebar di 3 gudang.` |

Contoh positif alih-register (RT seksi 2.1): bullet telegrafik beremoji menjadi narasi
formal dengan konteks anggaran dan pengakuan batasan, sementara angka 4 dan 57 unit
tidak berubah; chat `Done! ... Let me know if you need anything else!` menjadi
`Perubahan sudah saya terapkan pada berkas ... Silakan sampaikan bila perlu
penyesuaian lanjutan.`

## Indikator berat B1-B9 (ringkasan ber-rujukan; definisi + ambang referensi di RT seksi 2.2 tabel B)
| Kode | Indikator (ringkas) | Ambang referensi | Rujukan sumber |
|---|---|---|---|
| B1 | Rata-rata panjang kalimat terlalu pendek | < 18 kata (dokumen Tier 2+) | H.2.1 (`:631-641`, direvisi 30-09) |
| B2 | Paragraf kurang dari 3 kalimat (revisi NAT-C7 27-09; H.3.1 target 4-7 sejak 30-09) | > 1 paragraf pendek per dokumen | H.3.1 (`:692-702`) |
| B3 | Istilah EN / nama produk / standar di-*italic* | > 2 kemunculan; 0 untuk nama produk/standar | H.4.2 (`:766-779`) |
| B4 | Kosakata AI-typical ID + blacklist EN | > 1 per 1.000 kata | H.4.4 (`:792-806`), H.6.1 (`:871-880`) |
| B5 | Transisi monoton berulang (`Selanjutnya`/`Selain itu`/`Furthermore`) | > 60% transisi satu jenis | H.3.4 (`:738-753`) |
| B6 | Tebal berlebihan / header-inline jadi daftar vertikal | > 6 per 1.000 kata; > 2 item beruntun | humanizer pola 15-16 (`:292-315`) |
| B7 | Hedging berlebihan (`dapat`, `mungkin`, `berpotensi`) tanpa kuantifikasi | > 3 per 1.000 kata | H.6.2 (`:882-899`), humanizer pola 24 (`:403`) |
| B8 | Tanpa angka spesifik / tanpa pengakuan batasan | wajib ada >= 1 di dokumen analitis | H.5.3-5.4 (`:843-867`) |
| B9 | Kesimpulan datar/rapi tanpa implikasi | penilaian juri | H.3.3, H.6.2; humanizer pola 25 (`:414`) |
| B10 | Gaya catatan cepat: panah ASCII pengganti kata, rantai titik-koma perangkai fragmen tanpa predikat, singkatan chat tak baku (`masing2`, `yg`, `dgn`) | FAIL hanya bila >= 2 sinyal berbeda terpicu; 1 sinyal dilaporkan INFO | kartu `t_c79b5f6d` kandidat NAT-HIL-E1; bukti S-09/S-18 lolos scanner v1.2.0 padahal juri memilih lawannya 2/2 (`juri-pasangan-kunci.json`) |

Scanner melaporkan B10 sebagai baris `C-12 gaya catatan cepat` dan mendaftarkannya ke
agregasi D-TA-09 serta ke daftar kode yang boleh dikecualikan penanda blok kebijakan.
Rentang kode sebaris (backtick) tidak dihitung sebagai sinyal: token di dalamnya adalah
rujukan ke bentuk (dokumentasi daftar hitam), bukan pemakaian sungguhan (kelas bug sama
dengan positif palsu marker C-10 dan CHECK 9).

## Indikator baru NAT-GATE-R1 (30-09-2026): jawaban atas tiga temuan user

| Kode | Indikator | Ambang | Status penegakan |
|---|---|---|---|
| B11 | `C-13` kode mesin tanpa label manusia di prosa (id kartu `t_...`, status mentah `needs-review`, hash panjang, nama kolom `finished_at`) | FAIL mulai 3 identifier keras berbeda; 1-2 = INFO | aktif diberlakukan (masuk agregasi D-TA-09) |
| B12 | `C-14` gagasan ditulis ulang: kalimat berimbuhan-normalisasi dengan kemiripan Jaccard >= 0,70 dalam jendela 12 kalimat | FAIL mulai 2 salinan berlebih; 1 = INFO | aktif diberlakukan (masuk agregasi D-TA-09) |

Alasan dua check ini ada: pelonggaran ambang panjang (B1/B8) mengambil kembali daya
pisah yang selama ini menutupi cacat "terlalu panjang" dan "isi berulang". Tanpa B11/B12,
turunnya ambang hanya membuat gerbang lebih lemah. Aturan gaya tinggal di Module H.4.5
(kosakata utama ranah) dan H.4.6 (kode mesin untuk manusia); scanner adalah alat
ukurnya, bukan sumber aturannya.

**Skop C-13 (positif palsu yang sudah diukur dan ditambal).** Hanya baris narasi yang
dinilai; baris tabel dan heading dikecualikan karena kepala tabel adalah label sah
(Module L.4). Rentang backtick dibuang lebih dulu (rujukan bentuk, bukan pemakaian).
Pada docx, run berfont monospace (nama font memuat `mono`/`courier`/`consolas`,
case-insensitive - termasuk token gaya DATUM `IBM Plex Mono`) diperlakukan SETARA
backtick untuk penilaian C-13 saja: teks run mono keluar dari lapisan evaluasi C-13,
teks run non-mono pada paragraf campuran tetap dinilai penuh, dan identifier yang
keluar dilaporkan sebagai baris INFO `C-13 identifier monospace dikecualikan`
(visibilitas terjaga; preseden pengupasan komentar HTML kanal kitab yang tetap
khusus kanal itu). Check lain memakai lapisan utuh - regresi byte-identik wajib -
dan ambang `CODE_MIN_FAIL=3` tidak berubah (PUTUSAN-HEUR-1009 butir 3, kartu
`t_d9d918a6`; bukti basal: artefak DDV Rev A 57/57 identifier keras hanya muncul di
run mono). Jalur glosarium C-13 ikut aktif pada docx lewat deteksi gaya heading Word
(`Heading N`/`Judul N`) SEBAGAI TAMBAHAN di samping heading markdown (temuan
pendamping putusan: pencocok `^#{1,6}` tidak pernah cocok pada lapisan `para.text`).
Kode standar resmi dengan prefiks konteks (`MIL-STD-130`, `BS EN 62676`) dan daftar putih
satuan (`kW`, `kVA`, `Hz`) tidak dihitung. Kode yang muncul pada bagian **daftar
istilah/singkatan/glosarium** dianggap sudah berlabel (jalur sah H.4.1). Kelas
kode kebijakan/standar (`SPK-002`, `V-1`, `D-TA-09`, `C-4`) dilaporkan **INFO, belum
menagih**: pada laporan nyata kodenya sering menjadi objek pembicaraan yang penjelasannya
berupa prosa, bukan kurung, sehingga belum punya daya pisah yang aman. Naikkan kelas ini
ke FAIL hanya setelah korpus kalibrasi cukup (lihat Verification).

**Skop C-14.** Kalimat berlabel struktural (`Tabel 1.2 ...`, `Sumber ...`, `Gambar ...`)
dan kalimat yang memuat rujukan berkas dikecualikan karena formatnya wajib seragam antar
bagian, jadi persamaannya bukan pengulangan gagasan (terukur: tanpa pengecualian ini satu
deliverable nyata menghasilkan 18 temuan palsu, setelah ditambal 0). Metriknya salinan
berlebih (ukuran kelompok dikurangi 1), bukan jumlah pasangan, supaya satu gagasan yang ditulis
ulang tiga kali tidak terasa lebih ringan daripada dua gagasan yang ditulis ulang dua kali.

**Kalibrasi terukur pada artefak nyata (8 berkas, kanal etalase, 30-09-2026).**
Vonis tidak berubah 3 berkas; FAIL C-6 hilang 3 berkas (efek pelonggaran ambang); FAIL
baru C-13 pada 2 berkas (deliverable klien berisi `delegate_task` + nama kolom, dan satu
laporan berisi hash 64 karakter di prosa); C-14 FAIL 0 berkas. Perubahan PASS→FAIL 1
berkas. Rekam jejak lengkap: `scripts/fleet-ops/nat-gate-r1/compare_gate_versions.py`
dengan keluaran tersimpan di `$LOCALAPPDATA/Temp/regresi-nat-r1.txt`.

## Indikator baru NAT-GATE-R2 (30-09-2026): tujuh detektor dari audit PANDUAN-RAFIF-MOBILE + tambahan user

| Kode | Detektor | Ambang | Penegakan |
|---|---|---|---|
| B13 | `C-15` ekor kalimat: p90 dan maksimum lebar prosa (butir daftar `1) ... 2) ...` dikecualikan - struktur sah dokumen formal) | FAIL bila maks > 160 ATAU >= 10 kalimat lewat langit-langit 80 (H.2.1); 1-9 = INFO | diperhitungkan dalam penilaian agregat |
| B14 | `C-16` seksi terburuk: rata-rata kata/kalimat per paragraf >= 25 kalimat (unit ukur = unit pengalaman baca, bukan dokumen utuh) | FAIL bila seksi terburuk < 14 kata/kalimat | diperhitungkan dalam penilaian agregat |
| B15 | `C-17` kerangka label seragam: urutan label >= 3 pada >= 5 entri berseri | share >= 80% satu urutan = layak revisi | INFO pantauan dulu |
| B16 | `C-18` kepadatan rujukan: URL mentah + tanggal ISO vs bernama per 1.000 kata | ambang vonis menunggu kalibrasi | INFO pantauan |
| B16 | `C-19` daftar istilah: heading DAFTAR ISTILAH/SINGKATAN/GLOSARIUM hadir; **ambang panjang 6.000 kata DICABUT user 30-09** - dinilai pada semua berkas berprosa kanal panjang | jalur sah pengecualian glosarium C-13 ikut aktif | INFO pantauan |
| B16 | `C-20` suara penulis: densitas `Kami` + klausa sikap vs kemunculan `penulis`; pola Kami=0 dengan penulis>=2 ditandai TANPA sapaan | frasa `oleh penulis`/`menurut penulis`/`bagi penulis` masuk BLACKLIST_B4 (ambang densitas 1/1.000 kata menahan pemakaian sah) | INFO pantauan + B4 menagih |
| n/a | `C-21` manifest visual docx/pptx: kepala `Gambar k.n` vs objek tertanam (`word/media`, `ppt/media`) | FAIL bila kepala > 0 dan objek = 0 (janji visual kosong); rasio < 1/3 = INFO | menentukan hasil secara langsung |
| n/a | guard ekstraksi PDF: baris INFO tetap saat pdf berprosa - vonis metrik panjang pada pdf = NEEDS_REVIEW, wajib dibandingkan sumber markdown/docx (preseden ukur: 5,8 vs asli 29,5 kata/kalimat) | n/a | pelaporan |

Alasan kelas ini lahir (semua terukur, log di `docs/2026-09-30-nat-gate-r1/ukur_*.log`):
ekor kalimat RAFIF-MOBILE p99=116 kata dan maks 456 padahal rata-rata lulus; kerangka
`Intinya>Asalnya>Untuk proyekmu` identik 10/10 entri; URL mentah 12,2/1.000 kata; buku
385 halaman tanpa daftar istilah; LAPORAN-ADINT `Kami=0, penulis=8` lolos total; buku
sama 0 gambar tertanam dengan 1.236 penanda tabel sebagai tambalan. Aturan gaya tinggal
di Module H.1.3 (suara penulis), H.2.1 (langit-langit), I.11 (konten visual), dan
GSP-SDT butir 18 (manifest visual); scanner alat ukurnya.

**Kalibrasi R2 pada korpus nyata (6 berkas, kanal etalase, 30-09).** FAIL baru C-15
pada 3 berkas (RAFIF-MOBILE maks 294 kata/74 lewat langit-langit; ADINT 39 kalimat;
ANOMALY_SIX turun ke INFO setelah kalibrasi - dari 174 jadi 87 kata, cacat format sah);
C-16 PASS pada RAFIF (seksi terburuk 20,5 - detektor bekerja, cacat
dokumen ini memang di ekor bukan rata-rata seksi); C-17 INFO 73% (di bawah ambang 80,
deteksi pola tanpa menghukum). Selftest 66 tes VERDICT PASS, determinisme byte-identik
dua run (sha[:16] `f00089c3ce59e720`). Regresi: `$LOCALAPPDATA/Temp/regresi-nat-r2.txt`.

## Indikator baru NAT-GATE-R3 (30-09-2026): lengkung narasi (koreksi user ketiga)

Koreksi user atas C-20: densitas sapaan mengukur KEHADIRAN suara, bukan GERAK cerita.
Dokumen wajib bercerita: runut latar-ke-tujuan, bab bersambung, ada klimaks ditempatkan.
Aturan tinggal di Module H.3.5; scanner alat ukurnya. Berlaku hanya pada dokumen
bersistem bab (kanal pendek N/A; dokumen tanpa >=4 heading atas N/A, bukan PASS senyap).

| Kode | Detektor | Ambang | Penegakan |
|---|---|---|---|
| B17 | `C-22` lengkung: heading atas pertama area latar (PENDAHULUAN/CARA MEMAKAI/PETA PERJALANAN), heading tujuan (KESIMPULAN/REKOMENDASI/LANGKAH BERIKUTNYA) di seperempat akhir | kedua ujung ada dan berurutan = PASS | INFO pantauan |
| B18 | `C-23` sambungan antar bab: kalimat tepi (2 pertama/2 terakhir tiap bab) memuat penanda dari/ke bab lain | >= 60% bab bersambung = PASS | INFO pantauan |
| B19 | `C-24` momen pembalik: penanda klimaks (ternyata/kunci/di sinilah/bukan X melainkan Y/temuan terbesar) di badan dokumen (buang seperempat awal+akhir) | 0 penanda di badan = FAIL | **menentukan hasil secara langsung** (biner, risiko rendah) |
| B20 | `C-25` bab-katalog: porsi blok prosa berpredikat per bab (tabel/heading/register dikecualikan) | < 30% prosa pada bab >= 200 kata = dilaporkan | INFO pantauan |

**Kalibrasi R3 pada RAFIF-MOBILE (30-09, 16 dtk untuk 1,2 MB).** C-22 PASS (54 bagian;
latar di posisi 3, tujuan di 42); C-23 INFO 14% (4/28 bab bersambung - terkonfirmasi
manual: buku disusun unit-unit paralel, inilah ukuran dari keluhan 'bertele tanpa arah');
C-24 PASS (11 bab memuat momen pembalik, pertama 'KUNCI' di Bab 6); C-25 INFO 3/28 bab
katalog (terburuk Bab 15 di 23%). Dokumen tanpa bab (ANOMALY_SIX) keempatnya N/A dan
vonis tidak berubah PASS. Dua cacat detektor ditemukan dan ditambal saat kalibrasi:
lapisan gabungan menghancurkan pemecah paragraf (narrative_share terbaca 0% padahal
asli 50%; fix `_split_paras` memecah sebelum heading), dan ujung awal lengkung buta
terhadap bagian non-BAB (fix `spine_titles` memakai semua heading atas). Selftest
v1.7.0: 70 tes VERDICT PASS.

## Butir mekanisasi S14 (05-10-2026): GAYA-AHLI-1005 (scanner v1.9.0; kartu `t_d8e19ab2`, putusan `t_dbb77bfe`)

Putusan resmi 18 butir: approve 12 (termasuk M-17 berbentuk larangan), tunda 3
(M-06/M-11/M-16 - TIDAK diimplementasikan), reject 2 (M-07/M-14). Nomor dibuka:
C-26/C-27/C-28/C-33 + mekanisme D18; dicoret permanen: C-30/C-31/C-32/C-34
(C-30 diserap C-13, C-31 diserap C-18, C-34 diserap C-20 sebagai data).

| Kode | Detektor baru | Ambang | Penegakan |
|---|---|---|---|
| - | `C-26` kepadatan klausa (M-01): rata-rata pemisah klausa/kalimat + % kalimat berantai >=4 koma/titik-koma, lapis prosa scanner, populasi >=4 kata non-enumerasi | > 2,2 ATAU > 20% | INFO dulu (naik FAIL hanya setelah retrofit nol positif palsu; kanal kitab dilaporkan sebagai INFO) |
| - | `C-27` plafon rata-rata kata/kalimat (M-02): objek ukur avg_words lapis prosa scanner (BUKAN lapis ekstrak), koordinat C-16 tidak diubah | > 32,0 | INFO dulu; kitab ikut plafon P1a milik C-6 |
| - | `C-28` subjek verba keputusan (M-10): kalimat berverba keputusan bersubjek artefak alat (daftar tertutup di konstanta, dapat diaudit) | > 1,0/1.000 kata | INFO dulu; ambang putusan >2 terbukti terlalu longgar di lapis ini (kalibrasi 10 dokumen: DATUM 2,19 DEMS 2,41 vs manusia ED2 0,00 KAK 0,28) |
| - | `C-33` konsistensi konvensi numerik dalam satu dokumen (M-15): pembanding pada KELAS varian (Rp tempel/spasi, persen simbol/kata, tanggal ISO/bernama-ID/EN, skala kata/digit), bukan token mentah | >= 2 varian dengan populasi >=2 dalam satu kelas | INFO dulu; naik FAIL hanya untuk pola populasi timpang (mis. 3 vs 300) |
| - | INFO rasio pembuka (M-09): kata pertama setelah normalisasi case+strip tanda baca (definisi dibekukan di f3_impl-notes), aktif HANYA > 2.000 kalimat | < 0,20 | INFO pantauan murni, tanpa nomor C |
| D18 | Lapis satu (M-03): berkas berpenanda D16 dengan temuan U+2014/U+00B7 wajib baris INFO rincian aparatus daftar tertutup (kop/provenans/klasifikasi) vs prosa. Vonis C-1/C-2 TETAP mutlak atas total mentah - bukan celah, alamat baca | - | INFO (gate-options 8.3 utuh) |
| D18 | Lapis dua (M-03): baris `> Blok Kutipan: <rujukan sumber>` (varian heading/komentar HTML) membuka blok sampai heading berikutnya; rujukan sah = kartu t_xxxxxxxx / kata sumber,from,pengirim,dari / arsip,verbatim / nama berkas / akun @. Blok sah mengecualikan A4/A5/A6/A7/C-4 + metrik gaya dari prosa surat/vendor (I-5); tanpa rujukan -> DITOLAK, dilaporkan INFO | - | mewajibkan rujukan; C-1/C-2/C-3/C-5 tetap mutlak |
| - | Perluasan C-13 (M-12): kelas enum-status ALLCAPS bergaris-bawah + identifier API camelCase-berdigit = KELAS LEMBUT INFO di baris terpisah (`perluasan C-13 M-12 ...`), whitelist produk/standar berlaku; kelas keras lama tidak berubah | - | INFO permanen putaran ini |
| - | Perluasan C-18 (M-13): hitungan kalimat padat penanda `[R-n]` (>1 penanda per 20 kata) menempel di detail C-18; remedinya pindahkan mark ke baris tabel, jangan hapus rujukan | per kalimat | INFO (ikut induk C-18) |
| - | Data sapaan K2 (M-16 diserap ke M-06): penghitung `kamu/Yth./Bapak/Ibu/Saudara` menempel di detail C-20 sebagai DATA; vonis kenaikan predikat ikut naskah final langkah 11 | - | data referensi, belum menjadi dasar penilaian wajib |
| - | Whitelist struktural C-14 (M-04): pola boilerplate tertutup (tanda tangan surat, kepala turunan, baris notasi) keluar dari populasi salinan-berlebih; pemeriksaan TIDAK dihapus - narasi dobel tetap FAIL (fixture dua arah) | - | tetap berlaku seperti sebelumnya |
| BUG | Fix M-05: `frasa_hits` kini regex berbatas kata (sebelumnya substring murni `in`; kasus nyata CH17 `such as an aisle` divonis A4 oleh entri `as an ai`, jalur absolut). Berlaku untuk A4/A5/A6/A7/B4 karena satu fungsi. Cache isi-only deterministik | - | perbaikan vonis, dua arah dijaga selftest |
| Larangan | M-17: kelas penguat (holistik/sinergi/terdepan/paripurna/pemberdayaan/keberlanjutan/sangat+adjektif) dan kemubaziran sinonim DILARANG masuk daftar hitam pada revisi berikutnya (bukti G3: manusia lebih padat penguat dari fleet - tanpa daya pisah); aturan benar = tagih angka densitas B4 | - | komentar pengaman di kode |
| Data | M-18: `references/daftar-padanan-wajib.md` - berkas data referensi Manual L4; tiga pasangan berlabel ASSUMPTION (backup/rollback/pipeline + review) dilarang jadi dasar FAIL sampai bukti pakai | - | bukan gerbang |

Semua check S14 bekerja pada lapis prosa scanner dengan pemecah kanon `sentences_of`
dan menghormati blok kutipan D18. Temuan struktural Seksi 0 putusan dibukukan: FAIL
di nomor > C-25 TIDAK otomatis memblokir (VERDICT dirakit dari `absolut()` +
`HIGH_INDICATORS`); saat predikat naik, pemblokir wajib dipilih sadar lewat salah
satu jalur itu. Tagihan terbuka yang dinyatakan eksplisit (bukan pelonggaran):
C-8b keterangan LIMITATION berbahasa Inggris TETAP menagih dan butir S14 tidak
menyentuhnya; gerbang kelas karakter CJK dan blok register H.2.1 milik C-15 adalah
gelombang mekanisasi berikutnya. Selftest v1.9.0: 110 tes VERDICT PASS (89 lama +
21 baru merah-hijau kasus papan CH02/CH05/CH06/CH08/CH17 + fixture dua arah tiap
butir); regresi lima cetakan baseline: delta cek lama = 0.

## Guard cuplikan pendek C-6/C-7 (NAT-HIL-E2; kartu `t_c79b5f6d`)
Metrik panjang kalimat (C-6) dan kerapatan paragraf (C-7) tidak punya daya pisah pada
cuplikan pendek: kontrol juri NAT-S22 mencatat 12 dari 18 sisi manusiawi divonis FAIL oleh
kedua metrik ini, dan C-6 menyumbang 303 dari sekitar 350 sampel berat sapuan pasca-gerbang.
Aturan baru: pada lapisan yang dinilai, bila jumlah kalimat < 3 ATAU total kata < 40, baris
C-6/C-7 menjadi `N/A` dengan detail hitungan nyata (bukan `PASS`, agar tidak ada lolos
senyap). Kanal pendek chat/notif tetap `N/A` lebih dulu karena D-TA-05. Dokumen panjang
(>= 3 kalimat dan >= 40 kata) dinilai penuh seperti sebelumnya.

## Aturan agregasi (D-TA-09; diangkat dari Module H.6.2 `:899`)
- Jika 3+ indikator HIGH terdeteksi pada satu artefak, artefak WAJIB direvisi sebelum
  distribusi. Aturan Module H ini diangkat menjadi ambang gerbang fleet (D-TA-09),
  bukan lagi hanya aturan dokumen.
- Lapis artefak final (K2/K3/K6): ambang C-1..C-10 spesifikasi RT seksi 5.2 berlaku
  (rentang kode kini meluas sampai C-21; pemetaan per-kode di tabel NAT-GATE-R1/R2);
  C-1/C-2/C-3/C-4 wajib 0.
- Lapis kanal pendek (K1 chat, K4 notifikasi): C-6/C-7/C-10 TIDAK berlaku (D-TA-05);
  penegakan lewat sapuan sampel DB sesi: ambang pelanggaran absolut 0, pesan dengan
  >= 2 indikator berat maksimal 5% sampel (RT seksi 5.2).
- Verdict sapuan dilaporkan TERPISAH dari verdict artefak agar tidak saling menutupi.

## Prosedur 4 langkah (wajib berurutan, tiap keluaran; M-2)
1. **Draft** - konten faktual selesai lebih dulu; sifat konten-kekal mulai berlaku:
   angka, fakta, satuan, sitasi tidak boleh berubah saat naturalisasi.
2. **Naturalisasi** - sesuaikan register ke nilai aktif kanal (formal bila tidak ada
   override); terapkan A1-A7 (nol) dan B1-B9 (ambang agregasi di atas); ganti pola lewat
   daftar penggantian matriks sweep, bukan hyphen menempel.
3. **Cek gerbang** - jalankan scanner (seksi berikut) atau centang-manual berformat untuk
   kanal tanpa berkas; simpan jejaknya. Tanpa jejak, tahap dianggap tidak dijalankan.
4. **Serahkan** - kirim ke kanal hanya setelah langkah 3 PASS; hasil FAIL dikembalikan ke
   langkah 2, bukan diloloskan.

## Cara panggil scanner (skrip dibangun di NAT-S9)
```
python scripts/scan_ai_footprint.py <berkas|direktori> --channel <kanal>
python scripts/scan_ai_footprint.py --text "<cuplikan>" --channel chat
python scripts/scan_ai_footprint.py --selftest   # exit 0 wajib; byte-identik dua run
```
- Kanal: `chat|doc|deck|notif|kanban|etalase|kitab|standar|sosmed` (alias `k1`..`k8` diterima;
  `kitab` = K7 gaya kitab remaja, lihat tabel register di atas dan PUTUSAN t_77fd88c3;
  `standar`/`normatif`/`k8` = K8 naskah standar normatif rumah per PUTUSAN t_eec55819 -
  pemilihan kanal adalah keputusan controller sebelum sapuan, bukan pilihan pekerja).
  Default `doc`. Kanal tidak dikenal -> `VERDICT: FAIL`, exit 1.
- Keluaran: baris `CHECK n: PASS|FAIL|N/A|INFO - nama | detail` + satu baris `VERDICT:`.
  Exit 0 = tidak ada FAIL, exit 1 = ada FAIL. `N/A` berarti check tidak berlaku untuk
  kanal/format itu (bukan lolos); `INFO` berarti dilaporkan tanpa menghitung pelanggaran.
- Kanal pendek `chat`/`notif`: C-6/C-7/C-10 menjadi `N/A` sesuai D-TA-05.
- Penanda blok terkendali kebijakan (kartu `t_ec8bfdab`, spesifikasi
  `nat-s9hil-gate-options.md` seksi 8): baris `> Penanda Kebijakan: <alasan + rujukan kartu>`
  atau varian heading membuka blok sampai heading berikutnya; WAJIB memuat rujukan kartu
  (`t_` diikuti enam karakter alfanumerik atau lebih) atau blok ditolak dan dilaporkan INFO.
  Blok sah mengecualikan metrik gaya yang terdaftar (C-4 beserta A4/A6/A7, C-6, C-7, C-8,
  C-8b, C-9a, C-9b, C-9, D-TA-09) pada berkas kebijakan/internal; tiap pengecualian muncul
  sebagai baris INFO, tidak pernah lolos senyap. C-1, C-2, C-3, C-5, C-10, dan A5 berada di
  luar daftar dan tetap mutlak pada seluruh lapisan berkas (putusan `nat-s9hil-putusan.md`
  butir 1). Skop per-blok ini sengaja berbeda dari penanda D16 yang per-berkas dan hanya
  menekan C-2.
- C-10 (marker naturalisasi) default `N/A` agar artefak kerja tidak tertahan; jadikan
  FAIL dengan `--require-marker` HANYA sebagai gate pra-terbit deliverable (definisi
  RT 3.1: file final di `docs/`, `HASIL-PROJECT-*`, ZIP serah terima). Jangan tagihkan
  `--require-marker` pada berkas skill/references: artefak internal dipindai pada kanal
  doc (putusan `nat-s9hil-putusan.md` butir 1).
- Posisi sah marker C-10 (kartu `t_19e648d4`, perbaikan positif palsu gate-options
  seksi 3 butir K-2): hanya (1) baris frontmatter YAML dengan kunci `naturalisasi`
  bernilai PASS, atau (2) baris mandiri tempat marker menjadi SELURUH isi baris,
  termasuk bentuk baris tabel kaki `| naturalisasi: PASS | <skrip> | <tanggal> |`.
  Teks yang MENJELASKAN format marker di kalimat prosa atau sel tengah tabel, contoh
  di dalam blok kode berpagar, dan baris berisi placeholder sudut `<skrip>, <tanggal>`
  bukan marker. Vektor temuan lama (regex seluruh lapisan terbaca) digantikan
  pencocokan per-baris berposisi di scanner v1.2.0.
- Format: md/txt/json/py/html + docx/pptx/xlsx/pdf. Office dibaca lewat python-docx /
  python-pptx / openpyxl bila tersedia, selalu dilengkapi sapuan seluruh part XML
  (termasuk core properties). PDF memakai pypdf bila ada; tanpa pustaka itu hasilnya
  fallback byte mentah dan harus diperlakukan NEEDS_REVIEW, bukan PASS penuh.
- Kode sumber dan nilai mesin dikecualikan dari metrik prosa (RT 3.2) TETAPI literal,
  escape, dan entity U+2014/U+00B7 tetap dihitung padanya (kasus emitter R-6).
- Frontmatter YAML dikecualikan dari metrik prosa, tetap dihitung untuk C-1/C-2.
- Pengecualian-diri hanya untuk hasil jalan-jalan direktori; menyebut berkas scanner
  secara eksplisit tetap memindainya (kontrol gerbang tidak mati).
- Catatan interpreter host: `python`/`python3` di PATH git-bash adalah stub WindowsApps.
  Jalankan lewat interpreter nyata (mis. interpreter uv cpython-3.11 di
  `AppData/Roaming/uv/python/`) atau lewat pola `uv run --python 3.11 python ...`.
- Path scanner dari git-bash (rekaman kartu t_a780cf58, 05-10): variabel shell berisi
  `$HOME/AppData/...` diterjemahkan python NATIVE menjadi `C:\c\Users\...` dan gagal
  "No such file or directory". Pass skrip maupun berkas target sebagai path native
  forward-slash (`C:/Users/<user>/AppData/Local/hermes/...`), bukan `$HOME`/MSYS path.
- Kasus-linear penanda D16 (scanner v1.3.0, kartu `t_c79b5f6d`): pola penanda D16 memakai
  kuantifier possessive sehingga baris pemisah panjang (puluhan tanda minus) tidak lagi
  memicu backtracking eksponensial. Regresinya dijaga selftest dengan fixture potongan
  nyata pesan gsp-custodian `state.db` message id=292 (`scripts/fixtures/regresi-id292.txt`,
  isi verbatim, 6753 karakter sumber). Jangan melonggarkan kembali pola itu tanpa mengulang
  uji fixture tersebut.
- Lapisan ekstraksi HTML (scanner v1.8.1, NAT-GATE-R4, temuan kalibrasi artefak rekap
  `docs/2026-09-30-nat-gate-r1/`): isi `<style>`/`<script>` dibuang dari prosa (kelas P-3
  kode), dan `<table>` serta `<title>`/`<head>` dipisah ke lapisan tabel/meta masing-masing
  seperti padanan markdown-docx. Sebelum tambalan ini, satu berkas HTML laporan terbaca
  C-6 15,7 kata/kalimat dari prosa asli 26,2 dan C-15 maksimum 478 kata dari sel tabel
  yang tergabung jadi satu kalimat raksasa; keduanya vonis palsu. Fixture merah-hijau
  r88/r89 menjaga pembuangan style; regresi kanal doc pada artefak rekap: FAIL C-6/C-15
  hilang, PASS bertahan.

## Prosedur override (hanya atas permintaan user; M-4)
- Pemicu sah: permintaan tersurat user (`santai saja`, `lebih ringkas`, `gaya ngobrol`,
  `pakai gaya saya`, atau sampel tulisan untuk voice calibration humanizer `:54-72`).
- Pemicu TIDAK sah: tebakan agen tentang selera user, kebiasaan kanal, instruksi agen lain.
- Scoped: hanya kanal dan misi yang disebut; override "santai di chat" tidak melebar ke
  dokumen resmi; tidak melebar lintas misi.
- Umur: berlaku sampai user mencabut atau misi/kartu selesai, lalu auto-revert ke formal.
- Tercatat: wajib di Decision Log kontrak misi dengan format minimal: tanggal, kutipan
  permintaan user, register baru, cakupan (kanal + misi). Format catatan penuh:
  `references/kebijakan-naturalisasi.md` (NAT-S8).
- Batas keras: override tidak pernah mengampuni A1/A2 (jejak tipografi D16/D17 tetap nol
  di semua register).
- Sesi headless: jalankan default formal, catat opsi di komentar kartu (jangan `clarify`).

## Batas klaim (D-TA-10)
- DILARANG mengklaim `fleet-wide 0` atau `mustahil lolos`: tanpa hook transport, gerbang
  bersifat prosedural-terverifikasi, bukan hard-gate teknis (RT seksi 3.3).
- Klaim cakupan mengikuti pola `ai-footprint-sweep.md:44-48`: sebut metode, cakupan
  sampel, dan tanggal; angka nyata dari laporan scanner atau sapuan, bukan estimasi.
- Yang bisa dijamin fleet: (a) setiap deliverable punya bukti lolos scanner, (b) sampel
  acak keluaran chat diaudit berkala.

## Pitfalls
- Dokumen register/indeks gagal C-7 bukan karena prosa buruk melainkan karena lead-in
  satu kalimat sebelum blok kode atau tabel (kartu `t_f7e1945b`, INDEKS DATMANUAL: 4 dari
  8 paragraf pendek = FAIL agregasi D-TA-09 bersama B8/B19). Ambang C-7 hanya
  membolehkan SATU paragraf pendek per dokumen, dan setiap kalimat pengantar tabel
  dihitung paragraf sendiri. Perbaikan yang terbukti menurunkan FAIL ke nol tanpa
  menghapus konten: tulis lead-in sebagai 3+ kalimat (fungsi + apa yang diuji + di mana
  cetakannya), jangan menggabungkannya ke daftar bernomor. Untuk B19 (C-24 momen
  pembalik) pada dokumen nirsistem-bab-panjang, satu frasa pembeda berformat `bukan X,
  melainkan Y` di badan dokumen sudah cukup; untuk B8 cukup kata `batasan` dalam
  pengakuan batasan nyata. Diagnosa cepat dengan meniru pemecah scanner (`_split_paras`:
  pecah pada baris kosong ATAU sebelum heading), bukan split naif, agar tidak ada
  false-negative verifier.
- Inflasi C-15 pada docx dari penggabungan blok prosa (terukur kartu t_6b4ba247, 05-10): `extract_docx` menambahkan heading sebagai paragraf biasa dan `prose_paragraphs` merangkai segmen prose berurutan tanpa pemisah, sehingga pemecah kalimat menelan "ekor paragraf + kepala seksi + kalimat pertama seksi berikutnya" sebagai SATU kalimat. Akibat: maks kata terbaca 100 padahal tak ada kalimat prosa tunggal sepanjang itu; penanda nomor sub-seksi ("3.5 OFFER-005 - ...") tidak memecah karena huruf setelah titik adalah digit, dan singkatan ("WIB.") ikut menggabung. Implikasi penulis: target keras "maks<=80 per kalimat" TIDAK bisa dicapai penuh pada docx berat-seksi lewat pemecahan kalimat saja; yang dikejar adalah ambang vonis (maks<=160 DAN <10 kalimat lewat 80) plus p90<=60, dan sisa flag dibukukan sebagai artefak penggabungan dengan bukti daftar kalimat (pola w04fixe2_longleft.py). Jangan menurunkan ambang scanner untuk ini.
- Artefak ekstraksi PDF (temuan audit PANDUAN-RAFIF-MOBILE, 30-09-2026): memindai
  PDF terbit langsung menjatuhkan vonis palsu. Baris hasil ekstraksi memecah
  kalimat (rata-rata terbaca 5,8 kata padahal sumbernya 29,5), chrome header/footer
  yang berulang tiap halaman menggembungkan hitung C-2 (772 temuan, 384 di antaranya
  baris chrome), dan slug URL (nama halaman Wikipedia) dihitung C-13 sebagai nama
  kolom internal. Vonis panjang pada PDF adalah properti alat, bukan dokumen:
  laporkan NEEDS_REVIEW, jangan jadikan dasar revisi. Prosedur audit yang benar
  (sumber markdown sebagai lapis utama, pemisahan chrome, rekonstruksi paragraf):
  `references/audit-artefak-pdf-terbit.md`.
- Vonis FAIL tidak boleh naik jadi terbit. Artefak yang berhenti FAIL dengan
  catatan eskalasi (putusan ambang komposit dsb.) DILARANG dipromosikan ke
  PDF/etalase final sampai putusan controller tercatat di Decision Log kontrak.
  Preseden cacat alur: PANDUAN-RAFIF-MOBILE terbit 385 halaman padahal countersign
  misinya sudah memvonis FAIL dua indikator dan eskalasinya tidak pernah naik
  (terdeteksi saat audit balik 30-09).
- Jangan menyalin isi Module H atau humanizer ke sini (D-TA-01/D-TA-03): pointer saja;
  duplikasi = dua sumber kebenaran yang bisa drift.
- Naturalisasi = bersih dan formal, bukan ramah dan berbunga: menambah basa-basi, pujian,
  metafora paksa, atau tanda seru berlebih justru pelanggaran (humanizer pola 22, 30, 32,
  34).
- Klaim cakupan jujur mengikuti D-TA-10: dilarang mengklaim `fleet-wide 0` atau `mustahil
  lolos`; pola klaim lihat `ai-footprint-sweep.md:44-48`.
- Kontradiksi en dash (H.7.1 vs sweep) diselesaikan D-TA-04: U+2013 hanya sah dalam pola
  rentang angka `(?<=\d)\u2013(?=\d)`; di luar itu nol. Patch `ai-footprint-sweep.md`
  dieksekusi di NAT-S26 - sampai kartu itu done, baca kedua sumber sebelum menyimpulkan.
- Gerbang bersifat prosedural-terverifikasi, bukan hard-gate teknis (tidak ada hook
  transport); jangan menjanjikan penyaringan otomatis pra-kirim.
- Sebut karakter terlarang lewat nama kode titik (U+2014, U+00B7), JANGAN literal,
  termasuk di contoh cacat: artefak kebijakan harus ikut lolos sapuan.
- Substitusi otomatis padanan-kode (mis. `F11` -> `rumus konsentrasi engagement`) WAJIB
  diikuti pass penghalusan gramatikal, bukan ganti-kata mentah (kejadian 08-09, misi
  PRABOWO-SOSMED v3: 20 kata dobel beruntun 'aslinya aslinya', 'bobot bobot'; 742 titik
  rusak karena titik-koma sumber ikut tergantikan pola). Gerbang post-substitusi yang
  harus jalan SEBELUM serah: regex `\b(\w{4,}) \1\b` = 0 pada teks terlihat; cek silang
  tanda baca vs versi dasar (titik-koma sah tidak boleh jadi titik + huruf kecil);
  scanner ulang setelah penghalusan (penyatuan fragmen bisa menggeser statistik kalimat).
- Override register (C-6/C-7 kalimat pendek) TIDAK menggantikan entri Decision Log:
  verifier boleh NEEDS_REVIEW sampai controller mengesahkan override di kontrak misi;
  pengesahan hanya wewenang pemilik kontrak, bukan pekerja/verifier.
- Split kalimat penanda nomor (scanner v1.4.1, kartu `t_91146669`, kontrak
  `docs/2026-09-29_defect-scanner-sentsplit-c7`): pemecah kalimat kini ikut
  memecah sebelum penanda `(1) (2) (3)` sehingga blok CEK DIRI bernomor
  tidak lagi terhitung satu kalimat raksasa; bug lama membuat paragraf
  terlihat pendek dan menjatuhkan vonis palsu C-7/B2. Efek laten wajib
  diketahui penulis dokumen: penghitung basal MENGEMBUNG rata-rata kata per
  kalimat, jadi setelah split benar, dokumen bermargin C-6 tipis bisa
  terbit FAIL baru (terukur: w08-bagian-VI misi RAFIF-MOBILE turun dari
  26,7 ke 24,9 kata per kalimat lalu FAIL C-6). Ini koreksi kebenaran,
  bukan cacat tambalan: perbaiki prosa dokumennya, jangan turunkan ambang.
  Varian luas yang memecah semua kalimat berawal digit (kelas `A-Z0-9`)
  DITOLAK dengan bukti regresi lintas-misi pada berkas yang sudah terbit;
  cabang lookahead khusus `\(\d{1,3}\)` adalah bentuk yang disetujui.

## Verification
- Frontmatter valid: `name`, `version`, `description` (inline satu baris <=1024 char),
  `metadata.hermes` hadir; struktur FLAT `gsp-output-naturalization/SKILL.md`.
- Seksi wajib hadir (kriteria S-4 butir a-f): default register per kanal, A1-A7, B1-B9,
  aturan agregasi D-TA-09, prosedur 4 langkah, cara panggil scanner + prosedur override.
- Tiap aturan menyebut sumber (baris Module H / pola humanizer / D16-D17 / D-TA-xx).
- Berkas kebijakan ini dan `references/kebijakan-naturalisasi.md` lolos C-1/C-2/C-3 saat
  dipindai pada kanal doc; `--require-marker` hanya dijalankan sebagai gate pra-terbit
  deliverable, bukan sebagai vonis pada artefak internal (putusan
  `nat-s9hil-putusan.md` butir 1).
- Prosa skill ini sendiri bebas literal U+2014 dan U+00B7 (verifikasi grep byte-level).
- Salinan fleet (NAT-S12) identik sha256 dengan kanonik.

## Riwayat versi

- 1.11.0 (09-10-2026, kartu implementasi `t_d9d918a6`, putusan `PUTUSAN-HEUR-1009`
  butir 3 + temuan pendamping, misi DDV-STD-1009): pengecualian tipografis run
  monospace docx untuk C-13 SAJA (setara backtick markdown, preseden C-12/C-10) +
  baris INFO visibilitas baru `C-13 identifier monospace dikecualikan (tipografi
  docx)`; perbaikan aditif glosarium C-13 pada docx via gaya heading Word (bukan
  pengganti jalur markdown). Ambang tidak diubah (`CODE_MIN_FAIL=3`), kelas keras
  non-mono tetap jatuh, check lain memakai lapisan utuh. Gerbang dua arah terpenuhi:
  hijau artefak DDV Rev A (sha16 `1b2ad3277d9bc98b`) CHECK 21 FAIL->INFO dengan
  VERDICT FAIL->PASS dan INFO tercetak; merah fixture lama #56 md + kontrol docx
  prosa serif + kontrol campuran mono+serif tetap FAIL; mirror tanpa tambalan
  (`.orig`) tetap gagal seperti basal; regresi artefak terbit EOSRAY (VERDICT PASS)
  seluruh baris selain blok C-13 identik pra-vs-pasca + determinisme dua run
  byte-identik. Selftest naik 127 -> 133 tes VERDICT PASS (6 baru: merah serif,
  hijau mono-full + INFO, merah campuran, hijau glosarium-heading, merah glosarium
  tanpa gaya, plus kontrol lama utuh).
- 1.10.0 (06-10-2026, kartu implementasi `t_334c0a44`, putusan `t_eec55819`, misi
  GAYA-AHLI-1005 KAL2): kanal baru `standar` (K8, alias `k8`/`normatif`) untuk naskah
  standar normatif rumah - ADITIF, cabang check lama tidak disentuh dan dokumen tanpa
  kanal ini berperilaku identik (terbukti: runner 66 fixture lama byte-identik vs
  baseline v1.9.1 + regresi 9 korpus kanal doc byte-identik + dua run deterministik).
  Delta HANYA dua dengan alasan tercetak eksplisit: C-7/B2 ambang rasio paragraf <3
  kalimat <= 20% total (manual terukur 13,8%; di atas rasio tetap FAIL B2), C-8/B6
  pengecualian kosakata tertutup `STANDAR_FIELD_LABELS` enam label bidang S-2 dari
  pembilang tebal dengan ambang 6/1000 kata atas residu (residu manual 0,2/1000w;
  B6 tetap bisa terpicu). Putusan REJECT yang dihormati: whitelist namespace C-13
  (mekanisme backtick/D18 existing cukup), plafon C-6 (plafon hanya milik kitab;
  standar mewarisi floor doc >= 18), penanda blok per-bidang, ubah skema manual.
  Selftest naik 110 -> 127 tes VERDICT PASS (17 baru: registrasi kanal, fixture
  HIJAU standar PASS penuh, kontrol regresi doc pada berkas sama, tiga fixture
  MERAH A4/B6/rasio-C-7 tetap diberlakukan, floor C-6 utuh, tanpa demosi C-12/C-13,
  konstanta vocab tertutup enam label).
- 1.9.1 (06-10-2026, kartu perbaikan `t_7b3a29ad`, putusan DEFECT-1 controller
  pada kartu `t_bef365fc`): whitelist C-14 `_DUP_BOILER_RE` diperluas dengan
  padanan blok tanda tangan Inggris `kind regards` / `best regards` /
  `regards` (case-insensitive, word-boundary `\b` menahan 'regarding'/
  'regardless') sejajar padanan Indonesia yang sudah ada. Menambal positif-
  palsu laten DEFECT-1: surat EN yang diratakan menjadi satu kalimat panjang
  salah vonis FAIL C-14 pada v1.8.1 maupun v1.9.0. NOL perubahan lain;
  fixture penagih `f3-m04-kindregards-green.md` kini PASS tanpa isinya diubah
  (runner lapis-hijau target 66 check 0 FAIL 0 NEEDS_REVIEW exit 0).
- 1.9.0 (05-10-2026, kartu implementasi `t_d8e19ab2`, putusan `t_dbb77bfe`, misi
  GAYA-AHLI-1005 langkah 14): scanner v1.9.0 - check baru C-26/C-27/C-28/C-33
  (INFO dulu), INFO rasio pembuka M-09, mekanisme D18 dua lapis (rincian aparatus +
  blok kutipan ber-rujukan), perluasan C-13 (M-12) / C-18 (M-13) / C-20 data sapaan
  (M-16 diserap), whitelist boilerplate C-14 (M-04), fix bug batas kata `frasa_hits`
  (M-05), larangan perluasan daftar hitam penguat (M-17), berkas data
  `references/daftar-padanan-wajib.md` (M-18). Drift versi internal ditambal:
  `__version__` skrip 1.8.1 disinkronkan ke 1.9.0 bersama SKILL.md (temuan
  countersign pengawas atas kartu kembar `t_481c2889`). Butir tunda M-06/M-11/M-16
  dan reject M-07/M-14 TIDAK diimplementasikan; C-29/C-32 tidak dialokasikan.
- 1.8.2 dan sebelumnya: lihat seksi NAT-GATE di atas (perubahan tercatat inline per
  generasi: R1/R2/R3 30-09, NAT-HIL-E1/E2, NAT-GATE-R4 v1.8.1, penanda kebijakan
  v1.3.x-v1.5.x).
