# Integrasi WebUI Gateway/Channel ↔ Hermes dashboard (fix 2026-09-07, port 9119 → 9010)

Keluhan kelas: "menu Gateway/Channel gagal konfigurasi, gagal terhubung dengan
hermes dashboard" setelah dashboard pindah port. Akar masalah bisa TIGA LAPIS
berdiri sekaligus; berhenti di lapis pertama = perbaikan setengah.

## Peta jalur kode (gsp-brahma)

| Jalur panel | Modul | Transport | Terdampak pindah port? |
|---|---|---|---|
| Status chip / link dashboard (Settings → System) | `api/dashboard_probe.py` | probe GET `/api/status` loopback | YA (default 9119) |
| Konfigurasi channel manual (get/set env platform) | `api/gateway_channels_proxy.py` | import `hermes_cli.web_server` LANGSUNG via venv Hermes | TIDAK (tanpa HTTP) |
| QR pairing Telegram/WhatsApp | `api/dashboard_onboarding.py` (dipanggil rute `/api/gateway/manage/profiles/*/channels/*/qr-*` di `api/routes.py`) | HTTP ke endpoint onboarding dashboard | YA + butuh token |

## Gerbang yang harus dilewati (urutan diagnosis)

1. **Port target.** `webui.dashboard.url` di config.yaml AKTIF (profil aktif,
   resolve via `api.config._get_config_path()`; root =
   `AppData/Local/hermes/config.yaml`) kosong → probe jatuh ke default 9119.
   Tulis via jalur resmi: `save_dashboard_config({"enabled": ..., "url": ...})`
   (in-process, idempoten, reload otomatis by mtime) — jangan edit YAML manual.
   Port dashboard aktual terbaca dari cmdline proses:
   `Get-CimInstance Win32_Process` → `hermes dashboard --port NNNN`.
   Fallback baru (07-09): key `dashboard.port` / `dashboard_port` di config
   hermes ikut dibaca sebelum default 9119 (`_hermes_dashboard_port`).
2. **Gerbang bind-host.** `_webui_bind_host_allows_auto_probe()` menolak
   auto-probe saat WebUI bind 0.0.0.0 (produksinya GSP bind 0.0.0.0!). Sejak
   07-09 override url eksplisit menembus gerbang ini; pada kode LAMA (proses
   hidup pra-restart) hanya `enabled: always` yang membuat status tampil hidup.
   → Setelah deploy fix, kembalikan `enabled: auto`; selagi menunggu restart
   user, `always` adalah state sementara yang sah.
3. **Session-token dashboard.** Semua `/api/*` dashboard non-public dilindungi
   `_SESSION_TOKEN` ephemeral (loopback mode) — termasuk endpoint onboarding
   QR. Balasan `401 Unauthorized` padahal dashboard hidup ≠ auth gate OAuth
   (`auth_required=false` di status tidak menolong). Token diinjeksikan ke
   halaman indeks: regex `__HERMES_SESSION_TOKEN__\s*=\s*"([^"]+)"` pada
   `GET {base}/`, kirim sebagai header `X-Hermes-Session-Token`. Proxy QR kini
   melakukan ini sendiri (cache 30 dtk, retry sekali saat 401 = token basi
   pasca-restart dashboard). Verifikasi manual:
   ```
   tok=$(curl -s http://127.0.0.1:<port>/ | grep -oP '__HERMES_SESSION_TOKEN__\s*=\s*"\K[^"]+')
   curl -s -X POST -H "X-Hermes-Session-Token: $tok" -H 'Content-Type: application/json' \
        -d '{}' http://127.0.0.1:<port>/api/messaging/telegram/onboarding/start
   ```
   → 200 + pairing_id/deep_link/qr_payload = jalur sehat.

## Timeout probe

`DEFAULT_DASHBOARD_TIMEOUT` 0.5s → **5.0s** (07-09): `/api/status` host ini
terukur 2144–2335 ms bahkan warm (payload besar: gateway state + sessions +
components); 0.5s dan 2.0s memberi vonis false-unreachable. Port mati tetap
gagal seketika via connection-refused, jadi ambang besar murah. Test urutan
probe mengunci angka ini — sinkronkan `tests/test_dashboard_probe.py` bila
menaikkan nilainya lagi.

## Bersih-bersih sesi pairing uji

`start_pairing` yang dipakai untuk verifikasi MENINGGALKAN pairing menggantung
di memori dashboard. Batalkan: `DELETE /api/messaging/<platform>/onboarding/
<pairing_id>` dengan token yang sama (200 = bersih). Jangan lupa setelah uji
QR end-to-end.

## Verifikasi pasca-perbaikan (resep)

In-process (rute 9012 butuh login, jadi panggil modulnya langsung):
```python
import sys; sys.path.insert(0, r"C:/Users/TRIAL/gsp-brahma")
from api import dashboard_probe as dp, dashboard_onboarding as dob
dp.get_dashboard_status()          # running:true, port aktual
dob.start_pairing("telegram", "<profil>", {})   # ok:true + flow_id
dob.get_pairing_status("telegram", flow_id)     # status:waiting
```
Lalu pytest: `tests/test_dashboard_probe.py tests/test_dashboard_onboarding_proxy.py`
(TLS test-server fixture gagal boot di host ini — matikan via
`HERMES_WEBUI_TLS_CERT="" HERMES_WEBUI_TLS_KEY=""`; kegagalan boot TLS itu
pribase, bukan regresi). Restart WebUI = wewenang user (`./ctl.sh restart`);
kode server dianggap aktif hanya setelah proses baru lebih muda dari mtime fix.

## Catatan branch produksi (07-09)

Working tree produksi gsp-brahma berjalan dari branch **`webui-slow/fix`**
(bukan main) — static dilayani dari disk, jadi JANGAN tinggalkan checkout di
main saat bekerja; kembali ke `webui-slow/fix` sebelum menutup sesi. Fix ini
ada di main (`6cdd9b1`) dan ter-merge ke branch kerja via `ed037ba`.
