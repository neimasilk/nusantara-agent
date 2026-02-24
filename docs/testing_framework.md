# Testing Framework — Multi-Agent, Multi-Human, Multi-Device

Dokumen ini menetapkan framework testing operasional agar pipeline riset dapat diuji, direplikasi, dan diaudit lintas agen/manusia/perangkat.

## 1. Tujuan

1. Menurunkan risiko regressions pada modul deterministik (`router`, parser JSON, utilitas token, pencarian KG).
2. Menjaga konsistensi keluaran lintas device dengan test yang tidak bergantung API eksternal.
3. Memisahkan validasi ilmiah (human/LLM independent review) dari validasi engineering (tes kode).

## 2. Layer Testing

### Layer A — Deterministic Unit Tests (wajib, offline)
- Lokasi: `tests/`
- Cakupan minimum:
  - `src/utils/token_usage.py`
  - `src/agents/router.py`
  - `src/agents/debate.py` (JSON parser helper)
  - `src/kg_engine/search.py`
  - utilitas parser di evaluator independen

#### Coverage Aktual (2026-02-24)
- `tests/test_token_usage.py` -> `src/utils/token_usage.py` (4 tests: `extract_token_usage`, `merge_usage`, fallback totals)
- `tests/test_router.py` -> `src/agents/router.py` (9 tests: `route_query`, `classify_router_accuracy`, edge cases)
- `tests/test_debate_json_parser.py` -> `src/agents/debate.py` (8 tests: `_json_or_raw`, fenced JSON, fallback paths)
- `tests/test_kg_search.py` -> `src/kg_engine/search.py` (8 tests: `SimpleKGSearch`, dedup, not-found fallbacks)
- `tests/test_llm_judge_utils.py` -> `src/evaluation/llm_judge.py` (3 tests: JSON extraction utilities)
- `tests/test_text_processor.py` -> `src/utils/text_processor.py` (10 tests: `extract_text_from_pdf`, `clean_legal_text`, `chunk_text`)
- `tests/test_rule_engine.py` -> `src/symbolic/rule_engine.py` (22 tests: `ClingoRuleEngine` + domain ASP rules)
- `tests/test_orchestrator.py` -> `src/agents/orchestrator.py` (32 tests: offline supervisor decision logic)
- `tests/test_nusantara_pipeline.py` -> `src/pipeline/nusantara_agent.py` (5 tests, offline with mocked orchestrator builder)
- `tests/test_benchmark_contract.py` -> `src/utils/benchmark_contract.py` (5 tests: unresolved label policy + manifest compatibility)
- `tests/test_dataset_split.py` -> `src/utils/dataset_split.py` (6 tests: split defaults, policy validation, strict filtering)
- `tests/test_claim_gate.py` -> `scripts/claim_gate.py` (3 tests: canonical vs exploratory /70 ratio policy)

**Total: 118 Deterministic Tests passed (`python -m unittest discover -s tests -p "test_*.py" -v`).**

### Layer B — Script Syntax Smoke Check (wajib sebelum merge)
- Seluruh skrip `src/` + eksperimen aktif harus lolos kompilasi syntax.
- Tujuan: menangkap error struktur kode lebih awal.

### Layer C — Pipeline Smoke (opsional tanpa API, wajib jika API tersedia)
- Jalankan subset query kecil (`N<=3`) untuk memastikan alur run tidak crash.
- Output harus menghasilkan `summary.json` dan `run_index.json` yang valid JSON.
- Untuk benchmark Exp 09:
  - Mode `scientific_claimable` wajib fail-hard jika benchmark manifest tidak koheren (hash/count/evaluable mismatch atau `count_matches_reference_claim=false`).
  - Mode `operational_offline` boleh dipakai untuk tracking harian, tetapi tidak boleh langsung jadi klaim paper.
  - Snapshot validasi strict 2026-02-24: `python scripts/validate_benchmark_manifest.py --require-reference-match` -> `errors=0`, `warns=0`.

### Layer D — Scientific Review Gate (wajib untuk klaim paper)
- Layer engineering lulus tidak otomatis berarti valid secara ilmiah.
- Tetap wajib jalur:
  - Self-critique (`REVIEW.md`)
  - Adversarial AI review (LLM independen)
  - Human review gate

## 3. Eksekusi Standar

Jalankan dari root repository:

```bash
python scripts/run_test_suite.py
```

Mode cepat (skip syntax check):

```bash
python scripts/run_test_suite.py --skip-syntax
```

## 4. Matrix Multi-Device

Checklist minimum sebelum kolaborator push dari device manapun:

1. `python scripts/run_test_suite.py` lulus.
2. Tidak ada file sementara/handoff personal yang ditambahkan ke root docs aktif.
3. Artifact eksperimen (`results/`, `score_summary*.json`) tidak diubah manual.
4. Semua perubahan status task mengacu ke `docs/task_registry.md`.

## 5. Matrix Multi-Human

1. Task `HUMAN_ONLY` tidak boleh ditandai DONE hanya dengan auto-fill script.
2. File dengan label `DRAFT_NEEDS_HUMAN_REVIEW` wajib diperlakukan sebagai draft.
3. Klaim kuantitatif dalam `analysis.md` harus menyebut sumber evaluator dan batasannya.

## 6. Matrix Multi-Agent

1. Parser output LLM harus fail-safe (JSON invalid tidak boleh crash pipeline).
2. Semua agent logs yang tersimpan wajib memiliki indeks artefak (`summary.json` / `run_index.json`).
3. Prompt update harus disertai uji regresi pada subset query tetap.

## 7. Definition of Done (Engineering)

Suatu perubahan dianggap siap integrasi jika:

1. Unit tests lulus.
2. Syntax smoke lulus.
3. Tidak menambah drift dokumentasi (duplikasi handoff/context note di docs aktif).
4. Risiko residual dicatat pada `docs/failure_registry.md` jika berdampak ke metodologi.
