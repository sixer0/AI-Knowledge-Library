# KEMAMPUAN - domain STORAGE

<!-- BUKUV3-ING-1009 W4 | digest mesin dari KEMAMPUAN-REGISTER.csv,
tanggal beku 2026-10-09 | 15 unit kemampuan |
daya-ikat: P-5: SELURUH baris lahir pending_verification;
sign-off engineer 0/332 -> draft-tidak-terverifikasi-insan.
Angka dalam paket TIDAK sah sebagai ambang terima sampai verifier W7 + tanda tangan manusia. -->

Titik masuk: router `gsp-ekas-knowledge-index` -> `cari_ekas.py --kemampuan "<kata kunci>"`.
Register per paket: [`ekas/02_REGISTERS/KEMAMPUAN-REGISTER.csv`](../../02_REGISTERS/KEMAMPUAN-REGISTER.csv) (kolom staging_path = path sumber di staging BUKUV3).

| unit | skill | nama | kind | rumus | uji | sumber (per references.yaml) |
|---|---|---|---|---|---|---|
| K-0283 | <a id="DAT-001"></a>DAT-001 | System Capacity | stub-candidate | 0 |  | Designing Data-Intensive Applications - Kleppmann (2017) |
| K-0284 | <a id="DAT-002"></a>DAT-002 | Little's Law (Throughput-Latency-Concurrency) | calculator | 1 | 6 | Designing Data-Intensive Applications - Martin Kleppmann (2017, O'Reilly) [pdf hal. 31-33] |
| K-0285 | <a id="DAT-003"></a>DAT-003 | Data Platform Storage Sizing (RF + Growth) | calculator | 1 | 6 | Designing Data-Intensive Applications - Martin Kleppmann (2017, O'Reilly) [pdf hal. 167 & 31] |
| K-0286 | <a id="DAT-004"></a>DAT-004 | Database Selection | calculator | 1 | 6 | Designing Data-Intensive Applications - Martin Kleppmann [bab replikasi & partisi] |
| K-0287 | <a id="DAT-005"></a>DAT-005 | Quorum Replication (N, W, R) Check | calculator | 1 | 6 | Designing Data-Intensive Applications - Martin Kleppmann (2017, O'Reilly) [pdf hal. 193-197] |
| K-0288 | <a id="DAT-006"></a>DAT-006 | Hash Partitioning & Rebalance Cost | calculator | 1 | 6 | Designing Data-Intensive Applications - Martin Kleppmann (2017, O'Reilly) [pdf hal. 217 & 223] |
| K-0289 | <a id="DAT-007"></a>DAT-007 | Cache Effective Latency & Required Hit Ratio | calculator | 1 | 6 | Designing Data-Intensive Applications - Martin Kleppmann (2017, O'Reilly) [pdf hal. 33] |
| K-0290 | <a id="DAT-008"></a>DAT-008 | Consistency Tradeoff | calculator | 1 | 7 | Designing Data-Intensive Applications - Martin Kleppmann [bab replikasi & konsistensi (kuorum), hal. 334 (linearizability & kuorum)] |
| K-0291 | <a id="DAT-009"></a>DAT-009 | Composite Availability (Chain & Redundancy) | calculator | 1 | 6 | Site Reliability Engineering - Beyer dkk. (2016, O'Reilly) [pdf hal. 63] |
| K-0292 | <a id="DAT-010"></a>DAT-010 | SLO Error Budget & Downtime Window | calculator | 1 | 6 | Site Reliability Engineering - Beyer dkk. (2016, O'Reilly) [pdf hal. 51/59 & 503] |
| K-0293 | <a id="DAT-011"></a>DAT-011 | N+R Redundancy Sizing | calculator | 1 | 6 | The Practice of System and Network Administration Vol 1 3e - Limoncelli dkk. (2017, Addison-Wesley) [pdf hal. 285-286] / Site Reliability Engineering ... |
| K-0294 | <a id="DAT-012"></a>DAT-012 | RTO/RPO Failover Budget Check | calculator | 1 | 6 | Storage Networks Explained 2e - Troppens dkk. (2009, Wiley) [pdf hal. 385-393] / Designing Data-Intensive Applications - Martin Kleppmann (2017, O'Rei... |
| K-0295 | <a id="DAT-013"></a>DAT-013 | Capacity Planning | stub-candidate | 0 |  | Site Reliability Engineering - Google (2016) |
| K-0296 | <a id="DAT-014"></a>DAT-014 | Incident Response | document | 0 | 2 | Site Reliability Engineering (Google) - praktik manajemen insiden [-] / EKAS skill DAT-010 ERROR_BUDGET [-] |
| K-0297 | <a id="DAT-015"></a>DAT-015 | Monitoring Design | document | 0 | 2 | Site Reliability Engineering (Google) - empat sinyal emas [-] / EKAS skill DAT-009 SLA_SLO_SLI [-] |

## Prasyarat / komposit

Kolom `composite_parent` pada register menyebut rantai demo `qa/chains.py` tempat paket dipakai.

## Batas

- Paket `kind=stub-candidate` INERT: tanpa calculator; sumbernya berstatus blocked_missing_source (belum di rak).
- Lapisan kurasi/model (CURATION/TRAINING) TIDAK diingest sebagai teks (P-6, LOKAL-SAJA).

## Rantai demo `qa/chains.py` yang menyentuh domain ini

Ekstrak deterministik dari `qa/chains.py` (staging BUKUV3) oleh `w4_chains.py`;
pemetaan mata mengikuti keputusan analis W4 (tabel CHAIN_MAP).

| rantai | langkah | unit K-xxxx domain ini | mata RANTAI-JAMINAN |
|---|---|---|---|
| ML_PIPELINE | 15 skill (AIM-003, AIM-011, AIM-012, AIM-013, AIM-014, AIM-015, AIM-016, AIM-017, AIM-018, AIM-019, AIM-020, AIM-022, AIM-023, DAT-011, DAT-012) | KM-0293, KM-0294 | 3-hitung - pipeline ML -> domain baru (belum berantai) |
| DATA_PLATFORM | 10 skill (CCT-017, DAT-002, DAT-003, DAT-004, DAT-005, DAT-006, DAT-007, DAT-008, DAT-009, DAT-010) | KM-0284, KM-0285, KM-0286, KM-0287, KM-0288, KM-0289, KM-0290, KM-0291, KM-0292 | 3-hitung - platform data; domain tanpa rantai -> nyatakan belum berantai |
