# DeepSeek Round 7 R2: Kill-Test Plan (Finalized)
**Agent:** DeepSeek  
**Role:** Counterfactual Experiment Designer  
**Date:** 2026-02-09  
**Phase:** R2 (Post-Gate HOLD, Readiness for GO-P3)

---

## 1) Experiment Matrix

### Baseline (B0)
| Metric | Value | Source |
|--------|-------|--------|
| Accuracy | 41.67% (10/24) | `results_post_patch_n24_offline_2026-02-09.json` |
| Correct | 10 | — |
| Errors | 14 | — |
| A-gold recall | 0/7 (0%) | — |
| C-gold precision | ~69% (9/13) | — |

### Experiment Arms

| Arm | ID | Hipotesis | Intervensi | Target Metric |
|-----|----|-----------|------------|---------------|
| **A** | Alt-1 | Router fails on national law priority | Priority override: {paspor, akta, SHM, HAM, nikah KUA} → force A | A-gold recall ≥ 57% (4/7) |
| **B** | Alt-2 | Conflict detector terlalu sensitif | Strict threshold: require explicit {"konflik", "bertentangan"} for C | C-gold precision ≥ 77% (10/13) |
| **Control** | B0 | Status quo | No change | Accuracy = 41.67% |

---

## 2) Acceptance Criteria Numerik

### Primary Decision Thresholds

| Metric | Threshold | Pass | Fail |
|--------|-----------|------|------|
| **Accuracy improvement** | ≥ +10% (≥ 51.67%) | GO | HOLD/PIVOT |
| **A-gold recall** (Alt-1) | ≥ 4/7 (57%) | Alt-1 valid | Alt-1 invalid |
| **C-gold precision** (Alt-2) | ≥ 10/13 (77%) | Alt-2 valid | Alt-2 invalid |
| **No regression** | Neither Alt degrades B-gold recall below 50% | Safe | Unsafe |

### Decision Matrix

| Alt-1 | Alt-2 | Accuracy Δ | Decision |
|-------|-------|------------|----------|
| PASS | PASS | ≥ +10% | **GO-P3** (combine both) |
| PASS | FAIL | ≥ +10% | **GO-P3** (Alt-1 only) |
| FAIL | PASS | ≥ +10% | **GO-P3** (Alt-2 only) |
| PASS | PASS | < +10% | **HOLD** (not significant) |
| FAIL | FAIL | any | **PIVOT-P2** (baseline simpler) |

---

## 3) Run Order (24 Jam)

### Hour 0-2: Environment Prep
```powershell
# Verify dependencies
python -c "import clingo; print('clingo OK')"
python -c "import fitz; print('fitz OK')"

# Backup current state
Copy-Item "data/processed/gold_standard/gs_active_cases.json" `
          "data/processed/gold_standard/gs_active_cases_killtest_backup.json"
```
**Artifact:** `experiments/10_kill_test/env_check.log`

---

### Hour 2-4: Implement Alt-1 (Priority Override)
```python
# experiments/10_kill_test/alt1_priority_override.py
NATIONAL_PRIORITY_KEYWORDS = [
    "paspor", "akta", "SHM", "HAM", "nikah sah", 
    "KUA", "imigrasi", "pengadilan", "sertifikat"
]

def apply_priority_override(query: str, original_label: str) -> str:
    for kw in NATIONAL_PRIORITY_KEYWORDS:
        if kw.lower() in query.lower():
            return "A"  # Force national law
    return original_label
```
**Artifact:** `experiments/10_kill_test/alt1_priority_override.py`

---

### Hour 4-6: Run Alt-1 Benchmark
```powershell
cd d:\documents\nusantara-agent
$env:NUSANTARA_FORCE_OFFLINE = "1"
python experiments/10_kill_test/run_alt1.py `
  --input data/processed/gold_standard/gs_active_cases.json `
  --output experiments/10_kill_test/results_alt1.json
```
**Artifact:** `experiments/10_kill_test/results_alt1.json`

---

### Hour 6-8: Implement Alt-2 (Strict Conflict)
```python
# experiments/10_kill_test/alt2_conflict_threshold.py
EXPLICIT_CONFLICT_PHRASES = [
    "bertentangan", "konflik", "melawan", "vs", 
    "tidak sesuai", "berlawanan"
]

def apply_strict_conflict(query: str, original_label: str) -> str:
    if original_label == "C":
        has_explicit = any(p in query.lower() for p in EXPLICIT_CONFLICT_PHRASES)
        if not has_explicit:
            return "B"  # Demote to adat-only if no explicit conflict
    return original_label
```
**Artifact:** `experiments/10_kill_test/alt2_conflict_threshold.py`

---

### Hour 8-10: Run Alt-2 Benchmark
```powershell
python experiments/10_kill_test/run_alt2.py `
  --input data/processed/gold_standard/gs_active_cases.json `
  --output experiments/10_kill_test/results_alt2.json
```
**Artifact:** `experiments/10_kill_test/results_alt2.json`

---

### Hour 10-12: Comparison Analysis
```powershell
python experiments/10_kill_test/compare_results.py `
  --b0 experiments/09_ablation_study/results_post_patch_n24_offline_2026-02-09.json `
  --alt1 experiments/10_kill_test/results_alt1.json `
  --alt2 experiments/10_kill_test/results_alt2.json `
  --output experiments/10_kill_test/comparison_matrix.md
```
**Artifact:** `experiments/10_kill_test/comparison_matrix.md`

---

### Hour 12-16: Error Analysis
- Identify cases where Alt-1 and Alt-2 diverge from B0
- Categorize errors: false positive, false negative, label swap
- Document root cause per case

**Artifact:** `experiments/10_kill_test/error_analysis.md`

---

### Hour 16-20: Human Expert Review
- Review 5 critical error cases
- Sign-off on label decisions
- Document expert rationale

**Artifact:** `experiments/10_kill_test/expert_signoff.md`

---

### Hour 20-24: Final Report + Decision
```powershell
python experiments/10_kill_test/generate_report.py `
  --output experiments/10_kill_test/kill_test_report.md
```
**Artifact:** `experiments/10_kill_test/kill_test_report.md`

---

## 4) Decision Mapping

### GO-P3 Conditions
```
IF (Alt-1.accuracy >= 51.67% OR Alt-2.accuracy >= 51.67%)
   AND (no regression on B-gold)
   AND (expert signoff obtained)
THEN -> GO-P3 (dual-track with winning Alt)
```

### HOLD Conditions
```
IF (Alt-1.accuracy < 51.67% AND Alt-2.accuracy < 51.67%)
   AND (Alt-1.A-recall >= 57% OR Alt-2.C-precision >= 77%)
THEN -> HOLD (need more iteration)
```

### PIVOT-P2 Conditions
```
IF (Alt-1.accuracy < 41.67% AND Alt-2.accuracy < 41.67%)
   OR (both Alts cause regression)
   OR (B1-baseline >= B0 from separate test)
THEN -> PIVOT-P2 (abandon complex architecture)
```

---

## 5) Required Artifacts (Audit-Ready)

### Minimum Artifact Checklist

| # | Artifact | Path | Required For |
|---|----------|------|--------------|
| 1 | Environment check log | `experiments/10_kill_test/env_check.log` | Reproducibility |
| 2 | Alt-1 implementation | `experiments/10_kill_test/alt1_priority_override.py` | Code audit |
| 3 | Alt-2 implementation | `experiments/10_kill_test/alt2_conflict_threshold.py` | Code audit |
| 4 | Alt-1 results | `experiments/10_kill_test/results_alt1.json` | Metric verification |
| 5 | Alt-2 results | `experiments/10_kill_test/results_alt2.json` | Metric verification |
| 6 | Comparison matrix | `experiments/10_kill_test/comparison_matrix.md` | Decision justification |
| 7 | Error analysis | `experiments/10_kill_test/error_analysis.md` | Root cause |
| 8 | Expert signoff | `experiments/10_kill_test/expert_signoff.md` | Human validation |
| 9 | Final report | `experiments/10_kill_test/kill_test_report.md` | Decision record |
| 10 | Dataset backup | `gs_active_cases_killtest_backup.json` | Rollback |

### Audit Readiness Criteria
- [ ] All artifacts exist and are non-empty
- [ ] Results JSON parseable without errors
- [ ] Accuracy numbers traceable to individual case predictions
- [ ] Expert signoff dated and named
- [ ] Decision clearly stated with evidence links

---

## 6) Fallback Plan

### If Kill-Test Cannot Complete in 24h
1. Extend to 48h with status update at hour 24
2. Partial results acceptable if ≥1 Alt completes
3. Document blockers in `kill_test_blockers.md`

### If Expert Unavailable
1. Use 3-agent LLM-as-judge consensus (Claude, Gemini, DeepSeek)
2. Flag as "LLM-validated, pending human review"
3. Do not claim human expert signoff

---

**Prepared by:** DeepSeek  
**Status:** Ready for execution after gate PASS  
**Next Owner:** Operator (execution), Claude (gate QA)
