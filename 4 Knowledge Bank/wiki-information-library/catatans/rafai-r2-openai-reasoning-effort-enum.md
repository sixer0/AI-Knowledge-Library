---
id: rafai-r2-openai-reasoning-effort-enum
type: catatan
title: "Enumerasi resmi reasoning_effort OpenAI: none/minimal/low/medium/high/xhigh/max bergantung model; rekomendasi resmi per kasus guna"
status: active
sumber: https://developers.openai.com/api/docs/guides/reasoning.md
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
dipromosikan-ke: catatans/rafai-r2-openai-reasoning-effort-enum.md
catatan_keputusan: "dipromosikan: RAFAI-1004 CLOSEOUT-LIB t_7830d5ef: audit provenans 35/35 bersih (gate GS-1.2 run_id+ts cocok accepted.jsonl, sumber URL+tanggal_akses+kelas_bukti lengkap, kutipan R-id terverifikasi ada di berkas lajur); dedup 0 benturan (Jaccard<0,6 atas 958 objek kam/ft-eval/datmanual/wiki); non-sensitif non-dosir; lapis R13/VM tidak termasuk bahan (0 dari 35)"
---

# Enumerasi resmi reasoning_effort OpenAI: none/minimal/low/medium/high/xhigh/max bergantung model; rekomendasi resmi per kasus guna

Sumber: R2-F44, developers.openai.com/api/docs/guides/reasoning.md (pola .md curl 200 11:22Z). Kutipan: 'Supported values are model-dependent and can include none, minimal, low, medium, high, xhigh, and max. Lower effort favors speed and lower token usage...'; sebagian model tidak mendukung none/minimal dan default medium; tabel rekomendasi: voice/fast use low lalu none; xhigh untuk deep research/agentic long runs; max untuk tugas paling kompleks.

> gate: {"version": "GS-1.2", "run_id": "f17e08a6-fea2-4b64-8099-9804eb015dd7", "ts": "2026-10-04T11:28:21+00:00", "sanitasi": {"n_redaksi": 0, "pola": []}, "verdict": "ok"}
