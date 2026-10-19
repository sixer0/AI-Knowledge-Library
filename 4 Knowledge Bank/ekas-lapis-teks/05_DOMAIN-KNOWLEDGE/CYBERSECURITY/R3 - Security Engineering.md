# Resume — Security Engineering: A Guide to Building Dependable Distributed Systems

**Penulis:** Ross Anderson (University of Cambridge) · **Edisi:** ketiga · **Penerbit:** Wiley
**Berkas:** `Ross Anderson - Security Engineering (3rd Edition).pdf` — 1.044 halaman, 14,7 MB
**Disusun:** 19 Agustus 2026, dari teks buku ini

> **Rujukan halaman memakai nomor PDF.** Bookmark 31 entri; judulnya diperbaiki
> 19 Agustus 2026 (sebelumnya berupa kode berkas `SEv3-ch1-7sep`).

Buku keamanan sistem yang paling dihormati di bidangnya. Bukan buku "cara mengamankan
server" — ini buku **cara berpikir** tentang keamanan: mengapa sistem gagal, siapa
lawannya, dan mengapa solusi teknis yang benar sering tetap gagal karena faktor manusia,
ekonomi, atau kelembagaan.

Untuk GSP, nilainya ada pada **kerangka argumen** saat menyusun bagian keamanan pada
proposal instansi — terutama sistem bukti digital, di mana pertanyaannya bukan sekadar
"apakah terenkripsi" melainkan "apakah dapat dipercaya di pengadilan".

---

## Peta isi

| Bab | Judul | PDF | | Bab | Judul | PDF |
|---|---|---|---|---|---|---|
| 1 | What Is Security Engineering? | 4 | | 16 | Security Printing and Seals | 482 |
| 2 | **Who is the Opponent?** | 17 | | 17 | **Biometrics** | 502 |
| 3 | **Psychology and Usability** | 57 | | 18 | Tamper Resistance | 527 |
| 4 | Protocols | 107 | | 19 | Side Channels | 562 |
| 5 | Cryptography | 131 | | 20 | Advanced Cryptographic Engineering | 586 |
| 6 | **Access Control** | 187 | | 21 | **Network Attack and Defence** | 615 |
| 7 | Distributed Systems | 218 | | 22 | Phones | 648 |
| 8 | **Economics** | 245 | | 23 | Electronic and Information Warfare | 684 |
| 9 | **Multilevel security** | 279 | | 24 | Copyright and DRM | 717 |
| 10 | Boundaries | 302 | | 25 | Taking Stock | 761 |
| 11 | Inference Control | 331 | | 26 | **Surveillance or Privacy?** | 798 |
| 12 | Banking and Bookkeeping | 356 | | 27 | **Secure Systems Development** | 846 |
| 13 | Locks and Alarms | 414 | | 28 | **Assurance and Sustainability** | 889 |
| 14 | **Monitoring and Metering** | 437 | | 29 | Beyond "Computer Says No" | 928 |
| 15 | Nuclear Command and Control | 465 | | — | Bibliography | 930 |

---

## Bagian yang paling sering dipakai

### A. Siapa lawannya (Bab 2, PDF 17)

Pemodelan ancaman berdasarkan **siapa** yang menyerang, bukan **apa** yang diserang: negara,
kejahatan terorganisasi, orang dalam, dan pelaku oportunistik. Masing-masing punya
kemampuan, motif, dan batas berbeda.

Ini kerangka yang dipakai menyusun bagian analisis ancaman pada proposal instansi — jauh
lebih kuat daripada daftar kerentanan teknis.

### B. Kendali akses dan keamanan bertingkat (Bab 6 dan 9, PDF 187 dan 279)

Bab 9 membahas **multilevel security** — model klasifikasi bertingkat yang menjadi dasar
sistem pemerintahan dan pertahanan. Langsung relevan untuk sistem yang menangani informasi
berklasifikasi, termasuk RBAC bertingkat pada sistem bukti digital.

### C. Psikologi dan kegunaan (Bab 3, PDF 57)

Mengapa kontrol keamanan yang benar secara teknis gagal saat dipakai manusia. Argumen yang
berguna saat menolak persyaratan keamanan yang terlalu memberatkan operator — beban yang
berlebihan justru menurunkan keamanan karena akan diakali.

### D. Biometrik (Bab 17, PDF 502)

Kemampuan dan batas sistem biometrik, termasuk tingkat kesalahan dan serangan pemalsuan.
Dipakai saat menilai tawaran sistem pengenalan wajah atau sidik jari — bertemu dengan
`R3/CCTV-VSS/` (Szeliski) Bab 6 dari sisi algoritmanya.

### E. Pemantauan dan pencatatan (Bab 14, PDF 437)

Sistem pemantauan dan meterisasi, termasuk integritas catatan. Bertemu dengan kebutuhan
**jejak audit yang tidak dapat disangkal** pada sistem bukti digital.

### F. Ekonomi keamanan (Bab 8, PDF 245)

Mengapa sistem tidak aman meski secara teknis bisa diamankan — insentif yang salah tempat.
Berguna saat menjelaskan kepada pelanggan mengapa investasi keamanan perlu diarahkan ke
tempat tertentu.

### G. Pengembangan sistem aman dan jaminan mutu (Bab 27–28, PDF 846 dan 889)

Bagaimana keamanan dimasukkan ke dalam proses pengembangan, dan bagaimana klaim keamanan
dibuktikan. Dipakai saat menyusun bagian metodologi pada proposal pengembangan sistem.

### H. Pengawasan atau privasi (Bab 26, PDF 798)

Bab yang membahas ketegangan antara kemampuan pengawasan dan hak privasi, termasuk sisi
kebijakan dan regulasinya. Perlu dibaca oleh siapa pun yang menyusun proposal sistem
pengawasan untuk instansi — membantu mengantisipasi keberatan yang akan muncul.

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Analisis ancaman pada proposal instansi | Bab 2, PDF 17 |
| Rancangan klasifikasi dan RBAC bertingkat | Bab 9, PDF 279 + Bab 6, PDF 187 |
| Integritas jejak audit sistem bukti digital | Bab 14, PDF 437 |
| Menilai tawaran sistem biometrik | Bab 17, PDF 502 |
| Metodologi pengembangan sistem aman | Bab 27–28, PDF 846 dan 889 |
| Mengantisipasi keberatan privasi | Bab 26, PDF 798 |
| Menolak persyaratan keamanan yang kontraproduktif | Bab 3, PDF 57 |

**Pendamping di rak:** `R3/OPERATIONS/` (Limoncelli) untuk penerapan operasionalnya,
`R3/NETWORK/` Bab 8 untuk keamanan jaringan tingkat konsep,
`R3/CCTV-VSS/` (Szeliski) Bab 6 untuk sisi algoritma biometrik.

---

## Catatan mutu berkas

- Teks dapat dicari.
- **Judul bookmark diperbaiki** 19 Agustus 2026 — sebelumnya 31 entri bernama
  `SEv3-ch1-7sep` dan sejenisnya. Halaman tujuannya sudah benar sejak awal; judulnya diambil
  dari teks berukuran font terbesar di tiap halaman tujuan.
- Bookmark hanya sampai tingkat bab — buku ini tidak memuat penomoran sub-bagian yang dapat
  dibaca ekstraksi teks, sehingga sub-bab tidak dapat dibuatkan bookmark otomatis.
- Cadangan sebelum perbaikan: `_asli/Security Engineering - Anderson [ASLI sebelum perbaikan bookmark].pdf`
