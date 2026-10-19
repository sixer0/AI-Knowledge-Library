#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""find_skill.py — pencarian skill teks penuh atas registry fleet (SM-LB, 27-09-2026).

Kenapa ada: keadaan lama memilih skill dari indeks deskripsi yang terpotong 57 karakter.
Pilot SEM-PILOT-0925 mengukur recall@5 pada 49 pasangan ground truth (kartu tugas nyata ->
skill yang akhirnya dipakai): indeks terpotong 4,1%, BM25 teks penuh registry 91,8%.
Selisihnya berasal dari lapisan baca, bukan semantik. Alat ini memakai mesin dan lapisan
baca yang SAMA dengan yang terverifikasi GT itu: FTS5/bm25 SQLite atas nama+deskripsi+isi
awal (2500 char) tiap SKILL.md, dibaca READ-ONLY dari registry, indeks dibangun di memori.

Determinisme: tanpa acak, tanpa stempel waktu, tie-break urutan id; dua run pada korpus dan
kueri sama mencetak byte identik. stdlib saja, nol API, nol jaringan.

Pemakaian:
  python find_skill.py --query "teks tugas lengkap" [--top 5] [--registry PATH]
  python find_skill.py --selftest    # uji dua arah: PASS bersih DAN menangkap rusak

Keluaran: `SKOR <nama_skill> <skor_bm25>` terurut desc (skor kecil = paling relevan,
konvensi rank FTS5), lalu `SUMBER <registry>` dan `CORPUS <n> SKILL.md`. Ini LAPISAN BACA,
bukan vonis: keputusan rekomendasi tetap milik Skill Manager sesuai gate skill ini.
"""
import argparse, os, re, sqlite3, sys

DEFAULT_REGISTRY = os.path.join(
    os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "skills", "gsp")

SKIP_DIRS = ("node_modules", ".git", "__pycache__")

def load_corpus(reg):
    """Semua SKILL.md pada kedalaman apa pun; nested ganda <name>/<name>/ = cacat, diabaikan.
    Lapisan baca terverifikasi-GT: nama + deskripsi frontmatter + isi awal s.d. 2500 char
    (body utuh hingga 101KB menekan bm25 lewat normalisasi panjang: 91,8 -> 75,5, ukur 27-09)."""
    docs = {}
    for dp, dn, fn in os.walk(reg):
        dn[:] = [d for d in dn if d not in SKIP_DIRS and d != "scripts"]
        # catatan 27-09: tanpa buang 'scripts', fixture selftest di dalam paket
        # (scripts/fixtures/registry/<x>/SKILL.md) ikut terindeks sebagai skill produksi.
        if "SKILL.md" not in fn:
            continue
        name = os.path.basename(dp)
        if os.path.basename(os.path.dirname(dp)) == name:
            continue
        raw = open(os.path.join(dp, "SKILL.md"), encoding="utf-8", errors="replace").read()
        m = re.search(r"^description:\s*(.+)$", raw, re.M)
        text = f"{name}\n{m.group(1).strip() if m else ''}\n{raw[:2500]}"[:4800]
        docs[name] = re.sub(r"\s+", " ", text)
    return docs

def build_db(docs):
    db = sqlite3.connect(":memory:")
    db.execute("CREATE VIRTUAL TABLE d USING fts5(id UNINDEXED, text)")
    db.executemany("insert into d values(?,?)",
                   [(i, docs[i]) for i in sorted(docs)])
    db.commit()
    return db

def search(db, query, top):
    words = re.findall(r"[A-Za-z0-9\-]{3,}", query)[:20]
    if not words:
        return []
    match = " OR ".join(f'"{w}"' for w in words)
    try:
        return [(r[0], r[1]) for r in db.execute(
            "select id, rank from d where d match ? order by rank, id limit ?",
            (match, top))]
    except sqlite3.OperationalError:
        return []

def run(query, top, reg):
    docs = load_corpus(reg)
    if not docs:
        print(f"ERROR: registry kosong/tidak terbaca: {reg}", file=sys.stderr)
        return 2
    db = build_db(docs)
    ranked = search(db, query, top)
    for name, s in ranked:
        print(f"SKOR {name} {s:.4f}")
    if not ranked:
        print("SKOR - 0.0000  (tidak ada cocok; laporkan, jangan karang nama skill)")
    print(f"SUMBER {reg.replace(os.sep, '/')}")
    print(f"CORPUS {len(docs)} SKILL.md")
    return 0

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "registry")

def selftest():
    docs = load_corpus(FIX)
    db = build_db(docs)
    ok = True
    top1 = search(db, "distribusi skill on-demand fleet salin ke profil", 1)
    g1 = bool(top1) and top1[0][0] == "alpha-distribute"
    print(f"SELFTEST GREEN top1={'alpha-distribute' if g1 else (top1[0][0] if top1 else 'KOSONG')}: {'OK' if g1 else 'GAGAL'}")
    ok &= g1
    miss = search(db, "zulu qwerty xcvbnm", 3)
    g2 = len(miss) == 0
    print(f"SELFTEST RED kandidat-untuk-kueri-acak={len(miss)}: {'OK' if g2 else 'GAGAL'}")
    ok &= g2
    a = search(db, "verifikasi bukti gerbang selesai", 5)
    b = search(db, "verifikasi bukti gerbang selesai", 5)
    g3 = a == b
    print(f"SELFTEST DETEK determinisme: {'OK' if g3 else 'GAGAL'}")
    ok &= g3
    # arah rusak struktural: registry kosong harus exit!=0 saat run
    g4 = run("apa pun", 3, os.path.join(FIX, "TIDAKADA")) == 2
    print(f"SELFTEST RED registry-kosong exit2: {'OK' if g4 else 'GAGAL'}")
    ok &= g4
    print("SELFTEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--query")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--registry", default=DEFAULT_REGISTRY)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.query:
        ap.error("butuh --query atau --selftest")
    sys.exit(run(a.query, a.top, a.registry))

if __name__ == "__main__":
    main()
