# Accuracy Tuning Phase

Direktori ini berisi artefak operasional untuk fase **Accuracy Tuning & Recovery** (Phase 6).

---

## Dokumen Utama

| Dokumen | Deskripsi |
|---------|-----------|
| [`../SOP_ACCURACY_TUNING_PHASE.md`](../SOP_ACCURACY_TUNING_PHASE.md) | SOP lengkap fase accuracy tuning |
| [`../RENCANA_KERJA_ACCURACY_TUNING.md`](../RENCANA_KERJA_ACCURACY_TUNING.md) | Ringkasan rencana kerja |
| [`daily_log_template.md`](daily_log_template.md) | Template daily log |
| [`daily_log_2026-02-09.md`](daily_log_2026-02-09.md) | Log terbaru (stabilization + fallback hardening) |

---

## Status Sprint (Per 2026-02-09)

| Sprint | Target | Status | Tasks |
|--------|--------|--------|-------|
| Sprint 1: Quick Wins | >=65% accuracy | DONE | ART-090, ART-091 |
| Sprint 2: Structural | >=75% accuracy | IN_PROGRESS | ART-092, ART-093, ART-094 |
| Sprint 3: Optimization | >=85% accuracy | PENDING | ART-095 |

Catatan:
- ART-092 dan ART-096 telah menyentuh akurasi 72.73% pada subset 22 kasus (mode LLM).
- Run offline fallback terbaru menghasilkan 59.09% dan tidak boleh disetarakan langsung dengan run mode LLM.

---

## Link Penting

- **Task Registry:** [`../task_registry.md`](../task_registry.md)
- **Failure Registry:** [`../failure_registry.md`](../failure_registry.md)
- **Handoff ART-096:** [`../handoffs/20260209_ART096_completion.md`](../handoffs/20260209_ART096_completion.md)
- **Benchmark Script (preferred):** `../../experiments/09_ablation_study/run_bench_active.py`
- **Benchmark Script (legacy alias):** `../../experiments/09_ablation_study/run_bench_gs82.py`
- **Benchmark Manifest:** `../../data/benchmark_manifest.json`

---

## Mode Benchmark

- Mode default: warning-only jika ada mismatch count dataset vs manifest.
- Mode ketat:
  `python experiments/09_ablation_study/run_bench_active.py --strict-manifest`
- Validasi manifest:
  `python scripts/validate_benchmark_manifest.py`
- Validasi manifest + reference claim:
  `python scripts/validate_benchmark_manifest.py --require-reference-match`
- Rebuild manifest:
  `python scripts/rebuild_benchmark_manifest.py`

---

## Dependency Notes (Operational)

Agar benchmark mode LLM penuh dapat dijalankan konsisten lintas mesin, environment minimal perlu:
- `langchain_openai`
- `langgraph`
- `clingo`
- `pymupdf` (`fitz`)

Jika dependency tersebut belum ada, pipeline sekarang menyediakan fallback operasional untuk mencegah crash, tetapi metrik fallback tidak boleh dipakai sebagai klaim performa utama.

---

**Last Updated:** 2026-02-09
