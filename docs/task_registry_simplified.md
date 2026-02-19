# Simplified Task Registry — Post-Pivot
**Tanggal:** 2026-02-12
**Scope:** Paper "Neuro-Symbolic Legal Reasoning with Expert-Verified Customary Law Rules"
**Prinsip:** Hanya task yang LANGSUNG berkontribusi ke paper. Tidak ada nice-to-have.

---

## Status Legend
- DONE: Selesai dan ter-evidence
- IN_PROGRESS: Sedang dikerjakan
- NEXT: Prioritas berikutnya
- BLOCKED: Menunggu dependency
- CANCELLED: Tidak diperlukan untuk paper scope baru
- ARCHIVED: Selesai tapi tidak digunakan di paper scope baru

---

## Retained Tasks (Essential for Paper)

### Phase A: Foundation Data (Week 1)

| # | Task | Executor | Status | Notes |
|---|---|---|---|---|
| P-001 | Hitung Inter-Rater Agreement (Fleiss Kappa / Krippendorff Alpha) dari 24 overlapping cases | AI | DONE | Lihat `docs/ira_analysis_2026-02-12.md` |
| P-002 | Resolve 2 SPLIT cases (CS-MIN-005, CS-MIN-015) — dapatkan 4th rater atau mark sebagai "ambiguous" | HUMAN | NEXT | |
| P-003 | Fix environment: install clingo + langchain_openai + langgraph | HUMAN/AI | DONE | Verified 2026-02-16 (`clingo`, `langchain_openai`, `langgraph` import OK) |
| P-004 | Re-run benchmark di LLM mode, dapatkan angka reproducible | AI | DONE | `runtime_backend=llm_langgraph`, hasil di `experiments/09_ablation_study/results_week1_refresh_2026-02-16.json` |

### Phase B: Expand Dataset (Week 2-4)

| # | Task | Executor | Status | Notes |
|---|---|---|---|---|
| P-005 | Expand gold standard ke 100+ kasus (dari 82 pool, tambah 18+) | HUMAN | NEXT | Dr. Hendra + Dr. Indra |
| P-006 | Generate ASP test cases untuk Bali domain (saat ini minim) | HUMAN/AI | NEXT | Rules ada, test cases belum |
| P-007 | Generate ASP test cases untuk Jawa domain | HUMAN/AI | NEXT | Rules ada, test cases belum |
| P-008 | Verifikasi ASP rules vs expert-verified JSON rules (consistency check) | AI | IN_PROGRESS | Update 2026-02-19: 30 rule `PARTIAL` sudah ditutup (Bali 4, Minangkabau 12, Jawa 14). Coverage terbaru: Bali 25/0/9, Minangkabau 17/0/8, Jawa 29/0/7 (COVERED/PARTIAL/GAP) -> total 71/95 (`74.74%`) COVERED. Lihat `docs/handoffs/20260218_p008_bali_asp_json_consistency.md`, `docs/handoffs/20260219_p008_minangkabau_asp_json_consistency.md`, `docs/handoffs/20260219_p008_jawa_asp_json_consistency.md`. |

### Phase C: Core Experiment (Week 3-5)

| # | Task | Executor | Status | Notes |
|---|---|---|---|---|
| P-009 | Run LLM+Rules vs LLM-only comparison pada 100+ kasus | AI | BLOCKED (P-005) | Core ablation |
| P-010 | Statistical tests: McNemar, paired proportion test, 95% CIs | AI | BLOCKED (P-009) | |
| P-011 | Run 1-2 LLM alternatif (GPT-4 atau Claude) untuk cross-validation | AI | BLOCKED (P-005) | API cost needed |
| P-012 | Error analysis: where rules help vs where rules fail | AI | BLOCKED (P-009) | Qualitative analysis |

### Phase D: Paper Writing (Week 6-8)

| # | Task | Executor | Status | Notes |
|---|---|---|---|---|
| P-013 | Draft paper: Introduction + Related Work | HUMAN/AI | BLOCKED (P-010) | |
| P-014 | Draft paper: Methodology (ASP encoding, rule verification) | HUMAN/AI | BLOCKED (P-010) | |
| P-015 | Draft paper: Results + Discussion | HUMAN/AI | BLOCKED (P-010, P-012) | |
| P-016 | Draft paper: Conclusion + Limitations | HUMAN/AI | BLOCKED (P-015) | |
| P-017 | Internal review (adversarial) | AI | BLOCKED (P-016) | |
| P-018 | Format untuk target journal | HUMAN | BLOCKED (P-017) | |

**Total: 18 tasks** (down from 91)

---

## Cancelled Tasks (Not in Paper Scope)

| Original ART | Task | Reason |
|---|---|---|
| ART-036 | Setup Neo4j | No graph database in pivoted scope |
| ART-037 | Setup Qdrant | No vector database in pivoted scope |
| ART-052 | NusaCulture-Bench | Defer to future work |
| ART-053 | Bali Domain Agent | No multi-agent in pivoted scope |
| ART-054 | Jawa Domain Agent | No multi-agent in pivoted scope |
| ART-055 | Inter-Agent Communication | No multi-agent in pivoted scope |
| ART-068-072 | CCS Metric Validation (Exp 10) | Metric not used in pivoted scope |
| ART-073-084 | Paper Writing (old scope) | Replaced by P-013 to P-018 |

## Archived Tasks (Done but Not Central to Paper)

| Original ART | Task | Reason |
|---|---|---|
| ART-043-048 | Advanced Orchestration (Exp 07) | Negative result — mention in paper as "future work" |
| ART-090-096 | Accuracy Tuning | Superseded by new evaluation plan |
| ART-057-064 | Individual Baseline Implementations | May partially reuse for P-009 |

---

## Dependencies

```
P-001 (IRA) ─────────────────────────────────────────→ P-013 (paper)
P-002 (resolve SPLIT) ──→ P-005 (expand) ──→ P-009 (comparison) ──→ P-010 (stats) ──→ P-013
P-003 (fix env) ──→ P-004 (re-run) ──→ P-009
P-006, P-007 (test cases) ──→ P-008 (verify) ──→ P-009
P-009 ──→ P-010, P-011, P-012 ──→ P-015 ──→ P-016 ──→ P-017 ──→ P-018
```

---

## Weekly Milestones

| Week | Deliverable | Gate |
|---|---|---|
| 1 | IRA computed, env fixed, LLM benchmark re-run | Alpha ≥ 0.5 |
| 2-3 | 100+ gold cases, Bali/Jawa test cases | Cases balanced across 3 domains |
| 4-5 | LLM+Rules vs LLM-only results, stats, error analysis | p < 0.05 on primary comparison |
| 6-7 | Paper draft complete | Passes internal adversarial review |
| 8 | Submit | Formatted for target journal |

Catatan Week-1 (as of 2026-02-16):
- Deliverable teknis Week-1 selesai (P-001, P-003, P-004 = DONE).
- Gate kualitas belum tercapai (`Cohen's Kappa = 0.394` < target 0.5); lanjut ke adjudikasi P-002 dan ekspansi data.
