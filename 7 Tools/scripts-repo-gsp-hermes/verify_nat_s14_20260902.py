#!/usr/bin/env python3
# NAT-S14 verifier deterministik: cek per profil target — folder skill ada, SKILL.md
# readable, SOUL menyebut nama skill di ALWAYS LOAD, sha256 salinan == fleet, tanpa
# __pycache__, dan diff terhadap backup hanya menambah baris marker/seksi (tanpa
# karakter terlarang baru). Cetak CHECK n: PASS|FAIL + VERDICT akhir.
import hashlib
import os
import sys

FLEET = "C:/Users/TRIAL/AppData/Local/hermes/skills/gsp/gsp-output-naturalization"
PROFILES = "C:/Users/TRIAL/AppData/Local/hermes/profiles"
SKILL = "gsp-output-naturalization"
MARKER = "- `gsp-output-naturalization`"
BACKUP_RUN1 = ("C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/"
               "2026-09-02-naturalisasi-output/backup_nat_s14_20260902_121032")
TARGETS = ["gsp-document-writer", "gsp-pm-writer", "gsp-custodian", "gsp-creative",
           "gsp-document-reviewer", "gsp-document-analyst", "gsp-document-translator",
           "gsp-document-converter"]
FORBIDDEN = ("\u2014", "\u00b7")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def fleet_files():
    out = []
    for root, dirs, files in os.walk(FLEET):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for fn in files:
            if fn.endswith(".pyc"):
                continue
            out.append(os.path.relpath(os.path.join(root, fn), FLEET).replace("\\", "/"))
    return sorted(out)


results = []


def check(n, name, ok, detail=""):
    tag = "PASS" if ok else "FAIL"
    results.append(ok)
    print(f"CHECK {n}: {tag} - {name}" + (f" | {detail}" if detail else ""))


ff = fleet_files()
check(0, f"input fleet ada ({len(ff)} berkas)", len(ff) > 0 and os.path.isfile(os.path.join(FLEET, "SKILL.md")))

n = 1
for prof in TARGETS:
    dst = os.path.join(PROFILES, prof, "skills", SKILL)
    soul = os.path.join(PROFILES, prof, "SOUL.md")
    # a) folder + SKILL.md readable
    try:
        readable = len(open(os.path.join(dst, "SKILL.md"), encoding="utf-8").read(200)) > 0
    except Exception:
        readable = False
    check(n, f"{prof}: folder skill + SKILL.md readable", os.path.isdir(dst) and readable); n += 1
    # b) SOUL menyebut skill dalam seksi ALWAYS LOAD
    in_always, named = False, False
    try:
        lines = open(soul, encoding="utf-8").read().split("\n")
        start = next((i for i, l in enumerate(lines) if l.startswith("## Skill") and "ALWAYS LOAD" in l), None)
        if start is not None:
            end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
            seg = lines[start:end]
            in_always = any(MARKER in l for l in seg)
        named = any(SKILL in l for l in lines)
    except Exception:
        pass
    check(n, f"{prof}: SOUL menyebut {SKILL} di ALWAYS LOAD", in_always and named); n += 1
    # c) sha256 semua berkas salinan == fleet
    same = len(ff) > 0
    for rel in ff:
        b = os.path.join(dst, rel)
        if (not os.path.isfile(b)) or sha256(os.path.join(FLEET, rel)) != sha256(b):
            same = False
    check(n, f"{prof}: sha256 salinan == fleet ({len(ff)} berkas)", same); n += 1
    # d) tidak ada __pycache__/*.pyc ikut tersalin
    junk = [r for r, _, fs in os.walk(dst) for f in fs if f.endswith(".pyc")] + \
           [d for _, ds, _ in os.walk(dst) for d in ds if d == "__pycache__"]
    check(n, f"{prof}: tanpa __pycache__/.pyc", len(junk) == 0); n += 1
    # e) diff vs backup pra-edit: hanya penambahan baris yang memuat nama skill / header seksi baru
    bp = os.path.join(BACKUP_RUN1, prof + "__SOUL.md")
    if os.path.isfile(bp):
        import difflib
        old = open(bp, encoding="utf-8").read().split("\n")
        new = open(soul, encoding="utf-8").read().split("\n")
        added = [l for l in difflib.ndiff(old, new) if l.startswith("+ ") and l[2:].strip()]
        removed = [l for l in difflib.ndiff(old, new) if l.startswith("- ") and l[2:].strip()]
        clean_add = all((SKILL in l) or ("ALWAYS LOAD" in l) or ("skill_view" in l) for l in added)
        forbid_new = [ch for ch in FORBIDDEN for l in added if ch in l]
        check(n, f"{prof}: diff vs backup = hanya penambahan sah, tanpa karakter terlarang baru "
                 f"(+{len(added)} -{len(removed)})", clean_add and not removed and not forbid_new); n += 1
    else:
        check(n, f"{prof}: backup pra-edit tersedia", False, "backup run-1 tidak ditemukan"); n += 1

print(f"\nTOTAL: {sum(results)}/{len(results)} PASS")
print("VERDICT: " + ("PASS" if all(results) else "FAIL"))
sys.exit(0 if all(results) else 1)
