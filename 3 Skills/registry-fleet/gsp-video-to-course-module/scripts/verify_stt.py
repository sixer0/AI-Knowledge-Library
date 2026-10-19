#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STT-VER deterministic verification — misi STT-Hermes-Learning-Module (t_4f0be60b)
Read-only terhadap artefak misi; satu-satunya tulis = 90_meta/verification_report.md.
Check C0 (guard), AC1-AC10 (dari permintaan user asli 1..10), VERDICT akhir.
Pola fleet-scale: tiap check cetak 'CHECK n: PASS|FAIL|NEEDS_REVIEW — nama'.

VERSI: v2 (amandemen satu-jendela per 02_blueprint.md D3; v1 diarsipkan verify_stt_v1.py).
Delta v1->v2: (a) ambang kata AC1/AC9 >= 15.000 (RT K3; rasio 0,15 x 85.516 = 12.828);
(b) pesan detail disinkron ke kanon D1 (AC-M = poin user 1-10) dan D2 (label V2/V3 kanonis
_MANIFEST: V2=DYdvJCxWd6M Metics, V3=8yE6G1Lup1s Samin); (c) semantik check lain TIDAK diubah.
Setelah v2 ini jalan bersih -> FROZEN.
"""
import os, re, sys, hashlib, datetime

ROOT = "C:/Users/TRIAL/workspace/Test STT"
META = os.path.join(ROOT, "90_meta")
MOD_MD = os.path.join(ROOT, "05_module", "HERMES-ZERO-TO-HERO.md")
REPORT = os.path.join(META, "verification_report.md")

VIDS = {  # id -> (youtube id, expected transcript file)  [KANON D2/_MANIFEST; verify_stt.py = penengah]
    "V1": ("5_N84t1rUU0", "V1_5_N84t1rUU0.md"),
    "V2": ("DYdvJCxWd6M", "V2_DYdvJCxWd6M.md"),   # Metics Media
    "V3": ("8yE6G1Lup1s", "V3_8yE6G1Lup1s.md"),   # Samin Yasar
    "V4": ("G47mnkGkYwQ", "V4_G47mnkGkYwQ.md"),
    "V5": ("KKmnpuPdnUY", "V5_KKmnpuPdnUY.md"),
}
# CATATAN D2/steer controller: EXPANSION.md §1-2 punya label V2<->V3 TERTUKAR.
# Skrip ini TIDAK memakai EXPANSION.md sebagai ground-truth pemetaan; sumber pemetaan =
# nama file + header `YouTube:` di 02_transcripts/ (dicocokkan terhadap VIDS di bawah).
WORD_MIN = 15000  # ambang D3(a): AC1/AC9 >= 15.000 kata

def read(path):
    try:
        with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
            return f.read()
    except Exception:
        return None

def secs(ts):
    parts = [int(x) for x in ts.split(":")]
    if len(parts) == 2:
        return parts[0]*60 + parts[1]
    if len(parts) == 3:
        return parts[0]*3600 + parts[1]*60 + parts[2]
    return None

def inventory():
    inv = {}
    for dp, dn, fn in os.walk(ROOT):
        for x in fn:
            p = os.path.join(dp, x)
            try:
                st = os.stat(p)
                inv[os.path.relpath(p, ROOT).replace("\\", "/")] = (st.st_size, int(st.st_mtime))
            except Exception:
                pass
    return inv

def digest(inv):
    s = "|".join(f"{k}:{v[0]}:{v[1]}" for k, v in sorted(inv.items())
                 if not k.startswith("90_meta/verification_report") and not k.startswith("90_meta/countersign"))
    return hashlib.sha256(s.encode()).hexdigest()[:16]

results = []
evidence = {}

def record(n, name, ok, detail):
    status = "PASS" if ok is True else ("NEEDS_REVIEW" if ok == "NR" else "FAIL")
    results.append((n, name, status, detail))

def missing(n, name):
    # Artefak modul belum ada di disk = gate jadwal eksekusi, BUKAN FAIL (pitfall #9 skill).
    record(n, name, "NR", "artefak modul belum ada di disk (STT-MOD masih running) — run ulang wajib setelah MOD done")

# ---------- C0 guard read-only ----------
inv_before = inventory()
dig_before = digest(inv_before)

# ---------- load artifacts ----------
mod = read(MOD_MD)
mod_words = len(re.findall(r"\S+", mod)) if mod else 0
docx = []
for dp, dn, fn in os.walk(ROOT):
    for x in fn:
        if x.lower().endswith(".docx"):
            docx.append(os.path.join(dp, x))

transcripts = {}
map_mismatch = []
for vid, (yt, fname) in VIDS.items():
    t = read(os.path.join(ROOT, "02_transcripts", fname))
    if t:
        # guard D2: header `YouTube:` file transkrip WAJIB cocok dengan ID kanonis VIDS
        hy = re.search(r"youtube\.com/watch\?v=([A-Za-z0-9_-]+)", t)
        if hy and hy.group(1) != yt:
            map_mismatch.append(f"{vid}: header={hy.group(1)} vs kanon={yt}")
        stamps = [secs(m) for m in re.findall(r"\*\*\[(\d+:\d{2}(?::\d{2})?)\]\*\*", t)]
        stamps = [s for s in stamps if s is not None]
        dm = re.search(r"Duration:\s*([0-9:]+)", t)
        dur = secs(dm.group(1)) if dm else (max(stamps)+60 if stamps else 0)
        transcripts[vid] = {"text": t, "words": len(re.findall(r"\S+", t)),
                            "max_stamp": max(stamps) if stamps else 0, "dur": dur,
                            "segs": len(stamps)}
manifest = read(os.path.join(ROOT, "02_transcripts", "_MANIFEST.md"))

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ---------- CHECK 0: guard ----------
inv_after = inventory()
dig_after = digest(inv_after)
record(0, "Guard read-only (inventory pra==pasca, hanya laporan yang berubah)",
       dig_before == dig_after, f"digest pra={dig_before} pasca={dig_after}; modul={'ADA' if mod else 'BELUM ADA'} ({mod_words} kata); docx={len(docx)}")

# ---------- AC1: semua 5 video tertranskrip & terintegrasi ----------
if not mod:
    missing(1, "AC1 5 video saling melengkapi terintegrasi jadi SATU modul")
else:
    present = [v for v in VIDS if v in mod or VIDS[v][0] in mod]
    ok = len(present) == 5 and mod_words >= WORD_MIN
    record(1, "AC1 5 video saling melengkapi terintegrasi jadi SATU modul", ok,
           f"referensi video di modul: {present}; kata modul={mod_words} (min {WORD_MIN}, ambang D3)")

# ---------- AC2: nol-ke-hero (fundasi -> mahir) ----------
if not mod:
    missing(2, "AC2 jalur Zero-to-Hero berjenjang")
else:
    low = mod.lower()
    prog = sum(1 for k in ["zero to hero", "beginner", "fundamental", "advanced",
                            "chapter 1", "chapter 2", "module 1", "module 2",
                            "mastery", "mahasiswa", "student"])
    ok = prog >= 4 and re.search(r"(?i)(zero[\s-]*to[\s-]*hero|dari nol|fundamental.*advanced|beginner.*advanced)", mod, re.S)
    record(2, "AC2 jalur Zero-to-Hero berjenjang", bool(ok) and prog >= 4,
           f"penanda jenjang={prog}; frasa zero-to-hero/berjenjang={'YA' if ok else 'TIDAK'}")

# ---------- AC3: terstruktur & terintegrasi (kerangka bab) ----------
if not mod:
    missing(3, "AC3 informasi terstruktur jadi satu pembelajaran")
else:
    heads = re.findall(r"(?m)^#{1,3}\s+(.+)$", mod)
    chaps = [h for h in heads if re.search(r"(?i)(chapter|bab|modul|module|part\s+\d)", h)]
    ok = len(heads) >= 15 and len(chaps) >= 5
    record(3, "AC3 informasi terstruktur jadi satu pembelajaran", ok,
           f"heading={len(heads)}, heading bab/modul={len(chaps)}")

# ---------- AC4: langkah-demi-langkah di TIAP topik ----------
if not mod:
    missing(4, "AC4 panduan step-by-step di tiap topik")
else:
    # per section H2/H3: apakah ada marker langkah
    sections = re.split(r"(?m)^#{2,3}\s+", mod)
    step_pat = re.compile(r"(?m)^\s*(?:\d+[.)]|[-*]\s*\*\*(?:Step|Langkah)|Step\s*\d+\s*[:.]|Langkah\s*\d+\s*[:.])")
    total_steps = len(step_pat.findall(mod))
    topic_secs = [s for s in sections if len(s) > 400]
    with_steps = [s for s in topic_secs if step_pat.search(s)]
    ratio = len(with_steps)/max(1, len(topic_secs))
    ok = total_steps >= 20 and ratio >= 0.5
    record(4, "AC4 panduan step-by-step di tiap topik", ok,
           f"marker langkah total={total_steps}; seksi-topik={len(topic_secs)}, ber-langkah={len(with_steps)} ({ratio:.0%})")

# ---------- AC5: chapter expanded ----------
if not mod:
    missing(5, "AC5 chapter expanded untuk pemahaman/mastery")
else:
    exp = re.findall(r"(?im)^#{1,4}.*\b(expand|perdalam|pengayaan|deep[\s-]*dive|expanded)\b.*$", mod)
    deep_secs = [s for s in re.split(r"(?m)^#{2,3}\s+", mod) if len(s) > 1500]
    ok = len(exp) >= 3 or (len(exp) >= 1 and len(deep_secs) >= 5)
    record(5, "AC5 chapter expanded untuk pemahaman/mastery", ok,
           f"heading 'expanded/perdalam'={len(exp)}; seksi mendalam(>1500 ch)={len(deep_secs)}")

# ---------- AC6: ekspansi via browsing (sumber eksternal tersitasi) ----------
if not mod:
    missing(6, "AC6 ekspansi tip/teknik dari riset tambahan tersitasi")
else:
    urls = re.findall(r"https?://[^\s)\]>\"']+", mod)
    ext = [u for u in urls if "youtube.com" not in u]
    fmt = read(os.path.join(ROOT, "04_research", "FORMATS.md"))
    expf = read(os.path.join(ROOT, "04_research", "EXPANSION.md"))
    ok = len(ext) >= 5 and bool(fmt) and bool(expf)
    record(6, "AC6 ekspansi tip/teknik dari riset tambahan tersitasi", ok,
           f"URL eksternal di modul={len(ext)}; FORMATS.md={'ADA' if fmt else 'BELUM'}; EXPANSION.md={'ADA' if expf else 'BELUM'}")

# ---------- AC7: sitasi timestamp valid vs transkrip ----------
if not mod:
    missing(7, "AC7 klaim bersitasi timestamp transkrip yang valid")
else:
    cites = re.findall(r"(V[1-5])\s*[@(]?\s*\[?(\d{1,2}:\d{2}(?::\d{2})?)\]?", mod)
    # normalisasi: jika timestamp H:MM dan video >1 jam, regex di atas bisa menangkap
    # prefix HH:MM dari H:MM:SS — secs() sudah menangani kedua bentuk.
    bad = []
    for v, ts in cites:
        s = secs(ts)
        if v in transcripts and s is not None and s > transcripts[v]["dur"] + 60:
            bad.append(f"{v}@{ts}")
    ok = len(cites) >= 20 and len(bad) == 0 and not map_mismatch
    record(7, "AC7 klaim bersitasi timestamp transkrip yang valid", ok,
           f"sitasi timestamp={len(cites)} (min 20); di luar durasi video: {bad[:10] if bad else '0'}; "
           f"guard pemetaan kanonis D2 (header YouTube vs VIDS): {'COOK' if not map_mismatch else map_mismatch}")

# ---------- AC8: format course body profesional ----------
if not mod:
    missing(8, "AC8 format Professional Learning Docs (riset, bukan karangan)")
else:
    low = mod.lower()
    elems = {k: (k in low) for k in
             ["learning objective", "objective", "prerequisite", "durasi", "duration",
              "summary", "rangkuman", "assessment", "kuis", "quiz", "exercise", "latihan",
              "key takeaway", "glosarium", "glossary"]}
    hits = sum(elems.values())
    ok = hits >= 5 and bool(read(os.path.join(ROOT, "04_research", "FORMATS.md")))
    record(8, "AC8 format Professional Learning Docs (riset, bukan karangan)", ok,
           f"elemen format khas course body terdeteksi: {hits} ({[k for k,v in elems.items() if v][:12]}); FORMATS.md={'ADA' if read(os.path.join(ROOT,'04_research','FORMATS.md')) else 'BELUM'}")

# ---------- AC9: panduan lengkap 100% step-by-step (kedalaman) ----------
if not mod:
    missing(9, "AC9 cakupan materi sebanding sumber (kelayakan 'complete mastery')")
else:
    tr_words = sum(t["words"] for t in transcripts.values()) or 1
    ratio = mod_words / tr_words
    heads = len(re.findall(r"(?m)^#{1,3}\s", mod))
    ok = mod_words >= WORD_MIN and ratio >= 0.15 and heads >= 15
    record(9, "AC9 cakupan materi sebanding sumber (kelayakan 'complete mastery')", ok,
           f"modul={mod_words} kata vs transkrip={tr_words} kata (rasio {ratio:.2f}, min 0.15); min kata modul={WORD_MIN} (D3); heading={heads}")

# ---------- AC10: validated & verified ----------
if not mod:
    missing(10, "AC10 divalidasi & diverifikasi + deliverable .docx")
else:
    low = mod.lower()
    val = bool(re.search(r"(?i)(verif|validat|validasi|verifikasi|quality|mutu|review)", low))
    ok = val and len(docx) >= 1
    record(10, "AC10 divalidasi & diverifikasi + deliverable .docx", ok,
           f"bagian validasi/verifikasi di modul={'YA' if val else 'TIDAK'}; .docx={docx or 'BELUM ADA'}")

# ---------- verdict ----------
fails = [r for r in results if r[2] == "FAIL"]
nrs = [r for r in results if r[2] == "NEEDS_REVIEW"]
verdict = "FAIL" if fails else ("NEEDS_REVIEW" if nrs else "PASS")

# ---------- write report ----------
lines = []
lines.append("# Verification Report — Misi STT-Hermes-Learning-Module")
lines.append(f"**Run:** {now} | **Verifier:** gsp-verifier (t_4f0be60b) | **Skrip:** 90_meta/verify_stt.py v2 FROZEN (deterministic, read-only; v1 diarsipkan)")
lines.append("**Kanon pemetaan (D2):** V1=5_N84t1rUU0 Tina Huang · V2=DYdvJCxWd6M Metics · V3=8yE6G1Lup1s Samin · V4=G47mnkGkYwQ Ondrej · V5=KKmnpuPdnUY Kanasani — EXPANSION.md §1-2 TIDAK dipakai sbg ground-truth (label V2/V3 tertukar).")
lines.append(f"**Modul target:** 05_module/HERMES-ZERO-TO-HERO.md ({'ADA, ' + str(mod_words) + ' kata' if mod else 'BELUM ADA'})")
lines.append("")
lines.append("| # | Check | Status | Bukti |")
lines.append("|---|-------|--------|-------|")
for n, name, st, det in results:
    lines.append(f"| {n} | {name} | {st} | {det} |")
lines.append("")
lines.append(f"Guard digest pra={dig_before} pasca={dig_after} ({'CLEAN' if dig_before==dig_after else 'DRIFT!'})")
lines.append("")
lines.append(f"VERDICT: {verdict}")
with open(REPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

for n, name, st, det in results:
    print(f"CHECK {n}: {st} — {name} — {det}")
print(f"VERDICT: {verdict}")
print(f"report: {REPORT}")
