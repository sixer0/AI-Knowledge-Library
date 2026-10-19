# -*- coding: utf-8 -*-
"""Apply 'Fallback mandiri' block to all gsp-* profile SOUL.md files that lack it.
Byte-safe: preserves each file's original line endings (CRLF/LF).
Inserts after the line containing 'approve/reject' (end of the defect CHANGE REQUEST rule).
User-approved 2026-08-29 ("lanjutkan keduanya").
"""
import os

LOCALAPPDATA = os.environ.get("LOCALAPPDATA", r"C:\Users\TRIAL\AppData\Local")
PROFILES = os.path.join(LOCALAPPDATA, "hermes", "profiles")

FALLBACK_CONTENT = [
    "### Fallback mandiri (jika Skill Manager tidak dapat dihubungi / dispatch oneshot)",
    "Registry fleet adalah sumber tunggal skill on-demand: `$LOCALAPPDATA/hermes/skills/` (flat di `gsp/`,",
    "kategori lain di subfolder). Untuk memuat skill yang dibutuhkan TANPA menunggu Skill Manager:",
    "baca `SKILL.md` langsung dari fleet registry, lalu kerjakan sesuai isinya. Sertakan catatan",
    "request AWARENESS ke Skill Manager pada laporan (ROLE+TUGAS+SPEK) agar distribusi tetap tercatat.",
]

fixed, skipped, missing = [], [], []
for d in sorted(os.listdir(PROFILES)):
    p = os.path.join(PROFILES, d, "SOUL.md")
    if not (d.startswith("gsp-") and os.path.isfile(p)):
        continue
    raw = open(p, "rb").read()
    text = raw.decode("utf-8", errors="replace")
    if "Fallback mandiri" in text:
        skipped.append(d)
        continue
    if "approve/reject" not in text:
        missing.append(d + ":no-anchor")
        continue
    eol = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(eol)
    out, inserted = [], False
    for line in lines:
        out.append(line)
        if not inserted and "approve/reject" in line:
            out.append("")                     # blank separator
            out.extend(FALLBACK_CONTENT)       # block
            inserted = True
    if not inserted:
        missing.append(d + ":not-inserted")
        continue
    open(p, "wb").write(eol.join(out).encode("utf-8"))
    fixed.append(d)

print(f"fixed={len(fixed)} skipped_already={len(skipped)} missing={len(missing)}")
for m in missing:
    print("  MISSING:", m)
print("fixed_profiles:", ", ".join(fixed))
