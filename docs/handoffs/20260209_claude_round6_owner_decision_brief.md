# Owner Decision Brief: Final Reconciliation Round 6
**Agent:** Claude Sonnet 4.5  
**Tanggal:** 2026-02-09  
**Status:** FINAL — Ready for Owner Decision

---

## Executive Summary

Setelah ingest vote Ahli-4 (Round 1 + Follow-up), situasi dataset:

| Metrik | Nilai |
|--------|-------|
| Total Kasus Aktif | 24 |
| Kasus dengan 4-Expert Votes | **16** (12 + 4 follow-up) |
| Kasus dengan 3-Expert Votes | 8 |
| SPLIT Formal Tersisa | **0** ✅ |
| Mismatch Gold vs Derived | **6** |

**Highlight:** CS-MIN-005 dan CS-MIN-015 yang sebelumnya SPLIT kini resolved dengan vote Ahli-4 = **A**.

---

## 1. Status SPLIT Resolution

| ID | Status Sebelum | Vote Ahli-4 | Derived Final | Status Baru |
|----|----------------|-------------|---------------|-------------|
| CS-MIN-005 | SPLIT (B-C-A) | **A** | A (2-1-1) | ✅ RESOLVED → A |
| CS-MIN-015 | SPLIT (C-B-A) | **A** | A (2-1-1) | ✅ RESOLVED → A |

**Aksi:** Update `gold_label` dari "SPLIT" menjadi **"A"** untuk kedua kasus.

---

## 2. Tabel Mismatch Final (6 Kasus)

### Kategori 1: CLEAR UPDATE (Majority ≥ 3 votes)

| ID | Gold | A1 | A2 | A3 | A4 | Derived | Aksi | Alasan |
|----|------|----|----|----|----|---------|------|--------|
| CS-MIN-004 | B | A | C | C | C | **C (3-1)** | **UPDATE → C** | Majority jelas 3/4 |

### Kategori 2: TIE-BREAKER via Plurality (2 vs 1 vs 1)

| ID | Gold | A1 | A2 | A3 | A4 | Derived | Aksi | Alasan |
|----|------|----|----|----|----|---------|------|--------|
| CS-MIN-011 | C | B | C | A | B | **B (2-1-1)** | **UPDATE → B** | Plurality B = 2, paling dominan |
| CS-LIN-017 | A | A | C | C | A | **TIE A-C (2-2)** | KEEP A | Tie; gold original dipertahankan |

### Kategori 3: TIE (2-2 Split, No Majority)

| ID | Gold | A1 | A2 | A3 | A4 | Derived | Aksi | Alasan |
|----|------|----|----|----|----|---------|------|--------|
| CS-LIN-052 | D | D | C | D | C | **TIE D-C (2-2)** | KEEP D | D lebih konservatif |
| CS-BAL-014 | B | B | C | B | C | **TIE B-C (2-2)** | KEEP B | B konsisten adat Bali |
| CS-LIN-016 | C | C | A | C | A | **TIE C-A (2-2)** | KEEP C | C merefleksikan kompleksitas |

---

## 3. Rekomendasi Patch Final

### ✅ UPDATE (4 kasus)
| ID | Old Gold | New Gold | Justifikasi |
|----|----------|----------|-------------|
| CS-MIN-005 | SPLIT | **A** | 4-expert tiebreaker; 2 votes A |
| CS-MIN-015 | SPLIT | **A** | 4-expert tiebreaker; 2 votes A |
| CS-MIN-004 | B | **C** | Clear majority 3/4 |
| CS-MIN-011 | C | **B** | Plurality 2/4 |

### ⏸️ KEEP (2 kasus)
| ID | Gold | Derived | Justifikasi |
|----|------|---------|-------------|
| CS-LIN-017 | A | TIE A-C | Gold = salah satu tie; dipertahankan |
| CS-LIN-052 | D | TIE D-C | Gold = salah satu tie; dipertahankan |
| CS-BAL-014 | B | TIE B-C | Gold = salah satu tie; dipertahankan |
| CS-LIN-016 | C | TIE C-A | Gold = salah satu tie; dipertahankan |

---

## 4. Dampak ke Comparability Metrik

### Pre-Patch State
- Evaluable cases: 22 (24 - 2 SPLIT)
- Label distribution: C=13, B=4, A=4, D=1, SPLIT=2

### Post-Patch State (Projected)
- Evaluable cases: **24** (0 SPLIT)
- Label distribution: **C=12, A=6, B=4, D=2**

### Comparability Analysis

| Aspek | Pre-Patch | Post-Patch | Impact |
|-------|-----------|------------|--------|
| N evaluable | 22 | 24 | +2 kasus (+9%) |
| Label A count | 4 | 6 | +2 (CS-MIN-005, CS-MIN-015) |
| Label C count | 13 | 12 | -1 (CS-MIN-011 pindah ke B) |
| Label B count | 4 | 4 | 0 (CS-MIN-011 masuk, CS-MIN-004 keluar) |
| SPLIT count | 2 | 0 | -2 ✅ |

**Catatan Penting:** Metrik akurasi pre/post **TIDAK COMPARABLE** karena:
1. Jumlah N berbeda (22 vs 24)
2. 4 gold labels berubah
3. Harus di-report sebagai dataset version berbeda

---

## 5. Patch Plan (Dry-Run Only)

### Step 1: Backup
```powershell
Copy-Item "data/processed/gold_standard/gs_active_cases.json" `
          "data/processed/gold_standard/gs_active_cases_pre_patch_2026-02-09.json"
```

### Step 2: Ingest Follow-up Votes to Dataset
```powershell
# Create CSV for 4 follow-up cases
# File: interview_template_ahli4_followup.csv
```

```csv
id,label_ahli4,confidence_ahli4,rationale_ahli4,reference_1,reference_2,session_date,interviewer_name,follow_up_needed,mode
CS-MIN-005,A,Tinggi,"Harta pusako rendah adalah harta hasil pencaharian pribadi yang dapat dialihkan kepada anak kandung.",KUH Perdata Pasal 1666,Doktrin adat Minangkabau tentang pusako rendah,2026-02-09,Tim Nusantara-Agent,Tidak,online_interview
CS-MIN-015,A,Tinggi,"Perkawinan yang sah menurut negara dilindungi hukum nasional dan tidak dapat dibatalkan oleh sanksi adat.",UU Perkawinan No. 1 Tahun 1974,UUD 1945 Pasal 28B,2026-02-09,Tim Nusantara-Agent,Tidak,online_interview
CS-NAS-041,C,Sedang,"Izin tambang yang sah secara administratif harus mempertimbangkan keberadaan dan hak masyarakat adat. Prinsip FPIC diperlukan.",Putusan MK No. 35/PUU-X/2012,Prinsip FPIC dalam hukum adat dan internasional,2026-02-09,Tim Nusantara-Agent,Tidak,online_interview
CS-LIN-018,C,Sedang,"Sertifikat Hak Milik merupakan bukti hak yang kuat. Pengakuan hutan adat perlu disintesiskan melalui mekanisme hukum.",UUPA 1960,Putusan MK No. 35/PUU-X/2012,2026-02-09,Tim Nusantara-Agent,Tidak,online_interview
```

### Step 3: Ingest Command
```powershell
python scripts/ingest_expert_interview_votes.py `
  --input-csv data/processed/gold_standard/interview_online/interview_template_ahli4_followup.csv `
  --expert-id ahli4 `
  --in-place
```

### Step 4: Patch Gold Labels (4 updates)
```python
# scripts/patch_gold_labels_final.py
patches = {
    "CS-MIN-005": "A",  # SPLIT → A
    "CS-MIN-015": "A",  # SPLIT → A
    "CS-MIN-004": "C",  # B → C
    "CS-MIN-011": "B",  # C → B
}
```

```powershell
python scripts/patch_gold_labels_final.py --dry-run   # Preview
python scripts/patch_gold_labels_final.py --commit    # Execute (after approval)
```

### Step 5: Rebuild Manifest
```powershell
python scripts/rebuild_benchmark_manifest.py --as-of-date 2026-02-09
python scripts/validate_benchmark_manifest.py
```

---

## 6. Guardrails

### ❌ TIDAK BOLEH Diklaim
1. "Milestone M2 (≥75%) tercapai" — Belum ada benchmark post-patch
2. "Akurasi X% final" — Dataset masih dalam flux
3. "Semua kasus memiliki 4-expert votes" — Hanya 16/24

### ✅ BOLEH Diklaim
1. "SPLIT formal sudah 0; semua kasus evaluable"
2. "4 gold labels direkonsiliasi berdasarkan 4-expert majority/plurality"
3. "Dataset v2 siap untuk benchmark formal"

---

## 7. Owner Decision Required

| Keputusan | Opsi | Default |
|-----------|------|---------|
| Approve 4 gold updates? | Yes / No | **Yes** |
| Run post-patch benchmark? | Immediate / Defer | **Immediate** |
| Version label? | v1.1 / v2.0 | **v2.0** (breaking change) |

---

**Prepared by:** Claude Sonnet 4.5  
**Status:** Pending Owner Approval  
**Next Step:** Execute patch upon approval
