#!/usr/bin/env python3
# Pasang RULE RAIL-BUKTI-DUA-MODA ke SOUL.md: root (Swarm master) + semua profil.
# Direktif user 08-10-2026 ("Aplikasikan perbaikan ini pada disiplin... sehingga terus
# mengikuti aturan ini") atas vonis keluhan layout ADINPROP-1008 Rev A.
# Idempoten; guard identitas mengikuti pola install_ekas_index_rule_20261006.py.
import glob, io, os

BLOCK = """## RULE RAIL-BUKTI-DUA-MODA (WAJIB, kebijakan 08-10-2026; direktif user; marker RAIL-1008)
Setiap keluaran DOCX/PDF bergaya DATUM wajib memilih moda layout secara MEKANIS dari naskah (hitung sitasi per paragraf; bukan selera): MODA A bila ADA provenans per paragraf -> kolom teks 128 mm + rail bukti 32 mm (pgMar kanan 58 mm) dan rail WAJIB TERISI: tiap paragraf bersitasi mengangkat sitasinya menjadi chip rail (peran token evidence_rail; glif mark ikut naik; konten-kekal, pindah lapis bukan hilang), prosa badan bersih dari kurung sitasi (aparatus SUMBER figur/tabel/lampiran dikecualikan); rail kosong menyeluruh = cacat. MODA B bila TIDAK ADA provenans per paragraf -> margin kanan 20 mm, teks lebar penuh 166 mm; rail DILARANG dipesan-lalu-kosong (ruang dialokasikan untuk fungsi tak terpakai = cacat layout; preseden EKASLAP-1006, EOSADINT-RevB, ADINPROP-RevA: pgMar 58 mm dengan framePr=0). Gerbang ASSERT byte jadi (R-11.0, gagal = build exit nonzero): G-RAIL-1 jumlah framePr body == jumlah sitasi yang dipindah; G-RAIL-2 pola sitasi di w:t prosa badan == 0; G-RAIL-3 konsistensi dua-arah pgMar kanan 58 <=> chip>0 dan 20 <=> chip=0; pgSz A4 dan run badan 9,5 pt tidak berubah; register tersentuh = sha16 berubah = blokir. Mekanisme chip: pPr/w:framePr (w=1814 twips, anchorH=margin, offset x=7597, wrap=none) menempel paragraf host; tipografi dari tokens.json, DILARANG hardcode. Usulan tambalan instrumen datum_docx.rail_chip() + datum_lint G-RAIL lewat jalur defect->proposal gsp-skill-manager; sampai ditambal, gerbang jalan per-misi di ASSERT builder. Speks penuh: <ws>/docs/2026-10-08-adint-proposal-1008/SPEKS-RAIL-1008.md. Rollback: hapus blok antara heading ini dan baris marker RAIL-1008.

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
    if "RAIL-1008" in t:
        skipped.append(f); continue
    anchor = None
    for a in ("## RULE INDEKS-PENGETAHUAN", "## RULE PRESISI-HASIL",
              "## RULE PENCARIAN OFENSIF", "## GATE NATURALISASI",
              "## GATE ENFORCEMENT", "## Aturan Kerja", "## Memori & Dokumentasi"):
        if a in t:
            anchor = a; break
    try:
        if anchor:
            t = t.replace(anchor, BLOCK + anchor, 1)
        else:
            t = t.rstrip() + "\n\n" + BLOCK
        io.open(f, "w", encoding="utf-8", newline="\n").write(t)
        changed.append(f)
    except Exception as e:
        failed.append((f, "write: %s" % e))

print("CHANGED:", len(changed))
for f in changed[:6]: print("   ", f)
if len(changed) > 6: print("    ...")
print("SKIPPED (sudah ada):", len(skipped))
print("FAILED:", len(failed))
for f, e in failed: print("   FAIL", f, e)
