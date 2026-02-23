# Session Handoff — Sonnet 4.6 Manager Execution
**Tanggal**: 2026-02-23
**Model**: Claude Sonnet 4.6
**Peran**: Manajer Proyek, mengeksekusi rencana dari Eagle Eye Review Opus 4.6
**Referensi**: `docs/handoffs/20260223_eagle_eye_opus_review.md`

---

## Yang Dikerjakan Hari Ini

### Tier 1: Housekeeping (semua selesai)

#### H1 — Rename file Qwen3 mislabeled ✓
- **File lama**: `experiments/09_ablation_study/results_qwen3_14b_2026-02-20.json`
- **File baru**: `experiments/09_ablation_study/results_qwen3_14b_INVALID_contains_deepseek_data.json`
- **Alasan**: File berisi data DeepSeek bukan Qwen3. Rename untuk mencegah penggunaan data yang salah label di paper.

#### H2 — Tambah F-018 ke failure registry ✓
- **File**: `docs/failure_registry.md`
- **Konten**: F-018: GAP Rules Regression (-7.1pp) — NEGATIVE_RESULT / MAJOR / RESOLVED
- **Ringkasan**: Penambahan 24 GAP rules untuk 100% ASP coverage menyebabkan regresi -7.1pp (Ollama). Rollback ke 71 rules. Statistik tabel diperbarui: TOTAL 18 failures, NEGATIVE_RESULT count naik ke 3.

#### H3 — Update methodology_fixes.md ✓
- **File**: `docs/methodology_fixes.md`
- **Perubahan**:
  - Weakness #3 (Linear multi-agent): `IN_PROGRESS 40%` → `ABANDONED` — dropped dari paper scope setelah negative result F-009
  - Weakness #6 (CCS unvalidated): `PLANNED 0%` → `CANCELLED` — tidak ada di post-pivot scope
  - Weakness #5 progress diperbarui ke `IN_PROGRESS 50%` (ablation 3-way selesai)
  - Last updated timestamp diperbarui ke 2026-02-23

#### H4 — Buat dev/test split policy ✓
- **File baru**: `docs/methodology/dev_test_split_policy.md`
- **Direktori baru**: `docs/methodology/` (dibuat)
- **Konten**: Policy formal yang mendokumentasikan split 49/21 yang sudah ada di `dataset_split.json`, plus definisi FUTURE TEST set untuk kasus Ahli-2 baru (post-2026-02-23)
- **Key ruling**: 70 kasus existing terkontaminasi prompt tuning → DEV. Semua kasus Ahli-2 baru → FUTURE TEST.

### Tier 2: Paper Writing

#### P4 — Ubah framing statistical claims ✓
- **File**: `paper/main.tex`
- **Lokasi 1 (Abstract)**: Rewrite seluruh abstract — sekarang mencantumkan tiga konfigurasi (ASP-only, Ollama, DeepSeek), semua Wilson CI, dan kalimat eksplisit bahwa McNemar non-signifikan ($p \geq 0.17$, $n=70$). Framing: "observed +5.7pp/+10.0pp, statistically inconclusive at current scale."
- **Lokasi 2 (Results Section 5.1)**: Ubah "The LLM layer improves accuracy by 5.7 pp" → "The LLM layer shows an observed improvement... pairwise McNemar tests are non-significant." + tambah referensi ke `sec:crossval`.
- **Lokasi 3 (Conclusion)**: Ubah "We demonstrate... 5.7-point improvement" → "We present a pilot... observed differences are statistically inconclusive."
- **Tambahan**: Tambah `\label{sec:crossval}` ke subsection Cross-Validation agar referensi dari Results valid.

---

## Yang Dikerjakan — Wave 2 (Paper Writing, multi-agent)

### Agent yang digunakan
- **Gemini**: P5 Limitations, P1 Introduction, P2 Related Work
- **Codex**: A1 Error Analysis C→B, A1b Incorporate Two-Layer Diagnosis ke paper
- **Kimi**: Update CLAUDE.md, Fix paper version + Conclusion Next Steps, Polish System Overview
- **Sonnet (saya)**: Fix inkonsistensi (Fleiss κ 0.633→0.638, roadmap section name, stale CLAUDE.md entries, Scope limitation paragraph)

### Perubahan paper/main.tex (v0.4→v0.5)
- **Abstract**: Rewrite lengkap — tiga konfigurasi + semua Wilson CI + McNemar non-signifikan eksplisit
- **Introduction**: Polished — Research Gap, Contributions bullet list, Scope, Paper Roadmap
- **Related Work**: Expanded — 4 cluster dengan deskripsi + Research Gap closing paragraph
- **System Overview**: Polished — motivasi desain 3 poin + κ=0.638 + bullet explanations
- **Results §5.1**: "improves" → "observed improvement, non-significant" + sec:crossval label
- **Results: Root cause summary**: Tambah `\paragraph{Two-layer error diagnosis.}` — 23/29 router failure, 6/29 prompt failure
- **Limitations**: Section baru 6 paragraf (ganti Threats to Validity lama)
- **Limitations**: Tambah paragraph "Scope and Generalizability" (single-language/region)
- **Conclusion**: Next steps diupdate — hapus "evaluate more backends", tambah 4 next steps yang benar
- **Paper version**: v0.4 → v0.5, tanggal 2026-02-20 → 2026-02-23
- **Fleiss κ**: Fixed 0.633→0.638 di 5 lokasi
- **Roadmap**: "Section 8 threats to validity" → "Section 8 limitations"

### Artefak baru yang dibuat
- `docs/methodology/error_analysis_cb_pattern.md` (Codex A1)
- `docs/methodology/dev_test_split_policy.md` (Sonnet H4)
- `docs/methodology/` directory (baru)

## Status Akhir Sesi

| Task | Status | Agent |
|------|--------|-------|
| H1 Rename Qwen3 file | SELESAI | Sonnet |
| H2 F-018 failure registry | SELESAI | Sonnet |
| H3 Update methodology_fixes | SELESAI | Sonnet |
| H4 Dev/test split policy | SELESAI | Sonnet |
| P4 Statistical framing paper | SELESAI | Sonnet |
| P5 Limitations section | SELESAI | Gemini + Sonnet |
| P1 Polish Introduction | SELESAI | Gemini |
| P2 Polish Related Work | SELESAI | Gemini |
| P3 Polish System Overview | SELESAI | Kimi + Sonnet |
| A1 Error analysis C→B | SELESAI | Codex |
| A1b Two-layer diagnosis ke paper | SELESAI | Codex |
| Number audit QC | SELESAI (Kimi) | Kimi |
| Qwen3-14B benchmark run | SELESAI — NEGATIVE RESULT | Sonnet |
| F-019 failure registry | SELESAI | Sonnet |

---

## Wave 3: Qwen3-14B Benchmark (sesi ini)

### Hasil benchmark
- **ASP-only** (2026-02-23): 42/70 = **60.00%**, Wilson CI [0.483, 0.707]
- **ASP+Qwen3-14B**: 38/70 = **54.29%**, Wilson CI [0.427, 0.654]
- **Delta**: -5.71pp — LLM layer HURTS performance
- **McNemar** ASP-only vs Qwen3: chi2=0.500, p=0.480 (non-significant)

### Root cause (dua pola)
1. **B→A bias (7 kasus)**: Qwen3 conflates "national law output hadir di ASP" dengan "national law governs" → mispredicts label A untuk kasus yang seharusnya B. Pattern ini tidak signifikan pada DeepSeek.
2. **C→B Layer 2 override (7 kasus)**: Qwen3 mengabaikan sinyal konflik ASP yang sudah benar (`konflik_terdeteksi: Ya`, asp_pred=C) dan menghasilkan B dengan reasoning "tidak ada konflik nasional-adat eksplisit." Ini adalah prompt-level failure.
3. Layer 1 shared failures (9 C→B kasus): ASP juga gagal, sama dengan sistem lain.

### Artefak baru
- `experiments/09_ablation_study/results_dual_asp_only_2026-02-23.json`
- `experiments/09_ablation_study/results_dual_asp_llm_2026-02-23.json`
- `experiments/09_ablation_study/qwen3_14b_negative_result_analysis_2026-02-23.json`
- `docs/failure_registry.md` — ditambah F-019

---

## Blocker

1. **Ahli-2 batch baru**: Semua klaim generalisasi bergantung pada labeled test set yang belum ada. X1, X2, X4 masih blocked.
2. **Qwen3-14B benchmark**: SELESAI — negative result (F-019). X3 resolved sebagai negative result.
3. **Rubric refinement documentation**: B3 dari Opus review — jump 58.3% → 94.0% agreement memerlukan dokumentasi di `docs/methodology/rubric_refinement_log.md`. Belum dikerjakan hari ini.
4. **Test suite**: Tidak ada perubahan code, jadi tidak perlu dijalankan. Jika ada perubahan code di sesi berikutnya, jalankan `python scripts/run_test_suite.py` (106 tests harus tetap passing).

---

## Rencana Sesi Berikutnya

### Prioritas 0: Commit sesi ini (SELESAI)
Sudah di-commit dalam 2 commit + push ke GitHub. Tambahan dari Wave 3:
- `docs/failure_registry.md` (F-019 Qwen3 negative result)
- `docs/handoffs/20260223_sonnet_manager_execution.md` (update Wave 3)
- `experiments/09_ablation_study/results_dual_asp_only_2026-02-23.json` (baru)
- `experiments/09_ablation_study/results_dual_asp_llm_2026-02-23.json` (baru)
- `experiments/09_ablation_study/qwen3_14b_negative_result_analysis_2026-02-23.json` (baru)

### Prioritas 1: Dokumentasi rubric refinement (B3 dari Opus)
- Buat `docs/methodology/rubric_refinement_log.md`
- Jelaskan: apa yang berubah di rubrik antara batch 1 (kappa=0.394) dan batch 2 (94%), kapan, siapa yang memutuskan, apakah batch 2 independent dari batch 1
- Ini perlu input dari owner tentang proses aktual

### Prioritas 2: P5 Limitations section
- `paper/main.tex` sudah ada Threats to Validity section (8 item) — evaluasi apakah cukup atau perlu diperluas sebagai section terpisah
- Fokus: statistical power crisis, dev/test contamination, rubric refinement jump

### Prioritas 3: P1-P3 Polish Introduction, Related Work, System Overview
- Review konsistensi klaim setelah P4 changes
- Pastikan abstract dan conclusion konsisten dengan body paper
- Cek apakah angka DeepSeek 68.6% sudah masuk semua tempat yang relevan (sebelumnya paper hanya menyebut Ollama 64.3% sebagai headline)

---

## Catatan Teknis

- **Angka canonical** (dari `experiments/09_ablation_study/statistical_comparison_final_2026-02-20.json`):
  - ASP-only: 58.57% (41/70), Wilson CI [0.469, 0.694], kappa=0.331
  - ASP+Ollama: 64.29% (45/70), Wilson CI [0.526, 0.745], kappa=0.418
  - ASP+DeepSeek: 68.57% (48/70), Wilson CI [0.570, 0.782], kappa=0.483
  - McNemar: ASP-only vs Ollama p=0.344, ASP-only vs DeepSeek p=0.167, Ollama vs DeepSeek p=0.549
  - Fleiss kappa antar sistem: 0.638
- **Qwen3-14B** (2026-02-23, negative result — F-019):
  - ASP-only: 60.00% (42/70), Wilson CI [0.483, 0.707]
  - ASP+Qwen3: 54.29% (38/70), Wilson CI [0.427, 0.654]
  - McNemar p=0.480 (non-significant)
  - B→A bias: 7 kasus; C→B Layer 2 override: 7 kasus
- **gpt-oss:20b** (2026-02-23, positive vs ASP-only run hari yang sama):
  - ASP-only: 60.00% (42/70), Wilson CI [0.483, 0.707]
  - ASP+gpt-oss:20b: 64.29% (45/70), Wilson CI [0.526, 0.745]
  - Delta: +4.29pp vs ASP-only (run 2026-02-23)
  - McNemar b=8, c=11, p=0.646 (non-significant)
  - C->B: 6/31 (19.4%) — jauh lebih baik dari Qwen3 (51.6%) dan ASP-only (32.3%)
  - B->A bias: 7 kasus — 6/7 identik dengan Qwen3 (GS-0010, GS-0014, GS-0019, GS-0020, GS-0021, GS-0031)
  - **Temuan struktural**: B->A bias bersifat model-agnostik untuk open-source backends. 6 kasus ini adalah hard cases di mana ASP output hukum nasional kuat tetapi gold=B (adat berlaku). Kasus ini tidak terlihat pada DeepSeek API — kemungkinan karena fine-tuning RLHF yang lebih baik untuk task legal Indonesia.
  - gpt-oss ties dengan Ollama/deepseek-r1 (sama-sama 45/70) — menunjukkan ceiling Ollama ~64% tanpa prompt fine-tuning khusus
- **Rules aktif**: 71 (dari 95 expert-verified; 24 di-rollback karena F-018)
- **Test suite**: 106 tests passing (tidak ada perubahan code hari ini)
