# -*- coding: utf-8 -*-
"""Probe P5: apakah server GSP-AI melakukan prefix caching?
Kirim kerangka sistem besar yang IDENTIK dua kali dalam sesi singkat,
baca field usage (prompt_tokens_details.cached_tokens / cache_read_input_tokens).
Jalankan sebelum dan sesudah user mengaktifkan --enable-prefix-caching di vLLM.
Pemakaian: uv run --python 3.11 python probe_prefix_cache.py
"""
import io, json, os, time, urllib.request

BASE = "http://10.83.81.246:11400/v1"
KEY = os.environ.get("HERMES_CUSTOM_10_83_81_246_11400_API_KEY", "")
if not KEY:
    for envf in (r"C:/Users/TRIAL/AppData/Local/hermes/.env",
                 r"C:/Users/TRIAL/AppData/Local/hermes/profiles/gsp-data-collector/.env"):
        if os.path.exists(envf):
            for line in io.open(envf, encoding="utf-8"):
                if line.startswith("HERMES_CUSTOM_10_83_81_246_11400_API_KEY="):
                    KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
        if KEY:
            break
assert KEY, "API key tidak ditemukan"

# Kerangka sistem identik ~8-10 ribu token (diulang sampai >= 30000 karakter)
SKELETON = ("Anda adalah agen uji infrastruktur GSP. Aturan baku berikut tetap "
            "untuk seluruh percakapan ini dan wajib dipatuhi tanpa pengecualian. "
            "Aturan 1: jangan mengarang angka. Aturan 2: sebut sumber. Aturan 3: "
            "tutup dengan VERDICT. ") + ("Daftar panjang aturan operasional fleet: "
            "kartu kanban wajib, contract doc wajib, dispatch trace wajib, gerbang "
            "naturalisasi wajib, LAD wajib, verifikasi sebelum selesai wajib. " * 40)

def call(tag, tail):
    body = {
        "model": "worker-fast",
        "messages": [
            {"role": "system", "content": SKELETON},
            {"role": "user", "content": tail},
        ],
        "max_tokens": 16,
    }
    req = urllib.request.Request(
        BASE + "/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bear" + "er " + KEY},
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode())
    dt = time.time() - t0
    u = d.get("usage", {})
    det = u.get("prompt_tokens_details") or {}
    cached = det.get("cached_tokens", u.get("cache_read_input_tokens", 0)) or 0
    print(f"{tag}: latensi={dt:5.1f}s prompt={u.get('prompt_tokens')} "
          f"cached={cached} completion={u.get('completion_tokens')}")
    return u.get("prompt_tokens"), cached

p1, c1 = call("PANGGIL-1 (cold)", "Balas hanya kata SIAP.")
time.sleep(2)
p2, c2 = call("PANGGIL-2 (harusnya warm bila caching aktif)", "Balas hanya kata SIAP.")
print()
if c2 and p2 and c2 / p2 > 0.5:
    print("VERDICT: PREFIX CACHING AKTIF (cache read panggilan-2 = %d dari %d)" % (c2, p2))
else:
    print("VERDICT: PREFIX CACHING TIDAK AKTIF (cache read panggilan-2 = %d dari %d)" % (c2, p2))
