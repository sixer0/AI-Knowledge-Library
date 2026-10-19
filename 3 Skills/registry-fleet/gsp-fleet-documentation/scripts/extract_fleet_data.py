#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ekstraksi data fleet GSP dari sumber nyata → satu JSON + ringkasan.
Digunakan oleh skill gsp-fleet-documentation sebagai langkah data-gathering
sebelum generator dokumen. Baca: manifest.json, SOUL.md per profil, ROSTER
dashboard route.ts, dan frontmatter SKILL.md kanonik.

Usage:
    python3 extract_fleet_data.py [--manifest PATH] [--profiles-dir PATH]
        [--roster PATH] [--skills-dir PATH] [--out PATH]
Default: jalur kanonik GSP (~/workspace/gsp-hermes, ~/.hermes/profiles,
         ~/gsp-agent-headquarter/src/app/api/agents/route.ts, out=/tmp/gsp-extract/data.json)
"""
import argparse, json, os, re
from collections import Counter

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=os.path.expanduser("~/workspace/gsp-hermes/manifest.json"))
    ap.add_argument("--profiles-dir", default=os.path.expanduser("~/.hermes/profiles"))
    ap.add_argument("--roster", default=os.path.expanduser("~/gsp-agent-headquarter/src/app/api/agents/route.ts"))
    ap.add_argument("--skills-dir", default=os.path.expanduser("~/workspace/gsp-hermes/skills"))
    ap.add_argument("--out", default="/tmp/gsp-extract/data.json")
    return ap.parse_args()

def main():
    args = parse_args()
    data = {}

    # 1) Manifest (source of truth)
    with open(args.manifest) as f:
        manifest = json.load(f)
    data["model_text"] = manifest.get("model_text")
    data["model_vision"] = manifest.get("model_vision")
    data["provider"] = manifest.get("provider")
    data["base_url"] = manifest.get("base_url")
    profiles = []
    for gname, g in manifest.get("groups", {}).items():
        for p in g.get("profiles", []):
            p = dict(p)
            p["group"] = gname
            p["group_label"] = g.get("label")
            profiles.append(p)
    data["profiles"] = profiles

    # 2) SOUL.md — ringkasan persona per profil (4000 char awal cukup untuk parser)
    souls = {}
    for pid in [p["id"] for p in profiles]:
        sp = os.path.join(args.profiles_dir, pid, "SOUL.md")
        souls[pid] = open(sp).read()[:4000] if os.path.exists(sp) else ""
    data["souls"] = souls

    # 3) ROSTER HQ (route.ts statis) — parse blok entri
    roster = []
    if os.path.exists(args.roster):
        rt = open(args.roster).read()
        pat = re.compile(
            r"\{\s*id:\s*[\"']([^\"']+)[\"'][^{}]*?profile:\s*[\"']([^\"']+)[\"'][^{}]*?"
            r"name:\s*[\"']([^\"']*)[\"'][^{}]*?emoji:\s*[\"']([^\"']*)[\"'][^{}]*?"
            r"role:\s*[\"']([^\"']*)[\"'][^{}]*?model:\s*[\"']([^\"']*)[\"'][^{}]*?"
            r"level:\s*([0-9]+)[^{}]*?group:\s*[\"']([^\"']*)[\"']", re.S)
        for m in pat.finditer(rt):
            roster.append({"id": m.group(1), "profile": m.group(2), "name": m.group(3),
                           "emoji": m.group(4), "role": m.group(5), "model": m.group(6),
                           "level": int(m.group(7)), "group": m.group(8)})
    data["roster"] = roster

    # 4) Skill kanonik: deskripsi frontmatter + aset
    skills = []
    for d in sorted(os.listdir(args.skills_dir)):
        sp = os.path.join(args.skills_dir, d, "SKILL.md")
        if not os.path.exists(sp):
            continue
        head = open(sp).read(4000)
        m = re.search(r"^description:\s*[\"']?(.*?)[\"']?\s*$", head, re.M)
        desc = m.group(1).strip() if m else ""
        sub = os.listdir(os.path.join(args.skills_dir, d))
        has = {k: any(os.path.basename(x).startswith(k) for x in sub)
               for k in ["scripts", "templates", "references", "assets"]}
        skills.append({"name": d, "desc": desc, "has": has})
    data["skills"] = skills

    data["installed_profiles"] = sorted(x for x in os.listdir(args.profiles_dir) if x.startswith("gsp-"))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)

    # Ringkasan untuk verifikasi silang
    roster_profiles = {r["profile"] for r in roster if r["profile"] != "default"}
    print(f"profiles(manifest): {len(profiles)} | roster HQ: {len(roster)} | skills kanonik: {len(skills)} | installed: {len(data['installed_profiles'])}")
    print("group:", dict(Counter(p["group"] for p in profiles)))
    print("model:", dict(Counter(p["model"] for p in profiles)))
    print("missing SOUL:", [p["id"] for p in profiles if not souls.get(p["id"])])
    print("profil tanpa roster:", [p["id"] for p in profiles if p["id"] not in roster_profiles])
    print("saved:", args.out, os.path.getsize(args.out), "bytes")

if __name__ == "__main__":
    main()
