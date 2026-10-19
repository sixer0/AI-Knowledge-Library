#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""selftest_datumbind.py — gerbang eksekusi dua arah paket datum-house-style v2.0.0
(DHS-RB-01; preseden t_a21e89ab: kompilasi bukan gerbang, jalankan dan baca exit code).

Cara pakai: letakkan BERDAMPINGAN dengan datumbind.py + tokens.json lalu jalankan.
Hijau penuh hanya bila mesin menangkak cacat pada basal rusak DAN lulus pada basal benar.
Cetak CHECK n: PASS|FAIL per butir + VERDICT akhir; exit != 0 bila ada FAIL.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import datumbind as db
from datumbind import Register, Derivation, BindDefect, tokens_path

fails = []
def check(n, name, cond, detail=""):
    tag = "PASS" if cond else "FAIL"
    if not cond: fails.append(name)
    print(f"CHECK {n}: {tag} — {name}" + (f" | {detail}" if detail else ""))

# 1. resolver token lokal
try:
    tok = json.load(open(tokens_path(), encoding="utf-8"))
    ok = all(k in tok for k in ("colour", "type", "grid_mm", "rules_mm")) \
         and tok["colour"]["interior"]["ink700"] == "#2B3640" \
         and tok["grid_mm"]["text_column"] == 128
    check(1, "tokens_path() resolve + token kunci utuh", ok, tokens_path())
except Exception as ex:
    check(1, "tokens_path() resolve + token kunci utuh", False, repr(ex))

# 2. emit menolak besaran tanpa tanda asal
try:
    Register.emit(os.path.join(HERE, "_st_reg.json"),
                  {"nilai uji": (1000, 0, "Rp", None, None)})
    check(2, "emit menolak besaran tanpa tanda asal", False, "tidak raise")
except BindDefect:
    check(2, "emit menolak besaran tanpa tanda asal", True)

# 2b/2c FIX-DATUM-ENGINE (t_9b9494b6, DATUM-09 rev B): satuan wajib di emitter
try:
    Register.emit(os.path.join(HERE, "_st_reg_nounit.json"),
                  {"bobot uji": (15, 0, None, "DITURUNKAN", "st")})
    check("2b", "emit menolak besaran tanpa satuan", False, "tidak raise")
except BindDefect:
    check("2b", "emit menolak besaran tanpa satuan", True)
try:
    _g = Register.emit(os.path.join(HERE, "_st_reg_unit.json"),
                       {"bobot uji": (15, 0, "poin bobot", "DITURUNKAN", "st")})
    check("2c", "emit memancarkan satuan sesuai spec rev B",
          _g["bobot uji"]["unit"] == "poin bobot", str(_g["bobot uji"]))
except BindDefect as ex:
    check("2c", "emit memancarkan satuan sesuai spec rev B", False, str(ex)[:60])

# 3. Derivation: aritmetika cocok lolos, tidak cocok ditolak
N = Register(data={
    "nilai basis":    {"v": 1000000.0, "dec": 0, "unit": "Rp", "mark": "TERUKUR", "src": "st"},
    "nilai skenario": {"v": 750000.0,  "dec": 0, "unit": "Rp", "mark": "TERUKUR", "src": "st"},
    "ruang nilai":    {"v": 250000.0,  "dec": 0, "unit": "Rp", "mark": "DITURUNKAN", "src": "st"},
})
d = Derivation("D-ST", N); d.line("basis", "nilai basis"); d.line("skenario", "nilai skenario")
d.result("ruang", "nilai basis - nilai skenario", "ruang nilai"); d.closes("bila gagal, model ditinjau")
check(3, "Derivation aritmetika cocok lolos", d.build()[0] == "D-ST")
bad = Derivation("D-BAD", N)
try:
    bad.result("ruang", "nilai basis + nilai skenario", "ruang nilai")
    check(4, "Derivation aritmetika salah ditolak", False, "tidak raise")
except BindDefect:
    check(4, "Derivation aritmetika salah ditolak", True)

# 5-6. blok tanpa result()/tanpa closes() ditolak
t = Derivation("D-KOSONG", N); t.line("basis", "nilai basis")
try:
    t.build(); check(5, "blok tanpa result() ditolak", False)
except BindDefect: check(5, "blok tanpa result() ditolak", True)
t2 = Derivation("D-TUTUP", N); t2.result("ruang", "nilai basis - nilai skenario", "ruang nilai")
try:
    t2.build(); check(6, "blok tanpa closes() ditolak", False)
except BindDefect: check(6, "blok tanpa closes() ditolak", True)

# 7-9. audit_docx pada basal baik/jahat (perlu python-docx)
try:
    from docx import Document
    have_docx = True
except Exception:
    have_docx = False

if have_docx:
    def mkdoc(path, texts):
        doc = Document()
        for t_ in texts: doc.add_paragraph(t_)
        doc.save(path)
    good = os.path.join(HERE, "_st_good.docx"); evil = os.path.join(HERE, "_st_evil.docx")
    mkdoc(good, ["Nilai pekerjaan Rp 1.000.000 dan ruang Rp 250.000.",
                 "Skenario Rp 750.000 atas dasar 100 % verifikasi."])
    mkdoc(evil, ["Angka karangan 1.234.567 masuk tanpa izin.",
                 "Masih memuat 9.999.999 yang sudah ditarik model."])
    r1 = Register(data=N.d); stray = r1.audit_docx(good, allow=("100 %",), quiet=True)
    check(7, "audit_docx basal baik = nol stray", stray == [], str(stray))
    r2 = Register(data=N.d); hit = r2.audit_docx(evil, quiet=True)
    check(8, "audit_docx basal jahat = stray tertangkap", "1.234.567" in hit, str(hit))
    r3 = Register(data=N.d)
    ret = r3.audit_retired(evil, ["9.999.999"], quiet=True)
    check(9, "audit_retired menolak angka ditarik", ret == ["9.999.999"], str(ret))
    # limit E-12 terbukti: nilai dec=4 dilaporkan stray oleh desain
    r4 = Register(data={"rasio": {"v": 0.0201, "dec": 4, "unit": "kg/kg", "mark": "TERUKUR", "src": "st"}})
    e12 = r4.audit_text("rasio 0,0201 kg/kg", allow=())
    check(10, "limit E-12 terdokumentasi (dec=4 stray tanpa allow)", e12 == ["0,0201"], str(e12))
    ok_allow = r4.audit_text("rasio 0,0201 kg/kg", allow=("0,0201",)) == []
    check(11, "limit E-12 dapat diizinkan lewat allow", ok_allow)
else:
    print("CHECK 7-11: SKIP — python-docx tidak tersedia di interpreter ini")

for junk in ("_st_reg.json", "_st_reg_nounit.json", "_st_reg_unit.json",
             "_st_good.docx", "_st_evil.docx"):
    p = os.path.join(HERE, junk)
    if os.path.exists(p): os.remove(p)

print("VERDICT: " + ("PASS" if not fails else "FAIL — " + ", ".join(fails)))
sys.exit(0 if not fails else 1)
