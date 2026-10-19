# Kebijakan Naturalisasi Output: referensi detail (kanal, pengecualian, override, en dash)

- Skill induk: `gsp-output-naturalization` (kanonik `workspace/gsp-hermes/skills/gsp-output-naturalization/SKILL.md`).
- Sumber salinan sah: `workspace/docs/2026-09-02-naturalisasi-output/identification/01_translated.md` seksi 2.1, 2.3, 3.1, 3.2, 4.2 (RT `t_fbb290dd`) + keputusan D-TA-04/05/07/08 (`identification/02_structured.md`; adopt di `contract.md` seksi 4b).
- Kartu pembuat: NAT-S8 `t_bf871b59` (blueprint langkah 8).
- Aturan D-TA-01/D-TA-03 berlaku di sini: berkas ini TIDAK menduplikasi isi Module H maupun humanizer engine: yang menyangkut aturan tulis-menulis lengkap hanya pointer ke rumah asalnya (tabel paling bawah).
- Konvensi penulisan: karakter terlarang disebut lewat nama kode titik (U+2014, U+00B7, U+2013), tidak pernah literal, termasuk di dalam contoh, supaya berkas kebijakan ini sendiri lolos sapuan.

## 1. Kanal wajib K1-K6 + metode uji (RT seksi 3.1; D-TA-05/D-TA-07/D-TA-08)

Gerbang berlaku untuk semua keluaran ke kanal yang dibaca manusia. Tidak ada kanal "kecuali percakapan Swarm": jawaban orkestrator ikut tunduk (keputusan controller D-04).

| Kanal | Isi kanal | Register default | Metode uji | Check yang berlaku |
|---|---|---|---|---|
| T1 Chat ke user | Jawaban CLI/Telegram/WebUI dari worker maupun orkestrator (D-04) | Formal-effisien: kalimat pendek boleh; tanpa emoji; tanpa basa-basi servil; istilah teknis utuh tidak di-*italic* | Skrip sapuan DB sesi (sampel N=200 pesan asisten terbaru per profil): pesan dengan >=1 pelanggaran absolut ambang 0; pesan dengan >=2 indikator berat maksimal 5% sampel | C-1..C-5, C-8; C-6/C-7/C-10 TIDAK berlaku (D-TA-05) |
| T2 Dokumen & laporan | `.md`, `.docx`, `.xlsx`, `.pptx`, `.pdf`, `.html` hasil kerja | Formal institusional GSP (sapaan `Kami`, kalimat 21-32 kata rata-rata (revisi 30-09; lama 25-45), paragraf 4-7 kalimat) | Scanner per-format sesuai matriks `ai-footprint-sweep.md:17-25` saat gate pra-terbit | C-1..C-25 penuh (menagih: C-13/C-14/C-15/C-16/C-21/C-24; pantauan: C-17..C-20, C-22/C-23/C-25) |
| T3 Deck presentasi | Slide pptx/html untuk pimpinan/KAARSENAL | Formal institusional | Scanner per-run python-pptx + seluruh XML part termasuk core properties | C-1..C-25 penuh (menagih: C-13/C-14/C-15/C-16/C-21/C-24; pantauan: C-17..C-20, C-22/C-23/C-25) |
| T4 Notifikasi cron & pesan gateway | Ringkasan terjadwal ke Telegram/all | Formal-netral, informatif, tanpa dekorasi | Scanner teks sebelum kirim + sampel DB sesi | C-1..C-5, C-8; C-6/C-7/C-10 TIDAK berlaku (D-TA-05) |
| T5 Ringkasan handoff & komentar kanban | `kanban_complete.summary`, `metadata` yang dirender, `kanban_comment` | DIKECUALIKAN penuh dari gerbang sejak 03-09-2026 (kebijakan user, kartu t_ed3489c6): jejak orkestrasi antar-agen bebas pola jejak AI karena konsumennya sesama agen. Sebelumnya tunduk prosa via D-TA-07 | Tidak ada (kanal dikecualikan penuh) | - |
| K5b Jejak orkestrasi & markdown antar-agen (BARU 03-09) | contract doc `docs/<kontrak>/`, `identification/*` (RT/SPEC/blueprint), checkpoint, PHASE-REPORTS internal, laporan worker antar-agen | DIKECUALIKAN penuh (kebijakan user 03-09): boleh memuat pola jejak AI; scanner hanya sukarela saat audit internal | Tidak ada cek-gerbang | - |
| T6 Artefak etalase | File final di `docs/`, `HASIL-PROJECT-*`, ZIP paket serah terima | Formal institusional | Scanner saat gate pra-terbit; deliverable membawa marker `naturalisasi: PASS (<skrip>, <tanggal>)` | C-1..C-25 penuh (menagih: C-13/C-14/C-15/C-16/C-21/C-24; pantauan: C-17..C-20, C-22/C-23/C-25) |
| K7 Naskah panjang gaya kitab (BARU 30-09) | Naskah buku pelajaran/kitab remaja (korpus RAFIF-POLISH) | Gaya kitab remaja; BUKAN kanal pendek | Scanner `--channel kitab` (alias `k7`) | Mutlak C-1..C-5, A4-A7, C-8b, C-9a/C-9b/C-9, C-10 tidak berubah; C-6/C-16 = plafon atas FAIL hanya bila rata-rata > 20,0 kata/kalimat (P1a terkunci); C-7/B2, C-8/B6, C-12/B10, C-13/B11, C-15/B13 INFO beralasan 'kanal kitab' tanpa agregasi D-TA-09; komentar HTML provenansi bukan identifier keras; C-17..C-25 ikut doc |

K7 lahir dari PUTUSAN gerbang t_77fd88c3 (docs/2026-09-30-sm-c6e02-kitab-channel/PUTUSAN.md seksi 3): konflik terukur antara ambang misi AMBANG-MUTU KOSONG-01 (P1a ASL <= 20) dan indikator B1 kanal doc yang menilai arah sebaliknya pada naskah gaya kitab. Wewenang PEMAKAIAN kanal kitab vs doc untuk vonis fase misi tetap di controller misi; manager menyediakan instrumen + definisi.

Cakupan K6 (putusan controller `nat-s9hil-putusan.md` butir 1, koreksi cakupan, bukan pengecualian bebas): kolom "Check yang berlaku" pada baris K6 beserta tagihan marker hanya berlaku atas artefak deliverable sesuai definisi RT 3.1 pada baris K6 itu sendiri (file final di `docs/`, `HASIL-PROJECT-*`, ZIP paket serah terima). Berkas skill/references milik GSP adalah artefak internal: tetap dipindai pada kanal doc dengan C-1/C-2/C-3 mutlak tanpa penanda baru, tidak ditagih marker C-10 maupun ambang kerapatan prosa khas K6. Tidak ada nilai ambang yang berubah; yang ditegaskan adalah batas cakupan gerbang.

Media sosial / konten kreatif: pengecualian parsial (D-TA-08): mengikuti brief kampanye, tetapi A1 (U+2014) dan A2 (U+00B7 di luar blok berpenanda D16) tetap mutlak. Pemilik memvonis D-TA-08 SAH sebagai kebijakan tetap pada 02-09 (`contract.md` D-16, kutipan putusan: "Sah, parsial begitu"; kartu eksekusi `t_b29e4438`): masa tunggu konfirmasi rasa di HIL gate (`contract.md` seksi 4b) berakhir, perlakuan parsial ini berlaku permanen sampai keputusan pemilik berikutnya mencabutnya.

Gaya koreksi kanal K1 (KLAIM-TRIAGE, user 03-09): saat menanggapi temuan review, orkestrator TIDAK membuka balasan dengan permintaan maaf refleks ("maaf ini kesalahan klaim saya sebelumnya...") tanpa triase. Balasan yang sah: klasifikasi kelas (T1..T6 per `gsp-orchestrator-worker` Claim Discipline), bukti, jalur perbaikan. Pengakuan hanya untuk kelas T5 (gap klaim controller) dan disebut spesifik: klaim mana, bukti apa yang kurang, perbaikan proses apa. Ini bukan soal sopan santun: pengakuan general yang salah kelas merusak jejak audit dan menyembunyikan akar hulu (deviasi blueprint / mistranslasi intent fleet).

Cara panggil scanner per kanal: `python scripts/scan_ai_footprint.py <berkas|teks> --channel <k1..k6>` (scanner dibangun NAT-S9; `--channel k1`/`k4` mematikan C-6/C-7/C-10).

## 2. Tujuh jenis pengecualian (RT seksi 3.2; gerbang tidak boleh merusak fungsi)

Semua keluaran TIDAK tercakup gerbang bila termasuk salah satu dari tujuh jenis berikut. Daftar ini juga menjadi daftar pengecualian scanner NAT-S9; apa pun di luar daftar tetap tunduk gerbang.

| # | Jenis pengecualian | Alasan | Cara mengenali |
|---|---|---|---|
| P-1 | Isi `metadata` mesin kanban (sha, path, daftar angka) | Bukan prosa untuk dibaca; menaturalisasi kunci/nilai = merusak antarmuka | Field terstruktur JSON/YAML pada payload kanban; hanya `summary` dan komentar yang diperlakukan prosa (D-TA-07) |
| P-2 | Log, event board, keluaran build, stack trace, dump | Forensik butuh verbatim; suntingan merusak nilai buktinya | Keluaran mentah alat/event dengan stempel waktu, bukan narasi penulis |
| P-3 | Skrip, config, workflow JSON, kode sumber | Sintaks tidak bisa dinaturalisasi | Berkas sumber/konfigurasi; komentarnya ikut dikecualikan sebagai bagian berkas |
| P-4 | Arsip lossless `memory/refs/**`, `vault/**`, backup pra-verdict | Aturan arsip melarang perubahan verbatim (memory tiering: dilarang strip tanpa arsip) | Path di bawah `memory/refs/`, `vault/`, atau folder backup bertanggal |
| P-5 | Kutipan verbatim sumber eksternal (standar, petikan vendor, transkrip) | Mengubah kutipan = memalsukan bukti | Wajib ditandai sebagai kutipan (blok `>` atau tanda petik dengan atribusi sumber) |
| P-6 | Blok terkendali berpenanda D16 | Pengecualian yang sudah diputuskan user (retensi U+00B7 dari master design) | Blok diawali `> Penanda D16:` atau `# D16:`; retensi diverifikasi grep ke arsip sumber `extracted/` (`ai-footprint-sweep.md:8-10`) |
| P-7 | Isi berkas `SKILL.md` milik engine (read-only, D14) | Engine tidak boleh diedit fleet | Path di bawah registry engine `hermes/skills/` yang bukan milik GSP (mis. `creative/humanizer/`) |

Batas penting: pengecualian ini menggugurkan tahap naturalisasi pada konten tersebut, BUKAN pada dokumen pembungkusnya. Laporan kontrak yang memuat kutipan verbatim (P-5) tetap harus natural di prosa milik kita sendiri.

Status artefak internal (putusan controller `nat-s9hil-putusan.md` butir 1): berkas skill/references milik GSP TIDAK termasuk tujuh pengecualian di atas dan tidak sedang dikecualikan bebas olehnya. Statusnya adalah definisi cakupan: ia bukan artefak etalase menurut definisi K6/RT 3.1, sehingga kanal wajibnya adalah doc (dipindai penuh; C-1/C-2/C-3 mutlak), sementara marker C-10 dan ambang kerapatan prosa khas K6 tidak ditagihkan padanya. `SKILL.md` engine read-only tetap masuk P-7 seperti tertulis.

## 3. Prosedur override register + format catatan Decision Log (RT seksi 4.2; M-4)

Default register adalah formal di semua kanal. Register hanya boleh berubah atas permintaan user, dengan aturan:

| Aspek | Aturan |
|---|---|
| Pemicu sah | Permintaan user tersurat: "santai saja", "lebih ringkas", "gaya ngobrol", "pakai gaya saya", atau pemberian sampel tulisan untuk dicocokkan (voice calibration, humanizer `:54-72`) |
| Pemicu TIDAK sah | Penilaian agen sendiri bahwa "user mungkin lebih suka santai", kebiasaan kanal, atau instruksi dari agen lain |
| Scoped | Hanya kanal dan misi yang disebut. Override "santai di chat" tidak melebar ke dokumen resmi; override satu misi tidak melebar ke misi berikutnya |
| Umur / auto-revert | Berlaku sampai user mencabut, atau misi/kartu selesai, lalu auto-revert ke formal. Tidak persisten lintas proyek tanpa permintaan baru |
| Pencatatan | Wajib di Decision Log kontrak misi (format di bawah). Tanpa catatan, "default formal" tidak bisa dibuktikan saat audit |
| Batas keras | Override register TIDAK pernah mengampuni pelanggaran absolut A1/A2: jejak tipografi D17/D16 tetap nol di semua register |
| Sesi headless | Worker dilarang bertanya lewat `clarify`; jalankan default formal dan catat opsinya di komentar kartu |

Format catatan Decision Log (satu blok per override, ditempel di `contract.md` misi atau Decision Log kontrak terkait):

```
- OV-<n> [<tanggal YYYY-MM-DD] "<kutipan verbatim permintaan user>":
  register: <formal|formal-effisien|santai|calibrated:<nama sampel>>;
  cakupan: <kanal K1..K6 / media sosial> x <misi/kartu>;
  status: aktif | dicabut <tanggal> | auto-revert <tanggal akhir misi>.
```

Contoh isi (ilustrasi bentuk, bukan override nyata):

```
- OV-1 [2026-09-05] "Untuk chat harian santai saja, tidak perlu terlalu kaku.":
  register: santai; cakupan: K1 chat x misi NATURALISASI; status: aktif.
```

Kaidah pengisian: kutipan permintaan user harus verbatim (bukan parafrasa agen); satu baris status wajib diperbarui saat cabut/auto-revert; jika kolom kutipan kosong, override dianggap tidak sah dan register kembali ke formal.

## 4. Resolusi en dash U+2013 (D-TA-04; adopsi rekomendasi RT opsi b)

Kontradiksi lama: Module H.7.1 (`gsp-document-quality-standards/SKILL.md:920`) mewajibkan en dash U+2013 untuk rentang tahun, sementara `ai-footprint-sweep.md:42` menyatakan en dash ikut nol lolos. Dua aturan fleet saling menyangkal pada karakter yang sama.

Keputusan final (D-TA-04, adopt di `contract.md` seksi 4b):
- U+2013 diizinkan HANYA di dalam pola rentang angka/tahun, yaitu diapit dua digit. Regex sempit scanner: `(?<=\d)\u2013(?=\d)` (dalam regex Python; `\u2013` adalah nama kode titik U+2013, bukan literal di berkas ini).
- Di luar pola itu: nol, sama seperti karakter sapuan lain.
- Kemunculan yang cocok pola rentang dilaporkan scanner sebagai INFORMASI (bukan pelanggaran), beserta jumlahnya.
- Contoh sah: rentang tahun 2027 sampai 2028 ditulis dengan U+2013 di antara kedua angka (ditulis di sini dengan kata "sampai" agar berkas kebijakan bebas literal). Contoh tidak sah: sisipan dalam kalimat, pemisah label, atau en dash menempel pada kata: semuanya pelanggaran.
- Berkas internal (blueprint, kontrak kerja, skill) memakai tanda hubung biasa; kelonggaran pola rentang hanya untuk artefak deliverable resmi (konvensi dokumen resmi Indonesia).
- Deviasi ini dicatat eksplisit di skill DAN di `ai-footprint-sweep.md`: patch penghapusan kontradiksi di sumbernya dieksekusi NAT-S26 (kartu `t_3a5f473b`). Sampai kartu itu done, baca kedua sumber sebelum menyimpulkan.

## 5. Contoh positif/negatif siap-pakai (salinan RT seksi 2.3 + seksi 2.1)

Contoh negatif ringkas untuk uji merah-hijau verifier (RT seksi 2.3; `<U+xxxx>` = nama kode titik, bukan literal):

| Kode | Sebelum (cacat) | Sesudah (formal) |
|---|---|---|
| A1 | `Hasil audit <U+2014> 12 temuan kritis.` | `Hasil audit: 12 temuan kritis.` |
| A2 | `Ringkasan Eksekutif <U+00B7> Triwulan III` | `Ringkasan Eksekutif, Triwulan III` |
| A3 | emoji roket + centang untuk melaporkan deploy | `Deploy selesai.` |
| A4 | `Semoga membantu! Jangan ragu bertanya.` | `Kami siapkan rincian tambahan bila diperlukan.` |
| A5 | `Saya memanggil kanban_complete dulu.` | `Laporan diserahkan melalui kartu tugas.` |
| A6 | `Demikianlah pembahasan di atas.` | `Implikasinya pada TA 2027 kami uraikan di bab 4.` |
| A7 | `Di era digital ini, aset digital...` | `Aset produksi 2024 tersebar di 3 gudang.` |
| B3 | `Sistem *computer vision* kami...` | `Sistem computer vision kami...` |
| B4 | `Hal ini dikarenakan anggaran terbatas.` | `Karena pagu anggaran tidak bertambah.` |

Semua baris di atas adalah ilustrasi cacat. Berkas ini sendiri tidak memuat satu pun literal U+2014 maupun U+00B7, termasuk di dalam contoh, supaya artefak kebijakan ikut lolos sapuan.

Contoh positif alih-register dokumen (RT seksi 2.1). Sebelum (fakta lengkap, gaya mesin): bullet telegrafik `Status: Selesai` beremoji, `Jumlah unit: 57`, dan catatan penting berfrasa AI-typical. Sesudah (register formal GSP, fakta utuh): narasi bahwa pekerjaan 2026 telah memulihkan modul daya pada 4 unit sementara 57 unit selebihnya belum tersentuh peremajaan perangkat keras, dengan pengakuan jujur bahwa penundaan bersumber dari pagu anggaran yang belum bertambah sejak 2024 sehingga rekomendasi bersifat berbasis umur dan lingkungan, bukan pengukuran per unit. Yang berubah: bullet jadi narasi, emoji hilang, frasa AI-typical diganti, batasan diakui. Yang TIDAK berubah: angka 4 dan 57 (sifat konten-kekal).

Contoh positif kanal chat (RT seksi 2.1). Sebelum: `Done! ... Let me know if you need anything else!` (beremoji). Sesudah: `Perubahan sudah saya terapkan pada berkas contracts/notes.md. Silakan sampaikan bila perlu penyesuaian lanjutan.`

Counter-example yang menyesatkan (harus ditolak sebagai "naturalisasi"): menambah basa-basi, pujian ke user, pertanyaan retoris, metafora paksa, atau tanda seru berlebih. Naturalisasi GSP = bersih dan formal, bukan ramah dan berbunga (humanizer pola 22, 30, 32, 34 di `SKILL.md:379,485,511,537`).

## 6. Syarat metodologi uji juri berikutnya (NAT-HIL-E3; kartu `t_c79b5f6d`)

Kontrol juri NAT-S22 menghasilkan akurasi 18/18 justru karena konstruksi ujinya lemah:
juri adalah agen fleet yang memakai buku aturan sama dengan penulis aturan A1-A7, dan
kontras pasangan didominasi satu sumbu tipografis (penggantian U+2014), sehingga kriteria
"pemisah U+2014 menandakan mesin" menjadi hampir deterministik. Blueprint mengandaikan
juri manusia independen dan asumsi itu tidak terpenuhi. Untuk uji juri berikutnya, syarat
minimum berikut mengikat:

1. **Juri independen.** Penilaian dilakukan manusia atau agen non-fleet yang tidak ikut
   menulis aturan A1-A7/B1-B9 maupun restro-sweep. Juri dari profil fleet dengan buku
   aturan yang sama tidak sah sebagai juri utama; ia hanya boleh dipakai sebagai pembanding
   sekunder yang dilaporkan terpisah.
2. **Komposisi kontras.** Minimal separuh pasangan kontras bersifat non-tipografis: kontras
   gaya nyata (prosa naratif versus catatan cepat, register penuh versus fragmen), bukan
   hanya beda tanda baca pada teks yang sama.
3. **Pelaporan per kelompok.** Akurasi dilaporkan terpisah per kelompok kontras
   (tipografis versus non-tipografis), bukan hanya angka agregat. Agregat tunggal menutupi
   perbedaan daya pisah antar kelompok, seperti terjadi pada run NAT-S22 (6/6 tipis dan
   12/12 kontras gaya melebur jadi satu angka 18/18).
4. **Rujukan bukti.** Kunci pasangan, sumber per sampel, dan transkrip scanner per sampel
   disimpan bersama hasil juri agar rekonsiliasi hilir dapat memeriksa sampel yang lolos
   scanner total namun dipilih juri (kelas temuan S-09/S-18 pemicu NAT-HIL-E1).

Dasar: `juri-hasils.md` seksi 5 (kontrol NAT-S22), `juri-pasangan-kunci.json`, dan putusan
NAT-S23 atas kandidat NAT-HIL-E3 (`contract.md` seksi rekonsiliasi, disposition S22).

## 7. Pointer rumah asal (reference-don't-duplicate: jangan menyalin isinya ke sini)

| Rumah | Isi yang tinggal di sana | Lokasi |
|---|---|---|
| Module H | Aturan lengkap voice/kalimat/paragraf/kosakata/angka GSP (H.1-H.7) | `$LOCALAPPDATA/hermes/skills/gsp/gsp-document-quality-standards/SKILL.md:594-923` |
| Humanizer engine | Taksonomi 34 pola jejak AI, v2.5.1, MIT @blader (dikutip, tidak disalin, engine read-only D14) | `$LOCALAPPDATA/hermes/skills/creative/humanizer/SKILL.md` |
| Matriks sweep | Metode scan per format, aturan penggantian, kontrol merah-hijau, pola klaim cakupan | `$LOCALAPPDATA/hermes/skills/gsp/gsp-verification-before-completion/references/ai-footprint-sweep.md` |
| Spesifikasi RT | Definisi operasional penuh, tabel A1-A7/B1-B9 + ambang, kriteria S/C | `workspace/docs/2026-09-02-naturalisasi-output/identification/01_translated.md` |
| Blueprint TA + adopsi SM | DAG 30 langkah, D-TA-01..D-TA-10, basis profil resmi 53 | `workspace/docs/2026-09-02-naturalisasi-output/identification/02_structured.md` + `contract.md` seksi 4b |

## Verification (kriteria blueprint langkah 8)
- Berkas ada di `references/kebijakan-naturalisasi.md` dengan struktur FLAT skill.
- Ketujuh pengecualian P-1..P-7 tercantum semua (satu per baris tabel seksi 2).
- Contoh positif dan negatif A1-A7 hadir (seksi 5), karakter disebut via nama kode titik.
- Tidak menduplikasi isi Module H / humanizer: hanya pointer (seksi 7).
- Syarat metodologi uji juri NAT-HIL-E3 hadir (seksi 6; kartu `t_c79b5f6d`).
- Prosa bebas literal U+2014 dan U+00B7 (count 0); U+2013 tidak muncul sebagai literal di luar pola rentang.
