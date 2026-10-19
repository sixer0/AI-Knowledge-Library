# Rantai S - Infrastruktur kritis: perlindungan siber objek vital

> **PENAMAAN AD-HOC (kartu t_9b7ace41, 11-10-2026).** Huruf "S" dipakai di kepala ini hanya
> agar rantai bisa dirujuk; penunjukan resmi huruf rantai untuk langkah 15-17 adalah wewenang
> controller (preseden: `MECHANICAL/RANTAI-JAMINAN.md` CATATAN SILANG-PEMILIK butir 1, yang
> menduga alokasi berurutan S,T = pasangan-1). Ganti huruf di kepala bila controller memutuskan
> lain - isi mata rantai tidak terpengaruh.

## RANTAI BERANTAI PARSIAL TERBIMBING (terbit 11-10-2026, kartu t_9b7ace41)

Mata ①-③ dan ⑤ tersusun **terbimbing lapisan yang ada di rak ini** (satu resume ber-halaman
`REF-CIP-001` + kartu `04_KNOWLEDGE-CARDS/CRITICAL-INFRASTRUCTURE/` + digest sapu-baca L1/L3)
diperkuat buka-ulang halaman vault pada run kartu ini. Mata ④ **tanpa ambang terima dari rak**:
ukur 11-10-2026 `MASTER-REFERENCE-REGISTER.csv` = 0 baris R1/R2 ber-domain
CRITICAL-INFRASTRUCTURE (seluruh R1/R2 di rak hanyalah empat baris: IEEE 1188/IEC 62485-2
POWER-BACKUP, ANSI-NETA ATS-2017 ELECTRICAL, IEC 61280-4-2 FIBER-OPTIC, BS EN 62676-1-2
VIDEO-SURVEILLANCE). Celah dibukukan apa adanya di mata ④, bukan diisi nilai buku.

**Daya-ikat tidak naik.** Satu-satunya rujukan domain ini (`REF-CIP-001`) berstatus `ACTIVE`
dengan kolom `may_set_acceptance = no-unless-contract-adopts` di register induk (baris 4).
Susunan mata ②-⑤ ini **menyiapkan**, insan yang menandatangani; nol baris register disunting
oleh berkas ini.

**Ambang berasal dari:** bukan dari rak ini. Rak ini memasok **kerangka analisis dan bahasa
arsitektur** (aset kritis, ketergantungan antar-sektor, keamanan-sejak-rancangan, redundansi,
graph serangan). Ambang terima kepatuhan milik **kontrak** atau R1/R2 yang belum ada di rak -
dan untuk domain ini keempat celahnya sudah bernama: `GAP-002`, `GAP-003`, `GAP-006`, `GAP-007`.

**Posisi domain (penting sebelum memakai berkas ini).** Domain ini berdiri di laci sendiri
dengan satu buku suntingan 2015. **Norma keamanan teknisnya ada di rantai J (CYBERSECURITY)**,
bukan di sini; rantai ini memegang sisi *objek vital*: mengapa aset ini dibidik, sektor mana
saja, bagaimana ketergantungan antar-sistem membentuk risiko, dan bagaimana rancangan rekayasa
(sebabnya keamanan tidak boleh ditempel sesudah sistem jadi). Pemakai hilir wajib sadar dua
laci berbeda menilai materi sejenis `[R3, digest L3 CRITICAL-INFRASTRUCTURE, bagian Tumpang-tindih]`.

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman (PDF, dibuka ulang 11-10-2026 dengan pypdf + Xpdf 4.06 `pdftotext -layout`) |
|---|---|---|---|
| `REF-CIP-001` - Johnson (ed.), *Cybersecurity: Protecting Critical Infrastructures from Cyber Attack and Cyber Warfare*, CRC Press 2015, Bab 2 (Johnson sendiri) | **R3** ACTIVE | Aset kritis sebagai *target-rich environment*; kerangka klasifikasi sektor (Executive Order 13010 / PDD-63 / EO 13228 / USA PATRIOT Act / HSPD-7 / PPD-21); pemetaan ketergantungan antar-sektor; energi-grid, transportasi, telekomunikasi sebagai tiga sektor contoh. | `[R3, Johnson, PDF 51]` (peta isi bab 2, folio 33); `[R3, Johnson, PDF 53]` (EO 13010 + PDD-63, folio 35); `[R3, Johnson, PDF 54]` (PATRIOT Act mengklasifikasi sektor, folio 36); `[R3, Johnson, PDF 58]` (badan seksi 2.2 *Critical Infrastructure Interdependencies*, folio 40); `[R3, Johnson, PDF 65]` (grid kelistrikan + SCADA, folio 47); `[R3, Johnson, PDF 76]` (NIST *Framework for Improving Critical Infrastructure Cybersecurity*, folio 58) |
| `REF-CIP-001` bagian Bab 3 (Fred Cohen) | **R3** ACTIVE | Keamanan **sejak rancangan rekayasa**: sifat acak kegagalan, resilien, fault-intolerance vs fault-tolerance, fail-safe, desain redundansi untuk toleransi sistem, graph serangan, game theory, metode optimasi & manajemen risiko, lapisan perlindungan | `[R3, Johnson, PDF 85]` (peta isi bab 3 lengkap, folio 67); `[R3, Johnson, PDF 94]` (3.3.1 Resilience, folio 76); `[R3, Johnson, PDF 105]` (3.4.3 Redundancy Design for System Tolerance, folio 87); `[R3, Johnson, PDF 109]` (3.5.1 Attack Graphs, folio 91); `[R3, Johnson, PDF 162]` (defense-in-depth + common mode failure, folio 144) |
| `REF-CIP-001` bagian Bab 6-7 | **R3** ACTIVE | Biaya ekonomi keamanan (argumen "berapa bila tidak dilakukan"); lanskap ancaman 2015 | `[R3, Johnson, PDF 273]` (folio 255, peta bab); `[R3, Johnson, PDF 305]` (folio 287, peta bab) - **kedua halaman ini hanya dibuka sebagai peta bab**, isinya tidak dikutip sebagai angka |
| Padanan norma keamanan teknis | **R3/R5** | Anderson *Security Engineering*, Alsmadi NICE, panduan operasional | **laci CYBERSECURITY** - lihat Rantai J; bukan milik domain ini |
| **UU 11/2008 (ITE) + perubahan** | **R1** | Dasar hukum bukti elektronik Indonesia | ❌ **TIDAK ADA** - `GAP-002` |
| **Peraturan BSSN No. 4/2021** | **R1** | Kriteria audit keamanan instansi | ❌ **TIDAK ADA** - `GAP-003` |
| **ISO/IEC 27001 & 27002** | **R2** | Persyaratan SMKI | ❌ **TIDAK ADA** - `GAP-006` |
| **NIST SP 800-86 dan ISO/IEC 27037** | **R2** | Penanganan bukti digital | ❌ **TIDAK ADA** - `GAP-007` (status `sebagian`; teks register memakai kedua nama dalam satu baris) |
| **NIST CSF / IEC 62443 / NIST SP 800-82** (kerangka khusus infrastruktur kritis & sistem kendali industri) | **R2** | Isi yang paling dituntut tender objek vital | ❌ **TIDAK ADA** - **belum punya gap_id** (lihat mata ④ butir 3) |

**Konversi halaman (terukur hari ini).** Selisih **tetap +18** pada seluruh titik uji: PDF 51 ->
folio 33, PDF 58 -> 40, PDF 65 -> 47, PDF 85 -> 67, PDF 88 -> 70, PDF 105 -> 87, PDF 109 -> 91,
PDF 162 -> 144, PDF 273 -> 255, PDF 305 -> 287. Kutip nomor cetak maupun PDF sama-sama sah `[R3, berkas rak
Johnson, baris 7-8]`; berkas rak mengonfirmasi 346 halaman, 1,8 MB, 14 bookmark tingkat bab -
ketiganya terukur ulang hari ini (pypdf: pages=346, bookmarks=14, size=1,8 MB).

**Provenans pembukaan halaman.** Seluruh baris "Halaman" di tabel ① dibuka sendiri pada run
kartu ini; tidak ada jangkar yang diwarisi tanpa verifikasi. Dua butir yang **tidak** ditemukan
dan karenanya tidak diklaim apa adanya: (a) frasa *defense-in-depth* **tidak muncul** di Bab 2
maupun di paruh awal Bab 3 - ia terukur baru muncul di **PDF 162 (folio 144, seksi 3.9.2
Standard Design Approaches)** dan **PDF 300 (folio 282, di dalam Bab 6)**, keduanya di luar
semua halaman yang dicantumkan berkas resume; (b) kata "public-private partnership" dan
"CIIP" = 0 hitung pada seluruh lapis teks buku. Batas Bab 3 terukur: mulai PDF 85 (folio 67),
masih berlanjut di PDF 171 (folio 153), dan Bab 4 mulai PDF 173 (folio 155).

---

## ② Keputusan desain

Tingkat R3 **cukup** untuk mata ini: keputusan rekayasa memang penilaian; yang wajib tertulis
adalah pilihan + alternatif yang ditolak + alasannya (`01_GOVERNANCE/ASSURANCE-WORKFLOW.md`,
tabel "Aturan tingkat pada tiap mata rantai").

| Yang ditetapkan | Dasar | Alternatif yang ditolak dan alasannya |
|---|---|---|
| **Kelas aset dan sektor yang dilindungi ditetapkan lebih dulu**, per sektor, bukan per perangkat | Bab 2: infrastruktur kritis sebagai *target-rich environment*; klasifikasi sektor diturunkan EO 13010 -> PDD-63 -> PATRIOT Act -> HSPD-7 -> PPD-21 `[R3, Johnson, PDF 51, 53-54]` | Daftar perangkat tanpa penetapan aset/sektor **ditolak** - yang diserang adalah fungsi yang membuat aset itu vital, bukan barangnya |
| **Pemetaan ketergantungan antar-sistem** masuk dokumen rancangan (listrik <-> kendali <-> telekomunikasi <-> air) | `[R3, Johnson, PDF 65]` (gangguan terkoordinasi pada grid dapat menjalar ke *cascading failures* jauh dari titik serangan); `[R3, Johnson, PDF 58]` seksi 2.2 *Critical Infrastructure Interdependencies* (folio 40; badan seksi, merujuk riset Pederson, Dudenhoeffer, Hartley & Permann) | Perimeter tunggal di tepi jaringan **ditolak** - jalur masuk lewat sistem tetangga tidak terlihat dari perimeter sendiri |
| **Keamanan masuk sejak rancangan**, bukan ditempel sesudahnya | `[R3, Johnson, PDF 85]` (kerangka bab: 3.3 Random Nature of Faults -> 3.4 In the Presence of Attackers -> 3.5 Issues of Time and Sequence); `[R3, berkas rak Johnson, baris 50-54]` | Pengerasan pasca-pasang **ditolak** sebagai satu-satunya langkah - biaya per unit proteksi naik dan urutannya tidak dapat dibuktikan |
| **Redundansi dirancang terhadap kegagalan modus umum (common mode), bukan terhadap jumlah perangkat** | `[R3, Johnson, PDF 105]` (3.4.3 Redundancy Design for System Tolerance); `[R3, Johnson, PDF 162]` (folio 144: standardisasi -> common mode failures; defense-in-depth menaikkan biaya/skill penyerang dengan memvariasikan lapisan) | Dua perangkat identik dengan konfigurasi identik **ditolak** sebagai redundansi - satu cacat/one patch memukul keduanya sekaligus |
| **Fault tolerance vs fail-safe dipilih eksplisit per fungsi kendali** | `[R3, Johnson, PDF 85]` (3.3.2 Fault Intolerance and Fault Tolerance, cetak 78; 3.3.3 Fail-Safe, cetak 82); `[R3, Johnson, PDF 94]` (3.3.1 Resilience, folio 76) | Menyeragamkan semua fungsi pada "selalu hidup" **ditolak** - pada proses fisik, berhenti-aman lebih benar daripada terus-jalan |
| **Urutan serangan dimodelkan (attack graph / time-sequence)** sebelum kendali dibagi-bagi | `[R3, Johnson, PDF 109]` (3.5.1 Attack Graphs, folio 91); `[R3, Johnson, PDF 85]` (3.5.2 Game Theory Modeling cetak 94, 3.5.3 Model-Based Constraint and Simulations cetak 95) | Sebaran kendali tanpa urutan **ditolak** - tidak dapat menjawab "kendali mana yang benar-benar memutus jalur" |
| **Proteksi SCADA/ICS dipisah dari LAN kantor** (segmentasi, firewall, enkripsi, deteksi yang lebih halus) | `[R3, Johnson, PDF 65]` (perlindungan SCADA dengan firewall, enkripsi, deteksi penyusupan); `[R3, berkas rak Johnson, baris 56-62]` | Menyamaratakan jaringan kendali dengan jaringan kantor **ditolak** - pola lalu lintas dan konsekuensi gangguannya berbeda |
| **Bahasa arsitektur mengikuti kerangka NIST CSF** bila pemberi kerja memakainya | `[R3, Johnson, PDF 76]` (folio 58: seksi 2.6 Framework for Improving Critical Infrastructure Cybersecurity, tugas NIST) | Mengarang sendiri lima-fase-nya **ditolak** - tender instansi memeriksa terhadap kerangka yang bernama, bukan terhadap kosakata GSP |
| **Kriteria kepatuhan yang dijanjikan harus R1/R2 dan salinannya dipegang** | ⚠ **harus R1/R2** - lihat mata ④ | Menjanjikan "sesuai Perban BSSN / ISO 27001 / NIST CSF" **tanpa salinan standarnya ditolak** - menjanjikan sesuatu yang tidak dapat diperiksa sendiri (preseden rantai J) |

> Keputusan paling menentukan di rantai ini: **redundansi dinilai dari variasi, bukan dari
> jumlah** `[R3, Johnson, PDF 162]`. Dua lapis proteksi yang sama persis adalah satu lapis
> dengan dua tagihan.

---

## ③ Perhitungan

**Domain ini hampir tanpa perhitungan, dan itu keadaan sebenarnya, bukan kelalaian.**
`REF-CIP-001` di kartu register ditulis: rumus/metode = `-`, halaman jangkar = `-`
`[R3, kartu REF-CIP-001, bagian 1-2]`; digest L3 menegaskan kartu ini **penunjuk konsep**,
substansinya kerangka kualitatif `[R3, digest L3 CRITICAL-INFRASTRUCTURE, bagian GAP terkait]`.
Yang ada bersifat **penilaian yang harus diberi label metodenya**, bukan rumus:

| Yang dinilai | Cara | Sifat angka |
|---|---|---|
| Prioritas aset kritis | Kemungkinan x dampak per sektor/aset | `PROJECT-DERIVED` - **wajib menyebut metodenya internal**, bukan metode normatif |
| Cakupan ketergantungan | Matriks aset x sistem penunjang (listrik, pendingin, kendali, telekom, transportasi) | `PROJECT-DERIVED` (kerangka dari `[R3, Johnson, PDF 58]` seksi 2.2) |
| Kedalaman lapisan proteksi | Jumlah lapisan **yang berbeda modus kegagalannya** pada tiap jalur serangan | `PROJECT-DERIVED` (dasar penalaran `[R3, Johnson, PDF 162]`) |
| Urutan/lamanya serangan | Attack graph + time-sequence | `PROJECT-DERIVED` (metode `[R3, Johnson, PDF 109]`) |
| Pembenaran ekonomi investasi | Bandingkan biaya proteksi vs biaya akibat tidak dilakukan | `ASSUMPTION` bila angkanya belum dari kontrak/asuransi - **wajib sensitivitas + rencana penggantian** (kerangka `[R3, Johnson, PDF 273]`, peta bab 6) |

**Angka yang ada di lapisan ini dan TIDAK BOLEH dipakai sebagai milik proyek GSP**
(dicatat supaya tidak "dipinjam" diam-diam oleh pembaca berikutnya):

| Angka di buku | Letak | Mengapa bukan angka GSP |
|---|---|---|
| Bauran pembangkit listrik AS: batu bara >51%, nuklir 20%, minyak+gas 18%, hidro+terbarukan 11% | `[R3, Johnson, PDF 65]` (folio 47) | Statistik kelistrikan Amerika Serikat terbitan 2015; konteks Indonesia berbeda, dan buku ini bukan sumber statistiknya |
| "something like $1 trillion of work is needed just to bring critical infrastructure repairs up to the level they are supposed to normally operate" | `[R3, Johnson, PDF 88]` (folio 70) | Angka retorika kebijakan AS dalam bab esai, tanpa metode hitung; jangan pernah masuk proposal sebagai dasar biaya |

**Aturan yang membatalkan hasil bila dilanggar:** skor risiko yang tampak seperti angka objektif
padahal hasil penilaian sendiri adalah bentuk penyesatan yang paling halus - preseden tertulis
di rantai J mata ③. Setiap angka di mata ini ditandai `PROJECT-DERIVED` dan metodenya disebut
internal; `ASSUMPTION` tidak boleh menjadi ambang terima final tanpa persetujuan tertulis
(`pustaka-teknis`, aturan 5-6).

---

## ④ Pengujian - ⚠ MATA TANPA AMBANG

Urutan tingkat untuk mata ini adalah R1 -> R2 -> kontrak (`ASSURANCE-WORKFLOW.md`); R3 hanya
sah bila kontrak mengadopsinya tertulis, dan kolom register `REF-CIP-001` berbunyi
`no-unless-contract-adopts` `[R3, register induk baris 4]`.

| Butir | Ketentuan | Status sumber |
|---|---|---|
| Kelengkapan penetapan aset/sektor | Setiap aset yang dilindungi punya sektor + alasan kerentanan (mata ② baris 1) | Metode R3 `[R3, Johnson, PDF 51, 53-54]`; **ambang lulus = kontrak** |
| Matriks ketergantungan | Setiap fungsi kendali punya daftar sistem penunjang yang digantungkan | Metode R3 `[R3, Johnson, PDF 51, 65]`; **ambang = kontrak** |
| Segmentasi jaringan kendali | Tidak ada rute langsung LAN kantor -> perangkat kendali | Kontrak + **[R4]** lembar data peranti kendali; kerangka R3 `[R3, Johnson, PDF 65]` |
| Redundansi bebas modus-umum | Salinan cadang berbeda konfigurasi/model/firmware | R3 `[R3, Johnson, PDF 105, 162]`; **ambang = kontrak** (buku tidak menetapkan berapa lapis) |
| Bukti keamanan-sejak-rancangan | Catatan keputusan `TPL-01` berisi alternatif yang ditolak | Gerbang G2 (`ASSURANCE-GATES.md`); **bukan soal tingkat** |
| Uji penetrasi / uji redaman jalur | Lingkup, metode, kriteria dari kontrak | Kontrak; **buku ini tidak menetapkan metode uji** |
| **Kepatuhan Perban BSSN 4/2021** | ❌ **tidak dapat diuji dari rak** | Regulasinya tidak ada - `GAP-003` |
| **Kepatuhan ISO/IEC 27001-27002** | ❌ **tidak dapat diuji dari rak** | Standarnya tidak ada - `GAP-006` |
| **Keterterimaan bukti di pengadilan** | ❌ **tidak dapat dinyatakan** | UU ITE tidak ada - `GAP-002` |
| **Pemenuhan NIST CSF / IEC 62443 untuk objek vital** | ❌ **tidak dapat diuji dari rak** | Namanya ada di buku (`[R3, Johnson, PDF 76]`), teks standarnya tidak; **belum bernama di GAP-REGISTER** (butir 3 di bawah) |

### Celah yang dibukukan (bukan dikarang)

1. **Tidak ada satu pun sandaran R1/R2 di domain ini.** Ukur 11-10-2026:
   `02_REGISTERS/MASTER-REFERENCE-REGISTER.csv` (103 baris data) memuat tepat 4 baris R1/R2 dan
   keempatnya domain lain; `GAP-REGISTER.csv` (22 baris) tidak punya satu pun baris ber-domain
   CRITICAL-INFRASTRUCTURE; `07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md`
   = 0 butir menyebut infrastruktur kritis/objek vital (ukur grep, berkas 116 baris).
2. **Seluruh kebutuhan kepatuhan domain ini menumpang pada gap milik CYBERSECURITY** (`GAP-002`,
   `-003`, `-006`, `-007`). Kolom `domain` keempat baris itu hanya menyebut CYBERSECURITY -
   terukur ulang hari ini. Temuan ini **sudah** tercatat oleh lajur L1 (23-09-2026) sebagai
   rekomendasi perluasan kolom; sampai hari ini belum diterapkan. Lihat CATATAN SILANG-PEMILIK
   butir 2 - ini bukan edit di tempat, hanya laporan.
3. **Usulan butir GAP baru untuk langkah 25-26** (kewenangan penulis register GAP, bukan LOCK
   ini): kerangka/standar keamanan infrastruktur kritis dan sistem kendali industri - **NIST CSF
   (disebut di `[R3, Johnson, PDF 76]`), IEC 62443, NIST SP 800-82** - tidak ada di rak. Ukur
   hari ini: `grep -riec "62443|800-82"` pada `02_REGISTERS/*.csv` = 0; satu-satunya jejak NIST
   adalah `GAP-007` (SP 800-86, penanganan bukti digital - isu lain). Akibatnya **isi pokok tender
   objek vital** (kerangka keamanan + segmentasi ICS) hari ini hanya berkerangka R3.
4. **Bentuk jawaban yang sah hari ini** saat ambang kepatuhan objek vital diminta: nyatakan
   "tidak ada di rak ini; sumber yang seharusnya: R1 (UU ITE, Perban BSSN) atau R2 (ISO/IEC
   27001, NIST CSF/IEC 62443) beserta pasal/kontrolnya", lalu mintakan angka itu ke pemilik
   pekerjaan. **Jangan** memakai angka contoh buku (51%, 20%, $1 trillion) sebagai dasar apa pun.

### Yang boleh dan tidak boleh dikatakan

| ✅ Boleh | ❌ Tidak boleh |
|---|---|
| *"Aset dan sektor ditetapkan mengikuti kerangka klasifikasi infrastruktur kritis yang dirujuk bab 2 [R3, Johnson, PDF 51, 53-54]; kriteria kepatuhan mengacu regulasi yang salinannya dilampirkan."* | ~~"Sistem ini sesuai Perban BSSN 4/2021"~~ dengan sandaran buku/tesis |
| *"Rancangan memisahkan jaringan kendali dan mereduksi kegagalan modus umum melalui lapisan proteksi bervariasi [R3, Johnson, PDF 105, 162]."* | ~~"Redundansi kami defense-in-depth penuh"~~ tanpa menyebut lapisan mana yang berbeda modus gagal |
| *"Kerangka pelaporan mengikuti NIST CSF - salinan dokumen kerangka diperoleh terpisah dan dilampirkan."* | ~~"Memenuhi NIST CSF"~~ tanpa teks kerangka dan tanpa pemetaan kontrol |

---

## ⑤ Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| Dokumen penetapan aset + sektor + alasan kerentanan | ✅ | Dasar seluruh kendali; mata ② baris 1 |
| Matriks ketergantungan aset x sistem penunjang | ✅ | Bentuknya dari `[R3, Johnson, PDF 58]` seksi 2.2 |
| Catatan keputusan desain `TPL-01` (termasuk **alternatif yang ditolak**) | ✅ | Gerbang G2 gagal bila kolom alternatif kosong (`ASSURANCE-GATES.md` bagian G2) |
| Bukti keamanan-sejak-rancangan (jejak keputusan pada tahap rancangan) | ✅ | Yang membuat klaim "bukan tempelan" dapat diperiksa `[R3, Johnson, PDF 85]` |
| Basis konfigurasi pengerasan + penyimpangan yang disetujui | ✅ | Sandaran teknisnya rantai J (laci CYBERSECURITY), bukan domain ini |
| Bukti segmentasi jaringan kendali (skema + aturan firewall terpasang) | ✅ | Angka unjuk kerja peranti = **[R4]** |
| Peta lapisan proteksi vs modus kegagalan | ✅ | Membedakan redundansi sungguhan dari duplikasi `[R3, Johnson, PDF 162]` |
| Rekaman uji (lingkup, alat, kondisi, penyaksi) | ✅ | Kerangka umum `07_VERIFICATION-VALIDATION/TEST-PROCEDURES/TEMPLATE-BERITA-ACARA.md` bagian 1 - **tidak punya jenis uji khusus keamanan objek vital** (lihat catatan di bawah) |
| **Pernyataan batas kepatuhan** | ✅ **wajib** | Menyebut standar mana yang **belum** dapat dibuktikan (`GAP-002/003/006/007` + usulan butir 3) - baris yang membedakan dokumen jujur dari dokumen yang akan dipersoalkan (preseden rantai J) |
| Daftar asumsi terbuka + daftar butir menunggu data OEM `[R4]` | ✅ | Dua baris yang paling sering hilang di G6 (`ASSURANCE-GATES.md` bagian G6) |
| Kartu kendali rantai per besaran (`TPL-00`) | ✅ | Status kartu: **putus di mata ④**; sah tertulis begitu |

**Keterbatasan kerangka yang ada:** `TEMPLATE-BERITA-ACARA.md` menyediakan 8 jenis uji (serat,
pembumian, isolasi, baterai, genset, video, termal, penyimpanan) dan **tidak punya bagian untuk
uji keamanan siber maupun uji objek vital**; pakai "Rangka umum - berlaku untuk semua jenis"
(bagian 1 berkas itu) dan nyatakan bahwa jenis uji ini belum punya template khusus.

---

## Status rantai

**TERBIMBING SAMPAI MATA ④.** Mata ①-③ dan ⑤ tersusun; setiap angka bertanda `[R-n]` dengan
halaman yang dibuka ulang terhadap vault hari ini, dan setiap ambang yang tidak punya sandaran
dibukukan sebagai celah, bukan diisi.

**Kapan rantai ini boleh disebut utuh:** setelah (a) minimal satu sandaran R1/R2 kepatuhan masuk
rak (`GAP-002`, `-003`, `-006`, `-007` ditutup), (b) kerangka infrastruktur kritis (NIST CSF /
IEC 62443 / SP 800-82) punya gap_id dan salinannya, dan (c) insan menandatangani kriteria yang
dipakai pada pekerjaan serah terima.

**Batas usia yang menempel pada seluruh berkas ini.** Terbitan 2015 dan berorientasi Amerika
Serikat: Bab 7 (lanskap ancaman) diperlakukan sebagai catatan sejarah, bukan gambaran ancaman
masa kini; klasifikasi sektornya adalah kerangka acuan, **bukan** klasifikasi objek vital
Indonesia - padanan Indonesia belum ada di rak `[R3, berkas rak Johnson, baris 98-103]`.
Pengamanan **fisik/perimeter** objek vital bukan cakupan domain ini - ia dibahas buku lain di rak
`[R3, berkas rak Johnson, baris 105-106]`.

---

## CATATAN SILANG-PEMILIK (temuan di luar LOCK, dilaporkan, TIDAK ditambal di sini)

Tertanggal 11-10-2026, kartu t_9b7ace41. Berkas-berkas berikut bukan milik LOCK ini sehingga
tidak disunting.

1. **Berkas resume tidak menyebut NIST CSF dan menaruh letak defense-in-depth di luar jangkauannya.**
   `CRITICAL-INFRASTRUCTURE/R3 - Cybersecurity Protecting Critical Infrastructures.md` memetakan
   Bab 3 (cetak 67 / PDF 85) sebagai bab rancangan rekayasa - benar - tetapi tidak satu pun
   barisnya menyebut *defense-in-depth*, yang terukur hidup di dalam bab yang sama pada
   **PDF 162 (folio 144, seksi 3.9.2 Standard Design Approaches)** dan dikutip lagi di
   **PDF 300 (folio 282, Bab 6)**; halaman 162 itu sendiri tidak tercakup pemetaan mana pun di
   resume (resume berhenti di "Bab 3 = PDF 85"). Seksi 2.6 tentang **NIST Framework for Improving
   Critical Infrastructure Cybersecurity** (`PDF 76`, folio 58) juga tidak muncul di resume maupun
   di tabel "Pemakaian di GSP", padahal itulah rujukan kerangka yang paling mungkin diminta
   pemberi kerja. Pemilik: berkas resume + kartu `REF-CIP-001` (jalur RESUME-R3/kurator).
2. **Kolom `domain` GAP-002/003/006/007 tidak menyebut CRITICAL-INFRASTRUCTURE** walau seluruh
   mata ④ domain ini bergantung padanya. Terukur ulang 11-10-2026 pada `GAP-REGISTER.csv`;
   temuan yang sama sudah dibuat lajur L1 pada 23-09-2026 dan belum diediasi. Pemilik: penulis
   register GAP (langkah 25-26).
3. **Tidak ada gap_id untuk kerangka keamanan infrastruktur kritis/ICS** (NIST CSF, IEC 62443,
   NIST SP 800-82) padahal nama pertama disebut di buku rak. Pemilik: langkah 25-26.
4. **Tabrakan huruf rantai belum dialokasikan controller.** Rantai berjalan sampai R, lalu
   MECHANICAL memakai "W" ad-hoc dengan dugaan S,T = pasangan-1; rantai saudara
   `GEOSPATIAL-SURVEY` di kartu yang sama memakai "T". Blueprint 02 baris 31 mewajibkan
   "25/25 domain punya RANTAI bermata" tanpa menunjuk huruf. Pemilik: controller/TA.
   Preseden: `MECHANICAL/RANTAI-JAMINAN.md` CATATAN SILANG-PEMILIK butir 1.
5. **Duplikasi huruf "M" sudah terjadi lebih dulu** (`CONSTRUCTION` dan `PROJECT-QUALITY`
   keduanya berkepala "Rantai M", ukur 11-10-2026). Bukan temuan kartu ini, tetapi relevan
   sebelum huruf baru dialokasikan - penamaan rantai perlu satu registri, bukan kebiasaan lokal.
