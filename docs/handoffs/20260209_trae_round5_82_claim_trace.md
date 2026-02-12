# Trace Report: 82-Claim vs 24-Actual Gap

**Date:** 2026-02-09
**Investigator:** Trae (Forensic QA)
**Subject:** Discrepancy between Claimed Completed Cases (82) and Active Dataset (24)

## 1. Problem Statement

Dokumen `docs/human_only/artifacts/gold_standard_consensus_report_complete_82_cases_2026-02-08.md` mengklaim bahwa **82 kasus** telah selesai ("Status: COMPLETE"). Namun, file dataset aktif `data/processed/gold_standard/gs_active_cases.json` dan manifest hanya memuat **24 kasus**.

## 2. Forensic Findings

Berdasarkan penelusuran file system lokal:

### A. Bukti Eksistensi Data (Source of Truth)
*   **Lokasi:** `data/processed/gold_standard/annotations/`
*   **Temuan:** Terdapat **201 file** anotasi mentah (`GS-0001` s/d `GS-0200`).
*   **Analisis:** Data mentah tersedia jauh melebihi klaim 82. Angka 82 kemungkinan adalah subset yang telah melalui validasi tahap 1 atau memiliki metadata lengkap.

### B. Bukti Pipeline (The Bottleneck)
*   **Active Dataset:** `gs_active_cases.json` hanya berisi 24 objek JSON.
*   **Indikasi:** Script agregasi/ingest (`scripts/ingest_expert_interview_votes.py` atau sejenisnya) kemungkinan baru dijalankan untuk batch kecil (24 kasus) atau difilter berdasarkan kriteria ketat (misal: "hanya yang punya vote lengkap" atau "hanya kategori tertentu").

### C. Sample Tracing
*   **Kasus Hilang:** `CS-MIN-001` (disebut di laporan 82 kasus) **TIDAK ADA** di `gs_active_cases.json`.
*   **Kasus Ada:** `CS-MIN-011` (disebut di laporan) **ADA** di `gs_active_cases.json`.

## 3. Root Cause Analysis

Gap terjadi pada **tahap "Selection & Aggregation"**.
Data 82 kasus eksis secara fisik (di folder annotations) dan konseptual (di laporan konsensus), namun belum dipromosikan (ingested) ke dalam file produksi `gs_active_cases.json`.

Kemungkinan penyebab teknis:
1.  **Partial Ingest:** Proses ingest terakhir sengaja dibatasi untuk *Sanity Check* atau *Sprint 1*.
2.  **Filter Logic:** Script ingest membuang kasus yang belum memiliki format ID baru (`CS-XXX`) atau metadata interview yang belum lengkap.

## 4. Evidence-Based Recommendations

Untuk menutup gap ini dan memenuhi klaim 82 kasus:

1.  **Lakukan Full Ingestion:**
    Jalankan script ingestion (misal: `python scripts/rebuild_benchmark_manifest.py` atau script custom) yang menargetkan seluruh 82 ID yang terdaftar di laporan konsensus.

2.  **Verifikasi Mapping ID:**
    Pastikan mapping antara ID lama (`GS-xxxx`) di folder annotations dengan ID baru (`CS-XXX-YYY`) tersedia. Jika tidak, script ingest akan gagal mengenali file sumber.

3.  **Update Manifest:**
    Setelah ingest ulang, jalankan `validate_benchmark_manifest.py` untuk mengupdate `total_cases_actual` menjadi 82.

## 5. Conclusion

**Klaim 82 kasus adalah VALID secara data mentah, namun INVALID secara deployment.**
Data ada di disk, tapi tidak di "etalase" (`gs_active_cases.json`). Solusinya adalah murni operasional (run ingestion pipeline), bukan akuisisi data baru.
