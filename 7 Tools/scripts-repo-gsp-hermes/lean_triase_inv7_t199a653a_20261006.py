#!/usr/bin/env python3
"""Remediasi INV-7 lean-cap (kartu t_199a653a, 06-10-2026) untuk
gsp-master / gsp-master01 / gspuser02.

Pola gabungan teruji:
- scripts/lean_fix_inv7_20260929.py : keep diambil dari marker .lean-policy tiap profil
  (BUKAN trio kaku), backup zip penuh sebelum mutasi, verifikasi akhir fisik==keep<=cap.
- scripts/remediate_inv7_user01_20260902.py : dup-check sha256 vs registry fleet sebelum
  hapus, arsip lossless + manifest.

Kebijakan per entri non-keep (direktori top-level skills/ yang dihitung INV-7):
- TREE-IDENTIK dengan salinan registry fleet  -> HAPUS dari profil (salinan registry tetap).
- UNIK (tidak ada padanan di registry/kanonik) -> PINDAH (move) ke registry fleet:
    nama 'gsp-*'            -> <REG>/gsp/<nama>
    selain itu              -> <REG>/<kategori-asal>/<nama>   (buat folder kategori bila perlu)
  TIDAK ADA yang dihapus demi angka tanpa salinan/arsip.
Marker .lean-policy + .no-bundled-skills diverifikasi ada (tulis bila hilang).
Idempoten: jalankan ulang = semua skip. Mode --check = rencana saja, nol mutasi.
"""
import json, os, shutil, sys, time, hashlib, zipfile
from pathlib import Path

LA = Path("C:/Users/TRIAL/AppData/Local/hermes")
REG = LA / "skills"
CANON = Path("C:/Users/TRIAL/workspace/gsp-hermes/skills")
WS = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace")
STAMP = time.strftime("%Y%m%d_%H%M%S")
BACKUPS = WS / "backups" / f"2026-10-06-inv7-triase-{STAMP}"
NAMES = ["gsp-master", "gsp-master01", "gspuser02"]
CAP = 5
APPLY = "--check" not in sys.argv

def sha(f):
    try:
        return hashlib.sha256(Path(f).read_bytes()).hexdigest()
    except Exception:
        return None

def tree_hashes(root: Path):
    out = {}
    for dp, dn, fn in os.walk(root):
        for f in fn:
            p = Path(dp) / f
            out[str(p.relative_to(root)).replace(os.sep, "/")] = sha(p)
    return out

def index_skills(base: Path):
    idx = {}
    for dp, dn, fn in os.walk(base):
        if "SKILL.md" in fn:
            idx.setdefault(Path(dp).name, []).append(Path(dp))
    return idx

def registry_tree_index():
    """name -> list of (dir, treehash-json) untuk uji identik penuh."""
    idx = index_skills(REG)
    out = {}
    for name, dirs in idx.items():
        out[name] = [(d, json.dumps(tree_hashes(d), sort_keys=True)) for d in dirs]
    return out

def fix(NAME, reg_trees):
    pdir = LA / "profiles" / NAME
    skills = pdir / "skills"
    assert pdir.is_dir(), f"profil {NAME} tidak ada"
    mkf = pdir / ".lean-policy"
    mk = json.loads(mkf.read_text(encoding="utf-8"))
    keep = sorted(mk["always_load"])
    assert mk.get("lean") and mk.get("lane") == "controller", f"{NAME}: marker bukan lean-controller"
    actions, skipped = [], []

    have = sorted(d.name for d in skills.iterdir() if d.is_dir() and not d.name.startswith("."))
    if have == keep and len(have) <= CAP:
        return {"profile": NAME, "skipped_all": True, "have": have}

    # marker wajib: .lean-policy (sudah dibaca) + .no-bundled-skills di ROOT profil
    nb = pdir / ".no-bundled-skills"
    if not nb.exists():
        if APPLY:
            nb.write_text("", encoding="utf-8")
        actions.append({"action": "write-marker", "path": str(nb)})

    extras = [h for h in have if h not in keep]
    for e in extras:
        full = skills / e
        th = json.dumps(tree_hashes(full), sort_keys=True)
        # kasus A: entri flat dengan SKILL.md
        if (full / "SKILL.md").is_file():
            name = e
            cand = reg_trees.get(name, [])
            ident = next((d for d, h in cand if h == th), None)
            if ident:
                actions.append({"action": "delete-identical", "path": str(full),
                                "kept_at": str(ident), "sha_skillmd": sha(full / "SKILL.md")})
                if APPLY:
                    shutil.rmtree(full)
            else:
                tgt = REG / "gsp" / name if name.startswith("gsp") else REG / e / name
                actions.append({"action": "MOVE-unique", "path": str(full), "to": str(tgt),
                                "sha_skillmd": sha(full / "SKILL.md")})
                if APPLY:
                    assert not tgt.exists(), f"tabrakan target registry: {tgt}"
                    tgt.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(full), str(tgt))
            continue
        # kasus B: direktori kategori berisi skill bersarang
        nested = sorted(d for d in full.iterdir() if d.is_dir())
        for sp in nested:
            name = sp.name
            sk = sp / "SKILL.md"
            nth = json.dumps(tree_hashes(sp), sort_keys=True)
            if not sk.is_file():
                raise AssertionError(f"{NAME}/{e}/{name}: direktori tanpa SKILL.md - tangani manual")
            cand = reg_trees.get(name, [])
            ident = next((d for d, h in cand if h == nth), None)
            if ident:
                actions.append({"action": "delete-identical", "path": str(sp),
                                "kept_at": str(ident), "sha_skillmd": sha(sk)})
                if APPLY:
                    shutil.rmtree(sp)
            else:
                tgt = REG / "gsp" / name if name.startswith("gsp") else REG / e / name
                actions.append({"action": "MOVE-unique", "path": str(sp), "to": str(tgt),
                                "sha_skillmd": sha(sk)})
                if APPLY:
                    assert not tgt.exists(), f"tabrakan target registry: {tgt}"
                    tgt.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(sp), str(tgt))
        # sisa direktori kategori setelah isi diproses
        if APPLY:
            if full.exists():
                rest = list(full.iterdir())
                if rest:
                    raise AssertionError(f"{NAME}/{e}: sisa tak terklasifikasi {rest}")
                full.rmdir()

    # verifikasi akhir hanya saat apply
    after = None
    if APPLY:
        after = sorted(d.name for d in skills.iterdir() if d.is_dir() and not d.name.startswith("."))
        soul = (pdir / "SOUL.md").read_text(encoding="utf-8")
        assert after == keep, f"VERIFIKASI GAGAL {NAME}: fisik {after} != keep {keep}"
        assert len(after) <= CAP, f"VERIFIKASI GAGAL {NAME}: {len(after)} > cap"
        assert "GATE ENFORCEMENT" in soul and "LANE CONTROLLER" in soul, f"SOUL gate {NAME} rusak"
        assert (pdir / ".no-bundled-skills").exists(), f"marker .no-bundled-skills {NAME} hilang"
    return {"profile": NAME, "before": have, "after": after, "keep": keep,
            "actions": actions}

def main():
    results = []
    reg_trees = registry_tree_index()
    if APPLY:
        BACKUPS.mkdir(parents=True, exist_ok=True)
        for n in NAMES:
            src = LA / "profiles" / n / "skills"
            z = BACKUPS / f"{n}_skills.zip"
            with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
                for dp, dn, fn in os.walk(src):
                    for f in fn:
                        p = Path(dp) / f
                        zf.write(p, str(p.relative_to(src)))
    for n in NAMES:
        results.append(fix(n, reg_trees))
    out = {"mode": "apply" if APPLY else "check", "stamp": STAMP,
           "backup_dir": str(BACKUPS) if APPLY else None, "results": results}
    print(json.dumps(out, indent=1, ensure_ascii=False))
    if APPLY:
        (BACKUPS / "manifest.json").write_text(json.dumps(out, indent=1, ensure_ascii=False),
                                               encoding="utf-8")

if __name__ == "__main__":
    main()
