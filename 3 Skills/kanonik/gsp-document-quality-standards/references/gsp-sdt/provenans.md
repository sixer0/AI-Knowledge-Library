# Provenans Angka, Verifikasi A/D/I/T, Kustodi - Paket GSP-SDT

> Sumber: SPEC-DOC-SYSTEM.md §1.5 (C-18..C-20), §5.3, §2.4. Pemilik paket:
> `gsp-document-quality-standards`; kanal lain pointer. Selaras EKAS R1–R5 dan Module L.4.

## 1. Empat jenis provenans angka (C-18) - WAJIB pada setiap angka teknis

| Jenis | Simbol | Definisi (verbatim sumber Tabel 7.1) |
|---|---|---|
| Terukur | ■ | Angka dibaca langsung dari sumber atau instrumen. |
| Diturunkan | ◈ | Angka dihitung dari angka lain; rumus dapat ditelusuri. |
| Pemasok | ◇ | Angka dari klaim pemasok yang belum diverifikasi. |
| Asumsi | △ | Angka ditetapkan sebagai asumsi kerja yang harus diuji. |

Notasi provenans dan A/D/I/T **mengikat pada kelas berbobot tinggi (K1, K4, K5)**.

## 2. Cara menulis (bentuk teks, contoh sah §5.3)

```text
Beban puncak 412 W           [terukur / log PDU-03, hal 2]                    ■
Daya operasional 1,86 kWh/h  [diturunkan / 412 W × 24 h ÷ 1000; rumus §3.2]   ◈
MTBF 50.000 jam              [pemasok / datasheet vendor X rev 2, hal 7]      ◇
Faktor pertumbuhan 1,2       [asumsi / belum diuji; validasi Q4 2026]         △
```

Aturan:
1. **Satu angka = satu provenans.** Bentuk label `[jenis / sumber, hal]` selaras tanda rujukan
   Module L.4; simbol ■◈◇△ ditempel di sampingnya (atau kolom terpisah di XLSX/HTML).
2. Angka berlabel **pemasok** tidak boleh jadi dasar keputusan tanpa verifikasi.
3. Angka berlabel **asumsi** wajib diuji sebelum dokumen K1/K4/K5 disahkan.
4. Tanpa sumber → tulis sebagai asumsi eksplisit, bukan sebagai fakta (Module C.1 #2).

## 3. Metode verifikasi A/D/I/T (C-19)

| Kode | Metode | Jalan |
|---|---|---|
| A | Analisis | melalui perhitungan atau model |
| D | Demonstrasi | melalui peragaan fungsi |
| I | Inspeksi | melalui pemeriksaan langsung |
| T | Uji | melalui pengujian terukur |

Setiap titik uji wajib menyebut metodenya. BIZ menuliskan metode sebagai **(FAT/SAT)** bila
relevan. CY: tiap temuan `FND-Kx-nnn` membawa CVSS (pita Tabel 7.2: Kritis 9,0–10,0 · Tinggi
7,0–8,9 · Sedang 4,0–6,9 · Rendah 0,1–3,9 · Informasi 0,0) + pemetaan MITRE ATT&CK.

## 4. Rantai kustodi (C-20)

Dokumen berbukti dan bukti fisik: sidik **SHA-256 sebelum–sesudah** penyerahan/penyalinan,
dicatat di lampiran (baris `Rantai Kustodi`). PL: setiap barang bukti `BB-nnn` + SHA-256
(selaras KUHAP) dan **TTE/BSrE tersertifikasi** pada dokumen yang menuntut keabsahan (kelas
bukti K3 dan uji terima K5). CY: rantai kustodi insiden; detail eksploitasi disanitasi dari
dokumen serah, PoC penuh disimpan terpisah berklasifikasi lebih tinggi.

## 5. Padanan medium

| Medium | Bentuk provenans |
|---|---|
| DOCX | label teks + simbol di samping angka / catatan kaki tabel |
| XLSX | kolom `Provenans` wajib pada kolom nilai (lihat [`snippet-xlsx.py`](snippet-xlsx.py)) |
| HTML | atribut `data-provenance="terukur|diturunkan|pemasok|asumsi"` + ikon ■◈◇△ terlihat |

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.
