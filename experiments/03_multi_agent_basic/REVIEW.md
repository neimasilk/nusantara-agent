# REVIEW: Eksperimen 03 — Orkestrasi Multi-Agen Dasar

**Reviewer:** Framework SOP (retrospektif)
**Tanggal:** 2026-02-06
**Status:** CONDITIONAL PASS — pipeline berjalan, tapi klaim "orchestration" terlalu kuat

---

## Jawaban 10 Pertanyaan Devil's Advocate

### Q1: Apakah hasilnya circular?

**Jawaban:** Ya, pada dua level. (1) DeepSeek digunakan untuk semua 3 agen DAN untuk generate test data (Exp 01). Ini berarti model yang sama memproduksi knowledge base DAN melakukan reasoning atasnya. (2) Keberhasilan dinilai secara kualitatif oleh tim yang merancang prompt. Tidak ada evaluator independen.

**Severity jika tidak ditangani:** CRITICAL

**Rencana mitigasi:** Exp 06 (independent evaluation), Exp 07 (diverse model testing)

**Status mitigasi:** BELUM

### Q2: Apakah baseline-nya fair?

**Jawaban:** Tidak ada baseline. Tidak dibandingkan dengan: (1) single-agent approach (1 LLM call dengan semua konteks), (2) manual synthesis oleh legal expert, (3) simpler pipeline (tanpa LangGraph). Tanpa baseline, klaim "SANGAT BERHASIL" tidak memiliki referensi.

**Severity jika tidak ditangani:** CRITICAL

**Rencana mitigasi:** Exp 09 ablation study — Baseline 5 (full pipeline tanpa debate) secara langsung membandingkan single vs multi-agent.

**Status mitigasi:** BELUM

### Q3: Apakah skala datanya cukup?

**Jawaban:** Tidak. N=1 query. Satu kasus keberhasilan bukan evidence. Bahkan jika kasus ini sempurna, kita tidak tahu apakah pipeline bekerja pada kasus lain, pada domain lain, atau pada kasus adversarial.

**Severity jika tidak ditangani:** CRITICAL

**Rencana mitigasi:** 200 test cases (ART-050) dan scaling across 3 domains.

**Status mitigasi:** BELUM

### Q4: Apakah klaim "neuro-symbolic" genuinely earned?

**Jawaban:** Tidak di Exp 03. Ini murni neural — 3 LLM calls dengan prompt engineering berbeda. Tidak ada komponen symbolic. Knowledge Graph dari Exp 01 di-inject sebagai teks ke prompt Agen Adat, bukan digunakan untuk symbolic reasoning. Ini adalah RAG, bukan neuro-symbolic.

**Severity jika tidak ditangani:** CRITICAL

**Rencana mitigasi:** Rule engine integration (Exp 05) harus dibuktikan memberikan value.

**Status mitigasi:** BELUM

### Q5: Apakah novelty-nya real?

**Jawaban:** Multi-agent LLM systems adalah area yang well-explored. Sequential agent pipeline dengan LangGraph bukanlah novel — ini adalah documented pattern di LangGraph documentation. Novelty hanya ada di domain aplikasi (hukum adat Indonesia). Teknis, kontribusi sangat rendah.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Exp 07 harus mengimplementasikan genuine orchestration patterns (debate, self-correction, conditional routing) yang membedakan dari vanilla LangGraph usage.

**Status mitigasi:** BELUM

### Q6: Apa yang bisa dilakukan sistem ini yang TIDAK bisa dilakukan oleh GPT-4 + simple prompt?

**Jawaban:** Pada implementasi saat ini, kemungkinan besar tidak ada. Single prompt ke GPT-4: "Analisis kasus ini dari perspektif hukum nasional dan adat Minangkabau, lalu sintesiskan" mungkin menghasilkan output yang setara. Multi-agent approach belum menunjukkan keunggulan atas single-agent.

Potensi keunggulan multi-agent (specialization, debate, self-correction) belum diimplementasikan. Keunggulan harus dibuktikan secara empiris di Exp 07 dan 09.

**Severity jika tidak ditangani:** CRITICAL

**Rencana mitigasi:** Exp 07 + Exp 09 (ablation) harus menunjukkan measurable improvement dari multi-agent vs single-agent.

**Status mitigasi:** BELUM

### Q7: Apakah metrik evaluasi valid?

**Jawaban:** Tidak ada metrik evaluasi. `analysis.md` menggunakan kata "SANGAT BERHASIL" dan "elegan" tanpa kuantifikasi apapun. Ini bukan bahasa ilmiah. Paper Q1 membutuhkan: accuracy, completeness, cultural sensitivity scores, inter-rater reliability.

**Severity jika tidak ditangani:** CRITICAL

**Rencana mitigasi:** Formal evaluation framework di Exp 06 dan 10.

**Status mitigasi:** BELUM

### Q8: Bisakah hasilnya direproduksi?

**Jawaban:** Tidak sepenuhnya. (1) DeepSeek responses non-deterministic, (2) output tidak disimpan ke file, (3) result.json dari Exp 01 (yang dibaca oleh Agen Adat) juga non-deterministic. Jika Exp 01 dijalankan ulang, input ke Exp 03 berubah.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Simpan semua intermediate outputs, set temperature=0, log model versions.

**Status mitigasi:** BELUM

### Q9: Apakah ada selection bias?

**Jawaban:** Ya. Query test dipilih karena mewakili kasus di mana konvergensi diharapkan (Pusako Rendah — di mana hukum nasional dan adat cenderung sejalan). Kasus yang lebih sulit (Pusako Tinggi, kasus lintas domain, kasus ambigu) tidak diuji. Ini bias ke arah showing the system works.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** 200 test cases termasuk adversarial cases.

**Status mitigasi:** BELUM

### Q10: Apa yang TIDAK bisa dilakukan sistem ini?

**Jawaban:**
- Tidak bisa menangani kasus di mana agen disagreement secara genuine (no resolution mechanism selain supervisor summary)
- Tidak bisa explain reasoning chain (no provenance tracking)
- Tidak bisa handle multi-domain cases (hanya Minangkabau + Nasional)
- Tidak bisa self-correct jika salah satu agen memberikan informasi yang salah
- Tidak bisa routing berbeda berdasarkan tipe query
- Tidak bisa handle ambiguitas (selalu memberikan jawaban definitif)
- Tidak bisa operate tanpa full context (semua state dikirim ke setiap agen — tidak scalable)

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Exp 07 menangani debate, self-correction, conditional routing.

**Status mitigasi:** BELUM

---

## Catatan Khusus tentang Bahasa di analysis.md

`analysis.md` Exp 03 menggunakan bahasa yang perlu di-revisi untuk paper:

| Bahasa di analysis.md | Masalah | Alternatif untuk Paper |
|----------------------|---------|----------------------|
| "SANGAT BERHASIL" | Superlative tanpa kuantifikasi | "Pipeline executed successfully on the test case" |
| "elegan dan akademis" | Self-congratulatory | Hapus — biarkan evidence berbicara |
| "Baseline Sistem terbentuk" | Overclaim — ini bukan baseline ilmiah | "Initial prototype demonstrates feasibility" |

---

## Ringkasan Review

| Aspek | Rating | Catatan |
|-------|--------|---------|
| Validitas Internal | Sangat Lemah | Circular eval, no metrics, no baseline |
| Validitas Eksternal | Sangat Lemah | N=1, 1 domain, biased query |
| Reproduktibilitas | Lemah | Non-deterministic, output not saved |
| Novelty | Rendah | Standard LangGraph pattern |
| Kesiapan untuk Paper | Tidak Siap | Fundamental issues perlu ditangani |

**Nilai sebagai Pilot:** Sedang — menunjukkan bahwa 3-agent pipeline bisa berjalan
**Nilai sebagai Evidence untuk Paper Q1:** Sangat Rendah — klaim terlalu kuat untuk evidence yang ada
