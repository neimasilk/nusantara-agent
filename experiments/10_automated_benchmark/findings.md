# Experiment 10 — Data Source Feasibility Findings

**Date:** 2026-05-18
**Status:** Milestone 1 reached
**Question:** Can the nusantara-agent project pivot to a fully automated benchmark using publicly available Indonesian Supreme Court (MA) data, removing the customary-law expert bottleneck?

## TL;DR — Decision

**NO-GO for single-source automation.** **GO for hybrid pragmatic pivot.**

- `indo-law` (22,630 docs): dominated by general criminal cases — wrong domain for adat.
- `ledwindra/mahkamah-agung` (2,547 sample MA metadata): hit rate 0.08% under strict filter, ~0.47% under loose filter.
- `putusan3.mahkamahagung.go.id` direktori: rich category coverage (~89K potential adat cases across Waris/Tanah/Harta Bersama) but blocks bot access (HTTP 403, `robots.txt` `ai-train=no`).
- The remaining viable path is to **reuse the existing 74 expert-labeled cases as the gold benchmark**, augment with publicly-cited landmark adat decisions from academic literature, and run a wide multi-LLM evaluation. No new expert annotation required.

## Data Sources Investigated

### 1. indo-law (ir-nlp-csui/indo-law) — NOT VIABLE for adat

- **Size:** 22,630 XML files, ~526 MB. Full ZIP download truncated at 169 MB; full-corpus scan deferred and judged not worth re-running.
- **Coverage:** general criminal cases (`klasifikasi="pidana-umum"`), e.g. theft, forgery, assault, per the dataset README authored by the UI CSUI team.
- **Adat keyword sample (3 random files, full text inspected):** zero strict-mode matches; one loose-mode match was a substring false positive ("kaum" in a generic criminal context).
- **Verdict:** wrong domain. Adat disputes are dominantly civil (perdata) — inheritance, communal land, customary divorce. indo-law has no perdata coverage by design (UI's pipeline targeted criminal sentencing prediction).
- **Residual value:** possibly useful as a *control set* of non-adat criminal cases (to demonstrate that ASP rules don't falsely fire), but not as the primary corpus.
- **Decision rationale for skipping full scan:** even an optimistic upper-bound extrapolation (loose-filter hit rate 0.47% across random MA sample × 22K files = ~100 hits) would not be enough cases of the *right* type (these would be criminal-with-adat-context, not the perdata adat disputes our project targets).

### 2. ledwindra/mahkamah-agung — Useful for metadata, not full text

- **Asset:** `putusan-per-kasus.json` (4.5 MB, 2,547 records of MA decision metadata: nomor, klasifikasi, kata_kunci, catatan_amar, kaidah, abstrak).
- **Loose filter (token-level):** 12 hits / 2,547 (0.47%) — includes false positives ("Bali" as province, "marga" as surname).
- **Strict filter (phrase-level):** 2 hits / 2,547 (0.08%) — both confirmed Hindu-Bali customary divorce cases (PN Bangli, 2021).
- **Extrapolation to full MA:** if hit-rate constant, ~800 strict-mode adat cases across ~1M MA decisions. Realistic upper bound 2,000–3,000.
- **Critical gap:** metadata only — no full case text. Catatan amar is the only narrative field, often <1KB.
- **Verdict:** good for *finding* candidate cases by case number, but cannot serve as the corpus by itself.

### 3. putusan3.mahkamahagung.go.id — Rich but bot-blocked

- **Category counts (from ledwindra `klasifikasi.json`):**

  | Category (direktori) | Total cases |
  |---|---|
  | Tanah | 36,172 |
  | Waris Islam | 28,024 |
  | Harta Bersama | 16,462 |
  | Waris (perdata) | 5,442 |
  | Pembagian Harta | 1,331 |
  | Hibah | 1,023 |
  | **Total potentially adat-relevant** | **~88,500** |

- **Access:** `WebFetch` returns HTTP 403 on every request (Cloudflare + bot blocking).
- **`robots.txt`:** `ai-train=no` explicit policy; `ClaudeBot`, `GPTBot`, `CCBot` listed as disallowed.
- **Existing scrapers:** `okkymabruri/putusan` and `okkymabruri/putusan-mahkamahagung` are archived (Sep 2025), suggesting the site has hardened against scraping.
- **Verdict:** technically reachable with Playwright + careful rate-limiting, but ethically constrained by the explicit policy. For an *evaluation benchmark* (not training), the legal/ethical case is stronger than for fine-tuning, but reviewer pushback is realistic.

### 4. Existing 74 expert-labeled cases — Project asset, validated and split-ready

- **Provenance:** dual/quad-expert labels (Ahli-1 through Ahli-4); 70 evaluable + 4 disputed.
- **Label distribution (70 evaluable):** A=6 (8.6%), B=31 (44.3%), C=31 (44.3%), D=2 (2.9%).
- **Validation:** SHA256-tracked benchmark manifest; existing test suite (132 tests).
- **Pre-existing dev/test split (stratified by domain × label, seed=42):**

  | Split | Size | A | B | C | D |
  |---|---|---|---|---|---|
  | **Dev** | 49 | 3 | 23 | 21 | 2 |
  | **Locked test** | 21 | 3 | 8 | 10 | 0 |

- **Dev set narrative available**: `experiments/09_ablation_study/benchmark_dev_seed42.json` (49 cases with full `query` narrative, `gold_label`, all four `expert_votes`, `consensus`, and per-expert `interview_notes`). This is *more* than I expected to find — it is a publication-grade artifact.
- **Test set narrative status**: test set is locked-by-ID (`dataset_split.json`) but the per-case narratives are not in a single file. They must be reconstructed from `docs/human_only/artifacts/keputusan_ahli_final.md` (which has the four tie-resolution cases verbatim) plus other source-of-truth artifacts. Worth ~half a day of cleanup.
- **`gs_active_cases.json` itself is gitignored under `data/processed/`** and not present on disk. The dev seed file is the practical substitute.
- **Verdict:** the strongest asset the project owns. Took months of expert coordination to produce. Re-using it as the benchmark gold for a multi-LLM study sidesteps the very bottleneck that stalled the project.

### 5. Publicly-cited landmark adat decisions — Augmentable, no scraping

- Surfaced in web search of academic + MA Litbang sources:
  - **179 K/SIP/1961** — Karo customary inheritance (gender equality landmark)
  - **147 K/Pdt/2017** — Tionghoa customary inheritance
  - **573 K/Pdt/2017** — Batak Toba inheritance
  - **1130 K/Pdt/2017** — Manggarai customary inheritance
  - Plus MA Litbang book "Eksistensi dan Dinamika Hukum Adat Waris Bali dalam Putusan Pengadilan" (multiple Bali decisions)
  - Tapanuli yurisprudensi compilation (yonariza.com PDF)
- **Estimate:** 30–80 landmark decisions reachable through academic citations without touching the MA web direktori.
- **Verdict:** can supply an independent held-out test set of 20–50 high-value cases.

## Numeric summary

| Source | Records | Adat hits (strict) | Hit rate | Full text? |
|---|---|---|---|---|
| indo-law sample (3) | 3 | 0 | 0% | yes (XML) |
| indo-law full (planned) | 22,630 | TBD (likely <30) | TBD | yes (XML) |
| ledwindra metadata | 2,547 | 2 | 0.08% | no (metadata only) |
| MA direktori (theoretical) | ~1M | ~800–3000 | ~0.1–0.3% | yes (HTML/PDF) — blocked |
| Project gold (existing) | 74 | 74 (by construction) | 100% | yes (curated) |
| Landmark from literature | ~30–80 | ~30–80 | 100% | partial (cited fragments) |

## Why the original "fully automated from MA scrape" plan fails

1. **Robots.txt explicitly forbids AI use.** Even if technically possible, this puts a footnote-sized red flag on the paper that reviewers will catch.
2. **Adat hit rate in random MA sample is <1%.** Even with the full corpus accessible, the signal-to-noise ratio means most of the engineering effort would be filtering, not modeling.
3. **No full-text source for adat cases is publicly redistributable.** indo-law's license forbids re-hosting copies. ledwindra has no full text. Direktori MA is bot-blocked.
4. **Auto-labeling from court reasoning is not as clean as it sounds.** Sample inspection shows many adat-relevant decisions still apply national law (Hindu Bali divorces from PN Bangli use UU Perkawinan to dissolve marriages that were "adat-conducted"). The A/B/C/D classification is still genuinely ambiguous and may need expert review on edge cases.

## Why the existing 74-case benchmark is good enough for a preprint

- **n=70 evaluable** is small but defensible for an *introducing-the-benchmark* paper (ACL/EMNLP Findings, LREC).
- The novelty claim shifts from "we built a system that beats SOTA" to "we introduce the first labeled benchmark for Indonesian legal pluralism, with multi-LLM baselines."
- The 95 expert-verified ASP rules become a *resource* released alongside the benchmark, not the central efficacy claim.
- Negative findings (D-label collapse, A-vs-C confusion, McNemar non-significance) become *empirical lessons* contributed to the field.

## Recommended Hybrid Pivot

### Phase 1 — Multi-LLM benchmark on existing 74 cases (2–3 weeks)

- Run 6–7 LLM backends on the same 70 evaluable cases:
  - GPT-4o, Claude (Sonnet 4.x), Gemini 2.x, DeepSeek-V3, Llama-3.x-70B, Qwen3-14B, Mistral-Large
- Three condition variants per model: (a) LLM only, (b) LLM + ASP rules in context, (c) ASP-only (single deterministic baseline).
- Metrics: accuracy, Wilson CI, per-label F1, per-domain breakdown, Fleiss κ across systems, McNemar pairwise.
- API budget: ~$30–80 total (DeepSeek + OpenAI + Anthropic + Google) — request owner approval per CLAUDE.md cost-control mode.

### Phase 2 — Augment with landmark cases (1–2 weeks, after Phase 1)

- Manually curate 20–40 landmark adat decisions from academic literature (papers cited above).
- Auto-extract facts via LLM, label via cross-LLM consensus + author spot-check.
- Hold out as independent test set (never seen during Phase 1 development).

### Phase 3 — Optional MA scrape (3–4 weeks, only if Phase 1+2 leave room)

- Playwright-based scrape of `direktori/perdata/waris-1`, `harta-bersama-1`, `tanah-1` — categories most likely to contain adat content.
- Strictly evaluation-only; not redistributed.
- Document the ethical reasoning (public records, judicial decisions are public-mandate under SK KMA 144/2007).

### Phase 4 — Paper drafting (2 weeks)

- Repurpose existing `paper/main.tex` v0.7 as the base.
- Re-frame contribution: **resource + multi-LLM benchmark + neuro-symbolic augmentation**, not "system that beats baselines".
- Target venue: ACL/EMNLP Findings, LREC-COLING, or arXiv preprint as immediate working paper.

## What changes for the project

- **Owner unblocked.** No more waiting on Dr. Hendra / Dr. Indra correspondence.
- **74 cases are sufficient** for the new contribution frame; the original 344-case target is downgraded from "must-have" to "future-work".
- **Multi-LLM cost** replaces expert annotation cost. Roughly $50 vs months of expert coordination.
- **Paper title shift** (suggested): *"Can Large Language Models Reason About Indonesian Legal Pluralism? A Benchmark and Multi-Model Evaluation with Expert-Verified Customary Rules"*.

## Open questions for the owner

1. **API budget approval** for Phase 1 (estimated $30–80 across providers)? Required per CLAUDE.md cost-control mode.
2. **Venue preference:** ACL Findings, EMNLP Findings, LREC, or arXiv-first?
3. **Phase 3 (MA scrape) appetite:** is the project willing to absorb the ethical / technical complexity of Playwright-based scraping for incremental test data, or is Phase 1+2 enough?
4. **Title/scope:** keep "Neuro-Symbolic" framing or pivot harder to "Multi-LLM Benchmark"?

## Artifacts produced this milestone

- `experiments/10_automated_benchmark/scripts/filter_adat_cases.py` — loose-mode filter (12 hits)
- `experiments/10_automated_benchmark/scripts/filter_adat_strict.py` — strict-mode filter (2 hits)
- `experiments/10_automated_benchmark/scripts/scan_indo_law.py` — full indo-law scan (deferred until download completes)
- `experiments/10_automated_benchmark/samples/` — README + 3 sample XML + ledwindra metadata + classification
- `experiments/10_automated_benchmark/results/ledwindra_adat_report.md` — loose-mode report
- `experiments/10_automated_benchmark/results/ledwindra_adat_strict_report.md` — strict-mode report
- This document.
