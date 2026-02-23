# Eagle Eye Review — Opus 4.6 Strategic Assessment
**Tanggal**: 2026-02-23 (Minggu)
**Reviewer**: Claude Opus 4.6
**Tujuan**: Review strategis mingguan, menghasilkan action items untuk eksekusi oleh Sonnet 4.6 + sub-models

---

## A. STATE PROYEK SAAT INI

### Angka Kunci (Canonical, dari commit 09f8c26)

| Metric | Value |
|--------|-------|
| Total benchmark cases | 74 (70 evaluable, 4 disputed) |
| ASP rules encoded | 71 (dari 95 expert-verified; 24 GAP rules di-rollback) |
| ASP-only accuracy | 58.6% (41/70), Wilson CI [0.469, 0.694] |
| ASP+Ollama (Qwen2.5-7B, temp=0) | 64.3% (45/70), Wilson CI [0.526, 0.745] |
| ASP+DeepSeek (temp=0) | 68.6% (48/70), Wilson CI [0.570, 0.782] |
| McNemar p-values | 0.344, 0.167, 0.549 — semua NON-SIGNIFIKAN |
| Statistical power (n=70, delta=10pp) | ~0.3 (butuh ~344 untuk power=0.8) |
| Inter-rater Kappa (batch 1, 24 kasus) | 0.394 (fair) |
| Inter-rater agreement (batch 2, 50 kasus baru) | 94.0% (perlu penjelasan metodologis) |
| D-label recall | 0% (0/2) |
| Dominant error pattern | C→B misclassification |
| Test suite | 106 tests passing |

### Per-Domain Accuracy (DeepSeek)

| Domain | N | ASP-only | +Ollama | +DeepSeek |
|--------|---|----------|---------|-----------|
| Minangkabau | 21 | 71.4% | 76.2% | 71.4% |
| Bali | 21 | 71.4% | 81.0% | 76.2% |
| Jawa | 17 | 35.3% | 41.2% | 52.9% |
| Nasional | 7 | 42.9% | 28.6% | 71.4% |
| Lintas | 4 | 50.0% | 50.0% | 50.0% |

**Jawa adalah domain terlemah secara konsisten.**

### File/Folder Penting

```
src/symbolic/rule_engine.py      — ClingoRuleEngine (core contribution)
src/symbolic/rules/*.lp          — ASP rules (71 active, 4 domain files)
src/agents/orchestrator.py       — LangGraph orchestrator
src/agents/router.py             — Keyword router
src/pipeline/nusantara_agent.py  — Unified pipeline
src/utils/llm.py                 — get_llm() factory

experiments/09_ablation_study/   — Semua hasil ablation
paper/main.tex                   — Paper draft v0.4

docs/task_registry_simplified.md — 18-task plan
docs/failure_registry.md         — 17 failures logged
docs/methodology_fixes.md        — 6 weaknesses tracked
docs/handoffs/                   — Session handoffs
```

---

## B. 5 TEMUAN KRITIS

### B1. STATISTICAL POWER CRISIS
- n=70 → power ~0.3 → 70% chance miss real difference
- Semua McNemar non-signifikan
- **Action**: Ubah framing paper. Jangan klaim "LLM improves ASP." Klaim: "observed improvement, statistically inconclusive at current scale"
- **Lokasi edit**: `paper/main.tex` — abstract dan section Results

### B2. FILE QWEN3-14B MISLABELED
- `experiments/09_ablation_study/results_qwen3_14b_2026-02-20.json` berisi data DeepSeek, bukan Qwen3
- File ini untracked di git (lihat git status)
- **Action**: Rename ke `results_qwen3_14b_INVALID_contains_deepseek_data.json` atau hapus
- **Jangan** klaim 4 backend di paper sampai Qwen3 benar-benar dijalankan

### B3. AGREEMENT JUMP 58.3% → 94.0% PERLU PENJELASAN
- Batch 1: 24 kasus, Kappa=0.394 (58.3% agreement)
- Batch 2: 50 kasus baru, 94.0% agreement
- Jump ini akan ditanyakan reviewer: rubrik di-refine berdasarkan data yang sama? (circular?)
- **Action**: Tulis dokumentasi proses rubric refinement di `docs/methodology/rubric_refinement_log.md`
- Jelaskan: apa yang berubah di rubrik, kapan, siapa yang memutuskan, apakah batch 2 independent dari batch 1

### B4. TIDAK ADA DEV/TEST SPLIT
- 70 kasus dipakai untuk prompt tuning DAN evaluasi final = overfitting risk
- **Action**: Tetapkan 70 kasus existing = DEV set. Semua kasus baru dari Ahli-2 = TEST set
- Buat file `experiments/09_ablation_study/dataset_split.json` (atau update yang sudah ada) dengan field `"split": "dev"` atau `"split": "test"` per kasus
- Tulis policy di `docs/methodology/dev_test_split_policy.md`

### B5. FAILURE REGISTRY & METHODOLOGY FIXES OUTDATED
- GAP rules regression (-7.1pp, rollback) tidak ada di failure registry
- `methodology_fixes.md` terakhir update 2026-02-08
- Weakness #3 masih "IN_PROGRESS 40%" padahal ABANDONED
- Weakness #6 masih "PLANNED" padahal CANCELLED
- **Action**:
  - Tambah F-018 (GAP rules regression) di `docs/failure_registry.md`
  - Update status weakness #3 → "ABANDONED (F-009)" dan #6 → "CANCELLED (post-pivot)"

---

## C. ACTION ITEMS — ORDERED BY PRIORITY

### Tier 1: Housekeeping (bisa dikerjakan hari ini, tanpa dependency eksternal)

| ID | Task | File(s) | Estimasi | Model |
|----|------|---------|----------|-------|
| H1 | Rename/hapus file Qwen3 mislabeled | `experiments/09_ablation_study/results_qwen3_14b_2026-02-20.json` | 2 menit | Kimi/Codex |
| H2 | Tambah F-018 ke failure registry | `docs/failure_registry.md` | 10 menit | Kimi |
| H3 | Update methodology_fixes.md | `docs/methodology_fixes.md` | 10 menit | Kimi |
| H4 | Formalisasi dev/test split policy | Buat `docs/methodology/dev_test_split_policy.md`, update `dataset_split.json` | 15 menit | Codex |

### Tier 2: Paper Writing (sections yang tidak bergantung data final)

| ID | Task | File(s) | Estimasi | Model |
|----|------|---------|----------|-------|
| P1 | Review & polish Introduction | `paper/main.tex` | 30 menit | Gemini |
| P2 | Review & polish Related Work | `paper/main.tex` | 30 menit | Gemini |
| P3 | Review & polish System Overview | `paper/main.tex` | 30 menit | Gemini |
| P4 | Ubah framing statistical claims di abstract | `paper/main.tex` | 15 menit | Sonnet (langsung) |
| P5 | Tulis Limitations section | `paper/main.tex` | 20 menit | Gemini |

### Tier 3: Analysis (memerlukan code execution)

| ID | Task | File(s) | Estimasi | Model |
|----|------|---------|----------|-------|
| A1 | Error analysis C→B: identifikasi pattern | `experiments/09_ablation_study/` | 45 menit | Codex |
| A2 | Dokumentasi rubric refinement process | `docs/methodology/rubric_refinement_log.md` | 20 menit | Sonnet + owner input |

### Tier 4: BLOCKED (butuh human action)

| ID | Task | Blocker |
|----|------|---------|
| X1 | Expand dataset ke 100+ kasus | Ahli-2 harus melabeli batch baru |
| X2 | Resolve 4 disputed cases | Delphi Round 2 adjudication |
| X3 | Run Qwen3-14B benchmark | Model harus di-download dan diverifikasi |
| X4 | Final Results section | Butuh test set results |

---

## D. STOP / CONTINUE / START

### STOP
- Menambah backend LLM baru (3 sudah cukup, semua non-signifikan)
- Menambah ASP rules (71 stable, 24 GAP terbukti harmful)
- Optimasi prompt (tanpa test set = overfitting)

### CONTINUE
- Paper writing (Introduction, Related Work, System Overview)
- Koordinasi Ahli-2 untuk dataset expansion
- Menjaga 106 tests passing

### START
- Dev/test split formal
- F-018 documentation
- Error analysis C→B
- Limitations section di paper

---

## E. TIMELINE

| Minggu | Target | Dependency |
|--------|--------|------------|
| W3 (23-28 Feb) | Tier 1 + Tier 2 selesai. Paper sections 1-4 polished. | Claude only |
| W4 (1-7 Mar) | Ahli-2 batch 1 kembali. Error analysis done. | Ahli-2 |
| W5 (8-14 Mar) | Test set evaluation. Results section. | Ahli-2 |
| W6 (15-21 Mar) | Paper complete draft. | Claude + owner |
| W7 (22-28 Mar) | Submission prep. | Owner |

---

## F. RED FLAGS UNTUK SONNET SEBAGAI MANAJER

1. **Jangan jalankan DeepSeek API** tanpa persetujuan eksplisit owner (cost control mode)
2. **Jangan edit ASP rules** (`src/symbolic/rules/*.lp`) — ini sudah stable, jangan sentuh
3. **Jangan merge kasus dev ke test** — split harus dijaga ketat
4. **Jangan tulis angka di paper tanpa sumber** — setiap angka harus traceable ke file JSON di `experiments/`
5. **Jangan pakai bahasa self-congratulatory** — "BERHASIL", "elegan", "sangat baik" dilarang
6. **Paper dan code pakai bahasa Indonesia** — ikuti konvensi existing
7. **Cek `results_qwen3_14b_2026-02-20.json`** — ini INVALID, jangan pakai datanya
