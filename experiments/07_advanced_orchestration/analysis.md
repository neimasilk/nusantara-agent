# Analysis — Experiment 07: Advanced Orchestration

## Ringkasan Eksekusi

- Query dieksekusi: 12 (`test_queries.json`)
- Output tersimpan di `experiments/07_advanced_orchestration/results/` per query.
- Auto-scoring dilakukan dengan Kimi (model: `kimi-k2-turbo-preview`) menggunakan rubric `rubric.md`.
- File skor: `experiments/07_advanced_orchestration/llm_scores.json`
- Ringkasan skor: `experiments/07_advanced_orchestration/score_summary.json`

## Hasil Kuantitatif (Auto-Score Kimi)

### Advanced Orchestration (Exp 07)

| Metrik | Rata-rata |
|--------|-----------|
| Accuracy | 4.1667 |
| Completeness | 4.2500 |
| Cultural Sensitivity | 4.5000 |
| Total (sum) | 12.9167 |

### Baseline Sequential (Exp 03 re-run)

| Metrik | Rata-rata |
|--------|-----------|
| Accuracy | 4.8333 |
| Completeness | 4.9167 |
| Cultural Sensitivity | 4.8333 |
| Total (sum) | 14.5833 |

### Delta (Advanced - Baseline)

| Metrik | Delta |
|--------|-------|
| Accuracy | -0.6666 |
| Completeness | -0.6667 |
| Cultural Sensitivity | -0.3333 |
| Total (sum) | -1.6666 |

Catatan: Skor ini berasal dari evaluator LLM independen (Kimi) dan **bukan** human annotation. Ini mengurangi circularity pada level evaluator, tetapi belum menggantikan validasi manusia (lihat Exp 06).

## Hasil Efisiensi (Timing)

Perhitungan dari `results/run_index.json` dan `baseline_results/run_index.json` (N=12):

| Metrik Timing | Advanced (Exp 07) | Baseline (Exp 03 re-run) | Delta |
|---------------|-------------------|---------------------------|-------|
| Rata-rata total per query | 330.2823 s | 114.9940 s | +215.2883 s |
| Rasio waktu | 2.8722x | 1.0000x | +187.22% overhead |
| Min-max total | 308.0530 - 352.0957 s | 101.2856 - 147.8283 s | - |

Breakdown komponen advanced (rata-rata):
- Retrieval parallel: 97.0656 s
- Debate: 224.0476 s
- Supervisor: 9.1691 s

## Token Probe (Post-Patch, N=3)

Setelah penambahan logging usage token di runner, dilakukan rerun subset 3 query:
- Advanced (`results_token_probe`):
  - Rata-rata total token: 31,496/query
  - Rata-rata prompt/completion: 19,695.67 / 11,800.33
  - Breakdown token: retrieval 6,905; debate 22,975; supervisor 1,616
- Baseline (`baseline_results_token_probe`):
  - Rata-rata total token: 7,364.67/query
  - Rata-rata prompt/completion: 3,357 / 4,007.67
- Delta:
  - Rasio token advanced vs baseline: 4.2766x
  - Overhead token: +327.66%

Ringkasan terstruktur token probe:
- `experiments/07_advanced_orchestration/score_summary_token_probe.json`

## Proyeksi Biaya per Model Kimi (dari Token Probe N=3)

Berdasarkan rata-rata token probe, dihitung biaya per query dan kapasitas query dalam budget $6:

| Model | Input Miss $/1M | Input Hit $/1M | Output $/1M | Adv $/query (miss) | Adv $/query (hit) | Base $/query (miss) | Base $/query (hit) |
|-------|-----------------|----------------|-------------|--------------------|--------------------|---------------------|--------------------|
| **kimi-k2.5** | 0.60 | 0.10 | 3.00 | 0.047218 | 0.037371 | 0.014037 | 0.012359 |
| kimi-k2-0905-preview | 0.60 | 0.15 | 2.50 | 0.041318 | 0.032455 | 0.012033 | 0.010523 |
| kimi-k2-0711-preview | 0.60 | 0.15 | 2.50 | 0.041318 | 0.032455 | 0.012033 | 0.010523 |
| kimi-k2-turbo-preview | 1.15 | 0.15 | 8.00 | 0.117053 | 0.097357 | 0.035922 | 0.032565 |
| kimi-k2-thinking | 0.60 | 0.15 | 2.50 | 0.041318 | 0.032455 | 0.012033 | 0.010523 |
| kimi-k2-thinking-turbo | 1.15 | 0.15 | 8.00 | 0.117053 | 0.097357 | 0.035922 | 0.032565 |

Kapasitas query maksimal dengan budget $6:

| Model | Adv max (miss) | Adv max (hit) | Base max (miss) | Base max (hit) |
|-------|----------------|---------------|-----------------|----------------|
| **kimi-k2.5** | 127 | 160 | 427 | 485 |
| kimi-k2-0905 | 145 | 184 | 498 | 570 |
| kimi-k2-0711 | 145 | 184 | 498 | 570 |
| kimi-k2-turbo | 51 | 61 | 167 | 184 |
| kimi-k2-thinking | 145 | 184 | 498 | 570 |
| kimi-k2-thinking-turbo | 51 | 61 | 167 | 184 |

Catatan:
- K2.5 lebih mahal di output ($3.00 vs $2.50) tapi lebih murah di cache hit ($0.10 vs $0.15) dibanding model k2-0905/0711/thinking.
- K2.5 punya konteks 262K token dan native multimodal — fitur yang belum dimanfaatkan eksperimen ini.
- Untuk advanced pipeline, K2.5 ~14% lebih mahal per query (miss) dibanding k2-0905 karena output price lebih tinggi.
- File detail: `kimi_budget_projection_from_probe.json`

## Observasi Kualitatif

1. Revisi prompt debat memperketat evidence grounding, tetapi skor Kimi justru menurun dibanding baseline.
2. Jawaban menjadi lebih ringkas namun kehilangan detail penting → completeness turun.
3. Cultural framing tetap baik, namun tidak melampaui baseline pada skor evaluator.

## Keterbatasan

- Skor hanya berasal dari 1 evaluator LLM; belum ada human agreement atau inter-rater reliability.
- Hasil evaluator bergantung pada satu model Kimi; perlu validasi human untuk memastikan akurasi penilaian.
- Skala test set masih kecil (12 query) → belum cukup untuk klaim statistik.
- Data token run utama N=12 tidak tersedia secara historis; token saat ini hanya tervalidasi pada rerun probe N=3.

## Implikasi untuk Paper

- Hasil awal **tidak mendukung** hipotesis peningkatan kualitas; acceptance criteria tidak terpenuhi pada evaluasi Kimi.
- Klaim harus dinyatakan sebagai **preliminary** sampai ada validasi manusia dan/atau evaluator independen tambahan.

## Rekomendasi Langkah Berikutnya

1. Analisis kegagalan: identifikasi apakah debat memperpanjang jawaban secara tidak efektif atau menambah redundansi.
2. Tambahkan minimal 20–30 query tambahan untuk mengurangi bias selection.
3. Validasi subset skor dengan human annotation (Exp 06 pipeline).
