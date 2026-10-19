# Rantai M - Pelaksanaan konstruksi, taksiran biaya, dan penjadwalan

> **Objek kanonik:** IL/vault `construction-korpus-ekas-0929`
> (`vault/cvlk-0929/2026-09-29_construction-korpus-ekas-0929.md`, dipromosikan 2026-09-29,
> sha256 `bce992cd3f74635dcf01fde9012f3e18e93cd348a65de4b350c4bf2eefbe0113`).
> Berkas ini terbit pasca-VERIF C2 sebagai jalur aktivasi; muatan divonis custodian iter-2
> terverifikasi. Known-defek KD-N1/N7 tidak disalin ke sini; register lengkapnya hidup di
> objek kanonik Bagian 6.

---

### RANTAI M - Pelaksanaan konstruksi, taksiran biaya, dan penjadwalan

#### PERINGATAN: RANTAI INI PUTUS DI MATA 4 (dan sebagian mata 2 untuk konteks Indonesia)

Tidak ada satu pun sumber R1 atau R2 untuk harga satuan pekerjaan maupun norma produktivitas di
rak. Seluruh angka RAB yang mengikat - yang justru diminta tender - tidak dapat dibuktikan dari
rak ini. Mata 2 utuh untuk METODE, tetapi keputusan yang bersandar syarat kontrak dan regulasi
Indonesia (klaim perpanjangan waktu, K3) tidak punya sandaran normatif. Diterbitkan putus dengan
sengaja, seperti rantai D, J, dan K.

#### Mata 1 - Rujukan

| Sumber | Tingkat | Memasok | Halaman |
|---|---|---|---|
| Peurifoy, Construction Planning, Equipment, and Methods ed. 9 | R3 | ekonomi alat, pekerjaan tanah, excavator, crane, beton lapangan | PDF 57, 115, 392, 842 |
| Holm & Schaufelberger, Construction Cost Estimating (2021) | R3 | jenis & ketelitian estimasi, volume, harga pekerjaan sendiri, penawaran subkontrak, penyelesaian estimasi | PDF 30, 90, 150, 200, 234 |
| Mubarak, Construction Project Scheduling and Control (2019) | R3 | CPM, perataan sumber daya, pemutakhiran, pemampatan waktu-biaya | PDF 65, 149, 183, 243 |
| Lembar data alat + penawaran subkontraktor | R4 | produktivitas & biaya riil per proyek | per proyek (tiada laci) |
| REF-PRQ-001 (Siegel, manajemen proyek) | R3 domain PROJECT-QUALITY | pendamping manajemen | POINTER saja (V-15) |
| AHSP / SNI analisis harga satuan | R1 | harga satuan pekerjaan untuk RAB | TIDAK ADA - GAP-019 [csv:20] |
| SNI 1726/1727/1729/2847 (mutu struktur pekerjaan sipilnya) | R1 | ambang mutu hasil pekerjaan | TIDAK ADA - GAP-015..018 (ranah rantai K) |
| Regulasi K3 konstruksi (Permenaker PPPK) | R1 | syarat keselamatan kerja konstruksi | TIDAK ADA - laci PERMENAKER kosong; tidak dirujuk lapis mana pun (usulan U-1) |

Pola tabel identik rantai K: R1 kosong semua; yang ada hanya R3 + R4 per proyek.

#### Mata 2 - Keputusan desain (pelaksanaan)

| Yang ditetapkan | Dasar | Alternatif yang ditolak |
|---|---|---|
| Tingkat ketelitian estimasi per tahap (awal/anggaran/penawaran) dinyatakan eksplisit | Holm PDF 30 | Menyebut angka awal dengan ketelitian angka akhir DITOLAK - melindungi GSP saat angka awal dibandingkan dengan akhir [Holm:34-36] |
| Pemisahan pekerjaan sendiri vs subkontrak | Holm bagian IV PDF 200 | Menilai penawaran subkontrak tanpa breakdown DITOLAK |
| Sewa vs beli alat + biaya per jam | Peurifoy bab 2 PDF 57 + R4 | Angka taksiran umum buku dipakai sebagai angka pasti DITOLAK [Peurifoy:53-54] |
| Pemilihan crane + radius angkat | Peurifoy bab 16 PDF 842 | Salah pilih crane = alat datang tetapi tidak sanggup mengangkat [Peurifoy:48-49] |
| Jadwal dasar CPM dibekukan sebagai lingkup | Mubarak bab 4 PDF 65 + G1 | Jadwal tanpa jalur kritis DITOLAK - tidak bisa membedakan keterlambatan berarti dan tidak |
| Keputusan percepatan (crash) dengan pertukaran waktu-biaya | Mubarak bab 8 PDF 243 | Menjanjikan percepatan tanpa angka DITOLAK |
| Ketentuan klaim perpanjangan waktu Indonesia | SYARAT KONTRAK SETEMPAT (bukan rak) | Memakai istilah kontrak Amerika dari Mubarak sebagai dasar klaim DITOLAK [Mubarak:55-56] - DISINI MATA 2 PUTUS UNTUK KONTEKS ID |

#### Mata 3 - Perhitungan

Urutan tertelusur (hasil = PROJECT-DERIVED [REF-CON-001..003 seksi 6]):

1. Tetapkan lingkup + breakdown pekerjaan [Holm bagian I-II, PDF 30-90].
2. Hitung volume dari gambar (quantity take-off) [Holm PDF 90].
3. Produktivitas alat/tenaga: taksiran umum buku [R3] WAJIB disetel lembar data alat [R4] +
   kondisi lapangan; tanpa keduanya = ASSUMPTION + sensitivitas + rencana penggantian
   [Peurifoy:53-54; aturan asumsi pustaka-teknis].
4. Biaya kepemilikan/operasi alat per jam [Peurifoy bab 2] - masukan harga lokal, BUKAN dolar
   buku.
5. Harga satuan pekerjaan: dari AHSP/SNI/survei pasar - TIDAK ADA DI RAK (GAP-019); selama
   absen, angka HSP ditandai ASSUMPTION dengan sumber disebut (AHSP edisi mana / survei mana /
   penawaran siapa).
6. Penyelesaian estimasi: langsung + upah + overhead + laba + risiko [Holm bagian V, PDF 234].
7. Jadwalkan: CPM forward/backward [Mubarak PDF 65] lalu perataan sumber daya [PDF 149] lalu
   bila perlu crash, kurva waktu-biaya [PDF 243].
8. Mutakhirkan berkala dengan dasar pembanding terjaga [Mubarak PDF 183].

Peringatan silang: durasi TIDAK dipasok Mubarak [Mubarak:52-53]; mata 3 jadwal bergantung mata 3
biaya-produktivitas. KATALOG-RUMUS tanpa baris domain ini (terukur) - jembatan hitungan resmi
belum dibangun (KD-N4, usulan U-2).

#### Mata 4 - Pengujian - MATA YANG PUTUS

| Butir | Ambang | Sumber |
|---|---|---|
| Kebenaran volume take-off | Rekonsiliasi gambar + uji hitung orang kedua | Metode internal [R3] + gate G3 |
| Wajar tidaknya harga satuan | Pembanding >= 2 penawaran/AHSP resmi | TIDAK ADA DI RAK - GAP-019 |
| Produktivitas terlaksana vs rencana | Kurva nyata proyek (data sendiri) | bukan norma; R3 hanya metode |
| Mutu hasil pekerjaan sipil (beton/urugan/padatan) | Ambang SNI/ASTM | tidak dapat diuji dari domain ini - ranah rantai K (putus juga) + GAP-020 |
| Kelayakan jadwal (logika CPM) | Aturan jaringan | R3 metode - sah sebagai metode, BUKAN ambang |
| Kesesuaian RAB dengan AHSP/SNI | tidak dapat dinyatakan | Regulasinya tidak ada di rak |
| Kepatuhan K3 konstruksi | tidak dapat diuji | Permenaker tidak ada |

Tiga baris terakhir yang membuat rantai ini putus; dua di antaranya justru yang paling sering
dijanjikan dokumen penawaran (RAB "sesuai AHSP" dan komitmen K3).

##### Yang boleh dan tidak boleh dikatakan

| Boleh | Tidak boleh |
|---|---|
| "Struktur estimasi mengikuti bagian I-V Holm & Schaufelberger [R3, PDF 30-234]; harga satuannya dari AHSP edisi X / survei pasar Y (lampiran terpisah)." | "RAB disusun dengan harga satuan Holm." (konteks Amerika Utara + usang) |
| "Produktivitas alat memakai taksiran umum [R3, Peurifoy bab 2-9] yang disetel lembar data alat (terlampir)." | ~~"Produktivitas excavator 0,8 m3/jam."~~ tanpa R4 = angka dari awan |
| "Jadwal CPM mengikuti metode Mubarak [R3, PDF 65]; ketentuan perpanjangan waktu mengikuti syarat kontrak ini." | "Klaim EOT kami sesuai praktik kontrak internasional." |
| "Metode taksiran boleh dikutip dari rak." | SATU KALIMAT PUN "harga satuan sesuai AHSP/SNI" bersandar pada rak (uji penolakan V-10) |

#### Mata 5 - Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| Dokumen struktur estimasi berlabel ketelitian (tahap apa, akurasi berapa) | ya | Holm bagian I |
| Lembar perhitungan volume (take-off) tertelusur gambar | ya | Holm PDF 90 |
| Sumber harga satuan yang dipakai (salinan AHSP / surat penawaran / hasil survei) | ya | lampiran eksternal - TIDAK dapat digantikan rak |
| Hitungan sewa-vs-beli alat + lembar data alat [R4] | ya | Peurifoy bab 2 |
| Jadwal dasar beku + log pemutakhiran | ya | Mubarak bab 7; G6 |
| Dokumen pertukaran waktu-biaya untuk persetujuan percepatan | bila ada | Mubarak bab 8 |
| PERNYATAAN STANDAR YANG DIPAKAI (AHSP edisi/SNI mana, atau bahwa belum ada dan siapa yang menetapkan) | ya | pola rantai K [RANTAI-K:137] |
| Kartu kendali rantai berstatus "putus di mata 4" | ya | kejujuran status = isi |

#### Status rantai

"METODE LENGKAP - ANGKA & NORMA TIDAK ADA". Satu celah terdaftar mengikat (GAP-019, MENENGAH) +
dua keabsenan turunan (K3 yatim; ambang mutu milik rantai K). Menutup GAP-019 membuat MATA 3-4
harga bersandar R1 tetapi TIDAK membuat rantai utuh (ambang mutu tetap milik rantai K; K3 tetap
butuh regulasi; R4 tetap per proyek) - redaksi bertingkat, jangan klaim "sekali tutup jadi utuh"
(preseden KD-C9 sipil).
