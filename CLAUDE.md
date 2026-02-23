# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **scientific research repository** building a system for pluralistic legal reasoning in Indonesia. The target is a Scopus Q1 publication in journals like *Knowledge-Based Systems* or *Expert Systems with Applications*.

**Paper Focus (post-pivot 2026-02-12):** Neuro-Symbolic Legal Reasoning with Expert-Verified Customary Law Rules — combining ASP (Answer Set Programming) symbolic reasoning with LLM-based analysis for Indonesian customary law domains.

The project is written primarily in **Indonesian** (variable names, prompts, documentation). Code comments, docstrings, and LLM prompts use Indonesian. When contributing, follow the existing language conventions.

## Environment Setup

- Python 3.11+
- Virtual environment: `python -m venv venv && venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
- Install dependencies: `pip install -r requirements.txt`
- Copy `.env.example` to `.env` and set `DEEPSEEK_API_KEY`
- **Critical optional deps**: `clingo` (for ASP rule engine), `langchain_openai` + `langgraph` (for LLM pipeline)

## Running Experiments

Experiments are self-contained scripts in `experiments/`. They must be run **from the project root** because they use relative paths and `sys.path.append(os.getcwd())` to resolve `src/` imports.

```bash
python experiments/01_triple_extraction/run_experiment.py
python experiments/05_rule_engine/run_experiment.py
```

Formal test suite tersedia (`python scripts/run_test_suite.py`) dengan deterministic unit tests untuk modul inti.

## Architecture

### What Actually Exists (as of 2026-02-12)

- **`src/symbolic/rule_engine.py`** — `ClingoRuleEngine` class. ASP-based symbolic reasoning via Clingo. **This is the core contribution.**
- **`src/symbolic/rules/*.lp`** — ASP rule files for 4 domains: `minangkabau.lp`, `bali.lp`, `jawa.lp`, `nasional.lp`
- **`src/agents/orchestrator.py`** — LangGraph-based orchestrator (National → Adat → Supervisor). Has offline fallback mode with `_offline_supervisor_decision()` heuristic (HAM extreme → national dominant → symbolic conflict → route-based).
- **`src/agents/router.py`** — Query classifier (keyword-based, with LLM option).
- **`src/utils/llm.py`** — Shared `get_llm()` factory for DeepSeek ChatOpenAI instances.
- **`src/pipeline/nusantara_agent.py`** — Unified pipeline combining router + rules + agents.
- **`src/kg_engine/extractor.py`** — DeepSeek API wrapper for triple extraction.
- **`src/kg_engine/search.py`** — Simple keyword-based KG search.
- **`src/utils/text_processor.py`** — PDF extraction, text cleaning, chunking.

### What Does NOT Exist (Planned but Unimplemented)

- **Neo4j Graph Database** — Not implemented. Pipeline uses local JSON files.
- **Qdrant Vector Database** — Not implemented. Pipeline uses keyword matching fallback.
- **Real RAG Pipeline** — No embedding-based retrieval. "Retrieval" is keyword matching against hardcoded sentences.
- **Genuine Multi-Agent Orchestration** — Debate protocol (Exp 07) produced **negative result** (F-009). Self-correction loop showed no measurable improvement. Both are abandoned for paper scope.

### Data Flow (Actual)

```
Query → Keyword Router → Keyword Fact Extraction → ASP Rule Engine (Clingo)
                                                          ↓
                                         LLM Agents (DeepSeek, if available)
                                                          ↓
                                                   Label (A/B/C/D)
```

Offline mode replaces ASP + LLM with Python if/else keyword matching.

### LLM Integration

All LLM calls go through the **DeepSeek API** using the OpenAI Python client with `base_url="https://api.deepseek.com"` and model `deepseek-chat`. Two integration patterns exist:
- Direct `OpenAI` client (in `TripleExtractor` and experiment scripts)
- `ChatOpenAI` from `langchain_openai` (in multi-agent orchestration)

### API Cost-Control Mode (Effective 2026-02-08)

- Default workflow: offline-first (tanpa API berbayar).
- Jangan jalankan call DeepSeek/Kimi kecuali ada blocker kritis dan persetujuan eksplisit owner.
- Saat meminta persetujuan, sebutkan tujuan call, estimasi usage/token, dan alasan kenapa alternatif offline tidak cukup.

## Task System

**Post-pivot (2026-02-12):** See `docs/task_registry_simplified.md` for the focused 18-task plan.

Legacy registry: `docs/task_registry.md` (91 tasks, many cancelled/archived after pivot).

## Current State (as of 2026-02-23) — HONEST ASSESSMENT

### What Works
- **Rule Engine**: `ClingoRuleEngine` with ASP is functional (when `clingo` is installed)
- **95 Expert-Verified Rules**: Minangkabau (25), Bali (34), Jawa (36) — all verified by domain experts
- **82 Human-Labeled Cases**: From 2 qualified expert raters (Ahli-1 Dr. Hendra, Ahli-2 Dr. Indra), covering 3 adat domains + national law. Ahli-3 removed (under-qualified, S1 level only — see F-014).
- **74 Benchmark Cases**: 70 evaluable (agreed), 4 disputed (excluded from accuracy)
- **ASP-only**: 58.6% (41/70), Wilson CI [0.469, 0.694]
- **ASP+Ollama (Qwen-2.5-7B, temp=0)**: 64.3% (45/70), Wilson CI [0.526, 0.745]
- **ASP+DeepSeek (temp=0)**: 68.6% (48/70), Wilson CI [0.570, 0.782]
- **McNemar p-values**: 0.344, 0.167, 0.549 — semua NON-SIGNIFIKAN (n=70)
- **Inter-system agreement**: Fleiss kappa = 0.638 (substantial)
- **ASP rules aktif**: 71 dari 95 expert-verified (24 di-rollback, lihat F-018)
- **Test Suite**: 106 tests passing (termasuk benchmark contract tests untuk label `DISPUTED/SPLIT`)
- **Shared utils**: LLM init extracted to `src/utils/llm.py`, used by all agent modules

### What Doesn't Work
- **D-label prediction: 0%** — system predicts C instead of D for insufficient-info cases
- **Statistical power insufficient**: n=70 → power ~0.3; butuh ~344 kasus untuk power=0.8
- **Dev/test contamination**: 70 kasus existing sudah terkontaminasi prompt tuning; belum ada clean test set
- **Multi-Agent Debate: NEGATIVE RESULT** (F-009) — does not improve over sequential baseline
- **Independent Evaluation: BLOCKED** — Exp 06 blocked on human annotation (ART-028, ART-030)
- **Scale insufficient for statistical power**: n=70 → power ~0.3; butuh ~344 kasus untuk confident claims. Kasus baru dari Ahli-2 belum tersedia.

### Key Negative Results
- Exp 07: Advanced orchestration WORSE than baseline sequential (F-009)
- F-011: Adding agents DECREASED accuracy from 68% to 54% (MITIGATED: prompt tuning; canonical benchmark now 70 cases)
- F-014: Ahli-3 had negative Cohen's Kappa — removed from gold standard
- F-018: Penambahan 24 GAP rules menyebabkan regresi -7.1pp → di-rollback
- F-008: Gold standard was initially self-referential
- F-010: Auto-annotations have drift risk (circular evaluation)

### Strategic Pivot (2026-02-12)
Paper scope narrowed from "Neuro-Symbolic Agentic GraphRAG" to "Neuro-Symbolic Legal Reasoning with Expert-Verified Rules". See `docs/strategic_review_2026-02-12.md` for full rationale.

## Methodology Fixes

Six critical weaknesses documented in `docs/methodology_fixes.md`:

| # | Weakness | Post-Pivot Status |
|---|---|---|
| 1 | "Neuro-symbolic" claim not earned | **CORE FOCUS** — ASP rules are the main contribution |
| 2 | Circular evaluation | **MUST FIX** — need independent evaluation |
| 3 | Orchestration not justified | **DROPPED** — negative result, not in paper scope |
| 4 | Scale too small | **MUST FIX** — need 100+ cases minimum |
| 5 | Strawman baselines | **SIMPLIFIED** — focus on LLM+Rules vs LLM-only |
| 6 | CCS metric unvalidated | **DROPPED** — not in paper scope |

## Key Conventions

- **Experiment-driven development**: New features start as isolated experiments in `experiments/NN_name/` with a runnable script, `PROTOCOL.md`, `REVIEW.md`, and `analysis.md`. Failures are valid research findings — log them in `docs/failure_registry.md`.
- **Imports from `src/`**: Experiment scripts add the project root to `sys.path`. Always run from project root.
- **Domains**: Three customary law domains — Minangkabau, Bali, Jawa — plus national Indonesian law.
- **No self-congratulatory language**: Avoid "BERHASIL", "SANGAT BERHASIL", "elegan" in analysis. Use quantified, evidence-based language.
- **Independent evaluation**: Never use DeepSeek to evaluate DeepSeek-generated output. Use a different LLM or human annotators.
- **Evidence-based claims only**: Every claim in the paper must be backed by reproducible data with statistical tests.
