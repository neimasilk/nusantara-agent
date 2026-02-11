# PROTOCOL (Pre-Registration) — Experiment 06: Independent Evaluation Pipeline

**[PRE-REGISTRATION]** Dokumen ini menyiapkan eksekusi evaluasi independen untuk memutus circular evaluation.

---

## 1. Metadata

| Field | Isi |
|-------|-----|
| **ID Eksperimen** | `06_independent_eval` |
| **Tanggal Pre-registration** | 2026-02-07 |
| **Prasyarat** | ART-028, ART-029, ART-030 |
| **Status** | BLOCKED (menunggu ART-028 dan ART-030) |

## 2. Hipotesis

> Evaluasi independen (human annotator + LLM judge non-DeepSeek + putusan MA) akan menghasilkan metrik yang lebih kredibel dan mengurangi bias self-evaluation.

## 3. Acceptance Criteria

| Metrik | Target |
|--------|--------|
| Krippendorff's Alpha | >= 0.667 |
| Cohen's Kappa (LLM judge vs human) | >= 0.6 |
| Laporan metrik | Precision/Recall/F1 + confidence interval |

## 4. Input dan Output

- Input:
  - `data/raw/gold_standard_texts/`
  - `data/processed/gold_standard/annotations/`
  - `data/raw/ma_decisions/`
  - `src/evaluation/llm_judge.py`
- Output:
  - `experiments/06_independent_eval/results/`
  - `experiments/06_independent_eval/analysis.md`

## 5. Langkah Eksekusi (setelah unblock)

1. Jalankan precheck artefak:
   - `python experiments/06_independent_eval/run_precheck.py`
   - `python experiments/06_independent_eval/assess_readiness.py`
2. Konsolidasi anotasi manusia.
3. Jalankan penilaian LLM independen.
4. Hitung metrik dan confidence interval.
5. Tulis analisis dan review.
