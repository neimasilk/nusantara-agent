# Protocol: Experiment 05 - Formal Rule Engine

**ID:** EXP-05  
**Title:** Evaluasi Formal Rule Engine vs LLM Reasoning untuk Hukum Adat Minangkabau  
**Phase:** 2 (Core Methodology Fixes)  
**Status:** COMPLETED
**Date:** 2026-02-07

## 1. Hypothesis
Formal Rule Engine berbasis Prolog akan memberikan jawaban yang lebih akurat (100% konsisten dengan norma adat) dibandingkan LLM (DeepSeek) pada kasus-kasus *boundary* atau *edge cases* hukum waris Minangkabau, terutama pada perbedaan perlakuan harta Pusako Tinggi dan Pusako Rendah.

## 2. Methodology
1. **Rule Base**: Menggunakan `src/symbolic/rules/minangkabau.pl` yang diturunkan dari `data/rules/minangkabau_rules.json`.
2. **Engine**: `src/symbolic/rule_engine.py` (Wrapper PySwip).
3. **Test Suite**: 30 skenario kasus waris (TC-05-001 s/d TC-05-030).
4. **Comparison**:
   - Jalankan skenario pada Rule Engine.
   - Jalankan skenario yang sama pada DeepSeek-chat dengan prompting standar.
5. **Metrics**: Accuracy vs Gold Standard, Consistency, Reasoning Traceability.

## 3. Acceptance Criteria
- Rule Engine menghasilkan jawaban yang berbeda dari LLM pada minimal 30% kasus sulit.
- Rule Engine mampu mendeteksi konflik formal (misal: penjualan pusako tinggi tanpa konsensus).

## 4. Procedure
1. Load Prolog rules.
2. Iterasi melalui `test_cases.json`.
3. Assert fakta skenario ke dalam Prolog environment.
4. Jalankan query `can_inherit` atau `conflict`.
5. Catat hasil dan bandingkan dengan ekspektasi.

## 5. Results

Eksperimen telah dijalankan dengan N=30 test cases. Hasil lengkap tersedia di:
- **`result.json`** — Data mentah semua 30 skenario (symbolic vs LLM output).
- **`analysis.md`** — Analisis kuantitatif dan kualitatif.

### Ringkasan Hasil
- Rule Engine Accuracy: 70.0% (21/30)
- LLM Accuracy: 83.3% (25/30)
- Divergence Rate: 33.3% (10/30 cases)
- Acceptance criteria terpenuhi: divergensi 33.3% > threshold 30%.

### Status ART
- ART-021 (DONE), ART-022 (DONE), ART-023 (DONE)
