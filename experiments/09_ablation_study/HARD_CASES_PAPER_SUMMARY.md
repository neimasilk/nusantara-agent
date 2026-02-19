# Hard Cases Analysis Summary (for Paper)

**Analysis Date:** 2026-02-19  
**Scope:** 12 cases (17.1%) where ASP-only, ASP+Ollama, and ASP+DeepSeek all fail  
**Dataset:** 70 evaluable cases from Gold Standard

---

## Executive Summary

From 70 evaluable cases, **12 cases (17.1%)** represent "hard cases" where all three system variants (ASP-only, ASP+Ollama, ASP+DeepSeek) produce incorrect predictions. This analysis identifies patterns in these failures to guide future improvements.

---

## 1. Gold Label Distribution in Hard Cases

| Gold Label | Count | Percentage | Interpretation |
|------------|-------|------------|----------------|
| **C (Conflict)** | 6 | 50.0% | Over-represented vs. overall distribution (44%) |
| **B (Adat)** | 5 | 41.7% | Slightly over-represented vs. overall (44%) |
| **A (National)** | 1 | 8.3% | Under-represented vs. overall (9%) |
| **D (Error/Unclear)** | 0 | 0.0% | Not in hard cases (though system always fails on D) |

**Key Finding:** Conflict (C) cases are the most challenging, representing half of all hard cases.

---

## 2. Failure Pattern Analysis

| Pattern | Count | Description |
|---------|-------|-------------|
| **Conflict → Adat** | 4 | Gold=C, all systems predict B |
| **Adat → National** | 3 | Gold=B, all systems predict A |
| **Adat → Conflict** | 2 | Gold=B, all systems predict C |
| **Conflict → National** | 2 | Gold=C, all systems predict A |
| **National → Conflict** | 1 | Gold=A, all systems predict C |

**Key Findings:**

1. **Conflict Misclassification (50% of hard cases):** Systems struggle most with detecting conflicts
   - 4 cases: Conflict misclassified as pure Adat
   - 2 cases: Conflict misclassified as pure National

2. **Adat Over-prediction:** When systems fail, they tend to over-predict Adat (B)
   - 4 conflict cases → predicted as Adat
   - 3 adat cases → predicted as National (under-predicting adat)

3. **Systematic Bias:** All 3 systems fail identically, indicating the issue is in the **shared ASP rule set** or **router/prompt design**, not the LLM backend.

---

## 3. Domain Distribution

| Domain | Count | Percentage | Notes |
|--------|-------|------------|-------|
| **Minangkabau** | 4 | 33.3% | Land/inheritance conflicts |
| **General/Unknown** | 4 | 33.3% | Generic legal concepts |
| **Bali** | 2 | 16.7% | Inheritance, women's rights |
| **Lintas-Daerah** | 1 | 8.3% | Cross-region marriages |
| **Jawa** | 1 | 8.3% | Gono-gini rules |

**Key Finding:** Minangkabau cases are over-represented in failures (33% of hard cases vs. ~40% overall), particularly around:
- Harta pusako (inherited property)
- Inter-ethnic marriages
- Joint property (harta bersama)

---

## 4. Detailed Case Breakdown

### Case List (All 12 Hard Cases)

| # | Case ID | Domain | Gold | Predicted | Pattern | Key Issue |
|---|---------|--------|------|-----------|---------|-----------|
| 1 | CS-LIN-016 | Lintas-Daerah | A | C | National→Conflict | Mixed-ethnic Jakarta family |
| 2 | CS-MIN-004 | Minangkabau | C | B | Conflict→Adat | Joint business property |
| 3 | CS-MIN-005 | Minangkabau | C | B | Conflict→Adat | Pusako rendah donation |
| 4 | CS-MIN-015 | Minangkabau | C | B | Conflict→Adat | Marriage without KAN approval |
| 5 | GS-0014 | Bali | B | A | Adat→National | Druwe gabro property |
| 6 | GS-0019 | General | B | A | Adat→National | Gono-gini definition |
| 7 | GS-0020 | General | B | A | Adat→National | Divorce property division |
| 8 | GS-0028 | Bali | B | C | Adat→Conflict | Women's inheritance rights |
| 9 | GS-0030 | Jawa | B | C | Adat→Conflict | Gono-gini bilateral rules |
| 10 | GS-0033 | General | C | A | Conflict→National | Wife's share interpretation |
| 11 | GS-0034 | General | C | A | Conflict→National | Pluralistic decision |
| 12 | GS-0041 | Minangkabau | C | B | Conflict→Adat | Pusako tinggi mamak authority |

---

## 5. Root Cause Analysis

### Pattern 1: Conflict Detection Failure (6 cases)
**Gold=C, predicted as A or B**

Common characteristics:
- Cases involve **overlapping national and adat jurisdictions**
- Query text contains **strong adat keywords** (pusako, gono-gini, druwe)
- **Conflict keywords are subtle** or implied rather than explicit

Example (CS-MIN-004):
> "Sepasang suami istri di Minangkabau memiliki harta dari hasil usaha bersama..."

Systems see "Minangkabau" + "harta" → predict B (Adat), missing the conflict between joint property rules and inheritance laws.

### Pattern 2: Adat Under-recognition (3 cases)
**Gold=B, predicted as A**

Common characteristics:
- Cases describe **general legal concepts** (gono-gini, property division)
- **Domain markers are weak** or absent
- Systems default to national law when uncertain

### Pattern 3: Over-conflict Prediction (3 cases)
**Gold=B, predicted as C** or **Gold=A, predicted as C**

Common characteristics:
- Cases involve **rights tensions** (women's inheritance, inter-ethnic marriage)
- Systems interpret any tension as "conflict"

---

## 6. Recommendations for Paper

### Short-term (Implementation)

1. **Enhanced Conflict Detection**
   - Add explicit rules for "joint property" (harta bersama/gono-gini) which often triggers hidden conflicts
   - Strengthen keyword detection for implied conflicts ("mendahului", "tidak sah", "perselisihan")

2. **Domain-aware Classification**
   - Improve domain detection for "General/Unknown" cases
   - Add fallback rules when domain is unclear

3. **Label D Handling**
   - Current system never correctly predicts D
   - Add explicit training examples for edge cases
   - Consider confidence threshold: low confidence → predict D

### Medium-term (Research)

4. **Case-based Prompt Engineering**
   - Add these 12 cases to in-context learning examples
   - Evaluate if few-shot prompting improves performance

5. **Rule Set Expansion**
   - Minangkabau joint property rules need refinement
   - Bali women's inheritance rights need explicit handling

6. **Ensemble Strategy**
   - When systems disagree (31.4% of cases), current majority vote is no better than random (50%)
   - Consider confidence-weighted voting or meta-classifier

---

## 7. Impact on Overall Results

| Metric | Current | Potential (if hard cases fixed) |
|--------|---------|--------------------------------|
| ASP-only | 58.6% | 75.7% (+17.1 pp) |
| ASP+Ollama | 62.9% | 80.0% (+17.1 pp) |
| ASP+DeepSeek | 67.1% | 84.3% (+17.1 pp) |

**Key Insight:** Fixing these 12 systematic failures would improve all systems to **>75% accuracy**, with DeepSeek potentially reaching **84.3%**.

---

## Files Generated

- `experiments/09_ablation_study/hard_cases_analysis_2026-02-19.json` - Full analysis data
- `experiments/09_ablation_study/HARD_CASES_PAPER_SUMMARY.md` - This summary

---

*For Nusantara-Agent Paper - Error Analysis Section*
