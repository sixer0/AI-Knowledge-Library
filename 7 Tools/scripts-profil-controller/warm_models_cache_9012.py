#!/usr/bin/env python3
"""warm_models_cache_9012.py — penghangat cache katalog model WebUI 9012.

Akar masalah (06-09): setiap buka sesi, /api/models?freshness=session_visit
melakukan live-rebuild katalog provider bila berkas cache disk berumur >300s
(TTL _SESSION_VISIT_MODELS_FRESHNESS_SECONDS). Probe provider GSP-AI/kilocode
sering lambat (tercatat 21-50 detik) sehingga tab terasa membeku sesaat setelah
dibuka. Script ini memanggil jalur yang SAMA di luar proses server sehingga
berkas models_cache.<profil>.json selalu berumur < TTL; sesi berikutnya jatuh
ke jalur cache (<1 detik). Tidak menyentuh proses server (restart = wewenang
user). Diam = sukses (stdout kosong; cron no_agent tidak mengirim pesan).
"""
import os
import sys
import time

os.environ.setdefault("HERMES_HOME", r"C:\Users\TRIAL\AppData\Local\hermes")
REPO = r"C:\Users\TRIAL\gsp-brahma"
if REPO not in sys.path:
    sys.path.insert(0, REPO)

PROFILES = ["gsp-master01", "gsp-master"]
GRACE_SECONDS = 90


def _cache_mtime(profile: str) -> float:
    name = "models_cache.json" if profile in ("default", "") else f"models_cache.{profile}.json"
    path = os.path.join(os.environ["HERMES_HOME"], "webui", name)
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0


def main() -> int:
    problems = []
    try:
        from api import config as api_config
        from api import profiles as api_profiles
    except Exception as exc:  # import gagal = konfigurasi berubah
        print(f"warm-models: import gagal: {exc!r}")
        return 1
    for name in PROFILES:
        try:
            api_profiles.set_request_profile(name)
            try:
                api_config.get_available_models_for_session_visit()
            finally:
                api_profiles.clear_request_profile()
        except Exception as exc:
            problems.append(f"{name}: {exc!r}")
    # Terbitan out-of-band (rebuild yang lewat budget 4s) berjalan di thread
    # daemon; beri grace sampai berkas cache tiap profil segar (umur < TTL 300s
    # server), lalu baru keluar — kalau tidak, proses mati sebelum menulis cache.
    deadline = time.monotonic() + GRACE_SECONDS
    while time.monotonic() < deadline:
        if all(time.time() - _cache_mtime(p) < 280 for p in PROFILES):
            break
        time.sleep(2)
    missing = [p for p in PROFILES if time.time() - _cache_mtime(p) >= 280]
    if missing:
        problems.append("cache belum tertulis setelah grace: " + ",".join(missing))
    if problems:
        # hanya laporkan bila gagal — watchdog senyap saat sehat
        print("warm-models: " + "; ".join(problems))
    return 0


if __name__ == "__main__":
    sys.exit(main())
