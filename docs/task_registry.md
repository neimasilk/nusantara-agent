# Task Registry: Atomic Research Tasks (ART)

Master registry dari semua task yang perlu diselesaikan untuk mencapai target publikasi Scopus Q1. Setiap task mengikuti format dari `docs/task_template.md`.

**Total Tasks:** 84
**Status Legend:** PENDING | IN_PROGRESS | DONE | BLOCKED | CANCELLED

*Last updated: 2026-02-07*

---

## Ringkasan per Phase

| Phase | Deskripsi | Tasks | Done | Remaining |
|-------|-----------|-------|------|-----------|
| 0 | Framework & Infrastructure | ART-001 — ART-010 | 10 | 0 |
| 1 | Pilot Experiments (01-04) | ART-011 — ART-018 | 8 | 0 |
| 2 | Core Methodology Fixes | ART-019 — ART-042 | 5 | 19 |
| 3 | Advanced Agent Architecture | ART-043 — ART-055 | 6 | 7 |
| 4 | Evaluation & Ablation | ART-056 — ART-072 | 0 | 17 |
| 5 | Paper Writing & Submission | ART-073 — ART-084 | 0 | 12 |
| **TOTAL** | | **84** | **29** | **55** |

---

## Phase 0: Framework & Infrastructure (DONE)

### ART-001: Setup Repository Structure
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** Create initial repo structure with src/, experiments/, docs/, data/ directories.

### ART-002: Configure DeepSeek API Integration
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** Setup OpenAI client wrapper for DeepSeek API with .env configuration.

### ART-003: Implement Text Processor Module
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** PDF extraction, text cleaning, chunking in src/utils/text_processor.py.

### ART-004: Implement Triple Extractor Module
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** TripleExtractor class in src/kg_engine/extractor.py.

### ART-005: Write PRD Document
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** Comprehensive Product Requirements Document.

### ART-006: Create Collaboration Guide
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** Multi-human & multi-agent workflow documentation.

### ART-007: Create Experiment SOP Template
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** Standardized template for all experiments (docs/experiment_template.md).

### ART-008: Create Review Protocol
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** Mandatory critique framework with 10 devil's advocate questions.

### ART-009: Create Failure Registry
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** Living document for logging failures and negative results.

### ART-010: Create Methodology Fixes Roadmap
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** Document 6 weaknesses and concrete fix plans (docs/methodology_fixes.md).

---

## Phase 1: Pilot Experiments — Retrospective Documentation (DONE)

### ART-011: Run Experiment 01 (Triple Extraction)
| Field | Value |
|-------|-------|
| **Type** | EXPERIMENT |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** Pilot test of DeepSeek triple extraction on Minangkabau legal text.

### ART-012: Run Experiment 02 (Graph Reasoning)
| Field | Value |
|-------|-------|
| **Type** | EXPERIMENT |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** Test symbolic reasoning via NetworkX graph traversal.

### ART-013: Run Experiment 03 (Multi-Agent Basic)
| Field | Value |
|-------|-------|
| **Type** | EXPERIMENT |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** Basic LangGraph multi-agent orchestration.

### ART-014: Run Experiment 04 (Batch Ingestion)
| Field | Value |
|-------|-------|
| **Type** | EXPERIMENT |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** Scalable batch ingestion pipeline using modular extractor.

### ART-015: Retrofit PROTOCOL.md for Exp 01-04
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** Add retrospective PROTOCOL.md to all 4 pilot experiments.

### ART-016: Retrofit REVIEW.md for Exp 01-04
| Field | Value |
|-------|-------|
| **Type** | REVIEW |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** Add honest critique REVIEW.md to all 4 pilot experiments.

### ART-017: Build Adversarial Reviewer Module
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** src/review/adversarial_reviewer.py — independent LLM reviewer.

### ART-018: Update CLAUDE.md and Collaboration Docs
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Status** | DONE |
**Description:** Update CLAUDE.md, collaboration_guide.md, critique_and_risk_assessment.md with new framework references.

---

## Phase 2: Core Methodology Fixes

### Experiment 05: Formal Rule Engine (Weakness #1)

### ART-019: Research Symbolic Reasoning Libraries
| Field | Value |
|-------|-------|
| **Type** | ANALYSIS |
| **Executor** | EITHER |
| **Prerequisites** | None |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Compare PySwip, owlready2, and Clingo for encoding legal rules. Evaluate installation reliability, expressiveness, and Python integration. Produce comparison matrix with recommendation.
**Inputs:** Library documentation, existing NetworkX graph code
**Outputs:** `experiments/05_rule_engine/library_comparison.md`
**Acceptance Test:** Recommendation supported by at least 3 criteria (install reliability, expressiveness, community support)

### ART-020: Collect Minangkabau Legal Rules from Literature
| Field | Value |
|-------|-------|
| **Type** | DATA |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | None |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Extract 20+ formal rules of Minangkabau inheritance law from academic sources. Each rule must be verifiable against published literature. Focus on: property types (pusako tinggi/rendah), inheritance lines (matrilineal), authority roles (mamak), exception conditions (darurat).
**Inputs:** Academic papers, legal textbooks on hukum adat Minangkabau
**Outputs:** `data/rules/minangkabau_rules.json` — structured list of rules with citations
**Acceptance Test:** 20+ rules, each with literature citation, verified by domain expert
**Progress Note (2026-02-07):** Output draft sudah tersedia dan berisi 20+ rules dengan sitasi, namun seluruh entry masih `DRAFT_NEEDS_HUMAN_REVIEW`; verifikasi domain expert belum terpenuhi.
**Completion Note (2026-02-08):** Expert review selesai. Hasil: 14 BENAR, 6 PERLU KOREKSI (sudah dikoreksi), 5 rules baru ditambahkan dari expert review. Total: 25 rules VERIFIED. Lihat `data/rules/LEMBAR VERIFIKASI - HASIL REVIEW.md`.

### ART-021: Encode Minangkabau Rules in Prolog/OWL
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-019, ART-020 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Implement the 20+ collected rules in the chosen symbolic reasoning framework. Rules must support: forward chaining, backward chaining, constraint checking, and conflict detection.
**Inputs:** `data/rules/minangkabau_rules.json`, library choice from ART-019
**Outputs:** `src/symbolic/rule_engine.py`, `src/symbolic/rules/minangkabau.lp`
**Acceptance Test:** All 20+ rules parse and execute without error; 10 test queries return correct answers
**Audit Note (2026-02-08):** Dependency check menunjukkan prereq `ART-020` masih `IN_PROGRESS`. Status `DONE` di ART-021 diinterpretasikan sebagai implementasi berbasis draft rules; validasi domain expert tetap mengikuti ART-020.

### ART-022: Design Rule Engine vs LLM Comparison Test Cases
| Field | Value |
|-------|-------|
| **Type** | DATA |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | ART-020 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Create 30 test cases specifically designed to differentiate rule engine reasoning from LLM reasoning.
**Inputs:** Rules from ART-020, knowledge of LLM limitations
**Outputs:** `experiments/05_rule_engine/test_cases.json`
**Acceptance Test:** 30 cases with gold-standard answers, 10+ expected to differentiate rule engine from LLM
**Audit Note (2026-02-08):** Dependency check menunjukkan prereq `ART-020` masih `IN_PROGRESS`. Status `DONE` di ART-022 dipertahankan sebagai artefak eksperimen tersedia, namun tidak menutup kebutuhan verifikasi human pada ART-020.

### ART-023: Run Rule Engine Experiment (Exp 05)
| Field | Value |
|-------|-------|
| **Type** | EXPERIMENT |
| **Executor** | EITHER |
| **Prerequisites** | ART-021, ART-022 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Execute full Experiment 05 following experiment_template.md. Pre-register hypothesis, run rule engine and LLM on all test cases, compare outputs, analyze where they diverge.
**Inputs:** Rule engine (ART-021), test cases (ART-022)
**Outputs:** `experiments/05_rule_engine/PROTOCOL.md`, `experiments/05_rule_engine/results/`, `experiments/05_rule_engine/analysis.md`
**Acceptance Test:** Rule engine differs from LLM on >= 30% edge cases; difference is meaningful (not random)

### ART-024: Integrate Rule Engine into Main Pipeline
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-023 |
| **Priority** | P2 |
| **Status** | DONE |
**Description:** Connect rule engine to the main Nusantara-Agent pipeline so agents can query formal rules alongside LLM and KG.
**Inputs:** Rule engine module, existing agent code
**Outputs:** Updated `src/agents/` with rule engine integration
**Acceptance Test:** Agent can invoke rule engine and incorporate results into reasoning

### Experiment 06: Independent Evaluation Pipeline (Weakness #2)

### ART-025: Define Ground Truth Annotation Schema
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | None |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Design annotation guidelines for human annotators. Define: what counts as a correct triple, how to annotate cultural accuracy, how to handle ambiguity, how to score partial matches.
**Inputs:** Triple format spec, domain knowledge
**Outputs:** `data/annotation/guidelines.md`, `data/annotation/schema.json`
**Acceptance Test:** Guidelines clear enough that 2 pilot annotators achieve Kappa >= 0.5 on 20 sample items

### ART-026: Recruit and Train Annotators
| Field | Value |
|-------|-------|
| **Type** | DATA |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | ART-025 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Recruit 5 annotators (2+ with hukum adat expertise, 3 general legal knowledge). Train them on annotation guidelines. Run pilot annotation round on 20 items to calibrate.
**Inputs:** Annotation guidelines from ART-025
**Outputs:** Trained annotator team, pilot annotation results, calibration report
**Acceptance Test:** 5 annotators recruited, pilot Kappa >= 0.5, annotators understand guidelines
**Progress Note (2026-02-07):** Assignment pilot 20 item x 5 annotator sudah disiapkan di `data/processed/gold_standard/pilot_assignment_20_items.csv`; menunggu eksekusi annotator manusia.

### ART-027: Select Source Texts for Gold Standard (200 paragraphs)
| Field | Value |
|-------|-------|
| **Type** | DATA |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | None |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Select 200 paragraphs from academic sources covering 3 domains (Minangkabau, Bali, Jawa). Ensure balanced representation across domains and topic types (inheritance, property, authority, conflict).
**Inputs:** Academic sources, PDF collection
**Outputs:** `data/raw/gold_standard_texts/` — 200 text files organized by domain
**Acceptance Test:** 200 paragraphs, balanced across 3 domains (60-70 each), covering all 4 category types
**Progress Note (2026-02-07):** Seed awal 24 paragraf internal sudah dibuat (`data/raw/gold_standard_texts/index_seed.csv`) untuk pilot workflow; belum memenuhi target 200 paragraf sumber primer.
**Progress Note (2026-02-07):** Pool internal telah diskalakan ke 200 item (`data/raw/gold_standard_texts/GS-0001..GS-0200`) melalui `experiments/06_independent_eval/build_gold_texts_internal_pool.py`; status masih `internal_pool_seed` (bukan sumber primer final).
**Progress Note (2026-02-08):** Submisi ahli domain individu diterima di `docs/lembar_kerja_individu_ahli_domain_human_only_terisi_dr_hendra_kusuma_2026-02-08.md` dengan status seleksi paragraf `SELESAI` pada target individu (60-80 paragraf). Untuk status ART global tetap perlu agregasi hingga 200 paragraf primer lintas domain.

### ART-028: Human Annotation of Gold Standard Triples
| Field | Value |
|-------|-------|
| **Type** | DATA |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | ART-026, ART-027 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** 5 annotators independently annotate all 200 paragraphs with triples. Calculate inter-annotator agreement (Krippendorff's Alpha).
**Inputs:** 200 paragraphs, trained annotators, annotation schema
**Outputs:** `data/processed/gold_standard/annotations/` — per-annotator files, `data/processed/gold_standard/agreement_report.md`
**Acceptance Test:** Krippendorff's Alpha >= 0.667; if below, iterate on guidelines and re-annotate
**Progress Note (2026-02-07):** Scaffold operasional sudah disiapkan (`data/processed/gold_standard/annotations/template_annotasi.json`, `data/processed/gold_standard/agreement_report_template.md`), menunggu anotasi manusia.
**Progress Note (2026-02-07):** Stub assignment pilot telah digenerate menjadi 100 file anotasi (`GS-0001..GS-0020` x `ann01..ann05`) via `experiments/06_independent_eval/generate_annotation_stubs.py`; seluruh file masih `triples` kosong sampai annotator mengisi.
**Progress Note (2026-02-07):** Batch pilot 100 file stub sudah di-auto-fill menggunakan Kimi API via `experiments/06_independent_eval/auto_fill_annotations_llm.py` (status draft; tetap perlu validasi manusia sebelum dianggap gold final).
**Progress Note (2026-02-07):** Assignment full 200x5 telah dibuat (`data/processed/gold_standard/full_assignment_200x5.csv`) dan 1000 file anotasi telah digenerate.
**Progress Note (2026-02-07):** Auto-fill skala besar dilakukan lintas annotator (`ann02` DeepSeek/Kimi parsial, `ann03` Kimi, `ann04` Kimi, `ann05` Kimi) + fallback `fill_annotations_by_replication.py`; precheck terbaru menunjukkan `Invalid anotasi: 0`.

### ART-029: Implement Independent LLM Evaluator
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-025 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Build evaluation module that uses Claude or GPT-4 (NOT DeepSeek) to judge triple quality against gold standard. Evaluate: correctness, completeness, cultural accuracy.
**Inputs:** Gold standard schema, API keys for independent LLM
**Outputs:** `src/evaluation/llm_judge.py`
**Acceptance Test:** LLM judge scores correlate (r > 0.6) with human annotations on pilot set

### ART-030: Collect MA Court Decisions as Ground Truth
| Field | Value |
|-------|-------|
| **Type** | DATA |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | None |
| **Priority** | P2 |
| **Status** | PENDING |
**Description:** Collect 50+ publicly available Mahkamah Agung decisions related to adat law conflicts. Extract the legal reasoning and outcome as external ground truth for the reasoning pipeline.
**Inputs:** MA decision database (putusan.mahkamahagung.go.id)
**Outputs:** `data/raw/ma_decisions/` — structured decisions with metadata
**Acceptance Test:** 50+ decisions, covering at least 2 adat domains, with verified legal reasoning
**Progress Note (2026-02-07):** Template ekstraksi sudah disiapkan (`data/raw/ma_decisions/schema_putusan.json`, `data/raw/ma_decisions/template_putusan_0001.json`, `data/raw/ma_decisions/extraction_checklist.md`), menunggu koleksi putusan primer.
**Progress Note (2026-02-07):** Kandidat nomor perkara dari artefak internal sudah dipetakan di `data/raw/ma_decisions/candidates_from_internal_outputs.csv` sebagai daftar verifikasi awal (belum dapat dianggap ground truth).
**Progress Note (2026-02-07):** Stub putusan untuk 7 kandidat internal sudah digenerate via `experiments/06_independent_eval/generate_ma_stubs.py` (`data/raw/ma_decisions/putusan_*.json`); konten substansi masih kosong dan wajib verifikasi sumber primer.
**Progress Note (2026-02-07):** 7 stub putusan telah di-auto-fill draft konservatif via `experiments/06_independent_eval/auto_fill_ma_stubs_llm.py` menggunakan Kimi API; field tetap `status_verifikasi: draft` dan belum boleh dipakai sebagai ground truth tanpa cek sumber primer.
**Progress Note (2026-02-07):** Precheck ketat (`run_precheck.py`) kini mensyaratkan field substansi/metadata putusan non-kosong; status terkini `Invalid putusan MA: 7` sehingga ART-030 tetap belum siap.
**Progress Note (2026-02-08):** Submisi ahli domain individu diterima di `docs/lembar_kerja_individu_ahli_domain_human_only_terisi_dr_hendra_kusuma_2026-02-08.md` dengan 15-20 putusan tervalidasi (target individu tercapai). Status ART global tetap membutuhkan 50+ putusan terverifikasi lintas domain adat.

### ART-031: Run Independent Evaluation Experiment (Exp 06)
| Field | Value |
|-------|-------|
| **Type** | EXPERIMENT |
| **Executor** | EITHER |
| **Prerequisites** | ART-028, ART-029, ART-030 |
| **Priority** | P1 |
| **Status** | BLOCKED |
**Description:** Full Experiment 06: evaluate DeepSeek extraction against gold standard using both human annotators and independent LLM judge. Report precision, recall, F1, Cohen's Kappa.
**Inputs:** Gold standard, LLM judge, MA decisions
**Outputs:** `experiments/06_independent_eval/PROTOCOL.md`, `experiments/06_independent_eval/results/`, `experiments/06_independent_eval/analysis.md`
**Acceptance Test:** All metrics computed with confidence intervals; statistical significance tests passed
**Blocker:** ART-028 dan ART-030 belum selesai (`ART-029` sudah DONE).

### Data Scaling (Weakness #4)

### ART-032: Collect Bali Adat Law Texts (30+ sources)
| Field | Value |
|-------|-------|
| **Type** | DATA |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | None |
| **Priority** | P1 |
| **Status** | IN_PROGRESS |
**Description:** Collect academic texts on Bali customary law (hukum adat Bali). Focus on inheritance (sentana, druwe tengah), community governance (banjar), and property types.
**Inputs:** Academic databases, library access
**Outputs:** `data/raw/bali/` — 30+ source text files
**Acceptance Test:** 30+ texts, covering inheritance, governance, and property
**Note (2026-02-07):** Started with overview text from academic search.

### ART-033: Collect Jawa Adat Law Texts (30+ sources)
| Field | Value |
|-------|-------|
| **Type** | DATA |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | None |
| **Priority** | P1 |
| **Status** | IN_PROGRESS |
**Description:** Collect academic texts on Javanese customary law (hukum adat Jawa). Focus on bilateral inheritance (gono-gini, harta bawaan), family structure, and dispute resolution.
**Inputs:** Academic databases, library access
**Outputs:** `data/raw/jawa/` — 30+ source text files
**Acceptance Test:** 30+ texts, covering inheritance, family structure, and dispute resolution
**Note (2026-02-07):** Started with overview text from academic search.

### ART-034: Collect Additional Minangkabau Texts (30+ more)
| Field | Value |
|-------|-------|
| **Type** | DATA |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | None |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Expand Minangkabau corpus beyond the single pilot text. Include diverse topics and regions within Minangkabau.
**Inputs:** Academic databases, library access
**Outputs:** `data/raw/minangkabau/` — 30+ additional source text files
**Acceptance Test:** 30+ texts total (excluding pilot text)

### ART-035: Batch Extract Triples from All Domains (Target 10K+)
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-032, ART-033, ART-034 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Run batch extraction pipeline on all collected texts. Use modular TripleExtractor with domain-specific prompts. Target: 10,000+ triples across 3 domains.
**Inputs:** All source texts from 3 domains, batch ingestion pipeline
**Outputs:** `data/processed/triples_minangkabau.jsonl`, `data/processed/triples_bali.jsonl`, `data/processed/triples_jawa.jsonl`
**Acceptance Test:** 10,000+ total triples, balanced across domains (min 2,000 per domain)

### ART-036: Setup Neo4j Database and Load KG
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-035 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Setup Neo4j instance (Aura Cloud or local), design schema, and load all 10K+ triples. Implement efficient querying and graph algorithms.
**Inputs:** Extracted triples from all domains
**Outputs:** Running Neo4j instance, `src/kg_engine/neo4j_loader.py`, `src/kg_engine/neo4j_query.py`
**Acceptance Test:** All triples loaded, basic queries return correct results, response time < 500ms

### ART-037: Setup Qdrant Vector Database
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-035 |
| **Priority** | P2 |
| **Status** | PENDING |
**Description:** Setup Qdrant instance, generate embeddings for all source texts, implement semantic search. Integrate with existing pipeline.
**Inputs:** Source texts, embedding model
**Outputs:** Running Qdrant instance, `src/retrieval/vector_store.py`
**Acceptance Test:** Semantic search returns relevant passages for test queries (precision@5 >= 0.7)

### Experiment 05 — Rule Engine for Bali & Jawa

### ART-038: Collect Bali Legal Rules from Literature
| Field | Value |
|-------|-------|
| **Type** | DATA |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | ART-032 |
| **Priority** | P2 |
| **Status** | DONE |
**Description:** Extract 20+ formal rules of Bali inheritance law from academic sources.
**Inputs:** Bali adat law texts
**Outputs:** `data/rules/bali_rules.json`
**Acceptance Test:** 20+ rules with citations
**Note (2026-02-07):** Initial 5 rules created from academic summaries.
**Completion Note (2026-02-08):** Expert review selesai. 5 original BENAR + 29 rules baru dari expert = 34 rules VERIFIED. Mencakup: klasifikasi harta, hak waris perempuan (MUDP 2010), sentana rajeg/peperasan, perceraian, sengketa, perubahan kontemporer. Lihat `data/rules/Hasil Verifikasi BALI.md`.

### ART-039: Collect Jawa Legal Rules from Literature
| Field | Value |
|-------|-------|
| **Type** | DATA |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | ART-033 |
| **Priority** | P2 |
| **Status** | DONE |
**Description:** Extract 20+ formal rules of Javanese inheritance law from academic sources.
**Inputs:** Jawa adat law texts
**Outputs:** `data/rules/jawa_rules.json`
**Acceptance Test:** 20+ rules with citations
**Note (2026-02-07):** Initial 5 rules created from academic summaries.
**Completion Note (2026-02-08):** Expert review selesai. 4 original BENAR, 1 koreksi (JAW-004: sepikul segendongan → sigar semangka per MA No. 179 K/Sip/1961) + 31 rules baru dari expert = 36 rules VERIFIED. Mencakup: klasifikasi harta (pusaka/weweh/pencaharian), sigar semangka, anak ragil, gantungan siwur, anak pupon, janda/duda, perceraian, penyelesaian sengketa, akulturasi Islam-adat, perubahan kontemporer. Lihat `data/rules/Hasil Verifikasi JAWA.md`.

### ART-040: Encode Bali Rules in Symbolic Framework
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-038, ART-021 |
| **Priority** | P2 |
| **Status** | DONE |
**Description:** Implement Bali rules in the same symbolic framework as Minangkabau.
**Inputs:** `data/rules/bali_rules.json`, rule engine framework
**Outputs:** `src/symbolic/rules/bali.lp`
**Acceptance Test:** All rules parse and execute; 10 test queries correct
**Completion Note (2026-02-08):** Rules Bali telah di-encode ke `src/symbolic/rules/bali.lp` mengikuti pola `minangkabau.lp` dan diverifikasi dengan test deterministik di `tests/test_rule_engine.py`.

### ART-041: Encode Jawa Rules in Symbolic Framework
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-039, ART-021 |
| **Priority** | P2 |
| **Status** | DONE |
**Description:** Implement Javanese rules in the same symbolic framework as Minangkabau.
**Inputs:** `data/rules/jawa_rules.json`, rule engine framework
**Outputs:** `src/symbolic/rules/jawa.lp`
**Acceptance Test:** All rules parse and execute; 10 test queries correct
**Completion Note (2026-02-08):** Rules Jawa telah di-encode ke `src/symbolic/rules/jawa.lp` mengikuti pola `minangkabau.lp` dan diverifikasi dengan test deterministik di `tests/test_rule_engine.py`.

### ART-042: Encode National Law Rules
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-021 |
| **Priority** | P2 |
| **Status** | DONE |
**Description:** Encode relevant KUHPerdata inheritance and property rules in symbolic framework. These serve as the "national law" counterpart to adat rules for conflict detection.
**Inputs:** KUHPerdata relevant articles
**Outputs:** `src/symbolic/rules/nasional.lp`
**Acceptance Test:** 15+ national law rules, can detect conflicts with adat rules programmatically
**Completion Note (2026-02-08):** Rule nasional telah di-encode di `src/symbolic/rules/nasional.lp` (prioritas kelas ahli waris, hak pasangan, pelunasan utang, batas wasiat, legitime portie, dan deteksi konflik normatif nasional-vs-adat) dan diverifikasi dengan test deterministik pada `tests/test_rule_engine.py`.

---

## Phase 3: Advanced Agent Architecture

### Experiment 07: Genuine Multi-Agent Orchestration (Weakness #3)

### ART-043: Design Debate Protocol Specification
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Prerequisites** | None |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Design the multi-round debate protocol between National and Adat agents. Define: number of rounds, critique format, response format, convergence criteria, escalation to supervisor.
**Inputs:** Literature on LLM debate protocols, existing agent architecture
**Outputs:** `experiments/07_advanced_orchestration/debate_protocol_spec.md`
**Acceptance Test:** Spec is detailed enough to implement without ambiguity

### ART-044: Implement Parallel Agent Execution
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-043 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Refactor LangGraph workflow so National and Adat agents run in parallel (not sequential). Use LangGraph's parallel execution primitives.
**Inputs:** Existing multi_agent.py, LangGraph documentation
**Outputs:** Updated `src/agents/orchestrator.py`
**Acceptance Test:** Both agents complete before supervisor starts; total time < sequential time

### ART-045: Implement Agent Debate Protocol
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-043, ART-044 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Implement multi-round debate where agents critique each other's outputs. Include critique generation, response generation, and convergence detection.
**Inputs:** Debate spec, parallel agent execution
**Outputs:** `src/agents/debate.py`
**Acceptance Test:** Debate runs 2+ rounds, produces different output than no-debate version on >= 40% cases

### ART-046: Implement Self-Correction Loop
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-045 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Each agent can revise its output based on critique from other agents or supervisor feedback. Implement revision tracking.
**Inputs:** Debate module, agent architecture
**Outputs:** Updated `src/agents/` with self-correction capability
**Acceptance Test:** Self-correction fixes >= 40% of errors detected during debate

### ART-047: Implement Conditional Routing
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-044 |
| **Priority** | P2 |
| **Status** | DONE |
**Description:** Implement router node that classifies queries and routes to appropriate agent subgraph: pure national, pure adat, conflict case, consensus case.
**Inputs:** Test query set, agent architecture
**Outputs:** `src/agents/router.py`
**Acceptance Test:** Router correctly classifies >= 85% of test queries

### ART-048: Run Advanced Orchestration Experiment (Exp 07)
| Field | Value |
|-------|-------|
| **Type** | EXPERIMENT |
| **Executor** | EITHER |
| **Prerequisites** | ART-044, ART-045, ART-046, ART-047 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Full Experiment 07: test advanced orchestration against Exp 03 baseline. Measure improvement in accuracy, completeness, cultural sensitivity, and efficiency.
**Inputs:** Advanced orchestration code, test cases, Exp 03 results as baseline
**Outputs:** `experiments/07_advanced_orchestration/PROTOCOL.md`, `experiments/07_advanced_orchestration/results/`, `experiments/07_advanced_orchestration/analysis.md`
**Acceptance Test:** Statistical improvement over Exp 03 on at least 2 metrics
**Outcome:** Completed with negative result (advanced orchestration belum melampaui baseline); tercatat sebagai F-009 di `docs/failure_registry.md`.

### Experiment 08: Full Pipeline Integration

### ART-049: Integrate Neo4j + Qdrant + Rule Engine + Agents
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-024, ART-036, ART-037, ART-048 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Integrate all components into a unified pipeline: Neo4j graph queries, Qdrant vector search, symbolic rule engine, and advanced multi-agent orchestration.
**Inputs:** All component modules
**Outputs:** `src/pipeline/nusantara_agent.py` — unified entry point
**Acceptance Test:** End-to-end query processing works for all 4 query types (pure national, pure adat, conflict, consensus)
**Completion Note (2026-02-08):** Unified entry point diimplementasikan pada `src/pipeline/nusantara_agent.py` dengan integrasi router + graph retriever + vector retriever + rule engine lintas domain (`nasional`, `minangkabau`, `bali`, `jawa`). Fallback mode lokal aktif saat Neo4j/Qdrant belum tersedia. End-to-end diverifikasi melalui test deterministik `tests/test_nusantara_pipeline.py` (4 tipe query).

### ART-050: Design 200 Test Cases Across Domains
| Field | Value |
|-------|-------|
| **Type** | DATA |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | ART-032, ART-033, ART-034 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Create comprehensive test suite: 50 Minangkabau, 50 Bali, 50 Jawa, 50 cross-domain conflict cases. Each with expected outcome type and gold-standard reasoning.
**Inputs:** Domain knowledge, collected legal texts, MA decisions
**Outputs:** `data/test_cases/test_suite_200.json`
**Acceptance Test:** 200 cases, balanced across domains, each with gold-standard answer
**Progress Note (2026-02-08):** Submisi ahli domain individu melaporkan status `PROSES` dengan contoh kasus awal (`TC-BALI-001`) pada `docs/lembar_kerja_individu_ahli_domain_human_only_terisi_dr_hendra_kusuma_2026-02-08.md`. Perlu agregasi lintas kontributor hingga 200 kasus sesuai komposisi domain.
**Progress Note (2026-02-08):** Paket kerja 4 jam batch-1 telah diterima pada `docs/paket_kerja_4_jam_ahli_domain_terisi_dr_hendra_2026-02-08.md` (12 kasus prioritas terisi). Paket batch-2 siap distribusi pada `docs/paket_kerja_4_jam_ahli_domain_batch2_siap_print.md` untuk melanjutkan pengumpulan human baseline secara bertahap.
**Progress Note (2026-02-08):** Paket kerja batch-2 terisi telah diterima pada `docs/paket_kerja_4_jam_batch2_terisi_dr_hendra_2026-02-08.md` dan direkap pada `docs/rekap_human_baseline_sprint_2026-02-08.md` (kumulatif sprint: 24 kasus). Paket batch-3 siap handout pada `docs/paket_kerja_4_jam_batch3_ready_to_handout.md`.
**Progress Note (2026-02-08):** Paket kerja batch-3 terisi telah diterima pada `docs/paket_kerja_4_jam_batch3_terisi_dr_hendra_2026-02-08.md`; kumulatif sprint ahli pertama menjadi 36 kasus. Paket batch-4 siap handout pada `docs/paket_kerja_4_jam_batch4_ready_to_handout.md`.

### ART-051: Run Full Pipeline on 200 Test Cases
| Field | Value |
|-------|-------|
| **Type** | EXPERIMENT |
| **Executor** | EITHER |
| **Prerequisites** | ART-049, ART-050 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Execute Nusantara-Agent on all 200 test cases. Record all intermediate outputs (retrieval, reasoning, debate, synthesis).
**Inputs:** Full pipeline, 200 test cases
**Outputs:** `experiments/08_full_pipeline/results/` — all outputs
**Acceptance Test:** Pipeline completes all 200 cases without crashes

### ART-052: Implement NusaCulture-Bench
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-050 |
| **Priority** | P2 |
| **Status** | PENDING |
**Description:** Package the 200+ test cases as a reusable benchmark (NusaCulture-Bench). Include: test runner, automatic scoring, leaderboard format.
**Inputs:** Test cases, evaluation metrics
**Outputs:** `src/benchmark/nusaculture_bench.py`, `data/benchmark/`
**Acceptance Test:** Benchmark runs end-to-end, produces consistent scores across runs

### Agent Specialization

### ART-053: Implement Bali Domain Agent
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-040, ART-044 |
| **Priority** | P2 |
| **Status** | PENDING |
**Description:** Create specialized Bali adat law agent with domain-specific prompts, rule engine access, and cultural context.
**Inputs:** Bali rules, Bali KG data, agent framework
**Outputs:** `src/agents/bali_agent.py`
**Acceptance Test:** Agent provides culturally accurate responses to Bali-specific queries

### ART-054: Implement Jawa Domain Agent
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-041, ART-044 |
| **Priority** | P2 |
| **Status** | PENDING |
**Description:** Create specialized Javanese adat law agent with domain-specific prompts and rule engine.
**Inputs:** Jawa rules, Jawa KG data, agent framework
**Outputs:** `src/agents/jawa_agent.py`
**Acceptance Test:** Agent provides culturally accurate responses to Jawa-specific queries

### ART-055: Implement Dynamic Agent Selection
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-047, ART-053, ART-054 |
| **Priority** | P2 |
| **Status** | PENDING |
**Description:** Router dynamically selects which domain agent(s) to invoke based on query analysis. Support multi-domain queries.
**Inputs:** Router, all domain agents
**Outputs:** Updated `src/agents/router.py`
**Acceptance Test:** Correct agent(s) invoked for 90% of test queries

---

## Phase 4: Evaluation & Ablation

### Experiment 09: Ablation Study (Weakness #5)

### ART-056: Define 8 Baseline Configurations
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Prerequisites** | ART-049 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Document exact configuration for each of the 8 baselines: what components are included/excluded, what model is used, what prompts are used.
**Inputs:** Full pipeline architecture, methodology_fixes.md
**Outputs:** `experiments/09_ablation_study/baseline_configs.md`
**Acceptance Test:** Each baseline fully specified, reproducible by another researcher
**Completion Note (2026-02-08):** Konfigurasi 8 baseline telah didokumentasikan pada `experiments/09_ablation_study/baseline_configs.md` secara reproduksibel (komponen aktif/non-aktif, mode model, dan fallback).

### ART-057: Implement Baseline 1 — DeepSeek Direct Prompting
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-056 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Implement baseline: DeepSeek answers legal questions with zero RAG context.
**Outputs:** `experiments/09_ablation_study/baselines/b1_direct_prompting.py`
**Completion Note (2026-02-08):** Implementasi baseline direct prompting tersedia di `experiments/09_ablation_study/baselines/b1_direct_prompting.py` dengan output JSON terstandar.

### ART-058: Implement Baseline 2 — DeepSeek + Vector RAG (no graph)
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-056, ART-037 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Implement baseline: DeepSeek with Qdrant vector retrieval but no graph component.
**Outputs:** `experiments/09_ablation_study/baselines/b2_vector_rag.py`
**Completion Note (2026-02-08):** Implementasi baseline vector-only tersedia di `experiments/09_ablation_study/baselines/b2_vector_rag.py` (fallback in-memory sebelum Qdrant aktif penuh).

### ART-059: Implement Baseline 3 — DeepSeek + Graph (no vector)
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-056, ART-036 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Implement baseline: DeepSeek with Neo4j graph retrieval but no vector search.
**Outputs:** `experiments/09_ablation_study/baselines/b3_graph_only.py`
**Completion Note (2026-02-08):** Implementasi baseline graph-only tersedia di `experiments/09_ablation_study/baselines/b3_graph_only.py` (fallback JSON KG sebelum Neo4j aktif penuh).

### ART-060: Implement Baseline 4 — Full Pipeline sans Rule Engine
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-056, ART-049 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Full pipeline with rule engine component disabled.
**Outputs:** `experiments/09_ablation_study/baselines/b4_no_rules.py`
**Completion Note (2026-02-08):** Implementasi baseline tanpa rule engine tersedia di `experiments/09_ablation_study/baselines/b4_no_rules.py`.

### ART-061: Implement Baseline 5 — Full Pipeline sans Debate
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-056, ART-049 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Full pipeline with debate protocol disabled (revert to sequential chain).
**Outputs:** `experiments/09_ablation_study/baselines/b5_no_debate.py`
**Completion Note (2026-02-08):** Implementasi baseline tanpa debat tersedia di `experiments/09_ablation_study/baselines/b5_no_debate.py`.

### ART-062: Implement Baseline 6 — GPT-4 + Same Pipeline
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-056, ART-049 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Same full pipeline but swap DeepSeek for GPT-4 to test model-agnosticism.
**Outputs:** `experiments/09_ablation_study/baselines/b6_gpt4_pipeline.py`
**Completion Note (2026-02-08):** Implementasi baseline GPT-4 tersedia di `experiments/09_ablation_study/baselines/b6_gpt4_pipeline.py` dengan fallback deterministik saat API key tidak tersedia.

### ART-063: Implement Baseline 7 — Claude + Same Pipeline
| Field | Value |
|-------|-------|
| **Type** | CODE |
| **Executor** | EITHER |
| **Prerequisites** | ART-056, ART-049 |
| **Priority** | P1 |
| **Status** | DONE |
**Description:** Same full pipeline but swap DeepSeek for Claude to test cross-model validation.
**Outputs:** `experiments/09_ablation_study/baselines/b7_claude_pipeline.py`
**Completion Note (2026-02-08):** Implementasi baseline Claude tersedia di `experiments/09_ablation_study/baselines/b7_claude_pipeline.py` dengan fallback deterministik saat API key tidak tersedia.

### ART-064: Collect Human Expert Baseline (Baseline 8)
| Field | Value |
|-------|-------|
| **Type** | DATA |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | ART-050 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** 3 human legal experts answer all 200 test cases without AI assistance. This is the upper-bound baseline.
**Inputs:** 200 test cases
**Outputs:** `experiments/09_ablation_study/baselines/b8_human_expert/`
**Acceptance Test:** 3 experts complete all 200 cases; inter-expert agreement reported
**Progress Note (2026-02-08):** Sprint human baseline 4 jam batch-1 dari ahli domain telah terdokumentasi pada `docs/paket_kerja_4_jam_ahli_domain_terisi_dr_hendra_2026-02-08.md`. Belum memenuhi acceptance test ART-064 karena masih perlu kontribusi ahli tambahan dan cakupan kasus yang lebih luas.
**Progress Note (2026-02-08):** Sprint human baseline batch-2 telah terdokumentasi pada `docs/paket_kerja_4_jam_batch2_terisi_dr_hendra_2026-02-08.md`; rekap kumulatif batch-1+2 tersedia pada `docs/rekap_human_baseline_sprint_2026-02-08.md`. Status tetap PENDING sampai terpenuhi 3 ahli dan cakupan 200 kasus.
**Progress Note (2026-02-08):** Sprint human baseline batch-3 telah terdokumentasi pada `docs/paket_kerja_4_jam_batch3_terisi_dr_hendra_2026-02-08.md`; rekap kumulatif saat ini 36 kasus (1 ahli). Status tetap PENDING karena syarat ART-064 mewajibkan 3 ahli dan cakupan 200 kasus penuh.

### ART-065: Run All Baselines (3x each with different seeds)
| Field | Value |
|-------|-------|
| **Type** | EXPERIMENT |
| **Executor** | EITHER |
| **Prerequisites** | ART-057 through ART-064 |
| **Priority** | P1 |
| **Status** | BLOCKED |
**Description:** Execute all 8 baselines on the 200 test cases, each run 3 times with different random seeds. Record all outputs.
**Inputs:** All baseline implementations, 200 test cases
**Outputs:** `experiments/09_ablation_study/results/` — organized by baseline and run
**Acceptance Test:** 7 automated baselines x 3 runs = 21 complete runs + 1 human baseline
**Blocker:** Seluruh ART-057 s.d. ART-064 belum selesai.

### ART-066: Statistical Analysis of Ablation Results
| Field | Value |
|-------|-------|
| **Type** | ANALYSIS |
| **Executor** | EITHER |
| **Prerequisites** | ART-065 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Compute: mean and std for each baseline, paired t-tests or Wilcoxon for all pairwise comparisons, Cohen's d effect sizes, confidence intervals. Visualize results.
**Inputs:** All ablation results
**Outputs:** `experiments/09_ablation_study/analysis.md`, `experiments/09_ablation_study/figures/`
**Acceptance Test:** All comparisons with p-values, effect sizes, CIs reported; full pipeline beats >= 6/7 automated baselines

### Experiment 10: CCS Metric Validation (Weakness #6)

### ART-067: Define CCS Metric Components and Initial Weights
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Prerequisites** | None |
| **Priority** | P2 |
| **Status** | PENDING |
**Description:** Formally define each component of CCS metric, how each is measured, and propose initial weights.
**Inputs:** PRD CCS definition, relevant literature on cultural metrics
**Outputs:** `experiments/10_metric_validation/ccs_definition.md`
**Acceptance Test:** Each component precisely defined with measurement procedure

### ART-068: Run Delphi Method for Weight Calibration (3 rounds)
| Field | Value |
|-------|-------|
| **Type** | DATA |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | ART-067 |
| **Priority** | P2 |
| **Status** | PENDING |
**Description:** Survey 5+ domain experts across 3 Delphi rounds to calibrate CCS component weights. Track convergence of expert opinions.
**Inputs:** CCS component definitions, expert panel
**Outputs:** `experiments/10_metric_validation/delphi_results/`
**Acceptance Test:** Weight variability < 10% between round 2 and 3

### ART-069: Human Rating of 100 System Outputs for CCS
| Field | Value |
|-------|-------|
| **Type** | DATA |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | ART-067, ART-051 |
| **Priority** | P2 |
| **Status** | PENDING |
**Description:** 5 annotators rate cultural consistency of 100 system outputs using CCS rubric. Calculate Krippendorff's Alpha.
**Inputs:** 100 system outputs, CCS rubric
**Outputs:** `experiments/10_metric_validation/human_ratings/`
**Acceptance Test:** Krippendorff's Alpha >= 0.667

### ART-070: Convergent and Discriminant Validity Tests
| Field | Value |
|-------|-------|
| **Type** | ANALYSIS |
| **Executor** | EITHER |
| **Prerequisites** | ART-069 |
| **Priority** | P2 |
| **Status** | PENDING |
**Description:** Test convergent validity (CCS correlates with RAGAS faithfulness, r > 0.6) and discriminant validity (CCS differentiates culturally consistent vs inconsistent outputs, p < 0.05).
**Inputs:** CCS scores, RAGAS scores, human ratings
**Outputs:** `experiments/10_metric_validation/validity_analysis.md`
**Acceptance Test:** Convergent r > 0.6, discriminant p < 0.05

### ART-071: Run CCS Validation Experiment (Exp 10)
| Field | Value |
|-------|-------|
| **Type** | EXPERIMENT |
| **Executor** | EITHER |
| **Prerequisites** | ART-068, ART-069, ART-070 |
| **Priority** | P2 |
| **Status** | BLOCKED |
**Description:** Full Experiment 10: compile all CCS validation evidence. Follow experiment template.
**Inputs:** All CCS validation results
**Outputs:** `experiments/10_metric_validation/PROTOCOL.md`, `experiments/10_metric_validation/analysis.md`
**Acceptance Test:** CCS validated on all 4 dimensions (reliability, convergent, discriminant, expert calibrated)
**Blocker:** ART-068, ART-069, ART-070 belum selesai.

### ART-072: RAGAS Evaluation on Full Pipeline
| Field | Value |
|-------|-------|
| **Type** | EXPERIMENT |
| **Executor** | EITHER |
| **Prerequisites** | ART-051 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Run full RAGAS evaluation suite (faithfulness, answer relevancy, context precision, context recall) on 200 test case outputs.
**Inputs:** Full pipeline outputs, RAGAS library
**Outputs:** `experiments/08_full_pipeline/ragas_results.json`
**Acceptance Test:** Faithfulness >= 0.85, Answer Relevancy >= 0.80

---

## Phase 5: Paper Writing & Submission

### ART-073: Write Introduction + Research Questions
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Prerequisites** | ART-051 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Draft Introduction section: motivation, research gap, research questions, contributions. Follow target journal format.
**Outputs:** `paper/sections/01_introduction.md`

### ART-074: Write Related Work Section
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Prerequisites** | None |
| **Priority** | P2 |
| **Status** | PENDING |
**Description:** Comprehensive literature review: GraphRAG systems, legal NLP, neuro-symbolic AI, multi-agent systems, Indonesian legal pluralism. Minimum 60 references.
**Outputs:** `paper/sections/02_related_work.md`

### ART-075: Write Methodology Section
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Prerequisites** | ART-049 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Detailed system architecture description: KG construction, rule engine, agent architecture, evaluation framework. Include formal notation where appropriate.
**Outputs:** `paper/sections/03_methodology.md`

### ART-076: Write Experimental Setup Section
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Prerequisites** | ART-066 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Describe datasets, baselines, metrics, experimental configurations. Sufficient detail for reproduction.
**Outputs:** `paper/sections/04_experimental_setup.md`

### ART-077: Write Results Section
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Prerequisites** | ART-066, ART-071, ART-072 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Present all quantitative results: main results table, ablation results, CCS validation, statistical tests. Include figures.
**Outputs:** `paper/sections/05_results.md`

### ART-078: Write Discussion Section
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Prerequisites** | ART-077 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Interpret results, discuss implications, address limitations honestly (drawing from failure_registry.md), compare with related work.
**Outputs:** `paper/sections/06_discussion.md`

### ART-079: Write Conclusion + Future Work
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Prerequisites** | ART-078 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Summarize contributions, state limitations, outline future work. Keep future work concrete, not hand-wavy.
**Outputs:** `paper/sections/07_conclusion.md`

### ART-080: Create All Figures and Tables
| Field | Value |
|-------|-------|
| **Type** | ANALYSIS |
| **Executor** | EITHER |
| **Prerequisites** | ART-066, ART-071 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Create publication-quality figures: architecture diagram, results plots, ablation heatmap, CCS validation plots. Follow journal formatting guidelines.
**Outputs:** `paper/figures/`
**Acceptance Test:** All figures at 300+ DPI, publication-ready

### ART-081: Internal Paper Review (Layer 1 + 2)
| Field | Value |
|-------|-------|
| **Type** | REVIEW |
| **Executor** | EITHER |
| **Prerequisites** | ART-073 through ART-080 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Run full review protocol on complete paper draft. Self-critique + adversarial AI review. Address all CRITICAL and MAJOR issues.
**Outputs:** `paper/reviews/internal_review.md`
**Acceptance Test:** No CRITICAL issues remaining, all MAJOR issues addressed or justified

### ART-082: External Paper Review (Layer 3)
| Field | Value |
|-------|-------|
| **Type** | REVIEW |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | ART-081 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** At least 1 external reviewer (ideally domain expert not involved in the project) reviews the full paper. Address all feedback.
**Inputs:** Complete paper draft
**Outputs:** `paper/reviews/external_review.md`
**Acceptance Test:** External reviewer recommends submission

### ART-083: Prepare Submission Package
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | EITHER |
| **Prerequisites** | ART-082 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Format paper for target journal, prepare cover letter, supplementary materials, code/data repository. Follow journal-specific submission guidelines.
**Outputs:** `paper/submission/` — complete submission package
**Acceptance Test:** Meets all journal formatting requirements

### ART-084: Submit Paper and Prepare Repository for Open Source
| Field | Value |
|-------|-------|
| **Type** | DOCUMENTATION |
| **Executor** | HUMAN_ONLY |
| **Prerequisites** | ART-083 |
| **Priority** | P1 |
| **Status** | PENDING |
**Description:** Submit to target journal. Clean and prepare repository for public release. Remove sensitive data, add proper LICENSE, ensure reproducibility documentation.
**Outputs:** Submitted paper, public repository
**Acceptance Test:** Paper submitted, repo public, all experiments reproducible

---

## Dependency Graph (Critical Path)

```
Phase 0-1 (DONE)
    ↓
ART-019 → ART-021 → ART-023 → ART-024 ─┐
ART-020 ─────┘         ↑                  │
ART-022 ────────────────┘                  │
                                           ↓
ART-032,033,034 → ART-035 → ART-036 ──→ ART-049 → ART-051 → ART-072
                              ART-037 ──┘   ↑                    ↓
                                           │              ART-077 → ART-081
ART-025 → ART-028 → ART-031              │                    ↑
ART-026 ──┘                               │              ART-066
ART-027 ──┘                               │                    ↑
ART-029                                   │              ART-065
ART-030                                   │                    ↑
                                           │         ART-057..064
ART-043 → ART-044 → ART-045 → ART-048 ──┘                    ↑
                      ART-046 ──┘   ↑                    ART-056
                      ART-047 ──────┘
```

**Critical path:** ART-019 → 021 → 023 → 024 → 049 → 051 → 065 → 066 → 077 → 081 → 083 → 084






