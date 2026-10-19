#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GSP-SDT snippet XLSX - konvensi workbook subset SPEC-DOC §3.2 (keputusan D-TA-5/D14:
konvensi spreadsheet PENUH di sini, engine productivity/xlsx READ-ONLY). Pemilik:
gsp-document-quality-standards/references/gsp-sdt/; carrier pemakai: excel-master.
Aturan: sheet identitas = blok identitas (sheet pertama); kolom `Provenans` wajib pada kolom
nilai; klasifikasi di sel kepala setiap sheet cetak; kunci `REQ-Kx-nnn`/`LI-nnn`;
sheet riwayat revisi tersendiri (baris lama tak diubah). Jalankan langsung: exit 0 + contoh.

Ketergantungan: openpyxl (pip install openpyxl).
"""
import sys
import tempfile, os

IDENTITAS_KEYS = ["DOK NO", "REGISTER", "KLASIFIKASI", "REVISI", "STATUS",
                  "TANGGAL", "DISUSUN", "KELAS", "BOBOT"]
PROVENANS_VALID = {"terukur", "diturunkan", "pemasok", "asumsi"}


def sheet_identitas(wb, meta):
    """Sheet pertama = blok identitas (C-25 analog; subset §3.2)."""
    ws = wb.active if wb.active.max_row == 1 and wb.active.title == "Sheet" else wb.create_sheet()
    ws.title = "00 Identitas"
    ws["A1"] = f"KLASIFIKASI: {meta.get('KLASIFIKASI', 'TERBATAS')}"  # kepala cetak (C-08/C-22)
    r = 3
    for k in IDENTITAS_KEYS:
        if k in meta:
            ws.cell(row=r, column=1, value=k)
            ws.cell(row=r, column=2, value=str(meta[k]))
            r += 1
    return ws


def sheet_register(wb, judul, header, rows):
    """Sheet register/line-item: kolom Provenans wajib; kunci REQ/LI kolom pertama."""
    ws = wb.create_sheet(judul)
    ws["A1"] = f"[{judul}] \u00b7 klasifikasi mengikuti identitas \u00b7 Terkendali"
    hdr = ["ID"] + header + ["Provenans", "Metode A/D/I/T"]
    ws.append([]); ws.append(hdr)
    for row in rows:
        ws.append(row)
    return ws


def validate_rows(rows, id_col=0, prov_col=-2):
    """Deterministik: ID unik berpola REQ-Kx-nnn/LI-nnn/BB-nnn/FND-Kx-nnn; provenans valid."""
    import re
    pola = re.compile(r"^(REQ-K\d-\d{3}|LI-\d{3}|BB-\d{3}|FND-K\d-\d{3})$")
    errs, ids = [], set()
    for i, row in enumerate(rows, start=2):
        rid = str(row[id_col])
        if not pola.match(rid):
            errs.append(f"baris {i}: ID '{rid}' bukan REQ-Kx-nnn/LI-nnn/BB-nnn/FND-Kx-nnn")
        if rid in ids:
            errs.append(f"baris {i}: ID duplikat '{rid}'")
        ids.add(rid)
        prov = str(row[prov_col]).split()[0].lower() if row[prov_col] else ""
        if prov not in PROVENANS_VALID:
            errs.append(f"baris {i}: provenans '{row[prov_col]}' wajib salah satu {sorted(PROVENANS_VALID)}")
    return errs


def sheet_revisi(wb, rows):
    """Riwayat revisi (C-24): baris terbaru di puncak; JANGAN mengubah baris lama."""
    ws = wb.create_sheet("99 Revisi")
    ws.append(["Rev", "Tanggal", "Perubahan", "Oleh"])
    for row in rows:
        ws.append(list(row))
    return ws


def build_demo(out_path=None):
    from openpyxl import Workbook
    wb = Workbook()
    sheet_identitas(wb, {"DOK NO": "GSP-SDT-BIZ-001", "REGISTER": "033/GSP/STD/VIII/2026",
                         "KLASIFIKASI": "TERBATAS", "REVISI": "A", "STATUS": "Berlaku",
                         "TANGGAL": "27 AGU 2026", "DISUSUN": "Divisi Engineering",
                         "KELAS": "K7", "BOBOT": "6"})
    rows = [["LI-014", "Switch L3 48-port", 12, 18500000, "pemasok katalog vendor X rev 2 hal 7", "I"],
            ["LI-015", "Patch panel RJ45", 24, 145000, "terukur survei lokasi 2026-08-20", "I"]]
    errs = validate_rows(rows)
    if errs:
        print("VALIDATE FAIL:\n" + "\n".join(errs), file=sys.stderr)
        sys.exit(1)
    sheet_register(wb, "01 BOQ", ["Item", "Qty", "Harga (Rp)"], rows)
    sheet_revisi(wb, [("A", "27 AGU 2026", "Terbit pertama", "Divisi Engineering")])
    out = out_path or os.path.join(tempfile.gettempdir(), "gsp_sdt_demo.xlsx")
    wb.save(out)
    return out


if __name__ == "__main__":
    try:
        print("saved:", build_demo(sys.argv[1] if len(sys.argv) > 1 else None))
    except ImportError:
        print("openpyxl tidak tersedia - pip install openpyxl", file=sys.stderr)
        sys.exit(1)
