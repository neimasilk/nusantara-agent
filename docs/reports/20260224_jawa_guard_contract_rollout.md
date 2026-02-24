# Rollout Jawa Guard v1 + Reasoning Contract Gate

**Tanggal:** 2026-02-24  
**Tujuan:** mengeksekusi tindak lanjut audit Jawa: (1) guard anti B->A untuk konteks Jawa bilateral, (2) kontrak metadata reasoning agar diagnosis layer tetap claimable.

## Perubahan Kode

1. `src/config/domain_keywords.py`
- Tambah `SUPERVISOR_JAWA_BILATERAL_KEYWORDS`.
- Tambah `SUPERVISOR_NATIONAL_HARD_KEYWORDS`.

2. `src/agents/orchestrator.py`
- Prompt adjudikator diperkuat dengan **JAWA_GUARD_V1**:
  - jika sinyal Jawa bilateral kuat dan constraint nasional keras tidak terdeteksi, jangan pilih A kecuali ada dasar nasional keras/konflik eksplisit.
- Warning router kini memuat sinyal guard tersebut agar model mendapat prior yang eksplisit.

3. `src/pipeline/nusantara_agent.py`
- Ditambahkan **deterministic post-adjudication guard**:
  - ketika output supervisor = `A`, konteks Jawa bilateral kuat, tanpa constraint nasional keras, dan tanpa conflict signal/symbolic conflict -> override ke `B`.
  - output diberi marker `jawa_guard_v1="applied"` agar traceable.

4. `src/utils/reasoning_contract.py` (baru)
- Parser reasoning JSON robust.
- Ringkasan kontrak metadata reasoning:
  - field wajib: `label`, `langkah_keputusan`, `alasan_utama`, `konflik_terdeteksi`.
  - flag `claimable_for_layer_diagnosis`.

5. Integrasi gate ke runner benchmark
- `experiments/09_ablation_study/run_dual_benchmark.py`
  - menulis `reasoning_metadata_contract` pada output.
  - mode `scientific_claimable` untuk `asp_llm` sekarang fail-hard jika kontrak metadata tidak lengkap.
- `experiments/09_ablation_study/run_bench_gs82.py`
  - menulis `reasoning_metadata_contract`.
  - mode `scientific_claimable` fail-hard jika kontrak metadata tidak lengkap (dengan artefak fail yang tetap tersimpan).
- `experiments/09_ablation_study/run_single_mode.py`
  - menulis `reasoning_metadata_contract` pada checkpoint/output.

6. Testing
- `tests/test_reasoning_contract.py` (baru): parser + summary contract.
- `tests/test_nusantara_pipeline.py`: tambah test override/non-override Jawa guard.

## Validasi

1. Full test suite:
- `python scripts/run_test_suite.py` -> **128/128 PASS**.

2. Smoke run dual benchmark (operasional):
- Command: `python experiments/09_ablation_study/run_dual_benchmark.py --mode operational_offline --dataset-split dev`
- Output:
  - `results_dual_asp_only_dev_2026-02-24.json`
  - `results_dual_asp_llm_dev_2026-02-24.json`
- Kontrak metadata:
  - ASP-only dev: `49/49` lengkap, claimable `True`.
  - ASP+LLM dev: `49/49` lengkap, claimable `True`.

3. Targeted regression check (shared B->A Jawa):
- Output: `experiments/09_ablation_study/jawa_guard_targeted_check_2026-02-24.json`
- Kasus: `GS-0019`, `GS-0020`, `GS-0031`
- Baseline lama (canonical deepseek 2026-02-20): semua `A`
- Hasil terbaru: semua `B` (3/3 sesuai gold B)

## Catatan

- Untuk arsip historis, beberapa file eksploratori lama memang tidak memenuhi kontrak penuh:
  - `results_dual_asp_llm_gpt_oss_20b_2026-02-23.json`: `66/70` lengkap.
  - `results_dual_asp_llm_qwen3_14b_2026-02-23.json`: `69/70` lengkap.
- Dengan gate baru, kondisi ini akan otomatis ditandai non-claimable di mode `scientific_claimable`.
