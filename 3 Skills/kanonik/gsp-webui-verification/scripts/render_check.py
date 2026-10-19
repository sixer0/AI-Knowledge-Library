#!/usr/bin/env python3
"""Render-check GSP web UI via headless Chromium (Playwright) — tanpa daemon browser.

Pakai untuk HTTPS self-signed (Agent HQ :9011, Brahma WebUI :9012) atau halaman
web lokal apa pun yang perlu diverifikasi render/UX-nya. Dump teks body + daftar
button + screenshot. Ubah URL/EXE bila perlu.

Cara pakai:
    python render_check.py [url] [--click "Teks tombol"] [--out prefix]
Contoh:
    python render_check.py https://localhost:9011/information-library --out il
    python render_check.py https://localhost:9011/information-library --click "Legacy" --out il_legacy
"""
import argparse, json, sys
from playwright.sync_api import sync_playwright

# Browser Playwright yang SUDAH ter-install (cek versi yang ada dulu:
# gunakan search_files / ls pada C:/Users/TRIAL/AppData/Local/ms-playwright/).
DEFAULT_EXE = r"C:/Users/TRIAL/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--exe", default=DEFAULT_EXE)
    ap.add_argument("--click", default=None, help="klik tombol pertama yang teksnya diawali string ini")
    ap.add_argument("--wait", type=int, default=2500, help="ms tunggu setelah load/klik")
    ap.add_argument("--out", default="render", help="prefix file output (txt + png)")
    args = ap.parse_args()

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, executable_path=args.exe,
                              args=["--ignore-certificate-errors"])
        ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1440, "height": 960})
        page = ctx.new_page()
        page.goto(args.url, wait_until="networkidle", timeout=90000)
        page.wait_for_timeout(args.wait)

        if args.click:
            ok = page.evaluate("""(prefix) => {
                const el = [...document.querySelectorAll('button')]
                    .find(x => (x.innerText||'').trim().startsWith(prefix));
                if (el) el.click();
                return !!el;
            }""", args.click)
            print("click:", args.click, "->", "OK" if ok else "NOT FOUND")
            page.wait_for_timeout(args.wait)

        text = page.inner_text("body")
        with open(f"{args.out}.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("=== BODY TEXT (awal 1500) ===")
        print(text[:1500])

        btns = page.evaluate("""() => [...document.querySelectorAll('button')]
            .map(b => (b.innerText||'').trim()).filter(t => t && t.length < 70)""")
        print("=== BUTTONS ===")
        for x in btns[:30]:
            print("  ", x.replace("\n", " ")[:70])

        page.screenshot(path=f"{args.out}.png")
        print("\nscreenshot:", f"{args.out}.png")
        b.close()

if __name__ == "__main__":
    main()
