#!/usr/bin/env python3
"""X Watch - akun pertahanan/keamanan Indonesia (jalur publik, tanpa login).

Dijalankan tiap 5 menit oleh cron Hermes (no_agent). Selalu mencetak ringkasan
cek ke stdout -> dikirim verbatim; juga append ke watch-log.jsonl + watch-log.md.
Sumber: syndication.twitter.com timeline-profile (publik, tanpa API key).
"""
import json
import os
import re
import subprocess
import datetime

HANDLES = ["TNI_AD", "Puspen_TNI", "Kemlu_RI", "KemenhanRI", "TNI_AU"]
BASE = os.environ.get("XWATCH_DIR") or "C:/Users/TRIAL/workspace/gsp-xwatch"
STATE_F = BASE + "/state.json"
JSONL_F = BASE + "/watch-log.jsonl"
MD_F = BASE + "/watch-log.md"
TZ = datetime.timezone(datetime.timedelta(hours=7))
MAX_SHOW = 3


def parse_dt(s):
    try:
        return datetime.datetime.strptime(s, "%a %b %d %H:%M:%S +0000 %Y").replace(
            tzinfo=datetime.timezone.utc
        )
    except Exception:
        return None


def fetch(handle):
    url = "https://syndication.twitter.com/srv/timeline-profile/screen-name/" + handle
    try:
        p = subprocess.run(
            ["curl", "-s", "--max-time", "20", "-A", "Mozilla/5.0", url],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except Exception:
        return None
    html = p.stdout or ""
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return None
    try:
        data = json.loads(m.group(1))
    except Exception:
        return None
    entries = (
        data.get("props", {}).get("pageProps", {}).get("timeline", {}).get("entries", [])
        or []
    )
    out = []
    for e in entries:
        t = (e or {}).get("content", {}).get("tweet", {}) or {}
        if not t.get("id_str"):
            continue
        out.append(
            {
                "id": str(t["id_str"]),
                "user": (t.get("user") or {}).get("screen_name") or handle,
                "created": t.get("created_at", ""),
                "iso": (parse_dt(t.get("created_at", "")) or datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)).isoformat(),
                "text": re.sub(r"\s+", " ", (t.get("full_text") or t.get("text") or "")).strip(),
                "rt": int(t.get("retweet_count") or 0),
                "like": int(t.get("favorite_count") or 0),
            }
        )
    out.sort(key=lambda x: x["iso"], reverse=True)
    return out


def load_state():
    try:
        with open(STATE_F, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"seen": {}, "tick": 0}


def save_state(st):
    with open(STATE_F, "w", encoding="utf-8") as f:
        json.dump(st, f, ensure_ascii=False)


def main():
    os.makedirs(BASE, exist_ok=True)
    st = load_state()
    st["tick"] = int(st.get("tick", 0)) + 1
    now = datetime.datetime.now(TZ)
    stamp = now.strftime("%Y-%m-%d %H:%M WIB")
    lines = ["\U0001F6F0\ufe0f X Watch - Hankam Indonesia | %s | cek #%d" % (stamp, st["tick"])]
    rec = {"ts": now.isoformat(), "tick": st["tick"], "handles": {}}

    for h in HANDLES:
        tweets = fetch(h)
        if tweets is None:
            lines.append("@%s: \u26a0\ufe0f gagal ambil data (timeout/struktur berubah)" % h)
            rec["handles"][h] = {"error": True}
            continue
        seen = set(st["seen"].get(h, []))
        first_run = len(seen) == 0
        new = [t for t in tweets if t["id"] not in seen]
        for t in new:
            seen.add(t["id"])
        st["seen"][h] = list(seen)[-500:]
        rec["handles"][h] = {
            "total": len(tweets),
            "new": len(new),
            "newest": tweets[0]["iso"] if tweets else "",
            "new_items": new[:MAX_SHOW],
        }
        tag = "baseline" if first_run and new else ("+%d baru" % len(new) if new else "tidak ada perubahan")
        lines.append("@%s: %d tweet | %s" % (h, len(tweets), tag))
        for t in (new[:MAX_SHOW] if new else tweets[:1] if first_run else []):
            pre = "\u2022" if new else "\u2514 terbaru:"
            body = t["text"][:150]
            lines.append("   %s [%s] %s" % (pre, t["created"][4:10], body))

    with open(JSONL_F, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    with open(MD_F, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n\n")
    save_state(st)
    refresh_dashboard()
    lines.append("Log: %s" % MD_F)
    print("\n".join(lines))


def refresh_dashboard():
    import importlib.util

    cands = [
        BASE + "/x_dashboard.py",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "x_dashboard.py"),
    ]
    for cand in cands:
        if not os.path.exists(cand):
            continue
        try:
            spec = importlib.util.spec_from_file_location("x_dashboard", cand)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.main()
            return
        except Exception:
            pass


if __name__ == "__main__":
    main()
