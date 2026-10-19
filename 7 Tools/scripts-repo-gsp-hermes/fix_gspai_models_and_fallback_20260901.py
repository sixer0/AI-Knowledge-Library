# -*- coding: utf-8 -*-
"""Remediasi fleet 2026-09-01: (1) ganti model basi auto-worker/auto-auxilary -> worker/worker-fast
di blok custom_providers GSP-AI; (2) tambah fallback kilocode z-ai/glm-5.3-flash setelah kilo-auto/free.
Byte-safe CRLF, backup, validasi yaml, idempoten. Usage: python fix.py [--apply]"""
import os, re, sys, shutil, io
import yaml

APPLY = "--apply" in sys.argv
HERMES = r"C:/Users/TRIAL/AppData/Local/hermes"
BACKUP = os.path.join(HERMES, "workspace_backups", "2026-09-01-gspai-models-fallback")
TARGETS = [os.path.join(HERMES, "config.yaml")] + sorted(
    os.path.join(HERMES, "profiles", p, "config.yaml")
    for p in os.listdir(os.path.join(HERMES, "profiles"))
    if os.path.isfile(os.path.join(HERMES, "profiles", p, "config.yaml"))
)

STALE = ("auto-worker", "auto-auxilary")
NEW_MODELS = ("worker", "worker-fast")
GLM = {"provider": "kilocode", "model": "z-ai/glm-5.3-flash"}

def norm(t):  # bytes -> str with \n
    return t.decode("utf-8").replace("\r\n", "\n")

def denorm(s, crlf):  # str -> bytes restoring EOL
    return (s.replace("\n", "\r\n") if crlf else s).encode("utf-8")

def fix_models_block(txt):
    """Within each custom_providers GSP-AI entry's models: block, drop stale keys, add NEW_MODELS."""
    lines = txt.split("\n")
    out, i, changed = [], 0, False
    while i < len(lines):
        ln = lines[i]
        # detect start of a models: block under a provider named GSP-AI
        if re.match(r"^    models:\s*$", ln):
            # look back for '- name: GSP-AI' within previous 6 lines
            back = "\n".join(lines[max(0, i - 6):i])
            block = []
            j = i + 1
            while j < len(lines) and re.match(r"^      \S", lines[j]):
                block.append(lines[j]); j += 1
            if "GSP-AI" in back:
                kept = [b for b in block if not re.match(r"^      (%s):" % "|".join(STALE), b)]
                have = {re.match(r"^      ([^:]+):", b).group(1) for b in kept if re.match(r"^      ([^:]+):", b)}
                added = []
                for m in NEW_MODELS:
                    if m not in have:
                        added.append("      %s: {}" % m)
                if added or len(kept) != len(block):
                    changed = True
                    out.append(ln)
                    out.extend(kept)
                    out.extend(added)
                else:
                    out.append(ln); out.extend(block)
            else:
                out.append(ln); out.extend(block)
            i = j
            continue
        out.append(ln); i += 1
    return "\n".join(out), changed

def fix_fallback(txt):
    """Append GLM entry after the kilocode kilo-auto/free fallback entry, if absent."""
    if re.search(r"z-ai/glm-5\.3-flash", txt):
        return txt, False
    m = re.search(r"^fallback_providers:\n((?:    .*\n|  - .*\n)+)", txt, re.M)
    if not m:
        return txt, None  # no block at all -> skip, report
    block = m.group(1)
    # find last entry line of the first list item; append new item after the block
    new_block = block.rstrip("\n") + "\n  - provider: %s\n    model: %s\n" % (GLM["provider"], GLM["model"])
    return txt[:m.start(1)] + new_block + txt[m.end(1):], True

report = []
for path in TARGETS:
    raw = open(path, "rb").read()
    crlf = b"\r\n" in raw
    txt = norm(raw)
    try:
        before = yaml.safe_load(txt)
    except Exception as e:
        report.append((path, "YAML-BEFORE-ERR", str(e)[:60])); continue
    t2, c1 = fix_models_block(txt)
    t3, c2 = fix_fallback(t2)
    status = []
    if c1: status.append("models")
    if c2 is True: status.append("fallback+")
    if c2 is None: status.append("NO_FALLBACK_BLOCK")
    if not status:
        report.append((path, "unchanged", "")); continue
    try:
        after = yaml.safe_load(t3)
    except Exception as e:
        report.append((path, "YAML-AFTER-ERR", str(e)[:80])); continue
    # sanity: model.default & provider unchanged; custom_providers count unchanged
    ok = (before.get("model", {}).get("default") == after.get("model", {}).get("default")
          and before.get("model", {}).get("provider") == after.get("model", {}).get("provider")
          and len(before.get("custom_providers", []) or []) == len(after.get("custom_providers", []) or []))
    if not ok:
        report.append((path, "REJECTED-sanity", "")); continue
    rel = os.path.relpath(path, HERMES)
    if APPLY:
        os.makedirs(os.path.join(BACKUP, os.path.dirname(rel)), exist_ok=True)
        shutil.copy2(path, os.path.join(BACKUP, rel))
        with open(path, "wb") as f:
            f.write(denorm(t3, crlf))
    report.append((path, ("APPLIED:" if APPLY else "DRY:") + "+".join(status), ""))

for p, s, e in report:
    if s != "unchanged" or "-ERR" in s or "REJECT" in s:
        print(f"{s:35s} {os.path.relpath(p, HERMES)} {e}")
n_applied = sum(1 for _, s, _ in report if ("APPLIED" in s or "DRY:" in s))
print(f"\n{'APPLIED' if APPLY else 'DRY-RUN'}: {n_applied} file diubah, {len(report)-n_applied} tidak berubah/error dari {len(TARGETS)} target")
