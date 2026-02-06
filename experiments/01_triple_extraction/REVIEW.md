# REVIEW: Eksperimen 01 — Ekstraksi Tripel Hukum Adat

**Reviewer:** Framework SOP (retrospektif)
**Tanggal:** 2026-02-06
**Status:** CONDITIONAL PASS — pilot valid, belum publishable

---

## Jawaban 10 Pertanyaan Devil's Advocate

### Q1: Apakah hasilnya circular?

**Jawaban:** Ya. DeepSeek mengekstrak tripel, dan keberhasilan dinilai secara kualitatif oleh peneliti yang merancang prompt. Tidak ada ground truth independen, tidak ada annotator terlatih, tidak ada model kedua yang memvalidasi. Analisis dalam `analysis.md` yang menyatakan "BERHASIL" didasarkan sepenuhnya pada inspeksi visual oleh tim yang sama.

**Severity jika tidak ditangani:** CRITICAL

**Rencana mitigasi:** Experiment 06 — independent evaluation pipeline dengan annotator manusia dan LLM judge terpisah.

**Status mitigasi:** BELUM — direncanakan

### Q2: Apakah baseline-nya fair?

**Jawaban:** Tidak ada baseline sama sekali. Eksperimen ini tidak membandingkan DeepSeek dengan model lain, metode lain, atau bahkan human annotator. Tanpa baseline, klaim "berhasil" tidak memiliki titik referensi.

**Severity jika tidak ditangani:** CRITICAL

**Rencana mitigasi:** Experiment 09 — ablation study dengan 8 baselines termasuk GPT-4, Claude, dan human expert.

**Status mitigasi:** BELUM — direncanakan

### Q3: Apakah skala datanya cukup untuk klaim yang dibuat?

**Jawaban:** Tidak. 1 teks sumber (~118 kata) menghasilkan ~30 tripel dari 1 domain (Minangkabau). Tidak ada statistical power untuk klaim apapun. `analysis.md` menggunakan bahasa definitif ("BERHASIL", "AI ternyata cukup pintar") yang tidak sesuai dengan skala bukti.

**Severity jika tidak ditangani:** CRITICAL

**Rencana mitigasi:** Scaling ke 10K+ tripel dari 3 domains. Lihat methodology_fixes.md Weakness #4.

**Status mitigasi:** BELUM — direncanakan

### Q4: Apakah klaim "neuro-symbolic" genuinely earned?

**Jawaban:** Pada tahap Exp 01, belum ada komponen symbolic sama sekali. Ini murni neural (LLM extraction). Label "neuro-symbolic" belum berlaku di titik ini. Ini valid untuk pilot — tapi perlu dicatat bahwa klaim ini harus di-earn oleh eksperimen selanjutnya.

**Severity jika tidak ditangani:** MAJOR (di tingkat paper, bukan di tingkat Exp 01)

**Rencana mitigasi:** Experiment 05 — formal rule engine. Klaim neuro-symbolic hanya valid setelah rule engine terintegrasi.

**Status mitigasi:** BELUM — direncanakan

### Q5: Apakah novelty-nya real?

**Jawaban:** Untuk Exp 01 sendiri, tidak ada novelty teknis. Mengekstrak structured information dari teks menggunakan LLM adalah well-established technique. Novelty terletak pada: (1) domain aplikasi (hukum adat Indonesia), dan (2) integrasi ke pipeline yang lebih besar. Tapi Exp 01 sendiri bukan novel.

**Severity jika tidak ditangani:** MINOR (untuk Exp 01 — novelty diharapkan dari pipeline keseluruhan)

**Rencana mitigasi:** Paper harus memposisikan Exp 01 sebagai langkah dalam pipeline, bukan sebagai kontribusi berdiri sendiri.

**Status mitigasi:** BELUM — akan ditangani saat penulisan paper

### Q6: Apa yang bisa dilakukan sistem ini yang TIDAK bisa dilakukan oleh GPT-4 + simple prompt?

**Jawaban:** Pada tahap Exp 01, kemungkinan besar tidak ada. GPT-4 dengan prompt serupa kemungkinan menghasilkan output yang setidaknya setara. Diferensiasi belum ada. Ini jujur perlu diakui.

**Severity jika tidak ditangani:** CRITICAL (di tingkat paper)

**Rencana mitigasi:** Diferensiasi akan datang dari: rule engine (Exp 05), multi-agent orchestration (Exp 07), dan evaluation framework (Exp 06, 09, 10). Pipeline terintegrasi harus menunjukkan keunggulan atas simple prompting.

**Status mitigasi:** BELUM

### Q7: Apakah metrik evaluasi valid dan accepted di komunitas?

**Jawaban:** Tidak ada metrik formal yang digunakan di Exp 01. Evaluasi berupa inspeksi kualitatif. Untuk pilot test ini acceptable, tapi harus ada metrik formal di eksperimen selanjutnya.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Exp 06 (evaluation pipeline), Exp 10 (CCS validation)

**Status mitigasi:** BELUM

### Q8: Bisakah hasilnya direproduksi oleh lab lain?

**Jawaban:** Partially. Kode dan data tersedia, tapi: (1) DeepSeek API responses bersifat non-deterministic tanpa fixed seed, (2) model bisa berubah dari waktu ke waktu (API versioning), (3) prompt exact diperlukan. Reproduksibilitas tidak dijamin.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Set temperature=0, log model version, seed if available, simpan exact response.

**Status mitigasi:** BELUM

### Q9: Apakah ada selection bias dalam pemilihan test cases?

**Jawaban:** Ya. Teks sumber dipilih karena "representatif" menurut judgment peneliti, bukan secara random atau sistematik dari corpus yang representative. Ini memungkinkan (bahkan jika tidak disengaja) pemilihan teks yang "cocok" dengan kemampuan model.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Exp 06 akan menggunakan systematic sampling dari corpus yang lebih besar.

**Status mitigasi:** BELUM

### Q10: Apa yang TIDAK bisa dilakukan sistem ini?

**Jawaban (saat Exp 01):**
- Tidak bisa menangani teks multi-paragraf yang panjang (belum diuji)
- Tidak bisa membedakan ambiguitas dari kepastian (confidence selalu 1.0)
- Tidak bisa menangani teks berkualitas rendah (OCR artifacts)
- Tidak bisa mengekstrak relasi temporal atau kondisional secara akurat
- Tidak bisa di-evaluate tanpa human inspection
- Tidak ada mekanisme self-correction jika tripel salah

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Sebagian besar akan ditangani oleh Exp 04 (batch), 05 (rule engine), 06 (evaluation), 07 (self-correction)

**Status mitigasi:** SEBAGIAN — Exp 04 sudah menangani batch processing

---

## Ringkasan Review

| Aspek | Rating | Catatan |
|-------|--------|---------|
| Validitas Internal | Lemah | Tidak ada ground truth, circular evaluation |
| Validitas Eksternal | Sangat Lemah | N=1, 1 domain |
| Reproduktibilitas | Sedang | Kode tersedia, tapi non-deterministic |
| Novelty | Rendah | Standard LLM extraction |
| Kesiapan untuk Paper | Tidak Siap | Perlu scaling + validasi independen |

**Nilai sebagai Pilot:** Tinggi — membuktikan feasibility teknis dasar
**Nilai sebagai Evidence untuk Paper Q1:** Rendah — tidak cukup untuk klaim apapun
