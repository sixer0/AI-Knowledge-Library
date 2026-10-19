# Verifikasi Kartu Sunting-Skill Kanonik (pola WF-CRAWL-0911, 11-09)

Sumber pola: misi enforcement firecrawl+searxng paralel, kontrak `docs/2026-09-11-firecrawl-searxng-parallel-enforcement/contract.md`, kartu S1-S6 dikerjakan gsp-data-collector/gsp-skill-creator via bridge, controller = profil default. Referensi ini adalah checklist controller/verifier ketika objek verifikasi sebuah kartu adalah SUNTINGAN SKILL.md (bukan dokumen data; untuk .xlsx/.docx pakai `document-artifact-verification.md`).

## Gerbang tujuh langkah (berurutan)

1. **Bump versi cocok kontrak.** `grep -nE "^version" <skill>/SKILL.md` pada kanonik. Kontrak menyebut 1.0.0 -> 1.1.0 maka harus persis; versi loncat atau diam = temuan.
2. **Uji per butir kontrak dengan nomor baris, lalu baca utuh bloknya.** Grep frasa kunci tiap butir kontrak (mis. `maxDepth`, `unresponsive_engines`, `N=4`), catat nomor baris hasil, dan SEBELUM mengklaiak terbaca, `sed -n 'A,Bp'` blok yang dikutip. Preseden positif: baris bisa benar tapi norma melenceng; nomor baris bukan bukti, isi blok yang dibaca utuh baru bukti.
3. **Pisah-salin kanonik-vs-fleet yang DISENGAJA itu sah.** Pola benar fleet: worker mengedit HANYA kanonik (`workspace/gsp-hermes/skills/<skill>/SKILL.md`) dan membiarkan salinan fleet (`$LOCALAPPDATA/hermes/skills/gsp/<skill>/SKILL.md`) tetap versi lama, karena distribusi adalah kartu sendiri (satu penulis versi per waktu). Verifikasi DUA sisi: kanonik sudah baru DAN fleet masih lama, baru cocokkan dengan klaim kartu. Jangan vonis "distribusi gagal" saat salinan fleet masih versi lama bila kontrak memang menunda ke langkah distribusi.
4. **Spot-test hidup satu resep terkoreksi.** Resep API yang dikoreksi kartu wajib diprobe sekali oleh pengklaim terhadap mesin hidup (mis. `POST /v2/batch/scrape` -> `{"success":true,"id":...}` bentuk async persis terdokumentasi). `selfcheck.out` / `verify_exact.out` buatan worker BUKAN pengganti probe segar; cek juga ada salinan pra-sunting (`SKILL.md.v1.0.0.pre`) supaya auditor bisa diff.
5. **Klaim register/probe diuji pada bukti MENTAH.** Bila kartu melapor register merah-hijau berbasis angka (mis. sebar engine), buka berkas bukti mentah (`raw-probe.jsonl`, `probe-run.log`), cocokkan JUMLAH dan STRUKTUR rekaman dengan tabel yang dilaporkan (mis. 15 rekaman: 4x hasil-10 semua bing, 10x nol, 1 gabungan) — bukan hanya membaca laporan vonisnya. CAPPED-with-evidence adalah predikat sah; vonis buntu tanpa bukti mentah tidak.
6. **A1/A2 manual saat scanner tak tersedia di sesi worker.** Profil pekerja tanpa terminal kerap melapor scanner naturalisasi tak jalan (sticky-gate di artefak identifikasi). Controller menjalankan penghitung manual U+2014 / U+2013 / U+00B7 / CJK = nol pada kedua berkas identifikasi, dan melaporkannya sebagai "cek-manual berformat", bukan melewatkan tahap.
7. **Norma downstream disampaikan sebagai KOMENTAR kartu, bukan kartu baru.** Putusan controller (mis. D-06: rekomendasi engine hanya bing, larang klaim multi-engine, wajib baca unresponsive_engines) ditempel ke badan SEMUA kartu downstream yang akan menulis resep serupa: `hermes kanban --board default comment <id> "$(cat berkas)"`. Ini menutup lintasan notifikasi-kanban "jangan buat kartu/grafik baru" sekaligus menyuntik norma tanpa re-dekomposisi.

## Pitfall alat

- `hermes kanban comment` menerima teks POSISIONAL (`task_id text`), TIDAK mengenal flag `--file`; `--file` gagal `unrecognized arguments`. Pola: `comment $id "$(cat C:/Users/TRIAL/Temp/body.txt)"`.
- Dump board `hermes kanban --board default list --json` sesekali `exit 2`; fallback ke `show <id>` per kartu lalu ulangi dump di giliran berikutnya.
- Watchdog terminal `sleep N; cmd` foreground mati di batas timeout tool; pakai skrip polling Python background dengan notify_on_complete (pola `wfc_watch.py`: poll list --json tiap 90 dtk, cetak hanya transisi status, DEADLINE eksplisit).

## Batas klaim

Checklist ini mewajibkan pelaksanaan probe dan baca-blok oleh pengklaim pada run tertentu; tidak ada klaim gerbang ini otomatis lolos sefleet. Yang memverifikasi suntingan skill idealnya bukan penulis suntingannya (Iron Law penulis-bukan-verifikator tetap berlaku di lapis controller: controller menguji, verifier F4 mengulang lintas-waktu — status engine backoff bisa berubah antar-waktu).
