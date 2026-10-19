# Delta per Matra / Rezim - Paket GSP-SDT

> Sumber: SPEC-DOC-SYSTEM.md §2 (DELTA 6 kelompok: umum/kelas/anatomi/aparatus/acuan/gerbang).
> Ringkasan operasional; tabel lengkap tinggal di SPEC-DOC (jangan disalin ulang - D-TA-7.1).

## 1. Rezim dan sebutan

| Rezim | Kode | Dokumen sumber | Sebutan unit | Total bobot |
|---|---|---|---|---|
| Umum/profesional | SDT | R-1 GSP-SDT-001 | Klausul | 67 |
| Pertahanan (payung; berkas "AL") | SDTP | R-2 GSP-SDTP-001 | Klausul | 67 |
| Matra Darat | AD | R-3 GSP-SDTP-AD-001 | Klausul | 67 |
| Matra Udara | AU | R-4 GSP-SDTP-AU-001 | Klausul | 67 |
| Kepolisian | PL | R-5 GSP-SDT-PL-001 | **Pasal** | 66 |
| Keamanan Siber | CY | R-6 GSP-SDT-CY-001 | Klausul | 66 |
| Bisnis Pertahanan-Keamanan | BIZ | R-7 GSP-SDT-BIZ-001 | Klausul | 66 |

## 2. Yang berubah per rezim (pointer cepat)

| Aspek | SDT/umum | SDTP | AD | AU | PL | CY | BIZ |
|---|---|---|---|---|---|---|---|
| Nomor lembar | `n - mm` | `SHEET nn OF mm` | `LEMBAR n DARI m` | `HAL nn / mm` | `HLM n / mm` | `n / mm` | `n / mm` |
| Bingkai | tidak | navy | ganda hijau | azure | tidak | tidak | tidak |
| Margin mm | 24/24/22/26 | 22/18/22/20 | 22/18/22/20 | 22/18/22/20 | 23/22/21/24 | 23/22/21/24 | 23/22/21/24 |
| Logo | - | DILARANG | DILARANG | DILARANG | - | - | bermerek |
| Blok identitas | strip | kisi 6×4 (`BAHASA`) | kisi 6×4 (`MATRA`) | kisi 6×4 (`MATRA`) | strip | strip+INTEGRITAS | strip |
| Kunci khas | REQ-Kx-nnn | SHEET wajib semua lembar | - | uji darat+terbang | `BB-nnn`, TTE/BSrE | `FND-Kx-nnn`, CVSS, ATT&CK | `LI-nnn`, TKDN %, Draf/Final/TTD |
| Baris anatomi khas | inti | inti | inti | inti | "Rantai Kustodi & Bukti" | "Rantai Kustodi & Bukti" (K1 ●) | "Isi Teknis / Komersial", "Ketentuan Komersial", FAT/SAT |

Palet & huruf per rezim TIDAK diduplikasi di sini - sumbernya paket token DS
(`gsp-design-system-grill/references/master-design/`) + SPEC-DOC §2.1.

## 3. Gerbang khas per rezim (di luar 10 butir inti C-23)

- **SDTP**: RUU tak dipakai sebagai dasar wajib (A).
- **AD/AU**: materiil bersertifikat kelaikan bila K4/K5 (T); tata naskah dinas matra (A).
- **PL**: rantai kustodi SHA-256 di dokumen bukti (#6); TTE tersertifikasi (#7); tata naskah Polri (#9).
- **CY**: klasifikasi = dampak terparah bila bocor; daftar distribusi terbatas di sampul (K1/K3/K5);
  bukti eksploitasi tersanitasi, PoC penuh terpisah berklasifikasi lebih tinggi; CVSS terhitung +
  risiko diturunkan; pemetaan ATT&CK; rantai kustodi insiden. Catatan: CY mengganti butir #1 inti
  dengan butir klasifikasi-dampak - konsistensi Register Induk tetap diperiksa sebagai anatomi.
- **BIZ**: klaim kemampuan tertelusur ke bukti; harga & lingkup konsisten proposal↔BOQ↔kontrak;
  hasil FAT/SAT memenuhi kriteria; TKDN dapat dibuktikan; INCOTERMS & SLA jelas; NDA/PDP.

## 4. Acuan normatif (delta Tabel 2.1 - ringkas)

Setiap rezim punya daftar Wajib/Rujukan sendiri di SPEC-DOC §2.5. Yang paling sering salah
dipakai generator: nomor peraturan internal (Perpang/Perkasad/Perkasau/Perpol/TKDN/IMAA)
bertanda **"nomor dikonfirmasi"** - wajib konfirmasi sumber resmi sebelum dipakai mengikat;
**RUU KKS (CY) berstatus Pending** - pantau, jangan jadi dasar wajib.

## 5. Keterbatasan yang wajib dihormati generator (SPEC-DOC §6)

1. Nomor register ketujuh dokumen = provisional sampai Register Induk (ARSIP).
2. R-2 tidak menyebut matra laut dalam teks - perlakukan payung pertahanan sampai konfirmasi.
3. R-5: pakai pola footer `HLM n / mm` yang terbukti di PDF (Klausul 6.1 tidak menyebut pola).
4. Gambar raster 4.1/4.2: hanya caption+SUMBER yang terverifikasi teks.
