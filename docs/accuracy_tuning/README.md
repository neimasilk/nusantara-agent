# Accuracy Tuning Phase

Direktori ini berisi semua artefak terkait fase **Accuracy Tuning & Recovery** (Phase 6).

---

## 📚 Dokumen Utama

| Dokumen | Deskripsi |
|---------|-----------|
| [`../SOP_ACCURACY_TUNING_PHASE.md`](../SOP_ACCURACY_TUNING_PHASE.md) | SOP lengkap untuk fase ini |
| [`../RENCANA_KERJA_ACCURACY_TUNING.md`](../RENCANA_KERJA_ACCURACY_TUNING.md) | Ringkasan rencana kerja |
| [`daily_log_template.md`](daily_log_template.md) | Template untuk daily logging |

---

## 📊 Status Sprint

| Sprint | Target | Status | Tasks |
|--------|--------|--------|-------|
| Sprint 1: Quick Wins | ≥65% accuracy | NOT_STARTED | ART-090, ART-091 |
| Sprint 2: Structural | ≥75% accuracy | NOT_STARTED | ART-092, ART-093, ART-094 |
| Sprint 3: Optimization | ≥85% accuracy | NOT_STARTED | ART-095 |

---

## 📝 Daily Logs

| Tanggal | Log | Metrics | Notes |
|---------|-----|---------|-------|
| - | - | - | Belum ada log |

---

## 🔗 Link Penting

- **Task Registry:** [`../task_registry.md`](../task_registry.md) (Phase 6)
- **Failure Registry:** [`../failure_registry.md`](../failure_registry.md) (F-011)
- **Handoff Sebelumnya:** [`../archive/handoffs/2026-02-08_benchmarking_ready/`](../archive/handoffs/2026-02-08_benchmarking_ready/)
- **Benchmark Script (preferred):** `../../experiments/09_ablation_study/run_bench_active.py`
- **Benchmark Script (legacy alias):** `../../experiments/09_ablation_study/run_bench_gs82.py`
- **Benchmark Manifest:** `../../data/benchmark_manifest.json`
- **Paket Print Interview (master):** `../paket_print_interview_master_2026-02-08.md`
- **Paket Print Ahli-4 (split):** `../paket_interview_online_ahli4_split_siap_print_2026-02-08.md`

### Mode Eksekusi Benchmark

- Mode default: warning-only jika ada mismatch count dataset vs manifest.
- Mode ketat (direkomendasikan untuk audit):  
  `python experiments/09_ablation_study/run_bench_active.py --strict-manifest`
- Validasi manifest saja (tanpa menjalankan benchmark):  
  `python scripts/validate_benchmark_manifest.py`
- Validasi manifest + wajib match klaim referensi:  
  `python scripts/validate_benchmark_manifest.py --require-reference-match`
- Rebuild manifest dari dataset aktif (setelah ingest interview):  
  `python scripts/rebuild_benchmark_manifest.py`

---

**Last Updated:** 2026-02-08
