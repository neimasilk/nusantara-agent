# Inter-Rater Agreement Analysis
**Tanggal:** 2026-02-12
**Task:** P-001
**Input:** data/processed/gold_standard/gs_active_cases.json (24 cases)

---

## DECISION: Ahli-3 Removed

**Owner confirmed** Ahli-3 should be removed from the gold standard. Reason: under-qualified (S1 level, bukan ahli domain). The IRA analysis below documents both the original 3-rater findings and the post-removal 2-rater state.

**Action taken:**
- `ahli3` votes removed from `gs_active_cases.json`
- Original 3-rater data backed up to `gs_active_cases_backup_3raters.json`
- Gold labels recomputed using Ahli-1 + Ahli-2 only
- 10 cases where Ahli-1 and Ahli-2 disagree marked as `DISPUTED`

---

## Phase 1: Original 3-Rater Analysis (Historical Record)

| Metric | Value | Interpretation |
|---|---|---|
| Fleiss' Kappa (24 cases) | 0.102 | Slight agreement |
| Fleiss' Kappa (22 non-SPLIT) | 0.151 | Slight agreement |
| Krippendorff's Alpha (24) | 0.114 | Far below 0.667 threshold |
| Krippendorff's Alpha (22) | 0.164 | Far below 0.667 threshold |
| Average pairwise agreement | 43.1% | Low |
| Unanimous cases | 5/24 (20.8%) | Very low |

### Pairwise Cohen's Kappa (3 raters)

| Pair | Kappa | Interpretation |
|---|---|---|
| Ahli-1 vs Ahli-2 | 0.394 | Fair |
| Ahli-1 vs Ahli-3 | -0.015 | **Worse than chance** |
| Ahli-2 vs Ahli-3 | -0.006 | **Worse than chance** |

### Ahli-3 Deviation

| Rater | Deviates from both others | Rate |
|---|---|---|
| Ahli-1 | 8/24 | 33.3% |
| Ahli-2 | 5/24 | 20.8% |
| Ahli-3 | 12/24 | **50.0%** |

### Disagreement Patterns (3 raters)

| Pattern | Count | Interpretation |
|---|---|---|
| A vs C | 21 | Raters can't distinguish "National" from "Conflict" |
| B vs C | 14 | Raters can't distinguish "Adat" from "Conflict" |
| C vs D | 3 | Minor |
| A vs B | 2 | Rare — raters agree on the A/B distinction |

---

## Phase 2: Post-Removal (Ahli-1 + Ahli-2 Only)

| Metric | Value | Interpretation |
|---|---|---|
| Cohen's Kappa | 0.394 | Fair agreement |
| Raw agreement | 58.3% (14/24) | Moderate |
| Agreed cases | 14 | Usable as high-confidence gold standard |
| Disputed cases | 10 | Need adjudication by qualified expert |

### Label Distribution (14 agreed cases)

| Label | Count | Cases |
|---|---|---|
| B (Adat) | 4 | CS-MIN-004, CS-MIN-013, CS-BAL-014, CS-BAL-009 |
| C (Conflict) | 8 | CS-BAL-002, CS-JAW-015, CS-LIN-016, CS-BAL-012, CS-LIN-018, CS-NAS-022, CS-MIN-025, (plus CS-LIN-052 relabeled) |
| A (National) | 1 | CS-NAS-010 |
| D (Insufficient) | 1 | CS-LIN-052 |

Note: CS-LIN-017 (A, unanimous) also agreed.

### 10 Disputed Cases (Need Adjudication)

| Case | Ahli-1 | Ahli-2 | Old Gold | Status |
|---|---|---|---|---|
| CS-MIN-011 | D | A | C | DISPUTED — old label was from Ahli-3 tie-break |
| CS-JAW-006 | A | C | A | DISPUTED |
| CS-NAS-066 | A | C | A | DISPUTED |
| CS-MIN-005 | B | C | SPLIT | DISPUTED (was already SPLIT) |
| CS-JAW-011 | A | C | C | DISPUTED |
| CS-MIN-015 | C | B | SPLIT | DISPUTED (was already SPLIT) |
| CS-JAW-019 | B | C | C | DISPUTED |
| CS-BAL-020 | B | C | C | DISPUTED |
| CS-NAS-041 | A | C | C | DISPUTED |
| CS-JAW-030 | B | C | C | DISPUTED |

**Pattern in disputes:** 8 of 10 disputed cases involve one rater choosing C (conflict/synthesis) vs the other choosing A or B. This confirms A-vs-C ambiguity is the dominant challenge.

---

## Implications for Paper

### Current State
- **14 high-confidence cases** with Ahli-1+Ahli-2 agreement (Cohen's Kappa = 0.394)
- **10 disputed cases** requiring a 3rd qualified expert or adjudication session
- **Kappa = 0.394** is "fair" — reportable but with limitations acknowledged

### Recommended Next Steps
1. [x] Remove Ahli-3 (confirmed under-qualified)
2. [x] Recompute gold labels with 2 qualified raters
3. [ ] **PRIORITY**: Adjudicate 10 disputed cases — have Dr. Hendra (Ahli-1) and Dr. Indra (Ahli-2) discuss disagreements with clear criteria
4. [ ] Recruit Ahli-4/Ahli-5 (qualified, M.H./S2+ level) for additional annotation
5. [ ] Consider collapsing A+C categories to reduce ambiguity
6. [ ] Expand dataset to 100+ cases with new qualified raters

### For the Paper
- Report honestly: "Initial 3-rater IRA was low (Kappa=0.102) due to one under-qualified rater"
- Report post-removal: "After excluding the outlier, 2-rater Kappa = 0.394 (fair)"
- Use agreed subset (14 cases) for primary accuracy analysis
- Use disputed cases to illustrate task difficulty and ambiguity
- The A-vs-C confusion is itself a domain finding worth discussing

---

## Impact on Prior Accuracy Claims

**ALL prior accuracy claims are invalidated** for the old gold standard:
- "41.67% accuracy" — computed against labels partly determined by Ahli-3
- "72.73% accuracy" — same issue

**Going forward**, accuracy should only be reported on:
- The 14 agreed cases (high-confidence subset)
- Any newly adjudicated cases with documented agreement
- With IRA reported alongside accuracy as a quality indicator
