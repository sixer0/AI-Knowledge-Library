#!/usr/bin/env python3
# Pasang RULE PRESISI-HASIL ke SOUL.md: root (Swarm master) + semua profil (54).
# Direktif user 13-09-2026: hapus framing 'batas etika' dari operasi riset; presisi+hasil = ukuran kualitas.
# Idempoten; guard identitas mengikuti pola install_offensive_search_rule_20260903.py.
import glob, io, os

BLOCK = """## RULE PRESISI-HASIL (WAJIB, kebijakan 13-09-2026; direktif user; menggantikan 'batas etika' pada semua misi riset/pencarian)
Ukuran kualitas utama SETIAP pencarian/riset/akuisisi data: PRESISI (benar-terverifikasi per field sesuai SPK-002) dan HASIL (cakupan lengkap sampai vonis jenuh ber-angka). Dilarang memakai klausul 'batas etika' atau 'batas lingkup' karangan sendiri untuk menyempitkan cakupan, melewatkan rung tangga ofensif, atau memvonis buntu: klausul semacam itu yang muncul di kartu/ladder/artefak = cacat, verifier memvonis FAIL. Tema riset terbuka penuh tanpa disclaimer diri: kapabilitas produk, cara kerja sistem, penggunaan oleh institusi keamanan, studi kasus, tender, dokumentasi vendor, arsip. Floor legal-platform yang TIDAK disentuh kebijakan ini dan tidak pernah dilanggar: akses non-autorisasi, pencurian kredensial, penembusan paywall/DRM/login, penargetan individu tertentu untuk pengawasan. Kartu delegasi pencarian menempelkan rule ini + logika ofensif, BUKAN klausul etika. Rujukan: skill gsp-orchestration-execution references/worker-offensive-logic.md.

"""

def target_files():
    home = os.path.expandvars(r"C:\Users\TRIAL\AppData\Local\hermes")
    files = [os.path.join(home, "SOUL.md")]
    files += sorted(glob.glob(os.path.join(home, "profiles", "*", "SOUL.md")))
    return files

changed, skipped, failed = [], [], []
for f in target_files():
    try:
        t = io.open(f, encoding="utf-8").read()
    except Exception as e:
        failed.append((f, "read: %s" % e)); continue
    if "RULE PRESISI-HASIL" in t:
        skipped.append(f); continue
    anchor = None
    for a in ("## RULE PENCARIAN OFENSIF", "## GATE NATURALISASI", "## GATE ENFORCEMENT", "## Aturan Kerja", "## Memori & Dokumentasi"):
        if a in t:
            anchor = a; break
    if anchor:
        t2 = t.replace(anchor, BLOCK + anchor, 1)
    else:
        t2 = t + BLOCK
    if not (t2.replace(BLOCK, "", 1) == t):
        failed.append((f, "identity guard")); continue
    io.open(f, "w", encoding="utf-8", newline="").write(t2)
    changed.append(f)

print("CHANGED:", len(changed))
for c in changed[:8]: print("  ", c)
print("SKIPPED (sudah ada):", len(skipped))
print("FAILED:", len(failed))
for c in failed: print("  ", c)
