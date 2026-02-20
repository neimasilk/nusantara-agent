# Round 7 Debate Report: Counterfactual Experiment Designer
**Agent:** DeepSeek  
**Role:** Counterfactual Designer  
**Date:** 2026-02-09  
**Phase:** R1 (BLIND—independent analysis)

---

## Ringkasan 5 Poin

1. **Akurasi B0 (41.67%) terlalu rendah untuk klaim publikasi**, namun cukup tinggi untuk pilot proof-of-concept dengan N=24.

2. **Error pattern sistematis**: Sistem over-predicts C (hallucinated conflict) dan B (missed national law priority). Dari 14 errors, 7 kasus adalah gold=A predicted=B/C—artinya sistem gagal mendeteksi dominasi hukum nasional.

3. **Root cause hypothesis**: Router mendeteksi kata kunci adat → salah route ke B/C, padahal konteks menunjukkan national law priority (HAM, administrasi publik, lex domicilii).

4. **Held-out gap kritis**: Hanya 24/82 kasus aktif. 58 kasus belum teraktivasi = 70.7% dataset belum ditest.

5. **Dependency blocker signifikan**: `clingo` dan `fitz` tidak tersedia → symbolic verification tidak berjalan end-to-end.

---

## Dua Desain Alternatif

### Alt-1: Router Priority Override

| Aspek | Deskripsi |
|-------|-----------|
| **Hipotesis** | Router gagal mendeteksi national law priority saat ada kata kunci adat |
| **Input** | 24 kasus aktif, rule-based override list (HAM, administrasi, domisili urban) |
| **Proses** | Tambahkan priority checker sebelum routing: jika query mengandung {paspor, akta, SHM, HAM, perkawinan sah negara} → force route ke A |
| **Output** | Predicted labels dengan override |
| **Metric** | Accuracy on A-gold cases (target: 5/7 → 71%) |
| **Risiko** | Over-correction: kasus legitimate C dipaksa ke A |
| **Effort** | 2-4 jam coding + 1 jam benchmark |

### Alt-2: Conflict Detection Threshold

| Aspek | Deskripsi |
|-------|-----------|
| **Hipotesis** | Sistem terlalu sensitif mendeteksi "konflik" → over-predict C |
| **Input** | 24 kasus aktif, tunable threshold |
| **Proses** | Require explicit phrase {"bertentangan", "konflik", "vs", "melawan"} untuk label C |
| **Output** | Predicted labels dengan stricter conflict detection |
| **Metric** | Precision on C-gold cases (target: 9/13 → 69%) |
| **Risiko** | Under-detection: legitimate conflict cases mislabeled |
| **Effort** | 2-4 jam coding + 1 jam benchmark |

---

## 24h Kill-Test Plan

### Objective
Membunuh asumsi paling kritis: **"Router + conflict detector sudah cukup untuk membedakan A/B/C."**

### Test Design

| Fase | Waktu | Aktivitas | Deliverable |
|------|-------|-----------|-------------|
| 1 | 0-2h | Implement Alt-1 (priority override) | `experiments/10_kill_test/alt1_priority_override.py` |
| 2 | 2-4h | Run Alt-1 on N=24 | `results_alt1.json` |
| 3 | 4-6h | Implement Alt-2 (conflict threshold) | `experiments/10_kill_test/alt2_conflict_threshold.py` |
| 4 | 6-8h | Run Alt-2 on N=24 | `results_alt2.json` |
| 5 | 8-10h | Compare B0 vs Alt-1 vs Alt-2 | `comparison_matrix.md` |
| 6 | 10-12h | Error analysis on divergent cases | `error_analysis.md` |
| 7 | 12-16h | Human expert review of 5 critical errors | Sign-off |
| 8 | 16-20h | Write final report + recommendation | `kill_test_report.md` |
| 9 | 20-24h | Buffer / iteration | — |

### Acceptance Criteria

| Criterion | Pass | Fail |
|-----------|------|------|
| Alt-1 OR Alt-2 improves accuracy by ≥10% | ✅ Continue | ❌ PIVOT |
| Either Alt fixes ≥50% of A-gold errors | ✅ Router is fixable | ❌ Architecture flaw |
| Neither Alt degrades C-gold precision below 50% | ✅ Safe | ❌ Over-correction |
| Kill-test replicable by second verifier | ✅ Valid | ❌ Redo |

---

## Top 3 Fatal Risks

### Risk 1: Sample Size Invalidates Any Conclusion
- **Evidence:** N=24, Wilson CI = [24.47%, 61.17%] — range 36.7 pp.
- **Impact:** Any improvement <15% is statistically indistinguishable from noise.
- **Mitigation:** Activate held-out set (58 kasus) before final decision.
- **File:** `data/benchmark_manifest.json:10`

### Risk 2: Error Concentration on Label A
- **Evidence:** 7/14 errors are A→B or A→C (50% of errors on 29% of cases).
- **Impact:** System systematically fails on national law priority cases.
- **Mitigation:** Priority override (Alt-1) or domain-specific A-detector.
- **File:** `experiments/09_ablation_study/results_post_patch_n24_offline_2026-02-09.json`

### Risk 3: Symbolic Verifier Inactive
- **Evidence:** `clingo` not installed; symbolic checks bypassed.
- **Impact:** Rule engine provides no actual constraint; LLM free-runs.
- **Mitigation:** P4 (infra-first freeze) or mock verification layer.

---

## Kill Shot + Counter-Plan

### 🔴 Kill Shot
> **"Arsitektur kompleks tidak memberikan nilai tambah terhadap baseline sederhana karena: (1) router gagal pada kasus A-priority, (2) symbolic verifier tidak aktif, dan (3) N=24 terlalu kecil untuk membuktikan superioritas."**

### 🟢 Counter-Plan
1. **Immediate:** Run B1 (single-agent direct prompting) on same N=24.
2. **Compare:** If B1 ≥ 35%, arsitektur kompleks tidak justify overhead.
3. **Decision:** PIVOT to P2 (baseline sederhana) + tambahkan rule post-filter.

---

## Penilaian Proposal P1–P4

| Proposal | Score | Vote | Alasan | Evidence |
|----------|-------|------|--------|----------|
| P1: Lanjut arsitektur | 2/5 | HOLD | Dependencies broken, router unfixed | clingo missing |
| P2: Pivot baseline | 4/5 | APPROVE (conditional) | Baru approve jika B1 ≥ 35% | b1_direct_prompting.py exists |
| P3: Dual-track 70/30 | 4/5 | APPROVE (fallback) | De-risk dengan eksplorasi parallel | Default if tie |
| P4: Infra-first freeze | 3/5 | HOLD | Fix infra parallel, not freeze | clingo/fitz issues |

---

## Keputusan Sementara

### Vote: **HOLD → Conditional P3**

### Syarat untuk GO:
1. 24h kill-test selesai dengan salah satu Alt pass.
2. B1 baseline benchmark tersedia untuk comparison.
3. Held-out set (≥20 kasus tambahan) teraktivasi.

### Syarat untuk PIVOT to P2:
1. Kill-test: kedua Alt fail.
2. B1 ≥ B0 (baseline sama atau lebih baik).

---

**Prepared by:** DeepSeek  
**Phase:** R1 BLIND  
**Status:** Awaiting R2 Cross-Examination
