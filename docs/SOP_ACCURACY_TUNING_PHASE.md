# SOP: Accuracy Tuning Phase (Fase Perbaikan Akurasi)

**Tanggal Efektif:** 2026-02-08  
**Versi:** 1.0  
**Milestone Target:** Meningkatkan akurasi klasifikasi dari 54.55% ke ≥75% (intermediate), menuju >85% (production)  
**Status:** IN_PROGRESS

---

## 1. RINGKASAN EKSEKUTIF

### 1.1 Kondisi Terkini
- **Gold Standard:** 82 kasus dengan konsensus 3 ahli (75 kasus final, 7 kasus split pending Ahli-4)
- **Baseline Heuristic:** 68.18% accuracy (N=22)
- **Multi-Agent Integrated:** 54.55% accuracy (N=22) — **DROP 13.6%**
- **Registrasi Kegagalan:** F-011 (Negative Gain from Basic Agent Integration)

### 1.2 Root Cause Analysis (F-011)
1. **Hallucination of Conflict:** Supervisor agent terlalu sering memaksakan label C (Sintesis) padahal seharusnya A (Nasional) atau B (Adat)
2. **Information Overload:** Agen mengabaikan fakta keras dari rule engine, lebih mengandalkan general knowledge LLM
3. **Prompt Ambiguity:** Kriteria untuk label C tidak cukup ketat

### 1.3 Target Milestone
| Milestone | Target Akurasi | Deadline Relatif | Kriteria Kelulusan |
|-----------|---------------|------------------|-------------------|
| M1-QuickWin | ≥65% | Sprint 1 (2-3 hari) | Perbaikan prompt selektif |
| M2-Structural | ≥75% | Sprint 2 (1 minggu) | Refactor adjudicator logic |
| M3-Optimization | ≥85% | Sprint 3 (2 minggu) | KB expansion + fine-tuning |

---

## 2. TIMELINE DAN DELIVERABLES

### Sprint 1: Quick Wins (Prompt Engineering)
**Durasi:** 2-3 hari  
**Focus:** Perbaikan prompt tanpa perubahan kode struktural

#### 2.1.1 Tugas: Refactor Supervisor Agent Prompt (ART-090)
**Executor:** AI_ONLY  
**Input:** `src/agents/orchestrator.py` (fungsi `_supervisor_agent`)  
**Output:** Prompt yang lebih ketat untuk label C

**SOP Detail:**
```python
# KRITERIA LABEL C (SINTESIS) - SEBELUMNYA TERLALU LONGGAR
"Pilih C (Sintesis) HANYA JIKA: (a) Ada benturan antara aturan Nasional dan Adat..."

# KRITERIA LABEL C (SINTESIS) - VERSI KETAT
"Pilih C (Sintesis) HANYA JIKA SEMUA kondisi berikut TERPENUHI:
1. Ada EXPLICIT CONTRADICTION antara output rule engine nasional dan adat
2. Konflik tersebut MATERIAL (mempengaruhi outcome hak/keputusan)
3. Tidak ada solusi tunggal yang bisa menyelesaikan kasus tanpa mengorbankan hak dari salah satu pihak

JIKA RAGU, pilih label A atau B berdasarkan dominance aturan."
```

**Acceptance Test:**
- [ ] Run `python experiments/09_ablation_study/run_bench_gs82.py`
- [ ] Accuracy meningkat minimal 5% dari 54.55%
- [ ] False Positive label C turun minimal 30%

#### 2.1.2 Tugas: Synchronize Symbolic Facts (ART-091)
**Executor:** AI_ONLY  
**Input:** `src/pipeline/nusantara_agent.py` (fungsi `_facts_*`)  
**Output:** Fakta yang sinkron dengan `src/symbolic/rules/*.lp`

**Daftar Masalah Clingo Warnings:**
| Fakta di Pipeline | Status di LP | Tindakan |
|-------------------|--------------|----------|
| `consensus_reached` | Tidak ada | Tambah ke domain rules atau hapus |
| `action(A,pawn)` | Perlu cek | Sinkronkan dengan predikat valid |
| `female(putri)` | Mungkin mismatch | Gunakan variabel, bukan atom |

**SOP Detail:**
1. Baca setiap file `.lp` di `src/symbolic/rules/`
2. Identifikasi predikat yang di-head dalam rules
3. Pastikan pipeline hanya generate fakta yang valid
4. Hapus fakta yang tidak punya efek (dead facts)

**Acceptance Test:**
- [ ] Clingo warnings = 0 saat run benchmark
- [ ] Rule engine memberikan output non-kosong pada ≥80% kasus

---

### Sprint 2: Structural Fixes (Logic Refactor)
**Durasi:** 1 minggu  
**Focus:** Perubahan arsitektur untuk meningkatkan selektivitas

#### 2.2.1 Tugas: Implementasi Router-Augmented Adjudicator (ART-092)
**Executor:** EITHER  
**Input:** `src/agents/orchestrator.py`, `src/agents/router.py`  
**Output:** Adjudicator yang mempertimbangkan hasil routing

**Konsep:** Adjudicator harus memiliki "default position" berdasarkan hasil router:
- Jika router label = `pure_national` → default A, hanya pilih C jika ada konflik jelas
- Jika router label = `pure_adat` → default B, hanya pilih C jika ada konflik jelas
- Jika router label = `conflict` → pilih C atau D
- Jika router label = `consensus` → pilih A, B, atau C tergantung dominance

**SOP Implementasi:**
```python
def _supervisor_agent_v2(llm: ChatOpenAI, state: AgentState, route_label: str):
    # Tambahkan route_label sebagai input
    default_position = {
        "pure_national": "A",
        "pure_adat": "B", 
        "conflict": "C/D",
        "consensus": "A/B/C"
    }
    
    prompt = (
        f"Default position berdasarkan routing: {default_position.get(route_label, 'A/B/C')}\n"
        "Hanya deviasi dari default jika ada bukti KUAT di data simbolik..."
    )
```

**Acceptance Test:**
- [ ] Akurasi ≥70% pada N=22 sample
- [ ] Confusion matrix menunjukkan penurunan false C

#### 2.2.2 Tugas: Knowledge Base Expansion - Nasional (ART-093)
**Executor:** AI_ONLY  
**Input:** `src/pipeline/nusantara_agent.py` (`InMemoryVectorRetriever`)  
**Output:** Dokumen nasional yang lebih komprehensif

**SOP Detail:**
1. Kumpulkan 20+ pasal kunci KUHPerdata tentang waris
2. Kumpulkan 10+ pasal KHI terkait
3. Tambahkan ke `InMemoryVectorRetriever`
4. Pastikan pasal-pasal ini memiliki keywords yang overlap dengan test cases

**Daftar Pasal Prioritas:**
- KUHPerdata: 830-870 (warisan umum)
- KHI: Pasal 171-214 (kompilasi hukum islam waris)
- UU No. 1/1974: Pasal 34-37 (harta bersama)

**Acceptance Test:**
- [ ] National agent memiliki konteks ≥30 pasal
- [ ] Retrieval precision untuk query nasional ≥0.7

---

### Sprint 3: Optimization & Scaling
**Durasi:** 2 minggu  
**Focus:** Fine-tuning dan persiapan skala 200 kasus

#### 2.3.1 Tugas: Resolusi 7 Kasus Split (ART-094)
**Executor:** HUMAN_ONLY  
**Input:** `data/processed/gold_standard/gs_82_cases.json` (7 kasus split)  
**Output:** Keputusan final dari Ahli-4

**SOP Detail:**
1. Siapkan paket kerja untuk Ahli-4 dengan:
   - Narasi kasus lengkap
   - Label dari Ahli-1, Ahli-2, Ahli-3
   - Pertimbangan dari masing-masing ahli
2. Ahli-4 memberikan keputusan final tanpa melihat label sebelumnya
3. Update Gold Standard dengan keputusan Ahli-4

#### 2.3.2 Tugas: Draft 118 Kasus Baru (ART-095)
**Executor:** EITHER  
**Input:** `data/rules/*.json` (95 aturan terverifikasi)  
**Output:** `data/test_cases/cs_083_200_draft.json`

**SOP Detail:**
1. Untuk setiap aturan, buat 1-2 skenario kasus
2. Gunakan template narasi standar
3. Tentukan expected label berdasarkan rule coverage
4. Prioritaskan edge cases dan conflict scenarios

**Komposisi Target:**
| Domain | Jumlah Kasus | Prioritas |
|--------|--------------|-----------|
| Minangkabau | 40 kasus | Pusako tinggi/rendah, hak kemenakan |
| Bali | 40 kasus | Sentana rajeg/peperasan, druwe tengah |
| Jawa | 38 kasus | Gono-gini, sigar semangka, anak ragil |

---

## 3. PROTOKOL EVALUASI

### 3.1 Benchmarking Harian
```bash
# Jalankan setiap hari untuk tracking progress
python experiments/09_ablation_study/run_bench_gs82.py
```

### 3.2 Metrics yang Dilacak
| Metric | Target M1 | Target M2 | Target M3 |
|--------|-----------|-----------|-----------|
| Accuracy | ≥65% | ≥75% | ≥85% |
| Precision (macro) | ≥60% | ≥70% | ≥80% |
| Recall (macro) | ≥60% | ≥70% | ≥80% |
| F1 (macro) | ≥60% | ≥70% | ≥80% |
| False C Rate | ≤30% | ≤20% | ≤10% |

### 3.3 Confusion Matrix Analysis
Setiap sprint wajib menghasilkan confusion matrix untuk mengidentifikasi:
- **False C (Sintesis):** Kasus yang seharusnya A/B tapi diprediksi C
- **Missed Conflict:** Kasus conflict yang tidak terdeteksi
- **Label D Error:** False positive untuk tidak dapat diputuskan

---

## 4. RISK MANAGEMENT

### 4.1 Risk Register
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Prompt refactoring tidak efektif | Medium | High | A/B testing dengan 2-3 variasi prompt |
| Clingo warnings persist | Low | Medium | Fallback ke rule-based classification |
| KB expansion tidak meningkatkan retrieval | Medium | Medium | Evaluasi retrieval precision sebelum integrasi |
| Ahli-4 tidak tersedia | Medium | High | Eksternalisasi ke ahli cadangan atau majority vote |

### 4.2 Escalation Criteria
Eskalasi ke lead researcher jika:
1. Setelah Sprint 1, akurasi tidak naik (atau turun)
2. Clingo warnings >50 setelah ART-091
3. Ahli-4 tidak bisa memberikan keputusan dalam 1 minggu

---

## 5. DOKUMENTASI DAN REPORTING

### 5.1 Daily Standup Log
Format di `docs/accuracy_tuning/daily_log_YYYY-MM-DD.md`:
```markdown
## Tanggal: YYYY-MM-DD
### Progress
- [ ] Task yang diselesaikan
### Blockers
- [ ] Hambatan yang dialami
### Next Steps
- [ ] Rencana besok
### Metrics
- Accuracy: X.XX%
- Changes: +/- X.XX%
```

### 5.2 Sprint Retrospective
Setiap akhir sprint, update:
1. `docs/accuracy_tuning/sprint_N_retrospective.md`
2. `docs/failure_registry.md` (jika ada kegagalan baru)
3. `docs/task_registry.md` (update status task)

### 5.3 Handoff Document
Jika ada perubahan agent, buat handoff di:
`docs/archive/handoffs/YYYY-MM-DD_accuracy_tuning_N/`

---

## 6. REFERENSI

### 6.1 Dokumen Terkait
- `docs/archive/handoffs/2026-02-08_benchmarking_ready/` — Handoff sebelumnya
- `docs/failure_registry.md` — F-011 dan failure lainnya
- `docs/task_registry.md` — Status semua task
- `experiments/09_ablation_study/analysis.md` — Analisis baseline

### 6.2 Kode Kritis
- `src/agents/orchestrator.py` — Multi-agent orchestration
- `src/pipeline/nusantara_agent.py` — Pipeline utama
- `experiments/09_ablation_study/run_bench_gs82.py` — Benchmark script

### 6.3 Data
- `data/processed/gold_standard/gs_82_cases.json` — Gold Standard
- `src/symbolic/rules/*.lp` — Rule files

---

## 7. APPENDIX

### 7.1 Command Cheat Sheet
```bash
# Run benchmark
python experiments/09_ablation_study/run_bench_gs82.py

# Run specific test case
python -c "from src.pipeline.nusantara_agent import run_nusantara_query; print(run_nusantara_query('QUERY'))"

# Check Clingo warnings
python -c "from src.symbolic.rule_engine import ClingoRuleEngine; ..." 2>&1 | grep "atom does not occur"

# Run unit tests
python -m pytest tests/ -v
```

### 7.2 Label Definitions (Quick Reference)
| Label | Nama | Definisi | Contoh Kasus |
|-------|------|----------|--------------|
| A | Nasional Dominan | Hukum nasional mencakup seluruh aspek kasus | Warisan dengan wasiat sah |
| B | Adat Dominan | Hukum adat mencakup seluruh aspek kasus | Pusako tinggi Minangkabau |
| C | Sintesis/Dualitas | Konflik yang memerlukan harmonisasi | Poligami dengan gono-gini |
| D | Tidak Dapat Diputuskan | Informasi tidak cukup atau di luar yurisdiksi | Kasus tanpa data spesifik |

---

**Disusun oleh:** AI Agent (Accuracy Tuning Phase)  
**Review oleh:** [Pending Human Review]  
**Approval:** [Pending Lead Researcher]
