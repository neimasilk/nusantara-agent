# PROTOCOL (Pre-Registration) — Experiment 07: Advanced Orchestration

**[PRE-REGISTRATION]** Dokumen ini ditulis sebelum eksekusi eksperimen.

---

## Bagian 1: Pre-Registration (SEBELUM Eksekusi)

### 1.1 Metadata

| Field | Isi |
|-------|-----|
| **ID Eksperimen** | `07_advanced_orchestration` |
| **Peneliti** | AI Agent (Codex) |
| **Tanggal Pre-registration** | 2026-02-06 |
| **Prasyarat** | ART-044, ART-045, ART-046, ART-047 (DONE) |
| **Estimasi Durasi** | 2-4 jam (eksekusi + analisis) |

### 1.2 Hipotesis

> **H0 (Null):** Advanced orchestration (parallel + debate + self-correction + routing) **TIDAK** meningkatkan kualitas jawaban dibanding baseline Exp 03.
>
> **H1 (Alternatif):** Advanced orchestration **MENINGKATKAN** kualitas jawaban (akurasi, completeness, cultural sensitivity) dan efisiensi dibanding baseline Exp 03.

### 1.3 Kriteria Penerimaan (Acceptance Criteria)

| Metrik | Threshold Minimum | Metode Pengukuran |
|--------|-------------------|-------------------|
| Accuracy | >= +10% vs baseline pada test set | Evaluasi manual + rubric | 
| Completeness | >= +10% vs baseline | Rubric completeness (0-5) | 
| Cultural Sensitivity | >= +10% vs baseline | Rubric cultural sensitivity (0-5) |
| Efficiency | Total latency <= baseline * 1.2 | Runtime log | 

**Catatan:** Minimal **2 dari 3** metrik kualitas (accuracy/completeness/cultural sensitivity) harus meningkat sesuai threshold.

### 1.4 Desain Eksperimen

- **Independent Variable(s):** Orchestration strategy (baseline sequential vs advanced orchestration)
- **Dependent Variable(s):** Accuracy, completeness, cultural sensitivity, efficiency (runtime)
- **Control/Baseline:** Exp 03 (sequential pipeline)
- **Confounding Variables:** Prompt drift, query distribution bias, evaluator bias, random variability LLM

### 1.5 Data & Resources

- **Input Data:** `experiments/07_advanced_orchestration/test_queries.json` (daftar query) dan rubric di `experiments/07_advanced_orchestration/rubric.md`
- **Expected Output:** Log per query, debate logs, final synthesis, runtime stats
- **API/Resources:** DeepSeek API, token usage dicatat

---

## Bagian 2: Execution (SAAT Eksekusi)

### 2.1 Instruksi Step-by-Step

```bash
# Step 1: Aktivasi environment
python -m venv venv && venv\Scripts\activate

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Jalankan pipeline baseline (Exp 03)
python experiments/03_multi_agent_basic/multi_agent.py

# Step 4: Jalankan advanced orchestration (Exp 07)
# (script runner akan dibuat di eksperimen ini, memanggil orchestrator + debate)
python experiments/07_advanced_orchestration/run_experiment.py --query-file experiments/07_advanced_orchestration/test_queries.json

# Step 5: Verifikasi output
# Output harus ada di: experiments/07_advanced_orchestration/results/

# Step 6: Rekap skor manual
python experiments/07_advanced_orchestration/eval_scores.py --scores experiments/07_advanced_orchestration/scoring_template.json

# (Opsional) Auto-score dengan LLM independen (bukan DeepSeek)
# export OPENAI_API_KEY=... atau ANTHROPIC_API_KEY=...
# python experiments/07_advanced_orchestration/auto_score_llm.py --provider openai --model gpt-4o-mini
# python experiments/07_advanced_orchestration/auto_score_llm.py --provider kimi --model kimi-k2-turbo-preview
```

### 2.2 Log Eksekusi

| Timestamp | Event | Catatan |
|-----------|-------|---------|
| HH:MM | Mulai eksekusi | - |
| HH:MM | Baseline selesai | - |
| HH:MM | Advanced selesai | - |
| HH:MM | Selesai | Total waktu: X menit |

### 2.3 Deviasi dari Rencana

| Perubahan | Alasan | Dampak pada Validitas |
|-----------|--------|----------------------|
| - | - | - |

---

## Bagian 3: Post-Analysis (SETELAH Eksekusi)

### 3.1 Hasil Kuantitatif

| Metrik | Threshold | Hasil Aktual | PASS/FAIL |
|--------|-----------|--------------|-----------|
| Accuracy | >= +10% | -0.25 (vs baseline) | FAIL |
| Completeness | >= +10% | -0.33 (vs baseline) | FAIL |
| Cultural Sensitivity | >= +10% | -0.17 (vs baseline) | FAIL |
| Efficiency | <= 1.2x baseline | Belum diukur | TBD |

### 3.2 Analisis Kegagalan (WAJIB)

- **Apa yang hampir gagal?** TBD
- **Dalam kondisi apa ini bisa gagal?** TBD
- **Apa yang akan dikatakan reviewer skeptis?** TBD
- **Bagaimana kegagalan ini mempengaruhi klaim paper?** TBD

### 3.3 Hostile Reviewer Simulation

1. **[Validitas internal]:** TBD
2. **[Generalisasi]:** TBD
3. **[Novelty/kontribusi]:** TBD

Jawaban: TBD

### 3.4 Implikasi

- **Untuk paper:** TBD
- **Untuk eksperimen selanjutnya:** TBD
- **Untuk failure_registry:** TBD

---

## Bagian 4: Review Gate (SEBELUM Lanjut)

### 4.1 Checklist Mandatori

- [ ] Pre-registration diisi SEBELUM eksekusi (timestamp membuktikan)
- [ ] Acceptance criteria tidak diubah setelah melihat hasil
- [ ] Analisis kegagalan terisi lengkap
- [ ] Hostile reviewer simulation dijawab substantif
- [ ] Hasil dicatat di `docs/failure_registry.md`
- [ ] 10 pertanyaan review protocol dijawab (lihat `docs/review_protocol.md`)
- [ ] Kode bisa direproduksi dari instruksi step-by-step
- [ ] Data output disimpan dan di-commit
- [ ] Skoring manual menggunakan rubric (`experiments/07_advanced_orchestration/rubric.md`)

### 4.2 Keputusan Gate

| Keputusan | Kriteria |
|----------|----------|
| **PASS** | Semua acceptance criteria terpenuhi dan checklist lengkap |
| **CONDITIONAL PASS** | Sebagian terpenuhi, perlu eksperimen tambahan |
| **FAIL** | Criteria tidak terpenuhi |

**Keputusan:** FAIL

**Alasan:** Tidak ada peningkatan kualitas vs baseline pada evaluasi auto-score Kimi; semua metrik turun.

**Reviewer:** AI Agent (Codex)  **Tanggal:** 2026-02-07
Catatan hasil: perbandingan skor menggunakan auto-score Kimi (`kimi-k2-turbo-preview`) terhadap 12 query.
Baseline (Exp 03 re-run) memiliki skor lebih tinggi pada semua metrik.
