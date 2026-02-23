# Prompt Lanjutan — Sesi 2026-02-24

**Dibuat**: 2026-02-23 (akhir sesi)
**Untuk**: Sonnet 4.6 (atau model apapun yang melanjutkan)
**Copy-paste prompt ini di awal sesi besok.**

---

## PROMPT UNTUK SESI BESOK

```
Kamu adalah Claude Sonnet 4.6, melanjutkan sesi penelitian dari 2026-02-23.
Working directory: D:/documents/nusantara-agent
Baca file ini dulu sebelum melakukan apapun: docs/handoffs/20260224_prompt_lanjutan.md

Ini adalah proyek paper ilmiah "Neuro-Symbolic Legal Reasoning for Indonesian
Customary Law" (target: Knowledge-Based Systems / Scopus Q1). Kamu berperan sebagai
manajer proyek dengan akses ke 3 sub-agent: Codex (terkuat), Gemini (medium),
Kimi (butuh guidance detail).

---

## APA YANG SUDAH SELESAI KEMARIN (2026-02-23)

### Paper (main.tex v0.5 — SUDAH COMMIT cc2b48d)
- Abstract: rewrite lengkap — 3 konfigurasi + Wilson CI + McNemar qualifier
- Introduction: Research Gap, Contributions, Scope, Roadmap
- Related Work: 4 cluster + Research Gap paragraph
- System Overview: design motivation + kappa=0.638
- Results §5.1: "improves" → "observed improvement, non-significant"
- Results: tambah paragraph Two-layer error diagnosis (23/29 router, 6/29 prompt)
- Limitations: section baru 6 paragraf + Scope and Generalizability paragraph
- Conclusion: next steps diupdate, framing hedged
- Fleiss kappa: 0.633 → 0.638 (5 lokasi, fixed)
- Paper version: v0.4 → v0.5, tanggal 2026-02-23

### Dokumen baru (SUDAH COMMIT)
- docs/methodology/dev_test_split_policy.md
- docs/methodology/error_analysis_cb_pattern.md
- docs/failure_registry.md: F-018 (GAP rules) + F-019 (Qwen3 negative)

### Benchmark hasil (SUDAH COMMIT, semua di experiments/09_ablation_study/)
- results_dual_asp_only_2026-02-23.json (ASP-only: 42/70=60.00%)
- results_dual_asp_llm_qwen3_14b_2026-02-23.json (Qwen3: 38/70=54.29% — NEGATIVE F-019)
- results_dual_asp_llm_gpt_oss_20b_2026-02-23.json (gpt-oss: 45/70=64.29% — positive)
- gpt_oss_20b_result_analysis_2026-02-23.json
- qwen3_14b_negative_result_analysis_2026-02-23.json

---

## ANGKA CANONICAL (WAJIB HAFAL — JANGAN KARANG)

Sumber canonical: experiments/09_ablation_study/statistical_comparison_final_2026-02-20.json

| Backend | Correct | Accuracy | Wilson 95% CI | McNemar vs ASP-only |
|---|---|---|---|---|
| ASP-only | 41/70 | 58.57% | [0.469, 0.694] | — |
| ASP+Ollama (deepseek-r1) | 45/70 | 64.29% | [0.526, 0.745] | p=0.344 |
| ASP+DeepSeek API | 48/70 | 68.57% | [0.570, 0.782] | p=0.167 |
| ASP+gpt-oss:20b | 45/70 | 64.29% | [0.526, 0.745] | p=0.646 |
| ASP+Qwen3-14B (F-019) | 38/70 | 54.29% | [0.427, 0.654] | p=0.480 |

Semua McNemar non-signifikan. Fleiss kappa antar 3 sistem canonical: 0.638.
Rules aktif: 71 dari 95 (24 di-rollback — F-018).
Test suite: 106 tests passing.

---

## TEMUAN BARU DARI 2026-02-23 (BELUM MASUK PAPER)

### 1. B→A Bias Struktural (open-source backends)
- 6 kasus identik gagal di gpt-oss DAN Qwen3: GS-0010, GS-0014, GS-0019, GS-0020,
  GS-0021, GS-0031
- Pattern: ASP output sinyal hukum nasional kuat → model salah prediksi A (nasional
  dominan), padahal gold=B (adat berlaku)
- DeepSeek API tidak punya masalah ini (kemungkinan RLHF lebih baik untuk task legal)
- Ini adalah kandidat untuk dimasukkan ke Limitations atau Discussion paper

### 2. Ollama Ceiling ~64%
- Dua model Ollama berbeda (deepseek-r1 dan gpt-oss:20b) keduanya 45/70 = 64.29%
- Menunjukkan ceiling Ollama tanpa prompt fine-tuning per-backend
- DeepSeek API 68.57% melampaui ceiling ini

### 3. Error Rate C→B per Backend
- DeepSeek (canonical): 9/31 = 29.0%
- ASP-only: 10/31 = 32.3%
- gpt-oss:20b: 6/31 = 19.4% (terbaik!)
- Qwen3-14B: 16/31 = 51.6% (terburuk)

---

## PRIORITAS SESI BESOK

### Prioritas 1 (PALING PENTING): B3 — Rubric Refinement Log
File: docs/methodology/rubric_refinement_log.md (BELUM ADA)
Konten: dokumentasikan apa yang berubah antara:
- Batch 1 labeling Ahli-1: kappa=0.394 (24 kasus, Ahli-1 vs Ahli-2)
- Batch 2 labeling Ahli-2 baru: agreement 94.0%

PERLU INPUT OWNER: tanyakan kepada owner:
1. Apa yang berubah di rubrik antara batch 1 dan batch 2?
2. Kapan perubahan rubrik dibuat?
3. Apakah batch 2 sepenuhnya independent dari batch 1?
4. Siapa yang memutuskan perubahan rubrik?
Ini kritikal untuk reviewer Q1 — jump kappa 0.394 → 0.94 harus dijelaskan.

### Prioritas 2: Masukkan temuan cross-backend ke paper
File: paper/main.tex
Task: Tambahkan ke Discussion atau Limitations:
- B→A bias pada open-source backends (6 hard cases)
- Ollama ceiling ~64% vs DeepSeek API 68.57%
- Referensi gpt-oss:20b sebagai additional validation
- Framing: "Additional local model (gpt-oss:20b, 20B params) achieved identical
  accuracy to deepseek-r1 (64.29%), suggesting an Ollama deployment ceiling at
  current prompt formulation."

Kandidat section: Limitations §"Backend Dependence" atau Discussion sebelum Conclusion.
JANGAN ubah angka canonical di abstract/results — hanya tambah di discussion/limitations.

### Prioritas 3: Update tabel benchmark di paper
Cek apakah ada tabel yang hanya menampilkan 3 konfigurasi (ASP-only, Ollama, DeepSeek).
Pertimbangkan apakah gpt-oss:20b perlu masuk sebagai baris tambahan atau hanya
disebut di teks. McNemar tetap non-signifikan untuk semua, jadi framing "pilot
exploration" cukup.

### Prioritas 4 (jika waktu cukup): P6 — Polish Discussion section
Pastikan Discussion menghubungkan:
- Error analysis (C→B: router failure 79.3% vs prompt failure 20.7%)
- B→A bias temuan baru
- Statistical power crisis (n=70, semua p ≥ 0.17)
- Next steps yang konkret

---

## BLOCKER YANG TETAP ADA

1. Ahli-2 batch baru (FUTURE TEST set) — blocked, butuh manusia
2. Rubric refinement log (B3) — butuh input owner (TANYAKAN SEKARANG)
3. Statistical power — n=70 tidak cukup, semua McNemar non-signifikan

---

## RULES (JANGAN DILANGGAR)

1. Jangan ubah src/symbolic/rules/*.lp
2. Jangan panggil DeepSeek API tanpa persetujuan eksplisit owner
3. Hanya 1 model Ollama sekaligus (RTX 4080 16GB)
4. Setiap angka di paper harus traceable ke JSON file
5. Bahasa Indonesia untuk docs; bahasa Inggris untuk paper
6. Commit setelah setiap wave selesai
7. Jalankan git status sebelum commit — jangan commit paper/*.aux/*.bbl/*.blg/*.out
8. Test suite: python scripts/run_test_suite.py (106 tests harus passing jika ada
   perubahan code)

---

## PERINTAH PERTAMA YANG HARUS DIJALANKAN BESOK

```bash
# 1. Pastikan di root project
cd /d/documents/nusantara-agent

# 2. Pull jika ada update
git pull

# 3. Cek status
git log --oneline -5
git status

# 4. Baca handoff ini
# (sudah kamu baca)
```

Setelah itu, **tanyakan kepada owner**: apakah ada input tentang rubric refinement
(Prioritas 1), atau langsung mulai Prioritas 2 (masukkan temuan cross-backend ke paper)?
```

---

## CATATAN UNTUK OWNER (BUKAN UNTUK AI)

**Sebelum sesi besok, pikirkan jawaban untuk:**

1. **Rubric refinement**: Apa yang berubah di rubrik labeling antara batch Ahli-1
   (kappa=0.394) dan batch Ahli-2 baru (agreement 94%)? Ini akan ditanyakan reviewer Q1.

2. **gpt-oss:20b di paper**: Apakah ingin dimasukkan sebagai konfigurasi tambahan,
   atau hanya di discussion/limitations? Atau tidak sama sekali?

3. **Qwen3 negative result (F-019)**: Apakah ingin disebutkan di paper sebagai
   negative finding yang memperkuat argumen "LLM selection matters"?

4. **Timeline**: Kapan target submission draft ke co-authors/supervisor?
