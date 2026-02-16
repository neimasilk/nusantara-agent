# Handoff — Week 1 Milestone Refresh (2026-02-16)

## Konteks
- Fokus tetap: paper neuro-symbolic post-pivot.
- Eksekusi sesi ini diarahkan untuk menutup milestone Week-1 (P-001, P-003, P-004) secara end-to-end dan memperbaiki incoherence evaluasi setelah perubahan label `DISPUTED`.

## Keputusan Penting
1. Standarisasi label unresolved benchmark:
   - Label `DISPUTED`, `SPLIT`, `AMBIGUOUS` dikecualikan dari evaluasi akurasi.
2. Runner benchmark dan validator manifest diperbarui agar kompatibel dengan skema label terbaru.
3. `run_bench_gs82.py` ditambah guard `--require-llm` untuk fail-fast jika backend masih offline fallback.

## Perubahan Utama
- Utility baru: `src/utils/benchmark_contract.py`
  - `UNRESOLVED_GOLD_LABELS`
  - `is_evaluable_gold_label()`
  - `count_evaluable_cases()`
  - `resolve_manifest_evaluable_count()`
- Patch runner dan scripts:
  - `experiments/09_ablation_study/run_bench_gs82.py`
  - `experiments/09_ablation_study/run_bench_active.py`
  - `experiments/09_ablation_study/run_all_baselines.py`
  - `scripts/validate_benchmark_manifest.py`
  - `scripts/rebuild_benchmark_manifest.py`
- Test baru:
  - `tests/test_benchmark_contract.py`
- Dokumen status diperbarui:
  - `docs/task_registry_simplified.md`
  - `docs/testing_framework.md`
  - `CLAUDE.md`

## Status Milestone
- P-001: DONE
- P-003: DONE
- P-004: DONE  
  Artefak: `experiments/09_ablation_study/results_week1_refresh_2026-02-16.json`
  - `runtime_backend=llm_langgraph`
  - `total_raw_cases=24`
  - `unresolved_skipped=10`
  - `total_evaluated=14`
  - `accuracy=85.71%` (12/14)

## Validasi yang Sudah Dijalankan
- `python scripts/validate_benchmark_manifest.py` → `errors=0`
- `python experiments/09_ablation_study/run_bench_active.py --mode operational_offline --output experiments/09_ablation_study/results_week1_refresh_2026-02-16.json`
- `python scripts/run_test_suite.py` → `106/106` tests pass

## Risiko Aktif
1. Gate kualitas Week-1 belum lolos karena `Kappa=0.394` (< 0.5).
2. Dataset masih 24 dual-rated cases; 10 `DISPUTED` perlu adjudikasi human.
3. `scientific_claimable` mode tetap fail-hard selama `count_matches_reference_claim=false`.

## Langkah Berikutnya (Direkomendasikan)
1. Jalankan adjudikasi untuk 10 kasus `DISPUTED` (prioritas P-002).
2. Tambah kasus baru sampai 100+ dan re-freeze manifest.
3. Setelah data cukup, lanjut P-009 (LLM+Rules vs LLM-only) pada mode scientific-claimable.

## Prompt Singkat untuk Agen Selanjutnya
Lanjutkan dari `docs/task_registry_simplified.md` dan `docs/handoffs/handoff_week1_milestone_2026-02-16.md`. Fokus pada P-002 (adjudikasi 10 kasus DISPUTED) dan persiapan P-005 (ekspansi >100 kasus). Pertahankan kontrak evaluasi baru (`DISPUTED/SPLIT/AMBIGUOUS` tidak dievaluasi sebagai gold final), jalankan `python scripts/validate_benchmark_manifest.py` dan `python scripts/run_test_suite.py` setelah perubahan.
