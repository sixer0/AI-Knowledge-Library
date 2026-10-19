---
id: rafai-r2-claude-thinking-deprecation
type: catatan
title: Extended thinking budget deprecated pada Claude 4.6 dan ditolak 400 pada 4.7+; pengganti resmi adaptive thinking
status: active
sumber: https://platform.claude.com/docs/en/build-with-claude/extended-thinking
tanggal_akses: 2026-10-04
kelas_bukti: sekunder
sensitif: tidak
scope: rafai-1004
penulis: gate.py
diajukan: 2026-10-04
misi: RAFAI-1004
kartu: t_7830d5ef
gate: "{\"version\": \"GS-1.2\", \"run_id\": \"f17e08a6-fea2-4b64-8099-9804eb015dd7\", \"ts\": \"2026-10-04T11:28:21+00:00\", \"sanitasi\": {\"n_redaksi\": 0, \"pola\": []}, \"verdict\": \"ok\"}"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-05
dipromosikan-ke: catatans/rafai-r2-claude-thinking-deprecation.md
catatan_keputusan: "dipromosikan: RAFAI-1004 CLOSEOUT-LIB t_7830d5ef: audit provenans 35/35 bersih (gate GS-1.2 run_id+ts cocok accepted.jsonl, sumber URL+tanggal_akses+kelas_bukti lengkap, kutipan R-id terverifikasi ada di berkas lajur); dedup 0 benturan (Jaccard<0,6 atas 958 objek kam/ft-eval/datmanual/wiki); non-sensitif non-dosir; lapis R13/VM tidak termasuk bahan (0 dari 35)"
---

# Extended thinking budget deprecated pada Claude 4.6 dan ditolak 400 pada 4.7+; pengganti resmi adaptive thinking

Sumber: R2-F45, platform.claude.com/docs/en/build-with-claude/extended-thinking.md (docs.claude.com redirect ke platform.claude.com, DEFECT-R2-4; curl 200 11:22Z). Inti kutipan resmi: mode extended thinking (menyetel tipe thinking menjadi enabled dengan parameter anggaran) deprecated pada model Claude 4.6 - request masih diterima - dan model Claude 4.7 ke atas menolaknya dengan galat HTTP 400. Pengganti resmi: adaptive thinking yang menyela otomatis tanpa header beta. Bukti batas fitur reasoning terikat versi model; dukung kebijakan tanggal-potong.

> gate: {"version": "GS-1.2", "run_id": "f17e08a6-fea2-4b64-8099-9804eb015dd7", "ts": "2026-10-04T11:28:21+00:00", "sanitasi": {"n_redaksi": 0, "pola": []}, "verdict": "ok"}
