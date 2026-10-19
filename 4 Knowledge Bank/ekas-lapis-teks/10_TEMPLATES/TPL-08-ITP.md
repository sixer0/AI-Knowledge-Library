# TPL-08 — Inspection & Test Plan (ITP)

Disusun dan **disetujui sebelum uji dimulai** (gate G4). ITP yang disusun setelah uji bukan
rencana, melainkan laporan.

| Butir | Isi |
|---|---|
| **ITP-ID** | |
| Proyek | |
| Lingkup | |
| Disetujui oleh / tanggal | |

## Butir inspeksi & uji

| # | Butir | Metode | Sumber metode | Ambang | **Sumber ambang** | R | Penyaksi |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |
| 2 | | | | | | | |

**Kolom "Sumber ambang" dan "R" tidak boleh kosong.** Bila ambangnya belum ada, tulis
"belum ditetapkan" — dan butir itu dijalankan **tanpa pernyataan lulus/tidak lulus**.

## Prasyarat sebelum uji dimulai

- [ ] Kalibrasi seluruh alat **berlaku pada tanggal uji** — bukan pada tanggal serah
- [ ] Perhitungan yang menjadi sumber ambang **sudah diperiksa orang kedua** (gate G3)
- [ ] Kondisi uji terpenuhi (beban, suhu, konfigurasi)
- [ ] Penyaksi disepakati

> ⚠ **Prasyarat kedua adalah ketergantungan G4 pada G3.** Bila ambang berasal dari hitungan
> sendiri, ITP **tidak dapat disetujui** selama hitungan itu belum diverifikasi. Butir uji
> yang bersandar padanya diblokir sampai G3 tertutup.

## Titik tahan (hold point)

Butir yang **tidak boleh dilewati** tanpa kehadiran penyaksi atau persetujuan tertulis:

| # butir | Alasan |
|---|---|

## Rujukan

Ambang induk: `07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md`
Prosedur per butir: `TPL-03` · Rantai domain: `05_DOMAIN-KNOWLEDGE/<domain>/RANTAI-JAMINAN.md`
