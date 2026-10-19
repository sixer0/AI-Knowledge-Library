# -*- coding: utf-8 -*-
"""
Mengisi lapis dokumen EKAS: kartu pengetahuan, templat, dan README tiap map kerja.
Dijalankan setelah bangun_ekas_struktur.py.
"""
import io, os, csv

RAK = r"C:\Users\gspen\Videos\Buku"
EKAS = os.path.join(RAK, "GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM")


def tulis(rel, teks):
    p = os.path.join(EKAS, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, "w", encoding="utf-8").write(teks)


# ── isi khas tiap rujukan untuk kartu pengetahuan ────────────────────
ISI = {
 "REF-BAT-001": ("Ah = I × t ÷ DoD, lalu koreksi C-rate", "PDF 104, 109, 117",
   "Kerangka hitung kapasitas, rentang suhu timbal-asam tersegel −20…+50 °C",
   "DoD, umur siklus, dan kurva laju **wajib R4** — buku terbit 2000"),
 "REF-BAT-002": ("Q = v × q × s × n × I_gas × C_rt × 10⁻³ (m³/jam)", "PDF 15, 17, 19, 21",
   "Ambang ganti baterai < 90% rating · turun > 10% · 85% umur layan. Ventilasi ruang baterai",
   "Hanya **VRLA**. Baterai vented → IEEE 450, belum ada di rak. Derating ventilasi tidak diperbolehkan"),
 "REF-VSS-001": ("f = pD × d × s ÷ ph · GB = (Mb/s ÷ 8) × 3600 × jam × hari × kamera ÷ 1000",
   "PDF 115, 237–241, 277, 290",
   "Lensa, kerapatan piksel FI 250 / FR 125 pix/m, bitrate, kapasitas rekaman",
   "Sasaran pengamatan **ditetapkan pemilik**, bukan perancang. Bitrate nyata dari R4"),
 "REF-VSS-002": ("Tabel 7 — waktu deteksi hilang sinyal 8 / 4 / 2 detik", "PDF 34",
   "Persyaratan unjuk kerja transmisi video per security grade",
   "**Bukan ONVIF.** Interoperabilitas perangkat tidak tercakup"),
 "REF-CIP-001": ("—", "—",
   "Klasifikasi aset kritis, defense-in-depth, pemetaan ketergantungan",
   "Kualitatif. Persyaratan mengikat tetap R1/R2"),
 "REF-SEC-001": ("—", "PDF 268",
   "Proses forensik 4 tahap: collection · examination · analysis · reporting + rantai kustodi",
   "Meringkas, tidak menormakan. NIST SP 800-86 & ISO/IEC 27037 tetap perlu"),
 "REF-SEC-002": ("—", "—", "Kerangka keamanan sistem dan integritas catatan",
   "Tidak membahas penanganan bukti sebagai prosedur"),
 "REF-SEC-003": ("—", "—",
   "Hardening, event logging, threat detection, AD, program pembelajaran",
   "⚠ **Bundel campur.** NIST SP 800-50r1 dan advisori ASD-CISA/Joint CSI terkubur setingkat majalah. "
   "Bila mengutip, **rujuk dokumen aslinya terpisah** — jangan mengutip bundelnya"),
 "REF-SEC-004": ("—", "—",
   "Penunjuk ke UU 11/2008 (ITE) dan Peraturan BSSN No. 4/2021",
   "**Tidak pernah jadi sandaran akhir.** Yang dikutip pasal regulasi aslinya"),
 "REF-ELC-001": ("PI = R₁₀mnt ÷ R₁mnt (< 1) · DAR = R₆₀dtk ÷ R₃₀dtk (< 1,25)",
   "PDF 142, 144, 145",
   "Empat metode ukur isolasi, batas tegangan uji ≤ 75% terima / ≤ 60% pabrik",
   "Memberi **rasio dan metode**, bukan ambang MΩ mutlak"),
 "REF-ELC-002": ("Tabel 100.1 · koreksi suhu Tabel 100.14 · ΔT Tabel 100.18",
   "PDF 223, 241, 246",
   "600 V → 100 MΩ · 5 kV → 1.500 MΩ · 15 kV → 5.000 MΩ. ΔT > 15 °C antar komponen serupa atau > 40 °C terhadap udara",
   "**ATS = uji terima**, bukan pemeliharaan (MTS). **Bukan** ambang resistansi pembumian. Standar Amerika — bukan pengganti PUIL"),
 "REF-FO-001": ("rugi = (km × dB/km) + (n_konektor × 0,75) + (n_sambungan × rugi)",
   "PDF 98, 129, 145",
   "Loss budget, batas TIA-568 0,75 dB/konektor, 1 dB/km SM premises · 0,5 dB/km OSP, ambang = kolom terburuk",
   "OTDR **bukan pengganti** uji rugi OLTS"),
 "REF-FO-002": ("—", "cetak 37 / PDF 44",
   "OTDR, ketidakpastian ukur lab 0,02–0,05 dB/hari",
   "Terbit 2007 — periksa rujukan standarnya"),
 "REF-FO-003": ("Reflectance = 10 × log₁₀ (Pr ÷ Pin)", "PDF 14, 17, 20, 43",
   "Empat metode: one-cord · three-cord · two-cord · OTDR. RTM penyelesai perselisihan. ORL Annex E Method A",
   "**Singlemode saja.** Multimode → IEC 61280-4-1, belum ada. Tidak memberi angka ambang lulus"),
 "REF-PWR-001": ("kVA = (puncak ÷ PF) × derating × margin", "PDF 40–42, 136",
   "Kerangka derating lokasi, kelas rating genset",
   "⚠ **Bab 11 hilang** (± 55 hal). Faktor derating nyata **wajib R4**"),
 "REF-PWR-002": ("Rugi = P × (1 ÷ η − 1)", "PDF 20",
   "Rugi daya dan beban pendinginan UPS",
   "Terbit 2004 — **efisiensi wajib R4**"),
 "REF-GRD-001": ("ρ = 2 π a R", "PDF 562, 579–580, 1111, 1149",
   "Wenner, fall-of-potential, Apendiks G (daftar periksa) dan H (isi dokumentasi)",
   "⚠ **Tidak memberi ambang resistansi.** Prasyarat: konduktor penghubung dilepas sebelum diukur"),
 "REF-LPS-001": ("Rolling sphere — Level IV = 60 m", "PDF 89–90",
   "Tingkat proteksi, radius bola gelinding, peringatan mesh",
   "Mengutip **IEC 62305:2006** dan NFPA 780:2004 — nomor edisi usang"),
 "REF-RCM-001": ("interval = ½ × P-F · FFI = 2 × M_prkt × M_terproteksi ÷ M_majemuk",
   "PDF 31, 164, 166, 193, 195, 198",
   "Tujuh pertanyaan RCM, konsekuensi, 89% moda kegagalan tidak terkait umur",
   "Mengikat **hanya bila diadopsi kontrak**. Sasaran risiko ditetapkan pemilik"),
 "REF-RCM-002": ("—", "—", "Tata kelola, KPI, organisasi pemeliharaan", "Tidak memasok ambang teknis"),
 "REF-RCM-003": ("—", "—", "Perencanaan dan penjadwalan kerja pemeliharaan", "Terbit 2010"),
 "REF-MEC-001": ("—", "—", "Perhitungan mekanik — sangat banyak rumus",
   "Bookmark hanya sampai tingkat Part. Merangkum akan menyesatkan — buka panel bookmark 381 entri"),
 "REF-NET-001": ("—", "—", "Pola gangguan jaringan", "Terbit 2011 — platform tidak dijual lagi"),
 "REF-NET-002": ("—", "—", "Praktik jaringan terkini", "Edisi 2019 disimpan di `_arsip`"),
 "REF-NET-003": ("—", "—", "Dasar jaringan", "Edisi 7 (2017)"),
 "REF-NET-004": ("BDP = RTT × kapasitas_penyempit", "PDF 647, 769",
   "Window scaling wajib bila BDP > 64 kB",
   "Membahas protokol, **bukan perencanaan kapasitas**"),
 "REF-STG-001": ("RAID 5 = (n−1) × C · RAID 6 = (n−2) × C", "PDF 46–70",
   "Kapasitas terpakai, peringatan RAID 5, beban rekonstruksi",
   "Terbit 2009 — sebelum SSD/NVMe. **Unjuk kerja tulis wajib R4**"),
 "REF-OPS-001": ("—", "—", "Praktik operasional TI", "Tidak memasok ambang teknis"),
 "REF-THM-001": ("ΔT_serupa · ΔT_udara", "PDF 25, 128",
   "Delapan parameter wajib kamera, aturan IFOV",
   "**Buku fisika, bukan standar pemeliharaan.** Ambang ΔT dari NETA [R2]"),
 "REF-VAI-001": ("—", "—", "Dasar analitik video dan penglihatan komputer", "Tidak memasok ambang"),
}

BOLEH = {
 "R2": u"**Ya**, bila standar diadopsi kontrak dan edisinya tervalidasi",
 "R3": u"**Tidak sendirian.** Hanya bila kontrak mengadopsinya secara tertulis",
 "R5": u"**Tidak pernah.** Telusuri sumber primernya lebih dulu",
}
STATUS = {"R2": "ACTIVE_WITH_SCOPE_LIMITS", "R3": "ACTIVE", "R5": "POINTER_ONLY"}


def kartu(r):
    rid, R, judul, dom = r["reference_id"], r["r_level"], r["title"], r["domain"]
    rumus, hal, pasok, batas = ISI.get(rid, ("—", "—", "—", "—"))
    return u"""---
record_type: knowledge_card
reference_id: %s
reference_confidence_level: %s
title: "%s"
domain: %s
authority_status: %s
vault_path: %s
resume_path: %s
---

# %s — %s

**Tingkat keyakinan:** **%s** · **Status otoritas:** `%s`
**Laci sumber:** `%s`
**Resume lengkap:** `%s`

---

## 1. Yang dipasok rujukan ini

%s

**Halaman jangkar:** %s

## 2. Rumus / metode

```
%s
```

Setiap angka yang diambil dari sini **wajib ditandai** salah satu dari:
`SOURCE-DERIVED` · `PROJECT-DERIVED` · `OEM-DERIVED` · `ASSUMPTION`.

## 3. Boleh menetapkan ambang terima?

%s

## 4. Batas pemakaian — baca sebelum mengutip

%s

## 5. Rantai jaminan

```
REQUIREMENT → %s (%s) → KEPUTUSAN DESAIN → PERHITUNGAN → UJI → BUKTI → TERIMA
```

Dilarang melompat dari **rujukan langsung ke ambang terima** tanpa catatan keputusan dan
bukti verifikasi. Rantai domain lengkap: `05_DOMAIN-KNOWLEDGE/%s/RANTAI-JAMINAN.md`

## 6. Gate minimum sebelum ditutup

G0 sumber tervalidasi · G1 kebutuhan dibekukan · G2 desain disetujui ·
G3 hitungan diperiksa orang kedua · G4 metode uji disetujui · G5 uji lulus dengan bukti mentah ·
G6 bukti serah lengkap · G7 diterima pemberi kerja

Rincian: `01_GOVERNANCE/ASSURANCE-GATES.md`
""" % (rid, R, judul.replace('"', "'"), dom, STATUS.get(R, "ACTIVE"),
       r["vault_path"], r["resume_path"], rid, judul, R, STATUS.get(R, "ACTIVE"),
       r["vault_path"], r["resume_path"], pasok, hal, rumus, BOLEH.get(R, "—"),
       batas, rid, R, dom)


MAP_README = {
 "06_ENGINEERING/REQUIREMENTS": (u"Kebutuhan proyek",
   u"Satu berkas per proyek. Kebutuhan yang **dibekukan** sebelum desain dimulai (gate G1).",
   u"Kebutuhan yang berubah setelah G1 wajib lewat catatan perubahan — bukan disunting diam-diam."),
 "06_ENGINEERING/DESIGN-DECISIONS": (u"Catatan keputusan desain",
   u"Satu berkas per keputusan. Pakai `10_TEMPLATES/TPL-01`.",
   u"**Alternatif yang ditolak wajib ditulis.** Keputusan tanpa alternatif terlihat sewenang-wenang."),
 "06_ENGINEERING/ASSUMPTIONS": (u"Asumsi",
   u"`ASUMSI-BAKU.md` memuat asumsi baku lintas proyek; asumsi khas proyek ditulis per berkas.",
   u"Tiap asumsi wajib punya **sensitivitas** dan **rencana penggantian data**."),
 "06_ENGINEERING/CALCULATIONS": (u"Perhitungan",
   u"`KATALOG-RUMUS.md` induk rumus. Lembar hitung per proyek pakai `TPL-02`.",
   u"Tandai tiap masukan: `SOURCE-DERIVED` / `PROJECT-DERIVED` / `OEM-DERIVED` / `ASSUMPTION`."),
 "06_ENGINEERING/DESIGN-REVIEWS": (u"Tinjauan desain",
   u"Catatan tinjauan dan penutupan temuan.",
   u"Gate G3 menuntut hitungan diperiksa **orang kedua** — tinjauan ini buktinya."),
 "07_VERIFICATION-VALIDATION/ITP": (u"Inspection & Test Plan",
   u"Rencana inspeksi dan uji per proyek: apa diuji, kapan, oleh siapa, disaksikan siapa.",
   u"ITP disetujui sebelum uji dimulai, bukan disusun setelahnya."),
 "07_VERIFICATION-VALIDATION/FAT": (u"Factory Acceptance Test",
   u"Uji di pabrik/bengkel sebelum kirim.", u"Lulus FAT tidak menggantikan SAT."),
 "07_VERIFICATION-VALIDATION/SAT": (u"Site Acceptance Test",
   u"Uji di lokasi terpasang.", u"Ambangnya sama dengan yang tertulis di ITP — jangan diturunkan di lapangan."),
 "07_VERIFICATION-VALIDATION/TEST-PROCEDURES": (u"Prosedur uji",
   u"`TEMPLATE-BERITA-ACARA.md` memuat kerangka 8 jenis uji beserta sumber ambangnya.",
   u"Prosedur menyebut **metode + alat + ambang + sumber ambang**."),
 "07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA": (u"Kriteria terima",
   u"Satu berkas per jenis uji: ambang, sumbernya, dan tingkat R-nya.",
   u"⚠ Ambang bersumber **R3 wajib diadopsi kontrak**. Ambang tanpa sumber tidak sah."),
 "07_VERIFICATION-VALIDATION/NON-CONFORMANCE": (u"Ketidaksesuaian",
   u"Temuan yang tidak memenuhi ambang, beserta tindakan koreksinya.",
   u"NCR ditutup dengan **bukti uji ulang**, bukan dengan pernyataan."),
 "08_EVIDENCE/MEASUREMENT": (u"Hasil ukur mentah", u"Berkas mentah dari alat ukur.",
   u"**Jangan menyunting berkas mentah.** Olahannya disimpan terpisah."),
 "08_EVIDENCE/OTDR": (u"Jejak OTDR", u"Berkas `.sor` dan laporan jejak.",
   u"Sertakan setelan: lebar pulsa, rentang, launch cable."),
 "08_EVIDENCE/OLTS": (u"Hasil uji rugi sisipan", u"Keluaran OLTS/LSPM per core.",
   u"Sertakan rugi kabel referensi terukur (syarat ≤ 0,5 dB)."),
 "08_EVIDENCE/GROUNDING": (u"Bukti uji pembumian", u"Data Wenner dan fall-of-potential.",
   u"⚠ Wajib memuat **pernyataan konduktor penghubung telah dilepas**."),
 "08_EVIDENCE/ELECTRICAL": (u"Bukti uji kelistrikan", u"Megger, PI/DAR, termografi.",
   u"Wajib mencatat **suhu saat ukur** — tanpa itu hasilnya tidak dapat dibandingkan."),
 "08_EVIDENCE/SCREENSHOTS-LOGS": (u"Tangkapan layar dan log", u"Bukti konfigurasi dan perilaku sistem.",
   u"Sertakan penanda waktu yang terbaca."),
 "08_EVIDENCE/PHOTO": (u"Foto", u"Foto pemasangan, label, dan kondisi terpasang.",
   u"Untuk termografi: citra termal **berpasangan** dengan citra tampak."),
 "08_EVIDENCE/CERTIFICATES": (u"Sertifikat", u"Kalibrasi alat, sertifikat produk, sertifikat personel.",
   u"Kalibrasi harus **masih berlaku pada tanggal uji** — bukan pada tanggal serah."),
 "09_HANDOVER/AS-BUILT": (u"Gambar terbangun", u"Gambar sesuai kondisi terpasang.",
   u"Perbedaan terhadap gambar rancangan wajib dijelaskan."),
 "09_HANDOVER/ASSET-REGISTER": (u"Daftar aset", u"Aset terpasang beserta rujukan pemeliharaannya.",
   u"Kolom `interval_basis` menyebut **dari mana intervalnya** — hitungan, standar, atau kontrak."),
 "09_HANDOVER/CONFIGURATION-BACKUP": (u"Cadangan konfigurasi", u"Konfigurasi perangkat saat serah.",
   u"Sertakan versi firmware/perangkat lunak saat dicadangkan."),
 "09_HANDOVER/TEST-RESULT": (u"Hasil uji terkompilasi", u"Rekap hasil seluruh pengujian.",
   u"Tiap baris menunjuk ke bukti mentahnya di `08_EVIDENCE/`."),
 "09_HANDOVER/TRAINING": (u"Pelatihan", u"Materi, daftar hadir, dan evaluasi.",
   u"Daftar hadir bertanda tangan adalah buktinya, bukan materinya."),
 "09_HANDOVER/O&M-MANUAL": (u"Manual operasi & pemeliharaan", u"Termasuk tugas dan interval hasil analisis RCM.",
   u"Uraian tugas harus **dapat dikerjakan orang lapangan**, bukan judul kegiatan."),
 "09_HANDOVER/BERITA-ACARA": (u"Berita acara", u"Dokumen serah terima bertanda tangan.",
   u"Tiap BA menyebut **ambang beserta sumbernya**. Simpan kartu kendali bersamanya."),
}

TEMPLAT = [
 ("TPL-01-DESIGN-DECISION-RECORD.md", u"Catatan Keputusan Desain (DDR)", u"""
| Butir | Isi |
|---|---|
| **DDR-ID** | |
| Proyek | |
| Tanggal | |
| Penyusun / Penyetuju | |

## 1. Keputusan
_Satu kalimat: apa yang ditetapkan._

## 2. Konteks dan kebutuhan yang memicu
_Rujuk REQ-ID pada `02_REGISTERS/REQUIREMENT-REGISTER.csv`._

## 3. Rujukan yang dipakai

| REF-ID | Tingkat | Halaman | Yang diambil |
|---|---|---|---|
| | | | |

## 4. Alternatif yang dipertimbangkan dan **ditolak**

| Alternatif | Alasan penolakan |
|---|---|
| | |

> Bagian ini **wajib terisi.** Keputusan tanpa alternatif tidak dapat dinilai.

## 5. Konflik antar-sumber
_Bila dua sumber berbeda, catat di sini — jangan memilih diam-diam._

## 6. Akibat ke hilir
_Perhitungan, pengujian, dan bukti apa yang menjadi wajib karena keputusan ini._
"""),
 ("TPL-02-CALCULATION-SHEET.md", u"Lembar Perhitungan", u"""
| Butir | Isi |
|---|---|
| **CALC-ID** | |
| Besaran yang dihitung | |
| Disusun / Diperiksa | |

## 1. Rumus dan sumbernya

```
```
**Sumber rumus:** [R_] ................ halaman ........

## 2. Masukan

| Masukan | Nilai | Satuan | Tag | Sumber |
|---|---|---|---|---|
| | | | `SOURCE-DERIVED` / `PROJECT-DERIVED` / `OEM-DERIVED` / `ASSUMPTION` | |

## 3. Hasil

## 4. Kepekaan
_Untuk tiap masukan bertanda `ASSUMPTION`: bila meleset ±50%, hasilnya menjadi berapa._

## 5. Rencana penggantian asumsi
_Data apa yang akan menggantikan, dari siapa, kapan._

## 6. Pemeriksaan orang kedua (gate G3)
Diperiksa oleh .............. tanggal .......... · Temuan: ..........
"""),
 ("TPL-03-TEST-PROCEDURE.md", u"Prosedur Uji", u"""
| Butir | Isi |
|---|---|
| **TEST-ID** | |
| Jenis uji | |
| Objek uji | |

## 1. Metode
**Metode:** .................. **Sumber metode:** [R_] .......... hal. ..........

## 2. Alat
| Alat | Merek/tipe | No. seri | Kalibrasi berlaku s.d. |
|---|---|---|---|

## 3. Ambang terima
**Ambang:** .................. **Sumber ambang:** [R_] .......... hal. ..........

☐ Sumber ambang R1/R2 → sah
☐ Sumber ambang R3 → **wajib diadopsi kontrak**, pasal ..........
☐ Ambang belum ditetapkan → **uji dilaporkan tanpa pernyataan lulus**

## 4. Prasyarat
_Kondisi yang harus dipenuhi sebelum uji dimulai._

## 5. Langkah
## 6. Pencatatan
_Data apa yang dicatat, dalam bentuk apa._
## 7. Penyaksi
"""),
 ("TPL-04-ACCEPTANCE-RECORD.md", u"Catatan Penerimaan", u"""
| Butir | Isi |
|---|---|
| **ACC-ID** | |
| TEST-ID terkait | |
| Tanggal | |

## 1. Hasil terukur
| Objek | Nilai mentah | Koreksi | Nilai terkoreksi | Ambang | Lulus? |
|---|---|---|---|---|---|

## 2. Ambang dan sumbernya
## 3. Ketidaksesuaian
_NCR-ID bila ada._
## 4. Kesimpulan dan tanda tangan
"""),
 ("TPL-05-HANDOVER-EVIDENCE-PACK.md", u"Paket Bukti Serah Terima", u"""
Daftar periksa kelengkapan sebelum serah terima dinyatakan lengkap (gate G6).

| Butir | Ada | Lokasi |
|---|---|---|
| Gambar as-built | ☐ | `09_HANDOVER/AS-BUILT/` |
| Daftar aset | ☐ | `09_HANDOVER/ASSET-REGISTER/` |
| Cadangan konfigurasi + versi firmware | ☐ | `09_HANDOVER/CONFIGURATION-BACKUP/` |
| Rekap hasil uji | ☐ | `09_HANDOVER/TEST-RESULT/` |
| **Bukti mentah tiap uji** | ☐ | `08_EVIDENCE/` |
| Sertifikat kalibrasi (berlaku saat uji) | ☐ | `08_EVIDENCE/CERTIFICATES/` |
| Manual O&M + tugas & interval | ☐ | `09_HANDOVER/O&M-MANUAL/` |
| Rekaman pelatihan | ☐ | `09_HANDOVER/TRAINING/` |
| Berita acara bertanda tangan | ☐ | `09_HANDOVER/BERITA-ACARA/` |
| **Kartu kendali tiap besaran** | ☐ | dilampirkan pada BA |
| Daftar asumsi yang masih terbuka | ☐ | |
| Daftar butir menunggu data OEM [R4] | ☐ | |

> Dua baris terakhir yang paling sering hilang. Pekerjaan boleh diserahkan dengan asumsi
> terbuka — **asalkan tertulis**. Yang tidak boleh adalah asumsi yang tidak terlihat.
"""),
 ("TPL-06-REQUIREMENT-TRACEABILITY.md", u"Ketertelusuran Kebutuhan", u"""
Satu baris per kebutuhan, ditelusuri sampai bukti.

| REQ-ID | Kebutuhan | REF-ID | R | DDR-ID | CALC-ID | TEST-ID | EVIDENCE-ID | Status |
|---|---|---|---|---|---|---|---|---|

**Aturan:** baris yang kolom `EVIDENCE-ID`-nya kosong **belum selesai**, sekalipun
pekerjaan fisiknya sudah rampung.
"""),
 ("TPL-07-SOURCE-UPDATE-REQUEST.md", u"Permintaan Pembaruan Sumber", u"""
Dipakai saat sebuah sumber perlu ditambah, diganti edisi, atau diturunkan statusnya.

| Butir | Isi |
|---|---|
| **SUR-ID** | |
| Sumber yang diminta | |
| Tingkat R yang diharapkan | |
| Celah yang ditutup (GAP-ID) | |
| Pemicu | ☐ celah baru ☐ edisi baru terbit ☐ sumber lama usang ☐ temuan proyek |

## Akibat bila tidak diperoleh
_Pekerjaan apa yang tidak dapat dinyatakan memenuhi._

## Berkas yang wajib diperbarui setelah sumber masuk
☐ `02_REGISTERS/MASTER-REFERENCE-REGISTER.csv`
☐ `02_REGISTERS/GAP-REGISTER.csv`
☐ `04_KNOWLEDGE-CARDS/<domain>/`
☐ `05_DOMAIN-KNOWLEDGE/<domain>/RANTAI-JAMINAN.md`
☐ `06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md` — asumsi yang gugur
☐ `07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/`
☐ Berkas rujukan skill di luar EKAS
"""),
]


def main():
    reg = os.path.join(EKAS, "02_REGISTERS", "MASTER-REFERENCE-REGISTER.csv")
    rows = list(csv.DictReader(io.open(reg, encoding="utf-8")))
    for r in rows:
        tulis("04_KNOWLEDGE-CARDS/%s/%s.md" % (r["domain"], r["reference_id"]), kartu(r))

    for rel, (judul, isi, aturan) in MAP_README.items():
        tulis(rel + "/README.md", u"""# %s

%s

> **Aturan map ini:** %s

Kosong saat ini — diisi per proyek.
""" % (judul, isi, aturan))

    for nama, judul, isi in TEMPLAT:
        tulis("10_TEMPLATES/" + nama, u"# %s\n%s" % (judul, isi))

    print("kartu pengetahuan :", len(rows))
    print("README map kerja  :", len(MAP_README))
    print("templat           :", len(TEMPLAT))


if __name__ == "__main__":
    main()
