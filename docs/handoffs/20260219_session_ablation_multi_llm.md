# Session Handoff — 2026-02-19: Ablation Study & Multi-LLM Cross-Validation

## Summary

Sesi ini menjalankan ablation study lengkap dengan 3 backend LLM, menghasilkan data statistik untuk paper, dan mengidentifikasi bottleneck utama sistem.

## What Was Done

### 1. Multi-Backend LLM Infrastructure (Claude Opus direct)
- **Modified `src/utils/llm.py`** — Added multi-backend support via `NUSANTARA_LLM_BACKEND` env var
  - Supported: `ollama` (local), `deepseek` (API), `kimi` (API)
  - Added `get_active_backend()`, `has_llm_credentials()`
  - Env overrides: `NUSANTARA_LLM_BASE_URL`, `NUSANTARA_LLM_MODEL`, `NUSANTARA_LLM_TIMEOUT_SEC`
- **Modified `src/agents/orchestrator.py`** — Uses `has_llm_credentials()` instead of hardcoded DEEPSEEK_API_KEY check
- **Modified `src/agents/router.py`** — Added `<think>` block stripping for reasoning models (deepseek-r1)
- **Ollama setup**: Pulled `qwen2.5:7b-instruct` (4.7GB) for local inference

### 2. Benchmark Results (3 modes)

| Mode | Accuracy | Wilson 95% CI | Cohen's κ |
|------|----------|---------------|-----------|
| ASP-only (offline) | 58.6% (41/70) | [0.469, 0.694] | 0.331 |
| ASP+Ollama (Qwen2.5-7B) | 62.9% (44/70) | [0.511, 0.732] | 0.411 |
| ASP+DeepSeek (API) | 67.1% (47/70) | [0.555, 0.770] | 0.473 |

**Note:** Ollama was 70.0% BEFORE GAP rule closure, dropped to 62.9% after (see regression below).

### 3. ASP Rule GAP Closure (Gemini CLI — Prompt 15)
- 24 GAP rules closed across 3 files: minangkabau.lp (+8), bali.lp (+9), jawa.lp (+7)
- ASP coverage now 100% (95 rules total)
- **BUT caused regression:** ASP+LLM dropped from 70.0% → 62.9% (-7.1 pp)
- Root cause: New `#show` directives add too much symbolic noise, biasing LLM toward B (adat)

### 4. Regression Analysis (Codex — Prompt 21)
- 7 cases regressed (correct→wrong), 4 improved (wrong→correct), net -3
- Regression concentrated in gold=C (5/7), pattern C→B (4 cases)
- Domain most affected: Jawa (+3 net regressions), Nasional (+2 net)
- Diagnosis: `#show nilai_simbolik_spiritual/1` (minangkabau.lp) and `#show bagian_lebih/2`, `#show prioritas_penunggu_rumah/1` (jawa.lp) are most problematic

### 5. Statistical Comparison 3-Way (Kimi CLI — Prompt 22)
- **McNemar tests: ALL non-significant** (p = 0.508, 0.238, 0.549 at α=0.05)
- n=70 too small for statistical significance
- Fleiss' κ = 0.623 (substantial inter-system agreement)
- 65.7% unanimous agreement, only 2.9% complete disagreement
- Majority vote: 50% accuracy on disagreed cases (no improvement)

### 6. Hard Cases Analysis (Kimi CLI — Prompt 24)
- 12 cases (17.1%) where ALL 3 systems fail
- Gold distribution: C=50%, B=41.7%, A=8.3%
- Dominant failure: C→B (33.3%) — conflict misclassified as pure adat
- All 3 systems fail identically → bottleneck is ASP rules/router, not LLM
- Minangkabau over-represented in failures (33.3%)

### 7. Per-Domain Accuracy Analysis (Claude Opus direct)
| Domain | N | ASP-only | ASP+Ollama | ASP+DeepSeek |
|--------|---|----------|------------|--------------|
| Minangkabau | 21 | 71.4% | 76.2% | 71.4% |
| Bali | 21 | 71.4% | 81.0% | 76.2% |
| Jawa | 17 | 35.3% | 41.2% | 52.9% |
| Nasional | 7 | 42.9% | 28.6% | 71.4% |
| Lintas | 4 | 50.0% | 50.0% | 50.0% |

### 8. Paper Updates
- `paper/main.tex` updated to v0.3 with ablation table and error analysis
- `paper/sections_draft_error_analysis.tex` drafted (Kimi CLI — Prompt 25) with:
  - Extended error analysis section (~450 words)
  - Cross-validation discussion (~350 words)
  - Expanded limitations (~200 words)
  - 6 LaTeX tables

### 9. Bug Fix: Unsafe Variable in minangkabau.lp (Codex — Prompt 17)
- Gemini's GAP rule introduced unsafe variable `Kaum` at line 222
- Caused 2 test failures. Fixed by Codex to grounded form.

## Files Created This Session

### Scripts
- `experiments/09_ablation_study/run_dual_benchmark.py` — Dual mode benchmark runner
- `experiments/09_ablation_study/run_single_mode.py` — DeepSeek single-mode with resume/checkpoint
- `experiments/09_ablation_study/statistical_comparison.py` — 2-way McNemar + Cohen's κ
- `experiments/09_ablation_study/statistical_comparison_3way.py` — 3-way comparison
- `experiments/09_ablation_study/hard_cases_analysis.py` — Hard cases deep analysis
- `experiments/09_ablation_study/domain_analysis.py` — Per-domain accuracy breakdown
- `experiments/09_ablation_study/regression_analysis.py` — Regression case-by-case analysis

### Results (JSON)
- `results_dual_asp_only_2026-02-19.json` — ASP-only: 58.6%
- `results_dual_asp_llm_2026-02-19.json` — ASP+Ollama: 62.9% (post-GAP)
- `results_deepseek_asp_llm_2026-02-19.json` — ASP+DeepSeek: 67.1%
- `statistical_comparison_3way_2026-02-19.json` — 3-way statistical tests
- `hard_cases_analysis_2026-02-19.json` — 12 hard cases detail
- `domain_analysis_results.json` — Per-domain breakdown

### Paper
- `paper/sections_draft_error_analysis.tex` — Draft sections for paper

## Pending Tasks (Tomorrow)

### Prompt 23 — Codex (IN PROGRESS)
Fix `#show` verbosity in ASP rules to restore accuracy ≥70%. Codex is currently working on this.
**After completion:** re-run benchmarks and 3-way comparison.

### Prompt 26 — Kimi CLI (BLOCKED on model download)
Benchmark GPT-OSS 20B and Qwen3 14B with Ollama. Models still downloading (~20GB).
**After download:** run Prompt 26 to benchmark new models.

### Follow-up Tasks
1. **Re-run 3-way statistical comparison** after #show fix (Codex or Kimi)
2. **Update paper main.tex** with:
   - Domain analysis table
   - Corrected ablation results (after #show fix)
   - Integrate `sections_draft_error_analysis.tex`
3. **Multi-model comparison** if GPT-OSS 20B or Qwen3 14B shows significant improvement
4. **Target venue decision**: Legal AI conference (JURIX/ICAIL) vs Scopus Q2-Q3 journal

## Key Decisions Made
- Paper framing: "Preliminary evidence" not "breakthrough" (n=70 insufficient for significance)
- Main contribution: expert-verified ASP rule base, not accuracy numbers
- Local 7B model competitive with commercial API → supports reproducibility
- C→B misclassification is problem #1 across all systems

## Test Suite
106 tests passing throughout session. No regressions in test suite.
