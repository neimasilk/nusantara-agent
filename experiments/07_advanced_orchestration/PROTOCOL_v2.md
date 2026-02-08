# PROTOCOL (Pre-Registration) — Experiment 07 Iteration (Debate with Retrieval)

**[PRE-REGISTRATION]** Dokumen ini ditulis sebelum eksekusi iterasi kedua Experiment 07.

---

## Bagian 1: Pre-Registration (SEBELUM Eksekusi)

### 1.1 Metadata

| Field | Isi |
|-------|-----|
| **ID Eksperimen** | `07_advanced_orchestration_v2` |
| **Peneliti** | AI Agent (Gemini) |
| **Tanggal Pre-registration** | 2026-02-07 |
| **Prasyarat** | Exp 07 (Negative Result), ART-025 (DONE) |
| **Estimasi Durasi** | 1-2 jam |

### 1.2 Hipotesis

> **H0 (Null):** Penambahan mekanisme **Evidence Retrieval** selama debat **TIDAK** meningkatkan kualitas jawaban dibanding Exp 07 original.
>
> **H1 (Alternatif):** Penambahan mekanisme **Evidence Retrieval** selama debat akan **MENINGKATKAN** kualitas jawaban (terutama metrik Completeness) karena agen dapat mencari informasi tambahan yang terlewat pada retrieval awal.

### 1.3 Kriteria Penerimaan (Acceptance Criteria)

| Metrik | Threshold Minimum | Metode Pengukuran |
|--------|-------------------|-------------------|
| Accuracy | >= Exp 07 | Auto-score Kimi | 
| Completeness | >= +15% vs Exp 07 | Auto-score Kimi | 
| Cultural Sensitivity | >= Exp 07 | Auto-score Kimi |

**Catatan:** Fokus utama adalah memperbaiki penurunan *Completeness* yang terjadi di Exp 07.

### 1.4 Desain Eksperimen

- **Independent Variable(s):** Debate protocol with dynamic evidence retrieval.
- **Dependent Variable(s):** Accuracy, completeness, cultural sensitivity.
- **Control:** Exp 07 (Advanced Orchestration tanpa retrieval dinamis).
- **Tooling:** `src/kg_engine/search.py` (SimpleKGSearch) terintegrasi ke `run_debate`.

### 1.5 Data & Resources

- **Input Data:** `experiments/07_advanced_orchestration/test_queries.json`
- **Retrieval Data:** `experiments/01_triple_extraction/result.json`
- **API:** DeepSeek API

---

## Bagian 2: Execution (SAAT Eksekusi)

### 2.1 Instruksi Step-by-Step

```bash
# Step 1: Jalankan eksperimen v2 (subset N=3 untuk penghematan token/biaya awal)
python experiments/07_advanced_orchestration/run_experiment_v2.py --count 3 --output-dir experiments/07_advanced_orchestration/results_v2

# Step 2: Verifikasi log pencarian
# Cek apakah file debate_summary.json mengandung entry "type": "search"
```

### 2.2 Log Eksekusi

| Timestamp | Event | Catatan |
|-----------|-------|---------|
| HH:MM | Mulai eksekusi | - |

---

## Bagian 3: Post-Analysis (SETELAH Eksekusi)

*(Diisi setelah eksekusi)*

---

## Bagian 4: Review Gate

*(Diisi setelah eksekusi)*
