# Rencana Kerja: Accuracy Tuning Phase
**Tanggal:** 2026-02-08  
**Milestone:** Meningkatkan akurasi dari 54.55% ke ≥75%  
**Estimasi Durasi:** 3-4 minggu

---

## 📊 Situasi Saat Ini

| Metrik | Nilai | Target |
|--------|-------|--------|
| **Akurasi Multi-Agent** | 54.55% | ≥75% |
| **Baseline Heuristic** | 68.18% | - |
| **Gold Standard Kasus** | 82 kasus (75 final, 7 split) | 200 kasus |
| **Status Registrasi** | F-011 (MAJOR) | MITIGATED |

### Masalah Utama (F-011)
1. **Hallucination of Conflict**: Agen terlalu sering memilih label C (Sintesis)
2. **Information Overload**: Agen mengabaikan fakta dari rule engine
3. **Prompt Ambiguity**: Kriteria label C tidak cukup ketat

---

## 🎯 Milestone dan Target

### Sprint 1: Quick Wins (2-3 hari)
**Target:** ≥65% akurasi

| Task | ID | Executor | Fokus |
|------|-----|----------|-------|
| Refactor Supervisor Prompt | ART-090 | AI | Kriteria label C lebih ketat |
| Sinkronisasi Fakta Simbolik | ART-091 | AI | Hilangkan Clingo warnings |

### Sprint 2: Structural Fixes (1 minggu)
**Target:** ≥75% akurasi

| Task | ID | Executor | Fokus |
|------|-----|----------|-------|
| Router-Augmented Adjudicator | ART-092 | EITHER | Integrasi hasil routing |
| KB Expansion - Nasional | ART-093 | AI | 30+ pasal KUHPerdata & KHI |
| Resolusi 7 Kasus Split | ART-094 | HUMAN | Keputusan Ahli-4 |

### Sprint 3: Optimization (2 minggu)
**Target:** ≥85% akurasi

| Task | ID | Executor | Fokus |
|------|-----|----------|-------|
| Draft 118 Kasus Baru | ART-095 | EITHER | CS-083 s.d. CS-200 |

---

## 📋 Task Dependencies

```
Sprint 1 (Paralel):
├─ ART-090 ──┐
└─ ART-091 ──┘
       ↓
Sprint 2:
├─ ART-092 (depends on ART-090)
├─ ART-093 (parallel)
└─ ART-094 (HUMAN_ONLY, parallel)
       ↓
Sprint 3:
└─ ART-095 (depends on rules finalization)
```

---

## 📁 Dokumen Terkait

### SOP Utama
- **`docs/SOP_ACCURACY_TUNING_PHASE.md`** — Dokumen SOP lengkap

### Task Registry
- **`docs/task_registry.md`** — Phase 6 (ART-090 s.d. ART-095)

### Failure Registry
- **`docs/failure_registry.md`** — F-011 (updated dengan mitigation plan)

### Logging
- **`docs/accuracy_tuning/daily_log_template.md`** — Template daily log

### Handoff Sebelumnya
- **`docs/archive/handoffs/2026-02-08_benchmarking_ready/`** — Konteks awal

---

## 🔄 Protokol Evaluasi Harian

```bash
# Command utama untuk tracking progress
python experiments/09_ablation_study/run_bench_gs82.py
```

### Metrics yang Dilacak
1. **Accuracy** — Overall correct predictions
2. **Precision/Recall (macro)** — Per-class performance
3. **False C Rate** — False positive untuk label Sintesis
4. **Confusion Matrix** — Detail per-label errors

---

## ⚠️ Risk & Mitigation

| Risk | Prob | Impact | Mitigation |
|------|------|--------|------------|
| Prompt refactoring tidak efektif | Medium | High | A/B testing 2-3 variasi |
| Clingo warnings persist | Low | Medium | Fallback rule-based |
| Ahli-4 tidak tersedia | Medium | High | Ahli cadangan/majority vote |

---

## 📝 Logging & Reporting

### Daily Log
Format: `docs/accuracy_tuning/daily_log_YYYY-MM-DD.md`
- Progress hari ini
- Metrics snapshot
- Blockers & decisions
- Next steps

### Sprint Retrospective
- Update di akhir setiap sprint
- Update `docs/failure_registry.md` jika ada kegagalan baru
- Update `docs/task_registry.md` status task

---

## 🚀 Quick Start untuk Agent Berikutnya

### 1. Baca Konteks
```bash
# Handoff sebelumnya
cat docs/archive/handoffs/2026-02-08_benchmarking_ready/handoff_gs82_and_ai_benchmark_2026-02-08.md

# Analisis baseline
cat experiments/09_ablation_study/analysis.md

# SOP ini
cat docs/SOP_ACCURACY_TUNING_PHASE.md
```

### 2. Jalankan Baseline
```bash
python experiments/09_ablation_study/run_bench_gs82.py
```

### 3. Mulai Task Pertama (ART-090)
- Edit: `src/agents/orchestrator.py`
- Fokus: Fungsi `_supervisor_agent`
- Target: Kriteria label C lebih ketat

---

## 📞 Escalation

Eskalasi ke lead researcher jika:
1. Setelah Sprint 1, akurasi tidak naik (atau turun)
2. Clingo warnings >50 setelah ART-091
3. Ahli-4 tidak bisa memberikan keputusan dalam 1 minggu

---

**Status Dokumen:** FINAL  
**Version:** 1.0  
**Last Updated:** 2026-02-08
