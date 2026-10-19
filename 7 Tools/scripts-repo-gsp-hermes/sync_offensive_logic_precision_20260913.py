#!/usr/bin/env python3
# Distribusi referensi worker-offensive-logic.md (versi ter-patch Floor legal-platform)
# dari salinan profil gsp-master01 -> registry fleet + semua profil + kanonik workspace.
# Pola mengikuti install_offensive_search_rule_20260903.py (direktif user 13-09: presisi+hasil).
import glob, hashlib, io, os, shutil

SRC = os.path.expandvars(r"C:\Users\TRIAL\AppData\Local\hermes\profiles\gsp-master01\skills\gsp-orchestration-execution\references\worker-offensive-logic.md")
content = io.open(SRC, encoding="utf-8").read()
assert "Floor legal-platform" in content, "sumber tidak berisi patch"
src_sha = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

targets = []
# fleet registry
targets.append(os.path.expandvars(r"C:\Users\TRIAL\AppData\Local\hermes\skills\gsp\gsp-orchestration-execution\references\worker-offensive-logic.md"))
# semua profil yang punya skill ini
targets += glob.glob(os.path.expandvars(r"C:\Users\TRIAL\AppData\Local\hermes\profiles\*\skills\gsp-orchestration-execution\references\worker-offensive-logic.md"))
# kanonik workspace (jika struktur refs ada)
canon = os.path.expandvars(r"C:\Users\TRIAL\workspace\gsp-hermes\skills\gsp-orchestration-execution\references\worker-offensive-logic.md")
if os.path.isdir(os.path.dirname(canon)):
    targets.append(canon)

changed, same, failed = [], [], []
for f in targets:
    try:
        cur = io.open(f, encoding="utf-8").read() if os.path.exists(f) else None
        if cur == content:
            same.append(f); continue
        io.open(f, "w", encoding="utf-8", newline="").write(content)
        chk = hashlib.sha256(io.open(f, encoding="utf-8").read().encode("utf-8")).hexdigest()[:16]
        (changed if chk == src_sha else failed).append(f)
    except Exception as e:
        failed.append((f, str(e)))

print("SRC sha16:", src_sha)
print("CHANGED:", len(changed))
print("SUDAH SAMA:", len(same))
print("FAILED:", len(failed))
for x in failed[:10]: print("  ", x)
