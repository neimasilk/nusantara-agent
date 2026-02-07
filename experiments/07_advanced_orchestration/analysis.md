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

## Observasi Kualitatif

1. Revisi prompt debat memperketat evidence grounding, tetapi skor Kimi justru menurun dibanding baseline.
2. Jawaban menjadi lebih ringkas namun kehilangan detail penting → completeness turun.
3. Cultural framing tetap baik, namun tidak melampaui baseline pada skor evaluator.

## Keterbatasan

- Skor hanya berasal dari 1 evaluator LLM; belum ada human agreement atau inter-rater reliability.
- Hasil evaluator bergantung pada satu model Kimi; perlu validasi human untuk memastikan akurasi penilaian.
- Skala test set masih kecil (12 query) → belum cukup untuk klaim statistik.

## Implikasi untuk Paper

- Hasil awal **tidak mendukung** hipotesis peningkatan kualitas; acceptance criteria tidak terpenuhi pada evaluasi Kimi.
- Klaim harus dinyatakan sebagai **preliminary** sampai ada validasi manusia dan/atau evaluator independen tambahan.

## Rekomendasi Langkah Berikutnya

1. Analisis kegagalan: identifikasi apakah debat memperpanjang jawaban secara tidak efektif atau menambah redundansi.
2. Tambahkan minimal 20–30 query tambahan untuk mengurangi bias selection.
3. Validasi subset skor dengan human annotation (Exp 06 pipeline).
