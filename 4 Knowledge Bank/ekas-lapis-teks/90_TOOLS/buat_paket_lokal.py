# -*- coding: utf-8 -*-
"""
BUAT PAKET LOKAL — mengemas seluruh lapis teks EKAS ke satu .zip untuk
diolah model bahasa lokal.

Yang MASUK  : seluruh .md dan .csv (pengetahuan, register, rantai, kartu, resume, templat)
Yang KELUAR : PDF (3 GB), .zip arsip, berkas biner apa pun

Jalankan:  python buat_paket_lokal.py
"""
import io, os, re, sys, csv, glob, zipfile, hashlib, collections

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

EKAS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(os.path.dirname(EKAS), "GSP-EKAS-untuk-model-lokal.zip")
NL = chr(10)

IKUT = (".md", ".csv")
LEWAT_MAP = {"99_ARCHIVE", "95_IMPORT-SNAPSHOTS", "__pycache__"}


def kumpulkan():
    hasil = []
    for akar, dirs, berkas in os.walk(EKAS):
        dirs[:] = [d for d in dirs if d not in LEWAT_MAP]
        for b in sorted(berkas):
            if b.lower().endswith(IKUT):
                p = os.path.join(akar, b)
                hasil.append((p, os.path.relpath(p, EKAS).replace(os.sep, "/")))
    # perkakas ikut, supaya model tahu daftar & pemeriksa dibangkitkan bukan diketik
    for p in sorted(glob.glob(os.path.join(EKAS, "90_TOOLS", "*.py"))):
        hasil.append((p, os.path.relpath(p, EKAS).replace(os.sep, "/")))
    return hasil


def readme():
    reg = list(csv.DictReader(io.open(
        os.path.join(EKAS, "02_REGISTERS", "MASTER-REFERENCE-REGISTER.csv"), encoding="utf-8")))
    c = collections.Counter(r["r_level"] for r in reg)
    rantai = sorted(os.path.basename(os.path.dirname(p)) for p in
                    glob.glob(os.path.join(EKAS, "05_DOMAIN-KNOWLEDGE", "*", "RANTAI-JAMINAN.md")))
    pdf = len(glob.glob(os.path.join(EKAS, "03_SOURCE-VAULT", "**", "*.pdf"), recursive=True))
    return u"""# GSP EKAS — paket teks untuk model bahasa lokal

Engineering Knowledge & Assurance System milik PT Gemilang Satria Perkasa.
Dikemas 21 Agustus 2026.

## Apa isi paket ini

**Seluruh lapis teks** sistem: pengetahuan, register, rantai jaminan, kartu rujukan, resume
buku, templat, dan tata kelola.

**Yang TIDAK ikut: berkas PDF sumbernya** — %d berkas, sekitar 3 GB. Paket ini berisi
**pengetahuan yang sudah diekstrak** dari PDF itu, lengkap dengan nomor halamannya.

Bila sebuah jawaban menuntut membuka halaman aslinya, **itu pekerjaan manusia**, bukan model.
Jalur berkasnya tertulis pada kolom `vault_path` di register.

---

## Aturan yang WAJIB diikuti saat memakai paket ini

### 1. Setiap angka membawa tingkat keyakinan sumbernya

| | Jenis | Boleh menetapkan ambang lulus/tidak lulus? |
|---|---|---|
| **R1** | Regulasi Indonesia / SNI | ✅ ya — mengikat secara hukum |
| **R2** | Standar internasional (IEC, IEEE, BS EN, ANSI/NETA) | ✅ ya bila diadopsi kontrak |
| **R3** | Buku teks / handbook | ⚠ **tidak sendirian** — hanya bila kontrak mengadopsinya tertulis |
| **R4** | Dokumentasi pabrikan (OEM) | ✅ **wajib** untuk angka yang melekat produk |
| **R5** | Tesis, makalah, panduan | ❌ **tidak pernah** — penunjuk saja |

**Sebaran rak ini: R1=%d · R2=%d · R3=%d · R4=%d · R5=%d baris register (%d berkas PDF).**

### 2. R1 kosong — dan itu menentukan banyak jawaban

**Tidak ada satu pun regulasi Indonesia di rak.** Setiap pertanyaan tentang kepatuhan
PUIL, SNI, UU ITE, atau Peraturan BSSN **harus dijawab "tidak ada di rak"**, bukan dijawab
dari pengetahuan umum.

### 3. Bentuk jawaban yang benar saat sumbernya tidak ada

> *"Ambang resistansi pembumian tidak tersedia di rak ini. Joffe & Lock [R3] memberi metode
> pengukurannya, bukan ambangnya. Ambang harus ditetapkan pemilik sistem secara tertulis
> atau diambil dari PUIL/SNI [R1] — yang belum ada di rak. Lihat GAP-001."*

**Yang dilarang:**

> ~~"Umumnya ambang resistansi pembumian adalah 5 Ω."~~

Kalimat kedua terdengar membantu dan justru paling berbahaya: ia terlihat seperti fakta,
tidak membawa sumber, dan akan disalin ke dokumen serah oleh orang yang tidak tahu asalnya.

### 4. Tiga rantai jaminan PUTUS — ambangnya tidak ada

| Rantai | Domain | Yang tidak ada |
|---|---|---|
| **D** | GROUNDING-LIGHTNING | Ambang resistansi pembumian |
| **J** | CYBERSECURITY | **Seluruh R1/R2** — UU ITE, Perban BSSN, ISO 27001, NIST SP 800-86, ISO 27037 |
| **K** | CIVIL-STRUCTURAL | Empat SNI struktur: 1726, 1727, 1729, 2847 |

Pada ketiganya **metode tersedia tetapi ambang tidak**. Menghitung boleh; menyatakan lulus
tidak.

> ⚠ **Rantai K punya batas tambahan:** struktur yang gagal dapat menimpa orang. Perhitungan
> yang menanggung keselamatan **wajib ditandatangani ahli bersertifikat** — rak ini membuat
> mampu memeriksa dan berdiskusi, bukan menggantikan tanda tangan itu.

### 5. Buku berbasis standar Amerika — metodenya boleh, angkanya tidak

Seluruh buku sipil, bangunan, dan sebagian kelistrikan berbasis **ASCE 7, AISC, ACI 318,
ASTM, IBC, NEC, NFPA, ASHRAE**. Padanan Indonesianya tidak ada di rak.

Contoh paling nyata: **tabel profil baja Segui adalah profil W/HP/HSS Amerika**, bukan
WF/H-beam SNI. Dimensinya berbeda — **tidak dapat dipakai langsung** meski terlihat mirip.

---

## Peta isi

| Map | Isi | Mulai dari sini bila… |
|---|---|---|
| `00_START-HERE/` | README, peta sistem, kendali dokumen, riwayat, temuan uji coba | …baru pertama memakai |
| `01_GOVERNANCE/` | **R1–R5**, status otoritas, alur jaminan, **gate G0–G7**, kebijakan AI | …perlu tahu aturannya |
| `02_REGISTERS/` | Register rujukan · celah · enam register proyek | …mencari daftar |
| `03_SOURCE-VAULT/` | **Hanya `_ISI.md`** — manifest tiap laci; PDF-nya tidak ikut | …mencari letak berkas |
| `04_KNOWLEDGE-CARDS/` | **62 kartu** — satu per rujukan, memuat **batas pemakaian** | …ingin tahu bobot sebuah sumber |
| `05_DOMAIN-KNOWLEDGE/` | Resume buku + **%d rantai jaminan** | …mengerjakan proyek nyata |
| `06`–`09` | Map kerja proyek + **contoh P00** yang sudah dijalankan | …menyusun dokumen |
| `10_TEMPLATES/` | TPL-00 … TPL-09 | …butuh bentuk isian |
| `90_TOOLS/` | Perkakas — termasuk pemeriksa keutuhan | …ingin tahu apa yang dibangkitkan otomatis |

## Urutan membaca yang disarankan

1. `01_GOVERNANCE/REFERENCE-CONFIDENCE-LEVEL.md` — aturan R1–R5
2. `01_GOVERNANCE/ASSURANCE-GATES.md` — gate G0–G7
3. `02_REGISTERS/MASTER-REFERENCE-REGISTER.csv` — daftar seluruh rujukan
4. `05_DOMAIN-KNOWLEDGE/<domain>/RANTAI-JAMINAN.md` — sesuai pekerjaan yang ditanyakan
5. `04_KNOWLEDGE-CARDS/<domain>/<REF-ID>.md` — batas pemakaian sebelum mengutip

## Rantai jaminan yang tersedia (%d dari 22 domain)

%s

Sepuluh domain lain **belum punya rantai** — bila pertanyaannya menyentuh domain itu,
nyatakan bahwa jalur dari rujukan ke bukti serah **belum disusun**.

## Berkas yang dibangkitkan otomatis — jangan disunting

- `04-daftar-rujukan-lengkap.md` (di skill) ← `90_TOOLS/bangun_daftar_skill.py`
- `_ISI.md` tiap laci ← alat serap/migrasi
- `INTAKE-QUEUE.csv`, `INTAKE-RINGKAS.md` ← `90_TOOLS/triase_korpus.py`

## Pemeriksa keutuhan

`90_TOOLS/periksa_ekas.py` memeriksa delapan hal dan keluar dengan kode 1 bila ada **GALAT**.
Keadaan saat pengemasan: **GALAT 0 · PERINGATAN 1**.
""" % (pdf, c["R1"], c["R2"], c["R3"], c["R4"], c["R5"], pdf,
       len(rantai), len(rantai), NL.join(u"- **%s**" % d for d in rantai))


def main():
    isi = kumpulkan()
    rd = readme()
    mentah = len(rd.encode("utf-8"))
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("BACA-DULU.md", rd)
        for p, rel in isi:
            data = io.open(p, encoding="utf-8", errors="replace").read()
            z.writestr(rel, data)
            mentah += len(data.encode("utf-8"))

    with zipfile.ZipFile(OUT) as z:
        rusak = z.testzip()
        nama = z.namelist()
    c = collections.Counter(n.split("/")[0] if "/" in n else "(akar)" for n in nama)

    print("keluaran   :", OUT)
    print("berkas     :", len(nama))
    print("mentah     : %.0f KB" % (mentah / 1024))
    print("terkompresi: %.0f KB" % (os.path.getsize(OUT) / 1024))
    print("integritas :", "OK" if rusak is None else "RUSAK: " + rusak)
    print("sha256     :", hashlib.sha256(open(OUT, "rb").read()).hexdigest()[:16])
    print()
    for k in sorted(c):
        print("  %-28s %3d" % (k, c[k]))


if __name__ == "__main__":
    main()
