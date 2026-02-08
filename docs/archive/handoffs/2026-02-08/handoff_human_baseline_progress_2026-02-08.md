# HANDOFF: Human Baseline Progress + Pipeline/Ablation State

Tanggal: 2026-02-08  
Branch: `main`  
Commit terakhir saat handoff: `3330118`  
Repo: `nusantara-agent`

## Ringkasan Eksekutif

1. Rule domain adat sudah ter-encode:
   1. `src/symbolic/rules/minangkabau.lp`
   2. `src/symbolic/rules/bali.lp`
   3. `src/symbolic/rules/jawa.lp`
2. Rule nasional sudah ter-encode:
   1. `src/symbolic/rules/nasional.lp`
3. Pipeline unified (`ART-049`) sudah DONE:
   1. `src/pipeline/nusantara_agent.py`
   2. `tests/test_nusantara_pipeline.py`
4. Baseline Exp09 (`ART-056` s.d. `ART-063`) sudah DONE:
   1. `experiments/09_ablation_study/baseline_configs.md`
   2. `experiments/09_ablation_study/baselines/*.py`
5. Seluruh test saat terakhir dijalankan: PASS (`79 passed`).

## State Human-Only Saat Ini

### Ahli-1 (Dr. Hendra) — sprint sudah jalan 6 batch

Dokumen terisi:
1. `docs/paket_kerja_4_jam_ahli_domain_terisi_dr_hendra_2026-02-08.md`
2. `docs/paket_kerja_4_jam_batch2_terisi_dr_hendra_2026-02-08.md`
3. `docs/paket_kerja_4_jam_batch3_terisi_dr_hendra_2026-02-08.md`
4. `docs/paket_kerja_4_jam_batch4_terisi_dr_hendra_2026-02-08.md`
5. `docs/paket_kerja_4_jam_batch5_terisi_dr_hendra_2026-02-08.md`
6. `docs/paket_kerja_4_jam_batch6_terisi_dr_hendra_2026-02-08.md`

Rekap:
1. `docs/rekap_human_baseline_sprint_2026-02-08.md`
2. Kumulatif ahli-1: **72 kasus**.

### Ahli-2 (Dr. Indra) — onboarding sudah dimulai

Dokumen:
1. Handout: `docs/paket_kerja_4_jam_ahli2_batch1_ready_to_handout.md`
2. Hasil masuk: `docs/paket_kerja_4_jam_ahli2_batch1_terisi_dr_indra_2026-02-08.md`
3. Agreement awal: `docs/agreement_report_ahli1_vs_ahli2_batch1_2026-02-08.md`

Temuan agreement awal:
1. Match literal label: **4/12 (33.3%)**.
2. Perlu kalibrasi definisi label.

Kalibrasi yang sudah disiapkan:
1. `docs/paket_kerja_4_jam_ahli2_batch2_kalibrasi_ready_to_handout.md`

## Status Task Registry (kunci)

File: `docs/task_registry.md`

1. `ART-040` DONE (Bali ASP).
2. `ART-041` DONE (Jawa ASP).
3. `ART-042` DONE (Nasional ASP).
4. `ART-049` DONE (Unified pipeline).
5. `ART-056` s.d. `ART-063` DONE (Baseline configs + baseline scripts).
6. `ART-064` masih PENDING (HUMAN_ONLY), dengan progress notes terbaru.

## Blocker Aktif

1. `ART-064` masih blocker utama karena acceptance mewajibkan:
   1. 3 ahli,
   2. cakupan 200 kasus,
   3. agreement memadai.
2. `ART-065` dan seterusnya (ablation run/statistics) belum bisa final sebelum `ART-064` cukup.

## Next Action Prioritas (untuk agent berikutnya)

1. Tunggu hasil `ahli2_batch2_kalibrasi`.
2. Setelah hasil masuk:
   1. dokumentasikan file terisi,
   2. hitung ulang agreement ahli-1 vs ahli-2,
   3. putuskan apakah langsung onboarding ahli-3 atau perlu kalibrasi batch tambahan.
3. Jaga ritme 4 jam per handout (self-contained, siap print).
4. Terus update:
   1. `docs/rekap_human_baseline_sprint_2026-02-08.md`
   2. `docs/task_registry.md`

## Catatan Operasional

1. Ada perubahan lokal yang biasa muncul: `.claude/settings.local.json` (abaikan, jangan di-commit).
2. Setiap update besar selalu:
   1. commit,
   2. push `main`,
   3. catat progress note di registry.

