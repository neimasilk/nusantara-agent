# Handoff — Sesi 2026-03-04

**Dibuat**: 2026-03-04
**Executor**: Claude Opus 4.6
**Owner**: Mukhlis Amien (amien@ubhinus.ac.id)

---

## APA YANG BERUBAH

### 1. Paper v0.6 → v0.7 (`paper/main.tex`)

**Perbaikan konsistensi angka canonical** — semua angka sekarang traceable ke `experiments/09_ablation_study/statistical_comparison_final_2026-02-20.json`:

| Item | Sebelum (v0.6) | Sesudah (v0.7) | Sumber |
|---|---|---|---|
| Table 7: all-agree correct | 34 (48.6%) | 35 (50.0%) | JSON `all_agree.correct=35` |
| Table 7: all-agree total | 47 (67.1%) | 48 (68.6%) | JSON `all_agree.total=48` |
| Table 7: two-agree | 21 (30.0%) | 19 (27.1%) | JSON `two_agree.total=19` |
| Table 7: all-different | 2 (2.9%) | 3 (4.3%) | JSON `all_disagree.total=3` |
| Table 5: ASP+LLM per-label | Stale 2026-02-19 data | Canonical 2026-02-20 DeepSeek | JSON `modes.deepseek.per_label_metrics` |
| Table 5: A recall | 0.83 (wrong!) | 0.67 | JSON `deepseek.A.recall=0.667` |
| Table 5: header | "ASP+LLM" | "ASP+DeepSeek" | Clarifies which backend |
| Table 4: bold | On Ollama 64.3% | On DeepSeek 68.6% (best) | Convention: bold=best |
| Majority vote | 11/21=52.4% | 9/19=47.4% | JSON `majority_vote: 9/19` |
| Agreement text | "67.1%" | "68.6%" | Matches corrected Table 7 |
| §7.1 date | (2026-02-19) | (2026-02-20) | Canonical freeze date |

**Hard cases section: 12 → 13 cases** — aligned with canonical JSON and paper's own Table 7 (13 all-agree-wrong):
- Added 1 D-label case (gold=D, all 3 predict C) to hard case distribution
- Updated all percentages in Tables 6 and 8
- Added D→C failure pattern row
- Updated Minangkabau over-representation reference
- Strengthens D-label failure narrative (over-represented 2.67× in hard cases)

### 2. CLAUDE.md sync
- Test count: 106 → 132 (actual)
- Ollama backend name: Qwen-2.5-7B → deepseek-r1 (canonical)
- Date: 2026-02-23 → 2026-03-04

### 3. Validasi
- **Claim gate**: PASSED (warning tentang exploratory /70 ratios — expected)
- **Test suite**: 132/132 OK
- **pdflatex**: PDF 16 halaman, build bersih (2 pass)

---

## APA YANG BELUM SELESAI

### Dari handoff 20260224 — Status prioritas

| Prioritas | Task | Status |
|---|---|---|
| P1 | Rubric refinement log (B3) | DONE — `docs/methodology/rubric_refinement_log.md` sudah FINAL (owner-confirmed Q4) |
| P2 | Cross-backend findings ke paper | DONE — sudah masuk di §7.5.3-4 (gpt-oss, Qwen3, B→A bias) sejak v0.6 |
| P3 | Update tabel benchmark | DONE — Table 4 sudah 3 konfigurasi; gpt-oss/Qwen3 di teks §7.5.3 |
| P4 | Polish Discussion | PARTIAL — narrative coherence fixed (angka), tapi Discussion section belum punya paragraph dedicated untuk connecting semua threads |

### Blocker yang tetap ada

1. **Ahli-2 batch baru (FUTURE TEST set)** — BLOCKED, butuh manusia
2. **Statistical power** — n=70, semua McNemar non-signifikan (p ≥ 0.17)
3. **Dev/test contamination** — 70 kasus existing terkontaminasi prompt tuning
4. **Discussion section polish** — belum ada paragraph yang menghubungkan error analysis → B→A bias → statistical power → next steps secara naratif

### Items yang perlu verifikasi owner

1. **Hard cases 12→13**: Saya mengidentifikasi 1 D-label case dari confusion matrix analysis yang masuk ke all-agree-wrong. Gold label verified via canonical JSON. Owner perlu review apakah update ini akurat.
2. **Table 5 ASP+LLM→ASP+DeepSeek**: Sebelumnya menggunakan data 2026-02-19 (A recall=0.83, tp=5/6), sekarang canonical 2026-02-20 (A recall=0.67, tp=4/6). Ini perubahan signifikan — 1 kasus A yang sebelumnya benar menjadi salah di canonical snapshot. Owner confirm?
3. **"70.0% at temperature=1.0" claim**: Disebutkan di §7.1 tapi tidak traceable ke file JSON manapun yang saya temukan. Perlu bukti atau hapus.

---

## NEXT ACTION PALING BERDAMPAK

### 1. (HIGH) Dedicated Discussion section
Paper saat ini tidak punya `\section{Discussion}` terpisah. Semua diskusi tersebar di §7 (Results) dan §8 (Limitations). Untuk jurnal Q1, Discussion section yang menghubungkan:
- Error analysis threads (C→B router, B→A bias, D-label failure)
- Rule over-specification paradox (F-018)
- Statistical power crisis dan framing "pilot"
- Cross-backend sensitivity dan implikasi untuk deployment
...akan sangat memperkuat paper.

### 2. (HIGH) Verify/remove "70.0% temperature=1.0" claim
Ini satu-satunya angka di paper yang belum saya temukan sumber JSON-nya.

### 3. (MEDIUM) Expand benchmark ke 100+ kasus
Blocker utama untuk klaim yang lebih kuat. Butuh Ahli-2 batch baru.

### 4. (LOW) Journal formatting
Setelah Discussion section selesai dan angka final, format ke template target (KBS/ESWA).

---

## PERINTAH UNTUK SESI BERIKUTNYA

```bash
cd /d/documents/nusantara-agent
git log --oneline -5
git status
cat docs/handoffs/20260304_paper_polish_handoff.md
```

---

## ANGKA CANONICAL (WAJIB — JANGAN KARANG)

Sumber: `experiments/09_ablation_study/statistical_comparison_final_2026-02-20.json`

| Backend | Correct | Accuracy | Wilson 95% CI | McNemar vs ASP-only |
|---|---|---|---|---|
| ASP-only | 41/70 | 58.57% | [0.469, 0.694] | — |
| ASP+Ollama (deepseek-r1) | 45/70 | 64.29% | [0.526, 0.745] | p=0.344 |
| ASP+DeepSeek API | 48/70 | 68.57% | [0.570, 0.782] | p=0.167 |

Exploratory (2026-02-23, bukan canonical):
| ASP+gpt-oss:20b | 45/70 | 64.29% | [0.526, 0.745] | p=0.646 |
| ASP+Qwen3-14B (F-019) | 38/70 | 54.29% | [0.427, 0.654] | p=0.480 |

Cross-model agreement: Fleiss κ = 0.638 (substantial)
All-agree: 48/70 (68.6%), two-agree: 19/70 (27.1%), all-different: 3/70 (4.3%)
Majority vote: 9/19 = 47.4%
Test suite: 132/132 passing
