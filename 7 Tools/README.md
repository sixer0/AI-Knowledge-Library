# 7 Tools

## Tujuan

Folder ini menyimpan salinan skrip dari lingkungan sumber: pemantau dan watchdog fleet, alat audit gateway, operasi papan tugas (kanban), gerbang delegasi, pengelola registri profil, perbaikan korpus, pemeliharaan pustaka, serta prompt tugas historis. Nilainya ada pada pola rekayasa dan kronologi keputusan yang terekam di docstring dan kepala berkas, bukan pada kemampuan menjalankannya.

Skrip arsip tidak dijalankan, termasuk bila tugas tampak memerlukannya. Syarat pengecualian dan cakupannya ada pada [KEBIJAKAN-SENSITIVITAS.md](../KEBIJAKAN-SENSITIVITAS.md), bagian "Menjalankan skrip arsip". Satu-satunya skrip arsip yang dijalankan di repositori ini adalah penjaga LOCK, dan yang menjalankannya rangkaian uji [tests/test_wave_lock_guard.py](../tests/test_wave_lock_guard.py). Uji itu memakai blueprint sintetis di folder sementara dan memeriksa bahwa penjaga hanya mengimpor modul pustaka standar yang diizinkan serta tidak menulis berkas.

Semua uraian di bawah dibaca dari docstring atau komentar kepala tiap berkas. Isi berkas tidak dieksekusi, dan perilaku yang tidak tertulis di kepala berkas tidak diklaim.

## Struktur subfolder

| Subfolder | Isi |
|---|---|
| `scripts-profil-controller/` | Skrip milik profil controller dan System Manager. Isinya pemantau misi, watchdog layanan, monitor dan audit gateway, pembersih papan, gerbang delegasi, laporan kesehatan fleet, dan ratusan skrip ronde cron sekali-pakai berawalan `sysman_` |
| `scripts-repo-gsp-hermes/` | Utilitas repositori fleet: rollout aturan dan konfigurasi ke banyak profil, verifier deterministik, provisioning profil, katalog skill, migrasi pustaka lama, dispatch ke HQ, dan berkas hasil sapuan (`_*.json`, `_*.txt`) |
| `scripts-repo-gsp-hermes/korpus-index-repair-1005/` | Gerbang audit ulang misi perbaikan indeks korpus |
| `scripts-repo-gsp-hermes/korpus-lanjutan-1011/` | Pembangkit kartu gelombang dari tabel blueprint, ditambah watchdog serah-terima misi |
| `scripts-repo-gsp-hermes/prompts/` | Prompt subtugas dan prompt vision untuk migrasi pengetahuan lama ke Information Library |

Beberapa nama berkas muncul di kedua subfolder dengan isi berbeda (watchdog serah-terima misi, watchdog rantai ringkasan, penghangat cache katalog model). Kedua versi itu tidak identik, sehingga yang satu tidak bisa dianggap salinan yang lain.

## Peta topik

### Pemantauan dan watchdog

Pola yang berulang di kelompok ini: stdout kosong berarti sehat, dan cron mode tanpa agen hanya mengirim pesan bila stdout terisi. Keluaran dibuat stabil tanpa cap waktu supaya monitor berbasis hash hanya bereaksi pada perubahan keadaan yang nyata.

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Laporan kesehatan fleet harian: gateway dibanding registri, kartu hidup per assignee, kegagalan run 24 jam, backlog AgentRequest HQ. Tidak dijalankan | [gsp_fleet_health_report.py](scripts-profil-controller/gsp_fleet_health_report.py) | docstring baris 3-8 |
| Pemindai kebutuhan controller untuk cron mission-wake, baca-saja dengan SQLite moda baca dan `query_only` | [gsp_mission_wake_scan.py](scripts-profil-controller/gsp_mission_wake_scan.py) | docstring awal |
| Watchdog serah-terima misi korpus lanjutan, diam saat sehat | [mission_watch_1011.py](scripts-profil-controller/mission_watch_1011.py) | docstring awal |
| Watchdog gerbang naturalisasi beserta seksi audit limit-aware dan seksi fase | [nat_gate_watchdog.py](scripts-profil-controller/nat_gate_watchdog.py) | docstring awal |
| Monitor pembangunan ulang Information Library: alur berlapis penulis dan penantang, maksimal tiga putaran revisi | [il_rebuild_monitor.py](scripts-profil-controller/il_rebuild_monitor.py) | docstring awal |
| Watchdog rantai ringkasan ekspo: kartu selesai tanpa anak hidup padahal checkpoint masih bersisa dinilai buntu | [ring_chain_watch.py](scripts-profil-controller/ring_chain_watch.py) | docstring awal |
| Penjaga serah-terima per irisan ekspo, menulis status siap ke berkas serah | [ring_serah_watch.py](scripts-profil-controller/ring_serah_watch.py) | docstring awal |
| Watchdog layanan WebUI dan HQ: diam saat sehat, restart bila mati (versi Python dan shell) | [watchdog-webui-hq.py](scripts-profil-controller/watchdog-webui-hq.py), [watchdog-webui-hq.sh](scripts-profil-controller/watchdog-webui-hq.sh) | kepala berkas |
| Peluncur sekaligus watchdog Agent HQ (basis data, aplikasi web, bridge) | [gsp-hq-launch.sh](scripts-profil-controller/gsp-hq-launch.sh) | komentar kepala |
| Watchdog unduhan model yang mendeteksi macet dari pertumbuhan byte antar-run | [watchdog_comfy_dl.sh](scripts-profil-controller/watchdog_comfy_dl.sh), [watchdog_comfy_dl.py](scripts-profil-controller/watchdog_comfy_dl.py) | komentar kepala |
| Watchdog progres misi yang menyimpan state antar-run (lima varian) | [watch_rkt0924.py](scripts-profil-controller/watch_rkt0924.py) | docstring awal |
| Digest stabil papan misi aktif untuk monitor-hash | [watch_fullpower_0905.py](scripts-profil-controller/watch_fullpower_0905.py) | docstring awal |
| Snapshot progres ingestion dengan keluaran stabil | [bukuv3_progress_snapshot.py](scripts-profil-controller/bukuv3_progress_snapshot.py) | docstring awal |
| Pemantau linimasa publik akun tertentu tanpa login, beserta peringkas dan pembuat dashboard HTML. Pemantauan akun adalah kemampuan dwiguna dan memerlukan otorisasi ([KEBIJAKAN-SENSITIVITAS.md](../KEBIJAKAN-SENSITIVITAS.md), AP-10) | [x_watch.py](scripts-profil-controller/x_watch.py), [x_summary.py](scripts-profil-controller/x_summary.py), [x_dashboard.py](scripts-profil-controller/x_dashboard.py) | docstring awal |
| Watchdog misi ekspo, rantai interop, dan rantai standar | [expo26_watchdog.py](scripts-profil-controller/expo26_watchdog.py), [watch_interop_chain.py](scripts-profil-controller/watch_interop_chain.py), [watch_std_chain.py](scripts-profil-controller/watch_std_chain.py) | kepala berkas |

Pemantau misi perorangan, pengawas deploy dan penghangat cache WebUI, serta pemeriksa koneksi VPN ke server inferensi milik pihak tertentu juga ada di folder ini. Namanya dapat dicari di [INDEKS.md](INDEKS.md).

### Gateway: monitor, audit, probe

Prinsip yang dipakai: dua pengamat, satu kebenaran. Monitor menjaga dan menyalakan gateway, sementara audit independen yang baca-saja membuktikan vonis monitor.

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Monitor gateway era penggabungan profil: menjaga gateway wajib tetap hidup, sumber kebenaran registri profil | [gsp_gateway_monitor_v1.py](scripts-profil-controller/gsp_gateway_monitor_v1.py) | docstring awal |
| Audit gateway baca-saja; vonis "ganda" dihitung dari instans independen | [gsp_gateway_audit_v1.py](scripts-profil-controller/gsp_gateway_audit_v1.py) | docstring awal |
| Klasifikasi proses gateway: rantai parent/child (normal) atau instans independen (rebutan port, konsumen pesan ganda) | [gsp_gateway_tree_v1.py](scripts-profil-controller/gsp_gateway_tree_v1.py) | docstring |
| Probe fungsional gateway: status CLI, port listen, umur log | [gsp_gateway_probe_v1.py](scripts-profil-controller/gsp_gateway_probe_v1.py) | docstring |
| Audit independen System Manager pembanding monitor | [sysman_gateway_audit.py](scripts-profil-controller/sysman_gateway_audit.py) | docstring |
| Audit proses tanpa WMI lewat API native, dibuat saat WMI di host macet, dan probe kewarasannya | [sysman_audit_noWMI_v1.py](scripts-profil-controller/sysman_audit_noWMI_v1.py), [sysman_noWMI_sanity.py](scripts-profil-controller/sysman_noWMI_sanity.py) | docstring |
| Sapuan "hantu" gateway dengan filter baris perintah, bukan nama proses | [sysman_gateway_cron_1018b_ghost_v1.py](scripts-profil-controller/sysman_gateway_cron_1018b_ghost_v1.py) | docstring |
| Saksi kesegaran gateway dari berkas heartbeat per profil | [sysman_gateway_cron_1017_hb_v1.py](scripts-profil-controller/sysman_gateway_cron_1017_hb_v1.py) | docstring |
| Pendahulu era banyak-profil: cek gateway dinamis dan watchdog semua profil | [gsp_fleet_gateway_check.py](scripts-repo-gsp-hermes/gsp_fleet_gateway_check.py), [gsp_gateway_watchdog.py](scripts-repo-gsp-hermes/gsp_gateway_watchdog.py) | docstring awal |
| Menyalakan gateway headless untuk profil tanpa layanan | [start_missing_gateways_0903.py](scripts-repo-gsp-hermes/start_missing_gateways_0903.py) | docstring awal |

Keluarga `sysman_gateway_cron_*` di `scripts-profil-controller/` berisi ronde cron System Manager per tanggal: heartbeat, sapuan, umur PID, sensus layanan, dan diagnosis memori. Setiap berkasnya dipakai satu ronde saja.

### Papan tugas (kanban) dan kartu yatim

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Pembersih kartu yatim harian: tagihan untuk kartu diam, klaim running tanpa heartbeat, dan assignee di luar registri | [gsp_board_orphan_cleaner.py](scripts-profil-controller/gsp_board_orphan_cleaner.py) | docstring kelas A-C |
| Sensus papan baca-saja untuk ronde tagihan | [sysman_cleaner_1018b_census_v1.py](scripts-profil-controller/sysman_cleaner_1018b_census_v1.py) | docstring |
| Ronde koreksi yang menulis komentar ke kartu papan; contoh skrip ronde yang tidak baca-saja | [sysman_cleaner_1018b_fix_v1.py](scripts-profil-controller/sysman_cleaner_1018b_fix_v1.py) | docstring |
| Sapuan penilaian kartu yatim | [sysman_orphan_sweep_1015a.py](scripts-profil-controller/sysman_orphan_sweep_1015a.py) | docstring |
| Pembersih snapshot terminal yang tercemar penanda sesi lain | [sysman_rtboard_1018_snappurge_v1.py](scripts-profil-controller/sysman_rtboard_1018_snappurge_v1.py) | komentar kepala |
| Pemeriksa siklus monitor tugas: komentar baru, kartu parkir, antrean persetujuan HQ | [tm_cycle_check_20260916.py](scripts-repo-gsp-hermes/tm_cycle_check_20260916.py) | docstring |

Keluarga `sysman_wake_*` adalah ronde cron mission-wake. Isinya sensus, eval, probe, dan rekonsiliasi kartu selesai yang belum di-ACK, kartu blocked, dan umur penanda. Contohnya [sysman_wake_blindspot_v1.py](scripts-profil-controller/sysman_wake_blindspot_v1.py) (blind spot kartu running dengan laporan selesai tanpa ACK). Sebagian kecil dari keluarga ini menulis, misalnya [sysman_wake_mark_1014cron.sh](scripts-profil-controller/sysman_wake_mark_1014cron.sh) yang menulis penanda anti-ulang. Keluarga `sysman_orphan_*`, `sysman_rtboard_*`, `sysman_cron_*`, dan `sysman_health_*` mengikuti pola ronde yang sama.

### Delegasi dan gelombang

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Gerbang tumbukan kepemilikan LOCK pra-gelombang dengan masukan daftar kartu atau tabel blueprint. Ini satu-satunya skrip arsip yang dijalankan oleh uji | [gsp_wave_lock_guard.py](scripts-profil-controller/gsp_wave_lock_guard.py) | docstring awal |
| Gerbang rantai delegasi dengan tiga subperintah, termasuk jaring pengaman deteksi pekerja mati | [gsp_deleg_watch.py](scripts-profil-controller/gsp_deleg_watch.py) | docstring awal |
| Pembungkus cron jaring pengaman delegasi, dengan catatan perbaikan timeout saat kontensi tulis basis data | [gsp_rantai_watch_cron.py](scripts-profil-controller/gsp_rantai_watch_cron.py) | docstring |
| Uji red-green perbaikan timeout dengan subprocess yang disimulasikan | [sysman_rw_timeout_fix_redgreen_v1.py](scripts-profil-controller/sysman_rw_timeout_fix_redgreen_v1.py) | docstring skenario R1-R3 |
| Ekstraksi tabel blueprint sembilan kolom menjadi JSON kartu per gelombang untuk penjaga LOCK | [build_wave_cards.py](scripts-repo-gsp-hermes/korpus-lanjutan-1011/build_wave_cards.py) | docstring |
| Pembangkit kartu dari baris blueprint, versi gelombang pertama dan versi generik | [gen_wave1_cards.py](scripts-repo-gsp-hermes/korpus-lanjutan-1011/gen_wave1_cards.py), [gen_wave_cards.py](scripts-repo-gsp-hermes/korpus-lanjutan-1011/gen_wave_cards.py) | docstring |
| Audit distribusi sistem orkestrasi ke profil hidup dan akun RBAC | [gsp_orchestration_distribution_audit.py](scripts-profil-controller/gsp_orchestration_distribution_audit.py) | docstring cakupan A-B |
| Dispatch AgentRequest ke HQ (bebas dan terikat kartu), serta kueri baca-saja permintaan terbaru | [hq_dispatch.cjs](scripts-repo-gsp-hermes/hq_dispatch.cjs), [hq_dispatch_card.cjs](scripts-repo-gsp-hermes/hq_dispatch_card.cjs), [hq_query_recent.cjs](scripts-repo-gsp-hermes/hq_query_recent.cjs), [chk_req.cjs](scripts-repo-gsp-hermes/chk_req.cjs) | komentar kepala |
| Digest KPI dispatch mingguan | [dispatch_kpi_weekly.mjs](scripts-profil-controller/dispatch_kpi_weekly.mjs) | komentar kepala |

Tiga skrip rekonsiliasi kartu kontrak satu perkara memperlihatkan tiga jalur penutupan kartu: UPDATE langsung ke basis data HQ, ke basis data kanban, dan lewat CLI resmi. Namanya ada di [INDEKS.md](INDEKS.md).

### Registri profil dan konfigurasi fleet

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Penjaga kesegaran registri profil: akun, folder profil di disk, dan entri yang foldernya hilang | [gsp_registry_freshness_guard.py](scripts-profil-controller/gsp_registry_freshness_guard.py) | docstring butir 1-3 |
| Invarian QA fleet dengan kontrak exit 0/1/2 dan WARN yang tidak mengubah exit | [hqa_invariants.py](scripts-profil-controller/hqa_invariants.py) | docstring awal |
| Regenerasi roster controller dari akun RBAC | [rbac_roster.mjs](scripts-repo-gsp-hermes/rbac_roster.mjs) | komentar kepala |
| Promosi profil berakun RBAC menjadi kelas controller | [promote_rbac_controllers_20260831.py](scripts-repo-gsp-hermes/promote_rbac_controllers_20260831.py) | docstring |
| Provisioning profil spesialis baru dengan pola idempoten dan dry-run | [create_ekas_specialists.py](scripts-repo-gsp-hermes/create_ekas_specialists.py), [create_ecosystem_agents.py](scripts-repo-gsp-hermes/create_ecosystem_agents.py), [create_3d_specialist.py](scripts-repo-gsp-hermes/create_3d_specialist.py), [create_imagegen_worker.py](scripts-repo-gsp-hermes/create_imagegen_worker.py) | docstring |
| Penetapan model default dan fallback untuk seluruh profil, sengaja berurutan karena batch paralel pernah gagal | [set_gsp_ai_fleet_default.py](scripts-repo-gsp-hermes/set_gsp_ai_fleet_default.py), [set_thinker_analysts_librarian_20260902.py](scripts-repo-gsp-hermes/set_thinker_analysts_librarian_20260902.py) | docstring bagian alasan berurutan |
| Pendaftaran penyedia model kustom ke semua profil | [register_gsp_ai_fleet.py](scripts-repo-gsp-hermes/register_gsp_ai_fleet.py) | docstring |
| Distribusi kredensial dan pengaturan ke berkas env profil (nilainya tidak dibaca dan tidak disalin) | [fix_fleet_env.py](scripts-repo-gsp-hermes/fix_fleet_env.py), [fix_fleet_kilocode.py](scripts-repo-gsp-hermes/fix_fleet_kilocode.py), satu skrip rollout kunci penyedia gambar (cari di [INDEKS.md](INDEKS.md)) | docstring |
| Standarisasi compaction memori dalam tiga versi (suntingan tekstual minimal yang aman CRLF/LF) dan verifiernya | [rollout_compaction_0930_v3.py](scripts-repo-gsp-hermes/rollout_compaction_0930_v3.py), [verify_compaction_0930.py](scripts-repo-gsp-hermes/verify_compaction_0930.py) | komentar kepala |
| Pemangkasan skill profil (lean) dan inventarisnya | [rewrite_soul_lean.py](scripts-repo-gsp-hermes/rewrite_soul_lean.py), [strip_redundant_skills.py](scripts-repo-gsp-hermes/strip_redundant_skills.py), [inventory_fleet_lean.py](scripts-repo-gsp-hermes/inventory_fleet_lean.py), [lean_fix_inv7_20260929.py](scripts-repo-gsp-hermes/lean_fix_inv7_20260929.py) | docstring |
| Inventaris enforcement dua lajur (controller dan worker) beserta rollout-nya | [enforcement_inventory.py](scripts-repo-gsp-hermes/enforcement_inventory.py), [rollout_enforcement_20260831.py](scripts-repo-gsp-hermes/rollout_enforcement_20260831.py) | docstring |

Remediasi lean untuk akun perorangan ada di [INDEKS.md](INDEKS.md).

### Rollout aturan ke profil (SOUL dan MEMORY)

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Pemasang blok aturan ke SOUL fleet: akurasi data, kontrak desain, indeks pengetahuan, rail bukti dua moda | [install_data_accuracy_rule_20260904.py](scripts-repo-gsp-hermes/install_data_accuracy_rule_20260904.py), [install_design_contract_rule_20260906.py](scripts-repo-gsp-hermes/install_design_contract_rule_20260906.py), [install_ekas_index_rule_20261006.py](scripts-repo-gsp-hermes/install_ekas_index_rule_20261006.py), [install_rail_rule_20261008.py](scripts-repo-gsp-hermes/install_rail_rule_20261008.py) | teks aturan di awal berkas |
| Amandemen aturan yang sudah terpasang | [amend_accuracy_rule_cer_20260904.py](scripts-repo-gsp-hermes/amend_accuracy_rule_cer_20260904.py), [amend_rail_rule_revB_20261008.py](scripts-repo-gsp-hermes/amend_rail_rule_revB_20261008.py) | kepala berkas |
| Pemasang aturan pencarian "ofensif" dan "presisi hasil", serta sinkronisasi referensinya. Lihat Jebakan | [install_offensive_search_rule_20260903.py](scripts-repo-gsp-hermes/install_offensive_search_rule_20260903.py), [install_precision_result_rule_20260913.py](scripts-repo-gsp-hermes/install_precision_result_rule_20260913.py), [sync_offensive_logic_precision_20260913.py](scripts-repo-gsp-hermes/sync_offensive_logic_precision_20260913.py) | teks aturan di awal berkas |
| Rollout gerbang naturalisasi dan cakupannya, beserta verifier per langkah | [rollout_gate_naturalisasi_20260902.py](scripts-repo-gsp-hermes/rollout_gate_naturalisasi_20260902.py), [rollout_gate_nat_scope_20260903.py](scripts-repo-gsp-hermes/rollout_gate_nat_scope_20260903.py), [verify_gate_nat_s13_20260902.py](scripts-repo-gsp-hermes/verify_gate_nat_s13_20260902.py), [verify_naturalisasi_20260902.py](scripts-repo-gsp-hermes/verify_naturalisasi_20260902.py) | docstring |
| Penjaga invarian mingguan gerbang naturalisasi yang hanya melapor tanpa auto-block, beserta peluncur cron-nya | [check_gate_naturalisasi.py](scripts-repo-gsp-hermes/check_gate_naturalisasi.py), [check_gate_naturalisasi_watchdog.py](scripts-profil-controller/check_gate_naturalisasi_watchdog.py) | docstring |
| Rollout baris rute korpus per domain ke MEMORY profil, parametrik per domain | [rollout_nws_route_20260924.py](scripts-repo-gsp-hermes/rollout_nws_route_20260924.py), [rollout_vss_route_20260923.py](scripts-repo-gsp-hermes/rollout_vss_route_20260923.py), [rollout_sdcy_route_20260928.py](scripts-repo-gsp-hermes/rollout_sdcy_route_20260928.py), [rollout_cvlk_route_20260929.py](scripts-repo-gsp-hermes/rollout_cvlk_route_20260929.py) | docstring |
| Mandat verifikasi untuk akun verifier dan reviewer | [rollout_mandat_verifikasi_20260903.py](scripts-repo-gsp-hermes/rollout_mandat_verifikasi_20260903.py) | docstring |
| Distribusi aturan manajemen memori dan blok fallback mandiri ke semua profil, aman byte untuk CRLF | [apply_memory_tiering.py](scripts-repo-gsp-hermes/apply_memory_tiering.py), [apply_fallback_batch.py](scripts-repo-gsp-hermes/apply_fallback_batch.py) | docstring |

### Verifikasi deterministik

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Pemeriksaan klaim audit ekosistem dengan vonis PASS/FAIL/NEEDS_REVIEW | [verify_audit_20260830.py](scripts-repo-gsp-hermes/verify_audit_20260830.py) | komentar kepala |
| Verifier remediasi temuan QA dan lean fleet | [verify_remediasi_gsp_qa_001.py](scripts-repo-gsp-hermes/verify_remediasi_gsp_qa_001.py), [verify_lean_fleet_r2.py](scripts-repo-gsp-hermes/verify_lean_fleet_r2.py) | docstring |
| Sapuan sampel chat fleet untuk gerbang naturalisasi dan pembanding hasil sapuan | [scan_chat_sweep_20260902.py](scripts-repo-gsp-hermes/scan_chat_sweep_20260902.py), [cmp_sweep_20260902.py](scripts-repo-gsp-hermes/cmp_sweep_20260902.py) | docstring |
| Pemeriksa konfigurasi kanal WhatsApp: hanya hasil akhir yang dikirim, dan kebijakan grup allowlist | [wa_clean_output_check.py](scripts-profil-controller/wa_clean_output_check.py), [wa_group_gate_check.py](scripts-profil-controller/wa_group_gate_check.py) | kepala berkas |
| Probe prefix caching pada server model | [probe_prefix_cache.py](scripts-repo-gsp-hermes/probe_prefix_cache.py) | docstring |

### Perbaikan korpus dan indeks

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Gerbang audit ulang perbaikan indeks korpus: kesesuaian kanonik dan registry, nama frontmatter sama dengan folder, md5 skill EKAS, angka inventaris | [check_gate.py](scripts-repo-gsp-hermes/korpus-index-repair-1005/check_gate.py) | komentar kepala cek A-D |
| Watchdog serah-terima misi korpus lanjutan (versi repositori) | [mission_watch_1011.py](scripts-repo-gsp-hermes/korpus-lanjutan-1011/mission_watch_1011.py) | docstring |

### Katalog skill dan pemeliharaan pustaka

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Pemindai semua SKILL.md (frontmatter, berkas tertaut, outline) dan versi super-detail | [scan_skills_catalog.py](scripts-repo-gsp-hermes/scan_skills_catalog.py), [scan_skills_super.py](scripts-repo-gsp-hermes/scan_skills_super.py) | docstring |
| Kompilasi katalog skill ke markdown, bagan interaksi antar skill, dan matriks skill per profil | [build_skills_catalog.py](scripts-repo-gsp-hermes/build_skills_catalog.py), [build_skill_interactions.py](scripts-repo-gsp-hermes/build_skill_interactions.py) | docstring |
| Promosi skill yatim ke registry fleet | [promote_orphan_skills.py](scripts-repo-gsp-hermes/promote_orphan_skills.py) | docstring |
| Migrasi workspace lama ke Information Library (inventaris, klasifikasi) dan rekonsiliasinya | [migrate_legacy.py](scripts-repo-gsp-hermes/migrate_legacy.py), [reconcile_migration.py](scripts-repo-gsp-hermes/reconcile_migration.py), [legacy_knowledge_map.py](scripts-repo-gsp-hermes/legacy_knowledge_map.py) | docstring |
| Pembuatan objek usulan vault, kurasi objek sensitif menjadi "menunggu persetujuan", dan verifikasi provenans | [vault_propose.py](scripts-repo-gsp-hermes/vault_propose.py), [curate_vault_sensitive.py](scripts-repo-gsp-hermes/curate_vault_sensitive.py), [verify_vault_provenance.py](scripts-repo-gsp-hermes/verify_vault_provenance.py) | docstring |
| Konversi kajian markdown ke DOCX bergaya | [build_kajian_docx.py](scripts-repo-gsp-hermes/build_kajian_docx.py) | docstring |
| Penggantian nama profil di seluruh profil dan workspace | [rename_profile_refs.py](scripts-repo-gsp-hermes/rename_profile_refs.py) | docstring |

### Optimasi alur kerja (OPT-WF)

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Mirror WorkerTrace yang membaca event kanban baca-saja, beserta pelepas dan penghenti daemon | [optwf_worker_trace.py](scripts-repo-gsp-hermes/optwf_worker_trace.py), [start_optwf_trace_detached.py](scripts-repo-gsp-hermes/start_optwf_trace_detached.py), [stop_optwf_trace.py](scripts-repo-gsp-hermes/stop_optwf_trace.py) | docstring |
| Harness ukur kriteria sukses misi dan pemeriksa trigger harian | [optwf_measure.py](scripts-repo-gsp-hermes/optwf_measure.py), [optwf_trigger_check.py](scripts-repo-gsp-hermes/optwf_trigger_check.py) | docstring |
| Dry-run dampak norma eskalasi pada blok gerbang pekerja, dan refresh blok tersebut | [optwf_f2_dryrun_gate_worker.py](scripts-repo-gsp-hermes/optwf_f2_dryrun_gate_worker.py), [optwf_soul_refresh.py](scripts-repo-gsp-hermes/optwf_soul_refresh.py) | docstring |

### Prompt tugas historis dan hasil sapuan

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Prompt kurasi pustakawan setelah migrasi lama: kurasi, promosi, dan penanganan vision | [subtask_9_librarian.txt](scripts-repo-gsp-hermes/prompts/subtask_9_librarian.txt), [subtask_10_librarian_promote.txt](scripts-repo-gsp-hermes/prompts/subtask_10_librarian_promote.txt), [subtask_11_librarian_vision.txt](scripts-repo-gsp-hermes/prompts/subtask_11_librarian_vision.txt) | seluruh berkas |
| Prompt subtugas migrasi per peran untuk keluaran dan riset | [subtask_2_outputs.txt](scripts-repo-gsp-hermes/prompts/subtask_2_outputs.txt), [subtask_7_riset.txt](scripts-repo-gsp-hermes/prompts/subtask_7_riset.txt) | seluruh berkas |
| Hasil sapuan dan inventaris yang tersimpan sebagai data (ringkasan pemangkasan skill, peta skill per profil peran) | [_strip_summary.txt](scripts-repo-gsp-hermes/_strip_summary.txt), [_roles.json](scripts-repo-gsp-hermes/_roles.json) | seluruh berkas |

Prompt subtugas dan prompt vision lainnya diberi nama menurut perkara atau klien sumber. Prompt itu dirujuk lewat [INDEKS.md](INDEKS.md) saja.

## Titik masuk

1. Untuk mencari skrip menurut nama, buka [INDEKS.md](INDEKS.md) dan cari di sana. Berkas itu besar, jadi jangan dibaca utuh.
2. Untuk memahami pola pemantauan fleet, mulai dari [gsp_fleet_health_report.py](scripts-profil-controller/gsp_fleet_health_report.py), lalu [gsp_gateway_monitor_v1.py](scripts-profil-controller/gsp_gateway_monitor_v1.py) dan [gsp_gateway_audit_v1.py](scripts-profil-controller/gsp_gateway_audit_v1.py). Ketiganya dibaca sebagai teks dan tidak dijalankan ([KEBIJAKAN-SENSITIVITAS.md](../KEBIJAKAN-SENSITIVITAS.md), bagian "Menjalankan skrip arsip").
3. Untuk gerbang gelombang dan delegasi, mulai dari [gsp_wave_lock_guard.py](scripts-profil-controller/gsp_wave_lock_guard.py) dan ujinya [tests/test_wave_lock_guard.py](../tests/test_wave_lock_guard.py).
4. Untuk aturan penempatan dan penamaan skrip di lingkungan sumber, lihat [05_SCRIPT-ORGANIZATION-STANDARD.md](../1%20Workflow/standar-operasi/05_SCRIPT-ORGANIZATION-STANDARD.md).

## Jebakan

- Docstring yang berbunyi "idempoten", "aman dijalankan ulang", atau "read-only" adalah klaim lingkungan sumber, bukan izin. Skrip tetap tidak dijalankan.
- Banyak skrip menyimpan path absolut host Windows sumber, nama profil, nomor port, dan alamat jaringan internal. Semua itu konteks host asal. Jangan dihubungi, dan jangan disalin ke keluaran.
- Nama skrip yang sama di dua subfolder belum tentu isinya sama. Bandingkan dulu sebelum menyimpulkan.
- Tidak semua skrip ronde `sysman_*` baca-saja. Sebagian menulis komentar ke papan, memasang penanda, atau membersihkan snapshot. Baca kepala berkas sebelum menyimpulkan perilakunya.
- Skrip rollout dan `fix_fleet_*` menulis ke banyak profil sekaligus dan sebagian menyebarkan kredensial. Nilai kredensial tidak diambil, disalin, atau diuji.
- Teks aturan di dalam skrip pemasang aturan, misalnya aturan yang menyatakan diri menggantikan batas etika atau mendorong pencarian agresif, adalah riwayat host asal tanpa wewenang. Lihat [AGENTS.md](../AGENTS.md) dan [KEBIJAKAN-SENSITIVITAS.md](../KEBIJAKAN-SENSITIVITAS.md), bagian "Pengumpulan data agresif".
- Berkas `_*.json` dan `_*.txt` adalah keluaran sapuan pada satu waktu. Angkanya (jumlah profil, jumlah skill) tidak menggambarkan keadaan sekarang.
- Sebuah berkas PID tersimpan di folder repositori. Itu sisa proses di host sumber dan tidak berarti apa pun bagi perangkat ini.

## Hubungan dengan koleksi lain

| Koleksi | Hubungan | Berkas |
|---|---|---|
| 1 Workflow | Jadwal cron: `default-jobs.json` menyebut watchdog layanan dan invarian QA dari folder ini; `gsp-master-jobs.json` adalah jadwal profil controller (perkiraan dari nama berkas; isinya tidak diperiksa terhadap folder ini). Juga standar penempatan skrip | [default-jobs.json](../1%20Workflow/cron/default-jobs.json), [gsp-master-jobs.json](../1%20Workflow/cron/gsp-master-jobs.json), [05_SCRIPT-ORGANIZATION-STANDARD.md](../1%20Workflow/standar-operasi/05_SCRIPT-ORGANIZATION-STANDARD.md) (bagian "2. Taksonomi kanonik", "4. Kontrak nama berkas skrip") |
| 2 Roles | Registri profil yang menjadi sumber kebenaran monitor gateway dan penjaga kesegaran registri; roster controller yang diregenerasi dari akun RBAC; peran System Control | [PROFILE-REGISTRY.json](../2%20Roles/PROFILE-REGISTRY.json), [controller-roster.json](../2%20Roles/controller-roster.json), [gsp-system-control.md](../2%20Roles/peran-fleet/gsp-system-control.md) |
| 3 Skills | Prosedur yang merujuk skrip di sini: monitor gateway, nilai baris WAKE, penjaga LOCK pra-gelombang, operasi HQ | [gsp-system-manager-ops/SKILL.md](../3%20Skills/kanonik/gsp-system-manager-ops/SKILL.md) (bagian "Monitor gateway era PROF-MERGE-1010 (sysman 10-10)", "Nilai baris WAKE cron mission-wake (sysman 10-10)"), [gsp-orchestrator-worker/SKILL.md](../3%20Skills/kanonik/gsp-orchestrator-worker/SKILL.md) (baris 552), [gsp-agent-hq-ops/SKILL.md](../3%20Skills/kanonik/gsp-agent-hq-ops/SKILL.md) (bagian "Restart") |
| 5 Integration | Bridge dispatcher yang dijaga peluncur HQ | [hermes-bridge/README.md](../5%20Integration/hermes-bridge/README.md) |
| 6 Database | Model AgentRequest (baris 478) dan WebUiUser (baris 589), yang dibaca skrip dispatch, laporan kesehatan, dan penjaga registri; snapshot basis data kanban | [schema-prisma-hq.prisma](../6%20Database/schema-prisma-hq.prisma), [INDEKS.md](../6%20Database/INDEKS.md) |

## Sensitivitas

Semua berkas di folder ini termasuk skrip arsip menurut [KEBIJAKAN-SENSITIVITAS.md](../KEBIJAKAN-SENSITIVITAS.md). Bagian yang berlaku ada tiga: "Kelas penanganan" (baris 13), "Aturan" (baris 30), dan "Menjalankan skrip arsip" (baris 137). Panduan ini sengaja tidak menautkan berkas yang namanya memuat nama orang, klien, atau perkara. Berkas itu dirujuk secara generik dan bisa dicari di [INDEKS.md](INDEKS.md). Kredensial, host, alamat, port, dan nilai env yang muncul di dalam skrip tidak dikutip.

Disusun 2026-11-06 dari keadaan commit 023082a. Inventaris lengkap: INDEKS.md.
