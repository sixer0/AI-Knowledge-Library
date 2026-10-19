# -*- coding: utf-8 -*-
"""Penjaga invarian mingguan gerbang naturalisasi (NAT-S25, kebijakan 02-09-2026).

Pola: INV-7 (cron Selasa 06:00). Keputusan D-TA-06: TANPA auto-block, hanya laporan.

Cek:
  C-1  Blok GATE NATURALISASI utuh (marker awal + baris penutup) di SELURUH
       SOUL.md aktif: profiles/*/SOUL.md + SOUL.md HOME root (label ROOT(default)).
       Sensus glob saat-itu; basis beku kontrak 53 profil + root = 54 target.
       Profil baru yang muncul setelah baseline ikut dihitung dan dilaporkan
       sebagai drift satu baris (bukan kegagalan).
  C-2  Skill fleet gsp-output-naturalization tidak drift vs kanonik: sha256 per
       berkas relatif (SKILL.md, references/**, scripts/**), mengecualikan
       __pycache__ dan file .pyc.
  C-3  Laporan selisih ditulis ke folder kontrak docs/2026-09-02-naturalisasi-
       output/gate-watchdog/gate-nat-<YYYYMMDD_HHMMSS>.md + pointer latest.md.

Keluaran stdout (stdout kosong = diam saat semua hijau, pola watchdog):
  - Selalu menulis laporan ke disk (jejak mingguan).
  - stdout terisi HANYA bila ada FAIL (selisih), agar cron no_agent tidak
    spam saat sehat. Sensus ringkas tetap tercetak saat sehat? TIDAK: pola
    INV watchdog = diam saat sehat; laporan harian ada di file.

Exit code: 0 = semua utuh; 1 = ada selisih (tetapi TIDAK memblokir apa pun).
"""
import hashlib
import os
import sys
from datetime import datetime
from pathlib import Path

def _resolve_home() -> Path:
    """Home basis fleet = direktori yang memuat subfolder profiles/.
    PITFALL (teruji 02-09): HERMES_HOME di sesi worker menunjuk ROOT PROFIL
    (mis. .../profiles/gsp-system-manager), bukan home basis -- jangan dipercaya
    mentah. Kandidat: env HERMES_HOME bila punya profiles/, else env LOCALAPPDATA,
    else path eksplisit host GSP."""
    cands = []
    env_h = os.environ.get("HERMES_HOME")
    la = os.environ.get("LOCALAPPDATA")
    if env_h:
        cands.append(Path(env_h))
    if la:
        cands.append(Path(la) / "hermes")
    cands.append(Path("C:/Users/TRIAL/AppData/Local/hermes"))
    for c in cands:
        if (c / "profiles").is_dir():
            return c
    return Path("C:/Users/TRIAL/AppData/Local/hermes")


HERMES_HOME = _resolve_home()

PROFILES = HERMES_HOME / "profiles"
ROOT_SOUL = HERMES_HOME / "SOUL.md"
ROOT_LABEL = "ROOT(default)"

WS = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace")
CANONICAL_SKILL = Path("C:/Users/TRIAL/workspace/gsp-hermes/skills") / "gsp-output-naturalization"
FLEET_SKILL = HERMES_HOME / "skills" / "gsp" / "gsp-output-naturalization"

REPORT_DIR = WS / "docs" / "2026-09-02-naturalisasi-output" / "gate-watchdog"

BASIS_RESMI = 53  # bekuan kontrak seksi 4b (profil) ; +1 root = 54 target
SKILL_NAME = "gsp-output-naturalization"

# Konstanta pembanding verifikasi WAJIB substring literal persis dari blok
# (pitfall NAT-S13: konstanta bukan substring -> verifikasi salah lapor RUSAK).
BLOCK_START = "## GATE NATURALISASI"
BLOCK_END = "gerbang bersifat prosedural-terverifikasi, bukan hard-gate transport."


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def soul_targets():
    """Sensus glob saat-itu: (label, path) untuk tiap SOUL.md aktif."""
    out = []
    if ROOT_SOUL.is_file():
        out.append((ROOT_LABEL, ROOT_SOUL))
    if PROFILES.is_dir():
        for pdir in sorted(PROFILES.iterdir()):
            if not pdir.is_dir():
                continue
            soul = pdir / "SOUL.md"
            # hanya SOUL tingkat atas profil; artefak scratch lebih dalam diabaikan
            if soul.is_file():
                out.append((pdir.name, soul))
    return out


def check_souls():
    """C-1: blok utuh di semua target. Return (rows_ok, rows_missing, rows_partial, n_total)."""
    ok, missing, partial = [], [], []
    for label, path in soul_targets():
        t = read(path)
        has_start = BLOCK_START in t
        has_end = BLOCK_END in t
        if has_start and has_end:
            ok.append(label)
        elif has_start or has_end:
            partial.append(label)
        else:
            missing.append(label)
    return ok, missing, partial


def skill_files(root: Path):
    """Berkas relatif skill, eksklusif __pycache__/*.pyc."""
    files = {}
    if not root.is_dir():
        return files
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if "__pycache__" in rel or rel.endswith(".pyc"):
            continue
        files[rel] = p
    return files


def check_skill_drift():
    """C-2: sha256 fleet vs kanonik per berkas relatif.
    Return (status, detail_dict) dengan status in {OK, DRIFT, MISSING}."""
    canon = skill_files(CANONICAL_SKILL)
    fleet = skill_files(FLEET_SKILL)
    if not canon:
        return "MISSING", {"reason": f"kanonik tidak ditemukan: {CANONICAL_SKILL}"}
    if not fleet:
        return "MISSING", {"reason": f"fleet tidak ditemukan: {FLEET_SKILL}"}
    drift = []
    only_canon = sorted(set(canon) - set(fleet))
    only_fleet = sorted(set(fleet) - set(canon))
    for rel in sorted(set(canon) & set(fleet)):
        hc = sha256_file(canon[rel])
        hf = sha256_file(fleet[rel])
        if hc != hf:
            drift.append({"file": rel, "canonical_sha": hc[:12], "fleet_sha": hf[:12]})
    status = "OK" if not (drift or only_canon or only_fleet) else "DRIFT"
    return status, {"drift": drift, "only_canonical": only_canon, "only_fleet": only_fleet,
                    "n_files_compared": len(set(canon) & set(fleet))}


def main():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ok, missing, partial = check_souls()
    n_total = len(ok) + len(missing) + len(partial)
    sk_status, sk_detail = check_skill_drift()

    verdict = "PASS"
    problems = []
    if missing:
        verdict = "FAIL"
        problems.append("SOUL tanpa blok GATE NATURALISASI: " + ", ".join(missing))
    if partial:
        verdict = "FAIL"
        problems.append("SOUL blok parsial (marker awal/penutup salah satu): " + ", ".join(partial))
    if sk_status == "DRIFT":
        verdict = "FAIL"
        problems.append(f"skill fleet DRIFT vs kanonik: {sk_detail}")
    elif sk_status == "MISSING":
        verdict = "FAIL"
        problems.append(f"skill hilang: {sk_detail}")

    drift_count = n_total - BASIS_RESMI - 1  # target aktif minus basis beku (53+root)

    lines = []
    lines.append(f"# Laporan penjaga gerbang naturalisasi — {ts}")
    lines.append("")
    lines.append(f"Basis beku kontrak: {BASIS_RESMI} profil + root = {BASIS_RESMI + 1} target. "
                 f"Sensus glob saat-itu: {n_total} target (drift sensus: {drift_count:+d}).")
    lines.append("")
    lines.append("## C-1 blok GATE NATURALISASI di SOUL")
    lines.append(f"- CHECK 1: {'PASS' if not missing and not partial else 'FAIL'} "
                 f"- utuh {len(ok)}/{n_total}; hilang {len(missing)}; parsial {len(partial)}")
    if missing:
        lines.append("- hilang: " + ", ".join(missing))
    if partial:
        lines.append("- parsial: " + ", ".join(partial))
    lines.append("")
    lines.append(f"## C-2 skill {SKILL_NAME}: fleet vs kanonik (sha256)")
    lines.append(f"- CHECK 2: {'PASS' if sk_status == 'OK' else 'FAIL'} - status {sk_status}, "
                 f"{sk_detail.get('n_files_compared', 0)} berkas dibandingkan")
    if sk_status != "OK":
        for k, v in sk_detail.items():
            if v:
                lines.append(f"  - {k}: {v}")
    lines.append("")
    lines.append("## C-3 keputusan D-TA-06")
    lines.append("- TANPA auto-block: penjaga ini hanya melapor; perbaikan adalah kartu terpisah.")
    lines.append("")
    if problems:
        lines.append("## Selisih")
        for pr in problems:
            lines.append(f"- {pr}")
        lines.append("")
    lines.append(f"VERDICT: {verdict}")

    report = "\n".join(lines) + "\n"

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    rp = REPORT_DIR / f"gate-nat-{ts}.md"
    rp.write_text(report, encoding="utf-8")
    (REPORT_DIR / "latest.md").write_text(report, encoding="utf-8")

    # stdout untuk cron no_agent: diam saat PASS, lapor saat FAIL
    if verdict != "PASS":
        print("[GATE-NAT] " + verdict + " — penjaga gerbang naturalisasi menemukan selisih:")
        for pr in problems:
            print("[GATE-NAT] " + pr)
        print(f"[GATE-NAT] laporan lengkap: {rp}")

    # jejak debug ke stderr tidak diperlukan; exit code jujur
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
