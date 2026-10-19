# Resume — Microwave Engineering (Pozar, 2012)

**Penulis:** David M. Pozar · **Edisi:** keempat · **Penerbit:** Wiley, 2012
**Berkas vault:** `03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/RF-WIRELESS/Pozar, David M - Microwave engineering...pdf` — 756 hlm PDF
(buku inti; solutions manual-nya ING-0008 ditolak W1b)
**Disusun:** 09 Oktober 2026, dari teks ekstraksi lokal (pypdf)
**Status daya-ikat:** `pending_verification` (P-5).

> **Konversi halaman.** Halaman cetak + 20 = halaman PDF (folio `1` di PDF 21; running head `2.4 The Smith Chart 63` di PDF 83; `72 Chapter 2` di PDF 92; `252 Chapter 5` di PDF 272; `8.2 ... 389` di PDF 409 — terverifikasi konsisten). Ditulis nomor PDF.

## 1. Peta bab (bookmark PDF terverifikasi isi)

| Bab | Topik | PDF | Cetak |
|---|---|---|---|
| 1 | Electromagnetic Theory — Maxwell, syarat batas, persamaan gelombang, daya, refleksi bidang, insidensi oblik | `[R3, Pozar MW, PDF 21]`, `[R3, Pozar MW, PDF 26]`, `[R3, Pozar MW, PDF 35]`, `[R3, Pozar MW, PDF 48]` | 1–38 |
| 2 | Transmission Line Theory — model elemen lumped, analisis medan, garis lossless terminasi, Smith chart, transformer seperempat gelombang, mismatch generator-beban, garis rugi, transien | `[R3, Pozar MW, PDF 68]`, `[R3, Pozar MW, PDF 76]`, `[R3, Pozar MW, PDF 83]`, `[R3, Pozar MW, PDF 92]`, `[R3, Pozar MW, PDF 96]` | 48–… |
| 3 | Transmission Lines and Waveguides — solusi TEM/TE/TM, pandu gelombang persegi, koaksial, stripline, microstrip | `[R3, Pozar MW, PDF 116]`, `[R3, Pozar MW, PDF 130]`, `[R3, Pozar MW, PDF 150]`, `[R3, Pozar MW, PDF 167]` | 96–… |
| 4 | Microwave Network Analysis — matriks impedansi/admitansi, matriks S, ABCD, graf aliran sinyal | `[R3, Pozar MW, PDF 186]`, `[R3, Pozar MW, PDF 198]`, `[R3, Pozar MW, PDF 214]` | 166–… |
| 5 | Impedance Matching and Tuning — jaringan-L, tuning stub tunggal/ganda, taper | `[R3, Pozar MW, PDF 249]`, `[R3, Pozar MW, PDF 254]` | 229 |
| 6 | Microwave Resonators — rangkaian resonansi seri/paralel, Q loaded/unloaded | `[R3, Pozar MW, PDF 294]` (heading 6.1) | 272–273 |
| 7 | Power Dividers and Directional Couplers — T-junction, coupler arah | `[R3, Pozar MW, PDF 338]` (heading 7.1) | 317–319 |
| 8 | Microwave Filters — metode parameter gambar, konstanta k, m-derived | `[R3, Pozar MW, PDF 408]` | 388 |

## 2. Butir bertambat (teks dibuka)

- SWR/VSWR: 1 ≤ SWR ≤ ∞, SWR = 1 berarti beban match — . `[tanpa-jangkar]`
- Smith chart dipakai dengan desibel untuk rasio daya — `[R3, Pozar MW, PDF 83]`.
- Transformer seperempat gelombang: pencocokan praktis, terbatas pada beban resistif (beban kompleks dibuat resistif dulu pada satu frekuensi) — `[R3, Pozar MW, PDF 95]`–`[R3, Pozar MW, PDF 95]`.
- Filter desain metode image parameter: spesifikasi passband/stopband dua-port — `[R3, Pozar MW, PDF 408]`–`[R3, Pozar MW, PDF 409]`.
- Gelombang mikro = analisis & desain rangkaian distributed (kata pengantar edisi 4) — `[R3, Pozar MW, PDF 8]`.

## 3. Metode yang bisa diadopsi GSP

Desain tautan gelombang mikro (feeds antena radar/mikrowave link): teori garis transmisi, pencocokan (L-network, stub), kalkulasi SWR/refleksi, filter. Spesifikasi komponen konkret = R4.

## 4. Batas pemakaian

- R3 (2012): standar akademik; `pending_verification`. Solutions manual TIDAK di-vault — tidak ada jalan pintas jawaban soal.
- Kartu `04_KNOWLEDGE-CARDS/RF-WIRELESS/REF-RFW-003*.md`.


## 5. Butir bertambat tambahan (tambalan W10 BUKUV3-JURY-1009, 09-10-2026)

Diambil verbatim dari halaman vault yang dibuka ulang dengan pdftotext (Xpdf 4.06); sebelumnya butir ini hanya disebut judul/nama tanpa badan aturan. Daya-ikat tetap `pending_verification` (P-5) — tidak naik.

- Rumus impedansi seksi pencocok (Equation 5.25): "The single-section quarter-wave matching transformer circuit is shown in Figure 5.10, with the characteristic impedance of the matching section given as" Z1 = sqrt(Z0 ZL)  (5.25). Syarat: "At the design frequency, f0, the electrical length of the matching section is lambda0/4". Catatan ekstraksi: pdftotext Xpdf menjatuhkan tanda akar pada baris persamaan (keluar `Z1 = Z0ZL. (5.25)`); bentuk akar diterbitkan dari identitas di buku yang sama, pdf_p95: "which is seen to vanish if we choose Z1 = sqrt(Z0 RL), as in (2.63)". — `[R3, Pozar MW, PDF 267]`
  Sumber lengkap: Microwave Engineering 4e - Pozar (2012, Wiley) [vault R3/RF-WIRELESS] pdf_p267 (cetak 247, running head `5.4 The Quarter-Wave Transformer 247`) + cross-check pdf_p95 (cetak 75, Pers. 2.63) | jejak ukur: F2-RF-06
