#!/usr/bin/env python3
"""vault_propose — buat objek usulan vault GSP (format gsp-library-data-standards).

Membuat satu berkas markdown `vault/<perkara>/<YYYY-MM-DD>_<slug>.md` dengan
frontmatter lengkap. Siapa pun (agen/analis/librarian) boleh mengusulkan.

Pemakaian:
  vault_propose.py --vault PATH --perkara FOLDER --title T --type TYPE \
    [--sumber REL --halaman N --tanggal-akses YYYY-MM-DD --kelas-bukti X \
     --sensitif ya|tidak --perkara X --tags a,b --links a,b \
     --body TEXT | --body-file PATH --id SLUG --require-provenance]

Uji mandiri:  vault_propose.py --self-test
"""
import argparse
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

TYPES = {"vendor", "produk", "standar", "proyek", "dosir", "catatan",
         "keputusan", "pelajaran", "fakta"}
STATUS = "usulan"
KELAS = {"primer", "sekunder", "tersier", "sintesis"}


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "objek"


def build_frontmatter(a) -> str:
    fm = [
        "---",
        f"id: {a.id}",
        f"type: {a.type}",
        f'title: "{a.title}"',
        f"status: {STATUS}",
    ]
    if a.sumber:
        fm.append(f"sumber: {a.sumber}")
    if a.halaman:
        fm.append(f"halaman: {a.halaman}")
    fm.append(f"tanggal_akses: {a.tanggal_akses or date.today().isoformat()}")
    fm.append(f"kelas_bukti: {a.kelas_bukti}")
    fm.append(f"sensitif: {a.sensitif}")
    if a.perkara:
        fm.append(f"perkara: {a.perkara}")
    if a.tags:
        fm.append(f"tags: [{', '.join(a.tags)}]")
    if a.links:
        fm.append(f"links: [{', '.join(a.links)}]")
    fm.append(f"penulis: {a.penulis or 'dashboard'}")
    fm.append(f"diajukan: {date.today().isoformat()}")
    fm.append("---")
    return "\n".join(fm) + "\n"


def validate(a, body: str) -> list[str]:
    """Kembalikan daftar masalah (kosong = valid)."""
    errs = []
    if not a.title.strip():
        errs.append("title wajib")
    if a.type not in TYPES:
        errs.append(f"type '{a.type}' di luar taksonomi awal {sorted(TYPES)} (skema diamati — boleh baru, tapi sadar)")
    if a.kelas_bukti not in KELAS:
        errs.append(f"kelas_bukti '{a.kelas_bukti}' harus salah satu {sorted(KELAS)}")
    if a.sensitif not in ("ya", "tidak"):
        errs.append("sensitif harus 'ya' atau 'tidak'")
    # prinsip #3: angka tanpa halaman dianggap tidak ada
    if a.require_provenance and a.sumber is None:
        errs.append("klaim butuh sumber (--require-provenance aktif, sumber kosong)")
    if a.sumber and not a.halaman:
        # peringatan bukan penolakan — objek tetap dibuat; dicatat
        errs.append("(warn) sumber tanpa halaman — untuk angka, halaman wajib")
    return errs


def write_object(a, body: str) -> Path:
    vault = Path(a.vault)
    target = vault / a.perkara
    target.mkdir(parents=True, exist_ok=True)
    rel = f"{date.today().isoformat()}_{a.id}.md"
    out = target / rel
    content = build_frontmatter(a) + "\n" + body.strip() + "\n"
    out.write_text(content, "utf-8")
    return out


def self_test() -> None:
    with tempfile.TemporaryDirectory() as td:
        vault = Path(td) / "vault"
        a = argparse.Namespace(
            vault=str(vault), perkara="umum", title="Objek Uji", type="fakta",
            sumber="docs/uji.md", halaman="2", tanggal_akses=None,
            kelas_bukti="primer", sensitif="tidak", tags=["uji"], links=[],
            penulis="test", id="uji-001", require_provenance=True,
        )
        errs = validate(a, "Angka 12.000 (halaman 2).")
        assert not errs, f"seharusnya valid: {errs}"
        out = write_object(a, "Angka 12.000 (halaman 2).")
        assert out.exists() and "uji-001" in out.name
        # tanpa sumber + require → error
        a2 = argparse.Namespace(**{**vars(a), "sumber": None})
        assert validate(a2, "x") != [], "harus menolak klaim tanpa sumber"
        print(f"self-test OK — objek contoh: {out}")


def main() -> int:
    p = argparse.ArgumentParser(description="Buat objek usulan vault GSP")
    p.add_argument("--vault")
    p.add_argument("--perkara", default="umum")
    p.add_argument("--title")
    p.add_argument("--type")
    p.add_argument("--id")
    p.add_argument("--sumber")
    p.add_argument("--halaman")
    p.add_argument("--tanggal-akses")
    p.add_argument("--kelas-bukti", default="sekunder")
    p.add_argument("--sensitif", default="tidak", choices=["ya", "tidak"])
    p.add_argument("--tags")
    p.add_argument("--links")
    p.add_argument("--penulis", default="dashboard")
    p.add_argument("--body")
    p.add_argument("--body-file")
    p.add_argument("--require-provenance", action="store_true")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()

    if a.self_test:
        self_test()
        return 0

    missing = [n for n, v in (("--vault", a.vault), ("--title", a.title), ("--type", a.type)) if not v]
    if missing:
        p.error("the following arguments are required: " + ", ".join(missing))

    body = a.body
    if a.body_file:
        body = Path(a.body_file).read_text("utf-8")
    body = body or ""
    a.id = a.id or slugify(a.title)
    a.tags = [t.strip() for t in (a.tags or "").split(",") if t.strip()]
    a.links = [t.strip() for t in (a.links or "").split(",") if t.strip()]

    errs = validate(a, body)
    if errs:
        for e in errs:
            print(f"[{ 'WARN' if e.startswith('(warn)') else 'ERROR' }] {e}", file=sys.stderr)
        hard = [e for e in errs if not e.startswith("(warn)")]
        if hard:
            return 2
    out = write_object(a, body)
    print(f"ok: {out.relative_to(Path(a.vault).parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
