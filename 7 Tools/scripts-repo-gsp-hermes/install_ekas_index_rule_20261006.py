#!/usr/bin/env python3
# Pasang RULE INDEKS-PENGETAHUAN ke SOUL.md: root (Swarm master) + semua profil.
# Direktif user 06-10-2026 ("Terapkan aturan ini") atas metode indexing EKASLAP-1006.
# Menimpa putusan butir-2 gsp-skill-manager (REJECT) secara sah: direktif user > preferensi manager;
# alasan Lean Fleet dihormati sebagian: blok ringkas, penegakan tetap lewat router/skill/registry.
# Idempoten; guard identitas mengikuti pola install_precision_result_rule_20260913.py.
import glob, io, os

BLOCK = """## RULE INDEKS-PENGETAHUAN (WAJIB, kebijakan 06-10-2026; direktif user; marker EKAS-IDX-1006)
Pengetahuan fleet disajikan dan diakses lewat STRUKTUR TERINDEKS yang dipanggil tugas, bukan dihafal mentah. Delapan sifat mengikat: (1) memori = jalur bukan muatan - indeks menunjuk sumber, tidak menyalin isi; (2) satuan indeks = unit pengetahuan berjenis besaran/ambang/metode/vonis/aturan, satu bab induk per unit, berkas boleh menghasilkan banyak unit; (3) sumbu organisasi = subsistem keputusan pembaca (bukan per-dokumen sumber); (4) pencocokan deterministik tanpa LLM - setiap hit bisa diperlihatkan token pemicunya; (5) daya-ikat (tingkat R) dan provenans (digest asal) menempel per baris indeks dan tidak boleh lepas saat unit dipanggil; (6) protokol muat tiga langkah: pemantik (L0/AGENTS.md) -> panggil indeks SEBELUM menjawab dari ingatan -> buka sumber sesuai beban (cepat = laporan sajian; mengikat = digest/REF/RANTAI via gerbang pustaka-teknis; per-baris = berkas kerja); (7) larangan: menjawab pertanyaan pengetahuan tanpa memanggil indeks lebih dulu, dan menjadikan baris indeks sebagai dasar kutipan final; (8) pin kesegaran pada setiap indeks (tanggal beku + prosedur cek DELTA bila sumber berubah + prosedur regenerasi). Berlaku fleet-wide: router kanonik gsp-ekas-knowledge-index (kanonik <ws>/gsp-hermes/skills/, registry fleet, mirror repo; kanal muat AWARENESS per putusan manager t_04a2b6db). Spesifikasi metode penuh + diagram: docs/2026-10-06_ekas-laporan-komprehensif/SPEKS-INDEKS-PENGETAHUAN.md. Rollback: hapus blok antara heading ini dan baris marker EKAS-IDX-1006.

"""

def target_files():
    home = os.path.expandvars(r"C:\\Users\\TRIAL\\AppData\\Local\\hermes")
    files = [os.path.join(home, "SOUL.md")]
    files += sorted(glob.glob(os.path.join(home, "profiles", "*", "SOUL.md")))
    return files

changed, skipped, failed = [], [], []
for f in target_files():
    try:
        t = io.open(f, encoding="utf-8").read()
    except Exception as e:
        failed.append((f, "read: %s" % e)); continue
    if "EKAS-IDX-1006" in t:
        skipped.append(f); continue
    anchor = None
    for a in ("## RULE PRESISI-HASIL", "## RULE PENCARIAN OFENSIF", "## GATE NATURALISASI", "## GATE ENFORCEMENT", "## Aturan Kerja", "## Memori & Dokumentasi"):
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
for c in changed[:6]: print("   ", c)
print("SKIPPED (sudah ada):", len(skipped))
print("FAILED:", len(failed))
for c in failed: print("   ", c)
