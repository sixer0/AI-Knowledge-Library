---
id: hermes-agent-profil-framework-mit
type: fakta
title: Hermes Agent — profil framework (open-source MIT, Nous Research)
sumber: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/LICENSE
halaman: "-"
tanggal_akses: 2026-09-01
kelas_bukti: primer
sensitif: tidak
perkara: top40-agent-ai
tags: [hermes-agent, nous-research, framework, open-source, mit]
links: [002-opsi-hermes-padu-padan]
penulis: gsp-librarian
diajukan: 2026-09-01
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-01
catatan_verifikasi: "Verdict: perlu_revisi (metadata semata; isi lolos penuh) || Alasan: 6 dari 7 dimensi lolos — provenans lengkap (URL primer LICENSE + tanggal_akses + kelas primer); anti-karangan: custodian menarik ulang sendiri https://raw.githubusercontent.com/NousResearch/hermes-agent/main/LICENSE pada 2026-09-01 — 'MIT License / Copyright (c) 2025 Nous Research' cocok verbatim; tagline, dibuat 2025-07-22, snapshot ±239.175 stars / ±48.803 forks, koreksi TUJUH terminal backends, footer fan site 'not affiliated', 11 query terlog — semuanya cocok hermes_agent_findings.md §1–§5; dedup wiki nol-hasil, link 002-opsi-hermes-padu-padan punya target di vault/riset-sistem-ai-gsp-kam, id tanpa tabrakan; grouping & kelengkapan vs draf P1 sesuai; sensitif tidak. Cacat dimensi metadata ada DUA: (1) key title ('Hermes Agent — profil framework (open-source MIT, Nous Research)') tidak sama dengan H1 pertama ('Hermes Agent — profil framework') — melanggar konvensi title==H1 yang dijaga batch terverifikasi 2026-08-25 dan sudah dipatuhi 3 objek sekannya; (2) baris `halaman: -` INVALID secara YAML (parser: 'sequence entries are not allowed here') — defect generator yang ternyata sistemik: 41 dari 46 objek folder ini gagal yaml.safe_load karena pola sama. || Rekomendasi: sunting dua baris — samakan `title` dengan H1 (atau sebaliknya) DAN ganti `halaman: -` menjadi nilai string berlabel (mis. `halaman: \\\\\\\"tanpa halaman (berkas lisensi)\\\\\\\"`) atau kosongkan kunci; perbaiki juga generator/pemanggil vault_propose.py agar tidak lagi menulis `halaman: -` (berlaku utk 40 objek B1 sekaligus). JANGAN ubah body (verifikasi isi sudah menyeluruh, nol temuan isi); setelah penyelarasan langsung layak terverifikasi tanpa uji ulang konten. Gate promote tetap kewenangan gsp-librarian. || Revisi 2026-09-01: konfirmasi langsung - validator uv validate_yaml_s18b.py cetak 'yaml+title+field OK SEMUA' (45 objek); title==H1 cocok, sumber/halaman sudah dikutip kutipan (YAML valid, 1 status). Isi tidak perlu uji ulang - 6/7 dimensi sudah lolos gelombang-1. Layak terverifikasi."
status: active
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-01
dipromosikan-ke: faktas/hermes-agent-profil-framework-mit.md
catatan_keputusan: "dipromosikan: AI40-S18b: terverifikasi custodian 7 dimensi 2026-09-01"
---

# Hermes Agent — profil framework (open-source MIT, Nous Research)

Sumber primer terverifikasi (diakses 2026-09-01):

1. **Lisensi: MIT** — teks hak cipta verbatim "Copyright (c) 2025 Nous Research", dibaca
   langsung dari berkas `LICENSE` repo `NousResearch/hermes-agent`
   (https://raw.githubusercontent.com/NousResearch/hermes-agent/main/LICENSE, diakses
   2026-09-01 via web_extract, teks penuh dikembalikan). Dikonfirmasi silang oleh jalur
   evidence misi AI40 (GitHub API license endpoint, berkas LICENSE didekode dan dibaca
   langsung) [docs/2026-09-01-top40-agent-ai/evidence/hermes/hermes_agent_findings.md §1].
2. **Repo**: `NousResearch/hermes-agent` — tagline "The agent that grows with you"; dibuat
   2025-07-22; bahasa Python; homepage hermes-agent.nousresearch.com
   [hermes_agent_findings.md §1, api.github.com/repos/NousResearch/hermes-agent, akses 2026-09-01].
3. **Kapabilitas terdokumentasi** (dari README/docs resmi yang dibuka 2026-09-01, bukan angka
   kinerja): learning loop tertutup (skill dibuat & diperbaiki saat dipakai, memory persisten,
   FTS5 session search), gateway messaging multi-platform (Telegram/Discord/Slack/WhatsApp/
   Signal/CLI), TUJUH terminal backends (local, Docker, SSH, Singularity, Modal, Daytona,
   Vercel Sandbox — koreksi terhadap catatan lama "enam"), cron scheduler bawaan, subagent
   paralel, Bot Mode, jalur riset RL/trajectory, Nous Portal
   [hermes_agent_findings.md §1 koreksi RT §8.3; docs resmi hermes-agent.nousresearch.com/docs
   diakses 2026-09-01].

## Batas jujur (yang TIDAK boleh disimpulkan dari objek ini)

- Traksi repo besar (snapshot ±239.175 stars / ±48.803 forks per 2026-09-01 via GitHub API)
  adalah indikator popularitas open-source, BUKAN bukti adopsi korporat.
- Adopsi framework Hermes Agent oleh korporasi bernama: NOL terverifikasi per 2026-09-01
  (11 query pencarian terlog; hasil kosong = hasil sah)
  [hermes_agent_findings.md §2, §5].
- `hermes-agent.ai` = fan site (footer tertulis "not affiliated with Nous Research");
  `hermes.com` = rumah mode Hermès (tabrakan merek). Penggunaan model Hermes/Nous via API ≠
  mengadopsi framework [hermes_agent_findings.md §3, §4].
