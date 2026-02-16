# Focused Paper Roadmap
**Tanggal:** 2026-02-12
**Target Journal:** Knowledge-Based Systems atau Expert Systems with Applications (Q1)
**Timeline:** 6-8 minggu dari sekarang

---

## Paper Title (Draft)

**"Formal Customary Law Rules as Symbolic Anchors for LLM-based Legal Reasoning: Evidence from Indonesian Legal Pluralism"**

Alternatif:
- "Neuro-Symbolic Legal Reasoning with Expert-Verified Customary Law Rules"
- "ASP-based Symbolic Anchoring for LLM Reasoning in Pluralistic Legal Systems"

---

## Paper Story (1 paragraf)

Indonesia's pluralistic legal system — where national civil code, Islamic law, and diverse customary laws (adat) coexist — presents unique challenges for automated legal reasoning. We show that encoding expert-verified customary law rules as Answer Set Programs (ASP) and using their outputs as "symbolic anchors" for LLM-based reasoning significantly improves classification accuracy on pluralistic legal cases across three Indonesian adat domains (Minangkabau, Bali, Jawa). Our 95 formally encoded rules — verified by domain experts — enable automated detection of norm conflicts between national and customary law, something LLMs alone frequently miss or hallucinate. We contribute: (1) the first formally encoded and expert-verified Indonesian customary law rule base covering three distinct legal traditions, (2) empirical evidence that symbolic anchoring reduces LLM errors on conflict-detection tasks, and (3) an expert-annotated benchmark dataset for evaluating pluralistic legal reasoning systems.

---

## Paper Structure

### 1. Introduction (~1.5 pages)
- Problem: Pluralistic legal systems are hard for LLMs
- Gap: No formalized customary law knowledge bases; LLMs hallucinate norm conflicts
- Contribution: Expert-verified ASP rules + symbolic anchoring improves LLM reasoning

### 2. Related Work (~2 pages)
- Neuro-symbolic AI for legal reasoning
- LLM-based legal NLP (including limitations on non-Western legal systems)
- Answer Set Programming in knowledge representation
- Indonesian legal pluralism (brief legal background)

### 3. Methodology (~3 pages)
#### 3.1 Rule Base Construction
- Source: Academic literature on 3 adat domains
- Expert verification process (3 experts, verification protocol)
- ASP encoding (syntax, design decisions, examples)
- Rule coverage: 95 rules across property, inheritance, authority, conflict

#### 3.2 Symbolic Anchoring Pipeline
- Architecture: Query → Router → Fact Extraction → ASP Solver → LLM Agent
- How ASP output anchors LLM reasoning (injected as constraints/context)
- Comparison condition: LLM-only (no ASP output)

#### 3.3 Evaluation Design
- Gold standard: 100+ cases annotated by 3 expert raters
- Inter-rater agreement (Krippendorff Alpha)
- Task: Classify cases as A (National), B (Adat), C (Conflict), D (Insufficient)
- Metrics: Accuracy, per-class F1, McNemar test

### 4. Results (~2 pages)
#### 4.1 Rule Base Statistics
- 95 rules, distribution across domains and types
- Expert agreement rate on rule verification

#### 4.2 Symbolic Anchoring Effect
- LLM+ASP vs LLM-only accuracy comparison
- Per-class analysis (where does ASP help most?)
- Statistical significance (McNemar, 95% CIs)

#### 4.3 Error Analysis
- Where symbolic anchoring helps (conflict detection, constraint enforcement)
- Where symbolic anchoring fails (soft constraints, discretionary cases)
- Divergence analysis (cases where ASP and LLM disagree)

#### 4.4 Cross-Model Validation (optional but strengthens paper)
- Same pipeline with 2-3 different LLMs
- Is the symbolic anchoring effect model-agnostic?

### 5. Discussion (~1.5 pages)
- Implications for legal AI in pluralistic systems
- Limitations (sample size, domain scope, rule completeness)
- Negative results: debate protocol didn't help (honest reporting)

### 6. Conclusion (~0.5 pages)

---

## Data Requirements

| Data | Current | Needed | Action |
|---|---|---|---|
| Expert-verified rules | 95 (verified) | 95 (sufficient) | None |
| Gold standard cases | 82 (human pool) | 100+ with 3-rater labels | Expand 18+ cases |
| Active benchmark | 24 (evaluated) | 100+ (evaluated) | Promote from pool + expand |
| Inter-rater agreement | Not computed | Krippendorff Alpha | Compute from overlapping cases |
| LLM+Rules results | 41.67% offline | LLM mode results | Re-run with working env |
| LLM-only results | Not available | Baseline comparison | Run without ASP |
| Statistical tests | None | McNemar, CIs | Compute after experiments |

---

## Experiment Plan

### Experiment A: Inter-Rater Agreement (P-001)
- **Input**: 24 cases with 3 expert votes each
- **Method**: Compute Fleiss' Kappa and Krippendorff's Alpha
- **Expected Output**: Alpha score + interpretation
- **Gate**: Alpha >= 0.5 (moderate agreement) is acceptable; < 0.4 requires discussion

### Experiment B: LLM+Rules vs LLM-only (P-009)
- **Input**: 100+ gold standard cases
- **Conditions**:
  1. LLM (DeepSeek) WITH ASP rule output injected as context
  2. LLM (DeepSeek) WITHOUT ASP rule output
- **Metrics**: Accuracy, per-class F1, confusion matrix
- **Statistical Test**: McNemar's test (paired binary), p < 0.05
- **Expected Finding**: ASP anchoring improves conflict detection (label C) accuracy

### Experiment C: Rule Engine Standalone (P-008)
- **Input**: 100+ cases through ASP rules only (no LLM)
- **Purpose**: Measure what rules alone can classify correctly
- **Expected**: Lower overall accuracy but high precision on hard constraint cases

### Experiment D: Cross-Model (P-011, optional)
- **Input**: Same 100+ cases
- **Models**: GPT-4 and/or Claude (NOT DeepSeek-evaluating-DeepSeek)
- **Purpose**: Show symbolic anchoring is model-agnostic

---

## Risk Mitigation

| Risk | Likelihood | Plan |
|---|---|---|
| Inter-rater agreement too low | MEDIUM | Report honestly as limitation; focus on unanimous cases |
| ASP doesn't significantly help | MEDIUM | Publishable as negative result + report divergence analysis |
| N < 100 | MEDIUM | Minimum 82 cases + clear power analysis |
| Only DeepSeek tested | HIGH | Must test at least 1 alternative LLM |
| Expert unavailable | LOW | Dr. Hendra has been responsive; have backup plan |

---

## What This Paper Does NOT Claim

- Does NOT claim "GraphRAG" (no graph database exists)
- Does NOT claim multi-agent orchestration improves quality (negative result)
- Does NOT claim system is production-ready (research prototype)
- Does NOT claim symbolic reasoning is superior to LLM (they are complementary)
- Does NOT claim generalizability beyond Indonesian customary law

---

## Success Criteria

Paper is ready for submission when:
1. Inter-rater agreement computed and reported (any value — it's an empirical finding)
2. LLM+Rules vs LLM-only comparison done on 100+ cases
3. McNemar test shows p < 0.05 on at least one metric
4. At least 1 alternative LLM tested
5. Error analysis identifies specific categories where rules help
6. Limitations section is honest about scale, scope, and negative results
7. All claims are evidence-based with reproducible numbers
