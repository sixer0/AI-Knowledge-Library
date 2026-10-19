---
id: fleet-profil-vision-4-batasan
type: fakta
title: Fleet Profil Vision (4) & Batasan qwen3.7-flash
status: active
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 7.4
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: digital
writer: gsp-librarian
tags: [gsp-fleet, vision, qwen, toolset]
links: [fleet-40-profil-inventaris-dan-peran]
penulis: dashboard
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian 2026-09-03, challenge penuh 7 dimensi). Alasan: Tabel 4 profil vision dan toolsetnya identik byte-per-byte dengan kajian §7.4 baris 344-349 (image-analyst, image-specialist dengan image_gen, image-prompt-specialist, design-system-specialist). Kedua pitfall terverifikasi ada di baris 351: profil vision tanpa terminal menyebabkan search_files ber-root ke profile home sehingga bisa salah simpulkan file hilang, dan qwen3.7-flash rawan halusinasi detail gambar (smoke test 24-08-2026). Rujukan rekomendasi §15.D.11 terverifikasi di baris 552 ('Perkuat profil vision: sediakan toolset terminal/read ... dokumentasikan batas halusinasi qwen3.7-flash'). Tidak ada dimensi yang gagal. Kelas bukti primer sesuai (laporan audit langsung), seksi Batas mengakui perilaku model dapat berubah antar versi (pengakuan batasan eksplisit), grouping domain digital sesuai, links timbal-balik dengan objek fleet-40 valid. || Rekomendasi: Siap dipromosikan. Sunting status `terverifikasi` -> `ditinjau` sebelum promote (aturan I1). || Riwayat: catatan_verifikasi sebelumnya (custodian 2026-08-25 perlu_revisi, direvisi librarian Wave B fix-h1) dipertahankan sebagai riwayat."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/fleet-profil-vision-4-batasan.md
catatan_keputusan: "dipromosikan: IL-INGEST-01 B1a pilot: verdict custodian terverifikasi (C-B1a-verdict.md), cek YAML kelas-I5 lulus, non-sensitif non-dosir"
---

# Fleet Profil Vision (4) & Batasan qwen3.7-flash

4 profil fleet GSP bermodel **vision** (qwen3.7-flash via kilocode) dan
batasannya (kajian §7.4):

| Profil | Toolset khas |
|---|---|
| gsp-image-analyst | file, vision, skills, session_search, todo (tanpa terminal) |
| gsp-image-specialist | file, terminal, vision, **image_gen**, skills |
| gsp-image-prompt-specialist | file, vision, skills (tanpa terminal) |
| gsp-design-system-specialist | file, web, vision, skills (tanpa terminal) |

- **Pitfall terverifikasi:** profil vision tanpa toolset terminal →
  `search_files` default root = profile home → bisa salah simpulkan "file
  hilang"; instruksi wajib path eksplisit.
- **Pitfall terverifikasi:** model qwen3.7-flash rawan halusinasi detail
  gambar (smoke test 24-08-2026).
- Rekomendasi terkait (§15.D.11): perkuat profil vision dengan toolset
  terminal/read untuk menghindari kesimpulan "file hilang"; dokumentasikan
  batas halusinasi qwen3.7-flash.

Sumber: `kajian_ekosistem_brahma.md` bab 7.4 (+ rekomendasi §15 D.11).

# Bukti

- Smoke test vision 24-08-2026 mengonfirmasi kecenderungan halusinasi detail
  gambar pada qwen3.7-flash (kajian §7.4).

# Batas

- Perilaku model dapat berubah antar versi; catat tanggal verifikasi.
