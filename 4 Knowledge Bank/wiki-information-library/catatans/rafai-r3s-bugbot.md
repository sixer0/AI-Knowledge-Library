---
id: rafai-r3s-bugbot
type: catatan
title: Cursor Bugbot meninjau tiap PR dengan status CI success/neutral/failure dan Autofix spawn Cloud Agent
status: active
sumber: https://cursor.com/docs/bugbot.md
tanggal_akses: 2026-10-04
kelas_bukti: sekunder
sensitif: tidak
scope: rafai-1004
penulis: gate.py
diajukan: 2026-10-04
misi: RAFAI-1004
kartu: t_7830d5ef
gate: "{\"version\": \"GS-1.2\", \"run_id\": \"795ae9d2-597b-402f-a685-ef2ceeefaaf9\", \"ts\": \"2026-10-04T11:24:21+00:00\", \"sanitasi\": {\"n_redaksi\": 0, \"pola\": []}, \"verdict\": \"ok\"}"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-05
dipromosikan-ke: catatans/rafai-r3s-bugbot.md
catatan_keputusan: "dipromosikan: RAFAI-1004 CLOSEOUT-LIB t_7830d5ef: audit provenans 35/35 bersih (gate GS-1.2 run_id+ts cocok accepted.jsonl, sumber URL+tanggal_akses+kelas_bukti lengkap, kutipan R-id terverifikasi ada di berkas lajur); dedup 0 benturan (Jaccard<0,6 atas 958 objek kam/ft-eval/datmanual/wiki); non-sensitif non-dosir; lapis R13/VM tidak termasuk bahan (0 dari 35)"
---

# Cursor Bugbot meninjau tiap PR dengan status CI success/neutral/failure dan Autofix spawn Cloud Agent

Sumber: cursor.com/docs/bugbot.md diakses 2026-10-04. Bugbot berjalan otomatis tiap update PR atau via komentar cursor review; temuan default netral sehingga mewajibkan check saja tidak memblokir merge; konfigurasi dibaca dari branch base agar PR tidak mengubah cara Bugbot mereview dirinya.

> gate: {"version": "GS-1.2", "run_id": "795ae9d2-597b-402f-a685-ef2ceeefaaf9", "ts": "2026-10-04T11:24:21+00:00", "sanitasi": {"n_redaksi": 0, "pola": []}, "verdict": "ok"}
