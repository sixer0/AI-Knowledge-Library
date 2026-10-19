"""GSP-SDT snippet DOCX - blok identitas, kepala-kaki klasifikasi, nomor lembar per rezim,
tabel revisi. Pemilik: gsp-document-quality-standards/references/gsp-sdt/ (D-TA-7.4).
Carrier pemakai: gsp-report-format, gsp-word-report-deliverable. Sumber aturan:
SPEC-DOC-SYSTEM.md C-08/C-16/C-22/C-24/C-25. Jalankan langsung untuk contoh: exit 0.

Kepatuhan D17 (em-dash MUTLAK): pola SDT C-16 sumber tercetak `n <U+2014> mm` dirender
sebagai `n / mm` dan label provenans `[jenis <U+2014> sumber, hal]` sebagai
`[jenis / sumber, hal]` - preseden pola footer PDF keluarga GSP-SDT (HLM n / mm,
SPEC-DOC-SYSTEM.md R-5). Disengaja, bukan cacat.

Ketergantungan: python-docx (pip install python-docx).
"""

import sys
import tempfile, os

REZIM_PAGE = {  # C-16 pola nomor lembar per rezim
    "SDT":  lambda n, m: f"{n} / {m:02d}",
    "SDTP": lambda n, m: f"SHEET {n:02d} OF {m:02d}",
    "AD":   lambda n, m: f"LEMBAR {n} DARI {m}",
    "AU":   lambda n, m: f"HAL {n:02d} / {m:02d}",
    "PL":   lambda n, m: f"HLM {n} / {m:02d}",
    "CY":   lambda n, m: f"{n} / {m:02d}",
    "BIZ":  lambda n, m: f"{n} / {m:02d}",
}
PROFESIONAL = {"SDT", "PL", "CY", "BIZ"}   # C-25 bentuk strip; selain itu kisi 6x4


def add_identity_block(doc, meta):
    """Blok identitas C-25 di awal dokumen. meta: dict field -> nilai."""
    if meta.get("rezim") in PROFESIONAL:
        strip = (f"DOKUMEN {meta['dok_no']} | REGISTER {meta['register']} | "
                 f"REVISI {meta['revisi']} \u00b7 {meta['tanggal']} | STATUS {meta.get('status_dokumen', 'Berlaku')}")
        if meta.get("rezim") == "CY":
            strip = strip.rsplit("|", 1)[0] + "| INTEGRITAS: SHA-256 \u00b7 diisi saat terbit"
        doc.add_paragraph(strip)
        return
    pairs = [("DOK NO", "dok_no"), ("REVISI", "revisi"), ("REGISTER", "register"),
             ("TANGGAL", "tanggal"), ("KLASIFIKASI", "klasifikasi"), ("STATUS", "status_dokumen"),
             ("DISUSUN", "disusun"), ("KUSTODIAN", "kustodian"), ("DIPERIKSA", "diperiksa"),
             ("DISETUJUI", "disetujui"), ("LEMBAR", "lembar"),
             ("MATRA" if meta.get("rezim") in ("AD", "AU") else "BAHASA", "matra")]
    rows = [pairs[i:i + 2] for i in range(0, len(pairs), 2)]
    t = doc.add_table(rows=len(rows), cols=4)
    t.style = "Table Grid"
    for r, row in enumerate(rows):
        for c, (label, key) in enumerate(row):
            t.cell(r, c * 2).text = label
            t.cell(r, c * 2 + 1).text = str(meta.get(key, ""))


def add_header_footer(doc, kode, judul, klasifikasi, rezim="SDT", total_lembar=1):
    """C-22 kepala-kaki terkendali + C-16 nomor lembar pola rezim."""
    sec = doc.sections[-1]
    sec.header.paragraphs[0].text = f"{kode} \u00b7 {judul} \u00b7 {klasifikasi}"
    fn = REZIM_PAGE.get(rezim, REZIM_PAGE["SDT"])
    sec.footer.paragraphs[0].text = (f"PT GEMILANG SATRIA PERKASA | {klasifikasi} \u00b7 "
                                     f"Terkendali | {fn(1, total_lembar)}")


def add_revision_table(doc, rows):
    """C-24 riwayat revisi: baris terbaru di puncak; baris lama tidak diubah/dihapus.
    rows: list of (rev, tanggal, perubahan, oleh), urutan sudah dari baru ke lama."""
    t = doc.add_table(rows=1 + len(rows), cols=4)
    t.style = "Table Grid"
    for c, h in enumerate(["Rev", "Tanggal", "Perubahan", "Oleh"]):
        t.cell(0, c).text = h
    for r, row in enumerate(rows, start=1):
        for c, val in enumerate(row):
            t.cell(r, c).text = str(val)
    return t


def provenance_label(kind, sumber, hal=None):
    """C-18 label provenans satu angka: [jenis - sumber, hal] + simbol."""
    sym = {"terukur": "\u25a0", "diturunkan": "\u25c8", "pemasok": "\u25c7", "asumsi": "\u25b3"}
    loc = f"{sumber}, hal {hal}" if hal else sumber
    return f"[{kind} / {loc}]  {sym[kind]}"


def build_demo(out_path=None):
    from docx import Document
    doc = Document()
    meta = {"rezim": "AD", "dok_no": "GSP-SDTP-AD-001", "register": "028/GSP/STD/VIII/2026",
            "revisi": "A", "tanggal": "27 AGU 2026", "klasifikasi": "RAHASIA",
            "status_dokumen": "BERLAKU", "disusun": "Divisi Engineering",
            "kustodian": "ENG-01", "diperiksa": "Kepala Div. Engineering",
            "disetujui": "Direktur PT GSP", "lembar": "03 DARI 06", "matra": "Darat (AD)"}
    add_identity_block(doc, meta)
    add_header_footer(doc, meta["dok_no"], "SISTEM DOKUMEN TEKNIS MATRA DARAT",
                      meta["klasifikasi"], "AD", 6)
    doc.add_heading("5 Isi Teknis", level=1)
    doc.add_paragraph("Beban puncak 412 W " + provenance_label("terukur", "log PDU-03", 2))
    add_revision_table(doc, [("A", "27 AGU 2026", "Terbit pertama", "Divisi Engineering")])
    out = out_path or os.path.join(tempfile.gettempdir(), "gsp_sdt_demo.docx")
    doc.save(out)
    return out


if __name__ == "__main__":
    try:
        print("saved:", build_demo(sys.argv[1] if len(sys.argv) > 1 else None))
    except ImportError:
        print("python-docx tidak tersedia - pip install python-docx", file=sys.stderr)
        sys.exit(1)
