# -*- coding: utf-8 -*-
"""
SERAP R3 — memasukkan buku rujukan hasil triase ke 03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/

BERBEDA dari serap_r4.py: daftarnya DITULIS TANGAN, bukan hasil tebakan mesin.

Alasannya: dari 133 kandidat R3 hasil triase, hanya 13 yang benar-benar buku rujukan.
Sisanya dokumen kerja GSP sendiri (38), lembar data produk, dan berkas di luar lingkup.
Menyerap semuanya secara otomatis akan memasukkan dokumen kerja ke laci sumber —
kesalahan yang jauh lebih mahal daripada mengetik 13 baris.

Jalankan:  python serap_r3.py            uji coba
           python serap_r3.py --jalankan  menyalin sungguhan
"""
import io, os, re, sys, csv, shutil, hashlib

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RAK = r"C:\Users\gspen\Videos\Buku"
EKAS = os.path.join(RAK, "GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM")
VAULT = os.path.join(EKAS, "03_SOURCE-VAULT")
QUEUE = os.path.join(EKAS, "02_REGISTERS", "INTAKE-QUEUE.csv")
JALANKAN = "--jalankan" in sys.argv

# (potongan nama berkas, laci tujuan, catatan)
DAFTAR = [
 # ── laci baru: CIVIL-STRUCTURAL ──────────────────────────────────
 ("Russell Hibbeler - Structural Analysis",
  "R3_TEXTBOOK-HANDBOOK/CIVIL-STRUCTURAL", "Analisis struktur — menara, dudukan, portal"),
 ("David Darwin, Charles W. Dolan, Arthur H Nilson - Design of Concrete",
  "R3_TEXTBOOK-HANDBOOK/CIVIL-STRUCTURAL", "Perancangan beton bertulang — pondasi, pier"),
 ("William T. Segui - Steel Design",
  "R3_TEXTBOOK-HANDBOOK/CIVIL-STRUCTURAL", "Perancangan baja — menara, rangka, bracket"),
 ("Mamlouk, Michael S._ Zaniewski, John P. - Materials for civil",
  "R3_TEXTBOOK-HANDBOOK/CIVIL-STRUCTURAL", "Sifat bahan konstruksi"),
 # ── laci baru: GEOSPATIAL-SURVEY ─────────────────────────────────
 ("Paul Bolstad and Steven Manson - GIS Fundamentals",
  "R3_TEXTBOOK-HANDBOOK/GEOSPATIAL-SURVEY", "Dasar GIS — proyeksi, datum, analisis spasial"),
 ("Mastin, Tom B._ Kavanagh, Barry F - Surveying",
  "R3_TEXTBOOK-HANDBOOK/GEOSPATIAL-SURVEY", "Ilmu ukur tanah — pengukuran lapangan, koordinat"),
 # ── laci baru: PROJECT-QUALITY ───────────────────────────────────
 ("John M. Nicholas_ Herman Steyn - Project management for engineering",
  "R3_TEXTBOOK-HANDBOOK/PROJECT-QUALITY", "Manajemen proyek rekayasa"),
 ("Siegel, Neil - Engineering Project Management",
  "R3_TEXTBOOK-HANDBOOK/PROJECT-QUALITY", "Manajemen proyek rekayasa sistem"),
 ("Abdul Razzak Rumane - Quality Management in Const",
  "R3_TEXTBOOK-HANDBOOK/PROJECT-QUALITY", "Manajemen mutu konstruksi — ITP, inspeksi"),
 ("Quality Auditing in Construction Projects",
  "R3_TEXTBOOK-HANDBOOK/PROJECT-QUALITY", "Audit mutu — dipakai untuk gate G6/G7"),
 # ── laci baru: HVAC-BUILDING ─────────────────────────────────────
 ("Walter T. Grondzik, Alison G. Kwok - Mechanical and Electrical Equipment",
  "R3_TEXTBOOK-HANDBOOK/HVAC-BUILDING", "Peralatan mekanikal & elektrikal gedung — HVAC, penerangan, sanitasi"),
 # ── laci baru: SOFTWARE-DATA ─────────────────────────────────────
 ("Deep-learning.pdf",
  "R3_TEXTBOOK-HANDBOOK/SOFTWARE-DATA", "Dasar pembelajaran mendalam — analitik video, ASR"),
 # ── R4: dokumen produk yang salah masuk R3 ───────────────────────
 ("LiteAPI Document for NVR",
  "R4_OEM-TECHNICAL/VMS-NVR", "Dokumen API NVR — R4, bukan buku"),
 ("13_Western_Digital_Red_SA500",
  "R4_OEM-TECHNICAL/SERVER-STORAGE", "Ikhtisar cakram — R4"),
]

# TIDAK diserap, dan alasannya dicatat supaya keputusan ini dapat ditinjau ulang
DILEWATI = [
 ("AutoCAD Electrical 2026 (2 judul, 236 MB)",
  "Tutorial perangkat lunak, bukan rujukan rekayasa. Tidak memasok rumus, ambang, "
  "maupun metode uji. Bila kelak dibutuhkan, tempatnya laci perkakas — bukan laci sumber."),
 ("SL API_APAC.pdf",
  "Dokumen API layanan; belum jelas produknya. Tahan sampai diperiksa."),
 ("INVEST_RD_classguide_en-US.pdf",
  "Panduan kelas, bukan rujukan teknik."),
 ("Jay M. Shafritz - Introducing Public Administration",
  "Administrasi publik — di luar lingkup teknik."),
 ("38 dokumen kerja GSP (579 MB)",
  "Kajian Teknis Arsenal, Laporan Audit Log, Kajian Pemeliharaan IDS, Laporan Pelatihan, "
  "deck Geospatial & DEMS, Technical Report ADINT. **Ini keluaran GSP, bukan sumber rujukan.** "
  "Menaruhnya di 03_SOURCE-VAULT akan membuat pekerjaan sendiri terlihat seperti sandaran "
  "eksternal — kesalahan yang paling sulit diperbaiki kemudian. Lihat catatan di bawah."),
]


def hashfile(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for blok in iter(lambda: f.read(1 << 20), b""):
            h.update(blok)
    return h.hexdigest()


def main():
    ada = set()
    for r, d, bs in os.walk(VAULT):
        for b in bs:
            if b.lower().endswith(".pdf"):
                ada.add(hashfile(os.path.join(r, b)))

    rows = list(csv.DictReader(io.open(QUEUE, encoding="utf-8")))
    rencana, hilang, dup = [], [], []
    for potong, laci, catatan in DAFTAR:
        cocok = [r for r in rows if potong.lower() in r["nama"].lower()
                 and os.path.exists(r["jalur"])]
        if not cocok:
            hilang.append(potong)
            continue
        cocok.sort(key=lambda r: -float(r["mb"]))
        r = cocok[0]
        if hashfile(r["jalur"]) in ada:
            dup.append(r["nama"])
            continue
        rencana.append((laci, r["jalur"], r["nama"], float(r["mb"]), catatan))

    print("=" * 66)
    print("SERAP R3  —  %s" % ("SUNGGUHAN" if JALANKAN else "UJI COBA"))
    print("=" * 66)
    print("dalam daftar    :", len(DAFTAR))
    print("siap diserap    :", len(rencana), " (%.0f MB)" % sum(x[3] for x in rencana))
    if dup:
        print("sudah di vault  :", len(dup))
    if hilang:
        print("TIDAK DITEMUKAN :", len(hilang))
        for h in hilang:
            print("   ", h)
    print()
    laci_akhir = sorted(set(x[0] for x in rencana))
    for l in laci_akhir:
        print("  " + l)
        for x in rencana:
            if x[0] == l:
                print("      %6.1f MB  %s" % (x[3], x[2][:66]))
    print()
    print("SENGAJA DILEWATI:")
    for n, a in DILEWATI:
        print("   %s" % n)
        print("      %s" % a[:150])
    print()

    if not JALANKAN:
        print("UJI COBA — tidak ada berkas disalin.")
        print("Sungguhan:  python serap_r3.py --jalankan")
        return

    NL = chr(10)
    for laci, p, nama, mb, catatan in rencana:
        d = os.path.join(VAULT, laci)
        os.makedirs(d, exist_ok=True)
        shutil.copy2(p, os.path.join(d, nama))

    for laci in laci_akhir:
        d = os.path.join(VAULT, laci)
        bs = sorted(b for b in os.listdir(d) if b.lower().endswith(".pdf"))
        cat = {x[2]: x[4] for x in rencana}
        baris = NL.join("| `%s` | %.1f MB | %s |" % (
            b, os.path.getsize(os.path.join(d, b)) / 1048576.0, cat.get(b, "")) for b in bs)
        io.open(os.path.join(d, "_ISI.md"), "w", encoding="utf-8").write(
            u"# Isi laci — `%s`" % laci + NL * 2 +
            u"**%d berkas.**" % len(bs) + NL * 2 +
            u"> Buku rujukan **belum diresume**. Berstatus `INTAKE_ONLY` sampai resume dan" + NL +
            u"> kartu pengetahuannya dibuat — lihat `01_GOVERNANCE/SOURCE-UPDATE-PROCEDURE.md`." + NL * 2 +
            u"| Berkas | Ukuran | Dipakai untuk |" + NL + u"|---|---|---|" + NL + baris + NL)

    print("SELESAI. %d berkas diserap ke %d laci." % (len(rencana), len(laci_akhir)))


if __name__ == "__main__":
    main()
