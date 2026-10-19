#!/usr/bin/env python3
"""Add ALWAYS LOAD + AWARENESS block to profiles lacking the section (generic Swarm SOULs)."""
import os

LOCALAPPDATA = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
PROFILES_DIR = os.path.join(LOCALAPPDATA, "hermes", "profiles")

AWARENESS = (
    "## Skill — ALWAYS LOAD (wajib dimuat di awal sesi)\n"
    "Gunakan `skill_view(name=...)` untuk memuat skill berikut SEBELUM mulai bekerja:\n"
    "- `gsp-verification-before-completion`\n\n"
    "## Skill — AWARENESS (muat saat diminta / pemicu cocok)\n"
    "Kamu tidak membawa semua skill on-demand secara fisik di profil. Jika tugas "
    "membutuhkan skill spesifik, BERITAHU Skill Manager (`gsp-skill-manager`) dengan format:\n"
    "- **Role:** <peran kamu>\n"
    "- **Tugas:** <deskripsi tugas>\n"
    "- **Skill yang dibutuhkan:** <nama skill spesifik>\n"
    "Skill Manager akan memberikan daftar skill yang harus kamu load + rekomendasi "
    "skill penunjang lain yang mungkin dibutuhkan untuk menunjang tugas. Setelah "
    "menerima daftar, muat via `skill_view(name=...)` dan kerjakan tugas.\n\n"
    "### Defect / Proposal Skill\n"
    "Jika saat menggunakan skill kamu menemukan defect:\n"
    "- **BUG** (reproducible): usulkan kepada `gsp-skill-manager` — manager menimbang "
    "dan menilai; jika benar bug → approve → `gsp-skill-creator` memperbaiki.\n"
    "- **CHANGE REQUEST**: usulkan dengan alasan relevansi terhadap seluruh workflow "
    "ekosistem; manager menimbang sebelum approve/reject.\n"
)

targets = {
    "gsp-budi": ["gsp-verification-before-completion"],
    "gsp-creative": ["gsp-verification-before-completion"],
    "gsp-firman-custom": ["gsp-verification-before-completion"],
}

for profile, always in targets.items():
    path = os.path.join(PROFILES_DIR, profile, "SOUL.md")
    with open(path, encoding="utf-8", errors="replace") as f:
        soul = f.read()
    # Append block at end (these are generic Swarm souls without skill sections)
    new_soul = soul.rstrip() + "\n\n" + AWARENESS
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_soul)
    print(profile, "OK")
