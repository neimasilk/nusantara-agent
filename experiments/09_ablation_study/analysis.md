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

---

# Phase 4: Post-Arbiter Final Snapshot (Offline Reproducible)

Tanggal: 9 Februari 2026  
Kondisi data: Active set final N=24, `SPLIT=0`, mismatch gold-vs-majority = 0.  
Mode run: Offline forced (`NUSANTARA_FORCE_OFFLINE=1`) untuk reproducibility tanpa API berbayar.

## Hasil Benchmark (Run 4)

| Metric | Value |
|---|---|
| Total Kasus Diuji | 24 |
| Benar (Match) | 10 |
| Salah (Fail) | 14 |
| **Akurasi** | **41.67%** |
| 95% CI (Wilson) | 24.47% - 61.17% |

Artifact:
- `experiments/09_ablation_study/results_post_patch_n24_offline_2026-02-09.json`

## Observasi
1. **Regresi Offline Pasca-Patch:** Dibanding snapshot offline sebelumnya (59.09% pada N=22), performa offline final turun ke 41.67% pada N=24.
2. **Bias Prediksi ke B/C Masih Kuat:** Banyak kasus gold A diprediksi B/C (`CS-MIN-005`, `CS-MIN-015`, `CS-LIN-016`, `CS-LIN-017`, `CS-NAS-010`).
3. **Validitas Operasional vs Ilmiah:** Angka ini valid sebagai metrik operasional reproducible, tetapi bukan bukti final performa ilmiah lintas mode karena belum ada run LLM-mode post-patch pada data yang sama.

## Kesimpulan Phase 4
Setelah integritas label aktif set diperbaiki (arbiter + patch), pipeline offline menunjukkan performa konservatif 41.67%.
Prioritas berikutnya bukan over-claim angka ini, melainkan:
1. Menjalankan benchmark LLM-mode pada dataset freeze yang sama (N=24),
2. Menjaga pemisahan jelas antara metrik operasional offline dan metrik evaluasi ilmiah.

---

# Phase 5: ART-065/066 Operational Baseline Runs (Post-Mata Elang Priority Fix)

Tanggal: 11 Februari 2026  
Mode: `operational_offline` (`NUSANTARA_FORCE_OFFLINE=1`, external LLM disabled)  
Dataset: `data/processed/gold_standard/gs_active_cases.json` (evaluable 22)

## Eksekusi ART-065 (Automated Baselines)

- Runner baru: `experiments/09_ablation_study/run_all_baselines.py`
- Konfigurasi run: 7 baseline otomatis (`B1..B7`) x 3 seed (`11,22,33`) = **21 run**
- Artefak utama:
  - `experiments/09_ablation_study/results/run_all_baselines_summary.json`
  - `experiments/09_ablation_study/results/baseline_runs/B*/run_seed_*.json`

Ringkasan akurasi mean:

| Baseline | Mean Accuracy |
|---|---|
| B1 | 59.09% |
| B2 | 59.09% |
| B3 | 59.09% |
| B4 | 59.09% |
| B5 | 54.55% |
| B6 | 54.55% |
| B7 | 54.55% |

## Eksekusi ART-066 (Statistical Analysis)

- Script baru: `experiments/09_ablation_study/statistical_analysis.py`
- Reference baseline: `B5`
- Artefak statistik:
  - `experiments/09_ablation_study/results/statistical_analysis.json`
  - `experiments/09_ablation_study/results/statistical_analysis.md`

Output mencakup:
- mean, std, dan CI per baseline
- paired t-test, Wilcoxon, dan Cohen's d vs baseline acuan
- ranking baseline by mean accuracy

## Verifikasi Gate Benchmark (Mode Operational vs Scientific)

- Verifikasi operasional (offline):  
  `python experiments/09_ablation_study/run_bench_active.py --mode operational_offline`  
  menghasilkan akurasi **59.09%** pada 22 kasus evaluable  
  (artefak: `experiments/09_ablation_study/results/benchmark_operational_check_2026-02-11.json`).
- Verifikasi scientific gate: mode `scientific_claimable` kini ditolak otomatis jika `count_matches_reference_claim=false`.

## Catatan Metodologis (Wajib)

1. Run ini valid sebagai **operational progress** untuk ART-065/066, bukan penutupan klaim ilmiah final.
2. Cakupan masih active set (22 evaluable), belum target 200 kasus.
3. Snapshot ini menggunakan manifest terbaru (2026-02-11) yang mencatat `SPLIT=2`; ini berbeda dari snapshot historis sebelumnya yang sempat melaporkan `SPLIT=0`.
4. Human baseline B8 belum ikut dalam run ini.
5. Untuk mode `scientific_claimable`, runner benchmark kini fail-hard jika manifest reference mismatch (gate integrity aktif).
