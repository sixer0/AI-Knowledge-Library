#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""style_metrics.py - pengukur gaya prosa deterministik (kanonis sejak GAYA-AHLI-1005).

Dipakai untuk baseline dokumen manusia DAN korpus keluaran GSP dengan SATU alat,
supaya angka antar-lajur riset sebanding.
Input : berkas .docx (paragraf + SEL TABEL diekstrak semua) atau .txt.
Output: JSON per dokumen ke stdout.
Deterministik: tanpa stempel waktu, tanpa acak. Deps: uv run --with python-docx.

Metrik kunci dan ambang empiris yang terbukti membedakan teks-AI vs manusia
(ukur 05-10, korpus GSP vs target):
  chains_ge4_comma_pct   : % kalimat dengan >=4 klausa bertumpuk. GSP DATUM=23% (cacat); manusia <10%.
  semicolon_per_1000w    : GSP DATUM=33 (cacat); manusia <10.
  yang_per_100w          : >2 = relativisasi bertumpuk.
  stddev_sent / p90_sent : ritme seragam (stddev kecil) = fingerprint mesin; p90>45 atau maks>80 = bertele.
  paras_gt150w           : paragraf raksasa.
  distinct_opener_ratio  : pembuka kalimat monoton = terasa AI.
PITFALL: sel tabel sering memuat bagian terburuk (identifier telanjang, rantai titik-koma).
Ekstraksi HANYA paragraf meremehkan cacat 2-4x — wajib sertakan tables.
"""
import json, re, statistics, sys

def extract(path):
    texts = []
    if path.endswith(".docx"):
        import docx
        d = docx.Document(path)
        texts = [p.text.strip() for p in d.paragraphs if p.text.strip()]
        for t in d.tables:
            for row in t.rows:
                for c in row.cells:
                    if c.text.strip():
                        texts.append(c.text.strip())
    else:
        texts = [l.strip() for l in open(path, encoding="utf-8") if l.strip()]
    return texts

def measure(texts):
    prose = [t for t in texts if len(t.split()) > 25]
    sents = [s.strip() for t in prose for s in re.split(r'(?<=[.!?])\s+', t) if len(s.split()) > 5]
    if not sents:
        return {"sentences": 0}
    lens = [len(s.split()) for s in sents]
    cc = [s.count(',') + s.count(';') for s in sents]
    totw = sum(lens)
    openers = [s.split()[0].lower().strip('",.:') for s in sents]
    pw = [len(t.split()) for t in prose]
    return {
        "paras_prose_gt25w": len(prose),
        "sentences": len(sents),
        "total_words_prose": totw,
        "mean_sent": round(statistics.mean(lens), 1),
        "stddev_sent": round(statistics.pstdev(lens), 1),
        "p90_sent": int(sorted(lens)[int(len(lens)*0.9)]),
        "max_sent": max(lens),
        "sents_gt45": sum(1 for l in lens if l > 45),
        "chains_ge4_comma_pct": round(100*sum(1 for c in cc if c >= 4)/len(cc), 1),
        "mean_clauses_per_sent": round(statistics.mean(cc), 2),
        "semicolon_per_1000w": round(1000*sum(t.count(';') for t in prose)/totw, 1),
        "yang_per_100w": round(100*sum(len(re.findall(r'\byang\b', s.lower())) for s in sents)/totw, 2),
        "distinct_opener_ratio": round(len(set(openers))/len(openers), 2),
        "mean_para_words": round(statistics.mean(pw), 1) if pw else 0,
        "paras_gt150w": sum(1 for p in pw if p > 150),
    }

if __name__ == "__main__":
    out = {}
    for p in sys.argv[1:]:
        out[p.replace("\\", "/").split("/")[-1]] = measure(extract(p))
    print(json.dumps(out, indent=1, ensure_ascii=False))
