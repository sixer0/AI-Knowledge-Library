#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_fixtures.py - generator fixture red-green untuk gerbang doc_gate_check.py.

Deterministik: menjalankan ulang skrip ini menghasilkan berkas dengan SHA-256 yang sama (langkah 3
blueprint VERIF-GATE-0904). Determinisme dicapai dengan menstabilkan timestamp entri zip ke 1980-01-01
dan mengurutkan nama entri, bukan dengan menolak perbedaan isi. Setiap cacat diberi id FX-* dan dicatat
di manifest fixture_expected.json berisi vonis yang HARUS keluar per fixture (D-TA-09).

Kelas cacat: F1 tabel (F1a baca, F1b aritmetika turunan, F1c duplikat kunci, F1d placeholder),
F2 hyperlink/rel (F2a ekstraksi, F2b keutuhan rel, F2c probe hidup), F3 entity-match salah-target.

Pemisahan dua bidang manifest (penjelasan untuk verifier, syarat C-02):
  - "defects"        = cacat yang WAJIB muncul sebagai temuan pemblokir (failures.csv). Jumlahnya
                       dibandingkan CHECK 10 dengan jumlah temuan skrip (MG-R1).
  - "expected_notes" = vonis yang menurut D-TA-04/D-02 sah menjadi CATATAN register (MATI, KOSONG),
                       bukan pemblokir. Diperiksa terhadap notes_register.csv lewat CHECK 10 supaya
                       kelas F2c tetap teruji arahnya tanpa melanggar semantik pemblokir.

Aturan baseline (D-TA-10): URL baseline hanya domain IANA stabil (example.com/org/net) supaya hijau
tidak berganti merah karena situs pihak ketiga mati. Fixture F2/F3 memang memanggil jaringan saat
diuji; URL mati memakai TLD .invalid (RFC 2606, dijamin tidak pernah resolve).

Pustaka: stdlib + openpyxl + python-docx. Jalankan:
  uv run --python 3.11 --with openpyxl --with python-docx python make_fixtures.py [--outdir DIR]
"""
import argparse
import datetime
import json
import os
import zipfile

import docx
import openpyxl
from openpyxl.worksheet.hyperlink import Hyperlink

EPOCH = (1980, 1, 1, 0, 0, 0)          # timestamp zip tetap -> regenerasi bit-identik
EPOCH_DT = datetime.datetime(1980, 1, 1, 0, 0, 0)
HERE = os.path.dirname(os.path.abspath(__file__))
DEAD = "https://situs-mati-uji.invalid/"           # RFC 2606: .invalid tidak pernah resolve
DEAD2 = "https://pintu-hilang-uji.invalid/halaman"
SPACED = "https://example.com /index.html"         # preseden ADINT LV8: rel ber-spasi ditolak Excel
WRONG1 = "https://www.python.org"                  # hidup, milik entitas lain
WRONG2 = "https://httpbin.org/html"                # hidup, tanpa satu pun sinyal entitas
OK_COM = "https://example.com"
OK_ORG = "https://example.org"
OK_NET = "https://example.net"


# ------------------------------------------------------------------ util determinisme
def stabilize(path):
    """Tulis ulang container zip: entri terurut nama, timestamp tetap, isi utuh."""
    with zipfile.ZipFile(path) as z:
        items = {n: z.read(n) for n in z.namelist()}
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as out:
        for n in sorted(items):
            zi = zipfile.ZipInfo(n, date_time=EPOCH)
            zi.compress_type = zipfile.ZIP_DEFLATED
            out.writestr(zi, items[n])


def _sheet(wb, name, header, rows):
    ws = wb["Sheet"] if wb.sheetnames == ["Sheet"] else wb.create_sheet()
    ws.title = name
    ws.append(header)
    for r in rows:
        ws.append(r)
    return ws


def _link_cells(ws, col, first_row, n):
    """Tempel objek hyperlink openpyxl pada sel yang sudah berisi teks URL."""
    for i in range(first_row, first_row + n):
        c = ws.cell(row=i, column=col)
        if c.value:
            c.hyperlink = Hyperlink(ref=c.coordinate, target=str(c.value))
            c.style = "Hyperlink"


def _save_xlsx(wb, path):
    wb.properties.created = EPOCH_DT
    wb.save(path)
    _pin_core_times(path)


def _pin_core_times(path):
    """openpyxl menimpa dcterms:modified dengan waktu simpan nyata -> kunci pasca-simpan."""
    with zipfile.ZipFile(path) as z:
        items = {n: z.read(n) for n in z.namelist()}
    cp = "docProps/core.xml"
    if cp in items:
        import re as _re
        t = items[cp].decode("utf-8")
        t = _re.sub(r">(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})Z<", ">1980-01-01T00:00:00Z<", t)
        items[cp] = t.encode("utf-8")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as out:
        for n in sorted(items):
            zi = zipfile.ZipInfo(n, date_time=EPOCH)
            zi.compress_type = zipfile.ZIP_DEFLATED
            out.writestr(zi, items[n])


# ------------------------------------------------------------------ XLSX
def xlsx_baseline(path):
    wb = openpyxl.Workbook()
    ws = _sheet(wb, "Data", ["No", "Exhibitor", "Category", "Qty", "Unit Price", "Total Price", "Website"], [
        [1, "Example Mining Corp", "Minerals", 4, 250, 1000, OK_COM],
        [2, "Example Cloud Systems", "Software", 3, 900, 2700, OK_ORG],
        [3, "Example Logistics Partners", "Freight", 5, 120, 600, OK_NET],
        ["Total", "", "", 12, None, 4300, ""],
    ])
    _link_cells(ws, 7, 2, 3)
    _save_xlsx(wb, path)


def xlsx_f1_defects(path):
    wb = openpyxl.Workbook()
    ws = _sheet(wb, "Data", ["No", "Exhibitor", "Visited", "Booths", "Share %", "Website"], [
        [1, "Example Mining Corp", 60, 4, 60.0, OK_COM],
        [2, "Example Cloud Systems", 40, 2, 40.0, OK_ORG],
        [2, "Example Cloud Systems", 40, 2, 40.0, OK_ORG],            # duplikat kunci No
        [3, "Example Logistics Partners", None, 3, "[isi]", OK_NET],   # sentinel + slot template
        [4, "Example Robotics Institute", "#REF!", 1, 20.0, DEAD],      # sentinel error Excel
        ["Total", "", 100, 12, 120.0, ""],                              # Visited total salah (harusnya 140); Booths benar
    ])
    _link_cells(ws, 6, 2, 5)
    _save_xlsx(wb, path)


def xlsx_f2_defects(path):
    wb = openpyxl.Workbook()
    ws = _sheet(wb, "Data", ["No", "Exhibitor", "Website"], [
        [1, "Example Mining Corp", OK_COM],
        [2, "Example Cloud Systems", DEAD],
        [3, "Example Logistics Partners", DEAD2],
    ])
    _link_cells(ws, 3, 2, 3)
    _save_xlsx(wb, path)
    _inject_broken_sheet_rels(path)


def _inject_broken_sheet_rels(path):
    """Sisipkan dua cacat struktur rel pasca-simpan: target ber-spasi + rId dangling."""
    sheet_part, rels_part = "xl/worksheets/sheet1.xml", "xl/worksheets/_rels/sheet1.xml.rels"
    with zipfile.ZipFile(path) as z:
        items = {n: z.read(n) for n in z.namelist()}
    sx = items[sheet_part].decode("utf-8")
    RNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    tags = ('<hyperlink xmlns:r="%s" ref="A10" r:id="rIdSpasi1"/>'
            '<hyperlink xmlns:r="%s" ref="A11" r:id="rIdGantung1"/>' % (RNS, RNS))
    if "</hyperlinks>" in sx:                      # openpyxl sudah menulis blok hyperlinks -> sisip
        sx = sx.replace("</hyperlinks>", tags + "</hyperlinks>", 1)
    elif "<extLst>" in sx:
        sx = sx.replace("<extLst>", "<hyperlinks>" + tags + "</hyperlinks><extLst>", 1)
    else:
        sx = sx.replace("</worksheet>", "<hyperlinks>" + tags + "</hyperlinks></worksheet>", 1)
    items[sheet_part] = sx.encode("utf-8")
    new_rel = ('<Relationship Id="rIdSpasi1" Type="http://schemas.openxmlformats.org/officeDocument/'
               '2006/relationships/hyperlink" Target="%s" TargetMode="External"/>' % SPACED)
    if rels_part in items:
        rx = items[rels_part].decode("utf-8")
        assert rx.rstrip().endswith("</Relationships>"), "format part rels tak dikenali"
        items[rels_part] = rx.rstrip().replace("</Relationships>", new_rel + "</Relationships>").encode("utf-8")
    else:
        items[rels_part] = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                            + new_rel + "</Relationships>").encode("utf-8")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as out:
        for n in sorted(items):
            zi = zipfile.ZipInfo(n, date_time=EPOCH)
            zi.compress_type = zipfile.ZIP_DEFLATED
            out.writestr(zi, items[n])


def xlsx_f3_defects(path):
    wb = openpyxl.Workbook()
    ws = _sheet(wb, "Data", ["No", "Exhibitor", "Website"], [
        [1, "Example Mining Corp", OK_COM],                 # sah: token nama cocok host + judul
        [2, "PT Telkom Indonesia", WRONG1],                 # salah-target: hidup tapi tak relevan
        [3, "Example Cloud Systems", OK_ORG],               # sah
        [4, "Nimbus Freight Bhd", WRONG2],                  # salah-target: hidup tanpa sinyal
    ])
    _link_cells(ws, 3, 2, 4)
    _save_xlsx(wb, path)


# ------------------------------------------------------------------ DOCX
def _cell_hyperlink(cell, text, url):
    """python-docx tidak punya API pembuatan hyperlink; tulis rel eksternal + w:hyperlink manual."""
    from docx.oxml.ns import qn
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    cell.text = ""                      # hindari teks ganda: sel diisi oleh objek hyperlink saja
    part = cell.part
    rid = part.relate_to(url, RT.HYPERLINK, is_external=True)
    hl = part._element.makeelement(qn("w:hyperlink"), {qn("r:id"): rid})
    run = part._element.makeelement(qn("w:r"), {})
    rpr = part._element.makeelement(qn("w:rPr"), {})
    rpr.append(part._element.makeelement(qn("w:rStyle"), {qn("w:val"): "Hyperlink"}))
    run.append(rpr)
    t = part._element.makeelement(qn("w:t"), {})
    t.text = text
    run.append(t)
    hl.append(run)
    cell.paragraphs[0]._p.append(hl)
    return rid


def _para_hyperlink(d, text, url):
    from docx.oxml.ns import qn
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    rid = d.part.relate_to(url, RT.HYPERLINK, is_external=True)
    hl = d.part._element.makeelement(qn("w:hyperlink"), {qn("r:id"): rid})
    run = d.part._element.makeelement(qn("w:r"), {})
    t = d.part._element.makeelement(qn("w:t"), {})
    t.text = text
    run.append(t)
    hl.append(run)
    d.add_paragraph()._p.append(hl)
    return rid


def _table(d, header, rows):
    t = d.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    for i, h in enumerate(header):
        t.rows[0].cells[i].text = h
    for r in rows:
        cells = t.add_row().cells
        for i, v in enumerate(r):
            cells[i].text = "" if v is None else str(v)
    return t


def _save_docx(d, path):
    cp = d.core_properties
    cp.created = EPOCH_DT
    cp.modified = EPOCH_DT
    cp.author = "GSP fixture generator"
    cp.last_modified_by = "GSP fixture generator"
    cp.revision = 1
    d.save(path)
    stabilize(path)


def docx_baseline(path):
    d = docx.Document()
    d.add_heading("Laporan Baseline Gerbang Dokumen", level=1)
    d.add_paragraph("Dokumen bersih untuk uji hijau: aritmetika tabel cocok dan tautan milik entitasnya.")
    t = _table(d, ["No", "Exhibitor", "Qty", "Unit Price", "Total Price", "Website"], [
        [1, "Example Mining Corp", 4, 250, 1000, OK_COM],
        [2, "Example Cloud Systems", 3, 900, 2700, OK_ORG],
        ["Total", "", 7, None, 3700, ""],
    ])
    _cell_hyperlink(t.rows[1].cells[5], OK_COM, OK_COM)
    _cell_hyperlink(t.rows[2].cells[5], OK_ORG, OK_ORG)
    _save_docx(d, path)


def docx_f1_defects(path):
    d = docx.Document()
    d.add_heading("Fixture Cacat Tabel Word", level=1)
    _table(d, ["No", "Exhibitor", "Visited", "Booths", "Share %"], [
        [1, "Example Mining Corp", 60, 4, 60.0],
        [2, "Example Cloud Systems", 40, 2, 40.0],
        [2, "Example Cloud Systems", 40, 2, 40.0],                    # duplikat kunci
        [3, "Example Logistics Partners", None, 3, "[isi]"],           # sentinel + slot template
        ["Total", "", 100, 11, 120.0],                                # Visited total salah (harusnya 140)
    ])
    d.add_paragraph("[wajib diisi] ringkasan temuan belum tersedia.")
    _save_docx(d, path)


def docx_f2_defects(path):
    d = docx.Document()
    d.add_heading("Fixture Cacat Tautan Word", level=1)
    d.add_paragraph("Tautan aktif sah:")
    _para_hyperlink(d, "Example Commercial", OK_COM)
    d.add_paragraph("Tautan mati (harus terdeteksi dan tercatat di register):")
    _para_hyperlink(d, "Situs mati", DEAD)
    _para_hyperlink(d, "Halaman hilang", DEAD2)
    d.add_paragraph("Daftar pustaka menyalurkan URL polos: " + DEAD + " dan " + OK_NET)
    _save_docx(d, path)
    _inject_spaced_docx_rel(path)


def _inject_spaced_docx_rel(path):
    """Ubah satu rel eksternal docx menjadi target ber-spasi (cacat struktur nyata)."""
    rp = "word/_rels/document.xml.rels"
    with zipfile.ZipFile(path) as z:
        items = {n: z.read(n) for n in z.namelist()}
    rx = items[rp].decode("utf-8")
    assert DEAD in rx, "rel hyperlink mati tidak ditemukan; generator berubah bentuk"
    items[rp] = rx.replace('Target="%s"' % DEAD, 'Target="%s"' % SPACED, 1).encode("utf-8")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as out:
        for n in sorted(items):
            zi = zipfile.ZipInfo(n, date_time=EPOCH)
            zi.compress_type = zipfile.ZIP_DEFLATED
            out.writestr(zi, items[n])


def docx_f3_defects(path):
    d = docx.Document()
    d.add_heading("Fixture Salah-Target Word", level=1)
    t = _table(d, ["No", "Exhibitor", "Website"], [
        [1, "Example Mining Corp", OK_COM],
        [2, "PT Telkom Indonesia", WRONG1],
        [3, "Example Cloud Systems", OK_ORG],
        [4, "Nimbus Freight Bhd", WRONG2],
    ])
    # bukti utama C-02: objek hyperlink docx (bukan hanya URL polos) menuju situs entitas lain
    _cell_hyperlink(t.rows[4].cells[2], WRONG2, WRONG2)
    _save_docx(d, path)


# ------------------------------------------------------------------ manifest
MANIFEST = {
    "_skor": "Vonis di bawah adalah KONTRAK. doc_gate_check.py --mode fixture --expect berkas ini WAJIB "
             "menghasilkan verdict dan set CHECK yang sama persis; jumlah temuan pemblokir WAJIB sama "
             "dengan jumlah butir defects (MG-R1); setiap butir expected_notes WAJIB ditemukan pada "
             "notes_register.csv dengan jumlah minimal yang disebut.",
    "_cara_jalankan": "uv run --python 3.11 --with openpyxl --with python-docx python doc_gate_check.py "
                      "--target <fixture> --outdir <out> --mode fixture --expect fixture_expected.json "
                      "--name-col Exhibitor --url-col Website --key-col No",
    "_koreksi_t_b0cf1dc7": "Lokasi F3 xlsx dipindah ke kolom URL (C3/C5); rIdHyperlinkMati fiktif -> rId10 nyata; notasi alamat docx diseragamkan tabelN!rR/cC; F1d sel tabel beralamat sel (bukan indeks paragraf global) setelah pembacaan docx memetakan paragraf dalam tabel ke sel.",
    "_penamaan": "Kartu VGV-C1 menyebut fixture_cacat/fixture_bersih di direktori tests/. Kontrak tunggal "
                 "D-TA-08 (dibekukan SKILL-DECISION C-03) memakai jalur scripts/fixtures/document-gate/ dan "
                 "nama per-kelas di bawah, karena tester/countersign menyusun perintah dari D-TA-08. "
                 "Pemetaan: fixture_bersih.xlsx = xlsx_baseline.xlsx; fixture_cacat.xlsx = gabungan "
                 "xlsx_f1/f2/f3_defects.xlsx; fixture_bersih.docx = docx_baseline.docx; fixture_cacat.docx = "
                 "gabungan docx_f1/f2/f3_defects.docx. Pemecahan per kelas disengaja: satu berkas cacat "
                 "mencampur kelas membuat CHECK 10 tidak bisa membuktikan SET CHECK yang benar.",
    "fixtures": [
        {"file": "xlsx_baseline.xlsx", "expected_verdict": "PASS", "expected_failed_checks": [],
         "defects": [], "expected_notes": []},
        {"file": "docx_baseline.docx", "expected_verdict": "PASS", "expected_failed_checks": [],
         "defects": [], "expected_notes": []},
        {"file": "xlsx_f1_defects.xlsx", "expected_verdict": "FAIL", "expected_failed_checks": [2, 3, 4],
         "defects": [
            {"id": "FX-F1B-01", "class": "F1b", "location": "Data!E2", "desc": "Share % 60.0 tidak cocok 60/4=1500% maupun 4/60=6.67%"},
            {"id": "FX-F1B-02", "class": "F1b", "location": "Data!E3", "desc": "Share % 40.0 tidak cocok 40/2=2000% maupun 2/40=5%"},
            {"id": "FX-F1B-03", "class": "F1b", "location": "Data!E4", "desc": "Share % baris duplikat 40.0 tidak cocok 40/2 maupun 2/40"},
            {"id": "FX-F1B-04", "class": "F1b", "location": "Data!C7", "desc": "baris Total kolom Visited=100 padahal jumlah butir di atasnya=140"},
            {"id": "FX-F1C-01", "class": "F1c", "location": "Data!A3, Data!A4", "desc": "kunci No=2 muncul dua kali"},
            {"id": "FX-F1D-01", "class": "F1d", "location": "Data!E5", "desc": "slot template '[isi]' dalam sel"},
            {"id": "FX-F1D-02", "class": "F1d", "location": "Data!C6", "desc": "sentinel error Excel #REF!"},
         ],
         "expected_notes": [{"kind": "MATI", "min_count": 1, "why": "URL .invalid wajib divonis MATI dan masuk register, bukan pemblokir (D-02)"}]},
        {"file": "xlsx_f2_defects.xlsx", "expected_verdict": "FAIL", "expected_failed_checks": [6],
         "defects": [
            {"id": "FX-F2B-01", "class": "F2b", "location": "xl/worksheets/_rels/sheet1.xml.rels#rIdSpasi1", "desc": "Target hyperlink memuat spasi (preseden ADINT LV8: Excel menolak berkas)"},
            {"id": "FX-F2B-02", "class": "F2b", "location": "xl/worksheets/sheet1.xml#rIdGantung1", "desc": "rId dirujuk sel tapi tidak ada di part rels (dangling)"},
         ],
         "expected_notes": [{"kind": "MATI", "min_count": 2, "why": "dua URL .invalid harus tercatat MATI"}]},
        {"file": "xlsx_f3_defects.xlsx", "expected_verdict": "FAIL", "expected_failed_checks": [8],
         "defects": [
            {"id": "FX-F3-01", "class": "F3", "location": "Data!C3|PT Telkom Indonesia", "desc": "https://www.python.org hidup tapi milik entitas lain"},
            {"id": "FX-F3-02", "class": "F3", "location": "Data!C5|Nimbus Freight Bhd", "desc": "https://httpbin.org/html hidup tanpa satu pun sinyal entitas"},
         ],
         "expected_notes": []},
        {"file": "docx_f1_defects.docx", "expected_verdict": "FAIL", "expected_failed_checks": [2, 3, 4],
         "defects": [
            {"id": "FX-F1B-05", "class": "F1b", "location": "docx:tabel1!r2/c5", "desc": "Share % 60.0 tidak cocok 60/4 maupun 4/60"},
            {"id": "FX-F1B-06", "class": "F1b", "location": "docx:tabel1!r3/c5", "desc": "Share % 40.0 tidak cocok 40/2 maupun 2/40"},
            {"id": "FX-F1B-07", "class": "F1b", "location": "docx:tabel1!r4/c5", "desc": "Share % baris duplikat 40.0 tidak cocok 40/2 maupun 2/40"},
            {"id": "FX-F1B-08", "class": "F1b", "location": "docx:tabel1!r6/c3", "desc": "baris Total kolom Visited=100 padahal jumlah butir=140"},
            {"id": "FX-F1C-02", "class": "F1c", "location": "docx:tabel1!r3/c1, docx:tabel1!r4/c1", "desc": "kunci No=2 muncul dua kali"},
            {"id": "FX-F1D-03", "class": "F1d", "location": "docx:tabel1!r5/c5", "desc": "slot template '[isi]' dalam sel tabel"},
            {"id": "FX-F1D-04", "class": "F1d", "location": "word/document.xml#paragraf", "desc": "slot template '[wajib diisi]' dalam paragraf"},
         ],
         "expected_notes": []},
        {"file": "docx_f2_defects.docx", "expected_verdict": "FAIL", "expected_failed_checks": [6],
         "defects": [
            {"id": "FX-F2B-03", "class": "F2b", "location": "word/_rels/document.xml.rels#rId10", "desc": "rel eksternal docx ber-target mengandung spasi (cacat struktur, pemblokir)"},
         ],
         "expected_notes": [
            {"kind": "MATI", "min_count": 2, "why": "dua jalur URL mati (objek hyperlink + URL polos teks) wajib tercatat di register"},
            {"kind": "ENTITY-CONTEXT", "min_count": 1, "why": "URL tanpa baris bernama wajib dilaporkan sebagai keterbatasan konteks, bukan lulus diam-diam"},
         ]},
        {"file": "docx_f3_defects.docx", "expected_verdict": "FAIL", "expected_failed_checks": [8],
         "defects": [
            {"id": "FX-F3-03", "class": "F3", "location": "docx:tabel1!r3/c3|PT Telkom Indonesia", "desc": "https://www.python.org dalam sel tabel salah-target"},
            {"id": "FX-F3-04", "class": "F3", "location": "docx:tabel1!r5/c3|Nimbus Freight Bhd", "desc": "https://httpbin.org/html salah-target; URL yang sama juga ada sebagai objek w:hyperlink (bukti utama C-02)"},
         ],
         "expected_notes": []},
    ],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=os.path.join(HERE, "fixtures", "document-gate"))
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    jobs = [
        ("xlsx_baseline.xlsx", xlsx_baseline), ("xlsx_f1_defects.xlsx", xlsx_f1_defects),
        ("xlsx_f2_defects.xlsx", xlsx_f2_defects), ("xlsx_f3_defects.xlsx", xlsx_f3_defects),
        ("docx_baseline.docx", docx_baseline), ("docx_f1_defects.docx", docx_f1_defects),
        ("docx_f2_defects.docx", docx_f2_defects), ("docx_f3_defects.docx", docx_f3_defects),
    ]
    for name, fn in jobs:
        p = os.path.join(a.outdir, name)
        if os.path.exists(p):
            os.remove(p)
        fn(p)
        print("buat %-24s %8d B" % (name, os.path.getsize(p)))
    mp = os.path.join(a.outdir, "fixture_expected.json")
    with open(mp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(MANIFEST, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print("buat %-24s %8d B" % ("fixture_expected.json", os.path.getsize(mp)))
    nd = sum(len(x["defects"]) for x in MANIFEST["fixtures"])
    nn = sum(len(x["expected_notes"]) for x in MANIFEST["fixtures"])
    print("fixture=%d cacat_pemblokir=%d harapan_catatan=%d" % (len(MANIFEST["fixtures"]), nd, nn))


if __name__ == "__main__":
    main()
