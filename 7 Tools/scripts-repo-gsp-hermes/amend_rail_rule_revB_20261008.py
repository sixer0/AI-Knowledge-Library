#!/usr/bin/env python3
# Amandemen rev B RULE RAIL-BUKTI-DUA-MODA (RAIL-1008) pada SOUL fleet.
# Putusan user 08-10 ronde-2: (1) header/footer WAJIB full-span; (2) rail hanya
# bila kolom provenans benar-benar dipakai - halaman/paragraf tanpa provenans
# teks PENUH, tanpa ruang kosong; mekanisme berpindah dari margin-58mm ke
# per-paragraf (rail_host/rail_chip datum-house-style v2.1.0).
# Idempoten: ganti blok rev A dengan rev B; skip bila rev B sudah terpasang.
import glob, io, os, re

OLD_MARK = "## RULE RAIL-BUKTI-DUA-MODA"
NEW_MARK = "rev B"

BLOCK = """## RULE RAIL-BUKTI-DUA-MODA rev B (WAJIB, kebijakan 08-10-2026; direktif user; marker RAIL-1008)
Setiap keluaran DOCX/PDF bergaya DATUM memilih moda layout MEKANIS dari naskah (hitung sitasi per paragraf; bukan selera), dengan dua kekekalan dasar hasil amandemen rev B (putusan user 08-10 ronde-2): (K1) HEADER, FOOTER, dan garis krom HALAMAN PENUH (166 mm, margin fisik kanan = outer_margin 20 mm) pada SEMUA moda - krom tidak pernah dipangkas mengikuti rail; (K2) RAIL BUKTI = PROPERTI PER-PARAGRAF, bukan margin halaman: hanya paragraf yang benar-benar berprovenans menyempit sendiri ke kolom 128 mm (w:ind right 38 mm, helper DatumDocx.rail_host) dan mengangkat sitasinya menjadi chip rail (framePr w=1814 twips anchorH=margin offset x=7597 wrap=none yAlign=auto, peran token evidence_rail, konten-kekal); paragraf dan halaman TANPA provenans memakai teks PENUH 166 mm - ruang kosong yang dialokasikan untuk fungsi tak terpakai DILARANG di mana pun. MODA A = ada provenans per paragraf (campuran: tiap paragraf memilih sendiri); MODA B = tidak ada provenans (semua penuh). Pemilihan mekanis: builder hitung sitasi per paragraf. Gerbang ASSERT byte jadi (gagal = build exit nonzero): G-RAIL-1 jumlah framePr == jumlah sitasi pindah == manifest; G-RAIL-2 pola sitasi di w:t prosa == 0 (aparatus SUMBER figur/tabel/lampiran dikecualikan); G-RAIL-3 SEMUA pgMar kanan == outer_margin (20 mm) di semua seksi DAN tidak ada paragraf prosa melebar ke zona rail tanpa chip (host wajib ber-ind); chip tidak boleh duplikat identik dalam satu paragraf; pgSz A4 11906x16838 dan run badan 9,5 pt tidak berubah; sha16 register berubah = blokir. Mekanisme kanonis di datum-house-style v2.1.0 (rail_host/rail_chip; runtime-read tokens, nol hardcode) - builder DILARANG merakit framePr sendiri. Speks + sejarah amandemen: <ws>/docs/2026-10-08-adint-proposal-1008/SPEKS-RAIL-1008.md. Rollback: hapus blok antara heading ini dan baris marker RAIL-1008.

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
    if OLD_MARK not in t:
        failed.append((f, "blok rev A tidak ditemukan - tangani manual")); continue
    if NEW_MARK in t.split(OLD_MARK, 1)[1][:200]:
        skipped.append(f); continue
    # ganti blok rev A (dari heading sampai heading berikutnya / marker akhir)
    i = t.find(OLD_MARK)
    rest = t[i + len(OLD_MARK):]
    j = rest.find("\n## ")
    end = i + len(OLD_MARK) + (j if j >= 0 else len(rest))
    t2 = t[:i] + BLOCK + t[end:].lstrip("\n")
    if not t2.startswith(t[:i]):
        failed.append((f, "splice rusak")); continue
    try:
        io.open(f, "w", encoding="utf-8", newline="\n").write(t2)
        changed.append(f)
    except Exception as e:
        failed.append((f, "write: %s" % e))

print("CHANGED:", len(changed))
for f in changed[:5]: print("   ", f)
print("SKIPPED (rev B sudah ada):", len(skipped))
print("FAILED:", len(failed))
for f, e in failed[:8]: print("   FAIL", f, e)
