---
id: inventaris-layanan-port-ekosistem
type: fakta
title: Inventaris Layanan & Port Ekosistem GSP (audit 24-08-2026)
status: active
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 3.2
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: operations
writer: gsp-librarian
tags: [ekosistem-brahma, layanan, port, infrastruktur]
links: [arsitektur-ekosistem-brahma-5-lapisan]
penulis: dashboard
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian PUTARAN 2, 2026-09-03, re-challenge penuh 7 dimensi atas suntingan gsp-document-writer). Alasan: re-challenge PUTARAN 2: suntingan putaran 1 terverifikasi. Butir Bukti ditulis ulang menjadi '7 container Docker total (Firecrawl 6 + SearXNG 1), kajian 1 dan 13; 10.3 mendaftar 6 service Firecrawl' - diverifikasi ulang terhadap sumber: baris 34 '7 container Docker (Firecrawl stack + SearXNG)', baris 508 'Docker (Firecrawl 6 + SearXNG 1)', 10.3 enam service tanpa angka 7. Tabel port utama tetap identik 3.2 (verifikasi putaran 1); seksi Batas menegaskan snapshot. || Rekomendasi: objek siap lanjut ke lane librarian - sunting status 'terverifikasi' menjadi 'ditinjau' sebelum memanggil vault_promote.py (aturan I1); cek YAML kelas I5 dan klasifikasi dosir manual tetap prosedurnya. Tidak ada perubahan lain yang diperlukan penulis. Sensitif: tidak; dosir: tidak ada tema perkara hukum (kompensasi klasifikasi manual lane librarian, temuan I2). || Riwayat PUTARAN 1 (custodian 2026-09-03, perlu_revisi): Verdict: perlu_revisi (custodian 2026-09-03, challenge penuh 7 dimensi). Alasan: Tabel layanan & port identik dengan kajian §3.2 baris 118-127 untuk seluruh 10 baris (9011 HQ HTTPS self-signed node.exe ~1 GB, 9012 WebUI pythonw ~308 MB, 9010 dashboard HTTP 127.0.0.1, bridge internal, PostgreSQL 5433 dan 5432, SearXNG 8080 Up 10 jam, Firecrawl API 3002 Up 10 jam, MySQL 3306, Tailscale 100.102.23.27). Kolom PID sengaja tidak disalin - pilihan yang wajar untuk objek pengetahuan. Seksi Batas menegaskan status port sebagai snapshot, bukan kondisi terkini. Seksi Bukti menyatakan 'Firecrawl stack 7 container + SearXNG up 10 jam (kajian §10.3)' - dua kesalahan sekaligus. §10.3 (baris 448-451) tidak menyebut jumlah container sama sekali dan hanya mendaftar 6 service Firecrawl (api, playwright-service, redis, rabbitmq, nuq-postgres, foundationdb + init). Angka 7 berasal dari §1 baris 34 yang berarti 7 container TOTAL (Firecrawl stack + SearXNG), dan §13 baris 508 menegaskannya sebagai 'Firecrawl 6 + SearXNG 1'. Kalimat objek consequently membaca 7 Firecrawl + 1 SearXNG = 8, yang tidak didukung bacaan mana pun. || Rekomendasi: Tulis ulang butir Bukti itu menjadi '7 container Docker total (Firecrawl 6 + SearXNG 1), kajian §1 dan §13; §10.3 mendaftar 6 service Firecrawl' - atau cukup hapus angkanya dan rujuk §3.2. Setelah koreksi satu baris ini objek layak terverifikasi; tabel utamanya sudah utuh. || Riwayat: catatan_verifikasi sebelumnya (custodian 2026-08-25 perlu_revisi, direvisi librarian Wave B fix-h1) dipertahankan sebagai riwayat."
verifikasi-oleh: gsp-custodian
verifikasi-putaran: 2
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-document-writer
direvisi-pada: 2026-09-03
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/inventaris-layanan-port-ekosistem.md
catatan_keputusan: "dipromosikan: subset lolos re-challenge RC-9 putaran 2 (9/9 terverifikasi); angka snapshot dibaca sebagai snapshot audit 24-08-2026 (objek terkait sudah membawa seksi Batas)"
---

# Inventaris Layanan & Port Ekosistem GSP (audit 24-08-2026)

Matriks layanan & port ekosistem GSP saat audit 24-08-2026 (kajian §3.2):

| Layanan | Port | Protokol | Status |
|---|---|---|---|
| Agent Headquarter (gsp-datacenter) | 9011 | HTTPS TLS self-signed | ✅ Listening (node.exe ~1 GB RAM) |
| WebUI Brahma (gsp-brahma) | 9012 | HTTPS TLS self-signed | ✅ Listening (pythonw.exe ~308 MB) |
| Hermes Dashboard | 9010 | HTTP 127.0.0.1 | ✅ Listening |
| hermes-bridge | - | internal | ✅ node bridge.mjs aktif |
| PostgreSQL 17 (bus HQ) | 5433 | TCP | ✅ accepting |
| PostgreSQL lain/legacy | 5432 | TCP | ✅ accepting |
| SearXNG (Docker) | 8080 | HTTP | ✅ Up 10 jam |
| Firecrawl API (Docker) | 3002 | HTTP | ✅ Up 10 jam |
| MySQL (host) | 3306 | TCP | ✅ Listening |
| Tailscale (mesh) | 100.102.23.27 | UDP/WireGuard | ✅ Online |

Sumber: `kajian_ekosistem_brahma.md` bab 3.2 (tabel Matriks Layanan & Port).

# Bukti

- Semua layanan diverifikasi live via curl + netstat + docker ps (kajian §2
  metode, §3.2).
- 7 container Docker total (Firecrawl 6 + SearXNG 1), kajian §1 dan §13;
  §10.3 mendaftar 6 service Firecrawl. Semua up 10 jam saat audit.

# Batas

- Status port adalah snapshot: layanan bisa berhenti/berubah; gunakan data
  audit ini sebagai baseline, bukan kondisi terkini.
