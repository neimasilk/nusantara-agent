# Round 3 Report: Split Triage (Expert Arbitration Analysis)
**Date:** 2026-02-09
**Status:** ACTION REQUIRED

## A. Ringkasan Statistik Kesepakatan (N=12)

Analisis dilakukan terhadap 12 kasus utama yang diujikan kepada Ahli-1, Ahli-2, dan Ahli-3 melalui paket interview online.

| Tingkat Kesepakatan | Jumlah Kasus | Persentase | Status |
| :--- | :---: | :---: | :--- |
| **Unanimous (3-0)** | 2 | 16.7% | Finalized |
| **Majority (2-1)** | 9 | 75.0% | Stable (needs review) |
| **Total Split (1-1-1)** | 1 | 8.3% | **CRITICAL BLOCKER** |

**Catatan Khusus:** Terdapat 1 kasus (CS-LIN-052) dengan label **D (Klarifikasi)** sebagai mayoritas, yang menandakan ambiguitas narasi kasus.

---

## B. Tabel Per Kasus (A1/A2/A3 Analysis)

| ID Kasus | A1 | A2 | A3 | Mayoritas | Status Konflik | Rekomendasi Sementara |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **CS-MIN-011** | B | C | A | **SPLIT** | **High** (Adat vs Sintesis vs Nas) | **Arbitrase Ahli-4** |
| **CS-MIN-004** | A | C | C | **C** | Medium (Nasional vs Sintesis) | Label C (Evidence: A2/A3) |
| **CS-JAW-006** | A | A | C | **A** | Medium (Nasional vs Sintesis) | Label A (Evidence: UU Perkawinan) |
| **CS-LIN-052** | D | C | D | **D** | **High** (Klarifikasi vs Sintesis) | **Arbitrase Ahli-4** (Redraft?) |
| **CS-NAS-066** | A | A | C | **A** | Medium (Nasional vs Sintesis) | Label A (Evidence: HAM/UUD) |
| **CS-BAL-002** | C | A | C | **C** | Medium (Nasional vs Sintesis) | Label C (Evidence: MDP 2010) |
| **CS-NAS-010** | A | A | A | **A** | Low (Unanimous) | Label A (Final) |
| **CS-LIN-017** | A | C | C | **C** | Medium (Nasional vs Sintesis) | Label C (Evidence: Legalitas Adopsi) |
| **CS-MIN-013** | B | C* | B | **B** | Medium (Adat vs Sintesis) | Label B (A2 Mismatch internal) |
| **CS-BAL-014** | B | C | B | **B** | Medium (Adat vs Sintesis) | Label B (Evidence: Hak Janda) |
| **CS-JAW-015** | C | C | C | **C** | Low (Unanimous) | Label C (Final) |
| **CS-LIN-016** | C | A | C | **C** | Medium (Nasional vs Sintesis) | Label C (Evidence: Urban Family) |

*\*Ahli-2 memiliki mismatch antara rekap (B) dan detail (C) pada CS-MIN-013.*

---

## C. Prioritas Ahli-4 (Top-3)

1.  **CS-MIN-011 (SHM vs Ulayat)**: Terjadi kebuntuan total. Ahli-1 fokus pada prosedur adat (B), Ahli-2 pada proses mediasi sintesis (C), dan Ahli-3 pada supremasi agraria nasional (A). Ini adalah kasus fundamental untuk neuro-symbolic reasoning.
2.  **CS-LIN-052 (Kredit Tanah Ulayat)**: Mayoritas memilih D. Jika Ahli-4 juga tidak bisa memutuskan, narasi kasus harus diperbaiki karena dianggap kekurangan fakta material (Missing Facts).
3.  **CS-MIN-004 (Harta Pencaharian)**: Meskipun mayoritas C, pergeseran dari pandangan konservatif (B) ke modern (A/C) sangat tipis. Pendapat Ahli-4 akan mengunci apakah evolusi hukum adat sudah dianggap "Final" atau masih "Sintesis".

---

## D. Risiko Jika Tidak Segera Di-Arbitrase

- **Gold Standard Poisoning**: Jika label mayoritas (2-1) dipaksakan tanpa arbitrase pada kasus "High Conflict", model AI akan belajar pola yang tidak konsisten (Noisy Labels).
- **Metric Inaccuracy**: Akurasi 72.73% yang kita klaim saat ini bergantung pada validitas label Gold Standard. Jika label berubah setelah arbitrase, akurasi bisa turun drastis (Regression).
- **Researcher Bias**: Tanpa Ahli-4, tim teknis cenderung memilih label yang paling mudah diimplementasikan secara teknis (Label A/B), bukan yang paling benar secara hukum (Label C).

## E. Tindakan Selanjutnya (Rekomendasi)
- Kirimkan **Paket Interview Ahli-4 (Split Resolution)** segera.
- Gunakan narasi dari rationale A1/A2/A3 di atas sebagai bahan pertimbangan Ahli-4.
- Tandai CS-MIN-011 dan CS-LIN-052 sebagai "STRICT_BLOCKED" di manifest sampai arbitrase selesai.
