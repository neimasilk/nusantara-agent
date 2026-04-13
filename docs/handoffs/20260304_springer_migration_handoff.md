# Handoff — Sesi 2026-03-04 (Springer Migration)

**Dibuat**: 2026-03-04
**Executor**: Claude Opus 4.6
**Owner**: Mukhlis Amien (amien@ubhinus.ac.id)

---

## KEPUTUSAN STRATEGIS SESI INI

1. **Pivot ke methodology paper** — Ahli-2 susah dihubungi, jadi paper di-reframe dari empirical contribution ke methodology-first contribution.
2. **Target jurnal: Artificial Intelligence and Law (Springer)** — Scopus Q1-Q2, subscription model = **gratis** (no APC), double-blind review.
3. **Alternatif venue**: ICAIL 2026 Singapore (conference), JURIX 2026 (conference).

---

## APA YANG BERUBAH

### 1. Mata Elang Review #3
- File: `docs/handoffs/20260304_eagle_eye_opus_review.md`
- Temuan utama: deadline fork 11 hari, paper missing Discussion section, "70.0% at temp=1.0" claim untraceable, 868 baris dead code.

### 2. Paper Springer (`paper/main_springer.tex`) — FILE BARU
Migrasi penuh dari `paper/main.tex` (custom article class) ke Springer Nature `sn-jnl` format.

**Perubahan struktural besar:**
- Document class: `sn-jnl` dengan `sn-basic` bibliography style
- **Discussion section baru** (§8) — 4 subsections connecting error analysis, compensation dynamic, statistical power, implications
- **System Overview diperluas** — architecture diagram (verbatim figure), ASP rule example (verbatim figure), pipeline description 3-stage
- **Rule over-specification table** — before/after comparison (71 vs 95 rules, -7.1pp)
- **F1 scores** ditambahkan ke per-label table
- **Related Work** di-rewrite — dari citation dump ke thematic discussion per-work
- **Double-blind compliant** — anonymous@example.com, [Withheld] affiliation, no GitHub URL
- **Declarations block** lengkap (Funding, CoI, Ethics, Data/Code availability)

**Fixes dari critical review (23 issues):**
- `p >= 0.17` → `p >= 0.167` (5 lokasi)
- Removed conflicting packages: `\usepackage{geometry}`, `\usepackage[title]{appendix}`, `graphicx`, `algorithm*`, `textcomp`
- Terminologi standar: "ASP-only", "ASP+local-LLM", "ASP+API-LLM"
- Grammar fixes, table cross-references, merged Scope+Roadmap

### 3. Bibliography cleanup (`paper/references.bib`)
- **Dihapus** (5 unused): `vaswani2017attention`, `achiam2023gpt4`, `touvron2023llama2`, `jiang2023mistral`, `tyss-etal-2024-supporting`
- **Ditambahkan** (2 new): `wilson1927probable` (Wilson CI, JASA 1927), `lachin1992power` (McNemar power, Stat Med 1992)

### 4. Claim gate update (`scripts/claim_gate.py`)
- Sekarang menerima CLI argument: `python scripts/claim_gate.py paper/main_springer.tex`
- Regex baru untuk format "Total benchmark cases & 74"

### 5. Springer template (`paper/springer-ail-template/`)
- `sn-jnl.cls`, `sn-basic.bst` — copied to `paper/` for build
- Template reference files preserved in subdirectory

---

## STATUS VALIDASI

| Check | Status |
|---|---|
| pdflatex build | 17 halaman, clean (font warnings only — cosmetic) |
| bibtex | Clean, semua 27 entries resolved |
| Claim gate (main_springer.tex) | **PASSED** |
| Test suite | **132/132 OK** |
| Undefined citations | None |
| Double-blind | OK (anonymous author, withheld affiliation, no URLs) |

**Known cosmetic issue:** `\maketitle` produces "Misplaced \crcr" error in nonstop mode — ini bug sn-jnl class saat author block di-anonymize. PDF tetap correct. Non-blocking.

---

## BELUM DI-COMMIT

Semua perubahan sesi ini **belum di-commit**. File yang perlu di-stage:

```
# New files
paper/main_springer.tex
paper/sn-jnl.cls
paper/sn-basic.bst
paper/springer-ail-template/
docs/handoffs/20260304_eagle_eye_opus_review.md
docs/handoffs/20260304_springer_migration_handoff.md

# Modified files
paper/references.bib
scripts/claim_gate.py
```

`paper/main.tex` juga modified (dari sesi sebelumnya, v0.6→v0.7 fixes).

---

## APA YANG BELUM SELESAI

### Prioritas tinggi
1. **Commit semua perubahan** — belum ada commit untuk seluruh sesi ini
2. **Verify "70.0% at temperature=1.0" claim** — disebutkan di main.tex §7.1, tidak traceable ke JSON manapun. Perlu bukti atau hapus dari main_springer.tex juga (sudah tidak ada di Springer version, tapi main.tex masih punya)
3. **Hard cases 12→13 verification** — owner perlu confirm D-label case yang ditambahkan
4. **Table 5 ASP+LLM→ASP+DeepSeek verification** — A recall turun dari 0.83→0.67

### Prioritas medium
5. **Buat proper figures** — paper saat ini 0 real figures (hanya verbatim text boxes). Untuk Springer submission, minimal perlu 1-2 proper figures (architecture diagram, confusion matrix, dll)
6. **`\maketitle` cosmetic error** — investigate sn-jnl class fix untuk anonymized author block
7. **Dead code cleanup** — 868 baris dead code + 242 files Exp 07

### Prioritas rendah
8. **Expand benchmark ke 100+ kasus** — butuh Ahli-2 batch baru atau rater baru
9. **Journal formatting final check** — setelah semua content fixes

---

## ANGKA CANONICAL (WAJIB — JANGAN KARANG)

Sumber: `experiments/09_ablation_study/statistical_comparison_final_2026-02-20.json`

| Backend | Correct | Accuracy | Wilson 95% CI | McNemar vs ASP-only |
|---|---|---|---|---|
| ASP-only | 41/70 | 58.57% | [0.469, 0.694] | — |
| ASP+local-LLM (deepseek-r1) | 45/70 | 64.29% | [0.526, 0.745] | p=0.344 |
| ASP+API-LLM (DeepSeek) | 48/70 | 68.57% | [0.570, 0.782] | p=0.167 |

Fleiss' κ = 0.638, All-agree: 48/70 (68.6%), Test suite: 132/132

---

## PERINTAH UNTUK SESI BERIKUTNYA

```bash
cd /d/documents/nusantara-agent
git log --oneline -5
git status
cat docs/handoffs/20260304_springer_migration_handoff.md
```
