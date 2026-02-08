# HANDOFF FINAL: Untuk Agent #5 (Sprint 2 - ART-092)

**Tanggal Handoff:** 2026-02-09  
**Git Commit:** `dfb6b3b` - ART-090, ART-091: Prompt v4 dengan hierarki keputusan dan symbolic facts sync  
**Agent Selanjutnya:** Agent #5  
**Tugas:** ART-092 - Router-Augmented Adjudicator

---

## 🎯 Konteks Terakhir

### Status Proyek
- **Phase 6 (Accuracy Tuning)** - Sprint 1 selesai (partial success)
- **Label C Detection:** FIXED (dari 0% ke 100% critical cases)
- **Masalah tersisa:** False positive C tinggi - perlu structural constraint
- **Target Sprint 2:** ≥75% accuracy

### Hasil Sprint 1
| Kasus | Gold | v2 | v3 | Status |
|-------|------|-----|-----|--------|
| CS-MIN-011 | C | B | ✅ C | Fixed |
| CS-NAS-066 | A | A | ✅ A | Stable |
| CS-BAL-002 | C | A | ✅ C | Fixed |
| CS-MIN-004 | B | B | ✗ C | v3 over-detects |
| CS-JAW-006 | A | A | ✗ C | v3 over-detects |

---

## 📋 Keputusan Penting

### 1. Sprint 1 → Sprint 2 Transition
- **Keputusan:** Lanjut ke ART-092 (Router-Augmented) daripada iterasi prompt lagi
- **Rationale:** Structural constraint lebih efektif untuk mengurangi false positive

### 2. Prompt v4 Design (Current)
- 5-langkah hierarki keputusan
- HAM fundamental → A (priority)
- Pure internal adat → B
- Konflik material nasional-vs-adat → C
- Default: ragu C vs B → pilih B

### 3. Code Architecture
Router label sekarang tersedia dan perlu dipass ke supervisor agent sebagai **default position**.

---

## 🏗️ Asumsi Aktif

1. **Router label akurat** - `route_query()` memberikan klasifikasi yang cukup baik
2. **Rule engine output valid** - Placeholder facts sudah sync
3. **LLM API available** - DeepSeek API key tersedia di .env
4. **Benchmark 24 kasus** - Timeout normal, perlu ~12 menit untuk lengkap

---

## 📊 Status Milestone

| Milestone | Target | Status | Notes |
|-----------|--------|--------|-------|
| M1-QuickWin | ≥65% | Partial | Label C fixed, but balance needed |
| M2-Structural | ≥75% | IN_PROGRESS | ART-092 started |
| M3-Optimization | ≥85% | Pending | Post ART-092 |

---

## ⚠️ Risiko yang Diketahui

| Risk | Severity | Mitigation |
|------|----------|------------|
| Router label tidak akurat | Medium | Test dengan sample cases |
| LLM API latency | Low | Expected, ~30-60s per case |
| Benchmark timeout | Low | Normal untuk 24 kasus |

---

## 🚀 Langkah Berikutnya (ART-092)

### Implementation Steps

#### Step 1: Modify Orchestrator (2 jam)
**File:** `src/agents/orchestrator.py`

```python
def build_parallel_orchestrator(graph_data_path: str = None, route_label: str = None):
    ...
    workflow.add_node("adjudicator", lambda state: _supervisor_agent(llm, state, route_label))
    ...

def _supervisor_agent(llm: ChatOpenAI, state: AgentState, route_label: str = None):
    default_position = {
        "pure_national": "A",
        "pure_adat": "B", 
        "conflict": "C",
        "consensus": "A/B"
    }.get(route_label, "A/B/C")
    
    # Update prompt dengan default_position
```

#### Step 2: Modify Pipeline (1 jam)
**File:** `src/pipeline/nusantara_agent.py`

```python
def process_query(self, query: str) -> Dict:
    route = route_query(query, use_llm=False)
    route_label = route["label"]
    
    # ... rule processing ...
    
    # Pass route_label ke orchestrator
    self.orchestrator = build_parallel_orchestrator(route_label=route_label)
    inputs = {...}
    agent_result = self.orchestrator.invoke(inputs)
```

#### Step 3: Update Supervisor Prompt (2 jam)
Tambahkan ke prompt:
```
Router Classification: {route_label}
Default Position: {default_position}

INSTRUCTIONS:
- Start dengan default position: {default_position}
- Hanya deviasi jika ada bukti KUAT di data simbolik
- Jika ragu, tetap dengan default
```

#### Step 4: Testing (2 jam)
```bash
# Test individual cases
python -c "from src.pipeline.nusantara_agent import run_nusantara_query; print(run_nusantara_query('QUERY'))"

# Run benchmark
python experiments/09_ablation_study/run_bench_gs82.py
```

---

## 📝 Acceptance Criteria

- [ ] Router label terintegrasi ke supervisor agent
- [ ] Default position logic implemented  
- [ ] 10 sample cases tested
- [ ] Accuracy ≥75%
- [ ] No regression pada critical cases (3/3 OK)

---

## 📚 Referensi Penting

| Dokumen | Lokasi |
|---------|--------|
| Rencana Sprint 2 | `docs/RENCANA_SPRINT2_ART092.md` |
| SOP Accuracy Tuning | `docs/SOP_ACCURACY_TUNING_PHASE.md` |
| Handoff Sprint 1 | `docs/archive/handoffs/2026-02-09_sprint1_evaluation/handoff_sprint1_evaluation_complete.md` |
| Task Registry | `docs/task_registry.md` (ART-092 IN_PROGRESS) |
| Failure Registry | `docs/failure_registry.md` (F-011) |

---

## 💻 Prompt untuk Agent #5

**Konteks:**
Kamu adalah Agent #5 yang melanjutkan Accuracy Tuning Phase. Sprint 1 telah selesai dengan partial success - Label C detection sudah FIXED (dari 0% ke 100% critical cases), tapi ada masalah false positive tinggi. 

**Tugas Kamu:**
Implementasikan ART-092: Router-Augmented Adjudicator. Gunakan hasil router (`route_label`) sebagai **default position** untuk supervisor agent.

**Langkah-langkah:**
1. Baca `docs/RENCANA_SPRINT2_ART092.md` untuk detail implementasi
2. Modifikasi `src/agents/orchestrator.py` untuk menerima dan menggunakan `route_label`
3. Modifikasi `src/pipeline/nusantara_agent.py` untuk pass `route_label` ke orchestrator
4. Test dengan 10 kasus sample
5. Target: ≥75% accuracy

**Default Position Mapping:**
- `pure_national` → Default A
- `pure_adat` → Default B  
- `conflict` → Consider C
- `consensus` → Analyze dominance

**Catatan Penting:**
- Prompt v4 sudah ada di `src/agents/orchestrator.py` - tambahkan default position logic
- Jangan hapus hierarki keputusan yang sudah ada - tambahkan sebagai layer baru
- Test critical cases: CS-MIN-011 (C), CS-NAS-066 (A), CS-BAL-002 (C)

---

**Status:** READY TO START  
**Blockers:** None  
**Git Status:** Committed and pushed (`dfb6b3b`)  
**Next Review:** Setelah 10 kasus sample tested
