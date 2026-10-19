# Struktur Laporan Kajian - kerangka 16 bab (terbukti disukai user GSP, 24-08-2026)

Urutan bab yang dipakai pada Kajian Ekosistem Brahma dan diterima baik:

1. Ringkasan Eksekutif - skala terukur (angka), temuan utama, rekomendasi utama
2. Metodologi & Cakupan - tabel metode/cakupan + batasan (mis. secret tidak dibaca)
3. Peta Arsitektur Ekosistem - diagram komponen ASCII + matriks layanan/port + node
4. Node Inti (Brahma/default) - identitas, model, konfigurasi, memori
5. Komponen besar (HQ, WebUI, Bridge) - stack, halaman, API routes, model data, alur
6. Fleet/Tabel - tabel lengkap (auto-generated via placeholder), kelompok & peran
7. Skill - registry, kategori, per-profil
8. Knowledge & Memory - workspace, EKAS, wiki, Information Library, kanban
9. Infrastruktur - autostart, watchdog/cron, Docker, Postgres, jaringan
10. Workflow Orkestrasi - end-to-end
11. Keamanan & RBAC
12. Status Live Saat Audit - tabel ringkas (layanan/gateway/DB/requests/kanban)
13. Temuan, Risiko & Gap - tabel `# | Temuan | Dampak | Tingkat`
14. Rekomendasi Peningkatan - kelompok A..E, bernomor
15. Lampiran - perintah verifikasi, inventaris skrip, env keys (nama saja), referensi

## Format entri "super detail" (katalog skill / inventaris item)
Per entri wajib memuat SEMUA baris berikut (jangan ada yang dipotong):
- Kategori, Lokasi (relpath)
- Metadata: versi, author, lisensi, platform
- Tags
- Deskripsi lengkap (frontmatter utuh)
- Pemicu / When to Use (penuh)
- Struktur bagian (daftar semua section)
- Perintah/tool utama (hingga 25, diekstrak dari code fences)
- File lengkap: `path` - ukuran (termasuk SKILL.md, LICENSE, README, __pycache__/*.pyc)
- Ukuran body

## Contoh tabel Status Live (saat audit)
| Aspek | Status |
|---|---|
| Layanan web (9010/9011/9012) | ✅ listening (HTTPS/HTTP) |
| Bridge | ✅ node bridge.mjs |
| Docker | ✅ N container up |
| Gateway fleet | ⚠️ stopped / running |

## Contoh tabel Temuan
| # | Temuan | Dampak | Tingkat |
|---|---|---|---|
| F1 | Roster mismatch A vs B | Dispatch gagal | Tinggi |

## Pitfall verifikasi angka
- Jumlah yang diklaim ("130 skill", "42 agen", "1996 entri") harus dihitung
  ulang programatik dari data mentah, bukan dari header/komentar yang bisa
  kedaluwarsa (contoh nyata: komentar ROSTER menyebut 43, aktual 41).
