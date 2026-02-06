# Critique & Strategic Risk Assessment
**Tanggal:** 6 Februari 2026
**Status:** Internal Review (Pre-Execution)

## 1. Analisis Titik Kegagalan (Critical Failures)
Berdasarkan tinjauan awal, proyek Nusantara-Agent memiliki risiko tinggi pada poin-poin berikut:

*   **Semantic Loss in Triple Extraction:** Risiko hilangnya makna filosofis hukum adat (seperti pepatah-petitih) saat dipaksakan masuk ke format graf biner (S-P-O).
*   **Ambiguity of "The Right Answer":** Hukum adat seringkali berbasis negosiasi, bukan biner benar/salah. Menuntut AI memberikan resolusi mutlak bisa dianggap reduksionis oleh reviewer jurnal.
*   **Data Quality (The OCR Trap):** Teks hukum adat seringkali berada dalam dokumen tua atau scan PDF berkualitas rendah yang bisa menghasilkan "garbage in, garbage out".
*   **Agent Interaction Complexity:** Risiko loop tak berujung atau inkonsistensi antar agen dalam arsitektur multi-agen yang kompleks.

## 2. Strategi Mitigasi & Potensi Pivot
Jika dalam perjalanannya proyek ini menemui hambatan teknis, berikut adalah arah pivot yang disiapkan:

*   **Decision Support over Decision Making:** Mengubah fokus dari AI yang "memutuskan" menjadi AI yang "memetakan konflik" (Conflict Spotting).
*   **Hybrid Knowledge Engineering:** Mengurangi ketergantungan pada otomatisasi penuh (Bottom-Up) dengan memperkuat struktur ontologi manual (Top-Down).
*   **Depth over Breadth:** Jika 3 domain adat terlalu luas, fokus akan dipersempit ke satu domain (misal: Minangkabau) dengan kedalaman data yang lebih tinggi.

## 3. Komitmen Riset
Meskipun risiko teridentifikasi, proyek tetap dilanjutkan sesuai rencana awal (PRD v1.0) untuk menguji batas kemampuan teknologi (DeepSeek + GraphRAG) dalam domain hukum pluralistik. Kegagalan dalam fase eksperimen akan diperlakukan sebagai data riset yang berharga untuk dipublikasikan.
