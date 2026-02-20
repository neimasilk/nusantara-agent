# Round 7 R1 (BLIND) — Kimi Ops Reliability Report

**Tanggal:** 2026-02-09  
**Peran:** Ops Reliability + Execution Checklist  
**Mode:** Independent Analysis (BLIND)  
**Input Files:** 7 dokumen konteks

---

## Ringkasan 5 Poin

1. **Baseline B0 (Current Official)** terkunci di N=24 kasus dengan akurasi offline 41.67% (Wilson CI: 24.47%-61.17%), consensus strength 100%, tie rate 0% — namun rentan terhadap overfitting pada set kecil.

2. **4 Proposal (P1-P4)** dievaluasi: P1 (lanjut arsitektur) berisiko validitas rendah; P2 (pivot baseline) mengorbankan arsitektur yang sudah dibangun; P3 (dual-track 70/30) paling fleksibel; P4 (infra-first) aman tapi stagnan.

3. **Dependency Blocker HARD** ditemukan pada 2 item: (a) environment LLM parity belum terverifikasi, (b) held-out set (N=58 sisa dari klaim 82) belum dipromosikan ke active benchmark.

4. **Risk Escalation** tertinggi: klaim publikasi dini berbasis N=24 tanpa held-out validation akan merusak kredibilitas jika disubmisikan ke venue NLP tier-1.

5. **Rekomendasi Keputusan Sementara:** `P3-DUAL-TRACK` dengan syarat: (a) frozen B0 untuk stabilisasi, (b) eksplorasi B1/B2 paralel selama 7 hari, (c) held-out promotion sebelum klaim publik.

---

## Action Checklist (7 Hari)

| # | Task | Owner | Due | Output | Blocker |
|---|------|-------|-----|--------|---------|
| 1 | Freeze B0 dataset version + manifest lock | Kimi | D+0 | `gs_active_cases.frozen_20260209.json` + manifest signed | None |
| 2 | Run LLM-mode parity benchmark (same N=24) | Codex/Claude | D+2 | `results_b0_llm_mode_n24_2026-02-11.json` | API key valid, rate limit |
| 3 | Promote held-out set (N=58) dari klaim 82 | Gemini/Human | D+3 | `gs_heldout_58_cases.json` dengan gold labels | Expert vote coverage >=3 per kasus |
| 4 | Implement B1 (single-agent + symbolic) | DeepSeek | D+5 | `src/baselines/b1_single_symbolic.py` + hasil N=24 | Clingo install (soft blocker) |
| 5 | Implement B2 (retrieval-first minimal) | DeepSeek | D+5 | `src/baselines/b2_retrieval_minimal.py` + hasil N=24 | None |
| 6 | Dual-track evaluation report | Codex | D+7 | `docs/handoffs/20260216_round7_p3_evaluation.md` | Tasks 1-5 complete |
| 7 | Dependency install validation | Kimi | D+1 | `logs/dependency_check_20260210.log` dengan clingo+fitz OK | Admin access (hard blocker?) |
| 8 | Git version tag untuk B0 | Kimi | D+0 | Tag `v0.2-b0-frozen` di commit freeze | None |
| 9 | Update paper draft (limitations section) | Human | D+3 | `paper/main.tex` revision dengan CI Wilson | None |
| 10 | Risk re-assessment checkpoint | All | D+7 | Go/No-Go decision untuk publikasi | Tasks 6 completion |

---

## Dependency Gate

### HARD Blockers (Eksperimen Invalid Tanpa Ini)

| ID | Dependency | Evidence | Impact | Mitigasi |
|----|-----------|----------|--------|----------|
| HB-1 | Held-out set N=58 promoted | `data/benchmark_manifest.json` line 22: "declared_total_cases: 82" vs "total_cases_actual: 24" | Klaim generalisasi tidak valid | Promote 58 kasus dengan gold labels lengkap (min 3 expert votes) |
| HB-2 | LLM-mode parity verified | File `results_post_patch_n24_offline_2026-02-09.json` hanya offline mode | Perbandingan offline vs LLM tidak ada; risk mode variance | Jalankan `run_bench_active.py` dengan mode LLM, bandingkan confidence interval overlap |
| HB-3 | Expert-4 coverage 24/24 | `20260209_codex_arxiv_go_snapshot.md` line 12: "Expert-4 coverage: 16/24" | 8 kasus tanpa expert-4 vote; risk label instability | Ingest follow-up Ahli-4 untuk 8 kasus remaining (gunakan paket yang sudah disiapkan) |

### SOFT Blockers (Dapat Dikerjakan dengan Fallback)

| ID | Dependency | Evidence | Workaround |
|----|-----------|----------|------------|
| SB-1 | Clingo installed | `paper/main.tex` line 236: "full symbolic/PDF suite is blocked by missing optional dependencies (clingo, fitz)" | Gunakan mock symbolic engine untuk B1; tag hasil sebagai "partial" |
| SB-2 | Fitz (PyMuPDF) installed | Same as SB-1 | Skip PDF extraction tests; fokus pada text-based cases |
| SB-3 | Held-out evaluation complete | Timeline 7 hari mungkin tidak cukup untuk N=58 full evaluation | Sample 20 kasus held-out sebagai proxy; extrapolate dengan caveats |

---

## Risk Escalation List

| Priority | Risk | Likelihood | Impact | Detection | Mitigation Owner |
|----------|------|------------|--------|-----------|------------------|
| P0 | Premature submission ke venue tier-1 dengan klaim performa | Medium | **FATAL** — Reputasi, retraction risk | Reviewer scrutiny | Human PI |
| P1 | Label gold berubah lagi (expert-4 coverage incomplete) | Medium | High — Metrics invalidate | `audit_gold_vs_votes.py` mismatch >0 | Gemini |
| P2 | LLM-mode tidak reproducible (API variance) | High | High — Claim invalid | Wilson CI tidak overlap offline-vs-LLM | Claude |
| P3 | Dual-track resource split menyebabkan kedua track gagal | Low | Medium — Delay 2 minggu | Progress check D+3 | Codex |
| P4 | Dependency clingo/fitz tidak terselesaikan dalam 7 hari | Medium | Low — Fallback mock OK | D+1 dependency check | Kimi |
| P5 | Overfitting pada N=24 tidak terdeteksi | Medium | High — Generalisasi buruk | Held-out accuracy << pilot accuracy | DeepSeek |

---

## Top 3 Fatal Risks

### Fatal Risk #1: Publication Claim Without Held-Out Validation
**Bukti:** `paper/main.tex` line 258: "ready for an internal/working preprint draft, but not yet ready for a strong public NLP preprint claim"
**Kill Shot:** Jika disubmit ke ACL/EMNLP dengan N=24 pilot-only, reviewer akan menolak dengan alasan sample size dan overfitting.
**Counter-Plan:** Hold submission sampai held-out N>=50 dievaluasi; gunakan 7 hari untuk data collection, bukan tuning.

### Fatal Risk #2: Label Instability from Incomplete Expert-4 Coverage
**Bukti:** `20260209_codex_arxiv_go_snapshot.md` line 12: "Expert-4 coverage: 16/24"
**Kill Shot:** 8 kasus tanpa expert-4 vote bisa berubah gold label jika expert-4 memberi vote kontradiktif; patch gold label akan invalidate semua benchmark results.
**Counter-Plan:** Prioritize ingest Ahli-4 follow-up untuk 8 kasus sebelum D+2; freeze label setelah 24/24 coverage.

### Fatal Risk #3: Mode Variance (Offline vs LLM) Not Quantified
**Bukti:** `results_post_patch_n24_offline_2026-02-09.json` hanya offline; tidak ada file LLM-mode equivalent
**Kill Shot:** Klaim "neuro-symbolic multi-agent" tidak bisa diverifikasi jika LLM-mode tidak pernah diuji; risk arsitektur hanya bekerja di offline fallback.
**Counter-Plan:** Task #2 wajib sebelum D+2; jika Wilson CI offline vs LLM tidak overlap, escalate ke PIVOT decision.

---

## Runbook Command-by-Command (Paling Aman)

### Pre-Execution (D+0)
```bash
# 1. Backup dan freeze
$ cp data/processed/gold_standard/gs_active_cases.json \
    data/processed/gold_standard/gs_active_cases.frozen_20260209.json

# 2. Git tag
$ git tag -a v0.2-b0-frozen -m "Freeze B0: N=24, consensus 100%, offline accuracy 41.67%"
$ git push origin v0.2-b0-frozen

# 3. Dependency check
$ python -c "import clingo; print('clingo OK')" 2>&1 | tee logs/dep_clingo.log
$ python -c "import fitz; print('fitz OK')" 2>&1 | tee logs/dep_fitz.log
$ python -c "import openai; print('openai OK')" 2>&1 | tee logs/dep_openai.log

# 4. Validate manifest
$ python scripts/validate_benchmark_manifest.py --strict 2>&1 | tee logs/manifest_validation_d0.log
```

### Execution Phase (D+1 sampai D+7)

```bash
# D+1: Held-out promotion prep
$ python scripts/promote_heldout_cases.py \
    --source docs/gold_standard_consensus_report_complete_82_cases_2026-02-08.md \
    --target-active 24 \
    --target-heldout 58 \
    --output data/processed/gold_standard/gs_heldout_58_cases.json

# D+2: LLM-mode parity run
$ export NUSANTARA_LLM_MODE=1
$ python experiments/09_ablation_study/run_bench_active.py \
    --manifest data/benchmark_manifest.json \
    --mode llm \
    --output experiments/09_ablation_study/results_b0_llm_mode_n24_2026-02-11.json

# D+3: Compare offline vs LLM
$ python scripts/compare_offline_llm.py \
    --offline experiments/09_ablation_study/results_post_patch_n24_offline_2026-02-09.json \
    --llm experiments/09_ablation_study/results_b0_llm_mode_n24_2026-02-11.json \
    --output docs/handoffs/20260211_offline_llm_comparison.md

# D+4: Baseline B1 implementation (single-agent + symbolic)
$ python src/baselines/b1_single_symbolic.py \
    --input data/processed/gold_standard/gs_active_cases.frozen_20260209.json \
    --output experiments/09_ablation_study/results_b1_n24_2026-02-12.json

# D+5: Baseline B2 implementation (retrieval-first)
$ python src/baselines/b2_retrieval_minimal.py \
    --input data/processed/gold_standard/gs_active_cases.frozen_20260209.json \
    --output experiments/09_ablation_study/results_b2_n24_2026-02-12.json

# D+6: Held-out sample evaluation (N=20 proxy)
$ python experiments/09_ablation_study/run_bench_heldout.py \
    --heldout data/processed/gold_standard/gs_heldout_58_cases.json \
    --sample 20 \
    --output experiments/09_ablation_study/results_b0_heldout_sample20_2026-02-13.json

# D+7: Final aggregation
$ python scripts/aggregate_round7_results.py \
    --baseline-b0 experiments/09_ablation_study/results_post_patch_n24_offline_2026-02-09.json \
    --b0-llm experiments/09_ablation_study/results_b0_llm_mode_n24_2026-02-11.json \
    --b1 experiments/09_ablation_study/results_b1_n24_2026-02-12.json \
    --b2 experiments/09_ablation_study/results_b2_n24_2026-02-12.json \
    --heldout experiments/09_ablation_study/results_b0_heldout_sample20_2026-02-13.json \
    --output docs/handoffs/20260216_round7_p3_evaluation.md
```

### Post-Execution Validation (D+7)

```bash
# Final validation checklist
$ python scripts/final_validation_check.py \
    --frozen-manifest data/benchmark_manifest.json \
    --frozen-dataset data/processed/gold_standard/gs_active_cases.frozen_20260209.json \
    --evaluation-report docs/handoffs/20260216_round7_p3_evaluation.md

# Git commit all results
$ git add experiments/09_ablation_study/results_*.json
$ git add docs/handoffs/20260216_round7_p3_evaluation.md
$ git commit -m " Round 7 P3 evaluation complete: dual-track results, held-out sample"
```

---

## Penilaian P1..P4 (Score 1-5)

### P1: Lanjut Arsitektur Sekarang (Fokus Held-out + Parity)

| Kriteria | Score | Alasan + Bukti |
|----------|-------|----------------|
| Feasibility | 3 | Mudah dieksekusi, tapi risk overfitting pada arsitektur kompleks yang belum tervalidasi secara independen |
| Validity | 2 | `paper/main.tex` line 258: "not yet ready for a strong public NLP preprint claim" — validitas rendah tanpa held-out |
| Resource | 4 | Hanya membutuhkan LLM API calls dan waktu evaluasi |
| Risk | 2 | Fatal risk #1 dan #2 aktif; klaim dini berbahaya |
| **Total** | **11/20** | **Not recommended sebagai primary path** |

### P2: Pivot ke Baseline Sederhana (B1)

| Kriteria | Score | Alasan + Bukti |
|----------|-------|----------------|
| Feasibility | 4 | B1 lebih sederhana, lebih cepat diimplementasi |
| Validity | 3 | Baseline sederhana lebih mudah divalidasi, tapi mengorbankan kontribusi arsitektur multi-agent |
| Resource | 5 | Minimal resource, bisa jalan tanpa LLM API |
| Risk | 3 | Lower risk tapi potensi paper rejection karena "too simple" |
| **Total** | **15/20** | **Viable sebagai fallback, bukan primary** |

### P3: Dual-Track 70/30 (Stabilisasi + Eksplorasi)

| Kriteria | Score | Alasan + Bukti |
|----------|-------|----------------|
| Feasibility | 4 | Memungkinkan parallel work; 70% resource ke B0, 30% ke B1/B2 |
| Validity | 4 | Memberikan bukti perbandingan arsitektur; strengthen paper |
| Resource | 4 | Butuh koordinasi tapi resource terbagi efisien |
| Risk | 4 | Mengurangi fatal risk #1 dengan tetap explore alternatif; best risk-adjusted return |
| **Total** | **16/20** | **RECOMMENDED** |

### P4: Infra-First Freeze (Stop Tuning Sampai Dependency Lengkap)

| Kriteria | Score | Alasan + Bukti |
|----------|-------|----------------|
| Feasibility | 5 | Paling aman; tidak ada eksperimen yang invalid |
| Validity | 2 | Stagnasi tidak menghasilkan data baru untuk paper |
| Resource | 2 | Waktu 7 hari terbuang tanpa progress evaluatif |
| Risk | 3 | Low execution risk tapi high project risk (deadline missed) |
| **Total** | **12/20** | **Too conservative; reject** |

---

## Keputusan Sementara

**Status:** `GO — with P3-DUAL-TRACK variant`  
**Syarat:**
1. Expert-4 coverage harus 24/24 sebelum D+2 (hard gate)
2. LLM-mode parity harus dijalankan dan dibandingkan (D+2)
3. Held-out promotion minimal 20 kasus untuk proxy evaluation (D+6)
4. Paper draft tidak boleh klaim performa final; batasi ke "pilot evidence with confidence intervals"
5. Jika LLM-mode Wilson CI tidak overlap dengan offline, escalate ke `PIVOT` decision immediately

**Trigger untuk HOLD:**
- >=2 high-cap agents (Claude/Gemini/DeepSeek) melaporkan blocker HIGH unresolved
- Expert-4 coverage tidak mencapai 24/24 sampai D+3
- LLM-mode accuracy <30% (significant degradation dari offline 41.67%)

**Trigger untuk PIVOT:**
- B0 LLM-mode tidak stabil (variance >15% antar run)
- B1 single-agent performance >= B0 dengan resource 1/10
- Held-out sample accuracy <30% (indikasi overfitting parah)

---

**Ballot JSON:** `docs/handoffs/ballots/round7/20260209_kimi_round7_ballot.json` (dibuat terpisah)

**Signature:** Kimi (Ops Reliability)  
**Timestamp:** 2026-02-09
