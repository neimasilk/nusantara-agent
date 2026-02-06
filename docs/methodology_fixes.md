# Methodology Fixes Roadmap

Dokumen ini mendokumentasikan 6 kelemahan metodologi kritis yang teridentifikasi dari analisis honest terhadap status proyek saat ini, beserta rencana perbaikan konkret. Setiap kelemahan dipetakan ke eksperimen spesifik.

**Prinsip:** Mengakui kelemahan secara terbuka dan memperbaikinya secara sistematis lebih berharga untuk paper Q1 daripada menyembunyikannya.

---

## Weakness #1: Klaim "Neuro-Symbolic" Tidak Ter-Earn

### Masalah
Saat ini arsitektur terdiri dari LLM (neural) + Graph Database (storage). Tidak ada formal symbolic reasoning — graph traversal di NetworkX bukan penalaran simbolik dalam pengertian literatur AI. Label "neuro-symbolic" membutuhkan komponen reasoning berbasis aturan formal (logic programming, ontological reasoning, constraint satisfaction).

### Apa yang Akan Dikatakan Reviewer
> "The system appears to be a standard LLM-based extraction pipeline with graph storage. Where is the symbolic reasoning component? Graph traversal is not symbolic reasoning."

### Fix: Implement Formal Rule Engine (Experiment 05)

**Pendekatan:**
1. Encode prinsip-prinsip hukum adat sebagai Prolog-style rules menggunakan **PySwip** (Python-SWI-Prolog bridge) atau **owlready2** (OWL ontology reasoning)
2. Minimal 20 rules per domain hukum adat
3. Rules harus bisa melakukan inferensi yang TIDAK dilakukan oleh LLM:
   - Transitive reasoning (A waris B, B waris C → A indirect waris C)
   - Constraint checking (aturan X berlaku KECUALI kondisi Y)
   - Conflict detection (rule A kontradiksi rule B secara formal)

**Acceptance Criteria:**
- Rule engine menghasilkan jawaban yang BERBEDA dari pure LLM pada minimal 30% edge cases
- Formal proof bahwa inferensi tertentu membutuhkan symbolic reasoning (tidak bisa dicapai dengan prompting saja)
- Ablation: sistem dengan rule engine vs tanpa rule engine menunjukkan perbedaan signifikan (p < 0.05)

**Target Experiment:** `experiments/05_rule_engine/`

---

## Weakness #2: Circular Evaluation (DeepSeek Generate + Evaluate)

### Masalah
DeepSeek digunakan untuk mengekstrak tripel DAN keberhasilan dinilai secara kualitatif oleh peneliti tanpa ground truth independen. Ini adalah bentuk circular evaluation — sistem menilai outputnya sendiri. Tidak ada:
- Ground truth dataset dari expert annotations
- Independent model sebagai evaluator
- Inter-annotator agreement metrics
- Statistical significance tests

### Apa yang Akan Dikatakan Reviewer
> "How can you claim the extraction is successful when evaluation is based on subjective inspection by the same team that designed the system? Where is the ground truth? Where is the inter-rater reliability?"

### Fix: Independent Evaluation Pipeline (Experiment 06)

**Pendekatan:**
1. **Ground Truth Construction:**
   - Pilih 200 paragraf dari 3 domain hukum adat
   - 5 annotator manusia (minimal 2 ahli hukum adat) membuat gold-standard triples
   - Hitung Krippendorff's Alpha untuk inter-annotator agreement (target: >= 0.667)

2. **Independent LLM Judge:**
   - Gunakan model BERBEDA (Claude atau GPT-4) untuk mengevaluasi kualitas tripel
   - Model evaluator TIDAK boleh DeepSeek
   - Evaluasi dimensi: correctness, completeness, cultural accuracy

3. **External Ground Truth:**
   - Gunakan putusan MA (Mahkamah Agung) yang tersedia publik sebagai ground truth untuk legal reasoning
   - Bandingkan output sistem dengan keputusan pengadilan aktual

**Acceptance Criteria:**
- Krippendorff's Alpha >= 0.667 untuk inter-annotator agreement
- Evaluation menggunakan minimal 2 model LLM independen
- Statistical significance tests (paired t-test atau Wilcoxon) untuk semua perbandingan
- Cohen's Kappa >= 0.6 antara LLM judge dan human annotations

**Target Experiment:** `experiments/06_independent_eval/`

---

## Weakness #3: Multi-Agent Linear Chain, Bukan Real Orchestration

### Masalah
Arsitektur multi-agent saat ini adalah sequential chain sederhana:
```
national_law → adat_law → adjudicator → END
```
Ini bisa dicapai dengan 3 API calls berurutan tanpa framework multi-agent. Tidak ada:
- Parallel execution (agen bekerja bersamaan)
- Debate protocol (agen saling mengkritik)
- Self-correction (agen memperbaiki output sendiri berdasarkan feedback)
- Conditional routing (alur berbeda berdasarkan tipe query)

### Apa yang Akan Dikatakan Reviewer
> "What is the advantage of the multi-agent architecture over sequential prompting? The linear chain shows no emergent behavior or genuine agent interaction."

### Fix: Genuine Multi-Agent Orchestration (Experiment 07)

**Pendekatan:**
1. **Parallel Retrieval:** Agen Nasional dan Agen Adat berjalan paralel (bukan sequential)
2. **Debate Protocol:** Setelah initial analysis, kedua agen saling mengkritik output satu sama lain (minimal 2 rounds)
3. **Self-Correction Loop:** Agen bisa merevisi jawabannya berdasarkan kritik
4. **Conditional Routing:** Router node menentukan jalur berdasarkan tipe query (pure national, pure adat, conflict case, consensus case)
5. **Supervisor Arbitration:** Supervisor hanya aktif jika ada genuine disagreement

**Acceptance Criteria:**
- Measurable improvement dari debate protocol vs no-debate (pada metrik accuracy dan completeness)
- Conditional routing benar mengklasifikasikan minimal 85% test queries
- Self-correction memperbaiki minimal 40% errors yang terdeteksi
- Token efficiency: parallel execution mengurangi total time minimal 30%

**Target Experiment:** `experiments/07_advanced_orchestration/`

---

## Weakness #4: Scale Terlalu Kecil untuk Q1

### Masalah
Dataset saat ini:
- 1 teks sumber (~118 kata)
- ~30 tripel
- 1 test query
- 1 domain (Minangkabau saja)

Ini adalah proof-of-concept, bukan riset publishable. Jurnal Q1 mengharapkan:
- Ribuan data points
- Multiple domains/datasets
- Statistical tests dengan power yang cukup

### Apa yang Akan Dikatakan Reviewer
> "N=30 triples from a single text is insufficient to draw any conclusions. The single test query provides no statistical basis for the claims made."

### Fix: Scaling Plan

**Target Scale:**

| Dimensi | Current | Target | Rasio |
|---------|---------|--------|-------|
| Source texts | 1 | 100+ | 100x |
| Triples | ~30 | 10,000+ | 333x |
| Test queries | 1 | 200+ | 200x |
| Domains | 1 | 3 (Minangkabau, Bali, Jawa) + Nasional | 4x |
| Annotators | 0 | 5+ | ∞ |
| LLM models compared | 1 | 4+ (DeepSeek, GPT-4, Claude, Llama) | 4x |

**Implementation:**
- Phase 2 (Bulan 3-4): Scale KG ke 5,000+ triples dari 3 domains
- Phase 3 (Bulan 5-7): 200+ test cases, 5 annotators
- Phase 4 (Bulan 8-9): Full evaluation suite

**Tidak ada eksperimen tunggal** — ini adalah scaling effort across multiple experiments.

---

## Weakness #5: Ablation Menggunakan Strawman Baselines

### Masalah
Belum ada ablation study. Ketika direncanakan, baseline yang diusulkan harus kompetitif, bukan strawman. Baseline yang fair harus mencakup:
- Competitor LLM (GPT-4, Claude) dengan prompting yang sama
- Existing legal NLP tools
- Simple RAG (tanpa graph) sebagai ablation komponen
- Human expert baseline

### Apa yang Akan Dikatakan Reviewer
> "Without proper baselines including state-of-the-art LLMs and existing legal NLP systems, it is impossible to assess whether the proposed system provides genuine improvement."

### Fix: Proper Ablation Study (Experiment 09)

**8 Baselines yang Diperlukan:**

| # | Baseline | Tujuan |
|---|----------|--------|
| 1 | DeepSeek direct prompting (no RAG) | Apakah RAG membantu? |
| 2 | DeepSeek + Vector RAG (no graph) | Apakah graph membantu? |
| 3 | DeepSeek + Graph (no vector) | Apakah vector membantu? |
| 4 | Full pipeline tanpa rule engine | Apakah symbolic reasoning membantu? |
| 5 | Full pipeline tanpa debate protocol | Apakah multi-agent debate membantu? |
| 6 | GPT-4 + same pipeline | Apakah ini model-agnostic? |
| 7 | Claude + same pipeline | Cross-validation dengan model ketiga |
| 8 | Human expert (tanpa AI) | Upper bound performance |

**Acceptance Criteria:**
- Setiap baseline dijalankan 3x dengan random seed berbeda
- Statistical significance tests (paired t-test, p < 0.05) untuk setiap perbandingan
- Effect size dilaporkan (Cohen's d)
- Full pipeline harus beat minimal 6/7 automated baselines untuk claim validity
- Confidence intervals dilaporkan untuk semua metrics

**Target Experiment:** `experiments/09_ablation_study/`

---

## Weakness #6: CCS Metric Belum Divalidasi

### Masalah
Cultural Consistency Score (CCS) adalah metrik custom yang belum divalidasi. Tanpa validasi, reviewer akan mempertanyakan apakah metrik ini mengukur apa yang diklaim.

### Apa yang Akan Dikatakan Reviewer
> "The CCS metric appears to be ad-hoc. What evidence supports its validity? Has it been validated against human judgment? What is the inter-rater reliability?"

### Fix: Rigorous Metric Validation (Experiment 10)

**Pendekatan:**
1. **Inter-Rater Reliability:**
   - 5 annotator manusia menilai cultural consistency pada 100 outputs
   - Krippendorff's Alpha >= 0.667 (threshold untuk acceptable agreement)
   - Jika alpha < 0.667, metrik perlu redesign

2. **Convergent Validity:**
   - CCS harus berkorelasi (r > 0.6) dengan metrik lain yang mengukur konsep terkait
   - Kandidat: RAGAS faithfulness, human judgment scores

3. **Discriminant Validity:**
   - CCS harus TIDAK berkorelasi tinggi dengan metrik yang mengukur konsep berbeda
   - CCS harus bisa membedakan output yang culturally consistent vs inconsistent

4. **Weight Calibration:**
   - Gunakan Delphi method (3 rounds survey ke 5+ expert) untuk menentukan bobot komponen CCS
   - Bukan arbitrary weights yang ditentukan oleh researcher

**Acceptance Criteria:**
- Krippendorff's Alpha >= 0.667
- Convergent validity r > 0.6 dengan minimal 1 established metric
- Discriminant validity: significant difference antara consistent vs inconsistent outputs (p < 0.05)
- Delphi method menghasilkan stable weights (variasi < 10% antara round 2 dan 3)

**Target Experiment:** `experiments/10_metric_validation/`

---

## Ringkasan Timeline

| Weakness | Fix Experiment | Phase | Dependency |
|----------|---------------|-------|------------|
| #1 Neuro-Symbolic claim | Exp 05 (Rule Engine) | 2 | None |
| #2 Circular evaluation | Exp 06 (Independent Eval) | 2 | None |
| #3 Linear multi-agent | Exp 07 (Advanced Orchestration) | 3 | Exp 05 |
| #4 Scale too small | Scaling (across Exp 05-10) | 2-4 | None |
| #5 Strawman baselines | Exp 09 (Ablation) | 4 | Exp 05, 06, 07 |
| #6 CCS unvalidated | Exp 10 (Metric Validation) | 4 | Exp 06 |

---

## Status Tracking

| # | Weakness | Status | Progress |
|---|----------|--------|----------|
| 1 | Neuro-Symbolic claim | COMPLETED | 100% |
| 2 | Circular evaluation | PLANNED | 0% |
| 3 | Linear multi-agent | PLANNED | 0% |
| 4 | Scale too small | IN_PROGRESS | 15% |
| 5 | Strawman baselines | PLANNED | 0% |
| 6 | CCS unvalidated | PLANNED | 0% |

*Last updated: 2026-02-07*
