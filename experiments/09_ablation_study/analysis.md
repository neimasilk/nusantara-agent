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

---

# Phase 2: ART-093 Validation (National KB Expansion)

Tanggal: 9 Februari 2026
Tujuan: Mengukur dampak penambahan 20+ dokumen hukum nasional (KUHPerdata, KHI, UUPA) ke dalam `InMemoryVectorRetriever`.
Baseline (Prompt): 54.55%

## Hasil Benchmark (Run 2)

| Metric | Value |
|---|---|
| Total Kasus Diuji | 22 |
| Benar (Match) | 12 |
| Salah (Fail) | 10 |
| **Akurasi** | **54.55%** |

## Observasi
1.  **Tidak Ada Peningkatan Akurasi:** Akurasi stagnan di 54.55%. Ini menunjukkan bahwa penambahan KB saja belum cukup untuk memperbaiki penalaran, atau agen gagal memanfaatkan konteks yang ditarik secara efektif.
2.  **Retrieval Berhasil:** Log debug menunjukkan dokumen relevan berhasil ditarik (e.g., "Retrieved 3 docs").
3.  **Pergeseran Error (Pendulum Swing):**
    *   Terdapat peningkatan prediksi Label A (Nasional).
    *   Namun, ini menyebabkan **False Positives** pada kasus yang seharusnya C (Sintesis).
    *   Contoh Fail: `CS-JAW-015`, `CS-LIN-016`, `CS-BAL-020` diprediksi A, padahal Gold C.
    *   Ini menunjukkan Agen Nasional menjadi lebih dominan/agresif dengan adanya KB baru, mengalahkan argumen Adat/Sintesis pada kasus yang kompleks.

## Kesimpulan Phase 2
ART-093 berhasil diimplementasikan secara teknis (retrieval works), namun belum meningkatkan akurasi akhir. Diperlukan tuning pada **Supervisor Agent** (ART selanjutnya) untuk menyeimbangkan bobot argumen Nasional yang kini lebih kuat agar tidak "overkill" pada kasus kompromi (C).

---

# Phase 3: ART-096 Validation (Supervisor Tuning)

Tanggal: 9 Februari 2026
Tujuan: Menyeimbangkan kembali logika Adjudicator pasca ART-093. Mengoreksi dominasi Label A pada kasus konflik.
Baseline (ART-093): 54.55%

## Hasil Benchmark (Run 3)

| Metric | Value |
|---|---|
| Total Kasus Diuji | 22 |
| Benar (Match) | 16 |
| Salah (Fail) | 6 |
| **Akurasi** | **72.73%** |

## Observasi
1.  **Peningkatan Signifikan:** Akurasi naik dari 54.55% menjadi 72.73%.
2.  **Koreksi Label C:** Kasus-kasus kritis yang sebelumnya salah diprediksi A kini benar diprediksi C (Konflik/Sintesis).
    *   `CS-JAW-015` (Wekas): Correctly C.
    *   `CS-LIN-016` (Adat vs Nasional): Correctly C.
3.  **Residual Errors:**
    *   **Over-correction ke C:** Beberapa kasus B (Adat murni) atau A (Nasional murni) kini diprediksi C karena Supervisor terlalu sensitif terhadap konflik.
        *   `CS-MIN-004` (Gold B -> Pred C)
        *   `CS-BAL-009` (Gold B -> Pred C)
        *   `CS-NAS-010` (Gold A -> Pred C)
        *   `CS-LIN-017` (Gold A -> Pred C)
    *   **Missed Conflict:**
        *   `CS-BAL-020` (Gold C -> Pred A): Masih gagal mendeteksi konflik pada kasus ini.
    *   **Data Insufficiency:**
        *   `CS-LIN-052` (Gold D -> Pred C).

## Kesimpulan Phase 3
Tuning pada Supervisor Agent (ART-096) berhasil mengembalikan keseimbangan sistem (Akurasi > 70%). Meskipun muncul bias baru (over-correction ke C), ini lebih aman daripada bias sebelumnya (dominasi A) karena memaksa pengguna untuk melihat kedua sisi argumen. Akurasi 72.73% memenuhi kriteria penerimaan (>65%).

