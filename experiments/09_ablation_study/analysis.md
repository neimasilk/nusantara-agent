# Analysis: Experiment 09 (Ablation Study) - Phase 1

Tanggal: 8 Februari 2026
Sampel: 22 Kasus Gold Standard (Consensus by 3 Experts)
Model: DeepSeek-Chat (via NusantaraAgentPipeline)

## Hasil Utama

| Metric | Value |
|---|---|
| Total Kasus Diuji | 22 |
| Benar (Match) | 15 |
| Salah (Fail) | 7 |
| **Akurasi** | **68.18%** |

## Analisis Kegagalan (Error Analysis)

Berdasarkan `results_phase1.json`, berikut adalah pola kegagalan utama:

1.  **Over-Sensitivity to Adat (A -> B/C):** 
    *   Contoh: `CS-JAW-006` (Gono-gini poligami) dan `CS-NAS-066` (Kasepekang). 
    *   Masalah: Sistem cenderung mendeteksi konteks adat dan memberikan label B atau C, padahal ahli manusia menganggap hukum nasional sudah cukup (A) karena adanya pelanggaran HAM atau regulasi spesifik KHI.
    
2.  **Mismatched Symbolic Facts:**
    *   Banyak peringatan Clingo menunjukkan fakta yang diekstrak pipeline (misal: `female(putri)`) tidak sinkron dengan definisi rule di `.lp` (misal: `female(P)`). Ini menyebabkan *reasoning* simbolik sering kali kosong atau tidak memberikan kontribusi pada keputusan akhir.

3.  **Ambiguity in Synthesis (C vs B):**
    *   Sistem seringkali terjebak antara label B (Adat murni) dan C (Sintesis). Hal ini menunjukkan instruksi pada *Supervisor Agent* perlu dipertegas mengenai ambang batas keterlibatan hukum nasional.

## Temuan Teknis (Clingo Warnings)
Ditemukan puluhan info: `atom does not occur in any rule head`.
*   Penyebab: Pipeline mencoba menambahkan fakta seperti `consensus_reached` atau `action(A,pawn)` yang belum didefinisikan sebagai predikat valid dalam file `.lp`.
*   Dampak: Rule engine berjalan secara pasif (hanya mengembalikan fakta tanpa menjalankan inferensi logis baru).

## Rekomendasi Perbaikan

1.  **Refactor Router:** Menyeimbangkan bobot antara kata kunci nasional dan adat.
2.  **Standardisasi Predikat Simbolik:** Menyelaraskan antara `NusantaraAgentPipeline._facts_*` dengan skema yang ada di `src/symbolic/rules/*.lp`.
3.  **Prompt Engineering pada Adjudicator:** Memperkuat logika "Dualitas" (Label C) agar AI lebih selektif dalam menggabungkan dua sistem hukum.

## Kesimpulan Sementara
Akurasi 68% adalah fondasi yang baik, namun belum mencapai ambang batas produksi (target > 85%). Keunggulan sistem saat ini adalah kemampuan memberikan referensi *contextual* (retrieval) yang relevan, meskipun logika klasifikasinya masih perlu dipertajam.
