---
id: networking-korpus-ekas-0923
type: catatan
title: Korpus NETWORKING EKAS - peta, rumus, ambang, dan batas pengetahuan (NWSKILL-0923)
status: active
sumber: "docs/2026-09-23-nws-knowledge-register/research/networking-korpus-detail.md (hulu: 14 berkas ekas/ wajib dibaca penuh + 7 pendukung, terdaftar di Bagian 1 objek)"
halaman: "marker [R-n, sumber, hal] per butir di body: PDF 769 dan 647 (Fall & Stevens - BDP, window scaling; varian 770/766 = known-defect K-1/K-2); PDF 655-664, 651, 187, 679 (Fall & Stevens); PDF 51-75, 89, 107, 207, 441, 463 (Network Warrior - teratribusi ke Odom di rantai I, K-3); PDF 618 (Limoncelli); PDF 34 (BS EN 62676-1-2 - known-defect warisan VSSKB); PDF 46-70 (Troppens, rujukan silang STORAGE); PDF 277, 290 (Damjanovski, rujukan silang VSS)"
tanggal_akses: 2026-09-24
kelas_bukti: sintesis
sensitif: tidak
perkara: nwskill-0923
tags: [networking, jaringan, vlan, poe, bdp, tcp, window-scaling, switch, router, subnetting, lebar-pita, throughput, rtt, latensi, anggaran-poe, uji-kabel]
links: [faktas/waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2, ekas/05_DOMAIN-KNOWLEDGE/NETWORKING, ekas/05_DOMAIN-KNOWLEDGE/STORAGE, docs/2026-09-23-nws-knowledge-register/research/networking-korpus-detail.md]
defek-terkait: faktas/waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2.md ditandai known-defect oleh gsp-librarian 2026-09-23 (VSSKB-0923)
penulis: gsp-infra-specialist
diajukan: 2026-09-24
domain: NETWORKING
created: 2026-09-24
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-24
riwayat-catatan-verifikasi: "Verdict: perlu_revisi. || Alasan spesifik: (a) Bagian 1.3 jangkar 'MASTER-REFERENCE-REGISTER.csv :58-62' salah untuk REF-NET-001..004 dan REF-OPS-001 yang nyata duduk di baris 13-17 (hanya REF-OEM-NET di :59 yang benar; galat terwarisi dari studi hulu Bagian 1.3); (b) Bagian 1.5 sel 'Ukuran dilaporkan resume' untuk Fall & Stevens berbunyi 'jumlah hal tidak dilaporkan studi' padahal resume baris 4 melaporkan '1.059 halaman, 11,4 MB'; (c) skema beku G-1 seksi 8 menuntut blok CATATAN DEFECT Tabel 7 di RANTAI-JAMINAN.md:112 dikutip UTUH ke objek, tetapi objek hanya membawa parafrasa plus rujukan blok sehingga penanda 'Blok penuh: R2 - BS EN 62676-1-2.md (CATATAN DEFECT) + wiki/catatans/vss-korpus-ekas-0923.md sub-seksi Batas angka Tabel 7' hilang; (d) jangkar baris lapis bersama (KATALOG-RUMUS :387-400/:390/:541/:564-567, ASUMSI-BAKU :95-107/:103/:148-149, AMBANG-TERIMA :51-58/:76/:85-94) benar pada state rak saat ekstraksi tetapi bergeser oleh tambalan D2 13:55, D3 14:08, D4 14:18 setelah objek ditulis 14:07 - objek baru mendeklarasikan basis baris untuk RANTAI-JAMINAN, bukan untuk lapis bersama. || Rekomendasi konkret untuk penulis/librarian: (1) ganti jangkar register menjadi ':13-17 (REF-NET-001..004, REF-OPS-001) dan :59 (REF-OEM-NET)'; (2) isi sel Fall & Stevens dengan '1.059 halaman, 11,4 MB [R3, resume TCP-IP Illustrated, baris 4]'; (3) tempel kutipan verbatim blok CATATAN DEFECT :112 (termasuk penanda Blok penuh) ke Bagian 5 atau Bagian 8 sesuai skema seksi 8; (4) tambah satu baris batas-waktu: 'jangkar baris lapis bersama memakai state rak 2026-09-24 sebelum tambalan D2/D3/D4'. Dimensi lain lolos ukur: 25+ marker provenans terverifikasi ke berkas rak nyata, tags == daftar beku G-1 byte-per-byte (16 token), title == H1, YAML utuh tanpa kunci duplikat, non-ASCII = 0, seluruh jalur rak nyata, K-1..K-12 naik utuh dengan predikat, aritmetika 2.3 cocok, bentuk lama tidak dihapus diam-diam."
revisi-oleh: gsp-librarian
revisi-pada: 2026-09-24
catatan_keputusan: "dipromosikan: NWSKILL-0923 D1-L2: gerbang format librarian 10/10 PASS (validator mandiri + red-green), verdict custodian terlampir di catatan_verifikasi, non-sensitif non-dosir; known-defect K-1/K-2/K-3 + Tabel 7 ditandai BELUM TERKONFIRMASI terhadap PDF primer"
catatan_verifikasi: "Verdict: terverifikasi. || Re-verifikasi iterasi 2/3 atas empat perbaikan revisi librarian (fokus re-verifikasi bukan audit 7 dimensi ulang): T-1 LOLOS - sel Bagian 1.5 Fall & Stevens kini '1.059 halaman, 11,4 MB [R3, resume TCP-IP Illustrated, baris 4]' dan cocok dengan ekas/05_DOMAIN-KNOWLEDGE/NETWORKING/R3 - TCP-IP Illustrated Vol 1.md baris 4; T-2 LOLOS - jangkar MASTER-REFERENCE-REGISTER.csv :13-17 memuat REF-NET-001..004 dan REF-OPS-001 serta :59 memuat REF-OEM-NET (ukur langsung csv 63 baris), bentuk lama :58-62 hilang dari body dan hanya tersisa di riwayat; T-3 LOLOS - blok CATATAN DEFECT dikutip byte-per-byte identik dengan NETWORKING/RANTAI-JAMINAN.md:112 (431 char, md5 2699c73ad6c6) termasuk penanda 'Blok penuh:'; rujukan 'di atas' dalam kutipan diterima karena pembuka 'Kutipan verbatim ... :112' menyatakan basis barisnya; T-4 LOLOS - baris Batas-waktu Bagian 1.3 mendeklarasikan jangkar lapis bersama memakai state rak sebelum tambalan D2/D3/D4 dan angka kini 613/186/116 terukur cocok hari ini (KATALOG-RUMUS/ASUMSI-BAKU/AMBANG-TERIMA). Regresi LOLOS: yaml.safe_load aman; uji banding mentah-vs-parse per kunci bersih (kelas potong-# nol); satu baris status; nol dup kunci; title==H1; tags==16 token beku G-1 byte-per-byte; non-ASCII total 0; anatomi 8 bagian utuh; riwayat-catatan-verifikasi memuat verdict iterasi-1 utuh; diff body vs backup-pra-revisi-iter1 tepat 5 hunk seluruhnya terjelaskan 4 suntingan (65a66,70; 74c79; 93c98; 495c500; 498a504,507) tanpa penghapusan diam-diam. Batas verdict: ini verifikasi kualitas lapis teks - vonis halaman PDF primer dan putusan K-9/K-12 tetap wewenang manusia; promote vault ke wiki tetap kewenangan gsp-librarian."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-24
dipromosikan-ke: catatans/networking-korpus-ekas-0923.md
---

# Korpus NETWORKING EKAS - peta, rumus, ambang, dan batas pengetahuan (NWSKILL-0923)

Objek master misi NWSKILL-0923 (id `networking-korpus-ekas-0923`, type catatan, domain
NETWORKING = D1). Muatan = peta rak + rumus + angka acuan + kerangka hitung + ambang terima +
register kontradiksi + celah resmi + batas kemampuan, dalam satu berkas (granularitas SATU
objek master per domain sesuai skema beku G-1 seksi 1).

Provenans: body ini disalin terpadatkan dari SATU sumber,
`docs/2026-09-23-nws-knowledge-register/research/networking-korpus-detail.md` (studi
t_4f44563f status complete, 714 baris, ekstraksi read-only dari lapisan teks `ekas/` oleh
gsp-infra-specialist pada 2026-09-24). Tidak ada pembacaan ulang korpus untuk angka baru pada
giliran ini; satu-satunya bacaan langsung rak di giliran L1 adalah verifikasi ulang
`NETWORKING/RANTAI-JAMINAN.md` pasca-tambalan D1-FIXx (lihat catatan pergeseran baris Bagian 1).
Kelas bukti objek: sintesis - kekuatan utama R3 buku teks; R2 hanya lewat ambang warisan
BS EN 62676-1-2 (berstatus known-defect); R4 per proyek (anggaran PoE, kapasitas switching).
Kelas bukti berbeda dicampur dalam satu berkas; pemisahannya ditegakkan lewat penanda
`[R-n, sumber, hal]` per butir dan blok BATAS PENGETAHUAN di Bagian 8. Yang tidak ada di rak
dinyatakan "tidak ada di rak".

Catatan wewenang: tidak ada PDF primer yang dibuka pada misi ini. Semua vonis halaman adalah
vonis LAPISAN TEKS memakai aturan offset rak sendiri; penutup akhir wewenang manusia.

---

## Bagian 1 - Peta isi

Path memakai NAMA FOLDER NYATA di disk (kontrak jalur G-1 seksi 6). Label katalog berbentuk
`R3/NETWORK/` dan `R4/NETWORK/` adalah label laci, BUKAN path; padanan nyatanya dicantumkan
(butir K-11). Uji keberadaan = baca langsung/ls, bukan glob.

### 1.1 Lapis domain `ekas/05_DOMAIN-KNOWLEDGE/NETWORKING/` (6 berkas)

| Berkas | Peran | Tingkat R | Ukuran nyata |
|---|---|---|---|
| `RANTAI-JAMINAN.md` | Rantai I, urutan kerja mata 1-5 jaringan IP penopang sistem | peta pengetahuan | 9.182 B, 148 baris (pasca-tambalan D1-FIXx; studi mengukur 6.744 B / 140 baris sebelum tambalan) |
| `R3 - TCP-IP Illustrated Vol 1.md` | Resume Fall & Stevens; rujukan tingkat paket | R3 | 9.126 B, 192 baris |
| `R3 - CCNA 200-301 Official Cert Guide Library.md` | Resume Odom/Hucaby/Gooley; kurikulum sertifikasi | R3 | 3.530 B, 89 baris |
| `R3 - Computer Networking A Top-Down Approach.md` | Resume Kurose & Ross; dasar teori | R3 | 3.733 B, 96 baris |
| `R3 - Network Warrior.md` | Resume Donahue; praktik lapangan Cisco | R3 | 4.756 B, 112 baris |
| `R3 - The Practice of System and Network Administration.md` | Resume Limoncelli dkk.; praktik operasional TI | R3 | 4.211 B, 110 baris |

Pergeseran baris `RANTAI-JAMINAN.md`: dokumen studi dan skema G-1 mengutip nomor baris versi
prapatch (140 baris). Setelah tambalan CATATAN DEFECT D1-FIXx (hanya-tambah), posisi kini:
sitasi BDP `:64` -> `:70`; window scaling `:70` -> `:76`; contoh agregat `:74-81` -> `:82-89`;
ambang Tabel 7 `:101-103` -> `:109-111`; blok defect VSSKB `:104` -> `:112`; status rantai
`:128` -> `:136`; peringatan usia `:138-139` -> `:146-148`. Blok defect baru D1-FIXx duduk di
`:23-25`, `:40`, `:78`. Body ini mengutip nomor BARU (terverifikasi baca ulang giliran L1).

### 1.2 Lapis kartu `ekas/04_KNOWLEDGE-CARDS/NETWORKING/` (6 kartu, satu templat enam seksi)

| Kartu | R | Bobot rujukan | Halaman jangkar | Boleh tetapkan ambang | Batas pemakaian |
|---|---|---|---|---|---|
| `REF-NET-001.md` | R3 | Network Warrior - pola gangguan | kosong (:24) | tidak sendirian, hanya bila kontrak mengadopsi tertulis (:37) | terbit 2011, platform tidak dijual lagi (:41) |
| `REF-NET-002.md` | R3 | CCNA 200-301 - praktik terkini | kosong (:24) | idem | edisi 2019 diklaim di `_arsip` (:41; lihat K-10) |
| `REF-NET-003.md` | R3 | Kurose & Ross - dasar jaringan | kosong (:24) | idem | edisi 7 (2017) (:41) |
| `REF-NET-004.md` | R3 | TCP/IP Illustrated - window scaling wajib bila BDP > 64 kB | PDF 647, 769 (:24) | idem | membahas protokol, BUKAN perencanaan kapasitas (:41) |
| `REF-OEM-NET.md` | R4 | lembar data jaringan/PBX/interkom, 28 berkas (:13) | n/a (kartu laci) | ya untuk parameter produk (:25) | hanya model+firmware tercantum; cocokkan tanggal terbit (:31-37) |
| `REF-OPS-001.md` | R3 | Limoncelli - praktik operasional | kosong (:24) | idem | tidak memasok ambang teknis (:41) |

Struktur: 5 dari 6 kartu TANPA halaman jangkar - hanya REF-NET-004 yang bisa diuji alamatannya
otomatis. Bukan cacat templat, tetapi batas verifikasi otomatis domain ini.

### 1.3 Lapis bersama (baris terkait jaringan)

> Batas-waktu: jangkar baris lapis bersama di bawah memakai state rak 2026-09-24 SEBELUM
> tambalan D2/D3/D4 (saat ekstraksi: KATALOG-RUMUS 571 baris, ASUMSI-BAKU 180, AMBANG-TERIMA
> 107; kini 613/186/116 - posisi dapat bergeser, isi terverifikasi saat ekstraksi). Deklarasi
> basis baris RANTAI-JAMINAN terpisah ada di Catatan pergeseran Bagian 1.1.

| Berkas | Baris | Yang dipasok |
|---|---|---|
| `ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md` (571 baris, 23.219 B) | :51, :387-400 | indeks cepat BDP (PDF 769); seksi 11 Jaringan: BDP cetak 730/PDF 769; window scaling cetak 608/PDF 647; penegasan offset +39 (:390) |
| idem | :35, :97-105 | `Mb/s = MB/s x 8` (Damjanovski PDF 290) - pemasok angka bitrate mata 3 rantai I |
| idem | :541 | celah: rumus perencanaan kapasitas jaringan TIDAK ADA |
| `ekas/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md` (180 baris, 9.908 B) | :95-107, :148-149 | seksi E bitrate per kamera, faktor gerak 2-3 kali lipat (:103); waktu deteksi hilang sinyal 8/4/2 PDF 34 (:148) + CATATAN DEFECT (:149). Seksi A-F TIDAK punya seksi jaringan - lihat G-5 |
| `ekas/07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md` (107 baris, 6.602 B) | :21-22, :41, :46-47, :51-58, :76, :85-94 | detail Bagian 4-5 objek ini |
| `ekas/02_REGISTERS/GAP-REGISTER.csv` | :6, :12, :14, :15 | GAP-005, GAP-011, GAP-013, GAP-014 (Bagian 6) |
| `ekas/02_REGISTERS/MASTER-REFERENCE-REGISTER.csv` | :13-17 (REF-NET-001..004, REF-OPS-001) dan :59 (REF-OEM-NET) | REF-NET-001..004 + REF-OPS-001 = R3 `no-unless-contract-adopts`; REF-OEM-NET = R4 aktif 28 berkas [peta rak, ukur ulang giliran revisi 2026-09-24] |
| `ekas/00_START-HERE/README.md` | :34-38, :47 | keadaan rak R1=0 R2=5 R3=24 R4=0 R5=8; alasan R4 by-design (Bagian 8) |

### 1.4 Lapis laci sumber (keberadaan fisik terukur)

| Laci nyata | Klaim `_ISI.md` | Baris tabel terhitung | Cocok? |
|---|---|---|---|
| `ekas/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/NETWORK/` | 4 berkas (:3) | 4 | ya |
| `ekas/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/OPERATIONS/` | 1 berkas (:3) | 1 | ya |
| `ekas/03_SOURCE-VAULT/R4_OEM-TECHNICAL/NETWORK/` | 28 berkas (:3) | 28 | ya (komposisi timpang - G-13) |
| `ekas/03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/TIA/` | "Kosong." (:3) | 0 | ya - konfirmasi independen GAP-011 |

Keberadaan PDF fisik keempat buku R3 jaringan terkonfirmasi juga di vault nyata
`C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/NETWORK/`.

### 1.5 PDF primer (verifikasi halaman = wewenang manusia; agen bekerja dari lapisan teks)

| Buku | Edisi/tahun | Ukuran dilaporkan resume | Konvensi halaman (beku G-1 seksi 7) |
|---|---|---|---|
| Fall & Stevens, *TCP/IP Illustrated Vol 1* | 2012 | 1.059 halaman, 11,4 MB [R3, resume TCP-IP Illustrated, baris 4] | selisih TETAP cetak + 39 = PDF (satu-satunya konvensi sah) |
| Odom dkk., *CCNA 200-301 Official Cert Guide Library* | 2024 | 3.292 halaman, 144,8 MB [R3, resume CCNA, baris 4] | nomor PDF langsung |
| Kurose & Ross, *Computer Networking: A Top-Down Approach* | ed. 7, 2017 | 867 halaman, 20,0 MB [R3, resume Kurose, baris 4] | nomor PDF langsung |
| Donahue, *Network Warrior* | 2011 | 785 halaman, 8,1 MB [R3, resume Network Warrior, baris 4] | nomor PDF langsung |
| Limoncelli, Chalup, Kothari, *The Practice of System and Network Administration* | ed. 3, 2017 | 1.225 halaman, 13,4 MB [R3, resume Practice, baris 5] | nomor PDF langsung |

Domain tetangga yang memasok materi terkait (rujukan silang saja, TIDAK disalin - putusan P-8):
`ekas/05_DOMAIN-KNOWLEDGE/STORAGE/RANTAI-JAMINAN.md` (mitra F-3: BDP/window scaling + RAID),
`ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/` (bitrate Damjanovski, ambang Tabel 7),
`ekas/05_DOMAIN-KNOWLEDGE/CYBERSECURITY/` (rantai J, kata sandi bawaan ditolak).

---

## Bagian 2 - Rumus dan angka acuan

Setiap rumus dan angka membawa penanda sumbernya sendiri bentuk koma. Jangan memakai ulang satu
butir tanpa penandanya. Jalur baris merujuk lapis teks rak relatif shared workspace.

### 2.1 Rumus inti domain

```
BDP = RTT x kapasitas tautan penyempit
```
[R3, TCP-IP Illustrated Vol 1, PDF 769] (cetak 730; `R3 - TCP-IP Illustrated Vol 1.md:122,128`).
VARIANT YANG DICACAT: `NETWORKING/RANTAI-JAMINAN.md:70` mengutip PDF 770 - lihat K-1, bentuk
lama TIDAK dihapus, ditandai. Kapasitas yang dipakai adalah kapasitas TAUTAN TERKECIL sepanjang
jalur pengirim ke penerima, bukan kapasitas nominal langganan
[R3, TCP-IP Illustrated Vol 1, PDF 769].

```
Window scaling wajib aktif di kedua ujung bila BDP > 64 kB
```
[R3, TCP-IP Illustrated Vol 1, PDF 647] (cetak 608, bagian 13.3.3;
`R3 - TCP-IP Illustrated Vol 1.md:147,153`; `KATALOG-RUMUS.md:399-400`; `REF-NET-004.md:22,24`).
VARIANT YANG DICACAT: `NETWORKING/RANTAI-JAMINAN.md:76` mengutip PDF 766 - lihat K-2.
Penyelesaiannya Window Scale option, BUKAN menambah langganan
[R3, TCP-IP Illustrated Vol 1, PDF 647].

```
Mb/s_total = Sigma (bitrate per kamera) x faktor_puncak
```
[R3, peta rantai NETWORKING/RANTAI-JAMINAN.md:52-58] - bukan rumus buku. Bitrate
per kamera dari rantai B (VIDEO-SURVEILLANCE), nilai nyatanya [R4] atau hasil ukur instalasi
percobaan. Faktor puncak diperlukan karena rekaman berkorelasi (`:57-58`). GAGAL TATA KELOLA:
`faktor_puncak` tidak terdaftar di ASUMSI-BAKU - lihat G-5, Bagian 8 butir 6.

```
P_total_dibutuhkan = Sigma (daya per perangkat x faktor_rugi_kabel)  harus <= anggaran PoE switch
```
[R3, peta rantai NETWORKING/RANTAI-JAMINAN.md:62-65] - sisi kanan WAJIB [R4].
`faktor_rugi_kabel` juga tidak terdaftar di ASUMSI-BAKU (G-5).

```
RAID 5 = (n-1) x C   ;   RAID 6 = (n-2) x C
```
[R3, Troppens, PDF 46-70] via `KATALOG-RUMUS.md:47` dan `AMBANG-TERIMA-INDUK.md:42`. Milik
domain STORAGE (D5); dirujuk silang oleh rantai I untuk penyimpanan rekaman, tidak disalin.

```
Mb/s = MB/s x 8 ;  GB = Mb/s / 8 x 3600 x jam/hari x hari x jumlah kamera / 1000
```
[R3, Damjanovski, PDF 277, 290] via `KATALOG-RUMUS.md:35,100-101`. Milik rantai B; pemasok
angka bitrate yang dikonsumsi mata 3 rantai I.

### 2.2 Angka acuan per buku (salinan persis + jalur baris)

| Angka | Nilai persis di rak | Penanda + jalur |
|---|---|---|
| Konversi halaman Fall & Stevens | "halaman cetak + 39 = halaman PDF" | [R3, resume TCP-IP Illustrated, baris 8] |
| Contoh konversi | TIME_WAIT cetak 618 = PDF 657 | [R3, resume TCP-IP Illustrated, baris 8-9] |
| TIME_WAIT | menunggu dua kali Maximum Segment Lifetime (MSL); tiap implementasi memilih MSL sendiri | [R3, TCP-IP Illustrated Vol 1, PDF 655-664; resume baris 59-60,66] |
| Path MTU Discovery untuk TCP | bagian 13.4, cetak 612 / PDF 651 | [R3, TCP-IP Illustrated Vol 1, PDF 651; resume baris 88] |
| PMTU (bab) | cetak 148 / PDF 187 | [R3, TCP-IP Illustrated Vol 1, PDF 187; resume baris 81] |
| Jacobson (dasar slow start + congestion avoidance) | cetak 731 / PDF 770 | [R3, TCP-IP Illustrated Vol 1, PDF 770; resume baris 72] - halaman yang oleh rantai I dikutip untuk BDP (K-1) |
| SYN flood dalam konteks retransmisi | cetak 640 / PDF 679 | [R3, TCP-IP Illustrated Vol 1, PDF 679; resume baris 115-116] - label bab bergeser, lihat K-5 |
| Contoh BDP | tautan 100 Mb/s, RTT 40 ms -> 100.000.000 / 8 x 0,040 = 500.000 byte kira-kira 500 kB | [R3, TCP-IP Illustrated Vol 1, PDF 769; resume baris 136-137] - aritmetika teruji cocok persis (2.3) |
| Throughput tanpa window scaling | jendela 64 kB -> 64 kB / 0,040 s kira-kira 1,6 MB/s kira-kira 13 Mb/s vs kapasitas 100 Mb/s | [R3, TCP-IP Illustrated Vol 1, PDF 769; resume baris 139-141] - muat di kedua basis (2.3) |
| Batas cakupan Fall & Stevens | "tidak memuat rumus perancangan kapasitas jaringan" | [R3, resume TCP-IP Illustrated, baris 158-160] |
| Struktur CCNA dua jilid satu PDF | Volume 1 mulai PDF 9; Volume 2 mulai PDF 1936 | [R3, CCNA 200-301 Library, PDF 9 dan 1936; resume baris 8-9] |
| Ketebalan CCNA | 3.292 halaman, 144,8 MB | [R3, resume CCNA, baris 4] - klaim peringkat terbantahkan, lihat K-6 |
| Bookmark CCNA | 750 entri | [R3, resume CCNA, baris 32,86] |
| Edisi 2019 CCNA | diklaim diarsipkan `_arsip/`, 1.813 halaman, 38,1 MB | [R3, resume CCNA, baris 83-85] - jejak fisik nihil, lihat K-10 |
| Peta bab Kurose | Bab 1 PDF 31, Bab 2 PDF 113, Bab 3 PDF 217, Bab 4 PDF 335, Bab 5 PDF 403, Bab 6 PDF 469, Bab 7 PDF 549, Bab 8 PDF 623, Bab 9 PDF 705 | [R3, Computer Networking Top-Down, PDF 31-705; resume baris 22-30] |
| Peta bab Donahue | VLAN 51, Trunking 63, VTP 75, Link Aggregation 89, Spanning Tree 107, First Hop Redundancy 207, Access Lists 441, Authentication 463 | [R3, Network Warrior, PDF 51-463; resume baris 26-36] - sebagian teratribusi ke Odom di rantai I, lihat K-3 |
| Penyebab tersering tautan lambat | duplex mismatch - satu sisi dipaksa, sisi lain otomatis | [R3, Network Warrior, PDF 45 (Bab 3); resume baris 45,48-49] |
| Proses perubahan Limoncelli | Bagian VII, PDF 618 | [R3, Practice of System and Network Administration, PDF 618; resume baris 31,45] |
| Ambang PoE salah kaprah | "Switch 24 port PoE+ tidak berarti sanggup memberi 30 W ke 24 port sekaligus" | [peta rak, NETWORKING/RANTAI-JAMINAN.md:42-44] |
| Rugi kabel PoE | bertambah pada jarak mendekati 100 m; perangkat di ambang kelasnya gagal menyala pada ujung jauh | [peta rak, NETWORKING/RANTAI-JAMINAN.md:67-68] |
| Contoh agregat terhitung | 40 kamera, 4 Mb/s, faktor puncak 1,5 -> 240 Mb/s; uplink 1 Gb/s memadai | [hitungan rancangan, NETWORKING/RANTAI-JAMINAN.md:82-89] - aritmetika cocok persis (2.3); faktor 1,5 tak bersandar (G-5) |
| Ambang normatif tunggal rantai I | waktu deteksi hilangnya sinyal 8 / 4 / 2 detik | [R2, BS EN 62676-1-2, PDF 34; NETWORKING/RANTAI-JAMINAN.md:109-111] - KNOWN-DEFECT, lihat Bagian 5 blok Tabel 7; JANGAN dipakai sebagai ambang sah |
| Usia buku | Fall & Stevens (2012) dan Donahue (2011) melewati 14-15 tahun | [peta rak, NETWORKING/RANTAI-JAMINAN.md:146-148] |

### 2.3 Uji aritmetika deterministik atas angka rak (dijalankan sebagai perintah nyata pada giliran studi)

| Uji | Hasil ukur | Klaim rak | Vonis |
|---|---|---|---|
| `100000000/8*0.040` | 500000 byte | 500.000 byte (resume TCP-IP:137) | cocok persis |
| `64*1000/0.040` | 1.600.000 B/s = 12,80 Mb/s | "kira-kira 1,6 MB/s kira-kira 13 Mb/s" | cocok dalam pembulatan (kB desimal) |
| `64*1024/0.040` | 1.638.400 B/s = 13,11 Mb/s | idem | cocok (KiB biner); rak tidak menyatakan basis, keduanya muat |
| `40*4*1.5` | 240,0 | 240 Mb/s (RANTAI:85) | cocok persis |
| Offset cetak+39 pada 20 baris peta bab Fall & Stevens | 20 diperiksa, 0 pelanggaran | aturan +39 (resume TCP-IP:8; KATALOG:390) | konsisten internal - dasar adjudikasi K-1/K-2 |
| `18 + 187` | 205 | "Bookmark 207 entri (18 bab + 187 sub-bab)" (resume TCP-IP:9) | TIDAK cocok, selisih 2 - lihat K-4 |
| Letak cetak 640 dalam bab | masuk rentang Bab 13 (cetak 595-646); Bab 14 retransmisi mulai cetak 647 | label "konteks retransmisi" (resume TCP-IP:115-116) | label topik bergeser satu bab - lihat K-5 |

---

## Bagian 3 - Kerangka hitung terapan

### 3.1 Urutan pakai rantai I (lima mata)

Mata 3 (hitungan) berstatus UTUH; mata 4 (ambang uji) sebagian besar berstatus KONTRAK, bukan
standar - status dicetak eksplisit di `NETWORKING/RANTAI-JAMINAN.md:136`.

1. Tentukan kebutuhan: jumlah kamera, bitrate per kamera (rantai B, [R4] atau hasil ukur),
   segmen, ketersediaan.
2. Hitung lebar pita agregat dengan faktor puncak (3.2).
3. Hitung anggaran PoE terhadap lembar data, bukan terhadap jumlah port (3.3).
4. Periksa BDP setiap jalur jauh; aktifkan window scaling bila lewat 64 kB (3.4).
5. Rancang pemisahan VLAN, redundansi gateway, spanning tree, kapasitas uplink
   (`RANTAI-JAMINAN.md:33-36` - keputusan dengan alternatif ditolak; alamat halaman baris Odom
   dicacatkan K-3, keputusan desainnya TIDAK dibatalkan).
6. Uji dengan cabut kabel, ukur pada puncak, serahkan dengan cadangan konfigurasi (Bagian 4).

### 3.2 Lebar pita agregat (contoh terhitung rak)

Dari `NETWORKING/RANTAI-JAMINAN.md:82-89`, disalin persis:

```
40 kamera, bitrate sedang 4 Mb/s, faktor puncak 1,5:
Mb/s_total = 40 x 4 x 1,5 = 240 Mb/s
```

Aritmetika terverifikasi (2.3). Kesimpulan rak: uplink 1 Gb/s memadai untuk aliran rekam,
TETAPI aliran pemutaran ulang serentak menambah beban ke arah sebaliknya dan harus diperiksa
terpisah (`:88-89`). Catatan hulu yang wajib ikut terbit: faktor 1,5 TIDAK punya sandaran di
ASUMSI-BAKU - daftar asumsi hanya punya "faktor gerak/aktivitas ... bisa 2-3 kali lipat"
(`ASUMSI-BAKU.md:103`) dan tidak mendefinisikan `faktor_puncak` sama sekali (G-5). Contoh 240
Mb/s memakai besaran yang belum terdaftar sebagai asumsi baku. Ini bukan salah hitung; ini
lubang tata kelola angka.

### 3.3 Anggaran PoE (satu-satunya keputusan yang rak tandai "R4 wajib")

Dari `NETWORKING/RANTAI-JAMINAN.md:37,42-44,62-68`:

```
P_total_dibutuhkan = Sigma (daya per perangkat x faktor_rugi_kabel)
harus <= anggaran PoE switch   [R4]
```

Rak menolak dua kebiasaan: menghitung dari jumlah port (`:37`), dan menyamakan jumlah port
dengan daya per port serentak (`:42-44`). Alasan tercetak: "daya total catu hampir selalu lebih
kecil daripada jumlah daya maksimum semua port". Rugi kabel mendekati 100 m membuat perangkat
di ambang kelas dayanya gagal menyala pada ujung jauh meski switch tampak sanggup (`:67-68`).
Kartu laci mengulangi: "Anggaran PoE total sering lebih menentukan daripada jumlah port.
Periksa daya per port dan daya total catu" (`REF-OEM-NET.md:39`). CONTOH TERHITUNG PoE TIDAK
ADA DI RAK - nol angka watt lembar data ditranskripsikan ke lapis teks (G-3).

### 3.4 BDP dan window scaling (kerangka paling siap pakai)

1. Ukur RTT jalur, ambil kapasitas TAUTAN TERKECIL sepanjang jalur (bukan langganan)
   [R3, TCP-IP Illustrated Vol 1, PDF 769].
2. `BDP = RTT x kapasitas_penyempit` [R3, TCP-IP Illustrated Vol 1, PDF 769].
3. Bila BDP > 64 kB, window scaling wajib aktif di kedua ujung
   [R3, TCP-IP Illustrated Vol 1, PDF 647].

Contoh rak (100 Mb/s, RTT 40 ms): BDP 500.000 byte; dengan jendela lama 64 kB throughput satu
aliran mentok di kira-kira 13 Mb/s, sekitar 13 persen kapasitas. Diagnosis rak: "bandwidth
sudah 100 Mb/s tapi transfer tetap lambat" adalah masalah JENDELA, bukan kapasitas
(`R3 - TCP-IP Illustrated Vol 1.md:143-145`). Rantai H menyimpan gejala cerminnya: sering salah
didiagnosis "jaringan kurang cepat" lalu dijawab menambah lebar pita yang tidak menolong
(`STORAGE/RANTAI-JAMINAN.md:53-55`).

### 3.5 Subnetting dan pengalamatan

Resume CCNA menempatkan subnetting IPv4 Volume 1 sebagai "penjelasan paling sistematis yang
ada di rak" (`R3 - CCNA 200-301 Official Cert Guide Library.md:50-54,69`). Fall & Stevens
memasok arsitektur alamat Bab 2 (cetak 31 / PDF 70) dan DHCP Bab 6 (cetak 233 / PDF 272) untuk
pengalamatan massal perangkat lapangan (`R3 - TCP-IP Illustrated Vol 1.md:100-104,173`). Yang
TIDAK ada: satu pun tabel subnet, ambang penggunaan alamat, atau contoh pembagian prefix di
lapis teks - kerangkanya ada, angkanya tidak (G-4).

### 3.6 Hitung yang rak nyatakan TIDAK bisa dikerjakan dari buku ini

`R3 - TCP-IP Illustrated Vol 1.md:158-160`: buku tidak memuat rumus perancangan kapasitas
jaringan (kamera per uplink, oversubscription ratio); cakupannya perilaku protokol.
`KATALOG-RUMUS.md:541` dan `GAP-REGISTER.csv:14` (GAP-013) mencatat celah yang sama.

---

## Bagian 4 - Ambang terima

### 4.1 Tabel uji rantai I (`NETWORKING/RANTAI-JAMINAN.md:95-104`), disalin utuh

| Butir | Ambang | Sumber menurut rak | Kekuatan sandaran |
|---|---|---|---|
| Lebar pita pada uplink saat PUNCAK | di bawah kapasitas rancangan | hitungan mata 3 | hasil hitung (sah bila rincian dilampirkan, `AMBANG-TERIMA-INDUK.md:34-35`) |
| Daya PoE terpakai per switch | di bawah anggaran lembar data | R4 | kuat, tetapi per produk dan per proyek |
| Perangkat menyala pada ujung jauh (mendekati 100 m) | menyala dan stabil | R4 + praktik | setengah normatif |
| Peralihan gateway redundan | beralih tanpa kehilangan rekaman | kontrak | hanya sekuat kesepakatan tertulis |
| Pemulihan setelah lup / cabut kabel | pulih dalam waktu yang ditetapkan | kontrak | angka waktunya TIDAK ada di rak (G-9) |
| Pemisahan VLAN | jaringan pengawasan tidak terjangkau dari VLAN kantor | kontrak | uji bersifat negatif (harus gagal) |
| Tundaan dan kehilangan paket | sesuai kebutuhan sistem video | rantai B - BS EN 62676-1-2 [R2] | ANGKA AMBANGNYA TIDAK ADA di lapis teks (G-2, K-12) |
| Perkabelan terstruktur | peringatan: tidak ada sandaran standar di rak | TIA-568 - GAP-011 | TIDAK SAH |

Uji yang rak sebut paling sering dilewati: CABUT KABEL - "Redundansi yang dibayar hanya terbukti
bekerja bila diuji dengan mencabut, bukan dengan membaca konfigurasi" (`:106-107`).

### 4.2 Satu-satunya ambang normatif rantai I, dan status cacatnya

`NETWORKING/RANTAI-JAMINAN.md:109-111` menetapkan waktu deteksi hilangnya sinyal video
8 / 4 / 2 detik menurut security grade [R2, BS EN 62676-1-2, PDF 34], menyebutnya "satu-satunya
ambang jaringan di rantai ini yang tidak berasal dari kontrak". Blok `CATATAN DEFECT
(VSSKB-0923, 2026-09-23)` di `:112` mengikat padanya: ambang itu KNOWN-DEFECT, berkontradiksi
dengan bentuk empat nilai 8/4/4/2, dan pemetaan per-grade BELUM TERKONFIRMASI terhadap PDF
primer. Bentuk lama TIDAK dihapus dari rak, hanya dianotasi. Angka 8/4/2 dilarang dikutisi
objek mana pun sebagai ambang sah sebelum rekonsiliasi BSI/IEC oleh manusia. Sumber kebenaran
fakta tunggal ini tetap entri wiki `faktas/waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2.md`
(rujukan silang, bukan sumber kebenaran kedua).

### 4.3 Penempatan jaringan di ambang induk (sapuan penuh 107 baris)

Hanya tiga baris substantif menyentuh jaringan: `AMBANG-TERIMA-INDUK.md:21` (deteksi sinyal,
known-defect), `:22` (catatan defect), `:41` (kapasitas rekaman dan lebar pita = ambang hasil
hitung, metode Damjanovski PDF 277, 290 - R3 milik domain tetangga). Bagian "Perlu adopsi
kontrak - bersumber R3": NOL baris jaringan (`:51-58`). Bagian "Belum ada sumber sah": satu
baris perkabelan terstruktur (`:76`). Bagian "Wajib R4" (`:85-94`) tidak menyebut switch/PoE
padahal rantai I menggantungkan PoE ke R4 (K-8). Aturan induk di atas semuanya (`:6-7`,
`:46-47`): R1/R2 sah; R3 hanya bila kontrak mengadopsi tertulis; R5 tidak pernah; metode boleh
R3, angka lulus/tidak-lulus yang tidak dihitung tidak boleh R3.

Kesimpulan jujur: domain jaringan praktis TIDAK terwakili di ambang induk. Kekuatan ambang
jaringan GSP hari ini bertumpu pada hitungan rancangan sendiri dan kontrak tertulis - persis
status rantai di `:136-141`, termasuk instruksinya agar angka lebar pita, waktu pemulihan, dan
pemisahan jaringan MASUK KONTRAK, bukan hanya proposal.

### 4.4 Bukti serah rantai I (`NETWORKING/RANTAI-JAMINAN.md:119-130`)

Sepuluh lampiran wajib: diagram topologi as-built; tabel VLAN, alamat IP, dan port (termasuk
penomoran port fisik); CADANGAN KONFIGURASI + VERSI FIRMWARE; pengukuran lebar pita saat PUNCAK
(bukan rata-rata); laporan daya PoE terpakai per switch; hasil uji cabut kabel dan peralihan
gateway; bukti pemisahan VLAN (percobaan jangkau dari VLAN kantor harus gagal); lembar data
switch/AP [R4]; CATATAN PERUBAHAN KONFIGURASI (Limoncelli [R3, Practice of System and Network
Administration, PDF 618]); kartu kendali rantai satu per besaran. Praktik operasional di
baliknya (Limoncelli Bagian VII PDF 618): konfigurasi dikelola seperti kode, backup sebelum
perubahan, rencana pemulihan keadaan semula, perubahan tercatat - diangkat menjadi lampiran
wajib, bukan anjuran sukarela.

---

## Bagian 5 - Register kontradiksi / known-defect

Dua belas butir, naik utuh dengan predikat. "Kontradiksi terukur" = dua angka berbeda untuk hal
yang sama, keduanya terlihat di lapis teks dan tidak bisa benar bersamaan. "Calon" = perlu
pembacaan PDF primer oleh manusia untuk menutup. SEMUA vonis halaman berstatus BELUM
TERKONFIRMASI terhadap sumber primer sampai manusia membuka PDF; bentuk lama tidak dihapus,
hanya ditandai (rak sudah dianotasi lewat tambalan hanya-tambah D1-FIXx di
`NETWORKING/RANTAI-JAMINAN.md:23-25,40,78`; blok VSSKB `:112`). Sitasi yang dibatalkan tetap
tertulis di sini dengan tanda known-defect + dasar pembatalan.

### K-1. Sitasi halaman rumus BDP: PDF 770 vs PDF 769 (kontradiksi terukur; vonis sementara 769)

| Lapis | Sitasi |
|---|---|
| `NETWORKING/RANTAI-JAMINAN.md:70` (kini, pra-patch `:64`) | "Bandwidth-Delay Product - [R3, Fall & Stevens PDF 770]" - KNOWN-DEFECT |
| `STORAGE/RANTAI-JAMINAN.md:47` | "[R3, Fall & Stevens PDF 769]" |
| `KATALOG-RUMUS.md:51,397` | cetak 730 / PDF 769 |
| `R3 - TCP-IP Illustrated Vol 1.md:122` | cetak 730 / PDF 769 |
| `REF-NET-004.md:24` | halaman jangkar "PDF 647, 769" |

Adjudikasi dari aturan offset rak sendiri: cetak 730 + 39 = 769 (terverifikasi 20/20 baris peta
bab, 0 pelanggaran). PDF 770 = cetak 731, yang oleh resume menunjuk rumusan Jacobson tentang
kendali kemacetan (`R3 - TCP-IP Illustrated Vol 1.md:72`), bukan definisi BDP. Vonis lapis
teks: 769 benar untuk BDP; rantai I salah kutip satu halaman. Empat lapis terhadap satu lapis.
Tetap calon sampai manusia membuka PDF 769/770.

### K-2. Sitasi halaman aturan window scaling: PDF 766 vs PDF 647 (kontradiksi terukur; vonis sementara 647)

| Lapis | Sitasi |
|---|---|
| `NETWORKING/RANTAI-JAMINAN.md:76` (kini, pra-patch `:70`) | "Window scaling wajib bila BDP > 64 kB [PDF 766]" - KNOWN-DEFECT |
| `STORAGE/RANTAI-JAMINAN.md:53` | "[PDF 647]" |
| `R3 - TCP-IP Illustrated Vol 1.md:147` | cetak 608 / PDF 647 |
| `KATALOG-RUMUS.md:400` | cetak 608 / PDF 647 |
| `REF-NET-004.md:24` | "PDF 647, 769" |

PDF 766 = cetak 727 = awal Bab 16 Kendali Kemacetan; aturan window scale tinggal di bagian
13.3.3 (cetak 608 / PDF 647). Vonis lapis teks: 647 benar; rantai I salah kutip ke bab
tetangga. Pola K-1 dan K-2 identik dan searah (dua-duanya di baris BDP rantai I), menyarankan
satu suntingan hulu yang keliru, bukan dua kekeliruan bebas. Ini juga butir F-3 yang menaut
D1 dan D5 (satu buku Fall & Stevens dipakai kedua domain).

### K-3. Nomor halaman Donahue disematkan ke Odom (kontradiksi terukur lintas atribusi)

Baris rujukan rantai I (`NETWORKING/RANTAI-JAMINAN.md:15`) menulis: Odom, CCNA 200-301 (2024),
VLAN & trunking / spanning tree / redundansi gateway, "PDF 51-75, 107, 207"; keputusan desain
`:33, :34, :35` mengulang atribusi yang sama. Nomor itu persis peta isi NETWORK WARRIOR:
Bab 4 VLANs 51, Bab 5 Trunking 63, Bab 6 VTP 75 (rentang 51-75), Bab 8 Spanning Tree 107,
Bab 13 First Hop Redundancy 207 (`R3 - Network Warrior.md:26-36`). Sebaliknya resume CCNA TIDAK
memuat satu pun jangkar halaman selain Volume 1 = PDF 9 dan Volume 2 = PDF 1936
(`R3 - CCNA 200-301 Official Cert Guide Library.md:8-9,20-23`); angka 51, 107, 207 tidak muncul
di sana. Baris rantai I yang sama (`:18`) memberi Donahue hanya "PDF 89" (Link Aggregation).
Vonis lapis teks: tiga jangkar halaman milik Donahue dilaporkan atas nama Odom. Dampak hilir
nyata: verifikasi klaim desain VLAN/STP/gateway yang membuka CCNA pada halaman itu mendarat di
materi yang salah - kelas cacat sama dengan Tabel 7 (angka benar, alamat salah). Keputusan
desainnya TIDAK dibatalkan; yang dicacatkan alamat halamannya. Anotasi rak: `:23-25,40`.

### K-4. Komposisi bookmark Fall & Stevens: 207 vs 18 + 187 = 205 (kontradiksi aritmetika internal, belum tertutup)

`R3 - TCP-IP Illustrated Vol 1.md:9`: "Bookmark 207 entri (18 bab + 187 sub-bab)". Terukur:
18 + 187 = 205. Salah satu dari tiga angka keliru. Kandidat penjelasan yang tidak bisa ditutup
dari lapis teks: glossary/index ikut terhitung, atau jumlah sub-bab bertambah setelah koreksi
empat nomor halaman bab (`:190-191`). Perlu pembacaan outline PDF oleh manusia. Bukan angka
beban-rilis teknis, tetapi cacat presisi pada berkas yang sama dengan K-1/K-2.

### K-5. Label topik "konteks retransmisi" untuk cetak 640 (calon, geser satu bab)

`R3 - TCP-IP Illustrated Vol 1.md:115-116` menyebut SYN flood "dibahas di konteks retransmisi
TCP (cetak 640 / PDF 679)". Offset benar (640 + 39 = 679), tetapi cetak 640 jatuh di dalam
Bab 13 TCP Connection Management (mulai cetak 595; Bab 14 TCP Timeout and Retransmission baru
mulai cetak 647). Alamat halaman dan label topik tidak satu bab. Calon; butuh verifikasi manusia.

### K-6. Klaim peringkat berkas CCNA di rak (kontradiksi terukur terhadap laci sumber)

`R3 - CCNA 200-301 Official Cert Guide Library.md:87`: "Berkas 144,8 MB - terbesar kedua di rak
setelah Grounds for Grounding". Terukur dari `_ISI.md` semua laci vault: AutoCAD Electrical
2026 = 177,6 MB; Grondzik & Kwok = 172,8 MB; Professional Practice of Architectural Working
Drawings = 164,5 MB; CCNA = 144,8 MB; Grounds for Grounding = 133,1 MB. Tiga berkas lebih
besar, dan Grounds justru lebih kecil - kedua klausa baris itu salah. Peringkat ketebalan juga
saling meniadakan antar domain: CCNA mengklaim "buku paling tebal di rak (3.292 halaman)"
(`:11`) sementara resume Grondzik mengklaim "buku terbesar di rak ... 1.855 halaman ... hampir
dua kali buku mana pun" (`ekas/05_DOMAIN-KNOWLEDGE/HVAC-BUILDING/R3 - Mechanical and Electrical
Equipment for Buildings (Grondzik & Kwok).md:4,8,10`). Kedua klaim tidak bisa benar bersamaan.

### K-7. Klaim peringkat bookmark Limoncelli (kontradiksi terukur antar domain)

`R3 - The Practice of System and Network Administration.md:8`: "Bookmark bawaan 1.042 entri -
paling rinci kedua di rak setelah Grounds for Grounding". Grounds tercatat 979 entri
(`ekas/05_DOMAIN-KNOWLEDGE/GROUNDING-LIGHTNING/R3 - Grounds for Grounding.md:8,241`) sehingga
urutan "setelah Grounds" salah arah, dan resume Grondzik mengklaim 1.454 entri sebagai
bookmark terbanyak - 1.454 > 1.042. Catatan penenang: angka 2.377 entri yang muncul di sapuan
adalah outline sampah OCR yang sudah dibuang dari Diesel Generator Handbook
(`ekas/05_DOMAIN-KNOWLEDGE/POWER-BACKUP/R3 - Diesel Generator Handbook.md:185`), tidak ikut
dihitung sebagai pemegang rekor.

### K-8. PoE digantungkan ke R4 oleh rantai, tetapi tidak masuk daftar "wajib R4" induk (gap tumpang tindih; beban-rilis)

Rantai I menetapkan anggaran PoE "R4 wajib" (`NETWORKING/RANTAI-JAMINAN.md:37`) dan ujinya R4
(`:98-99`). Bagian "Wajib R4 - tidak ada penggantinya" di ambang induk
(`AMBANG-TERIMA-INDUK.md:85-94`) mendaftar derating genset, efisiensi UPS, DoD baterai, C-rate,
unjuk kerja tulis RAID, waktu rekonstruksi RAID, NETD/IFOV, redaman konektor - TANPA satu pun
butir jaringan (anggaran PoE, kapasitas switching, batas sesi). Bukan kontradiksi angka,
melainkan ambiguitas tata kelola yang membuat angka PoE bisa lolos dari gerbang R4 induk.

### K-9. R4 dihitung "0 sumber" oleh peta, "28 berkas" oleh kartu dan laci (kontradiksi semantik; butuh putusan manusia; beban-rilis)

`README.md:34,37` mencetak R1 = 0 dan R4 = 0 sumber, dengan alasan `README.md:47`: "R4 tidak
perlu diadakan. Ia melekat pada produk ... diminta per proyek". `EKAS-SYSTEM-MAP.md:66`
mengulangi "R4_OEM-TECHNICAL <- kosong secara rancangan. Diisi per proyek". Terhadap itu:
`ekas/03_SOURCE-VAULT/R4_OEM-TECHNICAL/NETWORK/_ISI.md:3` menyatakan 28 berkas (28 baris tabel
terhitung), `REF-OEM-NET.md:13` menyatakan 28 berkas `ACTIVE_WITH_SCOPE_LIMITS`, dan
`MASTER-REFERENCE-REGISTER.csv:59` mendaftarkan REF-OEM-NET sebagai sumber R4 aktif. Adjudikasi
yang benar kemungkinan semantik (R4 = 0 berarti "tidak ada angka produk tersimpan sebagai
pengetahuan tetap"), bukan salah hitung - tetapi dua bacaan menghasilkan keputusan berbeda di
gerbang G3/G5, jadi wajib diputuskan manusia sebelum objek IL menyalin salah satunya. Objek ini
mengutip KEDUA pembacaan apa adanya.

### K-10. Edisi CCNA 2019 diklaim terarsip, lacinya tidak ditemukan (calon)

`R3 - CCNA 200-301 Official Cert Guide Library.md:83-85`: edisi 2019 "diarsipkan, bukan dihapus
- ada di `_arsip/` (1.813 halaman, 38,1 MB)"; `REF-NET-002.md:41` mengulangi. Sapuan nama berkas
di dua pohon (lapis teks `ekas/` dan vault nyata `C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/`)
menghasilkan nol direktori `_arsip` dan nol berkas CCNA selain pustaka 2024. Kemungkinan besar
vault teks memang tidak membawa arsip fisik - calon kuat, bukan vonis; `EKAS-SYSTEM-MAP.md:121`
mengenal `SUPERSEDED/` sebagai direktori edisi lama, bukan `_arsip/`.

### K-11. Label folder/nama berkas katalog tidak sama dengan lapis domain (cacat penamaan terukur; beban-rilis jalur)

`KATALOG-RUMUS.md:389,564-567` menunjuk folder `R3/NETWORK/` dan resume berawalan `RESUME - ...`
(contoh `RESUME - TCP-IP Illustrated Vol 1.md`). Yang ada di disk: `05_DOMAIN-KNOWLEDGE/NETWORKING/`
dengan berkas berawalan `R3 - ...`. Label `R3/NETWORK/` juga tidak sama dengan nama domain
kanonik `NETWORKING`. Baris rute memori dan objek IL WAJIB memakai path yang benar-benar ada
(seksi 6 kontrak jalur G-1); menyalin label katalog mentah-mentah memutus probe verifikasi.
Objek ini sudah memakai path nyata di seluruh bagiannya.

### K-12. Rantai I menunjuk rantai B untuk ambang tundaan yang tidak ada angkanya di lapis teks (rujukan melebihi isi; beban-rilis)

`NETWORKING/RANTAI-JAMINAN.md:103` menetapkan "Tundaan dan kehilangan paket: sesuai kebutuhan
sistem video" dengan sandaran "Rantai B - BS EN 62676-1-2 [R2]". Lapis teks R2 tersebut
memodelkan tundaan, jitter, dan kehilangan paket sebagai satu kesatuan (Gambar 2, PDF 33) dan
mendaftar gejala kehilangan paket (PDF 32), tetapi TIDAK memuat satu pun angka ambang
tundaan/jitter/kehilangan paket (`ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/R2 - BS EN 62676-1-2.md:72-79`).
Rujukan silangnya sah sebagai kerangka, tidak sah sebagai sumber angka. Baris uji itu hari ini
tidak bisa dieksekusi tanpa angka kontrak sendiri (G-2).

### Blok warisan Tabel 7 (known-defect, ikut terbit karena rantai I memakainya)

Angka waktu deteksi hilangnya sinyal 8 / 4 / 2 detik [R2, BS EN 62676-1-2, PDF 34] yang
dipakai `NETWORKING/RANTAI-JAMINAN.md:109-111` berstatus KNOWN-DEFECT sejak VSSKB-0923
(2026-09-23): berkontradiksi dengan bentuk empat nilai 8/4/4/2 di
`ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/R2 - BS EN 62676-1-2.md:45-48`; pemetaan per-grade
BELUM TERKONFIRMASI terhadap geometri PDF primer (ukur gsp-custodian 2026-09-23); rekonsiliasi
BSI/IEC oleh manusia belum terjadi. Blok `CATATAN DEFECT` di `NETWORKING/RANTAI-JAMINAN.md:112`
dikutip UTUH di bawah ini (rak TIDAK diutak-atik); kunci `defek-terkait` frontmatter
terisi; entri wiki `faktas/waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2.md` sudah
ditandai known-defect oleh librarian 2026-09-23. Larangan tegas: JANGAN mengutip 8/4/2 (maupun
8/4/4/2) sebagai ambang sah uji serah terima dari objek ini.

Kutipan verbatim `NETWORKING/RANTAI-JAMINAN.md:112` (state rak 2026-09-24):

> **CATATAN DEFECT (VSSKB-0923, 2026-09-23):** ambang 8 / 4 / 2 detik di atas berstatus known-defect - berkontradiksi dengan bentuk empat nilai 8/4/4/2 di `../VIDEO-SURVEILLANCE/R2 - BS EN 62676-1-2.md:45-48`; pemetaan per-grade BELUM TERKONFIRMASI terhadap PDF primer (ukur gsp-custodian 2026-09-23). Blok penuh: `R2 - BS EN 62676-1-2.md` (CATATAN DEFECT) + `wiki/catatans/vss-korpus-ekas-0923.md` sub-seksi 'Batas angka Tabel 7'.

### Ringkasan predikat

| Butir | Kelas | Predikat | Beban-rilis? |
|---|---|---|---|
| K-1 | sitasi halaman BDP | kontradiksi terukur, 769 menang (sementara) | ya |
| K-2 | sitasi halaman window scaling | kontradiksi terukur, 647 menang (sementara) | ya |
| K-3 | atribusi halaman Donahue ke Odom | kontradiksi terukur | ya |
| K-4 | aritmetika jumlah bookmark | kontradiksi internal, belum tertutup | tidak |
| K-5 | label bab vs alamat halaman | calon | tidak |
| K-6 | peringkat ukuran berkas | kontradiksi terukur terhadap laci | tidak |
| K-7 | peringkat jumlah bookmark | kontradiksi terukur antar domain | tidak |
| K-8 | cakupan daftar wajib R4 | gap tumpang tindih | ya (PoE) |
| K-9 | R4 = 0 vs 28 berkas | kontradiksi semantik, butuh putusan manusia | ya |
| K-10 | arsip edisi 2019 | calon (jejak fisik nihil) | tidak |
| K-11 | label folder/nama berkas | cacat penamaan terukur | ya (jalur rute) |
| K-12 | ambang tundaan tanpa angka | rujukan melebihi isi | ya |

Tidak ada butir yang ditutup sebagai "mungkin sama saja" (pelajaran Tabel 7). Yang bisa
diadjudikasi dari rak diadjudikasi dengan aturan rak sendiri (K-1, K-2, K-3, K-6, K-7); sisanya
dinyatakan calon dengan alasan kenapa lapis teks tidak cukup.

---

## Bagian 6 - Gap register domain

### 6.1 Celah resmi ber-ID (dari `ekas/02_REGISTERS/GAP-REGISTER.csv`)

| ID | Celah | Lapis | Domain | Prioritas | Status |
|---|---|---|---|---|---|
| GAP-011 | TIA-568 / TIA-942 (perkabelan terstruktur, pusat data) | R2 | STORAGE, NETWORKING | MENENGAH | terbuka (csv:12; laci TIA `_ISI.md:3` "Kosong") |
| GAP-013 | Perencanaan kapasitas jaringan | R3 | NETWORKING | RENDAH | terbuka (csv:14; catatan "Fall & Stevens membahas protokol, bukan perancangan") |
| GAP-014 | Seluruh dokumentasi OEM | R4 | SEMUA | PER PROYEK | by-design (csv:15) |
| GAP-005 | ONVIF interoperabilitas (tetangga; rujukan silang, bukan celah transmisi) | R2 | VIDEO-SURVEILLANCE | TINGGI | terbuka (csv:6) |

### 6.2 Celah hasil sapuan (basis bukti, bukan dugaan)

| ID | Yang dicari | Keadaan | Bukti sapuan |
|---|---|---|---|
| G-1 | TIA-568 / TIA-942 | tidak ada di rak | GAP-011; `AMBANG-TERIMA-INDUK.md:76`; `RANTAI-JAMINAN.md:20,104,143-144`; laci `R2_INTERNATIONAL-STANDARDS/TIA/_ISI.md:3` "Kosong." |
| G-2 | Ambang numerik tundaan/jitter/kehilangan paket | tidak ada di rak (kerangka saja) | `VIDEO-SURVEILLANCE/R2 - BS EN 62676-1-2.md:72-79` tanpa satu pun angka; K-12 |
| G-3 | Angka lembar data PoE, kapasitas switching, batas sesi | tidak ada di lapis teks | 28 PDF ada di laci R4 (`_ISI.md:11-38`) tetapi nol angka ditranskripsikan ke resume/kartu/katalog/rantai; rantai I bahkan tanpa contoh PoE terhitung |
| G-4 | Tabel subnetting / skema pengalamatan terhitung | tidak ada di rak (deskripsi keberadaan saja) | `R3 - CCNA ... .md:50-54` menyebut bagian subnetting tanpa satu pun prefiks/mask/contoh |
| G-5 | Definisi `faktor_puncak` dan `faktor_rugi_kabel` | tidak ada di rak | `ASUMSI-BAKU.md` tidak punya seksi jaringan (seksi A-F: Keandalan, Serat optik, Pembumian, Catu daya, Sistem video, Penyimpanan). Sapuan per token: `puncak` 0, `1,5` 0, `PoE` 0, `jaringan` 0, `switch` 0, `RTT` 0, `TCP` 0, `VLAN` 0, `100 m` 0. Kata `Faktor` muncul 4 kali (:79 faktor daya beban, :84 faktor derating genset, :103 faktor gerak/aktivitas, :144 faktor koreksi suhu) - tidak satu pun faktor_puncak/faktor_rugi_kabel. Dua faktor yang dipakai `RANTAI-JAMINAN.md:53,63` tidak terdaftar sebagai asumsi baku |
| G-6 | Rumus perencanaan kapasitas jaringan (oversubscription, kamera per uplink) | tidak ada di rak | `R3 - TCP-IP ... .md:158-160`; `KATALOG-RUMUS.md:541`; GAP-013 |
| G-7 | ONVIF | tidak ada di rak | GAP-005; `AMBANG-TERIMA-INDUK.md:74` |
| G-8 | Dasar hukum Indonesia untuk jaringan/instalasi (PUIL, SNI) | tidak ada di rak | `README.md:34` R1 = 0; `AMBANG-TERIMA-INDUK.md:75`; `KATALOG-RUMUS.md:535` |
| G-9 | Waktu pemulihan STP/peralihan gateway sebagai angka | tidak ada di rak | `RANTAI-JAMINAN.md:100-101` menyerahkan keduanya ke kontrak tanpa nilai bawaan |
| G-10 | QoS angka (policing/shaping/penandaan DSCP) | tidak ada di rak | QoS hanya disebut topik Volume 2 CCNA (`R3 - CCNA ... .md:28`) dan Bab 9 Kurose "kebutuhan kualitas layanan" (`R3 - Computer Networking ... .md:43-44`); nol angka, nol tabel kelas lalu lintas |
| G-11 | Nirsinyal kapasitas WLAN, desain RF | tidak ada di rak | Bab 7 Kurose (PDF 549) dan bagian wireless CCNA disebut ada; nol angka densitas/plan kanal/ambang |
| G-12 | Arsip fisik edisi CCNA 2019 | tidak ditemukan | K-10; sapuan dua pohon nol hasil |
| G-13 | Lembar data access point di laci R4 jaringan | praktis tidak ada | `RANTAI-JAMINAN.md:21` menjanjikan "Lembar data switch, PBX, AP"; isi laci 28 berkas: mayoritas telepon/PBX VoIP (Fanvil, Yealink, Yeastar, Grandstream), intercom Hikvision, sensor COMET, motherboard MSI, PDU Gude, 1 switch TP-Link Omada SG2005P-PD, 1 media converter - AP NOL. Sebagian berkas tampak salah laci (mis. `19_MSI_B650_GAMING_PLUS_WIFI_Datasheet.pdf` = motherboard desktop) dan ada duplikat varian nama. Dampak: keputusan "R4 wajib" (anggaran PoE) hanya punya SATU dokumen sandaran di laci, belum ditranskripsikan |
| G-14 | Volume 2 Limoncelli | tidak ada di rak | `R3 - The Practice ... .md:108-109` |

### 6.3 Yang justru KUAT di rak ini (agar objek tidak timpang)

Rantai keputusan desain eksplisit dengan alternatif ditolak beserta alasan
(`RANTAI-JAMINAN.md:33-38`); kerangka BDP + window scaling lengkap dengan contoh terhitung dan
diagnosis gejala (`R3 - TCP-IP Illustrated Vol 1.md:122-155`) - satu-satunya angka buku domain
ini yang lolos uji aritmetika; konversi halaman terverifikasi 20/20 baris; daftar bukti serah
operasional yang bisa diaudit (`:119-130`); praktik proses Limoncelli diangkat jadi lampiran
wajib; peringatan usia buku yang jujur dan spesifik (`:146-148`).

---

## Bagian 7 - Kata kunci rute (16 token)

Tag beku objek ini (daftar beku G-1 seksi 4, byte-per-byte; frontmatter tetap otoritatif,
bagian ini hanya mirror):

`networking, jaringan, vlan, poe, bdp, tcp, window-scaling, switch, router, subnetting,
lebar-pita, throughput, rtt, latensi, anggaran-poe, uji-kabel` = 16 token.

| Token | Padanan kerja harian | Jangkar isi |
|---|---|---|
| networking / jaringan | jaringan IP, LAN instalasi | seluruh objek |
| vlan | pemisahan jaringan pengawasan | [R3, Network Warrior, PDF 51]; `RANTAI-JAMINAN.md:33` (atribusi Odom = K-3) |
| poe / anggaran-poe | daya switch port | `RANTAI-JAMINAN.md:37,42-44,62-68,98-99` [R4 wajib] |
| bdp / rtt | transfer lambat padahal bandwidth besar | [R3, TCP-IP Illustrated Vol 1, PDF 769] |
| tcp | perilaku protokol, TIME_WAIT, PMTU | [R3, TCP-IP Illustrated Vol 1, PDF 651, 655-664] |
| window-scaling | WAN besar, jendela TCP | [R3, TCP-IP Illustrated Vol 1, PDF 647] |
| switch / router | perangkat keras ruas, gateway redundan | `RANTAI-JAMINAN.md:34,36`; REF-OEM-NET [R4] |
| subnetting | skema pengalamatan | `R3 - CCNA ... .md:50-54` (kerangka saja, G-4) |
| lebar-pita / throughput | agregat kamera, uplink | `RANTAI-JAMINAN.md:52-58,82-89` |
| latensi | tundaan jalur | G-2/K-12 - ANGKA TIDAK ADA DI RAK |
| uji-kabel | uji cabut kabel, uji ujung jauh | `RANTAI-JAMINAN.md:99,106-107` |

Catatan jujur: istilah trunking, STP/spanning tree, uplink, dan QoS adalah keyword domain yang
sering dipakai, tetapi TIDAK termasuk daftar beku G-1 - rute mereka lewat token di atas
(trunking/vlan, STP/vlan, uplink/lebar-pita). QoS sendiri tidak punya angka di rak (G-10), jadi
token tambahan untuk QoS tidak akan menemukan muatan. Perubahan daftar tag = amandemen G-1
lewat kartu + Decision Log, bukan suntingan senyap.

---

## Bagian 8 - BATAS PENGETAHUAN / status rantai

Blok ini wajib ikut terbit bersama angkanya. Objek yang hanya berisi angka enak-dibaca tapi
menyembunyikan celah = gagal maksud registrasi dan menabrak aturan EKAS ("jawab tidak ada di rak
daripada mengarang").

1. **Status rantai apa adanya (tanpa perataan - temuan F-6):** `NETWORKING/RANTAI-JAMINAN.md:136`
   (pra-patch `:128`) mencetak: "UTUH pada perhitungan - TANPA SANDARAN NORMATIF pada sebagian
   besar ambang." Seluruh ambang kecuali waktu deteksi hilang sinyal berasal dari hitungan
   rancangan dan kontrak; itu sah, tetapi ambangnya HANYA SEKEKUAT KESEPAKATAN TERTULISNYA.
   Angka lebar pita, waktu pemulihan, dan pemisahan jaringan wajib MASUK KONTRAK, bukan hanya
   proposal (`:138-141`).
2. **R1 = 0 dan R4 = 0 global.** Keadaan rak: R1 = 0, R2 = 5, R3 = 24, R4 = 0, R5 = 8
   [peta rak: ekas/00_START-HERE/README.md baris 34-38]. Arti: korpus dapat menghitung dan
   menetapkan ambang uji, TIDAK dapat menyatakan kepatuhan hukum Indonesia (PUIL/SNI tidak di
   rak - G-8). Ketegangan semantik R4 = 0 vs laci 28 berkas (K-9) menunggu putusan manusia;
   objek ini tidak memilih salah satu.
3. **Known-defect yang wajib ikut terangkut.** (a) K-1/K-2: sitasi BDP/window scaling rantai I
   (770/766) divonis sementara lapis teks 769/647; anotasi D1-FIXx terpasang di
   `RANTAI-JAMINAN.md:23-25,78`; BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
   (b) K-3: jangkar halaman VLAN/STP/FHR atas nama Odom adalah halaman Network Warrior;
   anotasi `:23-25,40`. (c) Tabel 7 warisan VSSKB: 8/4/2 adalah known-defect, BUKAN ambang sah;
   blok `CATATAN DEFECT` di `:112` dirujuk utuh, rak tidak diutak-atik; probe yang menyinggungnya
   wajib membawa penanda BELUM TERKONFIRMASI. Bentuk lama tidak dihapus di mana pun, hanya
   ditandai.
4. **GAP register yang mengikat domain:** GAP-011 (TIA-568/TIA-942, MENENGAH - angka TIA hidup
   hanya sebagai kutipan R3 Hayes milik domain FIBER-OPTIC, standar primernya tidak di rak;
   lapis yang menyatakan lain = defect), GAP-013 (perencanaan kapasitas jaringan, RENDAH),
   GAP-014 (R4 by-design, angka melekat produk diminta per proyek). Plus 14 gap hasil sapuan
   G-1..G-14 di Bagian 6.2, semuanya berbasis bukti sapuan.
5. **Contoh PoE R4 tidak ada di rak.** Rak menetapkan anggaran PoE sebagai keputusan "R4 wajib"
   tetapi tidak ada satu pun angka watt yang ditranskripsikan ke lapis teks (G-3), dan laci R4
   jaringan timpang (1 switch, 0 AP - G-13). Bila lembar data belum ada: tulis "menunggu data
   pabrikan" (`AMBANG-TERIMA-INDUK.md:85-94`), jangan mengarang.
6. **Faktor puncak 1,5 dan faktor rugi kabel TIDAK TERDAFTAR di ASUMSI-BAKU** (G-5): contoh
   240 Mb/s dan kerangka PoE memakai besaran tanpa sandaran asumsi baku. Permohonan hilir:
   pendaftaran kedua faktor ke `ASUMSI-BAKU.md` oleh controller supaya contoh rak punya sandaran.
7. **Peringatan usia buku (F-7):** Fall & Stevens 2012 (14 th) dan Donahue 2011 (15 th)
   [peta rak, `RANTAI-JAMINAN.md:146-148` - glif peringatan rak ditulis deskripsi agar berkas
   ASCII]; perilaku protokol dan pola gangguan tetap berlaku, TETAPI platform dan perintah
   Donahue sudah tidak dijual. Odom 2024 paling mutakhir untuk praktik perangkat; Kurose 2017
   dan Limoncelli 2017 aman secara konsep. Waktu rekonstruksi RAID (rujukan silang D5) tidak
   dipakai sebagai kebenaran lintas-waktu.
8. **R3 bukan ambang hukum.** Metode boleh R3; angka lulus/tidak-lulus yang tidak dihitung tidak
   boleh R3 (`AMBANG-TERIMA-INDUK.md:46-47`). Kelas R2 (BS EN 62676-1-2) dan kelas R3 (buku)
   dilarang diratakan menjadi "standar". Lima dari enam kartu REF-NET mensyaratkan adopsi
   kontrak tertulis sebelum boleh menetapkan ambang.
9. **Domain tetangga hanya rujukan silang, tidak disalin (putusan P-8):** STORAGE
   `ekas/05_DOMAIN-KNOWLEDGE/STORAGE/RANTAI-JAMINAN.md` (mitra F-3 sitasi Fall & Stevens; RAID
   [R3, Troppens, PDF 46-70]); VIDEO-SURVEILLANCE (bitrate Damjanovski [R3, PDF 277, 290];
   pemilik fakta Tabel 7); CYBERSECURITY (kata sandi bawaan, rantai J). POWER-BACKUP dan
   GROUNDING-LIGHTNING di luar cakupan D1.
10. **Sumber dan kebaruan.** Seluruh angka berasal dari lapisan teks `ekas/` diekstrak read-only
    2026-09-24; tidak ada PDF primer yang dibuka - verifikasi per halaman wewenang manusia
    (PDF asli di `C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/`). `ekas/` read-only - objek
    ini tidak mengubah rak. Nomor baris `RANTAI-JAMINAN.md` di objek ini memakai versi pasca-
    tambalan D1-FIXx (148 baris); pemetaan ke nomor studi (versi 140 baris) ada di Bagian 1.1.

STATUS: complete
