# Review Protocol: Mandatory Critique Framework

Setiap eksperimen dan deliverable WAJIB melalui proses review ini sebelum dianggap selesai. Tujuannya: menangkap kelemahan **sebelum** reviewer jurnal menemukannya.

---

## 1. Sepuluh Pertanyaan Devil's Advocate

Setiap eksperimen HARUS menjawab **semua** pertanyaan berikut. Jawaban "tidak relevan" tidak diterima — jika sebuah pertanyaan terasa tidak relevan, jelaskan mengapa secara substantif.

### Integritas Metodologi

**Q1: Apakah hasilnya circular?**
Apakah sistem yang sama digunakan untuk generate DAN evaluate output? Jika DeepSeek mengekstrak tripel dan juga menilai kualitasnya, ini adalah circular evaluation. Bagaimana ini diatasi?

**Q2: Apakah baseline-nya fair?**
Apakah baseline yang digunakan benar-benar kompetitif, atau sengaja dibuat lemah (strawman)? Apakah ada sistem/metode existing yang seharusnya dibandingkan tapi tidak?

**Q3: Apakah skala datanya cukup untuk klaim yang dibuat?**
Berapa N? Apakah cukup untuk statistical significance? Apakah klaim generalization didukung oleh data dari multiple domains, bukan hanya satu contoh?

### Klaim & Kontribusi

**Q4: Apakah klaim "neuro-symbolic" genuinely earned?**
Jika symbolic reasoning hanya berupa graph traversal tanpa formal logic rules, apakah label "neuro-symbolic" justified? Apa yang membedakan ini dari sekadar LLM + database?

**Q5: Apakah novelty-nya real?**
Jika kita strip semua Indonesian legal domain specifics, apakah arsitekturnya masih novel? Atau ini hanyalah standard RAG pipeline yang di-rebrand?

**Q6: Apa yang bisa dilakukan sistem ini yang TIDAK bisa dilakukan oleh GPT-4 + simple prompt?**
Ini adalah pertanyaan paling penting. Jika jawabannya tidak convincing, arsitektur kita tidak justified.

### Validitas & Reproduktibilitas

**Q7: Apakah metrik evaluasi valid dan accepted di komunitas?**
Apakah metrik custom (seperti CCS) sudah divalidasi? Apakah ada bukti convergent/discriminant validity? Apakah inter-rater reliability dilaporkan?

**Q8: Bisakah hasilnya direproduksi oleh lab lain?**
Apakah semua data, kode, dan instruksi tersedia? Apakah ada dependency pada resource yang tidak publicly available?

**Q9: Apakah ada selection bias dalam pemilihan test cases?**
Apakah test cases dipilih karena "cocok" dengan sistem, atau secara random/sistematik dari corpus yang representative?

### Kejujuran Akademik

**Q10: Apa yang TIDAK bisa dilakukan sistem ini?**
Setiap paper Q1 harus memiliki Limitations section yang substantif. Jika limitations hanya berisi platitudes ("future work will address..."), ini adalah red flag.

---

## 2. Three-Layer Review Process

### Layer 1: Self-Critique (Peneliti sendiri)

- Jawab semua 10 pertanyaan di atas secara tertulis
- Tulis di `experiments/NN_nama/REVIEW.md`
- Minimum 200 kata per jawaban yang tidak trivial
- Deadline: segera setelah analisis selesai

### Layer 2: Adversarial AI Review (Independent LLM)

**KRITIS: Gunakan LLM BERBEDA dari DeepSeek untuk review.**

Ini memecah circular evaluation pada level meta. Jika DeepSeek digunakan untuk generate output, maka review harus menggunakan model independen.

```bash
# Jalankan adversarial reviewer
python -m src.review.adversarial_reviewer experiments/NN_nama/
```

Reviewer AI akan:
1. Membaca semua file dalam direktori eksperimen
2. Generate 5-10 kritik berdasarkan standar jurnal Q1
3. Memberikan severity rating (CRITICAL / MAJOR / MINOR)
4. Menyimpan output di `experiments/NN_nama/ai_review.json`

**Catatan:** Untuk Layer 2, opsi LLM yang bisa digunakan:
- Claude API (Anthropic) — **Recommended** karena arsitektur berbeda dari DeepSeek
- GPT-4 API (OpenAI) — Alternatif yang valid
- Model open-source besar (Llama 3, Mixtral) — Untuk budget terbatas

### Layer 3: Human Review Gate

- Minimal 1 reviewer manusia (idealnya domain expert)
- Reviewer membaca REVIEW.md + ai_review.json
- Keputusan final: PASS / CONDITIONAL / FAIL
- Documented di REVIEW.md bagian bawah

---

## 3. Review Timing

| Milestone | Review Required? | Layers |
|-----------|-----------------|--------|
| Setiap eksperimen selesai | **Ya** | Layer 1 + 2 |
| Sebelum integrasi ke pipeline utama | **Ya** | Layer 1 + 2 + 3 |
| Draft paper section selesai | **Ya** | Layer 1 + 2 + 3 |
| Pre-submission paper | **Ya** | Layer 1 + 2 + 3 (external reviewer jika memungkinkan) |

---

## 4. Severity Classification

Gunakan klasifikasi ini untuk temuan review:

| Severity | Definisi | Tindakan |
|----------|----------|----------|
| **CRITICAL** | Memilikinya dalam paper akan menyebabkan desk rejection | HARUS diperbaiki sebelum lanjut |
| **MAJOR** | Reviewer akan menggunakan ini sebagai alasan reject | HARUS diperbaiki atau dijustifikasi secara kuat |
| **MINOR** | Melemahkan paper tapi tidak fatal | SEBAIKNYA diperbaiki, minimal acknowledged |
| **SUGGESTION** | Peningkatan yang akan memperkuat paper | OPSIONAL tapi direkomendasikan |

---

## 5. Template Jawaban Review

Untuk setiap pertanyaan Q1-Q10, gunakan format:

```markdown
### Q[N]: [Judul Pertanyaan]

**Jawaban:** [Jawaban jujur, minimum 2-3 kalimat]

**Severity jika tidak ditangani:** [CRITICAL/MAJOR/MINOR]

**Rencana mitigasi:** [Langkah konkret, bukan "future work"]

**Status mitigasi:** [BELUM/SEDANG DIKERJAKAN/SELESAI]
```

---

## 6. Anti-Pattern yang Harus Dihindari

- **"BERHASIL"/"SANGAT BERHASIL" tanpa kuantifikasi** — Setiap klaim sukses harus disertai angka
- **Cherry-picking contoh** — Tunjukkan distribusi hasil, bukan hanya contoh terbaik
- **Mengabaikan kegagalan** — Kegagalan yang tidak dilaporkan adalah fraud akademik
- **Self-congratulatory language** — "Sistem kami sangat berhasil" bukan bahasa paper Q1
- **Metrics tanpa baseline** — Angka tanpa pembanding tidak bermakna
- **"Will be addressed in future work"** sebagai excuse — Jika sesuatu kritis, tangani sekarang
