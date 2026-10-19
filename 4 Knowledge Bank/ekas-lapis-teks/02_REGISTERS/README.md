# Register

Delapan `.csv` supaya dapat disaring, diurutkan, dan dibaca mesin — plus tiga `.md` penjelas.

| Berkas | Baris terisi | Diisi oleh |
|---|---|---|
| [`MASTER-REFERENCE-REGISTER.csv`](MASTER-REFERENCE-REGISTER.csv) | **103** | pengelola rak |
| [`GAP-REGISTER.csv`](GAP-REGISTER.csv) | **35** (32 terbuka, 2 sebagian, 1 by-design) | pengelola rak |
| [`REQUIREMENT-REGISTER.csv`](REQUIREMENT-REGISTER.csv) | 4 | tim proyek |
| [`DESIGN-DECISION-REGISTER.csv`](DESIGN-DECISION-REGISTER.csv) | 1 | tim proyek |
| [`CALCULATION-REGISTER.csv`](CALCULATION-REGISTER.csv) | 1 | tim proyek |
| [`TEST-REGISTER.csv`](TEST-REGISTER.csv) | 1 | tim proyek |
| [`EVIDENCE-REGISTER.csv`](EVIDENCE-REGISTER.csv) | 12 | tim proyek |
| [`ASSET-REFERENCE-REGISTER.csv`](ASSET-REFERENCE-REGISTER.csv) | 0 | tim proyek |

Catatan koreksi tertanggal 11-10-2026 (kartu IDX-REPAIR-H, langkah 29/G3 misi
KORPUS-LANJUTAN-1011): seluruh angka pada kolom 'Baris terisi' di atas diregenerasi
dari parser CSV saat eksekusi (`csv.DictReader`, metode identik dengan CHECK H pada
`gsp-hermes/scripts/korpus-index-repair-1005/check_gate.py`), bukan dari arsip.
Nilai lama menjadi baru: MASTER-REFERENCE 62 menjadi 103; GAP 21 menjadi 35
(rincian status ikut terukur: 32 terbuka, 2 sebagian, 1 by-design); REQUIREMENT 0
menjadi 4; DESIGN-DECISION 0 menjadi 1; CALCULATION 0 menjadi 1; TEST 0 menjadi 1;
EVIDENCE 0 menjadi 12; ASSET-REFERENCE tetap 0. Angka lama adalah warisan sensus
Agustus dan sudah melewatkan hasil langkah 18-29 (resume W3, merge R3, tulis GAP
CHAIN-C). Folder ini kini juga memuat dua csv di luar delapan register kanonis yang
sengaja tidak ikut tabel: [`INTAKE-QUEUE.csv`](INTAKE-QUEUE.csv) (308 baris data) dan
[`KEMAMPUAN-REGISTER.csv`](KEMAMPUAN-REGISTER.csv) (372 baris data); keanggotaan tabel delapan register adalah
keputusan pengelola rak, bukan lingkup kartu ini.

Hanya [`ASSET-REFERENCE-REGISTER.csv`](ASSET-REFERENCE-REGISTER.csv) yang kini masih kosong dan **berisi kepala
kolom**; kepala kolom itulah yang menetapkan data apa yang wajib dicatat. Kolom
yang paling menentukan:

- `TEST-REGISTER.criterion_source` + `r_level` — **dari mana ambangnya**. Kolom ini yang
  membedakan pengujian dari penyesuaian.
- `CALCULATION-REGISTER.input_tags` — tiap masukan bertanda `SOURCE-DERIVED` /
  `PROJECT-DERIVED` / `OEM-DERIVED` / `ASSUMPTION`.
- `ASSET-REFERENCE-REGISTER.interval_basis` — **dasar intervalnya**: hitungan, standar,
  atau kontrak.

Penjelasan naratif: [`MASTER-REFERENCE-REGISTER.md`](MASTER-REFERENCE-REGISTER.md) (seluruh sumber terklasifikasi) ·
[`GAP-REGISTER.md`](GAP-REGISTER.md) (peta celah) · [`GAP-ACQUISITION-PLAN.md`](GAP-ACQUISITION-PLAN.md) (rencana pengadaan).

---

## Kaidah domain (ditetapkan 05-10-2026, misi KORPUS-IDX-REPAIR-1005 butir G6)

Folder kartu di `04_KNOWLEDGE-CARDS/<domain>/` SELALU memakai nama domain kurasi yang
sama dengan folder di `05_DOMAIN-KNOWLEDGE/<domain>/` dan kolom `domain` register ini.
Label triase mesin dari `90_TOOLS/triase_korpus.py` (mis. `STORAGE-DATACENTER`,
`PERLU-DINILAI`) BUKAN nama domain: label itu hidup di [`INTAKE-QUEUE.csv`](INTAKE-QUEUE.csv) sampai
barisnya dinilai manusia, dan tidak boleh menjadi folder kartu maupun nilai `domain`
di register.

Preseden: kartu `REF-OEM-STG` (R4, laci `SERVER-STORAGE`) semula menempati folder
`STORAGE-DATACENTER` padahal kartu itu sendiri menyatakan menopang Rantai H milik
`STORAGE` - rantai yang sudah mencatat baris 'Lembar data pengendali RAID & cakram
(R4)'. Sejak 05-10-2026 kartunya berada di `STORAGE/`; kedua himpunan folder kini
20 = 20 dan audit berikutnya tidak perlu lagi melaporkan selisih ini.

Bila kelak pusat data butuh domain sendiri (TIA-942, pendinginan, tata letak rak -
GAP-REGISTER prioritas menengah butir f), domain baru dibuat saat resume/rantainya
nyata ada, bukan sebagai folder kosong.
