# Critique & Strategic Risk Assessment
**Tanggal:** 6 Februari 2026
**Status:** Internal Review — Updated with Honest Methodology Weaknesses
**Last Updated:** 2026-02-06

---

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

## 3. Update Pasca-Pilot (Eksperimen 1-3)

Berdasarkan hasil eksperimen awal pada Februari 2026, beberapa risiko awal telah berhasil dimitigasi:

*   **Mitigasi Semantic Loss (Exp 1):** DeepSeek terbukti mampu membedakan nuansa hukum yang halus (misal: memisahkan 'Otoritas Mamak' vs 'Kepemilikan Perempuan'). Risiko ini diturunkan dari *Tinggi* ke *Sedang/Terkendali*.
*   **Mitigasi Ambiguity (Exp 3):** Pendekatan Multi-Agent terbukti mampu menangani ambiguitas bukan dengan memberikan satu jawaban kaku, melainkan dengan sintesis pluralistik yang menghormati kedua sistem hukum. Ini membuktikan bahwa sistem bisa menghindari jebakan "reduksionisme".
*   **Mitigasi Graph Complexity (Exp 2):** Struktur tripel yang dihasilkan ternyata sangat *queryable* dan *traversable*, membuktikan bahwa pipeline Neuro-Symbolic ini layak diteruskan ke skala yang lebih besar.

**CATATAN PENTING:** Mitigasi di atas berdasarkan pilot dengan N sangat kecil (1 teks, ~30 tripel, 1 query). Lihat Bagian 5 untuk honest assessment dari kelemahan yang tersisa.

## 4. Komitmen Riset

Meskipun beberapa risiko telah dimitigasi, proyek tetap mempertahankan kewaspadaan terhadap kualitas data (OCR) dan skalabilitas agen. Fase selanjutnya akan fokus pada pengolahan data massal dengan tetap merujuk pada prinsip-prinsip mitigasi yang telah diperbarui ini.

---

## 5. Enam Kelemahan Metodologi Kritis (Honest Assessment)

Bagian ini menambahkan assessment jujur terhadap kelemahan fundamental yang harus ditangani sebelum paper layak submit ke jurnal Q1. Setiap kelemahan dipetakan ke rencana perbaikan di `docs/methodology_fixes.md`.

### Weakness #1: Klaim "Neuro-Symbolic" Tidak Substantif
**Severity:** CRITICAL

Saat ini arsitektur terdiri dari LLM (neural) + Graph Database (storage). Graph traversal di NetworkX bukan symbolic reasoning. Tidak ada formal logic, rule engine, constraint satisfaction, atau ontological reasoning. Reviewer Q1 akan langsung menolak klaim "neuro-symbolic" tanpa komponen reasoning formal.

**Fix:** Implement formal rule engine dengan PySwip/owlready2 (Experiment 05). Lihat `docs/methodology_fixes.md` Weakness #1.

### Weakness #2: Circular Evaluation
**Severity:** CRITICAL

DeepSeek mengekstrak data DAN hasilnya dinilai oleh tim yang sama tanpa ground truth independen. Ini adalah circular evaluation — fatal untuk paper Q1. Tidak ada:
- Ground truth dataset dari expert annotations
- Independent model sebagai evaluator
- Inter-annotator agreement metrics
- Statistical significance tests

**Fix:** Independent evaluation pipeline — LLM berbeda + 5 annotator manusia + putusan MA sebagai ground truth (Experiment 06). Lihat `docs/methodology_fixes.md` Weakness #2.

### Weakness #3: Multi-Agent Hanya Linear Chain
**Severity:** MAJOR

Arsitektur multi-agent adalah sequential chain (A → B → C) tanpa paralelisme, debate, self-correction, atau conditional routing. Ini tidak membedakan sistem dari 3 API calls berurutan. Klaim "orchestration" dan "agentic" tidak didukung oleh implementasi saat ini.

**Fix:** Parallel retrieval, agent debate protocol, self-correction loop, conditional routing (Experiment 07). Lihat `docs/methodology_fixes.md` Weakness #3.

### Weakness #4: Skala Terlalu Kecil
**Severity:** CRITICAL

Total data: 1 teks (~118 kata), ~30 tripel, 1 test query, 1 domain. Ini adalah proof of concept, bukan evidence untuk publication. Jurnal Q1 mengharapkan ribuan data points dengan statistical testing.

**Fix:** Scale ke 10K+ triples, 200+ test cases, 5+ annotators, 3 domains. Lihat `docs/methodology_fixes.md` Weakness #4.

### Weakness #5: Tidak Ada Baseline/Ablation yang Proper
**Severity:** CRITICAL

Belum ada perbandingan dengan sistem lain atau ablation komponen. Tanpa baseline (GPT-4, Claude, existing tools, human expert), klaim keunggulan tidak bisa dibuat. Ablation yang direncanakan harus menggunakan competitive baselines, bukan strawman.

**Fix:** 8 proper baselines dengan statistical significance testing (Experiment 09). Lihat `docs/methodology_fixes.md` Weakness #5.

### Weakness #6: CCS Metric Belum Divalidasi
**Severity:** MAJOR

Cultural Consistency Score (CCS) adalah metrik custom yang belum divalidasi. Tanpa inter-rater reliability, convergent/discriminant validity, dan expert calibration, reviewer akan menolak metrik ini.

**Fix:** Rigorous metric validation — Krippendorff's Alpha, Delphi method, validity testing (Experiment 10). Lihat `docs/methodology_fixes.md` Weakness #6.

### Ringkasan Status Kelemahan

| # | Weakness | Severity | Status | Fix |
|---|----------|----------|--------|-----|
| 1 | Neuro-Symbolic claim | CRITICAL | PLANNED | Exp 05 |
| 2 | Circular evaluation | CRITICAL | PLANNED | Exp 06 |
| 3 | Linear multi-agent | MAJOR | PLANNED | Exp 07 |
| 4 | Scale too small | CRITICAL | PLANNED | Scaling |
| 5 | No proper baselines | CRITICAL | PLANNED | Exp 09 |
| 6 | CCS unvalidated | MAJOR | PLANNED | Exp 10 |

---

## 6. Referensi Internal

- Failure registry detail: `docs/failure_registry.md`
- Methodology fixes roadmap: `docs/methodology_fixes.md`
- Task decomposition: `docs/task_registry.md`
- Review protocol: `docs/review_protocol.md`
- Experiment SOP: `docs/experiment_template.md`
