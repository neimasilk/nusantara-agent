# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **scientific research repository** (not commercial software) building a Neuro-Symbolic Agentic GraphRAG system for pluralistic legal reasoning in Indonesia. The target is a Scopus Q1 publication in journals like *Information Fusion*, *Knowledge-Based Systems*, or *Expert Systems with Applications*.

The project is written primarily in **Indonesian** (variable names, prompts, documentation). Code comments, docstrings, and LLM prompts use Indonesian. When contributing, follow the existing language conventions.

## Environment Setup

- Python 3.11+
- Virtual environment: `python -m venv venv && venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
- Install dependencies: `pip install -r requirements.txt`
- Copy `.env.example` to `.env` and set `DEEPSEEK_API_KEY`

## Running Experiments

Experiments are self-contained scripts in `experiments/`. They must be run **from the project root** because they use relative paths and `sys.path.append(os.getcwd())` to resolve `src/` imports.

```bash
python experiments/01_triple_extraction/run_experiment.py
python experiments/02_graph_reasoning/graph_logic.py
python experiments/03_multi_agent_basic/multi_agent.py
python experiments/04_batch_ingestion/run_batch.py
```

There is no formal test suite. Each experiment directory contains an `analysis.md` with results and findings.

## Architecture

### Core Modules (`src/`)

- **`src/kg_engine/extractor.py`** — `TripleExtractor` class. Wraps the DeepSeek API (via OpenAI client) to extract structured knowledge triples.
- **`src/symbolic/rule_engine.py`** — `ClingoRuleEngine` class. Implementation of symbolic reasoning using Answer Set Programming (ASP) via the `clingo` library. Handles hard constraints and formal legal logic.
- **`src/utils/text_processor.py`** — PDF text extraction (PyMuPDF/fitz), legal text cleaning (regex-based), and paragraph-based text chunking.
- **`src/agents/`** — Multi-agent modules: `orchestrator.py` (LangGraph state graph), `debate.py` (debate protocol), `router.py` (conditional routing), `self_correction.py` (self-correction loop).

### Multi-Agent Design (LangGraph)

The system uses a **sequential state graph** via LangGraph:

1. **National Law Agent** — Analyzes queries against KUHPerdata (Indonesian Civil Code)
2. **Customary Law Agent** — Analyzes queries using Knowledge Graph data from adat (customary) law
3. **Supervisor Agent** — Synthesizes both perspectives, identifies norm conflicts, produces pluralistic legal reasoning

State flows: `national_law → adat_law → adjudicator → END`

### Data Flow

```
PDF → PyMuPDF extraction → clean_legal_text() → chunk_text() → DeepSeek API → JSON triples
                                                                                    ↓
                                                                          Neo4j KG (planned)
                                                                                    ↓
                                                                         Qdrant Vector DB (planned)
```

### LLM Integration

All LLM calls go through the **DeepSeek API** using the OpenAI Python client with `base_url="https://api.deepseek.com"` and model `deepseek-chat`. Two integration patterns exist:
- Direct `OpenAI` client (in `TripleExtractor` and experiment scripts)
- `ChatOpenAI` from `langchain_openai` (in multi-agent orchestration)

## Experiment SOP (Mandatory)

Every experiment **MUST** follow the template in `docs/experiment_template.md`. Key requirements:

1. **Pre-registration:** Fill hypothesis and acceptance criteria BEFORE running code.
2. **PROTOCOL.md:** Every experiment directory must have a `PROTOCOL.md` following the template.
3. **REVIEW.md:** Every experiment must have a `REVIEW.md` answering the 10 devil's advocate questions from `docs/review_protocol.md`.
4. **Failure registry:** All findings (positive AND negative) must be logged in `docs/failure_registry.md`.
5. **Review gate:** Experiments pass through a 3-layer review (self-critique → adversarial AI → human) before being considered complete.

For existing experiments (01-04), retrospective PROTOCOL.md and REVIEW.md files have been added.

## Review Protocol

All experiments and deliverables must go through the mandatory review process in `docs/review_protocol.md`:

- **10 devil's advocate questions** covering methodology, claims, validity, and honesty
- **Three-layer review:** self-critique → adversarial AI review (independent LLM, NOT DeepSeek) → human review gate
- **Adversarial reviewer:** Run `python -m src.review.adversarial_reviewer experiments/NN_name/` to generate hostile peer review using an independent LLM (requires `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`)
- **Severity classification:** CRITICAL / MAJOR / MINOR / SUGGESTION

## Task System

Work is decomposed into Atomic Research Tasks (ARTs). See:

- **`docs/task_template.md`** — Format for task specifications
- **`docs/task_registry.md`** — Master list of ~84 tasks across all project phases
- Each task specifies: type, executor (HUMAN_ONLY/AI_ONLY/EITHER), prerequisites, inputs/outputs, acceptance tests, and failure modes
- Tasks should be picked up from the registry and marked IN_PROGRESS → DONE as completed

## Current State (2026-02-07)

- **Rule Engine Functional**: `ClingoRuleEngine` implementasi ASP siap pakai.
- **Minangkabau Rules Expanded**: `src/symbolic/rules/minangkabau.lp` mencakup 30+ aturan formal (inheritance, actions, emergency conditions).
- **Exp 05 COMPLETED**: Menemukan 33.3% divergensi antara Rule Engine dan LLM (N=30), membuktikan perlunya "Symbolic Anchor" untuk mencegah halusinasi hukum.
- **Exp 07 COMPLETED (Negative Result)**: Advanced orchestration (parallel + debate + self-correction + routing) belum mengungguli baseline sequential pada auto-score Kimi (N=12), sehingga protokol debat perlu iterasi.
- **Draft rules**: `data/rules/minangkabau_rules.json` berisi aturan hasil ekstraksi open-access.

## Methodology Fixes

Six critical weaknesses have been identified and documented in `docs/methodology_fixes.md`:

1. "Neuro-symbolic" claim needs formal rule engine (Exp 05)
2. Circular evaluation needs independent evaluation pipeline (Exp 06)
3. Orchestration quality gain not yet achieved after Exp 07; debate protocol still needs improvement
4. Scale too small — needs 10K+ triples, 200+ test cases (scaling plan)
5. Ablation needs proper baselines, not strawman (Exp 09)
6. CCS metric needs rigorous validation (Exp 10)

## Key Conventions

- **Experiment-driven development**: New features start as isolated experiments in `experiments/NN_name/` with a runnable script, `PROTOCOL.md`, `REVIEW.md`, and `analysis.md`. Failures are valid research findings — log them in `docs/failure_registry.md`.
- **Imports from `src/`**: Experiment scripts add the project root to `sys.path`. Always run from project root.
- **Triple format**: Knowledge graph triples follow `{"head": str, "relation": str, "tail": str, "category": str, "confidence": float}`.
- **Domains**: Three customary law domains — Minangkabau, Bali, Jawa — plus national Indonesian law.
- **HITL workflow**: AI extracts triples, humans validate via JSON review, AI refines prompts based on `data/processed/human_feedback.json`.
- **No self-congratulatory language**: Avoid "BERHASIL", "SANGAT BERHASIL", "elegan" in analysis. Use quantified, evidence-based language.
- **Independent evaluation**: Never use DeepSeek to evaluate DeepSeek-generated output. Use a different LLM or human annotators.
