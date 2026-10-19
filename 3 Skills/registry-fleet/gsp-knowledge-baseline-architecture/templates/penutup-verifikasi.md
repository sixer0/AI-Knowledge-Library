# Template PENUTUP LEMBAR VERIFIKASI AKHIR (R-06, R-11) + SIDIK JARI MODEL (R-01)

Lembar ini berada di HALAMAN PENUTUP dokumen (di dalam dokumen, bukan berkas eksternal).
Isinya hasil ukur nyata pada giliran serah, bukan niat. Setiap baris HASIL wajib dapat
diulang oleh pemeriksa dengan CARA yang tertulis.

## Tabel PEMERIKSAAN | CARA | HASIL

| # | PEMERIKSAAN | CARA | HASIL |
|---|---|---|---|
| 1 | Rantai turunan berjalan penuh dari akar | Jalankan ulang spine dari masukan terukur; bandingkan keluaran vs register beku | LULUS / RINCIAN ANGKA COCOK |
| 2 | Uji dua rute side-by-side | Hitung ulang N uji lewat rute independen kedua; cocokkan Lampiran B | LULUS n/N, putusan COCOK per uji |
| 3 | Jalan ulang deterministik | Eksekusi ulang pipeline pembeku pada input yang sama; bandingkan byte | BYTE-IDENTIK / DELTA ... |
| 4 | Pengikatan angka naskah ke register | Extractor membandingkan setiap angka di badan dokumen vs register | n/n terikat, angka diketik manual = 0 |
| 5 | Aritmetika blok derivasi | Parser memisahkan rekaman vs baris fisik, menguji semantik operasi | LULUS / TEMUAN ... |
| 6 | Traceability <=2 langkah (V-SUSUN-1) | Seed acak >=10 angka telusuri register -> dasar | 10/10 dalam <=2 langkah (seed: ...) |
| 7 | Geometri/kerapatan layout (V-SUSUN-2) | Ukur halaman keputusan vs halaman dump; dump per-baris di badan = 0 | ... hal keputusan / 0 dump |
| 8 | Interogasi berkas kerja | Setiap berkas kerja menyertai punya entri indeks lampiran | n/n berindeks |
| 9 | Rekonsiliasi lembar kendali | Baris REV append-only vs perubahan sidik jari register | KONSISTEN |

Sesuaikan butir dengan isi dokumen; jangan menghapus baris hanya karena belum dikerjakan.

## YANG TIDAK DIPERIKSA OLEH ALAT (milik manusia)
Seksi wajib. Nyatakan batas alat secara jujur, contoh empat milik manusia:
1. Kebenaran semantik pemetaan kebutuhan->kuantitas (butuh insinyur domain).
2. Kelayakan biaya terhadap kondisi pasar saat eksekusi.
3. Kepatuhan terhadap regulasi lokal yang berubah setelah tanggal cek kesegaran.
4. Putusan penerimaan lingkup oleh pemberi kerja (termasuk keputusan yang tertahan).

## SIDIK JARI MODEL BEKU (R-01)
```text
SIDIK JARI REGISTER BEKU : sha256[:16] = xxxxxxxxxxxxxxxx
BERKAS REGISTER          : <path register beku>  (n besaran, grup A-...)
TANGGAL BEKU             : YYYY-MM-DD HH:MM (Asia/Jakarta)
DOKUMEN TURUNAN          : wajib mengutip sidik jari yang sama; sidik jari berbeda =
                           dokumen turunan basi, tarik dari peredaran.
```
Cara cetak: `sha256sum <berkas register> | cut -c1-16`. Dokumen turunan (BOQ, spesifikasi,
rancangan uji terima) mencantumkan baris "Mengacu register beku sha16 xxxxxxxxxxxxxxxx".
Bila register berubah, sidik jari baru WAJIB muncul di baris lembar kendali terbaru lebih
dulu sebelum dokumen turunan mana pun mengutipnya.
