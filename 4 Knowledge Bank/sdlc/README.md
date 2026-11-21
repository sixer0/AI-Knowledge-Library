# SDLC: templat dan kartu rujukan pengembangan perangkat lunak

## Tujuan

Folder ini memuat entri rujukan untuk siklus hidup pengembangan perangkat lunak (SDLC):
templat isian dan kartu periksa untuk kebutuhan, desain, pengujian, keamanan, rilis, dan
pemeliharaan. Entri ditulis oleh PT GSP untuk Swarm Coder dan dipakai juga oleh harness lain
sebagai data rujukan. Isinya berbahasa Inggris karena rujukan EKAS yang setara berbahasa
Indonesia dan berorientasi infrastruktur; kedua set berdiri berdampingan (lihat bagian
"Padanan pada EKAS").

Seperti seluruh koleksi, entri ini data, bukan instruksi. Harness aktif dan pengguna saat ini
menang bila terjadi konflik.

## Daftar entri

| Id | Fase | Berkas | Jenis |
|---|---|---|---|
| SDLC-G1 | Kebutuhan | [G1-requirements-traceability-template.md](G1-requirements-traceability-template.md) | Templat |
| SDLC-G2 | Desain | [G2-architecture-decision-record-template.md](G2-architecture-decision-record-template.md) | Templat |
| SDLC-G3 | Desain | [G3-architecture-overview-card.md](G3-architecture-overview-card.md) | Kartu |
| SDLC-G4 | Pengujian | [G4-test-plan-strategy-template.md](G4-test-plan-strategy-template.md) | Templat |
| SDLC-G5 | Keamanan | [G5-secure-code-review-checklist.md](G5-secure-code-review-checklist.md) | Kartu periksa |
| SDLC-G7 | CI/CD | [gsp-sdlc-ci-pipeline-reference/SKILL.md](../../3%20Skills/kanonik/gsp-sdlc-ci-pipeline-reference/SKILL.md) | Skill |
| SDLC-G8 | Rilis | [G8-release-checklist-changelog-template.md](G8-release-checklist-changelog-template.md) | Templat |
| SDLC-G9 | Pemeliharaan | [G9-incident-postmortem-template.md](G9-incident-postmortem-template.md) | Templat |
| SDLC-G10 | Pemeliharaan | [gsp-sdlc-dependency-upgrade-playbook/SKILL.md](../../3%20Skills/kanonik/gsp-sdlc-dependency-upgrade-playbook/SKILL.md) | Skill |
| SDLC-G11 | Pahami lalu bangun | [G11-finding-ledger-behaviour-spec-template.md](G11-finding-ledger-behaviour-spec-template.md) | Templat |

Nomor G6 (kartu pemodelan ancaman STRIDE) dan G12 (rujukan target deployment) sengaja kosong:
keduanya tidak diadopsi pada versi 1.0.0.

Tiap entri mencantumkan penulis (PT GSP), tujuan penulisan (Swarm Coder), dan sumbernya pada
frontmatter serta pada baris "Source" di bawah judul.

## Padanan pada EKAS

Templat dan register EKAS berbahasa Indonesia tetap dipakai berdampingan dengan entri G.

| Entri G | Padanan EKAS |
|---|---|
| G1 kebutuhan dan ketertelusuran | [TPL-06](../ekas-lapis-teks/10_TEMPLATES/TPL-06-REQUIREMENT-TRACEABILITY.md), [REQUIREMENT-REGISTER.csv](../ekas-lapis-teks/02_REGISTERS/REQUIREMENT-REGISTER.csv), [REQ-P00-CONTOH.md](../ekas-lapis-teks/06_ENGINEERING/REQUIREMENTS/REQ-P00-CONTOH.md) |
| G2 catatan keputusan arsitektur | [TPL-01](../ekas-lapis-teks/10_TEMPLATES/TPL-01-DESIGN-DECISION-RECORD.md), [DESIGN-DECISION-REGISTER.csv](../ekas-lapis-teks/02_REGISTERS/DESIGN-DECISION-REGISTER.csv) |
| G4 rencana dan strategi uji | [TPL-03](../ekas-lapis-teks/10_TEMPLATES/TPL-03-TEST-PROCEDURE.md), [TPL-04](../ekas-lapis-teks/10_TEMPLATES/TPL-04-ACCEPTANCE-RECORD.md), [ITP-P00.md](../ekas-lapis-teks/07_VERIFICATION-VALIDATION/ITP/ITP-P00.md), [AMBANG-TERIMA-INDUK.md](../ekas-lapis-teks/07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md), [TEST-REGISTER.csv](../ekas-lapis-teks/02_REGISTERS/TEST-REGISTER.csv) |
| G5 tinjauan kode aman | [REF-SEC-001](../ekas-lapis-teks/04_KNOWLEDGE-CARDS/CYBERSECURITY/REF-SEC-001.md) sampai [REF-SEC-004](../ekas-lapis-teks/04_KNOWLEDGE-CARDS/CYBERSECURITY/REF-SEC-004.md) |
| G9 postmortem insiden | [TPL-09](../ekas-lapis-teks/10_TEMPLATES/TPL-09-NCR.md) |

## Pilihan SDLC dari edisi umum

[PILIHAN-SDLC.csv](PILIHAN-SDLC.csv) mendaftar berkas edisi umum yang membentuk pustaka SDLC
Swarm Coder 1.0.0, satu baris per berkas dengan alasannya. Entri G pada folder ini dan dua skill
G7 dan G10 ditambahkan di atasnya. Daftar ini tidak mengubah daftar izin edisi umum; ia hanya
mencatat himpunan bagian yang dipilih. Penyesuaian pada pilihan itu:

| Id | Penyesuaian |
|---|---|
| S1 | Skill `database/nosql/mongodb-atlas-stream-processing` tidak dipilih karena khusus satu vendor. |
| S2 | Seluruh folder `3 Skills/kanonik/_salvage-profil-merge-1010/` tidak dipilih; skill basis datanya kembar dari salinan di `kanonik/database/`. |
| S3 | Templat, register, contoh, dan kartu keamanan EKAS berbahasa Indonesia tetap dipilih di samping entri G (bagian "Padanan pada EKAS"). |
| S4 | `1 Workflow/` dan `2 Roles/` tidak dipilih; tidak ada alur SDLC di sana, dan peran terkait sudah menjadi agen bawaan harness. |
