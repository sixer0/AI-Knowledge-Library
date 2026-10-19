#!/usr/bin/env python3
# Pasang RULE PENCARIAN OFENSIF ke SOUL.md: root (Swarm master) + semua profil.
# Idempoten; guard identitas (preseden insiden 21-08: penulis-ulang menghapus prefix identitas).
import glob, io, os, sys

BLOCK = """## RULE PENCARIAN OFENSIF (WAJIB, kebijakan 03-09-2026; direktif user)
Untuk tugas pencarian/akuisisi data: TARGET tetap, CARA fleksibel. Dilarang vonis "buntu/tidak tersedia/stuck" sebelum seluruh kelas jalur berikut dieksplorasi dan dibukukan (URL exact, status HTTP/error, timestamp):
1. Jalur resmi primer (direktori, endpoint/API via network log render, export resmi penyelenggara).
2. Variasi domain/subdomain dan SEMUA varian sitemap.
3. Probe platform/CMS (WP REST/custom post type, Next.js data, payload SPA).
4. Pencarian aktif multi-bahasa (kueri lokal + site: + frasa direktori; hasil 1-30; aggregator bertanda PROV).
5. Arsip (CDX per URL dan per domain, archive.today).
6. Dokumen resmi (rilis pers, katalog PDF, OCR).
7. Sosial/berita sebagai suplemen nama (bukan pengganti direktori).
8. Render browser interaktif pemburu endpoint XHR.
Aturan turun-temurun: vonis per-jalur tanpa akun = dianggap TIDAK dijalankan; CAPPED-with-evidence = permohonan PUTUSAN ke controller setelah 8 kelas terekap, bukan keputusan pekerja; budget/rate habis = partial-handoff checkpoint resume, bukan buntu; robots/named-agent block membatasi CARA (UA, jalur), bukan tujuan - hormati lalu cari jalur sah lainnya. Penutupan kartu akuisisi WAJIB menyertakan tabel LADDER (rung | URL/aksi | status+ts | hasil | keputusan lanjut). Controller menempelkan rujukan ini di setiap kartu pengumpulan; verifier/countersign menguji ladder table dan ketiadaan vonis tanpa akun. Rujukan penuh: skill gsp-orchestration-execution references/worker-offensive-logic.md.

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
    if "RULE PENCARIAN OFENSIF" in t:
        skipped.append(f); continue
    head = t[:3]
    anchor = None
    for a in ("## GATE NATURALISASI", "## GATE ENFORCEMENT", "## Aturan Kerja", "## Memori & Dokumentasi"):
        if a in t:
            anchor = a; break
    if anchor:
        t2 = t.replace(anchor, BLOCK + anchor, 1)
    else:
        t2 = t + BLOCK  # append murni (replace mengembalikan teks asli)
    # guard identitas: buktikan penyisipan murni -> menghapus blok mengembalikan teks asli persis
    if not (t2.startswith(t[:3]) and t2.replace(BLOCK, "", 1) == t):
        failed.append((f, "identity guard")); continue
    io.open(f, "w", encoding="utf-8", newline="").write(t2)
    changed.append(f)

print("CHANGED:", len(changed))
for c in changed[:6]: print("  ", c)
print("SKIPPED (sudah ada):", len(skipped))
print("FAILED:", len(failed))
for c in failed: print("  ", c)
