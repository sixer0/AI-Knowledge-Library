# Template REL BUKTI (R-05) — tanda asal angka per paragraf

Bentuk: kolom kanan sempit (~32 mm pada layout cetak) berisi glif DATUM + rujukan sumber
untuk SETIAP paragraf yang memuat angka. Paragraf tanpa angka = kolom kosong (keadaan benar,
bukan kelalaian).

## Glif DATUM (empat jenis, tertutup)
| Tanda | Glif | Arti | Contoh rujukan |
|---|---|---|---|
| TERUKUR | ■ | Diukur langsung / dibaca dari dokumen dasar yang berlaku | P-0003 Rev A hal 42 |
| DITURUNKAN | ◈ | Hasil hitung dari rantai spine (register beku) | Reg. grp C-07 |
| PEMASOK | ◇ | Angka dari penawaran/katalog pemasok (belum diverifikasi independen) | Surat Penawaran PT X tgl ... |
| ASUMSI | △ | Asumsi penulis; wajib ada di lampiran asumsi + akibat bila salah | Asm. A-12 |

## Aturan pemasangan
1. Satu paragraf boleh lebih dari satu tanda bila memuat beberapa kelas angka; urutan glif
   mengikuti urutan kemunculan angka.
2. Rujukan sumber ditulis singkat di samping glif; penelusuran penuh lewat register beku
   (target <=2 langkah, V-SUSUN-1).
3. Sebaran glif WAJIB dihitung dan dicetak di bab metode, contoh bentuk:
   "569 besaran: 219 TERUKUR ■, 329 DITURUNKAN ◈, 1 PEMASOK ◇, 20 ASUMSI △."
4. Kanal non-cetak (markdown/HTML): gunakan tag inline `[■ P-0003 h42]` bila kolom kanan
   tidak tersedia; konsistensi glif tetap dijaga supaya V-SUSUN-4 dapat menghitung.
5. ASUMSI adalah tanda paling lemah: jumlah ASUMSI yang naik antar-revisi tanpa justifikasi
   di lembar kendali = temuan audit.
