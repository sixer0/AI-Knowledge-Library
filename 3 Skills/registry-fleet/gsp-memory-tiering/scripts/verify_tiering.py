#!/usr/bin/env python
"""Verifikasi deterministik kompresi L0 (gsp-memory-tiering).

Pakai: uv run --python 3.11 python verify_tiering.py [profil]   (default: gsp-master)
Cek  : 1) usage L0 + PINNED posisi 1; 2) setiap rujukan `...md#anchor` di L0 punya
       `## #anchor` di file refs-nya; 3) setiap entri L0 non-PINNED adalah pointer
       (memuat 'memory/refs/'); 4) file refs terdaftar di _INDEX.md.
Exit 0 = semua hijau; non-zero = ada temuan (cetak DAFTAR, bukan hanya ringkas).
"""
import io, os, re, sys

profil = sys.argv[1] if len(sys.argv) > 1 else "gsp-master"
local = os.environ.get("LOCALAPPDATA", "")
mem_p = f"{local}/hermes/profiles/{profil}/memories/MEMORY.md"
if not os.path.isfile(mem_p):  # profil default
    mem_p = f"{local}/hermes/memories/MEMORY.md"
REFS_ROOT = "C:/Users/TRIAL/workspace/gsp-hermes/workspace/memory/refs"

mem = io.open(mem_p, encoding="utf-8").read()
entries = [e.strip() for e in mem.split("\u00a7") if e.strip()]
fails = []

print(f"L0 {profil}: {len(mem)} char ({len(mem)*100//15000}% dari 15000), {len(entries)} entri")
if not entries or not entries[0].startswith("ATURAN MEMORY MANAGEMENT (PINNED"):
    fails.append("PINNED tidak di posisi 1 / hilang")
if len(mem) > 7500:
    print("WARN: usage > 50% target tiering")

for i, e in enumerate(entries[1:], 2):
    if "memory/refs/" not in e:
        fails.append(f"entri #{i} bukan pointer ke refs: {e[:60]}")

cache = {}
for path, anchor in re.findall(r"memory/refs/([\w/\-.]+\.md)#([a-z0-9-]+)", mem):
    full = f"{REFS_ROOT}/{path}"
    if full not in cache:
        cache[full] = io.open(full, encoding="utf-8").read() if os.path.isfile(full) else None
    if cache[full] is None:
        fails.append(f"file refs tidak ada: {path}")
    elif f"## #{anchor}" not in cache[full]:
        fails.append(f"anchor '{anchor}' tidak ada di {path}")

idx = io.open(f"{REFS_ROOT}/_INDEX.md", encoding="utf-8").read()
for path in {m.split("#")[0] for m in re.findall(r"memory/refs/([\w/\-.]+\.md)(?:#[a-z0-9-]+)?", mem)}:
    if path not in idx:
        fails.append(f"{path} tidak terdaftar di _INDEX.md")

if fails:
    print("FAIL:")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("PASS: PINNED utuh, semua entri pointer, anchor cocok, index lengkap")
