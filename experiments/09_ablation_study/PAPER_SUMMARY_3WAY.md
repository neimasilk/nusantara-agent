# 3-Way Statistical Comparison Summary (for Paper)

**Date:** 2026-02-19  
**Dataset:** 70 evaluable cases (74 raw, 4 skipped: AMBIGUOUS/DISPUTED/SPLIT)

---

## 1. Accuracy Overview

| Mode | Accuracy | 95% Wilson CI | Cohen's κ | Agreement Level |
|------|----------|---------------|-----------|-----------------|
| ASP-only | 58.6% (41/70) | [46.9%, 69.4%] | 0.331 | Fair |
| ASP+Ollama | 62.9% (44/70) | [51.2%, 73.3%] | 0.411 | Moderate |
| ASP+DeepSeek | 67.1% (47/70) | [55.5%, 77.0%] | 0.473 | Moderate |

**Key Finding:** DeepSeek achieves highest accuracy (+8.5 pp over ASP-only, +4.2 pp over Ollama).

---

## 2. McNemar Tests (Pairwise Significance)

| Comparison | p-value | Discordant | Better System | Significant? |
|------------|---------|------------|---------------|--------------|
| ASP-only vs Ollama | 0.5078 | 9 | Ollama (+3) | No |
| ASP-only vs DeepSeek | 0.2379 | 18 | DeepSeek (+6) | No |
| Ollama vs DeepSeek | 0.5488 | 11 | DeepSeek (+3) | No |

**Key Finding:** None of the pairwise differences reach statistical significance (α=0.05), likely due to limited sample size (n=70).

---

## 3. Inter-Rater Agreement (Fleiss' Kappa)

**Fleiss' κ = 0.623** (Substantial agreement among the 3 systems)

This indicates the three systems tend to agree with each other substantially, despite using different LLM backends.

---

## 4. Cross-Model Agreement Analysis

### Agreement Patterns

| Pattern | Count | Percentage | Description |
|---------|-------|------------|-------------|
| All 3 agree (correct) | 34 | 48.6% | Consensus correct |
| All 3 agree (wrong) | 12 | 17.1% | Consensus wrong |
| **All 3 agree (total)** | **46** | **65.7%** | High consensus rate |
| 2 agree, 1 different | 22 | 31.4% | Split decision |
| All 3 different | 2 | 2.9% | Complete disagreement |

### Majority Vote Analysis

For the 22 cases where 2 systems agree and 1 differs:
- Majority correct: 11 cases
- Majority wrong: 11 cases
- **Majority vote accuracy: 50.0%**

**Key Finding:** Majority vote does NOT improve accuracy in this scenario. When systems disagree, the majority is no more likely to be correct than random chance.

---

## 5. Per-Label Performance (F1 Scores)

| Label | ASP-only F1 | Ollama F1 | DeepSeek F1 | Best System |
|-------|-------------|-----------|-------------|-------------|
| A (National) | 0.471 | 0.444 | **0.526** | DeepSeek |
| B (Adat) | 0.633 | **0.708** | 0.697 | Ollama |
| C (Conflict) | 0.600 | 0.642 | **0.717** | DeepSeek |
| D (Error) | 0.000 | 0.000 | 0.000 | Tie (all fail) |

**Key Findings:**
- DeepSeek excels at detecting conflicts (C) with F1=0.717
- Ollama slightly better on pure adat cases (B)
- All systems fail on label D (insufficient training data, n=2)

---

## 6. Confusion Matrices

### ASP-only
```
G\P | A | B  | C  | D
----+---+----+----+--
A   | 4 | 0  | 1  | 1
B   | 4 | 19 | 8  | 0
C   | 3 | 10 | 18 | 0
D   | 0 | 0  | 2  | 0
```

### ASP+Ollama
```
G\P | A | B  | C  | D
----+---+----+----+--
A   | 4 | 1  | 1  | 0
B   | 4 | 23 | 3  | 1
C   | 4 | 9  | 17 | 1
D   | 0 | 1  | 1  | 0
```

### ASP+DeepSeek
```
G\P | A | B  | C  | D
----+---+----+----+--
A   | 5 | 0  | 1  | 0
B   | 6 | 23 | 2  | 0
C   | 2 | 10 | 19 | 0
D   | 0 | 2  | 0  | 0
```

---

## 7. Implications for Paper

1. **LLM Choice Matters, But Not Dramatically:** DeepSeek performs best but differences are not statistically significant with n=70.

2. **High Consensus Among Systems:** 65.7% of cases see all 3 systems agreeing, suggesting the ASP+LLM architecture provides consistent predictions regardless of LLM backend.

3. **Majority Vote Not Helpful:** When systems disagree, majority vote offers no advantage (50% accuracy).

4. **Label D Challenge:** All systems fail on the 2 cases requiring label D, indicating a systematic blind spot for "unclear/error" classifications.

5. **Cohen's Kappa Interpretation:** All systems achieve at least "Fair" agreement with gold standard, with DeepSeek reaching "Moderate" (κ=0.473).

---

## Files Generated

- `experiments/09_ablation_study/statistical_comparison_3way_2026-02-19.json` - Full statistical results
- `experiments/09_ablation_study/PAPER_SUMMARY_3WAY.md` - This summary

---

*Generated for Nusantara-Agent paper, February 2026*
