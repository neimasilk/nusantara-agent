# Review: Experiment 05 - Formal Rule Engine

**Reviewer:** Self-critique (Layer 1)
**Date:** 2026-02-07
**Status:** Layer 1 selesai. Layer 2 (Adversarial AI) dan Layer 3 (Human) belum dilakukan.

---

## Integritas Metodologi

### Q1: Apakah hasilnya circular?

**Jawaban:** Sebagian. Rule Engine (Clingo/ASP) bersifat deterministik dan tidak menggunakan LLM, sehingga sisi simbolik tidak circular. Namun, gold standard (expected answers di test_cases.json) disusun oleh tim yang sama yang membangun rule base. Ini berarti evaluasi Rule Engine bersifat self-referential: rules ditulis berdasarkan pemahaman yang sama dengan yang menghasilkan expected answers. LLM evaluation juga bermasalah karena expected answers belum divalidasi oleh domain expert independen.

**Severity jika tidak ditangani:** CRITICAL

**Rencana mitigasi:** (1) Validasi gold standard oleh minimal 2 ahli hukum adat Minangkabau independen. (2) Gunakan putusan pengadilan (MA/Pengadilan Tinggi) sebagai ground truth alternatif. (3) Exp 06 akan membangun independent evaluation pipeline.

**Status mitigasi:** BELUM

---

### Q2: Apakah baseline-nya fair?

**Jawaban:** Baseline adalah DeepSeek-chat dengan standard prompting. Ini adalah baseline yang reasonable untuk menunjukkan perbedaan neural vs symbolic, tetapi bukan baseline kompetitif dalam arti state-of-the-art. Tidak ada perbandingan dengan: (1) GPT-4 atau Claude sebagai LLM yang lebih kuat, (2) sistem legal reasoning yang sudah ada, (3) rule engine alternatif (Prolog, Drools). Klaim bahwa "LLM gagal pada hard constraints" hanya dibuktikan terhadap satu model.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Tambah minimal 1 LLM alternatif (GPT-4 atau Claude) sebagai baseline tambahan di iterasi berikutnya. Bandingkan juga dengan few-shot prompting yang mengandung aturan eksplisit.

**Status mitigasi:** BELUM

---

### Q3: Apakah skala datanya cukup untuk klaim yang dibuat?

**Jawaban:** N=30 test cases cukup untuk proof-of-concept dan menunjukkan pola divergensi, tetapi tidak cukup untuk klaim statistik yang kuat. Confidence interval untuk divergence rate 33.3% pada N=30 sangat lebar. Semua test cases berasal dari satu domain (Minangkabau) dan satu topik (hukum waris). Generalisasi ke domain lain (Bali, Jawa) atau topik lain (tanah, pidana adat) belum dibuktikan.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Scaling plan: 200+ test cases, 3 domains, multiple topik hukum. Lakukan power analysis untuk menentukan N minimum yang dibutuhkan untuk statistical significance.

**Status mitigasi:** BELUM

---

## Klaim & Kontribusi

### Q4: Apakah klaim "neuro-symbolic" genuinely earned?

**Jawaban:** Ya, lebih earned dibanding sebelum Exp 05. ClingoRuleEngine mengimplementasikan Answer Set Programming (formal logic) yang genuinely symbolic — bukan sekadar graph traversal atau keyword matching. Divergence rate 33.3% memberikan bukti empiris bahwa komponen simbolik memberikan nilai tambah yang tidak bisa direplikasi oleh komponen neural saja. Namun, integrasi keduanya masih loose-coupled: Rule Engine dan LLM dijalankan secara independen, bukan sebagai satu inference pipeline yang terintegrasi.

**Severity jika tidak ditangani:** MINOR

**Rencana mitigasi:** Implementasi "Symbolic-First Validation" di mana hasil Rule Engine menjadi mandatory context untuk LLM (direncanakan di arsitektur Phase 3).

**Status mitigasi:** BELUM

---

### Q5: Apakah novelty-nya real?

**Jawaban:** Novelty parsial. Penggunaan ASP untuk formalisasi hukum adat (bukan hanya hukum positif/tertulis) relatif baru dalam literatur. Namun, arsitektur "rule engine vs LLM comparison" sendiri bukan novel — banyak paper yang sudah membandingkan symbolic vs neural. Kontribusi utama ada pada domain application (hukum adat pluralistik Indonesia) bukan pada metode.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Perkuat novelty melalui: (1) formalisasi multi-domain (3 sistem adat), (2) mekanisme conflict resolution otomatis antara symbolic dan neural output, (3) CCS metric yang divalidasi.

**Status mitigasi:** BELUM

---

### Q6: Apa yang bisa dilakukan sistem ini yang TIDAK bisa dilakukan oleh GPT-4 + simple prompt?

**Jawaban:** Berdasarkan data Exp 05, pada 10/30 kasus Rule Engine menolak jawaban LLM yang "terlihat benar secara moral" tapi salah secara formal adat. Contoh konkret: LLM memberikan hak waris pusako tinggi kepada laki-laki yang "sudah mengabdi lama" — Rule Engine menolak karena gender adalah predikat mutlak dalam aturan matrilineal. GPT-4 dengan simple prompt kemungkinan besar akan menunjukkan bias yang sama (cenderung "adil" menurut standar modern, bukan standar adat). Namun, ini belum dibuktikan secara empiris terhadap GPT-4.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** Jalankan test suite yang sama pada GPT-4 dan Claude untuk membuktikan bahwa bias ini bukan spesifik DeepSeek.

**Status mitigasi:** BELUM

---

## Validitas & Reproduktibilitas

### Q7: Apakah metrik evaluasi valid dan accepted di komunitas?

**Jawaban:** Metrik utama (accuracy vs gold standard, divergence rate) adalah metrik standar dan accepted. Namun, validitas gold standard sendiri dipertanyakan (lihat Q1). Tidak ada inter-rater reliability karena hanya satu annotator yang membuat gold standard.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** (1) Minimal 3 annotator untuk gold standard, (2) Hitung Cohen's kappa / Fleiss' kappa, (3) Gunakan putusan pengadilan sebagai external validation.

**Status mitigasi:** BELUM

---

### Q8: Bisakah hasilnya direproduksi oleh lab lain?

**Jawaban:** Sebagian besar ya. Rule Engine bersifat deterministik dan akan menghasilkan output yang sama. Namun, LLM output tidak deterministik (temperature, model version). `result.json` menyimpan semua output sehingga analisis bisa direplikasi. Kode dan rules tersedia di repository. Keterbatasan: DeepSeek API mungkin berubah versi model tanpa pemberitahuan.

**Severity jika tidak ditangani:** MINOR

**Rencana mitigasi:** Catat versi model yang digunakan (deepseek-chat), simpan semua raw output, dan sediakan script reproduksi yang self-contained.

**Status mitigasi:** SEDANG DIKERJAKAN (result.json sudah tersimpan)

---

### Q9: Apakah ada selection bias dalam pemilihan test cases?

**Jawaban:** Ada risiko. Test cases dirancang untuk menguji skenario yang "menarik" (edge cases, konflik norma). Ini by design untuk proof-of-concept, tapi bisa menghasilkan overestimate divergence rate jika dibandingkan dengan distribusi kasus real di pengadilan. Tidak ada sampling dari corpus kasus pengadilan yang representative.

**Severity jika tidak ditangani:** MAJOR

**Rencana mitigasi:** (1) Tambahkan test cases dari putusan MA aktual, (2) Buat distribusi yang mencerminkan frekuensi kasus real, (3) Laporkan divergence rate per kategori kasus.

**Status mitigasi:** BELUM

---

## Kejujuran Akademik

### Q10: Apa yang TIDAK bisa dilakukan sistem ini?

**Jawaban:** Keterbatasan substansif:
1. **Rule Engine gagal pada 30% kasus** — skenario situasional (mufakat, darurat, konteks sosial) tidak bisa diformalisasi dalam ASP tanpa fuzzy logic atau probabilistic reasoning.
2. **Hanya satu domain** — belum diuji pada Bali atau Jawa.
3. **Hanya hukum waris** — belum diuji pada tanah, pidana adat, atau hukum keluarga lainnya.
4. **Tidak ada real-time update** — rules harus diubah manual oleh developer, bukan learned dari data.
5. **Gold standard belum tervalidasi** — semua angka accuracy bersifat provisional.
6. **Tidak bisa menangani ambiguitas linguistik** — teks hukum adat yang ambigu memerlukan interpretasi kontekstual yang di luar kemampuan ASP.

**Severity jika tidak ditangani:** CRITICAL (jika limitations tidak dilaporkan secara jujur di paper)

**Rencana mitigasi:** Semua keterbatasan di atas akan masuk ke Limitations section paper. Tidak ada mitigasi yang bisa menghilangkan semua keterbatasan ini — sebagian adalah inherent trade-off dari pendekatan symbolic.

**Status mitigasi:** ACKNOWLEDGED

---

## Ringkasan Severity

| Severity | Count | Pertanyaan |
|----------|-------|------------|
| CRITICAL | 2 | Q1, Q10 |
| MAJOR | 6 | Q2, Q3, Q5, Q6, Q7, Q9 |
| MINOR | 2 | Q4, Q8 |

---

## Status Review

- [x] **Layer 1: Self-Critique** — Selesai (2026-02-07)
- [ ] **Layer 2: Adversarial AI Review** — Belum. Jalankan: `python -m src.review.adversarial_reviewer experiments/05_rule_engine/`
- [ ] **Layer 3: Human Review Gate** — Belum.
