# -*- coding: utf-8 -*-
"""
BANGUN DAFTAR RUJUKAN UNTUK SKILL (adaptasi Hermes)

Membangkitkan `references/04-daftar-rujukan-lengkap.md` di dalam skill ini langsung dari
MASTER-REFERENCE-REGISTER.csv korpus EKAS, sehingga daftar tidak dapat menyimpang dari rak.

Jalankan ulang setiap kali register berubah:
    python scripts/bangun_daftar_skill.py
"""
import io, os, sys, csv, glob, collections

sys.stdout.reconfigure(encoding="utf-8")

# Kanonik korpus EKAS (shared workspace). Ubah bila lokasi berubah.
EKAS = os.environ.get("EKAS_CORPUS", r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/ekas")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "references", "04-daftar-rujukan-lengkap.md")
NL = chr(10)

BOLEH = {
    "R1": "ya — mengikat",
    "R2": "ya bila diadopsi kontrak",
    "R3": "hanya bila kontrak mengadopsinya",
    "R4": "wajib untuk angka produk",
    "R5": "tidak pernah",
}

def main():
    rows = list(csv.DictReader(io.open(
        os.path.join(EKAS, "02_REGISTERS", "MASTER-REFERENCE-REGISTER.csv"), encoding="utf-8")))
    rantai = sorted({os.path.basename(os.path.dirname(p))
                     for p in glob.glob(os.path.join(EKAS, "05_DOMAIN-KNOWLEDGE", "*", "RANTAI-JAMINAN.md"))})
    putus = {"GROUNDING-LIGHTNING", "CYBERSECURITY", "CIVIL-STRUCTURAL",
             "CONSTRUCTION", "BUILDING-CONSTRUCTION"}
    belum_penuh = {"RF-WIRELESS", "COMPUTER-VISION", "AI-ML",
                   "SYSTEMS-ENGINEERING", "NUMERICAL-METHODS"}

    per_dom = collections.defaultdict(list)
    for r in rows:
        per_dom[r.get("domain") or "?"].append(r)
    c = collections.Counter(r.get("r_level") or "?" for r in rows)

    L = []
    L.append("# 04 — Daftar rujukan lengkap\n")
    L.append("> **Dibangkitkan otomatis** dari `02_REGISTERS/MASTER-REFERENCE-REGISTER.csv` oleh")
    L.append("> `scripts/bangun_daftar_skill.py`. **Jangan disunting tangan** — suntingan akan hilang")
    L.append("> saat dibangun ulang.\n")
    L.append("Berkas ini menjawab: **rak ini punya apa saja, dan masing-masing boleh dipakai untuk apa.**\n")
    L.append("Tingkat R: R1 regulasi Indonesia (mengikat hukum) · R2 standar internasional ·")
    L.append("R3 buku teks/handbook · R4 dokumentasi pabrikan · R5 sumber sekunder (penunjuk).\n")

    L.append("## Sebaran\n")
    L.append("| Tingkat | Jumlah | Boleh menetapkan ambang? |")
    L.append("|---|---|---|")
    for lvl in ("R1", "R2", "R3", "R4", "R5"):
        L.append(f"| **{lvl}** | {c.get(lvl, 0)} | {BOLEH.get(lvl, '?')} |")
    L.append("| Total | %d | |" % len(rows))
    L.append("")

    L.append("## Per domain\n")
    for dom in sorted(per_dom):
        L.append(f"### {dom}  {'⚠ PUTUS' if dom in putus else ('⚠ BELUM PENUH (W2 baru)' if dom in belum_penuh else '')}")
        L.append("")
        L.append("| ID | Sumber | Edisi/Tahun | R | Halaman kunci |")
        L.append("|---|---|---|---|---|")
        for r in per_dom[dom]:
            L.append(f"| {r.get('ref_id') or r.get('reference_id') or r.get('id') or '-'} | {r.get('judul') or r.get('title') or '-'} "
                     f"| {r.get('tahun') or r.get('year') or '-'} | {r.get('r_level') or '?'} | {r.get('halaman') or r.get('pages') or '-'} |")
        L.append("")

    L.append("## Rantai jaminan tersedia")
    L.append("")
    L.append("| Domain | Status |")
    L.append("|---|---|")
    for d in rantai:
        L.append(f"| {d} | {'⚠ PUTUS — ambang tidak ada di rak' if d in putus else ('⚠ BELUM BERANTAI PENUH (W2 baru)' if d in belum_penuh else 'tersedia')} |")
    L.append("")

    # Header register berubah mungkin; tangani kolom dengan cara defensif di atas.
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L))
    print(f"OK: {OUT} ({len(rows)} rujukan, {len(rantai)} rantai)")

if __name__ == "__main__":
    main()