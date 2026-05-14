# Nusantara-Agent (Research Repository)

**Neuro-Symbolic Legal Reasoning with Expert-Verified Customary Law Rules**

> **Note:** This is a scientific research repository (not a commercial product), targeting publication in Scopus Q1 journals, primarily *Knowledge-Based Systems* or *Expert Systems with Applications*.

## Research Focus (Post-Pivot 2026-02-12)
1. **Knowledge Base:** 95 customary law rules (Minangkabau, Bali, Javanese) verified by domain experts.
2. **Formal Reasoning:** Encoding rules into ASP (Clingo) to detect norm conflicts between national and customary law.
3. **Empirical Evaluation:** Comparing LLM+Rules vs. LLM-only on expert-labelled cases with defensible statistical reporting.

## Research Philosophy
- **Simple is better:** Only components that directly contribute to the paper's claims are retained.
- **Fail fast, pivot early:** Negative results are documented as scientific contributions.
- **Rigorous standards:** All claims must be evidence-based and reproducible.

## Current Status (as of 2026-02-24)
- `ClingoRuleEngine` active in `src/symbolic/rule_engine.py` with 95 rules across 4 domains (`minangkabau`, `bali`, `jawa`, `nasional`).
- Active benchmark: 74 cases (70 evaluable + 4 `DISPUTED` excluded from accuracy score).
- Benchmark manifest strict-check passes (`python scripts/validate_benchmark_manifest.py --require-reference-match` → `errors=0`, `warns=0`).
- Multi-agent debate/self-correction documented as negative results (F-009) and **not** the primary paper direction.
- Deterministic test suite passes `118/118` (`python scripts/run_test_suite.py`).
- Benchmark runner uses a centralised split contract (`full/dev/locked_test`) with equivalent gate modes (`scientific_claimable` vs `operational_offline`).
- Default workflow is offline-first; paid API calls only when required and authorised.

## Priority Milestones
1. Adjudication of 10 `DISPUTED` cases by qualified raters.
2. Benchmark expansion to 100+ labelled cases.
3. Re-run LLM+Rules vs. LLM-only comparison in a controlled environment.
4. Statistical testing (McNemar + 95% CI) and at least one non-DeepSeek comparison model.

## Directory Structure
- `data/`: Raw and processed data artefacts (gold standard, benchmark, manifest).
- `src/`: Main pipeline code, rule engine, router, orchestrator.
- `experiments/`: Isolated experiments with result artefacts.
- `docs/`: Methodology documents, gate reviews, task/failure registry, handoffs.
- `tests/`: Deterministic unit tests.

## Getting Started
1. **Set up environment**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configuration**
   - Copy `.env.example` to `.env`.
   - Fill in required credentials (e.g. `DEEPSEEK_API_KEY`) if running in online mode.

## Active Tech Stack
- **Symbolic Reasoning:** Clingo (ASP — Answer Set Programming)
- **LLM Integration:** DeepSeek API (optional, controlled usage)
- **Orchestration:** LangGraph + offline fallback
- **Retrieval:** Local JSON / keyword fallback

> Scope note: Neo4j / Qdrant / GraphRAG and CCS metrics are out of scope for the post-pivot paper.

## Domain Terminology
Key Indonesian customary law terms used throughout the codebase are intentionally left untranslated, as they refer to culturally specific legal concepts with no direct English equivalents:

| Term | Domain | Meaning |
|------|--------|---------|
| *pusako tinggi* | Minangkabau | High ancestral property (matrilineally inherited, inalienable) |
| *pusako rendah* | Minangkabau | Low ancestral property (individually acquired, inheritable by children) |
| *kemenakan* | Minangkabau | Matrilineal nephew/niece (primary customary heir) |
| *mamak* | Minangkabau | Maternal uncle (guardian of matrilineal assets) |
| *gono-gini* | Javanese | Marital joint property |
| *harta asal* | Javanese | Pre-marital property |
| *purusa* | Balinese | Patrilineal heir status |
| *sentana rajeg* | Balinese | Appointed female heir in absence of male heirs |
| *druwe tengah* | Balinese | Sacred communal property (not alienable) |
