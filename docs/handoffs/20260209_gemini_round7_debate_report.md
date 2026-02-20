# Round 7 Debate Report: Consistency & Statistical Audit
**Agent:** Gemini  
**Role:** Long-Context Consistency + Statistical Auditor  
**Date:** 2026-02-09  

## 1. Ringkasan Eksekutif (5 Poin)
1.  **Metric Schism:** Terdapat jurang fatal antara *Scientific Capability* (LLM Mode: ~72%) dan *Operational Snapshot* (Offline B0: 41.67%). Menggunakan B0 sebagai acuan "improvement" adalah *strawman fallacy*.
2.  **Statistical Insignificance:** Pada N=24, akurasi 41.67% memiliki 95% Confidence Interval `[22.1%, 63.4%]`. Batas bawahnya berada di zona *random guess*.
3.  **Dependency Gap:** Rendahnya B0 bukan karena arsitektur buruk, melainkan absennya `clingo` dan `fitz` di lingkungan eksekusi (F-013).
4.  **Data Mismatch:** Manifest mengklaim referensi 82 kasus, namun hanya 24 yang aktif. Validasi "generalisasi" mustahil dilakukan saat ini.
5.  **Verdict:** **REJECT P1**, **APPROVE P4** (Infra First). Jangan tuning model yang "buta" karena dependensi hilang.

## 2. Consistency Matrix

| Klaim Dokumen | Bukti Artifact | Gap / Status | Severity |
| :--- | :--- | :--- | :--- |
| **"Rule Engine Functional"** (CLAUDE.md) | B0 Score: 41.67% (10/24) | **CRITICAL**. Rule engine kemungkinan besar *fail-open* atau *error* di mode offline tanpa `clingo`, menyebabkan skor jatuh drastis dari 72%. | High |
| **"Reference: 82 Cases"** (Manifest) | `total_cases_actual: 24` | **MAJOR**. 70% data *held-out* belum diaktifkan. Klaim generalisasi tidak valid. | High |
| **"Stabilization Phase"** (Log) | Offline metric drop 59% -> 41% | **MAJOR**. Alih-alih stabil, performa fallback terdegradasi pasca-patch/strict-mode. | Medium |
| **"Gold Standard"** (Registry) | `SPLIT=0`, Mismatch=0 | **CONSISTENT**. Data cleaning berhasil, tapi volume data tidak memadai. | Low |

## 3. Statistical Risk Notes
- **Sample Size (N=24):** Sangat kecil. Satu kasus bernilai ~4.17%.
- **Confidence Interval (B0):** `[22.1%, 63.4%]`.
  - Rentang ini mencakup angka 33.3% (random guess 3 kelas).
  - Secara statistik, B0 **tidak dapat dibedakan** dari *random classifier*.
- **Overclaim Risk:** Melaporkan kenaikan dari 41% ke X% nanti, padahal 41% adalah *artificial low* akibat missing dependency, akan dianggap *cherry-picking* baseline.

## 4. Top 3 Fatal Risks
1.  **The Broken Ruler:** Mengoptimalkan P1 berdasarkan B0 (41%) sama dengan memperbaiki mobil yang mogok karena bensin habis dengan cara mengganti mesinnya. Masalahnya adalah bensin (dependency), bukan mesin (arsitektur).
2.  **Publication Suicide:** Submit paper dengan N=24 dan baseline setara random guess akan menjamin *desk rejection* di Q1.
3.  **Training on Noise:** Tanpa symbolic verification yang jalan (`clingo` absent), agent hanya berhalusinasi atau menebak label distribution.

## 5. Kill Shot + Counter-Plan
- **Kill Shot (against P1/B0):** "Baseline B0 (41.67%) secara statistik indistinguishable dari *random chance* karena ketiadaan `clingo`/`fitz`. Menjadikannya landasan eksperimen (P1) adalah cacat logika fundamental; kita mengukur *environment failure*, bukan *model performance*."
- **Counter-Plan (P4 -> P3):**
  1.  **Stop Tuning.**
  2.  **Fix Environment:** Install `clingo`, `pymupdf` (fitz) di lingkungan eksekusi.
  3.  **Re-Run Benchmark:** Dapatkan B0' (B-Zero-Prime) yang setara dengan capability asli (~70%+).
  4.  Baru putuskan strategi tuning.

## 6. Penilaian Proposal (P1..P4)

### **P1: Lanjut arsitektur sekarang (Focus Held-out)**
- **Score: 1/5 (Strong Reject)**
- **Alasan:** "Lanjut" di atas baseline rusak (41%) adalah buang waktu. Held-out test juga akan gagal/rendah jika dependensi belum diperbaiki.
- **Bukti:** `daily_log` menunjukkan gap 72% vs 41% hanya karena mode eksekusi.

### **P2: Pivot ke Baseline Sederhana**
- **Score: 3/5 (Abstain/Neutral)**
- **Alasan:** Valid secara ilmiah untuk komparasi, tapi prematur. Arsitektur kompleks (B0) terbukti bisa 72% di LLM mode. Masalahnya di infra, bukan arsitektur.

### **P3: Dual-track 70/30**
- **Score: 4/5 (Approve)**
- **Alasan:** Pragmatis, TAPI hanya jika "Stabilisasi B0" didefinisikan sebagai "Fix Dependency & Parity", bukan "Prompt Tuning".

### **P4: Infra-first Freeze**
- **Score: 5/5 (Strong Approve)**
- **Alasan:** **Syarat Mutlak.** Tidak ada eksperimen yang valid ("Scientific Metric") sampai environment mendukung reproduksi skor 72% secara offline/lokal (via container atau dependency fix).
- **Bukti:** F-013 di `failure_registry.md` secara eksplisit menyebut dependency gap ini sebagai blocker validasi.
