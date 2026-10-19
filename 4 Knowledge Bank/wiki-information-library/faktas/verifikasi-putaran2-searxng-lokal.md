---
id: verifikasi-putaran2-searxng-lokal
type: fakta
title: "Verifikasi putaran 2: SearXNG lokal sehat (HTTP 200, 30 hasil)"
status: active
sumber: docs/2026_08_24_verifikasi_putaran2/status.md
halaman: baris 42-43
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: verifikasi-putaran2
domain: digital
writer: gsp-librarian
tags: [verifikasi, putaran2, searxng, websearch, il-rebuild, inspeksi-harian]
links: [ekosistem-matriks-layanan-port]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/verifikasi-putaran2/2026-08-25_verifikasi-putaran2-searxng-lokal.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Verifikasi putaran 2: SearXNG lokal sehat (HTTP 200, 30 hasil)

## Ringkasan
Endpoint pencarian SearXNG lokal (web search backend fleet) sehat dan mengembalikan hasil valid.

## Bukti (sumber: status.md baris 42-43)
- `GET http://127.0.0.1:8080/search?q=test&format=json` → HTTP 200, 20.047 byte, 30 hasil
  (title count), respons JSON valid.
