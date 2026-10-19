#!/usr/bin/env python3
"""cari_ekas.py — pemanggil indeks pengetahuan EKAS (skill gsp-ekas-knowledge-index).

Kasus pakai: tugas menyentuh topik teknik -> cari unit pengetahuan terkait SEBELUM
menjawab, lalu buka titik masuk yang ditunjuk (digest/rak/laporan). Deterministik,
tanpa LLM. Stdlib saja.

Contoh:
  python cari_ekas.py "loss budget konektor"
  python cari_ekas.py --bab C3 "PoE"
  python cari_ekas.py --domain FIBER-OPTIC
  python cari_ekas.py --unit U-0770
  python cari_ekas.py --kemampuan "defleksi balok"     # hanya indeks kemampuan
Mode campuran (default): kueri bebas mencari di INDEKS-UNIT dan INDEKS-KEMAMPUAN
sekaligus; tiap hasil berlabel jenisnya. Daya-ikat kemampuan: lahir
pending_verification / draft-tidak-terverifikasi-insan (P-5, sign-off 0/332).
"""
import argparse
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "references")
INV = os.path.join(REF, "INDEKS-UNIT.csv")
KAP = os.path.join(REF, "INDEKS-KEMAMPUAN.csv")
DOM = os.path.join(REF, "PETA-DOMAIN.csv")

STOP = {"yang", "dengan", "untuk", "pada", "dalam", "dari", "atau", "tidak", "ada",
        "ini", "itu", "agar", "sebagai", "secara", "telah", "akan", "sudah", "bisa",
        "harus", "hanya", "juga", "oleh", "karena", "setiap", "antara", "atas", "bagi"}


def load(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="|"))


def tokens(q):
    return [t for t in re.findall(r"[a-zà-ÿ0-9\-\.]{3,}", q.lower()) if t not in STOP]


def load_optional(path):
    if not os.path.isfile(path):
        return []
    return load(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?", default="")
    ap.add_argument("--bab")
    ap.add_argument("--domain")
    ap.add_argument("--unit")
    ap.add_argument("--jenis")
    ap.add_argument("--kemampuan", nargs="?", const="", default=None,
                    metavar="KATA-KUNCI",
                    help="hanya indeks kemampuan (INDEKS-KEMAMPUAN.csv)")
    ap.add_argument("--limit", type=int, default=15)
    a = ap.parse_args()

    inv = load(INV)
    kap = load_optional(KAP)

    if a.unit:
        for r in inv + kap:
            if r["unit_id"] == a.unit:
                extra = ""
                if r.get("signoff_status"):
                    extra = f" | signoff={r['signoff_status']}"
                print(f"UNIT {r['unit_id']} | {r['jenis']} | bab/domain {r.get('bab') or r.get('domain')} | R={r['R']}{extra}")
                print(f"  ringkas : {r['ringkas']}")
                print(f"  digest  : {r['digest'] or '(lihat PETA-DOMAIN)'}")
                return 0
        print(f"unit {a.unit} tidak ada di indeks", file=sys.stderr)
        return 1

    if a.domain:
        d = a.domain.upper()
        for r in load(DOM):
            if r["domain"] == d:
                print(f"DOMAIN {d} | rantai_jaminan={r['rantai']} | berkas_rak={r['berkas_rak']}")
                print(f"  titik masuk rak    : ekas/05_DOMAIN-KNOWLEDGE/{d}/")
                if r["rantai"] == "ADA":
                    print(f"  rantai jaminan     : ekas/05_DOMAIN-KNOWLEDGE/{d}/RANTAI-JAMINAN.md")
                if r["digest"]:
                    print(f"  digest terverifikasi: {r['digest']}")
                print(f"  laporan (sajian utuh): docs/2026-10-06_ekas-laporan-komprehensif/output/EKASLAP-1006-Laporan-Komprehensif.docx")
                hits = [r2 for r2 in inv if d.replace("-", "") in (r2["kw"] + r2["digest"]).lower().replace("-", "")]
                if hits:
                    print(f"  unit terkait (contoh {min(5,len(hits))}):")
                    for h in hits[:5]:
                        print(f"   - {h['unit_id']} [{h['bab']}/{h['jenis']}/R={h['R']}] {h['ringkas'][:90]}")
                kh = [k for k in kap if k["domain"] == d]
                if kh:
                    kp = f"ekas/05_DOMAIN-KNOWLEDGE/{d}/KEMAMPUAN.md"
                    print(f"  kemampuan domain ini: {len(kh)} unit -> digest {kp if os.path.isfile(os.path.join(os.environ.get('GSP_WS', 'C:/Users/TRIAL/workspace/gsp-hermes/workspace'), kp)) else '(belum dibuat)'}")
                    for h in kh[:5]:
                        print(f"   - {h['unit_id']} [kemampuan/R={h['R']}] {h['ringkas'][:90]}")
                return 0
        # domain baru hasil W2 belum tentu ada di PETA-DOMAIN lama; fallback indeks kemampuan
        kh = [k for k in kap if k["domain"] == a.domain.upper()]
        if kh:
            d = a.domain.upper()
            print(f"DOMAIN {d} | (tidak terdaftar di PETA-DOMAIN lama) | kemampuan={len(kh)}")
            print(f"  titik masuk rak: ekas/05_DOMAIN-KNOWLEDGE/{d}/")
            for h in kh[:5]:
                print(f"   - {h['unit_id']} [kemampuan/R={h['R']}] {h['ringkas'][:90]}")
            return 0
        print(f"domain {a.domain} tidak dikenal; lihat PETA-DOMAIN.csv", file=sys.stderr)
        return 1

    # mode kemampuan saja
    if a.kemampuan is not None:
        q = a.kemampuan or a.query
        if not q:
            print("perlu kata kunci setelah --kemampuan", file=sys.stderr)
            return 2
        scored = []
        qs = tokens(q)
        for r in kap:
            hay = r["kw"] + " " + r["ringkas"].lower()
            s = sum(2 if t in hay else 0 for t in qs)
            if qs and s == 0:
                continue
            if not qs:
                s = 1
            scored.append((s, r))
        scored.sort(key=lambda x: (-x[0], x[1]["unit_id"]))
        n = 0
        for s, r in scored[: a.limit]:
            print(f"[{s}] {r['unit_id']} | kemampuan | domain {r['domain']} | R={r['R']} | {r['ringkas'][:100]}")
            print(f"     digest  : {r['digest']}")
            print(f"     daya-ikat: {r['authority_status']} / {r['signoff_status']}")
            n += 1
        print(f"--- {n} kemampuan dari {len(kap)} unit (indeks 09-10; angka paket BELUM sah jadi ambang terima)")
        return 0

    if not a.query and not a.bab:
        print("perlu query, --domain, --unit, --bab, atau --kemampuan", file=sys.stderr)
        return 2

    qs = tokens(a.query)
    scored = []
    for r in inv:
        if a.bab and r["bab"] != a.bab:
            continue
        if a.jenis and r["jenis"] != a.jenis:
            continue
        hay = (r["kw"] + " " + r["ringkas"].lower())
        s = sum(2 if t in hay else 0 for t in qs)
        if qs and s == 0:
            continue
        if not qs:
            s = 1
        scored.append((s, r["unit_id"], r, "unit"))
    for r in kap:
        if a.bab:
            continue
        if a.jenis and a.jenis != "kemampuan":
            continue
        hay = (r["kw"] + " " + r["ringkas"].lower())
        s = sum(2 if t in hay else 0 for t in qs)
        if qs and s == 0:
            continue
        if not qs:
            s = 1
        scored.append((s, r["unit_id"], r, "kap"))
    scored.sort(key=lambda x: (-x[0], x[1]))
    n = 0
    for s, _, r, kind in scored[: a.limit]:
        tag = "UNIT" if kind == "unit" else "KEMAMPUAN"
        loc = r.get("bab") or r.get("domain")
        print(f"[{s}] {tag} {r['unit_id']} | {loc} | {r['jenis']} | R={r['R']} | {r['ringkas'][:100]}")
        print(f"     digest: {r['digest'] or '(via PETA-DOMAIN/laporan)'}")
        n += 1
    print(f"--- {n} hasil dari {len(inv)} unit + {len(kap)} kemampuan (indeks 06-10/09-10; bila rak berubah, jalankan cek kesegaran dulu)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
