#!/usr/bin/env python3
"""fix_fleet_env.py — sinkronkan SEMUA env kredensial/setting kanonik ke .env semua profil gsp-*.

Sumber kebenaran: HERMES_HOME/.env (15 kunci: KILOCODE_API_KEY, GITHUB_TOKEN,
FIRECRAWL_API_URL, SEARXNG_URL, BROWSERBASE_*, TERMINAL_*, *_TOOLS_DEBUG,
TERMINAL_MODAL_IMAGE). Tiap profil gsp-* mendapat SALURAN LENGKAP dari kunci
tersebut; kunci lain yang sudah ada di .env profil (non-managed) dipertahankan.

Alasan (24-08-2026): dispatch/delegasi ber-profil gagal karena profil tidak punya
kredensial (KILOCODE_API_KEY) & env setting yang dibutuhkan; env warisan desktop
kosong. Dengan kunci di <profil>/.env, `hermes -p gsp-* -z` memuatnya (override=True)
dan SEMUA flow orkestrasi/dispatch bisa berjalan dari proses mana pun.

Usage: python fix_fleet_env.py [--dry-run] [--key KILOCODE_API_KEY,GITHUB_TOKEN]
"""
import os
import sys

HERMES_HOME = r"C:\Users\TRIAL\AppData\Local\hermes"
PROFILES_DIR = os.path.join(HERMES_HOME, "profiles")
MANAGE_SUFFIXES = ("_API_KEY", "_TOKEN", "_URL", "_TIMEOUT", "_LIFETIME_SECONDS",
                   "_DEBUG", "_STEALTH", "_PROXIES", "_MODAL_IMAGE", "_SESSION_TIMEOUT", "_INACTIVITY_TIMEOUT")


def parse_env(path):
    keys = {}
    if not os.path.exists(path):
        return keys
    for line in open(path, encoding="utf-8", errors="replace").read().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k = line.split("=", 1)[0].strip()
        v = line.split("=", 1)[1].strip()
        if len(v) >= 2 and ((v[0] == v[-1] == '"') or (v[0] == v[-1] == "'")):
            v = v[1:-1]
        keys[k] = v
    return keys


def canonical_keys(home_env):
    """Kunci home yang dikelola (kredensial/URL/setting), urut stabil."""
    order = ["KILOCODE_API_KEY", "GITHUB_TOKEN", "FIRECRAWL_API_URL", "SEARXNG_URL",
             "BROWSERBASE_ADVANCED_STEALTH", "BROWSERBASE_PROXIES",
             "BROWSER_INACTIVITY_TIMEOUT", "BROWSER_SESSION_TIMEOUT",
             "TERMINAL_LIFETIME_SECONDS", "TERMINAL_TIMEOUT", "TERMINAL_MODAL_IMAGE",
             "IMAGE_TOOLS_DEBUG", "MOA_TOOLS_DEBUG", "VISION_TOOLS_DEBUG", "WEB_TOOLS_DEBUG"]
    return [k for k in order if k in home_env]


def main():
    dry = "--dry-run" in sys.argv
    only = None
    for a in sys.argv:
        if a.startswith("--key="):
            only = set(a.split("=", 1)[1].split(","))
    home_env = parse_env(os.path.join(HERMES_HOME, ".env"))
    manage = canonical_keys(home_env)
    if only:
        manage = [k for k in manage if k in only]
    if not manage:
        raise SystemExit("FATAL: tidak ada kunci kanonik yang dikelola")
    profiles = sorted(d for d in os.listdir(PROFILES_DIR) if d.startswith("gsp-"))
    if not profiles:
        raise SystemExit("FATAL: tidak ada profil gsp-*")
    print(f"Kunci kanonik ({len(manage)}): {manage}")
    print(f"Profil gsp-*: {len(profiles)} | dry={dry}")
    ok = 0
    for p in profiles:
        env_path = os.path.join(PROFILES_DIR, p, ".env")
        cur = parse_env(env_path)
        lines = []
        if os.path.exists(env_path):
            lines = open(env_path, encoding="utf-8", errors="replace").read().splitlines()
        kept = []
        replaced = set()
        for line in lines:
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                kept.append(line)
                continue
            k = s.split("=", 1)[0].strip()
            if k in manage:
                replaced.add(k)
                continue  # akan ditulis ulang dengan nilai kanonik
            kept.append(line)
        # kunci managed yang belum ada
        missing = [k for k in manage if k not in replaced]
        # pastikan newline sebelum blok baru
        if kept and kept[-1].strip() != "":
            kept.append("")
        for k in manage:
            kept.append(f"{k}={home_env[k]}")
        new_content = "\n".join(kept).rstrip("\n") + "\n"
        if dry:
            print(f"  {p}: ganti {len(replaced)} | tambah {len(missing)} -> total {len(manage)} kunci")
            ok += 1
            continue
        with open(env_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)
        print(f"  {p}: ganti {len(replaced)} | tambah {len(missing)} -> total {len(manage)} kunci managed")
        ok += 1
    print(f"DONE: {ok}/{len(profiles)} profil diproses.")


if __name__ == "__main__":
    main()
