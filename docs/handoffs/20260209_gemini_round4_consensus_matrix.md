# Round 4 Report: Consensus Matrix Analysis (Post-Expert-4 Arbitration)
**Date:** 2026-02-09
**Status:** VALIDATION REQUIRED

## A. Ringkasan Konsensus (N=12)

Setelah integrasi Ahli-4 (Dr. Eko Susilo), distribusi kesepakatan adalah sebagai berikut:

| Status Konsensus | Jumlah Kasus | Deskripsi |
| :--- | :---: | :--- |
| **Unanimous (4-0)** | 2 | Kesepakatan mutlak lintas semua ahli. |
| **Majority (3-1)** | 4 | Terdapat satu pendapat berbeda yang bersifat minoritas. |
| **Majority (2-1-1)** | 2 | Terdapat satu label dominan dengan dua label minoritas berbeda. |
| **Split (2-2)** | 4 | Kebuntuan antara dua label (Nasional vs Sintesis atau Adat vs Sintesis). |

---

## B. Consensus Matrix & Gold Label Mismatch

| ID Kasus | A1 | A2 | A3 | A4 | Konsensus | Gold (JSON) | Mismatch? | Rekomendasi Final |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **CS-MIN-011** | B | C | A | B | **B (2:1:1)** | C | **Ya** | Label **B** (Adat) |
| **CS-MIN-004** | A | C | C | C | **C (3:1)** | B | **Ya** | Label **C** (Sintesis) |
| **CS-JAW-006** | A | A | C | A | **A (3:1)** | A | Tidak | Label **A** (Nasional) |
| **CS-LIN-052** | D | C | D | C | **Split (2:2)** | D | Tidak | Label **D** (Klarifikasi) |
| **CS-NAS-066** | A | A | C | A | **A (3:1)** | A | Tidak | Label **A** (Nasional) |
| **CS-BAL-002** | C | A | C | C | **C (3:1)** | C | Tidak | Label **C** (Sintesis) |
| **CS-NAS-010** | A | A | A | A | **A (4:0)** | A | Tidak | Label **A** (Nasional) |
| **CS-LIN-017** | A | C | C | A | **Split (2:2)** | A | Tidak | Label **C** (Sintesis)* |
| **CS-MIN-013** | B | C | B | D | **B (2:1:1)** | B | Tidak | Label **B** (Adat) |
| **CS-BAL-014** | B | C | B | C | **Split (2:2)** | B | Tidak | Label **C** (Sintesis)* |
| **CS-JAW-015** | C | C | C | C | **C (4:0)** | C | Tidak | Label **C** (Sintesis) |
| **CS-LIN-016** | C | A | C | A | **Split (2:2)** | C | Tidak | Label **A** (Nasional)* |

*\*Rekomendasi label pada kasus Split (2:2) didasarkan pada bobot rationale hukum tertulis vs praktik lapangan.*

---

## C. Analisis Kasus Kritikal

### 1. Mismatch Serius (Gold vs Consensus)
- **CS-MIN-011 (SHM vs Ulayat)**: Gold Label saat ini **C** (Sintesis), namun konsensus ahli mengarah ke **B** (Adat - 2 suara) atau tersebar (A, B, C). Ahli-1 dan Ahli-4 sepakat bahwa ini adalah murni masalah pelanggaran prosedur adat (B).
- **CS-MIN-004 (Harta Pencaharian)**: Gold Label saat ini **B** (Adat), namun konsensus ahli (A2, A3, A4) sangat kuat di **C** (Sintesis - 3 suara). Ini menunjukkan perlunya koreksi dataset secepatnya.

### 2. Kebuntuan (Split 2:2)
- **CS-LIN-052 (Kredit Adat)**: Ahli tetap terbagi antara **D** (Klarifikasi) dan **C** (Sintesis). Kasus ini sebaiknya tetap dilabeli **D** dengan catatan "Ambiguous Storyline".
- **CS-LIN-017 (Adopsi Adat)**: Terjadi pembelahan antara **A** (Nasional - A1, A4) dan **C** (Sintesis - A2, A3). Mengingat implikasi paspor adalah administratif murni, label **A** lebih pragmatis namun label **C** lebih mencerminkan pluralisme hukum.

---

## D. Rekomendasi Label Final & Confidence

| ID Kasus | Label Final | Confidence | Rationale |
| :--- | :---: | :---: | :--- |
| **CS-NAS-010** | **A** | **High** | Unanimous 4-0. |
| **CS-JAW-015** | **C** | **High** | Unanimous 4-0. |
| **CS-MIN-004** | **C** | **High** | Majority 3-1 (A2, A3, A4). |
| **CS-JAW-006** | **A** | **High** | Majority 3-1 (A1, A2, A4). |
| **CS-NAS-066** | **A** | **High** | Majority 3-1 (A1, A2, A4). |
| **CS-BAL-002** | **C** | **High** | Majority 3-1 (A1, A3, A4). |
| **CS-MIN-011** | **B** | Medium | Majority 2-1-1 (A1, A4). |
| **CS-MIN-013** | **B** | Medium | Majority 2-1-1 (A1, A3). |
| **CS-LIN-052** | **D** | Low | Split 2:2. Membutuhkan revisi narasi. |
| **CS-LIN-017** | **C** | Low | Split 2:2. C cenderung lebih komprehensif. |
| **CS-BAL-014** | **C** | Low | Split 2:2. C (A2, A4) lebih akomodatif thd modernitas. |
| **CS-LIN-016** | **A** | Low | Split 2:2. A (A2, A4) lebih sesuai prinsip domisili urban. |

---

## E. Risiko & Langkah Selanjutnya

- **Noisy Gold Data**: Jika `gs_active_cases.json` tidak segera di-patch mengikuti konsensus terbaru, akurasi benchmark AI akan terus bias terhadap label yang salah (terutama CS-MIN-004 dan CS-MIN-011).
- **Human Error**: Ditemukan ketidakkonsistenan label pada lembar jawaban Ahli-2 (rekap vs detail), disarankan verifikasi ulang untuk data input masa depan.
- **Decision Required**: Codex QA harus memutuskan apakah akan mengikuti mayoritas numerik (misal 2:1:1) atau melakukan penggabungan label (misal A+C menjadi Sintesis).
