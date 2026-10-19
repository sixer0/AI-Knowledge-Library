#!/usr/bin/env python3
"""vault_promote — promote objek vault → wiki (GERBANG LIBRARIAN).

HANYA dipakai profil gsp-librarian (gatekeeper library). Menyalin objek vault
yang lolos attest ke ~/.hermes/wiki, menandai status dipromosikan, dan
mencatat jejak attestasi.

Gate yang ditegakkan:
  * sensitif=ya  → wajib --approval-ref <id persetujuan user>  (tanpa ini: menolak)
  * perkara dosir → wajib --verification-by <verifikator manusia>
  * objek berstatus ditolak/perlu_revisi → tidak bisa di-promote

Pemakaian:
  vault_promote.py --vault PATH --wiki PATH --object <rel> --by <librarian-id> \
    [--approval-ref ID] [--verification-by NAMA] [--reason "catatan"]

Uji mandiri: vault_promote.py --self-test
"""
import argparse
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

PROMOTABLE = {"usulan", "ditinjau", "menunggu_persetujuan", "menunggu_verifikasi"}
TERMINAL = {"ditolak", "perlu_revisi"}


def _json_unescape(v: str) -> str:
    """Kembalikan nilai terkutip ke teks aslinya (setara json.loads, tanpa dependensi)."""
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        try:
            import json
            out = json.loads(v)
            if isinstance(out, str):
                return out
        except Exception:  # noqa: BLE001
            pass
        return v[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return v


def parse_fm(raw: str) -> dict:
    """Ekstrak frontmatter YAML sederhana (baris `key: value`)."""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", raw, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = _json_unescape(v.strip())
    return fm


def rel_body(raw: str) -> str:
    m = re.match(r"^---\n.*?\n---\n?(.*)$", raw, re.S)
    return m.group(1) if m else raw


_YAML_BOOLISH = {"true", "false", "yes", "no", "on", "off", "null", "~"}
_YAML_INDICATORS = "-?:,[]{}#&*!|>'\"%@`"


def _plain_is_safe(v: str) -> bool:
    """Apakah nilai boleh ditulis TANPA kutip dan tetap terparse utuh?

    Konservatif: kalau ragu, jangan tulis plain (pemanggil akan mengutip).
    """
    if v == "" or v != v.strip():
        return False
    if v[0] in _YAML_INDICATORS:
        return False
    if ": " in v or v.endswith(":"):          # colon-space = pemisah mapping baru
        return False
    if "#" in v:                              # ' #' dianggap komentar; '#' pun berisiko
        return False
    if v.lower() in _YAML_BOOLISH:            # agar tidak berubah jadi bool/None
        return False
    return True


def _yaml_scalar(v) -> str:
    """Serialisasi nilai frontmatter agar valid YAML TANPA mengubah konvensi grep.

    Nilai yang aman dibiarkan plain (`status: active`, `di-attest-oleh: gsp-librarian`)
    supaya grep ekosistem tetap cocok; hanya nilai bermasalah yang dikutip lewat
    json.dumps (subset YAML 1.2, selalu terparse kembali identik). Menutup defect
    2026-09-01: `halaman: -` gagal parse dan judul berisi `#` terpotong diam-diam.
    """
    import json
    if v is None:
        return '""'
    s = str(v)
    # flow-style yang memang sah (tags/links: [a, b]) dipertahankan apa adanya
    if s.startswith("[") and s.endswith("]"):
        return s
    return s if _plain_is_safe(s) else json.dumps(s, ensure_ascii=False)


def rebuild(fm: dict, body: str) -> str:
    lines = ["---"]
    for k, v in fm.items():
        lines.append(f"{k}: {_yaml_scalar(v)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.strip() + "\n"


def gate(fm: dict, a) -> list[str]:
    errs = []
    status = fm.get("status", "usulan")
    if status in TERMINAL:
        errs.append(f"status '{status}' tidak bisa di-promote")
    if status not in PROMOTABLE:
        errs.append(f"status '{status}' bukan status promotable {sorted(PROMOTABLE)}")
    if fm.get("sensitif") == "ya" and not a.approval_ref:
        errs.append("objek SENSITIF wajib --approval-ref (persetujuan user) sebelum promote")
    if fm.get("perkara", "").strip().lower().startswith("dosir") and not a.verification_by:
        errs.append("objek DOSIR wajib --verification-by (verifikasi manusia) sebelum promote")
    if not fm.get("id") or not fm.get("title"):
        errs.append("frontmatter id/title wajib")
    # prinsip #3: objek yang mengklaim angka wajib sumber
    if not fm.get("sumber"):
        errs.append("(warn) objek tanpa sumber — pastikan tidak ada klaim angka tanpa halaman")
    return errs


def promote(fm: dict, body: str, a) -> tuple[Path, str]:
    wiki = Path(a.wiki)
    wtype = fm.get("type", "note")
    slug = fm["id"]
    wrel = f"{wtype}s/{slug}.md"
    wfull = wiki / wrel
    wfull.parent.mkdir(parents=True, exist_ok=True)

    # Entri WIKI memakai lifecycle wiki (active/superseded/archived) — entri yang
    # terbit berstatus active. Status "dipromosikan" tetap tinggal di OBJEK VAULT.
    fm_wiki = dict(fm)
    fm_wiki["status"] = "active"
    fm_wiki["di-attest-oleh"] = a.by
    fm_wiki["di-attest-pada"] = date.today().isoformat()
    fm_wiki["dipromosikan-ke"] = wrel
    if a.approval_ref:
        fm_wiki["persetujuan-ref"] = a.approval_ref
    if a.verification_by:
        fm_wiki["verifikasi-oleh"] = a.verification_by
    if a.reason:
        fm_wiki["catatan_keputusan"] = f"dipromosikan: {a.reason}"
    wfull.write_text(rebuild(fm_wiki, body), "utf-8")

    # Objek VAULT mencatat promosi (lifecycle vault)
    fm["status"] = "dipromosikan"
    fm["di-attest-oleh"] = a.by
    fm["di-attest-pada"] = date.today().isoformat()
    fm["dipromosikan-ke"] = wrel
    if a.approval_ref:
        fm["persetujuan-ref"] = a.approval_ref
    if a.verification_by:
        fm["verifikasi-oleh"] = a.verification_by
    if a.reason:
        fm["catatan_keputusan"] = f"dipromosikan: {a.reason}"
    return wfull, wrel


def git_commit(wiki: Path, msg: str) -> None:
    try:
        if not (wiki / ".git").exists():
            subprocess.run(["git", "-C", str(wiki), "init"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(wiki), "add", "-A"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(wiki), "commit", "-m", msg],
                       check=True, capture_output=True)
    except subprocess.CalledProcessError:
        pass  # tidak ada perubahan / bukan repo — bukan kegagalan promote


def self_test() -> None:
    with tempfile.TemporaryDirectory() as td:
        vault = Path(td) / "vault"; wiki = Path(td) / "wiki"
        vault.mkdir(); wiki.mkdir()
        obj = vault / "umum" / "2026-08-23_vendor-uji.md"
        obj.parent.mkdir(parents=True, exist_ok=True)
        obj.write_text(
            "---\nid: vendor-uji\ntype: vendor\ntitle: Vendor Uji\nstatus: usulan\n"
            "sumber: docs/uji.md\nhalaman: 2\nsensitif: tidak\nperkara: umum\n"
            "---\n\nRingkasan (halaman 2).\n", "utf-8")
        a = argparse.Namespace(vault=str(vault), wiki=str(wiki), object="umum/2026-08-23_vendor-uji.md",
                               by="gsp-librarian", approval_ref=None, verification_by=None, reason="ok")
        raw = obj.read_text("utf-8")
        fm = parse_fm(raw)
        assert gate(fm, a) == [], f"seharusnya lolos: {gate(fm, a)}"
        wfull, wrel = promote(fm, rel_body(raw), a)
        assert (wiki / wrel).exists()
        wiki_txt = (wiki / wrel).read_text("utf-8")
        assert "status: active" in wiki_txt, "entri wiki harus berstatus active (terbit)"
        assert "di-attest-oleh: gsp-librarian" in wiki_txt, "wiki harus membawa jejak attest"
        # main() menulis ulang objek vault dengan fm yang sudah dimutasi promote()
        obj.write_text(rebuild(fm, rel_body(raw)), "utf-8")
        obj_txt = obj.read_text("utf-8")
        assert "status: dipromosikan" in obj_txt, "objek vault harus mencatat dipromosikan"
        # sensitif tanpa approval → ditolak
        raw2 = raw.replace("sensitif: tidak", "sensitif: ya")
        fm2 = parse_fm(raw2)
        assert any("SENSITIF" in e for e in gate(fm2, a)), "sensitif harus butuh approval-ref"
        # dosir tanpa verifikasi → ditolak
        raw3 = raw.replace("perkara: umum", "perkara: dosir-x")
        fm3 = parse_fm(raw3)
        assert any("DOSIR" in e for e in gate(fm3, a)), "dosir harus butuh verifikasi"
        print(f"self-test OK — contoh wiki: {wrel}")


def main() -> int:
    p = argparse.ArgumentParser(description="Promote objek vault → wiki (gatekeeper librarian)")
    p.add_argument("--vault")
    p.add_argument("--wiki")
    p.add_argument("--object")
    p.add_argument("--by", default="gsp-librarian")
    p.add_argument("--approval-ref")
    p.add_argument("--verification-by")
    p.add_argument("--reason")
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()

    if a.self_test:
        self_test()
        return 0

    missing = [n for n, v in (("--vault", a.vault), ("--wiki", a.wiki), ("--object", a.object)) if not v]
    if missing:
        p.error("the following arguments are required: " + ", ".join(missing))

    obj = Path(a.vault) / a.object
    if not obj.exists():
        print(f"error: objek tidak ada: {obj}", file=sys.stderr)
        return 2
    raw = obj.read_text("utf-8")
    fm = parse_fm(raw)
    errs = gate(fm, a)
    if errs:
        for e in errs:
            print(f"[{'WARN' if e.startswith('(warn)') else 'ERROR'}] {e}", file=sys.stderr)
        if any(not e.startswith("(warn)") for e in errs):
            return 2
    wfull, wrel = promote(fm, rel_body(raw), a)
    git_commit(Path(a.wiki), f"wiki: promote {wrel} (oleh {a.by})")
    # tandai objek vault jadi dipromosikan juga
    obj.write_text(rebuild(fm, rel_body(raw)), "utf-8")
    print(f"ok: promoted {wrel} -> {wfull}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
