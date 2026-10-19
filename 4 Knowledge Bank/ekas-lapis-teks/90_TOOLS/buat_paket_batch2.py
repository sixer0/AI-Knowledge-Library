# -*- coding: utf-8 -*-
"""
Membangun Pustaka-Teknis-GSP-Batch2.zip — HANYA bahan yang masuk pada batch 2
(19 Agustus 2026), terpisah dari paket induk Pustaka-Teknis-GSP-Markdown.zip.

Jalankan:  python "C:/Users/gspen/Videos/Buku/_tools/buat_paket_batch2.py"
"""
import io, os, zipfile, hashlib

RAK = r"C:\Users\gspen\Videos\Buku"
OUT = os.path.join(RAK, "Pustaka-Teknis-GSP-Batch2.zip")

# (sumber relatif ke rak, tujuan dalam zip)
ISI = [
    # --- Lapis 1: standar ---
    (r"Electrical Maintenance\_standar\RESUME STANDAR - ANSI-NETA ATS-2017.md",
     r"00-standar/ANSI-NETA ATS-2017.md"),
    (r"Battery\_standar\RESUME STANDAR - IEEE 1188-2005 dan IEC 62485-2.md",
     r"00-standar/IEEE 1188-2005 dan IEC 62485-2.md"),
    (r"CCTV VSS\_standar\RESUME STANDAR - BS EN 62676-1-2.md",
     r"00-standar/BS EN 62676-1-2.md"),
    (r"FO Test Advanced\_standar\RESUME STANDAR - IEC 61280-4-2.md",
     r"00-standar/IEC 61280-4-2.md"),
    # --- Lapis 2: tesis & panduan ---
    (r"Cybersecurity\_tesis\RESUME TESIS - Keamanan Siber dan Forensik Digital (Universitas Indonesia).md",
     r"01-tesis-panduan/TESIS - Keamanan Siber dan Forensik Digital (UI).md"),
    (r"Cybersecurity\_panduan\RESUME PANDUAN - Keamanan Siber Operasional.md",
     r"01-tesis-panduan/PANDUAN - Keamanan Siber Operasional.md"),
    # --- Lapis 3: buku baru ---
    (r"Cyber Operations\RESUME - The NICE Cyber Security Framework.md",
     r"02-buku-baru/Cyber Operations - The NICE Cyber Security Framework.md"),
    (r"Critical Infrastructure\RESUME - Cybersecurity Protecting Critical Infrastructures.md",
     r"02-buku-baru/Critical Infrastructure - Protecting Critical Infrastructures.md"),
    # --- Koleksi non-teknis ---
    (r"_koleksi-lain\README.md", r"03-koleksi-lain/README.md"),
    (r"_koleksi-lain\Makalah IEEE\INDEKS-MAKALAH.md", r"03-koleksi-lain/INDEKS-MAKALAH.md"),
]

README = u"""# Paket Batch 2 — Pustaka Teknis GSP

**Dibangun:** 19 Agustus 2026 · **Rak:** `C:\\Users\\gspen\\Videos\\Buku`

Paket ini berisi **hanya bahan yang masuk rak pada batch 2**. Paket induk
`Pustaka-Teknis-GSP-Markdown.zip` berisi **seluruh rak (batch 1 + batch 2 tercampur)`.

> Bila sudah memakai paket induk, **paket ini tidak menambah isi baru** — gunanya
> untuk meninjau *apa yang berubah*, bukan sebagai sumber tambahan.

---

## Isi

| Map | Berkas | Keterangan |
|---|---|---|
| `00-standar/` | 4 | **Standar badan resmi** — rujukan berbobot tertinggi di rak |
| `01-tesis-panduan/` | 2 | **Rujukan sekunder** — penunjuk, bukan sumber kutipan |
| `02-buku-baru/` | 2 | Dua buku yang naik ke perlakuan penuh |
| `03-koleksi-lain/` | 2 | Indeks koleksi non-teknis (60 berkas, tanpa resume per judul) |
| *(akar)* | `DELTA-SISTEM.md` | Apa yang berubah pada berkas sistem karena batch 2 |

---

## Bobot rujukan — bacalah sebelum mengutip

| Map | Boleh dikutip di dokumen resmi? |
|---|---|
| `00-standar/` | **Ya.** Ini yang menetapkan angka ambang |
| `02-buku-baru/` | Ya, sebagai buku teks — sebutkan tahun terbit |
| `01-tesis-panduan/` | **Tidak langsung.** Tesis menyebut UU 11/2008 dan Perban BSSN 4/2021 — yang dikutip **regulasi aslinya**, bukan tesisnya |
| `03-koleksi-lain/` | Tidak. Penunjuk literatur saja |

---

## Delapan ambang yang dibuka batch 2

| Pertanyaan | Jawaban | Standar | Halaman |
|---|---|---|---|
| Berapa MΩ minimum tahanan isolasi? | Tabel 100.1 — 600 V → 100 MΩ · 5 kV → 1.500 MΩ · 15 kV → 5.000 MΩ | ANSI/NETA ATS-2017 | PDF 223 |
| Koreksi hasil ukur ke 20 °C? | Tabel 100.14 | ANSI/NETA ATS-2017 | PDF 241 |
| ΔT berapa yang berarti cacat? | Tabel 100.18 — > 15 °C antar komponen serupa · > 40 °C terhadap udara | ANSI/NETA ATS-2017 | PDF 246 |
| Kapan baterai diganti? | < 90% rating · turun > 10% · 85% umur layan | IEEE 1188-2005 | PDF 17 |
| Ventilasi ruang baterai? | `Q = v × q × s × n × I_gas × C_rt × 10⁻³` m³/jam | IEC 62485-2 | PDF 21 |
| Waktu deteksi hilang sinyal video? | Tabel 7 — 8 / 4 / 2 detik per security grade | BS EN 62676-1-2 | PDF 34 |
| Metode uji redaman serat SM? | Empat metode: one-cord · three-cord · two-cord · OTDR | IEC 61280-4-2 | PDF 17 |
| Proses forensik digital? | Empat tahap + rantai kustodi | Alsmadi, NICE Framework | PDF 268 |

---

## Tiga celah yang TIDAK tertutup — jangan disangka tertutup

1. **ONVIF ≠ BS EN 62676-1-2.** Yang masuk standar **transmisi** video, bukan
   interoperabilitas perangkat. Spesifikasi tender yang menyebut ONVIF belum terjawab.
2. **PUIL ≠ ANSI/NETA.** NETA menutup celah **ambang uji**, bukan celah **kepatuhan
   hukum Indonesia**. Seluruh buku kelistrikan di rak tetap berbasis AS/Inggris.
3. **NETA memberi ambang tahanan isolasi, BUKAN resistansi pembumian.** Dua besaran
   berbeda dan sering tertukar. Ambang pembumian tetap ditetapkan pemilik sistem.

Celah baru yang muncul justru karena batch 2: **ANSI/NETA MTS** (uji *pemeliharaan* —
yang ada di rak ATS, uji *terima*) dan **IEEE 450** (baterai *vented* — IEEE 1188 hanya
VRLA).
"""

DELTA = u"""# Delta Sistem — akibat batch 2

Berkas berikut **berubah** karena batch 2. Salinan lengkapnya ada di paket induk
`Pustaka-Teknis-GSP-Markdown.zip`; di sini hanya dicatat **apa** yang berubah, supaya
peninjau tahu bagian mana yang perlu dibaca ulang.

## Berkas rak

| Berkas | Perubahan |
|---|---|
| `KATALOG-RUMUS.md` | Bagian 13 baru — ambang dari lima standar |
| `TEMPLATE-BERITA-ACARA.md` | Kolom "sumber ambang" terisi untuk uji isolasi, termografi, baterai, dan serat SM |
| `PETA-CELAH-KOLEKSI.md` | Status celah diperbarui |
| `ASUMSI-BAKU.md` | Bagian baru **"Asumsi yang GUGUR"** — 7 besaran kini dikutip, bukan ditaksir |
| `DAFTAR-PENGADAAN-BAHAN.md` | Status batch 2 — tak satu pun dari 4 bahan tertutup penuh; bukti digital jadi 🟡 sebagian |
| `PROSEDUR-TAMBAH-BUKU.md` | Konvensi `_standar/_tesis/_panduan` + daftar berkas rujukan skill yang wajib ikut diperiksa |
| `RENCANA-KERJA.md` | T15–T18 |

## Berkas rujukan skill

| Berkas | Perubahan |
|---|---|
| `pustaka-teknis/SKILL.md` | 4 baris standar pada tabel domain + kaidah *standar didahulukan atas buku teks* |
| `pustaka-teknis/references/01-indeks-rumus.md` | Tabel "Ambang dari standar" — 8 baris |
| `pustaka-teknis/references/02-rantai-hitung-proyek.md` | Rantai termografi langkah 4: "TIDAK ADA di Vollmer" → NETA Tabel 100.18 |
| `pustaka-teknis/references/03-batas-dan-celah.md` | 4 baris "tidak ada" → ✅ ADA; ONVIF & ISO 27001 ditegaskan **masih** terbuka |
| `power-backup-sizing/references/04-batas-dan-peringatan.md` | Bagian 7 — IEEE 1188, IEC 62485-2, NETA |
| `fiber-link-design/references/02-uji-dan-berita-acara.md` | Bagian 6b — IEC 61280-4-2, empat metode, RTM, ORL |
| `grounding-lightning-design/references/03-verifikasi-dan-telusur.md` | Peringatan agar NETA tidak disalahpakai sebagai ambang pembumian |

> **Pelajaran yang dimasukkan ke prosedur:** menambah buku **tidak selesai di rak** —
> berkas rujukan skill ikut basi tanpa ada yang memberi tahu. Lima dari delapan berkas
> basi yang ditemukan pada pemindaian adalah berkas rujukan skill.
"""


def main():
    hilang = [s for s, _ in ISI if not os.path.exists(os.path.join(RAK, s))]
    if hilang:
        for h in hilang:
            print("HILANG:", h)
        raise SystemExit("berhenti — berkas sumber tidak lengkap")

    mentah = 0
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("README.md", README)
        z.writestr("DELTA-SISTEM.md", DELTA)
        mentah += len(README.encode("utf-8")) + len(DELTA.encode("utf-8"))
        for src, dst in ISI:
            data = io.open(os.path.join(RAK, src), encoding="utf-8").read()
            z.writestr(dst, data)
            mentah += len(data.encode("utf-8"))

    with zipfile.ZipFile(OUT) as z:
        rusak = z.testzip()
        n = len(z.namelist())

    print("keluaran   :", OUT)
    print("berkas     :", n)
    print("mentah     : %.1f KB" % (mentah / 1024))
    print("terkompresi: %.1f KB" % (os.path.getsize(OUT) / 1024))
    print("integritas :", "OK" if rusak is None else "RUSAK: " + rusak)
    print("sha256     :", hashlib.sha256(open(OUT, "rb").read()).hexdigest()[:16])


if __name__ == "__main__":
    main()
