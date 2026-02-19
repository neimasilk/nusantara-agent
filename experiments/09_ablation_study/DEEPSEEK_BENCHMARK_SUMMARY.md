# DeepSeek Cross-Validation Benchmark - Final Summary

**Date:** 2026-02-19  
**Mode:** asp_llm (ASP+LLM hybrid)  
**Backend:** deepseek (via llm_langgraph runtime)

---

## Overall Results

| Metric | Value |
|--------|-------|
| Total Cases Evaluated | 70 |
| Correct Predictions | 47 |
| **Accuracy** | **67.1%** |
| Wilson 95% CI Lower | 55.5% |
| Wilson 95% CI Upper | 77.0% |

---

## Per-Label Performance

| Label | Support | Precision | Recall | F1-Score (calc) |
|-------|---------|-----------|--------|-----------------|
| A | 6 | 38.5% | 83.3% | 52.6% |
| B | 31 | 65.7% | 74.2% | 69.7% |
| C | 31 | 86.4% | 61.3% | 71.7% |
| D | 2 | 0.0% | 0.0% | 0.0% |

---

## Comparison with Baseline

| Backend | Accuracy | Delta |
|---------|----------|-------|
| Ollama (baseline) | 70.0% | - |
| **DeepSeek** | **67.1%** | -2.9 pp |

DeepSeek performed slightly below the Ollama baseline by 2.9 percentage points,
though the difference falls within the Wilson 95% confidence interval.

---

## Key Observations

1. **Label C Performance**: Highest precision (86.4%) but lower recall (61.3%)
   - Model is conservative when predicting C, rarely wrong but misses some C cases

2. **Label A Performance**: High recall (83.3%) but low precision (38.5%)
   - Model tends to over-predict A, catching most true A cases but with many false positives

3. **Label D Performance**: Complete failure (0% precision, 0% recall)
   - Only 2 support cases, insufficient data to learn D patterns

4. **Label B Performance**: Balanced precision/recall, largest support (31 cases)

---

## Error Analysis

- **No runtime errors** - All 70 cases processed successfully
- 23 cases were misclassified (32.9% error rate)

---

## Files Generated

- `results_deepseek_asp_llm_2026-02-19.json` - Full results with per-case predictions
- `DEEPSEEK_BENCHMARK_SUMMARY.md` - This summary report

---

## Notes

- Skipped labels: AMBIGUOUS, DISPUTED, SPLIT (4 cases skipped from 74 total)
- Checkpoint saved every 5 cases for resume capability
- Timeout per case: 60 seconds
