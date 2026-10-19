# -*- coding: utf-8 -*-
"""selftest_chip_para.py — gerbang dua arah lapis baca chip rail (chip_texts_para).

v2.4.0 (CTXWIN-FOLLOWUP-1 t_be1b447e, putusan manager t_618c93d4): preseden byte nyata
uji A/B t_fcdd32ac — dengan hAnchor="margin" aktif Word memecah run chip terpanjang
melewati lebar frame saat round-trip; sensor teks chip LEVEL-RUN positif-palsu, level
PARAGRAF bersih. Helper chip_texts_para() adalah lapis baca kanonis; selftest ini
membuktikan dua arah:
  ARAH HIJAU : byte utuh dan byte TERBELAH-DUA-RUN (repaginasi tertanam) sama-sama
               lolos banding manifest lewat helper; sensor per-run tandingan WAJIB
               jatuh di byte terbelah (kelas cacat nyata, bukan siluman).
  ARAH MERAH : kehilangan konten NYATA (chip dihapus) wajib terdeteksi helper sebagai
               hilang (helper tidak buta); input rusak wajib TypeError.

Cara pakai: letakkan BERDAMPINGAN dengan datum_docx.py + tokens.json lalu:
    uv run --python 3.11 --no-project --with python-docx python selftest_chip_para.py
Cetak CHECK n: PASS|FAIL per butir + baris VERDICT; exit != 0 bila ada FAIL.
"""
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import datum_docx as DD

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def q(t):
    return "{%s}%s" % (W, t)


def read_docxml(path):
    with zipfile.ZipFile(path) as z:
        return z.read("word/document.xml")


def run_layer_texts(docxml):
    """Sensor tandingan lapis RUN (pola builder lama): teks per w:r, BUKAN per paragraf."""
    from xml.etree import ElementTree as ET
    root = ET.fromstring(docxml)
    out = []
    for p in root.iter(q("p")):
        pPr = p.find(q("pPr"))
        if pPr is None or pPr.find(q("framePr")) is None:
            continue
        for r in p.iter(q("r")):
            tt = "".join(x.text or "" for x in r.findall(q("t")))
            if tt.strip():
                out.append(tt.strip())
    return out


def split_one_run(docxml, needle):
    """Tanam repaginasi Word: belah SATU w:t yang memuat `needle` jadi dua w:r."""
    from xml.etree import ElementTree as ET
    ET.register_namespace("w", W)
    root = ET.fromstring(docxml)
    parent = {c: p for p in root.iter() for c in p}
    n_split = 0
    for t in root.iter(q("t")):
        if t.text and needle in t.text and len(t.text) > 20 and n_split == 0:
            cut = len(t.text) // 2
            head, tail = t.text[:cut], t.text[cut:]
            run = parent[t]
            para = parent[run]
            idx = list(para).index(run)
            t.text = head
            run2 = ET.fromstring(ET.tostring(run))
            for tt in run2.iter(q("t")):
                tt.text = tail
            para.insert(idx + 1, run2)
            n_split = 1
    assert n_split == 1, "tanaman split gagal: needle tidak ditemukan/terlalu pendek"
    return ET.tostring(root, xml_declaration=True, encoding="UTF-8", method="xml")


def drop_chip(docxml, needle):
    """Cacat nyata: hapus seluruh paragraf chip yang memuat `needle`."""
    from xml.etree import ElementTree as ET
    ET.register_namespace("w", W)
    root = ET.fromstring(docxml)
    body = root.find(q("body"))
    n_drop = 0
    for p in list(body.iter(q("p"))):
        pPr = p.find(q("pPr"))
        if pPr is None or pPr.find(q("framePr")) is None:
            continue
        joined = "".join(x.text or "" for x in p.iter(q("t")))
        if needle in joined:
            body.remove(p)
            n_drop += 1
            break
    assert n_drop == 1, "penghapusan chip gagal: needle tidak ditemukan"
    return ET.tostring(root, xml_declaration=True, encoding="UTF-8", method="xml")


fails = []


def check(n, cond, label, detail=""):
    status = "PASS" if cond else "FAIL"
    if not cond:
        fails.append(n)
    print("CHECK %s: %s — %s%s" % (n, status, label, (" | " + detail) if detail else ""))


# ---------- bangun dokumen basal dengan 3 chip rail ----------
CHIPS = [
    "[R - ADINT-LIBRARY-INDEX-MASTER-V1.MD BAGIAN 8]",  # 47 char: kandidat split nyata
    "[R - SPM 2019 HAL 12]",
    "[R - OEM DATASHEET REV C HAL 4]",
]
doc = DD.DatumDocx("Uji chip rail", "TST-CHIP-PARA", "A")
doc.para("Paragraf prosa uji tanpa provenans memakai lebar penuh.")
host = doc.para("Paragraf berprovenans: angka uji 42,5 mm.[R - SPM 2019 HAL 12]")
doc.rail_host(host)
for c in CHIPS:
    doc.rail_chip(c)
out_path = os.path.join(HERE, "selftest-chip-para.docx")
doc.save(out_path)
basal = read_docxml(out_path)

manifest_up = {c.upper() for c in CHIPS}

# ---------- ARAH HIJAU ----------
# H1: basal — helper mengembalikan semua chip, banding manifest bersih.
got = DD.chip_texts_para(out_path)
lost = sorted(t for t in manifest_up if t not in {g.upper() for g in got})
check("H1", len(got) == len(CHIPS) and not lost,
      "basal: helper level-paragraf == manifest", "n=%d lost=%d" % (len(got), len(lost)))

# H2: byte terbelah-dua-run (repaginasi tertanam) — helper TETAP bersih.
split = split_one_run(basal, "ADINT-LIBRARY-INDEX-MASTER-V1.MD")
got2 = DD.chip_texts_para(split)
lost2 = sorted(t for t in manifest_up if t not in {g.upper() for g in got2})
n_runs = len(run_layer_texts(split))
check("H2", not lost2 and len(got2) == len(CHIPS),
      "pasca-split: helper level-paragraf tetap == manifest (konten kekal)",
      "lost=%d run-layer-n=%d" % (len(lost2), n_runs))

# H3: sensor tandingan per-run WAJIB positif-palsu di byte yang sama (kelas nyata).
runs3 = run_layer_texts(split)
lost3 = sorted(t for t in manifest_up if t not in {r.upper() for r in runs3})
check("H3", len(lost3) == 1,
      "tandingan per-run jatuh tepat 1 di byte terbelah (kelas cacat terkonfirmasi)",
      "hilang=%s" % [t[:40] for t in lost3])

# ---------- ARAH MERAH ----------
# M1: kehilangan konten nyata — helper wajib melaporkan hilang (bukan buta).
dropped = drop_chip(basal, "SPM 2019")
got4 = DD.chip_texts_para(dropped)
lost4 = sorted(t for t in manifest_up if t not in {g.upper() for g in got4})
check("M1", len(lost4) == 1 and "SPM" in lost4[0],
      "cacat nyata: chip dihapus -> helper laporkan hilang=1",
      "hilang=%s" % [t[:40] for t in lost4])

# M2: input rusak -> TypeError (kontrak API).
try:
    DD.chip_texts_para(object())
    check("M2", False, "input non-XML -> TypeError")
except TypeError:
    check("M2", True, "input non-XML -> TypeError")
except Exception as e:  # noqa: BLE001
    check("M2", False, "input non-XML -> TypeError", "dapat %r" % e)

# M3: jalur input bytes XML langsung == jalur path .docx (konsistensi antar-modus).
same = DD.chip_texts_para(basal) == DD.chip_texts_para(out_path)
check("M3", same, "modus bytes XML == modus path .docx")

try:
    os.remove(out_path)
except OSError:
    pass

print("VERDICT: " + ("PASS" if not fails else "FAIL %s" % fails))
sys.exit(1 if fails else 0)
