# Gold Label Policy Decision
**Agent:** Claude Sonnet 4.5 (Integrator)  
**Tanggal:** 2026-02-09  
**Mode:** Read-Only Analysis

---

## 1. Ringkasan Situasi Saat Ini

### Dataset State
| Parameter | Nilai |
|-----------|-------|
| Total Kasus dalam GS | 24 |
| Kasus dengan 4-Expert Votes | 12 |
| Kasus dengan 3-Expert Votes | 10 |
| Kasus SPLIT (belum resolved) | 2 |
| Kasus dengan Gold ≠ Derived | **6** |

### Sumber Data (Traceable)
- Dataset: `data/processed/gold_standard/gs_active_cases.json`
- Manifest: `data/benchmark_manifest.json`
- Expert-4 Source: `docs/paket_interview_online_ahli4_terisi.md`

---

## 2. Kasus Mismatch: Gold vs Derived Consensus

Dari 12 kasus dengan 4-expert votes, **6 kasus** menunjukkan potensi mismatch:

| # | ID | Gold | A1 | A2 | A3 | A4 | Derived (4-vote) | Match? |
|---|-----|------|----|----|----|----|------------------|--------|
| 1 | CS-MIN-011 | C | B | C | A | B | B (2-1-1) | ❌ |
| 2 | CS-MIN-004 | B | A | C | C | C | C (3-1) | ❌ |
| 3 | CS-LIN-052 | D | D | C | D | C | D (2-2 SPLIT) | ⚠️ |
| 4 | CS-MIN-013 | B | B | C | B | D | B (2-1-1) | ✅ |
| 5 | CS-BAL-014 | B | B | C | B | C | B (2-2 SPLIT) | ⚠️ |
| 6 | CS-LIN-016 | C | C | A | C | A | C (2-2 SPLIT) | ⚠️ |

**Kasus CLEAR MISMATCH (gold ≠ majority):** CS-MIN-011, CS-MIN-004  
**Kasus AMBIGUOUS (2-2 split, no clear majority):** CS-LIN-052, CS-BAL-014, CS-LIN-016

---

## 3. Opsi Rekonsiliasi

### Opsi A: Keep Current Gold (Status Quo)

**Deskripsi:** Pertahankan gold_label saat ini tanpa perubahan. Vote ahli4 tercatat tapi tidak mengubah label.

| Aspek | Evaluasi |
|-------|----------|
| **Pro** | Stabilitas dataset; tidak ada perubahan retroaktif; audit trail jelas |
| **Kontra** | Dataset mungkin tidak mencerminkan konsensus expert terbaru |
| **Dampak Evaluasi** | Akurasi dihitung terhadap label asli; klaim konsisten dengan sprint sebelumnya |
| **Risiko Bias** | Rendah; gold ditetapkan sebelum ahli4 |
| **Implikasi M2** | Target ≥75% diukur terhadap label original; angka tidak inflated/deflated |

### Opsi B: Update Gold to 4-Expert Derived

**Deskripsi:** Ubah gold_label menjadi majority vote dari 4 ahli.

| Aspek | Evaluasi |
|-------|----------|
| **Pro** | Mencerminkan konsensus terkuat; meningkatkan validitas ilmiah |
| **Kontra** | Breaking change pada dataset; metrik tidak comparable lintas sprint |
| **Dampak Evaluasi** | Akurasi mungkin berubah; perlu rebaseline |
| **Risiko Bias** | Sedang; jika model sudah di-tune ke label lama, maka evaluasi tidak fair |
| **Implikasi M2** | Target M2 harus dievaluasi ulang; tidak valid membandingkan pre/post |

### Opsi C: Dual-Track Sensitivity

**Deskripsi:** Pertahankan dua versi label: `gold_label_v1` (original) dan `gold_label_v2` (4-expert derived).

| Aspek | Evaluasi |
|-------|----------|
| **Pro** | Transparansi penuh; dapat run benchmark dua versi; academic rigor |
| **Kontra** | Kompleksitas operasional; perlu dua pipeline evaluasi |
| **Dampak Evaluasi** | Menyediakan sensitivity analysis; claim harus specify versi |
| **Risiko Bias** | Rendah; menghindari pilihan bias dengan menyajikan keduanya |
| **Implikasi M2** | M2 dapat diklaim pada salah satu atau kedua versi dengan qualifier jelas |

---

## 4. Tabel Keputusan per Kasus Mismatch

| ID | Votes (A1-A2-A3-A4) | Gold_v1 | Derived_v2 | Selisih | Rekomendasi | Alasan |
|----|---------------------|---------|------------|---------|-------------|--------|
| CS-MIN-011 | B-C-A-B | C | B | **MISMATCH** | **UPDATE to B** | 2 ahli pilih B (dominan adat); C hanya 1 vote |
| CS-MIN-004 | A-C-C-C | B | C | **MISMATCH** | **UPDATE to C** | 3/4 ahli pilih C; gold B tidak memiliki dukungan mayoritas |
| CS-LIN-052 | D-C-D-C | D | SPLIT(2-2) | Ambiguous | **KEEP D** | Tie; D lebih konservatif (klarifikasi) |
| CS-BAL-014 | B-C-B-C | B | SPLIT(2-2) | Ambiguous | **KEEP B** | Tie; B mendapat dukungan kuat dari ahli adat Bali |
| CS-LIN-016 | C-A-C-A | C | SPLIT(2-2) | Ambiguous | **KEEP C** | Tie; C memperhitungkan kompleksitas antar-adat |
| CS-MIN-013 | B-C-B-D | B | B (plurality) | Match | ✅ KEEP B | B dominan; D adalah klarifikasi ahli4 |

---

## 5. Rekomendasi Final

### Keputusan Terintegrasi: **Opsi C (Dual-Track) + Selective Update**

**Langkah-langkah:**

1. **Tambah field `gold_label_v2`** di setiap kasus dengan 4-expert votes, berisi derived label.
2. **Update `gold_label` (v1)** hanya untuk 2 kasus clear mismatch:
   - CS-MIN-011: C → B
   - CS-MIN-004: B → C
3. **Pertahankan gold_label** untuk 4 kasus ambiguous (2-2 split).
4. **Jalankan benchmark paralel** dengan v1 dan v2 sebagai sensitivity check.

### Alasan:
- 2 kasus clear mismatch memiliki majority 2+ yang jelas berbeda dari gold → harus diperbaiki untuk validitas.
- 4 kasus 2-2 split tidak memiliki majority → original gold adalah keputusan valid.
- Dual-track menjaga academic rigor dan auditability.

---

## 6. Rencana Eksekusi Teknis (No Execution)

### Step 1: Backup Dataset
```powershell
# Backup current state
Copy-Item -Path "data/processed/gold_standard/gs_active_cases.json" `
          -Destination "data/processed/gold_standard/gs_active_cases_backup_2026-02-09.json"
```

### Step 2: Create Mismatch Patch Script
```python
# scripts/patch_gold_labels_v2.py (pseudo-code, tidak dijalankan)
import json

updates = {
    "CS-MIN-011": {"gold_label": "B", "gold_label_v2": "B", "reconciliation_note": "4-expert majority B (2-1-1)"},
    "CS-MIN-004": {"gold_label": "C", "gold_label_v2": "C", "reconciliation_note": "4-expert majority C (3-1)"},
    "CS-LIN-052": {"gold_label_v2": "SPLIT", "reconciliation_note": "4-expert tie D-C (2-2)"},
    "CS-BAL-014": {"gold_label_v2": "SPLIT", "reconciliation_note": "4-expert tie B-C (2-2)"},
    "CS-LIN-016": {"gold_label_v2": "SPLIT", "reconciliation_note": "4-expert tie C-A (2-2)"},
    "CS-MIN-013": {"gold_label_v2": "B", "reconciliation_note": "4-expert plurality B (2-1-1)"},
}
```

### Step 3: Apply Patch (After Review)
```powershell
# Only after user approval
python scripts/patch_gold_labels_v2.py --dry-run  # Preview changes
python scripts/patch_gold_labels_v2.py --commit   # Apply changes
```

### Step 4: Rebuild Manifest
```powershell
python scripts/rebuild_benchmark_manifest.py --as-of-date 2026-02-09
python scripts/validate_benchmark_manifest.py
```

### Step 5: Run Dual Benchmark
```powershell
# Benchmark v1 (original gold)
python scripts/run_benchmark.py --gold-version v1 --output results_v1.json

# Benchmark v2 (updated gold)
python scripts/run_benchmark.py --gold-version v2 --output results_v2.json
```

---

## 7. Guardrails Klaim

### ❌ TIDAK BOLEH Diklaim
1. "Akurasi final X%" — Belum ada benchmark pasca-reconciliation.
2. "Gold Standard sudah final" — 2 kasus SPLIT belum terarbitrase.
3. "4-expert consensus untuk seluruh dataset" — Hanya 12 dari 24 kasus.

### ⚠️ PERLU QUALIFIER
1. "Akurasi X% pada gold_v1 (pre-reconciliation)" — Valid jika eksplisit.
2. "6 kasus memerlukan reconciliation" — Hanya jika decision sudah dieksekusi.

### ✅ BOLEH Diklaim
1. "Analisis gold label reconciliation telah diselesaikan."
2. "2 kasus (CS-MIN-011, CS-MIN-004) teridentifikasi sebagai clear mismatch."
3. "4 kasus memiliki 2-2 tie dan tetap menggunakan gold original."

---

## 8. Referensi Lokal

| File | Isi |
|------|-----|
| `data/processed/gold_standard/gs_active_cases.json` | Dataset utama 24 kasus |
| `data/benchmark_manifest.json` | Manifest dengan SHA256 dan distribusi label |
| `docs/paket_interview_online_ahli4_terisi.md` | Sumber vote Ahli-4 |
| `docs/handoffs/20260209_claude_sonnet45_round4_decision_gate.md` | Keputusan ingest sebelumnya |

---

**Status:** READY FOR EXECUTION (Pending User Approval)  
**Prepared by:** Claude Sonnet 4.5 (Integrator)  
**Date:** 2026-02-09
