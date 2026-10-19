#!/usr/bin/env python3
"""fix_fleet_kilocode.py — tulis KILOCODE_API_KEY ke .env SEMUA profil gsp-*.

Akar masalah (24-08-2026): `hermes -p gsp-* -z` memuat <profil>/.env dengan
override=True; env yang diwarisi proses (dari desktop) berisi KILOCODE_API_KEY
KOSONG, dan tidak ada profil yang mendefinisikan kunci di .env-nya sendiri →
"No usable credentials found for provider 'kilocode'".

Perbaikan: salin nilai KILOCODE_API_KEY dari HERMES_HOME/.env (kanonik) ke
<profil>/.env setiap profil gsp-*, PRESERVE baris lain (SEARXNG_URL,
FIRECRAWL_API_URL, dll). Idempotent — aman dijalankan berulang.

Usage: python fix_fleet_kilocode.py [--dry-run]
"""
import os
import re
import sys

HERMES_HOME = r"C:\Users\TRIAL\AppData\Local\hermes"
PROFILES_DIR = os.path.join(HERMES_HOME, "profiles")
KEY = "KILOCODE_API_KEY"


def parse_value(line: str) -> str:
    """Nilai setelah '=' pertama; buang satu lapis kutip di tepi."""
    v = line.split("=", 1)[1].strip()
    if len(v) >= 2 and ((v[0] == v[-1] == '"') or (v[0] == v[-1] == "'")):
        v = v[1:-1]
    return v


def read_home_key() -> str:
    txt = open(os.path.join(HERMES_HOME, ".env"), encoding="utf-8", errors="replace").read()
    for line in txt.splitlines():
        line = line.strip()
        if line.startswith(KEY + "="):
            return parse_value(line)
    raise SystemExit(f"FATAL: {KEY} tidak ditemukan di {HERMES_HOME}/.env")


def ensure_key_in_profile(profile: str, key_value: str, dry: bool) -> str:
    env_path = os.path.join(PROFILES_DIR, profile, ".env")
    lines = []
    if os.path.exists(env_path):
        lines = open(env_path, encoding="utf-8", errors="replace").read().splitlines()
    # Hapus baris KILOCODE_API_KEY lama (kosong/stale), pertahankan yang lain
    kept = []
    replaced = False
    for line in lines:
        if line.strip().startswith(KEY + "="):
            replaced = True
            continue
        kept.append(line)
    # Tambahkan kunci jika belum ada
    if not replaced:
        # pastikan ada newline sebelum baris baru jika file tidak kosong
        if kept and kept[-1].strip() != "":
            kept.append("")
    kept.append(f"{KEY}={key_value}")
    new_content = "\n".join(kept).rstrip("\n") + "\n"
    if dry:
        action = "ganti" if replaced else "tambah"
        return f"{profile}: [{action}] {KEY} length={len(key_value)}"
    with open(env_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)
    return f"{profile}: {'ganti' if replaced else 'tambah'} {KEY} length={len(key_value)}"


def main() -> None:
    dry = "--dry-run" in sys.argv
    key_value = read_home_key()
    if not key_value:
        raise SystemExit("FATAL: kunci kosong")
    profiles = sorted(d for d in os.listdir(PROFILES_DIR) if d.startswith("gsp-"))
    if not profiles:
        raise SystemExit("FATAL: tidak ada profil gsp-*")
    print(f"Kunci kanonik length={len(key_value)} | profil gsp-*: {len(profiles)} | dry={dry}")
    changed = 0
    for p in profiles:
        print(" ", ensure_key_in_profile(p, key_value, dry))
        changed += 1
    print(f"DONE: {changed}/{len(profiles)} profil diproses.")


if __name__ == "__main__":
    main()
