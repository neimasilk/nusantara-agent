# Rencana Sprint 2: ART-092 Router-Augmented Adjudicator

**Tanggal:** 2026-02-09  
**Agent:** Agent #5  
**Target:** ≥75% accuracy  
**Estimasi Durasi:** 3-4 hari

---

## 🎯 Tujuan Sprint 2

### Masalah Sprint 1
- Label C detection FIXED (dari 0% ke 100% critical cases)
- Tapi: False positive tinggi - agen terlalu sering memilih C
- Perlu: Structural constraint untuk mengurangi over-detection

### Solusi: Router-Augmented Adjudicator
Gunakan hasil router sebagai **default position** untuk supervisor agent.

---

## 🏗️ Arsitektur

### Current Flow
```
Query → Router → (label: pure_national/pure_adat/conflict/consensus)
           ↓
    Rule Engine → Facts
           ↓
    Orchestrator → National Agent + Adat Agent → Supervisor Agent → Output
```

### Target Flow (ART-092)
```
Query → Router → (label: pure_national/pure_adat/conflict/consensus)
           ↓
    Rule Engine → Facts
           ↓
    Orchestrator → National Agent + Adat Agent → Supervisor Agent(route_label) → Output
           ↑
    Default Position dari Router
```

---

## 📋 Implementation Plan

### Step 1: Modify Orchestrator (2 jam)
**File:** `src/agents/orchestrator.py`

**Changes:**
1. Modify `build_parallel_orchestrator()` untuk menerima `route_label` parameter
2. Pass `route_label` ke `_supervisor_agent()`
3. Update prompt untuk menggunakan default position

### Step 2: Modify Pipeline (1 jam)
**File:** `src/pipeline/nusantara_agent.py`

**Changes:**
1. Extract router label sebelum memanggil orchestrator
2. Pass router label ke orchestrator

### Step 3: Update Supervisor Prompt (2 jam)
**File:** `src/agents/orchestrator.py`

**Changes:**
1. Add default position logic:
   - `pure_national` → Default A
   - `pure_adat` → Default B
   - `conflict` → Consider C
   - `consensus` → Analyze dominance
2. Only override default dengan evidence KUAT

### Step 4: Testing (2 jam)
1. Test 10 sample cases
2. Compare dengan baseline
3. Target: ≥75% accuracy

---

## 💻 Code Changes

### 1. Orchestrator Signature Change
```python
def build_parallel_orchestrator(graph_data_path: str = None, route_label: str = None):
    ...
    
def _supervisor_agent(llm, state, route_label: str = None):
    default_position = {
        "pure_national": "A",
        "pure_adat": "B",
        "conflict": "C",  # But need strong evidence
        "consensus": "A/B"  # Analyze
    }.get(route_label, "A/B/C")
    
    # Update prompt dengan default_position
```

### 2. Pipeline Integration
```python
def process_query(self, query: str) -> Dict:
    route = route_query(query, use_llm=False)
    route_label = route["label"]  # Extract router label
    
    # ... rule processing ...
    
    # Pass route_label ke orchestrator
    self.orchestrator = build_parallel_orchestrator(route_label=route_label)
    agent_result = self.orchestrator.invoke(inputs, route_label=route_label)
```

### 3. Prompt Template
```
Router Classification: {route_label}
Default Position: {default_position}

INSTRUCTIONS:
- Start with default position: {default_position}
- Only deviate jika ada bukti KUAT di data simbolik
- Jika ragu, stick dengan default
```

---

## ✅ Acceptance Criteria

- [ ] Router label terintegrasi ke supervisor agent
- [ ] Default position logic implemented
- [ ] 10 sample cases tested
- [ ] Accuracy ≥75%
- [ ] No regression pada critical cases (3/3 OK)

---

## 📁 Files to Modify

1. `src/agents/orchestrator.py` - Main changes
2. `src/pipeline/nusantara_agent.py` - Integration

---

## 🔗 References

- Handoff Sprint 1: `docs/archive/handoffs/2026-02-09_sprint1_evaluation/`
- SOP: `docs/SOP_ACCURACY_TUNING_PHASE.md`
- Task Registry: ART-092

---

**Status:** READY TO START  
**Blockers:** None  
**Confidence:** HIGH
