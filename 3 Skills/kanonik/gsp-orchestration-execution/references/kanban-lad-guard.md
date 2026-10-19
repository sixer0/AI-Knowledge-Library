# LAD-GUARD menolak kartu kanban ber-assignee tanpa blok LIMIT (02-09-2026)

Kejadian nyata (misi restart HQ 9011): kartu kontrak infra/ops kecil dicoba dibuat
langsung lewat CLI kanban:

```
hermes kanban --board default create "Fix HQ 9011 autostart bind 0.0.0.0" \
  --body "..." --assignee brahma --priority 2 --json
```

Hasil: DITOLAK, kartu tidak tercipta sama sekali:

```
LAD-GUARD: kartu delegasi ber-assignee tanpa blok LIMIT-AWARE+ESTIMASI di body ditolak
(kebijakan LAD 02-09, kontrak docs/2026-09-02-limit-aware-delegation). Jalur sah:
scripts/lad_card.py dari skill gsp-limit-aware-delegation (--est/--shape atau
--interaktif). Kerja interaktif singkat pun otomatis lolos karena lad_card.py menempel
jejak ESTIMASI. Sumber periksa: perintah shell 'terminal'.
```

## Implikasi

- Guard ini aktif pada SEMUA create kartu ber-assignee, termasuk kartu kerja
  infra/ops singkat oleh controller (pengecualian Q1/D3 tidak membebaskan dari
  jejak; ia hanya membebaskan dari kewajiban perhitungan ESTIMASI manual).
- Kartu pribadi TANPA assignee tetap bebas lewat `hermes kanban create`.
- Jangan ulangi percobaan create langsung setelah ditolak; langsung pakai jalur sah.

## Jalur sah (terbukti 02-09)

```
python "C:/Users/TRIAL/AppData/Local/hermes/skills/gsp/gsp-limit-aware-delegation/scripts/lad_card.py" \
  --assignee brahma \
  --title "<judul>" \
  --interaktif \
  --body "<deskripsi + bukti + rencana verify>"
```

Output sukses: `Created t_xxxxxxxx (ready, assignee=brahma)`. Skrip menempel blok
LIMIT-AWARE + jejak ESTIMASI otomatis dan menyetel max-runtime 1800. Penutupan kartu
tetap lewat `hermes kanban --board default complete <id> --result "<bukti>"`.

## Catatan kurasi

Pitfall ini seharusnya masuk seksi Pitfalls SKILL.md skill ini (satu paragraf pendek
setelah bullet "Worker self-dispatch works"), tetapi patch body SKILL.md dari sesi
background kurator ditolak guard read-before-write (pola sama dengan catatan 01-09
pada repo-docs-changelog). Tambahkan baris itu saat sesi foreground berikutnya, atau
jalankan `hermes curator adopt` bila skill ini akan dikelola penuh.
