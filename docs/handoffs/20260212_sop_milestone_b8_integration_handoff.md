# Handoff SOP Execution — 2026-02-12 (Milestone B8 Integration)

## Konteks Ringkas
Milestone lanjutan pasca handoff 2026-02-11 difokuskan pada penutupan gap operasional ART-065/066:
1. Integrasi baseline B8 (human expert) ke runner ART-065.
2. Hardening ART-066 agar tidak gagal saat menemui seed non-integer dari baseline human.
3. Sinkronisasi dokumentasi agar konsisten dengan artefak terbaru.

## Keputusan Penting
1. B8 dijalankan dari `expert_votes` pada active set (`gs_active_cases.json`) sebagai artefak operasional.
2. Seed B8 diset `human_panel` (string), bukan angka, untuk membedakan dari run stochastik B1..B7.
3. Statistik pairwise hanya memakai seed numerik berpasangan; B8 dicatat `n_pairs=0` terhadap baseline referensi.
4. Klaim ilmiah tetap tidak dipromosikan karena cakupan masih active set (22 evaluable), belum 200 kasus.

## Artefak Baru/Diupdate
- `experiments/09_ablation_study/run_all_baselines.py`
- `experiments/09_ablation_study/statistical_analysis.py`
- `experiments/09_ablation_study/results/run_all_baselines_summary.json`
- `experiments/09_ablation_study/results/statistical_analysis.json`
- `experiments/09_ablation_study/results/statistical_analysis.md`
- `experiments/09_ablation_study/results/baseline_runs/B8/run_seed_human_panel.json`
- `experiments/09_ablation_study/baselines/b8_human_expert/active_set_human_baseline_summary.json`
- `experiments/09_ablation_study/analysis.md`
- `experiments/09_ablation_study/baseline_configs.md`
- `docs/task_registry.md`

## Snapshot Hasil
- ART-065 total run: 22 (B1..B7 x 3 seed + B8 x 1 human panel).
- Mean accuracy:
  - B8: 95.45%
  - B1-B4: 59.09%
  - B5-B7: 54.55%
- ART-066: report sukses digenerate ulang, B8 masuk ranking, pairwise vs B5 untuk B8 `n_pairs=0`.

## Asumsi Aktif
1. `expert_votes` pada active set cukup untuk artefak B8 operasional.
2. B8 operasional bukan substitusi acceptance ART-064 yang mensyaratkan 200 kasus human-complete.
3. Gate scientific claim tetap mengacu ke integrity manifest dan coverage target penuh.

## Status Milestone
- Milestone-E (B8 artifact integration ke ART-065 operasional): **DONE**
- Milestone-F (ART-066 tahan seed non-integer): **DONE**
- Milestone-G (paper-grade closure 200 kasus + human complete): **IN_PROGRESS**

## Risiko yang Diketahui
1. Efek B8 tidak bisa diuji paired-test terhadap baseline referensi karena tidak punya seed numerik berpasangan.
2. Data scientific readiness Exp06 masih blocked (ART-028/030 belum memenuhi syarat).
3. Klaim performa paper-grade belum valid sampai cakupan 200 kasus terpenuhi.

## Langkah Berikutnya Direkomendasikan
1. Lengkapi ART-064 ke cakupan 200 kasus human baseline dan simpan artefak final yang setara struktur B8 saat ini.
2. Jalankan ulang ART-065/066 pada dataset paper-grade yang sudah promoted (bukan active set parsial).
3. Tambahkan protokol statistik khusus human-vs-automated yang tidak bergantung pada seed pairing (mis. uji proporsi per-kasus pada sample sama).

## Prompt Singkat Untuk Agen Selanjutnya
"Lanjutkan dari handoff `docs/handoffs/20260212_sop_milestone_b8_integration_handoff.md`. Fokus pada penutupan gap paper-grade: selesaikan ART-064 full 200 kasus, lalu rerun ART-065/066 pada dataset promoted. Pertahankan gate `scientific_claimable` dan jangan naikkan klaim jika integrity/coverage belum lolos."

## SOP Final Verification (Sesi Ini)
- Test suite: `python scripts/run_test_suite.py` -> PASS (79/79)
- Manifest validation: `python scripts/validate_benchmark_manifest.py --manifest data/benchmark_manifest.json` -> errors=0, warns=1 (reference claim mismatch acknowledged)
- Readiness check: `python experiments/06_independent_eval/assess_readiness.py` -> operational_ready=false, scientific_ready=false (expected blockers)
- Temporary artifact: tidak ada file sementara; artefak baru bersifat deliverable (`B8` run + summary)
