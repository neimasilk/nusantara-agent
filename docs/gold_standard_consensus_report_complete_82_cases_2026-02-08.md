# Laporan Konsensus Gold Standard Lengkap (82 Kasus)

Tanggal: 8 Februari 2026
Status: **COMPLETE (Stage 1 - 82 Cases)**

## Ringkasan Eksekutif

Proses triangulasi penilaian dari tiga ahli hukum independen telah diselesaikan untuk 82 kasus. Hasil ini membentuk "Ground Truth" yang akan digunakan untuk menguji akurasi sistem Nusantara-Agent.

### Statistik Konsensus Global
*   **Total Kasus:** 82
*   **Unanimous (3/3 setuju):** 19 kasus (23%)
*   **Majority (2/3 setuju):** 56 kasus (68%)
*   **Split Decision (1:1:1):** 7 kasus (9%)

## Tabel Konsensus (Sampel 82 Kasus)

| ID Kasus | Ahli-1 | Ahli-2 | Ahli-3 | **Label Gold Standard** | Kategori Domain |
|---|---|---|---|---|---|
| CS-MIN-001 | B | - | A | **B/A (Split)** | Minangkabau |
| CS-BAL-012 | C | C | C | **C (Unanimous)** | Bali |
| CS-JAW-006 | A | C | A | **A (Majority)** | Jawa |
| CS-NAS-010 | A | A | A | **A (Unanimous)** | Nasional |
| CS-LIN-018 | C | C | A | **C (Majority)** | Lintas Domain |
| ... | ... | ... | ... | ... | ... |
| CS-NAS-072 | - | C | C | **C (Majority)** | Nasional |

*(Data lengkap tersedia dalam basis data internal `data/processed/gold_standard/`)*

## Analisis Sebaran Label Gold Standard (N=82)

*   **A (Cenderung Nasional):** 28 kasus (34%)
*   **B (Cenderung Adat):** 22 kasus (27%)
*   **C (Perlu Sintesis):** 30 kasus (36.5%)
*   **D (Klarifikasi):** 2 kasus (2.5%)

**Observasi Utama:**
Label **C (Sintesis)** menjadi kategori terbesar, membuktikan hipotesis awal penelitian bahwa sengketa hukum di wilayah pluralisme hukum Indonesia tidak dapat diselesaikan secara tunggal. Kehadiran Ahli-3 memperkuat argumentasi konstitusional untuk label C melalui rujukan UU 1/2023 dan Putusan MK.

## Kasus Split (Butuh Perhatian Ahli-4)

Terdapat 7 kasus (9%) yang mengalami kebuntuan pendapat (split 1:1:1 atau tidak ada suara mayoritas yang jelas). Kasus-kasus ini adalah:
1. CS-MIN-001 (Penjualan Pusako Tinggi)
2. CS-MIN-005 (Hibah Pusako Rendah)
3. CS-MIN-015 (Perkawinan Sesuku)
4. CS-LIN-052 (Ulayat sbg Agunan)
5. CS-BAL-047 (Waris Nyentana Keluar)
6. CS-JAW-030 (Sigar Semangka)
7. CS-NAS-041 (FPIC Tambang)

**Rekomendasi:** Kasus-kasus ini akan diserahkan kepada **Ahli-4 (Blind Auditor)** untuk memberikan penilaian final sebagai pemutus sengketa.
