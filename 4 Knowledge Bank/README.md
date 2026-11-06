# 4 Knowledge Bank

## Tujuan

Folder ini menyimpan pengetahuan teknis dan catatan pustaka yang dipakai saat menyusun
dokumen rekayasa, menjawab pertanyaan "berapa angkanya dan dari mana", serta menelusuri
keputusan dan pelajaran lama. Isinya empat bagian:

- `ekas-lapis-teks/`: lapis teks EKAS (Engineering Knowledge & Assurance System). Isinya
  aturan tingkat sumber R1-R5, register, kartu rujukan, resume buku, rantai jaminan per
  domain, contoh proyek, templat, dan perkakas. Berkas PDF sumbernya tidak ikut; yang ada
  adalah pengetahuan yang sudah diekstrak beserta nomor halaman PDF-nya.
- `indeks-pengetahuan/`: indeks rute ke unit pengetahuan dan kemampuan EKAS.
- `katalog-docs/`: berkas JSON kerja dari pembangunan ulang Information Library.
- `wiki-information-library/`: objek wiki yang sudah dipromosikan, dikelompokkan menurut
  jenisnya.

Panduan ini menunjukkan letak aturan dan pengetahuan sampai ke berkas dan bagiannya.
Panduan ini bukan inventaris. Daftar lengkap berkas ada di [INDEKS.md](INDEKS.md), dan
INDEKS.md dicari, tidak dibaca utuh.

## Struktur subfolder

| Folder | Isi | Sifat |
|---|---|---|
| `ekas-lapis-teks/00_START-HERE/` | Pintu masuk EKAS: README dengan enam aturan, peta sistem, kendali dokumen, riwayat pembangunan rak, temuan uji coba contoh P00 | Pengetahuan |
| `ekas-lapis-teks/01_GOVERNANCE/` | Aturan main: R1-R5, status otoritas sumber, alur jaminan lima mata rantai, gate G0-G7, kebijakan pemakaian model bahasa, prosedur menambah sumber | Pengetahuan |
| `ekas-lapis-teks/02_REGISTERS/` | Register CSV (rujukan, celah, kebutuhan, keputusan desain, perhitungan, uji, bukti, aset), register kemampuan, antrean intake, dan berkas penjelas `.md` | Pengetahuan dan proyek |
| `ekas-lapis-teks/03_SOURCE-VAULT/` | Laci sumber per tingkat R1-R5. Hanya `_ISI.md` tiap laci yang ada; PDF-nya tidak ikut | Penunjuk letak |
| `ekas-lapis-teks/04_KNOWLEDGE-CARDS/` | Satu kartu per rujukan, dikelompokkan per domain: apa yang dipasok, boleh tidaknya menetapkan ambang, batas pemakaian | Pengetahuan |
| `ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/` | Per domain: `RANTAI-JAMINAN.md`, resume buku bertanda tingkat R pada nama berkas, dan pada sebagian domain `KEMAMPUAN.md` serta `README.md` | Pengetahuan |
| `ekas-lapis-teks/06_ENGINEERING/` | Kebutuhan, keputusan desain, perhitungan, asumsi, tinjauan desain. Memuat katalog rumus induk, asumsi baku, dan contoh P00 | Pekerjaan proyek |
| `ekas-lapis-teks/07_VERIFICATION-VALIDATION/` | Kriteria terima, ITP, prosedur uji, FAT, SAT, ketidaksesuaian. Memuat ambang terima induk dan templat berita acara uji | Pekerjaan proyek |
| `ekas-lapis-teks/08_EVIDENCE/` | Laci bukti mentah per jenis (sertifikat, kelistrikan, pembumian, ukur, OLTS, OTDR, foto, log) beserta aturan tiap laci, dan arsip `BUKUV3/` | Pekerjaan proyek |
| `ekas-lapis-teks/09_HANDOVER/` | Serah terima: as-built, daftar aset, berita acara, cadangan konfigurasi, manual O&M, hasil uji, pelatihan | Pekerjaan proyek |
| `ekas-lapis-teks/10_TEMPLATES/` | Templat isian TPL-00 sampai TPL-09 | Pengetahuan |
| `ekas-lapis-teks/90_TOOLS/` | Skrip Python pembangun dan pemeriksa rak, laporan migrasi, README paket ekspor. Dibaca, tidak dijalankan | Kode arsip |
| `indeks-pengetahuan/` | CSV rute domain, kemampuan, dan unit; `META.json`; satu catatan pelajaran | Indeks |
| `katalog-docs/` | `classification.json` dan `rebuild-manifest.json` | Berkas kerja |
| `wiki-information-library/` | Folder kategori `catatans`, `faktas`, `keputusans`, `pelajarans`, `produks`, `proyeks`, `standars`, `vendors` | Wiki, tanpa katalog |

EKAS membedakan dua jenis folder. Folder 01-05 dan 10 berisi pengetahuan lintas proyek,
sedangkan folder 06-09 diisi per proyek ([peta sistem](ekas-lapis-teks/00_START-HERE/EKAS-SYSTEM-MAP.md),
bagian "Dua jenis folder dan cara memakainya"). Angka proyek ditulis di folder proyek,
bukan di folder pengetahuan.

## Peta topik

### Aturan dan tata kelola EKAS (00, 01)

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Aturan wajib saat memakai paket teks: penanda R, rak R1 kosong, bentuk jawaban bila sumber tidak ada, rantai yang putus, buku berbasis standar Amerika | [BACA-DULU.md](ekas-lapis-teks/BACA-DULU.md) | Aturan yang WAJIB diikuti saat memakai paket ini (butir 1-5) |
| Tingkat sumber R1-R5 dan enam aturan yang tidak boleh dilanggar | [README EKAS](ekas-lapis-teks/00_START-HERE/README.md) | Enam aturan yang tidak boleh dilanggar; Batas yang harus diketahui pemakai |
| Definisi R1-R5, tingkat minimum per jenis keluaran, empat larangan, penurunan mutu karena usia, cara menulis penanda `[R2, sumber, tabel, PDF n]` | [REFERENCE-CONFIDENCE-LEVEL.md](ekas-lapis-teks/01_GOVERNANCE/REFERENCE-CONFIDENCE-LEVEL.md) | Definisi; Aturan pemakaian menurut jenis keluaran; Empat larangan; Penanda dalam dokumen |
| Apa isi tiap folder EKAS dan alur satu pekerjaan dari kebutuhan sampai serah | [EKAS-SYSTEM-MAP.md](ekas-lapis-teks/00_START-HERE/EKAS-SYSTEM-MAP.md) | Rincian tiap folder; Alur satu pekerjaan, dari awal sampai serah |
| Kapan sebuah butir boleh dinyatakan selesai (G0 sumber tervalidasi sampai G7 diterima) | [ASSURANCE-GATES.md](ekas-lapis-teks/01_GOVERNANCE/ASSURANCE-GATES.md) | Delapan gate; Aturan yang mengikat seluruh gate |
| Lima mata rantai rujukan, keputusan, hitungan, uji, bukti serah; kartu kendali | [ASSURANCE-WORKFLOW.md](ekas-lapis-teks/01_GOVERNANCE/ASSURANCE-WORKFLOW.md) | Lima mata rantai; Aturan tingkat pada tiap mata rantai; Kartu kendali rantai |
| Status otoritas sumber (`ACTIVE_WITH_SCOPE_LIMITS`, `POINTER_ONLY`, `INTAKE_ONLY`, `SUPERSEDED`) | [AUTHORITY-STATUS.md](ekas-lapis-teks/01_GOVERNANCE/AUTHORITY-STATUS.md) | Enam status; Peringatan usia |
| Batas pekerjaan model bahasa di EKAS: boleh, tidak boleh, penandaan, konflik antarsumber, yang wajib diperiksa manusia | [AI-USAGE-POLICY.md](ekas-lapis-teks/01_GOVERNANCE/AI-USAGE-POLICY.md) | Boleh; Tidak boleh; Bila model tidak menemukan sumbernya; Yang wajib diperiksa manusia |
| Menambah buku ke rak: OCR, daftar isi, penamaan, kerangka resume | [SOURCE-UPDATE-PROCEDURE.md](ekas-lapis-teks/01_GOVERNANCE/SOURCE-UPDATE-PROCEDURE.md) | Langkah 0-4 |
| Penomoran dokumen, kode domain pada `REF-`, versi, keadaan migrasi | [DOCUMENT-CONTROL.md](ekas-lapis-teks/00_START-HERE/DOCUMENT-CONTROL.md) | Penomoran; Kode domain pada `REF-`; Keadaan migrasi |
| Temuan saat perangkat gate diuji pada contoh P00 | [TEMUAN-UJI-COBA-P00.md](ekas-lapis-teks/00_START-HERE/TEMUAN-UJI-COBA-P00.md) | Lima temuan |
| Riwayat pembangunan rak (OCR, bookmark, kebersihan koleksi) | [CHANGELOG.md](ekas-lapis-teks/00_START-HERE/CHANGELOG.md) | P0-P3 |

### Register (02)

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Arti tiap register, siapa yang mengisi, kolom yang paling menentukan, kaidah nama domain | [README register](ekas-lapis-teks/02_REGISTERS/README.md) | Tabel register; Kaidah domain |
| Daftar seluruh rujukan dengan `r_level`, domain, `vault_path`, `resume_path`, `authority_status`, `may_set_acceptance` | [MASTER-REFERENCE-REGISTER.csv](ekas-lapis-teks/02_REGISTERS/MASTER-REFERENCE-REGISTER.csv) dan penjelasnya [MASTER-REFERENCE-REGISTER.md](ekas-lapis-teks/02_REGISTERS/MASTER-REFERENCE-REGISTER.md) | Penjelas: bagian R1 sampai R5; Ringkasan sebaran dan artinya |
| Register celah: sumber yang tidak ada, tingkat R yang hilang, dampak, prioritas | [GAP-REGISTER.md](ekas-lapis-teks/02_REGISTERS/GAP-REGISTER.md) dan [GAP-REGISTER.csv](ekas-lapis-teks/02_REGISTERS/GAP-REGISTER.csv) | `.md`: Yang sudah tertutup rapat; Celah yang berdampak langsung pada pekerjaan (prioritas tinggi, menengah, rendah). `.csv`: kolom `gap_id`, `missing_r_level`, `status` |
| Rencana pengadaan bahan untuk menutup celah | [GAP-ACQUISITION-PLAN.md](ekas-lapis-teks/02_REGISTERS/GAP-ACQUISITION-PLAN.md) | Urutan prioritas; Yang harus dilakukan saat bahan tiba |
| Register bukti: `evidence_id`, `test_id`, jenis bukti, path berkas, nomor BA | [EVIDENCE-REGISTER.csv](ekas-lapis-teks/02_REGISTERS/EVIDENCE-REGISTER.csv) | Kepala kolom, baris 1 |
| Register perhitungan: rumus, sumber rumus, masukan, `input_tags` (`SOURCE-DERIVED`, `PROJECT-DERIVED`, `OEM-DERIVED`, `ASSUMPTION`) | [CALCULATION-REGISTER.csv](ekas-lapis-teks/02_REGISTERS/CALCULATION-REGISTER.csv) | Kepala kolom, baris 1; baris contoh P00 |
| Register keputusan desain: keputusan, alasan, rujukan, `r_level`, alternatif yang ditolak | [DESIGN-DECISION-REGISTER.csv](ekas-lapis-teks/02_REGISTERS/DESIGN-DECISION-REGISTER.csv) | Kepala kolom, baris 1 |
| Register kebutuhan, uji (dengan `criterion_source` dan `r_level`), dan aset (dengan `interval_basis`) | [REQUIREMENT-REGISTER.csv](ekas-lapis-teks/02_REGISTERS/REQUIREMENT-REGISTER.csv), [TEST-REGISTER.csv](ekas-lapis-teks/02_REGISTERS/TEST-REGISTER.csv), [ASSET-REFERENCE-REGISTER.csv](ekas-lapis-teks/02_REGISTERS/ASSET-REFERENCE-REGISTER.csv) | Kepala kolom, baris 1 |
| Register kemampuan (paket kalkulator per skill, jumlah rumus dan uji, status sign-off) | [KEMAMPUAN-REGISTER.csv](ekas-lapis-teks/02_REGISTERS/KEMAMPUAN-REGISTER.csv) | Kolom `status`, `signoff_status`, `sumber_halaman` |
| Antrean intake hasil triase mesin dan ringkasannya | [INTAKE-QUEUE.csv](ekas-lapis-teks/02_REGISTERS/INTAKE-QUEUE.csv), [INTAKE-RINGKAS.md](ekas-lapis-teks/02_REGISTERS/INTAKE-RINGKAS.md) | CSV: baris 1 komentar metode, header pada baris 2. Ringkas: Cara memakai; Batas alat ini |
| Status penyaringan kandidat R3 dan butir "menunggu data pabrikan" R4 | [R3-STATUS.md](ekas-lapis-teks/02_REGISTERS/R3-STATUS.md), [R4-STATUS.md](ekas-lapis-teks/02_REGISTERS/R4-STATUS.md) | R3: Diserap; Sengaja dilewati. R4: Butir yang MASIH TERBUKA; Peringatan pemakaian |

### Laci sumber (03)

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Laci R1 (regulasi nasional: PUIL, SNI, SKKNI, Permenaker, regulasi lain), semuanya kosong dan memuat aturan bahwa tingkat R ditentukan penerbit, bukan topik | [_ISI.md laci PUIL](ekas-lapis-teks/03_SOURCE-VAULT/R1_NATIONAL-NORMATIVE/PUIL/_ISI.md), [_ISI.md laci SNI](ekas-lapis-teks/03_SOURCE-VAULT/R1_NATIONAL-NORMATIVE/SNI/_ISI.md) | Seluruh isi (pendek) |
| Laci R2 standar internasional (IEC, IEEE, EN-BS, ANSI-NETA, ISO-IEC, TIA, ITU-T) | [_ISI.md laci IEC](ekas-lapis-teks/03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/IEC/_ISI.md), [_ISI.md laci ANSI-NETA](ekas-lapis-teks/03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/ANSI-NETA/_ISI.md) | Seluruh isi |
| Laci R3 buku teks per topik, R4 dokumentasi pabrikan per jenis perangkat, R5 tesis, makalah, panduan | [_ISI.md laci R3 serat optik](ekas-lapis-teks/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/FIBER-OPTIC/_ISI.md), [_ISI.md laci R4 perlu diperiksa](ekas-lapis-teks/03_SOURCE-VAULT/R4_OEM-TECHNICAL/_PERLU-DIPERIKSA/_ISI.md), [_ISI.md laci R5 tesis](ekas-lapis-teks/03_SOURCE-VAULT/R5_RESEARCH-SECONDARY/THESIS/_ISI.md) | Seluruh isi; laci lain dicari di INDEKS.md |

### Pengetahuan per domain (05)

Mulai dari `RANTAI-JAMINAN.md` domain, bukan dari resume ([peta sistem](ekas-lapis-teks/00_START-HERE/EKAS-SYSTEM-MAP.md),
bagian "`05_DOMAIN-KNOWLEDGE/` — pengetahuan per domain"). Tiap rantai punya mata ① Rujukan,
② Keputusan desain, ③ Perhitungan, ④ Pengujian, ⑤ Bukti serah. Kolom Bagian menyebut
subbagian mata ③ yang memuat rumus, dan keadaan mata ④. `KEMAMPUAN.md` adalah digest
mesin dari register kemampuan (lihat Jebakan butir 4).

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Jalur serat optik: loss budget, ambang rugi sisipan dari hitungan rancangan, metode uji IEC 61280-4-2 | [rantai FIBER-OPTIC](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/FIBER-OPTIC/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/FIBER-OPTIC/KEMAMPUAN.md), [resume R2 IEC 61280-4-2](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/FIBER-OPTIC/R2%20-%20IEC%2061280-4-2.md) | ③ Perhitungan: Contoh terhitung; ④ Pengujian |
| Sistem pengawasan video: panjang fokus lensa, kerapatan piksel sasaran, kapasitas rekaman; transmisi dari BS EN 62676-1-2 | [rantai VIDEO-SURVEILLANCE](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/KEMAMPUAN.md), [resume R2 BS EN 62676-1-2](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/R2%20-%20BS%20EN%2062676-1-2.md) | ③: Panjang fokus lensa; Kerapatan piksel sasaran; Kapasitas rekaman |
| Catu daya cadangan: kapasitas baterai, rugi daya dan beban pendinginan UPS, ventilasi ruang baterai, kapasitas genset, interval uji fungsi tersembunyi | [rantai POWER-BACKUP](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/POWER-BACKUP/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/POWER-BACKUP/KEMAMPUAN.md), [resume R2 IEEE 1188 dan IEC 62485-2](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/POWER-BACKUP/R2%20-%20IEEE%201188-2005%20dan%20IEC%2062485-2.md), [resume genset diesel](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/POWER-BACKUP/R3%20-%20Diesel%20Generator%20Handbook.md) | ③: Kapasitas baterai; Rugi daya & beban pendinginan UPS; Ventilasi ruang baterai; Kapasitas genset |
| Uji instalasi listrik (tahanan isolasi): polarization index, dielectric absorption ratio, batas tegangan uji, koreksi ke suhu acuan; ambang ANSI/NETA ATS-2017 | [rantai ELECTRICAL](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/ELECTRICAL/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/ELECTRICAL/KEMAMPUAN.md), [resume R2 ANSI-NETA ATS-2017](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/ELECTRICAL/R2%20-%20ANSI-NETA%20ATS-2017.md) | ③: Polarization Index; Dielectric Absorption Ratio; Koreksi ke suhu acuan |
| Termografi: delapan parameter wajib, aturan IFOV, uji pantulan, perhitungan ΔT; ambang ANSI/NETA Tabel 100.18 | [rantai THERMAL](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/THERMAL/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/THERMAL/KEMAMPUAN.md), [resume citra termal inframerah](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/THERMAL/R3%20-%20Infrared%20Thermal%20Imaging.md) | ③ Perhitungan dan prasyarat ukur |
| Pembumian dan proteksi petir: resistivitas tanah metode Wenner, rolling sphere. Rantai putus di ④: ambang resistansi pembumian tidak ada di rak | [rantai GROUNDING-LIGHTNING](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/GROUNDING-LIGHTNING/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/GROUNDING-LIGHTNING/KEMAMPUAN.md), [resume pembumian](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/GROUNDING-LIGHTNING/R3%20-%20Grounds%20for%20Grounding.md), [resume proteksi petir](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/GROUNDING-LIGHTNING/R3%20-%20The%20Art%20and%20Science%20of%20Lightning%20Protection.md) | ③: Resistivitas tanah; Rolling sphere; Jangan tertukar. ④ MATA YANG PUTUS; Cara menutup rantai ini |
| Keandalan dan program pemeliharaan: interval on-condition, interval failure-finding (bentuk sederhana dan lengkap); ambang dari sasaran risiko pemilik | [rantai RCM](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/RCM/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/RCM/KEMAMPUAN.md) | ③: Interval pemeriksaan on-condition; Interval failure-finding |
| Penyimpanan: kapasitas setelah RAID, bandwidth-delay product; tanpa standar normatif di rak | [rantai STORAGE](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/STORAGE/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/STORAGE/KEMAMPUAN.md), [resume jaringan penyimpanan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/STORAGE/R3%20-%20Storage%20Networks%20Explained.md) | ③: Kapasitas setelah RAID; Bandwidth-Delay Product |
| Jaringan IP untuk sistem terpasang: lebar pita agregat, anggaran PoE, bandwidth-delay product | [rantai NETWORKING](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/NETWORKING/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/NETWORKING/KEMAMPUAN.md), [resume TCP/IP](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/NETWORKING/R3%20-%20TCP-IP%20Illustrated%20Vol%201.md) | ③: Kebutuhan lebar pita agregat; Anggaran PoE; Bandwidth-Delay Product |
| Keamanan siber dan penanganan bukti digital. Rantai putus di ④: tidak ada R1 atau R2 keamanan siber di rak | [rantai CYBERSECURITY](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/CYBERSECURITY/RANTAI-JAMINAN.md) | ④ MATA YANG PUTUS; Yang boleh dan tidak boleh dikatakan; Cara menutup rantai ini |
| Perlindungan siber objek vital (infrastruktur kritis); ④ tanpa ambang | [rantai CRITICAL-INFRASTRUCTURE](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/CRITICAL-INFRASTRUCTURE/RANTAI-JAMINAN.md), [resume](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/CRITICAL-INFRASTRUCTURE/R3%20-%20Cybersecurity%20Protecting%20Critical%20Infrastructures.md) | ④: Celah yang dibukukan; Yang boleh dan tidak boleh dikatakan |
| Struktur penopang perangkat: urutan hitung, beban yang wajib diperhitungkan. Rantai putus di ④ (SNI struktur tidak ada); hitungan keselamatan wajib ditandatangani ahli bersertifikat | [rantai CIVIL-STRUCTURAL](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/CIVIL-STRUCTURAL/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/CIVIL-STRUCTURAL/KEMAMPUAN.md) | ③: Urutan yang benar; Beban yang wajib diperhitungkan. ④: Tiga jalan sah selama SNI belum ada |
| Batasan bangunan tempat perangkat dipasang: struktur balik permukaan, penetrasi sekat tahan api. Angka ambang di rak berasal dari kode bangunan AS | [rantai BUILDING-CONSTRUCTION](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/BUILDING-CONSTRUCTION/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/BUILDING-CONSTRUCTION/KEMAMPUAN.md) | Mata 2 - Keputusan desain; Mata 3 - Perhitungan - BATAS KONTEKS; Mata 4 - MATA YANG PUTUS |
| Pelaksanaan konstruksi, taksiran biaya, penjadwalan (CPM, perataan sumber daya). Putus di mata 4: tidak ada R1/R2 untuk harga satuan dan norma produktivitas | [rantai CONSTRUCTION](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/CONSTRUCTION/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/CONSTRUCTION/KEMAMPUAN.md) | Mata 1 - Rujukan; Mata 3 - Perhitungan; Mata 4 - MATA YANG PUTUS |
| Mutu, audit, dan kendali dokumen; rantai ini melingkupi rantai lain, bukan satu besaran | [rantai PROJECT-QUALITY](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/PROJECT-QUALITY/RANTAI-JAMINAN.md) | Rantai ini berbeda bentuknya; ④ Pengujian (berupa audit); Kaitan ke rantai lain |
| Bangunan tempat sistem bekerja: daya gedung, pendinginan ruang perangkat, proteksi kebakaran | [rantai HVAC-BUILDING](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/HVAC-BUILDING/RANTAI-JAMINAN.md) | ③ Perhitungan; ④ Pengujian; Status rantai |
| Perhitungan mekanikal: dudukan, komponen mesin, fluida, termal | [rantai MECHANICAL](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/MECHANICAL/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/MECHANICAL/KEMAMPUAN.md) | ③: Inventaris metode terakun; Bentuk hitung yang mengikat |
| Operasi layanan dan sistem padat data (arsip video, VMS/NVR, monitoring): anggaran downtime dari SLO, kapasitas arsip | [rantai SOFTWARE-DATA](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/SOFTWARE-DATA/RANTAI-JAMINAN.md) | ③: Anggaran downtime dari SLO; Bentuk SLO yang sah dikutip; Kerangka kapasitas arsip |
| Rekayasa sistem: kebutuhan, arsitektur, trade study skor berbobot, probabilitas keberhasilan rantai antarmuka | [rantai SYSTEMS-ENGINEERING](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/SYSTEMS-ENGINEERING/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/SYSTEMS-ENGINEERING/KEMAMPUAN.md), [README domain](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/SYSTEMS-ENGINEERING/README.md) | ③: Skor berbobot (trade study); Probabilitas keberhasilan rantai antarmuka |
| Gambar kerja dan set serah: kaidah, susunan set, penyajian, alat produksi CAD | [rantai DRAWING-CAD](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/DRAWING-CAD/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/DRAWING-CAD/KEMAMPUAN.md) | ② Keputusan desain; ④ Pengujian |
| Survei dan pemetaan: kurvatur dan refraksi, arithmetic check leveling, precision ratio traversi, compass rule | [rantai GEOSPATIAL-SURVEY](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/GEOSPATIAL-SURVEY/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/GEOSPATIAL-SURVEY/KEMAMPUAN.md) | ③: butir 1-5; ④ MATA TANPA AMBANG SAH |
| Tautan radio dan gelombang mikro: rugi lintasan ruang bebas, persamaan Friis, pencocokan feeder, kapasitas kanal | [rantai RF-WIRELESS](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/RF-WIRELESS/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/RF-WIRELESS/KEMAMPUAN.md), [README domain](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/RF-WIRELESS/README.md) | ③: Rugi lintasan ruang bebas; Persamaan transmisi Friis; Metrik pencocokan feeder; Kapasitas kanal |
| Metode numerik sebagai mesin hitung domain lain: anggaran iterasi bisection | [rantai NUMERICAL-METHODS](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/NUMERICAL-METHODS/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/NUMERICAL-METHODS/KEMAMPUAN.md), [README domain](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/NUMERICAL-METHODS/README.md) | ③: Anggaran iterasi bisection; Contoh terhitung |
| Pengolahan dan analisis citra untuk analitik video: geometri multi-pandang, pengolahan citra digital | [rantai COMPUTER-VISION](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/COMPUTER-VISION/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/COMPUTER-VISION/KEMAMPUAN.md), [README domain](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/COMPUTER-VISION/README.md) | ③: Geometri (MVG); Pengolahan citra (DIP) |
| Pembelajaran mesin untuk analitik dan otomasi: metrik utama tertambat halaman | [rantai AI-ML](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/AI-ML/RANTAI-JAMINAN.md), [kemampuan](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/AI-ML/KEMAMPUAN.md), [README domain](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/AI-ML/README.md) | ③: Metrik utama yang tertambat halaman; Contoh terhitung |

Domain tanpa rantai bawaan yang mengikat (mata ④ "tanpa ambang") tetap boleh dipakai untuk
metode dan hitungan. Yang tidak boleh adalah menyatakan lulus dari rak.

### Kartu rujukan (04)

Satu kartu per rujukan, nama berkas = ID rujukan. Semua kartu memuat bagian "Boleh
menetapkan ambang terima?" dan "Batas pemakaian"; nomor bagiannya berbeda antarkartu. Kartu
rujukan pabrikan (`REF-OEM-*`) adalah penunjuk lembar data R4 per proyek. Buka kartu sebelum
mengutip angka dari sebuah resume.

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Serat optik: panduan rujukan, panduan pengujian, IEC 61280-4-2, komunikasi serat optik | [REF-FO-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/FIBER-OPTIC/REF-FO-001.md), [REF-FO-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/FIBER-OPTIC/REF-FO-002.md), [REF-FO-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/FIBER-OPTIC/REF-FO-003.md), [REF-FO-004](ekas-lapis-teks/04_KNOWLEDGE-CARDS/FIBER-OPTIC/REF-FO-004.md) | Yang dipasok; Rumus / metode; Batas pemakaian |
| Pengawasan video: CCTV, BS EN 62676-1-2, video digital, algoritma visi komputer, lembar data kamera dan PTZ, lembar data NVR/VMS | [REF-VSS-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-VSS-001.md), [REF-VSS-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-VSS-002.md), [REF-VSS-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-VSS-003.md), [REF-VAI-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-VAI-001.md), [REF-OEM-CAM](ekas-lapis-teks/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-OEM-CAM.md), [REF-OEM-VMS](ekas-lapis-teks/04_KNOWLEDGE-CARDS/VIDEO-SURVEILLANCE/REF-OEM-VMS.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Catu daya cadangan: buku rujukan baterai, IEEE 1188 dan IEC 62485-2, genset diesel, UPS dan filter aktif, katalog UPS pabrikan | [REF-BAT-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/POWER-BACKUP/REF-BAT-001.md), [REF-BAT-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/POWER-BACKUP/REF-BAT-002.md), [REF-PWR-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/POWER-BACKUP/REF-PWR-001.md), [REF-PWR-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/POWER-BACKUP/REF-PWR-002.md), [REF-OEM-UPS](ekas-lapis-teks/04_KNOWLEDGE-CARDS/POWER-BACKUP/REF-OEM-UPS.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Kelistrikan: pemeliharaan dan pengujian peralatan daya, ANSI/NETA ATS-2017, prinsip teknik elektro, analisis dan desain sistem tenaga, elektronika, proteksi dan relai, distribusi daya, mesin listrik | [REF-ELC-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/ELECTRICAL/REF-ELC-001.md), [REF-ELC-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/ELECTRICAL/REF-ELC-002.md), [REF-ELC-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/ELECTRICAL/REF-ELC-003.md), [REF-ELC-004](ekas-lapis-teks/04_KNOWLEDGE-CARDS/ELECTRICAL/REF-ELC-004.md), [REF-ELC-005](ekas-lapis-teks/04_KNOWLEDGE-CARDS/ELECTRICAL/REF-ELC-005.md), [REF-ELC-006](ekas-lapis-teks/04_KNOWLEDGE-CARDS/ELECTRICAL/REF-ELC-006.md), [REF-ELC-007](ekas-lapis-teks/04_KNOWLEDGE-CARDS/ELECTRICAL/REF-ELC-007.md), [REF-ELC-008](ekas-lapis-teks/04_KNOWLEDGE-CARDS/ELECTRICAL/REF-ELC-008.md), [REF-ELC-009](ekas-lapis-teks/04_KNOWLEDGE-CARDS/ELECTRICAL/REF-ELC-009.md), [REF-ELC-010](ekas-lapis-teks/04_KNOWLEDGE-CARDS/ELECTRICAL/REF-ELC-010.md), [REF-ELC-011](ekas-lapis-teks/04_KNOWLEDGE-CARDS/ELECTRICAL/REF-ELC-011.md), [REF-ELC-012](ekas-lapis-teks/04_KNOWLEDGE-CARDS/ELECTRICAL/REF-ELC-012.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Termografi: citra termal inframerah | [REF-THM-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/THERMAL/REF-THM-001.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Pembumian dan proteksi petir | [REF-GRD-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/GROUNDING-LIGHTNING/REF-GRD-001.md), [REF-LPS-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/GROUNDING-LIGHTNING/REF-LPS-001.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Keandalan dan pemeliharaan: praktik terbaik, perencanaan dan penjadwalan, RCM II, rekayasa keandalan | [REF-RCM-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/RCM/REF-RCM-001.md), [REF-RCM-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/RCM/REF-RCM-002.md), [REF-RCM-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/RCM/REF-RCM-003.md), [REF-RCM-004](ekas-lapis-teks/04_KNOWLEDGE-CARDS/RCM/REF-RCM-004.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Penyimpanan: jaringan penyimpanan, lembar data server, SSD, komputer tepi | [REF-STG-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/STORAGE/REF-STG-001.md), [REF-OEM-STG](ekas-lapis-teks/04_KNOWLEDGE-CARDS/STORAGE/REF-OEM-STG.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Jaringan: operasional jaringan, CCNA, jaringan komputer top-down, TCP/IP, administrasi sistem dan jaringan, lembar data perangkat jaringan, PBX, interkom | [REF-NET-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/NETWORKING/REF-NET-001.md), [REF-NET-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/NETWORKING/REF-NET-002.md), [REF-NET-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/NETWORKING/REF-NET-003.md), [REF-NET-004](ekas-lapis-teks/04_KNOWLEDGE-CARDS/NETWORKING/REF-NET-004.md), [REF-OPS-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/NETWORKING/REF-OPS-001.md), [REF-OEM-NET](ekas-lapis-teks/04_KNOWLEDGE-CARDS/NETWORKING/REF-OEM-NET.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Keamanan siber: kerangka NICE, security engineering, keamanan siber operasional, keamanan siber dan forensik digital (R5) | [REF-SEC-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CYBERSECURITY/REF-SEC-001.md), [REF-SEC-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CYBERSECURITY/REF-SEC-002.md), [REF-SEC-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CYBERSECURITY/REF-SEC-003.md), [REF-SEC-004](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CYBERSECURITY/REF-SEC-004.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Infrastruktur kritis | [REF-CIP-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CRITICAL-INFRASTRUCTURE/REF-CIP-001.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Sipil dan struktur: analisis struktur, struktur beton, desain baja (profil AS), material, mekanika bahan, statika, dinamika | [REF-CIV-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CIVIL-STRUCTURAL/REF-CIV-001.md), [REF-CIV-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CIVIL-STRUCTURAL/REF-CIV-002.md), [REF-CIV-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CIVIL-STRUCTURAL/REF-CIV-003.md), [REF-CIV-004](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CIVIL-STRUCTURAL/REF-CIV-004.md), [REF-CIV-005](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CIVIL-STRUCTURAL/REF-CIV-005.md), [REF-CIV-006](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CIVIL-STRUCTURAL/REF-CIV-006.md), [REF-CIV-007](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CIVIL-STRUCTURAL/REF-CIV-007.md), [REF-CIV-008](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CIVIL-STRUCTURAL/REF-CIV-008.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Bangunan: konstruksi bangunan bergambar, BIM, kode bangunan bergambar (IBC) | [REF-BLD-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/BUILDING-CONSTRUCTION/REF-BLD-001.md), [REF-BLD-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/BUILDING-CONSTRUCTION/REF-BLD-002.md), [REF-BLD-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/BUILDING-CONSTRUCTION/REF-BLD-003.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Konstruksi: perencanaan, alat dan metode; estimasi biaya; penjadwalan dan pengendalian | [REF-CON-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CONSTRUCTION/REF-CON-001.md), [REF-CON-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CONSTRUCTION/REF-CON-002.md), [REF-CON-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/CONSTRUCTION/REF-CON-003.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Mutu proyek: manajemen proyek rekayasa, manajemen dan audit mutu konstruksi, kendali dokumen rekayasa | [REF-PRQ-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/PROJECT-QUALITY/REF-PRQ-001.md), [REF-PRQ-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/PROJECT-QUALITY/REF-PRQ-002.md), [REF-PRQ-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/PROJECT-QUALITY/REF-PRQ-003.md), [REF-PRQ-004](ekas-lapis-teks/04_KNOWLEDGE-CARDS/PROJECT-QUALITY/REF-PRQ-004.md), [REF-PRQ-005](ekas-lapis-teks/04_KNOWLEDGE-CARDS/PROJECT-QUALITY/REF-PRQ-005.md), [REF-PRQ-006](ekas-lapis-teks/04_KNOWLEDGE-CARDS/PROJECT-QUALITY/REF-PRQ-006.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Peralatan mekanikal dan elektrikal bangunan | [REF-HVA-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/HVAC-BUILDING/REF-HVA-001.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Mekanikal: desain teknik mesin, handbook teknik mesin, mekanika fluida, manual rujukan teknik mesin, elemen mesin, termodinamika, handbook permesinan | [REF-MEC-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/MECHANICAL/REF-MEC-001.md), [REF-MEC-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/MECHANICAL/REF-MEC-002.md), [REF-MEC-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/MECHANICAL/REF-MEC-003.md), [REF-MEC-004](ekas-lapis-teks/04_KNOWLEDGE-CARDS/MECHANICAL/REF-MEC-004.md), [REF-MEC-005](ekas-lapis-teks/04_KNOWLEDGE-CARDS/MECHANICAL/REF-MEC-005.md), [REF-MEC-006](ekas-lapis-teks/04_KNOWLEDGE-CARDS/MECHANICAL/REF-MEC-006.md), [REF-MEC-007](ekas-lapis-teks/04_KNOWLEDGE-CARDS/MECHANICAL/REF-MEC-007.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Layanan dan data: makalah deep learning, site reliability engineering, aplikasi padat data | [REF-SWD-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/SOFTWARE-DATA/REF-SWD-001.md), [REF-SWD-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/SOFTWARE-DATA/REF-SWD-002.md), [REF-SWD-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/SOFTWARE-DATA/REF-SWD-003.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Rekayasa sistem: prinsip dan praktik, handbook INCOSE, manajemen rekayasa sistem | [REF-SYS-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/SYSTEMS-ENGINEERING/REF-SYS-001.md), [REF-SYS-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/SYSTEMS-ENGINEERING/REF-SYS-002.md), [REF-SYS-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/SYSTEMS-ENGINEERING/REF-SYS-003.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Gambar dan CAD: gambar teknik, grafis arsitektur, gambar kerja arsitektur, AutoCAD Electrical, AutoCAD Civil 3D, dasar gambar teknik | [REF-DRW-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/DRAWING-CAD/REF-DRW-001.md), [REF-DRW-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/DRAWING-CAD/REF-DRW-002.md), [REF-DRW-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/DRAWING-CAD/REF-DRW-003.md), [REF-DRW-004](ekas-lapis-teks/04_KNOWLEDGE-CARDS/DRAWING-CAD/REF-DRW-004.md), [REF-DRW-005](ekas-lapis-teks/04_KNOWLEDGE-CARDS/DRAWING-CAD/REF-DRW-005.md), [REF-DRW-006](ekas-lapis-teks/04_KNOWLEDGE-CARDS/DRAWING-CAD/REF-DRW-006.md), [REF-DRW-007](ekas-lapis-teks/04_KNOWLEDGE-CARDS/DRAWING-CAD/REF-DRW-007.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Survei dan GIS | [REF-GEO-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/GEOSPATIAL-SURVEY/REF-GEO-001.md), [REF-GEO-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/GEOSPATIAL-SURVEY/REF-GEO-002.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Radio dan gelombang mikro: komunikasi nirkabel, teori antena, rekayasa gelombang mikro | [REF-RFW-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/RF-WIRELESS/REF-RFW-001.md), [REF-RFW-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/RF-WIRELESS/REF-RFW-002.md), [REF-RFW-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/RF-WIRELESS/REF-RFW-003.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Metode numerik | [REF-NUM-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/NUMERICAL-METHODS/REF-NUM-001.md), [REF-NUM-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/NUMERICAL-METHODS/REF-NUM-002.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Visi komputer: pengolahan citra digital, geometri multi-pandang | [REF-CVI-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/COMPUTER-VISION/REF-CVI-001.md), [REF-CVI-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/COMPUTER-VISION/REF-CVI-002.md) | Boleh menetapkan ambang terima?; Batas pemakaian |
| Pembelajaran mesin: desain sistem ML produksi, sains berbasis data, ML praktis, deep learning | [REF-AIM-001](ekas-lapis-teks/04_KNOWLEDGE-CARDS/AI-ML/REF-AIM-001.md), [REF-AIM-002](ekas-lapis-teks/04_KNOWLEDGE-CARDS/AI-ML/REF-AIM-002.md), [REF-AIM-003](ekas-lapis-teks/04_KNOWLEDGE-CARDS/AI-ML/REF-AIM-003.md), [REF-AIM-004](ekas-lapis-teks/04_KNOWLEDGE-CARDS/AI-ML/REF-AIM-004.md) | Boleh menetapkan ambang terima?; Batas pemakaian |

### Rekayasa proyek (06)

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Rumus, ambang, dan angka acuan beserta buku dan halaman PDF-nya: optik dan video, serat optik, pembumian, proteksi petir, uji instalasi listrik, keandalan, penyimpanan, baterai, UPS, genset, jaringan, termografi, ambang standar R2 | [KATALOG-RUMUS.md](ekas-lapis-teks/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md) | Indeks cepat — pertanyaan ke rumus (baris 29); bagian 1-13; Yang TIDAK ada di rak ini |
| Asumsi baku bila data tipis, per domain (keandalan, serat optik, pembumian, catu daya, video, penyimpanan), dan asumsi yang dilarang | [ASUMSI-BAKU.md](ekas-lapis-teks/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md) | Tiga aturan; Daftar asumsi menurut domain; Asumsi yang TIDAK boleh dipakai; Asumsi yang GUGUR |
| Contoh lembar hitung dan kartu kendali rantai (proyek contoh P00, angka karangan) | [CALC-P00-001.md](ekas-lapis-teks/06_ENGINEERING/CALCULATIONS/CALC-P00-001.md), [KARTU-P00-001.md](ekas-lapis-teks/06_ENGINEERING/CALCULATIONS/KARTU-P00-001.md) | Seluruh isi; banner CONTOH di baris 1 |
| Contoh catatan keputusan desain dengan alternatif yang ditolak dan konflik antarsumber | [DDR-P00-001.md](ekas-lapis-teks/06_ENGINEERING/DESIGN-DECISIONS/DDR-P00-001.md) | Alternatif yang dipertimbangkan dan ditolak; Konflik antar-sumber |
| Contoh kebutuhan yang dibekukan (gate G1) | [REQ-P00-CONTOH.md](ekas-lapis-teks/06_ENGINEERING/REQUIREMENTS/REQ-P00-CONTOH.md) | Lingkup; Keputusan pemilik yang sudah tertulis |
| Aturan tiap map kerja (perhitungan, keputusan desain, tinjauan desain, kebutuhan, asumsi) | [README perhitungan](ekas-lapis-teks/06_ENGINEERING/CALCULATIONS/README.md), [README keputusan desain](ekas-lapis-teks/06_ENGINEERING/DESIGN-DECISIONS/README.md), [README tinjauan desain](ekas-lapis-teks/06_ENGINEERING/DESIGN-REVIEWS/README.md), [README kebutuhan](ekas-lapis-teks/06_ENGINEERING/REQUIREMENTS/README.md), [README asumsi](ekas-lapis-teks/06_ENGINEERING/ASSUMPTIONS/README.md) | Kutipan "Aturan map ini" |

### Verifikasi dan validasi (07)

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Ambang terima induk beserta tingkat sumbernya: sah dari R2, sah dari hitungan rancangan, perlu adopsi kontrak (R3), belum ada sumber sah, wajib R4 | [AMBANG-TERIMA-INDUK.md](ekas-lapis-teks/07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md) | Sah tanpa syarat — bersumber R2; Perlu adopsi kontrak — bersumber R3; Belum ada sumber sah; Wajib R4; Cara memakai berkas ini |
| Kerangka berita acara untuk delapan jenis uji: serat optik, pembumian, tahanan isolasi, kapasitas baterai, komisioning genset, sistem video, termal, penyimpanan/RAID | [TEMPLATE-BERITA-ACARA.md](ekas-lapis-teks/07_VERIFICATION-VALIDATION/TEST-PROCEDURES/TEMPLATE-BERITA-ACARA.md) | Rangka umum; bagian 1-8; Ringkasan sumber ambang |
| Contoh prosedur uji rugi sisipan (metode, alat, ambang, prasyarat, langkah, pencatatan, penyaksi) | [TEST-P00-001.md](ekas-lapis-teks/07_VERIFICATION-VALIDATION/TEST-PROCEDURES/TEST-P00-001.md) | bagian 1-7 |
| Contoh inspection and test plan | [ITP-P00.md](ekas-lapis-teks/07_VERIFICATION-VALIDATION/ITP/ITP-P00.md) | Prasyarat sebelum uji |
| Aturan FAT, SAT, ITP, NCR, kriteria terima, prosedur uji | [README FAT](ekas-lapis-teks/07_VERIFICATION-VALIDATION/FAT/README.md), [README SAT](ekas-lapis-teks/07_VERIFICATION-VALIDATION/SAT/README.md), [README ITP](ekas-lapis-teks/07_VERIFICATION-VALIDATION/ITP/README.md), [README NCR](ekas-lapis-teks/07_VERIFICATION-VALIDATION/NON-CONFORMANCE/README.md), [README kriteria terima](ekas-lapis-teks/07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/README.md), [README prosedur uji](ekas-lapis-teks/07_VERIFICATION-VALIDATION/TEST-PROCEDURES/README.md) | Kutipan "Aturan map ini" (misalnya lulus FAT tidak menggantikan SAT; NCR ditutup dengan bukti uji ulang) |

### Bukti, serah terima, templat (08, 09, 10)

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Aturan menyimpan bukti mentah per jenis: kalibrasi berlaku pada tanggal uji, suhu saat ukur, konduktor penghubung dilepas, berkas mentah tidak disunting, setelan OTDR, citra termal berpasangan | [README sertifikat](ekas-lapis-teks/08_EVIDENCE/CERTIFICATES/README.md), [README kelistrikan](ekas-lapis-teks/08_EVIDENCE/ELECTRICAL/README.md), [README pembumian](ekas-lapis-teks/08_EVIDENCE/GROUNDING/README.md), [README ukur mentah](ekas-lapis-teks/08_EVIDENCE/MEASUREMENT/README.md), [README OLTS](ekas-lapis-teks/08_EVIDENCE/OLTS/README.md), [README OTDR](ekas-lapis-teks/08_EVIDENCE/OTDR/README.md), [README foto](ekas-lapis-teks/08_EVIDENCE/PHOTO/README.md), [README log](ekas-lapis-teks/08_EVIDENCE/SCREENSHOTS-LOGS/README.md) | Kutipan "Aturan map ini" |
| Arsip `BUKUV3/`: deskriptor korpus pemetaan buku ke skill, metadata latih model lokal, lembar sign-off; tercatat di register bukti | Folder `ekas-lapis-teks/08_EVIDENCE/BUKUV3/`; cari berkasnya di INDEKS.md | Lihat Sensitivitas: berkas asal-usulnya memuat rincian host sumber |
| Contoh berita acara uji jalur serat optik: ambang beserta cara memperolehnya, hasil per core, OTDR, ketidakpastian ukur | [BA-P00-FO-001.md](ekas-lapis-teks/09_HANDOVER/BERITA-ACARA/BA-P00-FO-001.md) | Ambang lulus — beserta cara memperolehnya; Catatan ketidakpastian pengukuran; Lampiran wajib |
| Contoh ketertelusuran kebutuhan ke bukti | [TPL-06-P00-KETERTELUSURAN.md](ekas-lapis-teks/09_HANDOVER/TPL-06-P00-KETERTELUSURAN.md) | Seluruh isi |
| Aturan serah terima: as-built, daftar aset (`interval_basis`), berita acara, cadangan konfigurasi, manual O&M, hasil uji, pelatihan | [README berita acara](ekas-lapis-teks/09_HANDOVER/BERITA-ACARA/README.md), [README daftar aset](ekas-lapis-teks/09_HANDOVER/ASSET-REGISTER/README.md), [README hasil uji](ekas-lapis-teks/09_HANDOVER/TEST-RESULT/README.md), [README manual O&M](ekas-lapis-teks/09_HANDOVER/O&M-MANUAL/README.md), [README as-built](ekas-lapis-teks/09_HANDOVER/AS-BUILT/README.md), [README cadangan konfigurasi](ekas-lapis-teks/09_HANDOVER/CONFIGURATION-BACKUP/README.md), [README pelatihan](ekas-lapis-teks/09_HANDOVER/TRAINING/README.md) | Kutipan "Aturan map ini" |
| Templat isian: kartu kendali, DDR, lembar hitung, prosedur uji, catatan penerimaan, paket bukti serah, ketertelusuran, permintaan pembaruan sumber, ITP, NCR | [TPL-00](ekas-lapis-teks/10_TEMPLATES/TPL-00-KARTU-KENDALI.md), [TPL-01](ekas-lapis-teks/10_TEMPLATES/TPL-01-DESIGN-DECISION-RECORD.md), [TPL-02](ekas-lapis-teks/10_TEMPLATES/TPL-02-CALCULATION-SHEET.md), [TPL-03](ekas-lapis-teks/10_TEMPLATES/TPL-03-TEST-PROCEDURE.md), [TPL-04](ekas-lapis-teks/10_TEMPLATES/TPL-04-ACCEPTANCE-RECORD.md), [TPL-05](ekas-lapis-teks/10_TEMPLATES/TPL-05-HANDOVER-EVIDENCE-PACK.md), [TPL-06](ekas-lapis-teks/10_TEMPLATES/TPL-06-REQUIREMENT-TRACEABILITY.md), [TPL-07](ekas-lapis-teks/10_TEMPLATES/TPL-07-SOURCE-UPDATE-REQUEST.md), [TPL-08](ekas-lapis-teks/10_TEMPLATES/TPL-08-ITP.md), [TPL-09](ekas-lapis-teks/10_TEMPLATES/TPL-09-NCR.md) | Seluruh isi |

### Perkakas EKAS (90), dibaca tanpa dijalankan

Uraian di bawah diambil dari docstring tiap skrip. Skrip tidak dijalankan (lihat Sensitivitas).

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Pemeriksa keutuhan rak: register yang menunjuk berkas hilang, kartu tanpa berkas vault, manifest laci tertinggal, kutipan halaman melebihi jumlah halaman, salinan ganda; hanya melaporkan | [periksa_ekas.py](ekas-lapis-teks/90_TOOLS/periksa_ekas.py) | Docstring modul |
| Triase korpus kandidat menjadi antrean intake berlabel R1-R5 dan kategori teknik (menghasilkan `INTAKE-QUEUE.csv` dan `INTAKE-RINGKAS.md`) | [triase_korpus.py](ekas-lapis-teks/90_TOOLS/triase_korpus.py) | Docstring modul |
| Penyerapan sumber ke laci: R3 dari daftar tulis tangan, R4 dari antrean intake (menyalin, bukan memindahkan); pemindahan PDF ke laci vault | [serap_r3.py](ekas-lapis-teks/90_TOOLS/serap_r3.py), [serap_r4.py](ekas-lapis-teks/90_TOOLS/serap_r4.py), [migrasi_sumber.py](ekas-lapis-teks/90_TOOLS/migrasi_sumber.py) | Docstring modul |
| Pembangun struktur dan lapis dokumen EKAS; pembangun daftar rujukan skill dari register rujukan | [bangun_ekas_struktur.py](ekas-lapis-teks/90_TOOLS/bangun_ekas_struktur.py), [isi_ekas_dokumen.py](ekas-lapis-teks/90_TOOLS/isi_ekas_dokumen.py), [bangun_daftar_skill.py](ekas-lapis-teks/90_TOOLS/bangun_daftar_skill.py) | Docstring modul |
| Pengolahan buku: OCR PDF berbasis gambar, EPUB ke PDF, penarik bahan resume per buku | [ocr_book.py](ekas-lapis-teks/90_TOOLS/ocr_book.py), [epub_ke_pdf.py](ekas-lapis-teks/90_TOOLS/epub_ke_pdf.py), [bahan_resume.py](ekas-lapis-teks/90_TOOLS/bahan_resume.py) | Docstring modul |
| Pembuat paket ekspor (paket induk, batch 2, paket lokal teks, korpus Markdown) dan katalog DOCX | [buat_paket_ekas.py](ekas-lapis-teks/90_TOOLS/buat_paket_ekas.py), [buat_paket_batch2.py](ekas-lapis-teks/90_TOOLS/buat_paket_batch2.py), [buat_paket_lokal.py](ekas-lapis-teks/90_TOOLS/buat_paket_lokal.py), [buat_paket_markdown.py](ekas-lapis-teks/90_TOOLS/buat_paket_markdown.py), [buat_katalog_docx.py](ekas-lapis-teks/90_TOOLS/buat_katalog_docx.py) | Docstring modul |
| Batasan korpus Markdown hasil ekspor; laporan berkas `.md` yang masih menyebut folder lama | [README-ekspor.md](ekas-lapis-teks/90_TOOLS/README-ekspor.md), [LAPORAN-MIGRASI.csv](ekas-lapis-teks/90_TOOLS/LAPORAN-MIGRASI.csv) | README: Batasan yang harus dipahami lebih dulu |

### Indeks, katalog, dan wiki

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Rute domain: per domain, ada tidaknya rantai, jumlah berkas rak, path digest sapuan, catatan | [PETA-DOMAIN.csv](indeks-pengetahuan/PETA-DOMAIN.csv) | Pemisah pipa; kolom `domain`, `rantai`, `digest` |
| Indeks kemampuan: unit `K-*` per domain dengan tingkat R, ringkas, rujukan digest `KEMAMPUAN.md`, kata kunci, status otoritas dan sign-off | [INDEKS-KEMAMPUAN.csv](indeks-pengetahuan/INDEKS-KEMAMPUAN.csv) | Pemisah pipa; kolom `digest`, `signoff_status` |
| Indeks unit: unit `U-*` per bab laporan (C1-C9) dengan ringkas dan kata kunci; rute, bukan bukti | [INDEKS-UNIT.csv](indeks-pengetahuan/INDEKS-UNIT.csv) | Pemisah pipa; kolom `bab`, `ringkas`, `kw` |
| Arti kode bab C1-C9, tanggal bangun indeks, daya ikat indeks kemampuan | [META.json](indeks-pengetahuan/META.json) | Kunci `bab`, `indeks_kemampuan` |
| Pelajaran percobaan adapter model: gaya sitasi berpindah ke bobot, fakta angka tidak; sitasi keluaran model bukan bukti | [pelajaran-adapter-model.md](indeks-pengetahuan/pelajaran-adapter-model.md) | Butir 1-5 |
| Draf pengelompokan folder arsip lama menurut domain, proyek, dan jenis (bukan klasifikasi final); manifest tugas pembangunan ulang per folder | [classification.json](katalog-docs/classification.json), [rebuild-manifest.json](katalog-docs/rebuild-manifest.json) | Kunci `note`, `items` |
| Wiki Information Library | `wiki-information-library/<kategori>/` | Lihat Titik masuk butir 5 |

## Titik masuk

1. **Aturan EKAS dan tingkat sumber R1-R5.** Baca [README EKAS](ekas-lapis-teks/00_START-HERE/README.md),
   lalu [REFERENCE-CONFIDENCE-LEVEL.md](ekas-lapis-teks/01_GOVERNANCE/REFERENCE-CONFIDENCE-LEVEL.md).
   Ringkasnya: R1 regulasi dan standar nasional (mengikat hukum), R2 standar internasional
   (mengikat bila diadopsi kontrak), R3 buku teks (menjelaskan metode, tidak menetapkan ambang
   kecuali diadopsi kontrak tertulis), R4 dokumentasi pabrikan (wajib untuk angka melekat
   produk), R5 sumber sekunder (penunjuk, tidak pernah sandaran akhir). Ambang lulus menuntut
   R1 atau R2. Yang tidak ada di rak dinyatakan tidak ada.
2. **Pekerjaan teknis per domain.** Buka rute domain di
   [PETA-DOMAIN.csv](indeks-pengetahuan/PETA-DOMAIN.csv), lalu `RANTAI-JAMINAN.md` domainnya
   (tabel Pengetahuan per domain di atas), lalu kartu rujukan sebelum mengutip angka.
3. **Mencari rumus atau angka acuan.** Mulai dari
   [KATALOG-RUMUS.md](ekas-lapis-teks/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md) bagian
   "Indeks cepat", lalu periksa daya ikat ambangnya di
   [AMBANG-TERIMA-INDUK.md](ekas-lapis-teks/07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md).
4. **Apa yang belum ada di rak.** [GAP-REGISTER.md](ekas-lapis-teks/02_REGISTERS/GAP-REGISTER.md)
   untuk peta celah naratif, [GAP-REGISTER.csv](ekas-lapis-teks/02_REGISTERS/GAP-REGISTER.csv)
   untuk baris `GAP-*` yang dikutip rantai.
5. **Wiki.** `wiki-information-library/` tidak punya katalog. Pada clone ini wiki hanya untuk
   pencarian terarah pada tugas tentang pustaka itu sendiri ([HARNESS.md](../HARNESS.md), tabel
   "Pilih koleksi"). Cari menurut kata kunci di dalam satu folder kategori; jangan membaca
   folder utuh. Isi tiap kategori:
   - `catatans/`: catatan sintesis dari pekerjaan lama, misalnya ringkasan blueprint, rekomendasi, dan penjelasan alur.
   - `faktas/`: pernyataan fakta tunggal bersumber, misalnya profil adopsi teknologi sebuah organisasi atau batas teknis sebuah alat.
   - `keputusans/`: keputusan yang pernah diambil beserta alasannya, misalnya prioritas pekerjaan atau konfigurasi.
   - `pelajarans/`: pelajaran dari kegagalan atau perbaikan, misalnya jebakan alat dan hasil audit lintas berkas.
   - `produks/`: lembar ringkas produk atau perangkat lunak dengan spesifikasi dari dokumen sumbernya.
   - `proyeks/`: rencana dan blueprint proyek lama, misalnya langkah, dependensi, dan kriteria terima.
   - `standars/`: standar dan rubrik kerja internal, misalnya rubrik skoring atau klasifikasi galat.
   - `vendors/`: entri vendor dari riset pameran dan direktori, satu berkas per vendor.

   Tiap objek memakai frontmatter yang sama: `id`, `type`, `title`, `status`, `sumber`,
   `halaman`, `tanggal_akses`, `kelas_bukti`, `sensitif`, `perkara`, `tags`, serta jejak
   pengajuan, verifikasi, dan promosi.

## Jebakan

1. **Tiga CSV indeks memakai pemisah pipa.** `PETA-DOMAIN.csv`, `INDEKS-KEMAMPUAN.csv`, dan
   `INDEKS-UNIT.csv` dipisah `|`; CSV lain, termasuk register EKAS, dipisah koma. Pembaca CSV
   bawaan hanya melihat satu kolom ([HARNESS.md](../HARNESS.md), bagian "Jebakan format").
2. **`INDEKS-UNIT.csv` adalah rute, bukan bukti.** Kolom `digest` menunjuk berkas sapuan yang
   tidak disertakan di clone. Kolom `ringkas` boleh dipakai untuk menemukan topik, tetapi tidak
   dikutip sebagai bukti; nyatakan bahwa sumbernya tidak tersedia ([HARNESS.md](../HARNESS.md),
   bagian "Menemukan rujukan lama").
3. **Kolom `digest` pada `PETA-DOMAIN.csv` juga menunjuk berkas di luar clone**, dan kolom
   `rantai` lebih tua dari folder domain: beberapa domain bertanda `TIDAK` kini sudah punya
   `RANTAI-JAMINAN.md` yang terbit kemudian. Yang berlaku adalah berkas rantai di folder domain.
4. **Kemampuan adalah draf.** `KEMAMPUAN.md` tiap domain, `INDEKS-KEMAMPUAN.csv`, dan
   `KEMAMPUAN-REGISTER.csv` menyatakan seluruh barisnya menunggu verifikasi tanpa sign-off
   engineer. Angkanya tidak sah sebagai ambang terima (lihat komentar di kepala
   [kemampuan FIBER-OPTIC](ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/FIBER-OPTIC/KEMAMPUAN.md) dan
   kunci `daya_ikat` di [META.json](indeks-pengetahuan/META.json)).
5. **`INTAKE-QUEUE.csv` diawali baris komentar sebelum header**, dan kolom `jalur`-nya memuat
   path mesin asal. Label kategori triase mesin bukan nama domain
   ([README register](ekas-lapis-teks/02_REGISTERS/README.md), bagian "Kaidah domain").
6. **Angka hitungan pada dokumen EKAS adalah potret bertanggal dan saling berbeda.** Sebaran R,
   jumlah rantai, dan jumlah templat pada README, BACA-DULU, peta sistem, dan README domain
   ditulis pada tanggal berbeda. Contohnya, README domain AI-ML menyebut mata ②-⑤ belum
   tersusun, padahal rantainya kini berbanner "berantai parsial terbimbing". Yang berlaku
   adalah isi folder dan register; jangan mengutip hitungan tanpa tanggalnya.
7. **Huruf rantai tidak unik.** Rantai CONSTRUCTION dan PROJECT-QUALITY sama-sama berkepala
   "Rantai M", dan beberapa huruf lain dinyatakan ad hoc pada kepala berkasnya. Rujuk rantai
   dengan nama folder domain, bukan hurufnya.
8. **Nomor halaman adalah halaman PDF**, kecuali dinyatakan keduanya. PDF tidak ada di clone;
   `03_SOURCE-VAULT/` hanya berisi `_ISI.md`. Membuka halaman asli adalah pekerjaan manusia
   ([BACA-DULU.md](ekas-lapis-teks/BACA-DULU.md), bagian "Apa isi paket ini").
9. **Buku sipil, bangunan, dan sebagian kelistrikan berbasis standar Amerika.** Metodenya boleh,
   angkanya tidak, misalnya tabel profil baja AS bukan profil SNI ([BACA-DULU.md](ekas-lapis-teks/BACA-DULU.md),
   butir 5).
10. **Contoh P00 bukan pekerjaan nyata.** Berkas `*-P00-*` dan baris register `P00 (CONTOH)`
    memuat angka karangan untuk menguji gate; jangan disalin ke dokumen keluaran.
11. **Folder yang disebut peta sistem tetapi tidak ada di clone.** `95_IMPORT-SNAPSHOTS/` dan
    `99_ARCHIVE/` disebut pada [EKAS-SYSTEM-MAP.md](ekas-lapis-teks/00_START-HERE/EKAS-SYSTEM-MAP.md)
    tetapi tidak disertakan.
12. **Path dalam teks EKAS memakai alias `ekas/` atau path mesin asal.** Terjemahkan dengan
    resolver baca-saja `tools/library.py` ([HARNESS.md](../HARNESS.md), bagian "Menemukan
    rujukan lama"); status `missing` dilaporkan, tidak diganti berkas bernama mirip.
13. **Penanda `sensitif: tidak` pada frontmatter wiki bukan penyaring.** Lihat AP-02 pada
    kebijakan sensitivitas.

## Hubungan dengan koleksi lain

- **3 Skills.** Beberapa skill kanonik memakai pengetahuan di sini sebagai sumber:
  [gsp-ekas-knowledge-index](../3%20Skills/kanonik/gsp-ekas-knowledge-index/SKILL.md) adalah
  router ke unit, domain, dan register EKAS; [pustaka-teknis](../3%20Skills/kanonik/pustaka-teknis/SKILL.md)
  untuk dokumen rekayasa yang butuh angka bersumber. Skill desain per domain, yaitu
  [fiber-link-design](../3%20Skills/kanonik/fiber-link-design/SKILL.md),
  [cctv-system-designer](../3%20Skills/kanonik/cctv-system-designer/SKILL.md),
  [grounding-lightning-design](../3%20Skills/kanonik/grounding-lightning-design/SKILL.md), dan
  [rcm-analysis](../3%20Skills/kanonik/rcm-analysis/SKILL.md), sejalan dengan rantai domainnya.
  Keterkaitan isi skill desain dengan rantai adalah perkiraan dari deskripsinya; periksa
  SKILL.md sebelum mengandalkannya. `LAPORAN-MIGRASI.csv` mencatat berkas skill yang dulu
  menyebut folder rak lama. Pilih salinan skill menurut [HARNESS.md](../HARNESS.md), bagian
  "Pilih skill".
- **1 Workflow.** Standar operasi dan metadata pustaka ada di [1 Workflow/INDEKS.md](../1%20Workflow/INDEKS.md).
- **7 Tools.** Perkakas lintas pustaka diarsipkan di [7 Tools/INDEKS.md](../7%20Tools/INDEKS.md);
  perkakas khusus EKAS ada di `ekas-lapis-teks/90_TOOLS/`.
- **Pintu masuk pustaka.** [HARNESS.md](../HARNESS.md) menetapkan cara baca tiap berkas di
  folder ini (cari INDEKS.md, baca utuh README EKAS, wiki hanya pencarian terarah).

## Sensitivitas

Kebijakan lengkap ada di [KEBIJAKAN-SENSITIVITAS.md](../KEBIJAKAN-SENSITIVITAS.md), bagian
"Kelas penanganan" (baris 13), "Aturan" (baris 30), dan "Menjalankan skrip arsip" (baris 137).
Hal yang khas pada folder ini:

- **Wiki, `katalog-docs/`, dan register antrean EKAS tertolak bawaan pada edisi umum.** Wiki
  memuat penunjuk perkara dan entri riset vendor; `katalog-docs/` memuat nama folder arsip dan
  proyek lama (KM-2). Panduan ini sengaja tidak menautkan objek wiki satu per satu dan tidak
  menyebut nama perkara, klien, atau orang. Turunan isi wiki mewarisi kelas sumbernya (AP-06).
- **Rincian host dan path mesin asal** muncul pada beberapa berkas: berkas asal-usul arsip
  `08_EVIDENCE/BUKUV3/`, kolom `jalur` `INTAKE-QUEUE.csv`, `LAPORAN-MIGRASI.csv`, kepala
  `GAP-REGISTER.md`, `README-ekspor.md`, dan docstring skrip `90_TOOLS/`. Alamat itu
  menggambarkan lingkungan sumber, bukan endpoint harness ini; tidak dihubungi dan tidak
  disalin ke keluaran (AP-16).
- **Skrip `90_TOOLS/` tidak dijalankan.** Daftar cakupan "skrip arsip" pada kebijakan tidak
  menyebut folder ini secara eksplisit; panduan ini memperlakukannya sebagai kode arsip yang
  dapat dijalankan (KM-7) dan menerapkan aturan yang sama. Agen boleh menaikkan kelas, tidak
  menurunkannya (AP-02).
- **Sitasi keluaran model bukan bukti.** Angka yang muncul dari model atau dari digest wajib
  ditelusuri ke register dan kartu rujukan sebelum dipakai.

Disusun 2026-11-06 dari keadaan commit 023082a. Inventaris lengkap: INDEKS.md.
