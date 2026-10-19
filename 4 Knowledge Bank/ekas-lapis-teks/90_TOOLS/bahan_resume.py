# -*- coding: utf-8 -*-
"""
BAHAN RESUME — menarik bahan mentah tiap buku INTAKE_ONLY supaya resumenya
disusun dari bukunya, bukan dari ingatan.

Untuk tiap buku: jumlah halaman, ada/tidak lapis teks, daftar isi tingkat atas,
dan letak halaman kata kunci teknis (rumus, tabel, ambang).

Jalankan:  python bahan_resume.py [REF-XXX-000 ...]
           tanpa argumen = seluruh INTAKE_ONLY
"""
import io, os, re, sys, csv, json

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import fitz

EKAS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(EKAS, "02_REGISTERS", "MASTER-REFERENCE-REGISTER.csv")

# kata yang menandai halaman berisi angka yang dapat dipakai
KUNCI = [
    r"\bformula\b", r"\bequation\b", r"\bEq\.\s*\(", r"\btable\s+\d", r"\bfigure\s+\d",
    r"\bminimum\b", r"\bmaximum\b", r"\ballowable\b", r"\brequired\b", r"\bfactor\b",
    r"\bcoefficient\b", r"\bshall\s+not\s+exceed\b", r"\btolerance\b", r"\bcriteria\b",
    r"\bsafety\s+factor\b", r"\bload\s+factor\b", r"\bexample\s+\d", r"\bstandard\b",
]


def ringkas(p, maks_toc=40):
    d = fitz.open(p)
    n = d.page_count
    toc = d.get_toc()
    # cuplik teks 8 halaman tersebar untuk menguji lapis teks
    cuplik = [d[i].get_text() for i in range(0, n, max(1, n // 8))][:8]
    bertext = sum(1 for t in cuplik if len(t.strip()) > 80)

    # cari halaman berkata kunci — hanya 1/3 pertama & tengah supaya cepat
    hit = {}
    langkah = max(1, n // 260)
    for i in range(0, n, langkah):
        t = d[i].get_text()
        if not t:
            continue
        skor = sum(len(re.findall(k, t, re.I)) for k in KUNCI)
        if skor >= 4:
            judul = t.strip().split("\n")[0][:70]
            hit[i + 1] = (skor, judul)
    d.close()

    atas = [t for t in toc if t[0] <= 1][:maks_toc]
    padat = sorted(hit.items(), key=lambda x: -x[1][0])[:14]
    return dict(halaman=n, bertext=bertext, toc_total=len(toc),
                toc_atas=[(t[1][:66], t[2]) for t in atas],
                padat=[(h, s, j) for h, (s, j) in sorted(padat)])


def main():
    rows = list(csv.DictReader(io.open(REG, encoding="utf-8")))
    minta = [a for a in sys.argv[1:] if a.startswith("REF-")]
    target = [r for r in rows
              if r["authority_status"] == "INTAKE_ONLY" and r["r_level"] == "R3"
              and (not minta or r["reference_id"] in minta)]
    print("buku yang diproses:", len(target))
    hasil = {}
    dipakai = set()
    for r in target:
        d = os.path.join(EKAS, r["vault_path"].replace("/", os.sep))
        pdf = sorted(b for b in os.listdir(d) if b.lower().endswith(".pdf"))
        # cocokkan menurut tumpang tindih kata judul <-> nama berkas,
        # dan pastikan tiap berkas hanya dipakai satu rujukan
        def kata(s):
            return set(w.lower() for w in re.findall(r"[A-Za-z]{4,}", s))
        kj = kata(r["title"])
        urut = sorted(((len(kj & kata(b)), b) for b in pdf), reverse=True)
        pilih = next((b for _, b in urut if b not in dipakai), None)
        if not pilih:
            print("  ?? tidak dapat mencocokkan berkas:", r["reference_id"], r["title"][:44])
            continue
        dipakai.add(pilih)
        try:
            info = ringkas(os.path.join(d, pilih))
        except Exception as e:
            print("  !! gagal:", r["reference_id"], str(e)[:50])
            continue
        info["berkas"] = pilih
        info["judul"] = r["title"]
        info["laci"] = r["vault_path"]
        hasil[r["reference_id"]] = info
        print("  %-14s %5d hal · toc %3d · teks %d/8 · %s"
              % (r["reference_id"], info["halaman"], info["toc_total"],
                 info["bertext"], pilih[:40]))

    out = os.path.join(EKAS, "90_TOOLS", "bahan-resume.json")
    io.open(out, "w", encoding="utf-8").write(json.dumps(hasil, ensure_ascii=False, indent=1))
    print("\nbahan ditulis ke:", out)


if __name__ == "__main__":
    main()
