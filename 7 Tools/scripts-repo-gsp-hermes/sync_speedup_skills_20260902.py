# -*- coding: utf-8 -*-
"""Sinkron 2 skill yang di-patch EXPO-OPT: kanonik -> registry fleet -> salinan profil.
Verifikasi SHA256 cocok di semua tujuan. Pemakaian: uv run --python 3.11 python sync_speedup_skills_20260902.py
"""
import hashlib, io, os, shutil, sys

CANON = r"C:/Users/TRIAL/workspace/gsp-hermes/skills"
FLEET = os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", "skills", "gsp")
PROF_ROOT = r"C:/Users/TRIAL/AppData/Local/hermes/profiles"
SKILLS = ["gsp-orchestration-execution", "gsp-limit-aware-delegation"]

def sha(p):
    return hashlib.sha256(io.open(p, "rb").read()).hexdigest()[:12]

def tree_files(root):
    out = []
    for dp, _, fns in os.walk(root):
        for fn in fns:
            out.append(os.path.join(dp, fn))
    return out

def sync_dir(src, dst, label):
    n = 0
    for f in tree_files(src):
        rel = os.path.relpath(f, src)
        d = os.path.join(dst, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if not os.path.exists(d) or sha(f) != sha(d):
            shutil.copy2(f, d)
            n += 1
    return n

total_profiles = 0
for sk in SKILLS:
    c_src = os.path.join(CANON, sk)
    f_dst = os.path.join(FLEET, sk)
    changed = sync_dir(c_src, f_dst, "fleet")
    print(f"{sk}: fleet registry update={changed} file")
    # salinan profil
    cnt = 0
    for prof in sorted(os.listdir(PROF_ROOT)):
        p_sk = os.path.join(PROF_ROOT, prof, "skills", sk)
        if os.path.isdir(p_sk):
            ch = sync_dir(f_dst, p_sk, prof)
            if ch:
                cnt += 1
                total_profiles += 1
    print(f"{sk}: profil disinkron = {cnt}")
    # verifikasi
    bad = []
    if sha(os.path.join(c_src, "SKILL.md")) != sha(os.path.join(f_dst, "SKILL.md")):
        bad.append("fleet")
    for prof in sorted(os.listdir(PROF_ROOT)):
        p_md = os.path.join(PROF_ROOT, prof, "skills", sk, "SKILL.md")
        if os.path.exists(p_md) and sha(p_md) != sha(os.path.join(c_src, "SKILL.md")):
            bad.append(prof)
    print(f"{sk}: verifikasi SHA mismatches = {bad if bad else '0'}")
print("SELESAI. profil total berubah:", total_profiles)
