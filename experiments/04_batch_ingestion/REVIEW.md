# REVIEW: Eksperimen 04 — Scalable Batch Ingestion

**Reviewer:** Framework SOP (retrospektif)
**Tanggal:** 2026-02-06
**Status:** CONDITIONAL PASS — modular code validated, scalability not yet proven

---

## Jawaban 10 Pertanyaan Devil's Advocate

### Q1: Apakah hasilnya circular?

**Jawaban:** Sama dengan Exp 01 — DeepSeek mengekstrak, dan keberhasilan dinilai tanpa ground truth. Tambahan: karena input identik dengan Exp 01, ini tidak memberikan informasi baru tentang kualitas ekstraksi.

**Severity jika tidak ditangani:** CRITICAL (inherited dari Exp 01)

**Rencana mitigasi:** Exp 06 — independent evaluation pipeline

**Status mitigasi:** BELUM

### Q2: Apakah baseline-nya fair?

**Jawaban:** Baseline implisit adalah Exp 01 (inline extraction). Tapi perbandingan tidak dilakukan secara formal — tidak ada metrik yang membandingkan output Exp 04 vs Exp 01. Kita tidak tahu apakah output identik, lebih baik, atau lebih buruk.

**Severity jika tidak ditangani:** MINOR (Exp 04 tentang engineering, bukan output quality)

**Rencana mitigasi:** Diff analysis antara result.json dan extracted_triples.jsonl bisa dilakukan.

**Status mitigasi:** BELUM

### Q3: Apakah skala datanya cukup?

**Jawaban:** Tidak. 1 file, ~118 kata. Klaim "Scalable Batch Ingestion" di judul eksperimen misleading — yang diuji adalah "Modular Code Execution on Single Small Input." Batch memerlukan multiple files. Scalable memerlukan load testing.

**Severity jika tidak ditangani:** MAJOR (misleading framing)

**Rencana mitigasi:** Rename eksperimen secara internal menjadi "Modular Pipeline Validation" dan uji skalabilitas sesungguhnya saat data tersedia (ART-035).

**Status mitigasi:** BELUM

### Q4: Apakah klaim "neuro-symbolic" genuinely earned?

**Jawaban:** Exp 04 tidak mengklaim neuro-symbolic. Ini adalah infrastructure experiment. Tidak relevan untuk pertanyaan ini secara langsung.

**Severity jika tidak ditangani:** N/A untuk Exp 04

**Rencana mitigasi:** N/A

**Status mitigasi:** N/A

### Q5: Apakah novelty-nya real?

**Jawaban:** Tidak ada novelty. Menulis script Python yang mengimpor module lain dan menulis JSONL bukan kontribusi teknis. Ini adalah standard software engineering practice.

**Severity jika tidak ditangani:** MINOR (ini infrastructure, bukan kontribusi utama)

**Rencana mitigasi:** Tidak perlu — Exp 04 tidak akan diklaim sebagai kontribusi di paper.

**Status mitigasi:** N/A

### Q6: Apa yang bisa dilakukan sistem ini yang TIDAK bisa dilakukan oleh GPT-4 + simple prompt?

**Jawaban:** Pertanyaan ini kurang relevan untuk Exp 04 karena ini tentang engineering pipeline, bukan reasoning capability. Yang Exp 04 tunjukkan: modular code structure memungkinkan reuse TripleExtractor di berbagai konteks. Ini standard engineering, bukan AI capability.

**Severity jika tidak ditangani:** N/A untuk Exp 04

**Rencana mitigasi:** N/A

**Status mitigasi:** N/A

### Q7: Apakah metrik evaluasi valid?

**Jawaban:** Tidak ada metrik evaluasi kuantitatif. "Pipeline works" dan "JSONL valid" bukan metrik ilmiah — ini adalah pass/fail tests untuk code correctness. Tidak ada pengukuran: extraction rate, precision, recall, throughput, latency.

**Severity jika tidak ditangani:** MAJOR (jika klaim scalability dibuat)

**Rencana mitigasi:** Tambahkan throughput metrics (triples/minute, errors/chunk) saat scaling (ART-035).

**Status mitigasi:** BELUM

### Q8: Bisakah hasilnya direproduksi?

**Jawaban:** Partially. Kode deterministic dalam hal control flow, tapi DeepSeek API responses non-deterministic. Menjalankan ulang bisa menghasilkan tripel berbeda. `extracted_triples.jsonl` yang ter-commit adalah snapshot satu run.

**Severity jika tidak ditangani:** MINOR

**Rencana mitigasi:** Set temperature=0, log model version, commit output snapshot.

**Status mitigasi:** SEBAGIAN — output di-commit

### Q9: Apakah ada selection bias?

**Jawaban:** Input identik dengan Exp 01. Jika teks tersebut sudah di-select untuk Exp 01 (yang memang bias — lihat Review Exp 01), bias ini diwarisi.

**Severity jika tidak ditangani:** MINOR (inherited)

**Rencana mitigasi:** Systematic sampling di scaling phase.

**Status mitigasi:** BELUM

### Q10: Apa yang TIDAK bisa dilakukan sistem ini?

**Jawaban:**
- Tidak bisa memproses multiple files secara otomatis (perlu wrapper script)
- Tidak bisa handle PDF input langsung (text_processor.py bisa, tapi run_batch.py membaca .txt)
- Tidak bisa deduplicate tripel antar chunks
- Tidak bisa recover dari API failures gracefully (prints error, continues)
- Tidak bisa report progress meaningfully (hanya "Processing chunk X/Y")
- Tidak bisa validate output quality (no quality checks)
- Tidak bisa handle rate limiting (no retry logic)

**Severity jika tidak ditangani:** MAJOR (saat scaling)

**Rencana mitigasi:** Pipeline improvements needed for ART-035 (batch extraction at scale): retry logic, dedup, quality checks, PDF support, progress reporting.

**Status mitigasi:** BELUM

---

## Ringkasan Review

| Aspek | Rating | Catatan |
|-------|--------|---------|
| Validitas Internal | N/A | Engineering test, bukan scientific claim |
| Validitas Eksternal | Rendah | Belum diuji pada skala nyata |
| Reproduktibilitas | Sedang | Code works, API non-deterministic |
| Novelty | Tidak Ada | Standard Python engineering |
| Kesiapan untuk Paper | Tidak Langsung | Ini infrastructure — tidak akan jadi section sendiri |

**Nilai sebagai Infrastructure:** Sedang — membuktikan modularitas kode, tapi perlu banyak improvement untuk production-scale ingestion
**Nilai sebagai Evidence untuk Paper Q1:** Sangat Rendah — engineering work, bukan scientific contribution
