#!/usr/bin/env python3
# NAT-S14: pasang ALWAYS LOAD `gsp-output-naturalization` + salinan fisik skill ke profil penulis.
# Idempoten: run kedua harus melapor 0 perubahan. Backup pra-edit SOUL ber-stempel waktu,
# disimpan DI LUAR kanban/workspaces (folder kontrak docs/). Copy selektif per komponen
# (tanpa copytree utuh) supaya __pycache__ tidak pernah ikut.
import hashlib
import os
import shutil
import sys
import time

FLEET = "C:/Users/TRIAL/AppData/Local/hermes/skills/gsp/gsp-output-naturalization"
PROFILES = "C:/Users/TRIAL/AppData/Local/hermes/profiles"
SKILL = "gsp-output-naturalization"
BACKUP_ROOT = ("C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/"
               "2026-09-02-naturalisasi-output")
TARGETS = [
    "gsp-document-writer",
    "gsp-pm-writer",
    "gsp-content-research-writer",  # diverifikasi nyata; boleh tidak ada di disk
    "gsp-custodian",
    "gsp-creative",
    "gsp-document-reviewer",
    "gsp-document-analyst",
    "gsp-document-translator",
    "gsp-document-converter",
]
MARKER = "- `gsp-output-naturalization`"
TS = time.strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = os.path.join(BACKUP_ROOT, f"backup_nat_s14_{TS}")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def fleet_files():
    out = []
    for root, dirs, files in os.walk(FLEET):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for fn in files:
            if fn == "__pycache__" or fn.endswith(".pyc"):
                continue
            full = os.path.join(root, fn)
            out.append(os.path.relpath(full, FLEET).replace("\\", "/"))
    return sorted(out)


def copy_skill(dst):
    """Copy selektif per komponen dari fleet ke dst (flat <dst>/SKILL.md)."""
    n = 0
    for rel in fleet_files():
        src = os.path.join(FLEET, rel)
        tgt = os.path.join(dst, rel)
        os.makedirs(os.path.dirname(tgt), exist_ok=True)
        if os.path.exists(tgt) and sha256(src) == sha256(tgt):
            continue
        shutil.copy2(src, tgt)
        n += 1
    return n


def soul_insert(soul_path, backup_dir):
    """Sisipkan MARKER di akhir daftar bullet seksi '## Skill — ALWAYS LOAD'.

    Return: 'skip' (sudah ada), 'inserted', atau 'no-section'.
    """
    with open(soul_path, encoding="utf-8") as f:
        text = f.read()
    lines = text.split("\n")
    try:
        start = next(i for i, l in enumerate(lines)
                     if l.startswith("## Skill") and "ALWAYS LOAD" in l)
    except StopIteration:
        start = None
    if start is None:
        # Profil tanpa seksi ALWAYS LOAD (mis. SOUL bahasa Inggris hasil kurasi lama):
        # buat seksi kompak sebelum blok GATE pertama. Header pakai tanda hubung biasa,
        # TIDAK menambah karakter em dash baru ke disk.
        gate = next((i for i, l in enumerate(lines) if l.startswith("## GATE")), None)
        if gate is None:
            return "no-section"
        block = [
            "## Skill - ALWAYS LOAD (wajib dimuat di awal sesi)",
            "Gunakan `skill_view(name=...)` untuk memuat skill berikut SEBELUM mulai bekerja:",
            MARKER,
            "",
        ]
        lines[gate:gate] = block
        with open(soul_path, "w", encoding="utf-8", newline="") as f:
            f.write("\n".join(lines))
        return "created-section"
    # cari batas seksi berikutnya
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    seg = lines[start:end]
    if any(MARKER in l for l in seg):
        return "skip"
    # sisip setelah bullet terakhir yang bersambung di seksi
    last_bullet = None
    for i in range(start + 1, end):
        if lines[i].startswith("- "):
            last_bullet = i
    if last_bullet is None:
        return "no-section"
    # backup pra-edit sudah dilakukan caller (main) dan diverifikasi sha256
    lines.insert(last_bullet + 1, MARKER)
    with open(soul_path, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines))
    return "inserted"


def main():
    missing_input = False
    if not os.path.isfile(os.path.join(FLEET, "SKILL.md")):
        print(f"BLOCKER: skill fleet tidak ada di {FLEET}")
        sys.exit(2)
    ff = fleet_files()
    print(f"Input fleet: {len(ff)} berkas, SKILL.md sha256 {sha256(os.path.join(FLEET, 'SKILL.md'))[:16]}...")

    os.makedirs(BACKUP_DIR, exist_ok=True)
    print(f"Backup dir (di luar kanban/workspaces): {BACKUP_DIR}")

    rows = []
    for prof in TARGETS:
        pdir = os.path.join(PROFILES, prof)
        if not os.path.isdir(pdir):
            rows.append((prof, "TIDAK ADA DI DISK", "-", "-"))
            print(f"[{prof}] dilewati: profil tidak ada di disk")
            continue
        soul = os.path.join(pdir, "SOUL.md")
        if not os.path.isfile(soul):
            rows.append((prof, "tanpa SOUL.md", "-", "-"))
            print(f"[{prof}] BLOCKER: SOUL.md tidak ada")
            missing_input = True
            continue
        # backup pra-edit hanya bila SOUL akan disentuh (belum berisi marker)
        with open(soul, encoding="utf-8") as f:
            already = MARKER in f.read()
        if not already:
            before = sha256(soul)
            shutil.copy2(soul, os.path.join(BACKUP_DIR, prof + "__SOUL.md"))
            bpath = os.path.join(BACKUP_DIR, prof + "__SOUL.md")
            if os.path.getsize(bpath) == 0 or sha256(bpath) != before:
                print(f"[{prof}] BLOCKER: backup pra-edit tidak terverifikasi")
                sys.exit(2)
        # 1) salinan fisik skill
        dst = os.path.join(pdir, "skills", SKILL)
        ncop = copy_skill(dst)
        # 2) SOUL ALWAYS LOAD
        res = soul_insert(soul, BACKUP_DIR)
        # 3) verifikasi hash salinan vs fleet
        ok = len(ff) > 0
        for rel in ff:
            a = os.path.join(FLEET, rel)
            b = os.path.join(dst, rel)
            if (not os.path.isfile(b)) or sha256(a) != sha256(b):
                ok = False
        print(f"[{prof}] salinan fisik: {'+' + str(ncop) + ' berkas baru/ganti' if ncop else 'sudah identik (skip)'}, "
              f"SOUL: {res}, hash==fleet: {'OK' if ok else 'BEDA'}")
        rows.append((prof, f"skill {'OK' if ok else 'BEDA'} ({ncop} berkas ditulis)", res, sha256(os.path.join(dst, 'SKILL.md'))[:16]))

    print("\n=== RINGKASAN ===")
    for r in rows:
        print(" | ".join(str(x) for x in r))
    if missing_input:
        sys.exit(2)
    print("OK: rollout selesai (idempoten; jalankan ulang untuk membuktikan 0 perubahan)")


if __name__ == "__main__":
    main()
