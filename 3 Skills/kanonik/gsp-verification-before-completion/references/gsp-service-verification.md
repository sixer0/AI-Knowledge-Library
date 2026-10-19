# Verifikasi kesehatan servis GSP di host Windows

Pola teruji 02-09-2026 (kasus: laporan salah "WebUI 9012 down" dan akar sebenarnya
HQ 9011 bind sempit). Detail kasus lengkap:
workspace/gsp-hermes/workspace/docs/2026-09-02-hq-9011-bind/contract.md.

## Prinsip: satu probe bukan vonis

1. netstat dulu, bukan curl dulu: `netstat -ano | grep ":9011"`. LISTENING berarti
   proses hidup; catat alamat bind (0.0.0.0 = semua interface; IP tunggal = sempit)
   dan PID.
2. Servis GSP (HQ 9011, WebUI 9012, dashboard) memakai TLS self-signed: probe HARUS
   `curl -sk https://...`. HTTP polos ke port TLS-only gagal "empty reply" (curl
   exit 52) padahal server sehat; ini penyebab klasik laporan salah "down".
3. Respons 302/307 ke halaman login = sehat (auth aktif), bukan error.
4. Identifikasi proses dari PID, jangan dari nama proses:
   `powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'ProcessId=<PID>' | Select-Object -ExpandProperty CommandLine"`.
   Contoh nyata: pythonw.exe = Brahma WebUI server.py; node hq-server.mjs = Agent HQ.
5. Firewall dicek, tidak dicurigai: `netsh advfirewall firewall show rule name=all
   dir=in | grep -B7 <port>`; baca profil dan RemoteIP rule-nya.

## Diagnosa bind sempit (akses remote gagal)

1. Gejala: remote tidak bisa mengakses; netstat menunjukkan LISTENING hanya pada
   127.0.0.1 dan/atau satu IP spesifik.
2. Cari default bind di kode server (grep "listen" / konstanta HOSTS atau PORT),
   lalu telusuri rantai autostart: Startup folder .vbs -> shell script -> baris
   launch. Autostart tanpa env override mewarisi default kode, jadi perbaiki
   defaultnya di kode server (bukan menambal skrip autostart) agar semua jalur
   peluncur konsisten.
3. Scan hardcode IP: `grep -rn "<ip>" <repo> --include="*.mjs"` dan semacamnya,
   kecualikan node_modules dan .next.

## Uji live perubahan server TANPA menyentuh port produksi

1. Restart listener produksi adalah wewenang user (kebijakan 9012 dan 9011).
   Controller menguji kode yang sudah dipatch di port terisolasi, contoh:
   `HQ_PORT=9013 node hq-server.mjs` dijalankan lewat terminal background=true
   (foreground menolak '&').
2. Bukti yang diwajibkan sebelum klaim: netstat menunjukkan 0.0.0.0:<port-uji>;
   `curl -sk` dari localhost DAN dari IP Tailscale sama-sama merespons;
   `node --check` lulus untuk berkas yang diedit.
3. Matikan proses uji setelah selesai dan pastikan port uji kembali bersih.
4. Serahkan restart produksi ke user disertai perintah siap pakai dan instruksi
   verifikasi pasca-restart (netstat harus menampilkan 0.0.0.0:<port>).
