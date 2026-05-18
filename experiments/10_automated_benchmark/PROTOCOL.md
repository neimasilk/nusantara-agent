# Experiment 10 Phase 1 — Multi-LLM Benchmark Protocol (Hemat Mode)

**Status:** Owner-approved with hard budget cap. Providers + models confirmed.
**Date:** 2026-05-18
**Budget ceiling:** <$5 per provider × 3 providers = <$15 total (likely <$1 actual).

## Hypotheses

- **H1** — Independent LLM backends share a bias on Indonesian legal pluralism: across-LLM agreement (Fleiss κ) exceeds LLM-vs-gold agreement (Cohen κ).
- **H2** — Adding the project's expert-verified ASP rules to the prompt narrows the LLM-vs-gold gap by ≥5pp on average (95% Wilson CI excludes zero).
- **H3** — Label-D (insufficient information) failure replicates across all backends, generalising F-014.

All three testable on the existing 70 evaluable cases without new annotation.

## Dataset

- **Dev (49 cases, full narrative):** `experiments/09_ablation_study/benchmark_dev_seed42.json`
- **Test (21 cases, ID-locked):** `experiments/09_ablation_study/dataset_split.json:locked_test_set` — narratives reassembled into `experiments/10_automated_benchmark/data/benchmark_test_recovered.json` (Task #7).
- **Disputed (4 cases):** reserved as qualitative case study.

## Providers and models (REVISED for hemat mode)

### Tier-paid (with credit cap <$5 each)

| Provider | Model | Base URL | Why |
|---|---|---|---|
| DeepSeek | `deepseek-chat` | `https://api.deepseek.com` | Cheapest; supports context caching; already integrated |
| xAI (Grok) | `grok-2-latest` or `grok-2-mini` | `https://api.x.ai/v1` | Cross-vendor reference; user has key |
| Moonshot (Kimi) | `moonshot-v1-8k` | `https://api.moonshot.cn/v1` | Asian-language strength; cheap 8k context |

### Tier-free (local Ollama, unlimited runs)

| Model | Purpose |
|---|---|
| `deepseek-r1` (or current local install) | Reasoning baseline |
| `qwen3-14b` (already shown in Exp 09) | Cross-architecture reference |
| `llama-3.x` if available locally | Open-weight baseline |

**Out of scope** (no API access): GPT-4o, Claude, Gemini.

## Token economy contract

Per the [[feedback-token-economy]] guideline, every paid call must be cheaper than necessary.

### Prompt design

- **Indonesian only** (no English doubling). Indonesian Mata uang dalam tokenization compact.
- **Single system prompt** shared across all calls — cached.
- **Single user message** containing only the case narrative.
- **Forced structured output**: `{"label": "A|B|C|D", "alasan": "≤30 kata"}`. No chain-of-thought, no reasoning trace.

### Cost saving features mandatory

- **Context caching ON** for DeepSeek (75% cache discount), Moonshot (50% cache discount).
- **Temperature 0** (deterministic, no resampling waste).
- **`max_tokens` cap on output** at 120 tokens (well above what JSON needs; prevents runaway).
- **Strip whitespace from rules dump** in condition 2 (compact ASP representation).

### Per-call token estimate

| Condition | Input tokens | Output tokens |
|---|---|---|
| 1: LLM-only | ~280 (sys 100 + case 150 + instr 30) | ≤80 (JSON) |
| 2: LLM + ASP rules | ~680 (sys 100 + rules 400 + case 150 + instr 30) | ≤80 (JSON) |

### Per-provider cost estimate (70 cases × 2 conditions = 140 calls)

| Provider | Input tokens | Output tokens | Without cache | With cache | Verdict |
|---|---|---|---|---|---|
| DeepSeek | ~67K | ~11K | ~$0.04 | ~$0.02 | ✅ <0.5% of $5 cap |
| Grok-2 | ~67K | ~11K | ~$0.25 | n/a | ✅ <5% of $5 cap |
| Kimi-v1-8k | ~67K | ~11K | ~$0.20 | ~$0.10 | ✅ <2% of $5 cap |
| **Total paid** | | | **~$0.49** | **~$0.32** | Far under $15 ceiling |

(Pricing as of best knowledge 2026-05; verify with smoke test before full sweep.)

## Conditions per case

For every model:
1. **LLM-only** — narrative → label
2. **LLM + ASP-derived facts** — narrative + Clingo's derivation for this case → label

Plus deterministic **ASP-only baseline** (no LLM) run once on all 70 cases. Already captured in `results_dual_asp_only_2026-02-19.json`.

## Workflow (execution order)

1. **Recover test narratives** (Task #7) — offline, no API.
2. **Build harness** (Task #8) — offline, no API.
3. **Smoke test on Ollama** (Task #9) — local, free. Validates harness on 5 stratified cases.
4. **Confirm token estimate to owner** (Task #10) — measured against actual smoke-test counts.
5. **Run DeepSeek** (Task #11) — cheapest first. Owner sees per-call cost in stream output.
6. **Run Grok and Kimi** (Task #12) — only if DeepSeek run succeeds and bill matches estimate.
7. **Stats and error analysis** (Task #13) — offline.

If at step 5 the actual DeepSeek cost exceeds 2× the estimate, halt and re-estimate before proceeding to Grok / Kimi.

## Metrics

- Accuracy + Wilson 95% CI per (model × condition).
- Per-label F1 (focus on label-D recall).
- Per-domain breakdown (Minangkabau, Bali, Jawa, Lintas, Nasional, Other).
- Fleiss κ across models per condition.
- Cohen κ model vs gold per (model × condition).
- McNemar pairwise between every (model × condition) pair.
- Operational: tokens, latency, cost per case (logged from raw API responses).

## Storage

```
experiments/10_automated_benchmark/
├── data/
│   └── benchmark_test_recovered.json     (Task #7 output)
├── prompts/
│   ├── system_prompt.txt                 (cached prefix)
│   └── rules_context.txt                 (cached ASP dump)
├── harness/
│   ├── runner.py                         (OpenAI-compatible multi-provider client)
│   ├── prompt_builder.py
│   └── label_parser.py
├── runs/
│   └── YYYY-MM-DD/
│       └── <provider>_<condition>.jsonl  (one line per case)
└── analysis/
    └── ...                                (Task #13 output)
```

## Hard rules (non-negotiable)

- Never commit `.env.txt` or any file containing API keys.
- Show the estimated bill before any paid sweep.
- Halt and ask owner if any provider's measured per-call cost is ≥2× the estimate.
- Local Ollama runs come BEFORE any paid call.
- No multi-agent debate, no self-correction, no chain-of-thought output — all proven counterproductive (F-009) or expensive without benefit.

## What we are not doing in Phase 1

- No GPT-4o / Claude / Gemini (no API access).
- No new annotation.
- No web scraping of putusan3.mahkamahagung.go.id.
- No fine-tuning.
- No paid run before smoke test passes.
