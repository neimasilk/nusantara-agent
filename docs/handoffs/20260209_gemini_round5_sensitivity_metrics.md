# Round 5 Report: Statistical QA & Metric Sensitivity Analysis
**Date:** 2026-02-09
**Analyst:** Gemini Statistical QA

## 1. Executive Summary
Analisis statistik menunjukkan bahwa dataset aktif (N=22) saat ini berada dalam kondisi **instabilitas metrik tinggi**. Perubahan 6 label (27% dari data) akibat ingest Ahli-4 menciptakan potensi fluktuasi akurasi hingga ±27%, yang secara teknis membatalkan validitas klaim Milestone M2 (75%) sampai dilakukan audit dataset menyeluruh.

## 2. Metrik Operasional vs Ilmiah

| Metrik | Nilai Saat Ini | Status | Rekomendasi |
| :--- | :---: | :--- | :--- |
| **Operational (N=22)** | 72.73% | Volatile | Gunakan hanya untuk internal debugging. |
| **Scientific (N=82)** | N/A | **Incomplete** | Wajib untuk klaim performa di paper. |

## 3. Sensitivity Analysis (N=22)
- **Dataset Noise Level:** 27.2% (6 mismatch / 22 kasus).
- **Per Case Weight:** 4.54% per label.
- **Sensitivity Policy B:** Jika label diubah mengikuti konsensus Ahli-4, akurasi sistem kemungkinan besar akan **menurun**, karena sistem sebelumnya menunjukkan bias ke arah label C (F-011) yang justru dikoreksi oleh Ahli-4 pada beberapa kasus (misal: CS-MIN-011 kembali ke B).

## 4. Analisis Ketidakpastian (95% CI)
Berdasarkan distribusi Binomial untuk N=22 dan p=0.727:
- **Interval:** [49.8% — 89.3%]
- **Kesimpulan:** Klaim akurasi 72% pada sampel sekecil ini memiliki *margin of error* sebesar ±20%. Secara ilmiah, angka ini tidak dapat membedakan sistem "Medioker" (50%) dengan sistem "Ekselen" (90%).

## 5. Decision Gate Numerik

| Checkpoint | Status | Syarat Kelulusan (Go) |
| :--- | :---: | :--- |
| **Dataset Patch** | **FAIL** | Semua 6 mismatch harus di-resolve di JSON. |
| **Statistical Power** | **FAIL** | Minimal N=50 untuk menekan CI di bawah ±15%. |
| **Scientific Accuracy** | **PENDING** | Re-run benchmark pada dataset pasca-arbitrase. |

## 6. Rekomendasi Strategis
**STOP** iterasi arsitektur sementara. Fokus pada **DATA PATCHING** dan **EXPANSION (N=82)**. Tanpa fondasi data yang stabil, perbaikan prompt atau kode hanya akan menghasilkan *overfitting* terhadap noise label yang ada.
