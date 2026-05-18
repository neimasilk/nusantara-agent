# Experiment 10 — Automated Benchmark Feasibility & Pivot

## Purpose

Following the strategic pivot conversation on 2026-05-18, this experiment
investigates whether the nusantara-agent project can move to a fully
automated benchmark pipeline that removes the customary-law expert
bottleneck (which stalled the original project).

## Status

**Milestone 1 (data source feasibility): REACHED.**

See [`findings.md`](findings.md) for the full assessment. The headline result is:

- **Single-source automation is not viable** — indo-law is criminal, ledwindra is metadata-only, MA direktori is bot-blocked.
- **Hybrid pragmatic pivot is viable** — reuse the existing 74 expert-labeled cases, augment with literature-cited landmark decisions, and run a wide multi-LLM evaluation. No new expert annotation needed.

## Directory layout

```
10_automated_benchmark/
├── README.md                         (this file)
├── findings.md                       (milestone 1 strategic write-up)
├── PROTOCOL.md                       (to be drafted before Phase 1)
├── samples/                          (downloaded raw data for analysis)
│   ├── indo-law-README.md
│   ├── *.xml                         (3 sample indo-law files)
│   ├── ledwindra-klasifikasi.json    (~19 KB, MA category totals)
│   └── ledwindra-putusan-per-kasus.json  (4.5 MB, 2547 case metadata)
├── scripts/
│   ├── filter_adat_cases.py          (loose-mode adat keyword filter)
│   ├── filter_adat_strict.py         (phrase-level strict filter)
│   └── scan_indo_law.py              (full-corpus scan, run after extract)
├── results/
│   ├── ledwindra_adat_report.md
│   ├── ledwindra_adat_filtered.json
│   ├── ledwindra_adat_strict_report.md
│   ├── ledwindra_adat_strict.json
│   └── indo_law_scan_report.md       (pending, after extract)
└── indo-law.zip                      (526 MB, download artifact, gitignored)
```

## How to run the existing analyses

```powershell
# Strict adat filter on ledwindra MA metadata sample
python experiments/10_automated_benchmark/scripts/filter_adat_strict.py

# Loose-mode filter (broader keyword set, more false positives)
python experiments/10_automated_benchmark/scripts/filter_adat_cases.py

# Full indo-law scan (after extracting indo-law.zip)
python experiments/10_automated_benchmark/scripts/scan_indo_law.py
```

## Next steps

Phase 1 of the recommended pivot — multi-LLM benchmark on the existing
74 cases — requires owner sign-off because it touches the API cost-control
policy in `CLAUDE.md`. See `findings.md` § "Open questions for the owner".

Until Phase 1 starts, all artifacts here are deterministic, offline, and
do not consume API budget.

## Why this experiment exists

Original project (paper v0.7) ran into a wall: expanding the gold-standard
benchmark from 70 to 344+ cases requires more expert annotation, and
expert coordination has stalled. This experiment formalises the decision
that "we cannot wait for more experts" is itself a finding, and answers
"what *can* we do with what's already on the shelf?".
