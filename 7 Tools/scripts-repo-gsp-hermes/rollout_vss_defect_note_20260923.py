#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sunting baris rute VSS di 54 MEMORY.md: tambah penanda known-defect EN62676
(VSSKB-0923 P-D, putusan controller 23-09 22:05). Idempoten: hanya menimpa baris
bertoken yang belum memuat 'defect62676'. Arsip pra-sunting sudah ada (rollout
21:05) -> arsip ulang dengan sufiks rev1 untuk jejak."""
import sys
from pathlib import Path

HERMES = Path(r"C:/Users/TRIAL/AppData/Local/hermes")
REFS = Path(r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/memory/refs")
MARK = "INDEX #vss-korpus"
ADD = " known-defect: pemetaan 4-nilai BS EN 62676 Tabel 7 BELUM TERKONFIRMASI thd PDF primer (objek IL vss-korpus-ekas-0923 \u00a74)."

targets = [p / "memories" / "MEMORY.md" for p in sorted((HERMES / "profiles").iterdir())
           if (p / "memories" / "MEMORY.md").exists()]
targets.append(HERMES / "memories" / "MEMORY.md")

apply = "--apply" in sys.argv
n_edit = n_skip = n_notok = 0
for t in targets:
    text = t.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    hit = False
    for i, ln in enumerate(lines):
        if MARK in ln:
            hit = True
            if "defect62676" in ln or "known-defect" in ln:
                n_skip += 1
            else:
                if apply:
                    prof = t.parent.parent.name if t.parent.parent.name != "hermes" else "default-profile"
                    ad = REFS / prof / "2026_09_23_arsip_memory_rev1_sebelum_defectnote.md"
                    ad.parent.mkdir(parents=True, exist_ok=True)
                    if not ad.exists():
                        ad.write_text("<!-- arsip pra-sunting rev1 (defect note) -->\n\n" + text, encoding="utf-8")
                    lines[i] = ln.rstrip() + ADD
                    t.write_text("\n".join(lines), encoding="utf-8")
                    assert "known-defect" in t.read_text(encoding="utf-8", errors="replace")
                n_edit += 1
            break
    if not hit:
        n_notok += 1
print(f"[{'APPLY' if apply else 'DRY'}] edit={n_edit} sudah={n_skip} tanpa_token={n_notok} total={len(targets)}")
