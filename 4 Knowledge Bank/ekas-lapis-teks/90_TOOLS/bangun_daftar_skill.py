# -*- coding: utf-8 -*-
"""
BANGUN DAFTAR RUJUKAN UNTUK SKILL

Membangkitkan `pustaka-teknis/references/04-daftar-rujukan-lengkap.md` langsung dari
MASTER-REFERENCE-REGISTER.csv, sehingga daftar di skill tidak dapat menyimpang dari rak.

Jalankan ulang setiap kali register berubah.
"""
import io, os, sys, csv, glob, collections

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

EKAS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = r"C:\Users\gspen\.claude\skills\pustaka-teknis\references"
OUT = os.path.join(SKILL, "04-daftar-rujukan-lengkap.md")
NL = chr(10)

BOLEH = {
    "R1": u"✅ ya — mengikat",
    "R2": u"✅ ya bila diadopsi kontrak",
    "R3": u"⚠ hanya bila kontrak mengadopsinya",
    "R4": u"✅ wajib untuk angka produk",
    "R5": u"❌ tidak pernah",
}


def main():
    rows = list(csv.DictReader(io.open(
        os.path.join(EKAS, "02_REGISTERS", "MASTER-REFERENCE-REGISTER.csv"), encoding="utf-8")))
    rantai = {os.path.basename(os.path.dirname(p))
              for p in glob.glob(os.path.join(EKAS, "05_DOMAIN-KNOWLEDGE", "*", "RANTAI-JAMINAN.md"))}
    putus = {"GROUNDING-LIGHTNING", "CYBERSECURITY", "CIVIL-STRUCTURAL"}

    per_dom = collections.defaultdict(list)
    for r in rows:
        per_dom[r["domain"]].append(r)

    c = collections.Counter(r["r_level"] for r in rows)
    bagian = []
    bagian.append(u"""# 04 — Daftar rujukan lengkap

> **Dibangkitkan otomatis** dari `02_REGISTERS/MASTER-REFERENCE-REGISTER.csv` oleh
> `90_TOOLS/bangun_daftar_skill.py`. **Jangan disunting tangan** — suntingan akan hilang
> saat dibangun ulang, dan daftar yang disunting tangan akan menyimpang dari rak.

Berkas ini menjawab satu pertanyaan: **rak ini punya apa saja, dan masing-masing boleh
dipakai untuk apa.** Untuk pertanyaan "rumus apa di halaman berapa", lihat
`01-indeks-rumus.md`.

**Akar rak:** `C:\\Users\\gspen\\Videos\\Buku\\GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM\\`

## Sebaran

| Tingkat | Jumlah | Boleh jadi ambang terima? |
|---|---|---|""")
    for lv in ["R1", "R2", "R3", "R4", "R5"]:
        bagian.append(u"| **%s** | %d | %s |" % (lv, c[lv], BOLEH[lv]))
    berkas = len(glob.glob(os.path.join(EKAS, "03_SOURCE-VAULT", "**", "*.pdf"), recursive=True))
    bagian.append(u"""
**%d baris register menunjuk %d berkas PDF.** Angkanya berbeda dan itu disengaja:

- **REF-BAT-002 mewakili dua standar** — IEEE 1188-2005 dan IEC 62485-2 berbagi satu resume
  karena keduanya menjawab pertanyaan yang sama (baterai stasioner).
- **Enam baris `REF-OEM-*` mewakili 97 lembar data** — dokumen produk didaftar per **laci**,
  bukan per berkas. Mendaftar 97 lembar data satu per satu akan menenggelamkan register
  tanpa menambah kejelasan.

**R1 kosong.** Tidak ada satu pun regulasi Indonesia di rak — setiap pernyataan kepatuhan
hukum harus bersandar salinan yang diperoleh terpisah.

---
""" % (len(rows), berkas))

    for dom in sorted(per_dom):
        st = (u" · rantai **⚠ PUTUS**" if dom in putus else
              u" · rantai ✅" if dom in rantai else u" · **belum ada rantai**")
        bagian.append(u"## %s%s" % (dom, st) + NL)
        bagian.append(u"| ID | R | Rujukan | Status | Laci |")
        bagian.append(u"|---|---|---|---|---|")
        for r in sorted(per_dom[dom], key=lambda x: (x["r_level"], x["reference_id"])):
            laci = r["vault_path"].split("/")[-1]
            stat = {"ACTIVE": u"aktif", "ACTIVE_WITH_SCOPE_LIMITS": u"**terbatas**",
                    "POINTER_ONLY": u"**penunjuk**", "INTAKE_ONLY": u"**belum dinilai**"}.get(
                        r["authority_status"], r["authority_status"])
            bagian.append(u"| `%s` | %s | %s | %s | `%s` |" % (
                r["reference_id"], r["r_level"], r["title"][:70], stat, laci))
        bagian.append(u"")

    bagian.append(u"""---

## Cara memakai daftar ini

1. **Cari domainnya**, bukan judul bukunya — nama buku jarang diingat, domain selalu.
2. **Periksa kolom R.** Bila menjawab pertanyaan ambang, hanya R1/R2 (dan R4 untuk angka
   produk) yang sah berdiri sendiri.
3. **Periksa status rantai.** Domain bertanda **⚠ PUTUS** berarti ambangnya tidak ada di
   rak — nyatakan itu, jangan diisi.
4. **Buka kartunya** di `04_KNOWLEDGE-CARDS/<domain>/<ID>.md` untuk batas pemakaian,
   lalu resumenya di `05_DOMAIN-KNOWLEDGE/<domain>/` untuk isinya.

## Tiga rantai yang putus

| Rantai | Domain | Yang tidak ada |
|---|---|---|
| **D** | GROUNDING-LIGHTNING | Ambang resistansi pembumian — tidak ada R1/R2 |
| **J** | CYBERSECURITY | **Seluruh R1/R2**: UU ITE, Perban BSSN, ISO 27001, NIST SP 800-86, ISO 27037 |
| **K** | CIVIL-STRUCTURAL | Empat SNI struktur: 1726, 1727, 1729, 2847 |

Pada ketiganya, **metode tersedia tetapi ambang tidak**. Menghitung boleh; menyatakan lulus
tidak — kecuali lewat penetapan pemilik, adopsi kontrak, atau tanda tangan ahli bersertifikat.

> ⚠ **Rantai K punya batas tambahan.** Struktur yang gagal dapat menimpa orang. Melaporkan
> hasil tanpa pernyataan lulus **tidak sah** untuk menara atau dudukan di ketinggian —
> hanya adopsi standar lewat kontrak atau tanda tangan ahli yang berlaku.
""")

    io.open(OUT, "w", encoding="utf-8").write(NL.join(bagian))
    print("ditulis:", OUT)
    print("rujukan:", len(rows), "· domain:", len(per_dom),
          "· berantai:", len(rantai), "· putus:", len(putus))


if __name__ == "__main__":
    main()
