# kesegaran heartbeat gateway 3 profil wajib (non-WMI, read-only)
import json, os, datetime
base = os.path.join(os.environ["LOCALAPPDATA"], "hermes", "profiles")
now = datetime.datetime.now(datetime.timezone.utc)
for p in ["gsp-thinker", "gsp-worker", "gsp-worker-fast"]:
    f = os.path.join(base, p, "state", "gateway.heartbeat")
    try:
        d = json.load(open(f))
        ts = datetime.datetime.fromisoformat(d["updated_at"])
        age = (now - ts).total_seconds()
        print(f"{p}: pid={d['pid']} umur_heartbeat={age:.0f}s")
    except Exception as e:
        print(f"{p}: GAGAL_BACA {e}")
