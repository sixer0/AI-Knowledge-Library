# Remediasi INV-7 user01 (kartu t_5c69d7a9): marker .no-bundled-skills + hapus bundled re-seed.
# Idempoten, arsip lossless ber-sha256 SEBELUM hapus, tidak menyentuh SOUL.md/.lean-policy/config.
# Target marker: user01 (kasus nyata) + agentriset/firmanhidayat/novriandy (controller lean tanpa
# marker, pencegahan re-seed berikutnya). Hapus bundled: hanya user01, hanya file yang sha256-nya
# IDENTIK dengan fleet home $LOCALAPPDATA/hermes/skills (duplikat); file unik DIPERTAHANKAN.
import os, sys, json, hashlib, shutil, argparse
from datetime import datetime

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
PROF = os.path.join(HOME, "profiles")
FLEET = os.path.join(HOME, "skills")
WS = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace"
ARCHIVE = os.path.join(WS, "memory", "refs", "archive", "lean-bundled-user01-2026_09_02")
MARKER = ".no-bundled-skills"
MARKER_PROFILES = ["user01", "agentriset", "firmanhidayat", "novriandy"]
PRUNE_PROFILE = "user01"
BUNDLED_TREES = ["apple", "autonomous-ai-agents", "creative", "email", "github", "media",
                 "mlops", "note-taking", "productivity", "research", "smart-home", "social-media"]
PROTECTED = {"gsp-orchestrator-worker", "gsp-orchestration-execution",
             "gsp-verification-before-completion"}

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="hanya audit, tanpa tulis/hapus")
    args = ap.parse_args()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    manifest_path = os.path.join(ARCHIVE, "_manifest.json")
    report = {"ts": ts, "markers": {}, "prune": {}, "kept_unique": [], "errors": []}
    changed = 0

    # 1) Marker di root profil (mekanisme resmi tools/skills_sync.py)
    for name in MARKER_PROFILES:
        pdir = os.path.join(PROF, name)
        if not os.path.isdir(pdir):
            report["markers"][name] = "SKIP (profil tidak ada)"
            continue
        mk = os.path.join(pdir, MARKER)
        if os.path.isfile(mk):
            report["markers"][name] = "sudah ada (skip)"
            continue
        report["markers"][name] = "DITULIS" if not args.check else "akan ditulis"
        if not args.check:
            with open(mk, "w", encoding="utf-8") as f:
                f.write(f"opt-out bundled skills seed; kartu t_5c69d7a9 {datetime.now().isoformat()}\n")
            if not os.path.isfile(mk):
                report["errors"].append(f"marker gagal tertulis di {name}")
            changed += 1

    # 2) Arsip + hapus bundled tree user01 (hanya yang identik fleet home)
    sd = os.path.join(PROF, PRUNE_PROFILE, "skills")
    fleet_idx = {}
    for root, dirs, files in os.walk(FLEET):
        for fn in files:
            fp = os.path.join(root, fn)
            fleet_idx[os.path.relpath(fp, FLEET).replace("\\", "/")] = sha256_file(fp)

    existing_trees = [t for t in BUNDLED_TREES if os.path.isdir(os.path.join(sd, t))]
    if existing_trees:
        # kumpulkan entri + verifikasi dup
        to_archive, keep_files = [], []
        for tree in existing_trees:
            tdir = os.path.join(sd, tree)
            for root, dirs, files in os.walk(tdir):
                for fn in files:
                    fp = os.path.join(root, fn)
                    rel = os.path.relpath(fp, sd).replace("\\", "/")
                    h = sha256_file(fp)
                    if fleet_idx.get(rel) == h:
                        to_archive.append((rel, fp, h))
                    else:
                        keep_files.append(rel)
        report["prune"]["identik_fleet"] = len(to_archive)
        report["kept_unique"] = keep_files
        if keep_files:
            report["errors"].append("ADA file unik dalam tree bundled - tidak dihapus, perlu review")

        if to_archive and not args.check:
            os.makedirs(ARCHIVE, exist_ok=True)
            # arsip verbatim dulu (lossless), lalu verifikasi sha256 salinan
            man = {"card": "t_5c69d7a9", "ts": ts, "profile": PRUNE_PROFILE,
                   "archive_root": ARCHIVE, "files": []}
            for rel, fp, h in to_archive:
                dst = os.path.join(ARCHIVE, PRUNE_PROFILE, rel.replace("/", os.sep))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(fp, dst)
                h2 = sha256_file(dst)
                if h2 != h:
                    report["errors"].append(f"arsip rusak sha mismatch: {rel}")
                    continue
                man["files"].append({"rel": rel, "sha256": h, "size": os.path.getsize(fp)})
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(man, f, indent=1, ensure_ascii=False)
            # hapus hanya jika arsip terverifikasi penuh
            if not report["errors"]:
                for tree in existing_trees:
                    tdir = os.path.join(sd, tree)
                    uniq = [r for r in keep_files if r.split("/")[0] == tree]
                    if uniq:
                        continue  # tree mengandung file unik -> jangan sentuh
                    shutil.rmtree(tdir)
                    report["prune"].setdefault("removed_trees", []).append(tree)
                changed += len(report["prune"].get("removed_trees", []))
            # verifikasi pasca-hapus
            still = [t for t in BUNDLED_TREES if os.path.isdir(os.path.join(sd, t))]
            report["prune"]["trees_remaining"] = still
    else:
        report["prune"]["status"] = "bersih (0 tree bundled)"

    # 3) Verifikasi akhir kondisi target
    have = sorted(e for e in os.listdir(sd) if os.path.isdir(os.path.join(sd, e)) and not e.startswith(".")) \
        if os.path.isdir(sd) else []
    report["final_user01_skills"] = have
    missing_protected = PROTECTED - set(have)
    if missing_protected:
        report["errors"].append(f"SKILL ALWAYS LOAD HILANG: {sorted(missing_protected)}")

    print(json.dumps(report, indent=1, ensure_ascii=False))
    if args.check:
        print(f"CHECK MODE | perubahan dibutuhkan: {changed > 0 or bool(existing_trees)}")
    else:
        print(f"EXIT_OK changed_units={changed} errors={len(report['errors'])}")
    return 1 if report["errors"] else 0

if __name__ == "__main__":
    sys.exit(main())
