# Handoff Prompt — Nusantara-Agent (2026-02-07, v2)

Kamu melanjutkan pekerjaan di repositori riset ilmiah **Nusantara-Agent** (Neuro-Symbolic Agentic GraphRAG untuk penalaran hukum pluralistik Indonesia). Target: publikasi Scopus Q1.

## Baca Dulu (Wajib)
1. `CLAUDE.md`
2. `docs/methodology_fixes.md`
3. `docs/task_registry.md`
4. `docs/failure_registry.md`
5. `docs/readiness_audit_exp06_exp09_exp10_2026-02-07.md`

## State Terkini (Sinkron 2026-02-07)
- Exp 01-05: selesai. Exp 05 menemukan divergensi Rule Engine vs LLM 33.3% (N=30).
- Exp 07: selesai dengan hasil negatif. Advanced orchestration belum mengungguli baseline sequential pada auto-score Kimi (N=12), dengan overhead token dan waktu signifikan.
- Tracking token: terintegrasi via `src/utils/token_usage.py`.
- Dokumentasi eksperimen: PROTOCOL.md, REVIEW.md, analysis.md tersedia.

## Prioritas Aktif

### Prioritas 1 — Exp 06 (Independent Evaluation Pipeline)
- Status utama: `ART-031` masih `BLOCKED`.
- Dependency aktual:
  - `ART-025`: **DONE** (`data/annotation/guidelines.md`, `data/annotation/schema.json` sudah ada).
  - `ART-029`: **DONE** (independent LLM evaluator).
  - `ART-028`: **PENDING** (human annotation 200 paragraf).
  - `ART-030`: **PENDING** (putusan MA sebagai external ground truth).
- Fokus eksekusi berikutnya: dorong `ART-028` dan `ART-030`.

### Prioritas 2 — Iterasi Exp 07 (Debate Protocol Improvement)
- Temuan negatif: debat menurunkan completeness tanpa evidence baru.
- Hipotesis perbaikan: debat harus punya akses retrieval evidence baru, bukan hanya transformasi konteks.
- Belum ada ART khusus iterasi ini; perlu dekomposisi ART baru sebelum coding besar.

### Prioritas 3 — Scaling (ART-032 s.d. ART-038)
- Status: pengumpulan korpus lintas domain masih tertinggal.
- Target skala: 10K+ triples, 200+ test cases, 3 domain (Minangkabau, Bali, Jawa).

### Prioritas 4 — Exp 09 & Exp 10
- Exp 09 tetap blocked oleh `ART-049` dan turunan baseline.
- Exp 10 tetap blocked oleh `ART-068/069/070`.

## Konvensi Wajib
- Bahasa Indonesia untuk variabel, prompt, dokumentasi.
- Semua eksperimen wajib punya `PROTOCOL.md`, `REVIEW.md`, `analysis.md`.
- Kegagalan wajib dicatat di `docs/failure_registry.md`.
- Hindari klaim normatif/self-congratulatory; gunakan bahasa evidence-based.
- Jangan gunakan DeepSeek untuk mengevaluasi output DeepSeek.
- Jalankan eksperimen dari root repo.

## File Kunci
- Orchestrator: `src/agents/orchestrator.py`
- Debate: `src/agents/debate.py`
- Self-correction: `src/agents/self_correction.py`
- Rule engine: `src/symbolic/rule_engine.py`, `src/symbolic/rules/minangkabau.lp`
- Token utils: `src/utils/token_usage.py`
- Exp 07 runner: `experiments/07_advanced_orchestration/run_experiment.py`
- Exp 07 baseline: `experiments/07_advanced_orchestration/run_baseline_exp03.py`
- Exp 07 scoring: `experiments/07_advanced_orchestration/eval_scores.py`

## Catatan untuk LLM Tujuan (anti-error)
- Perlakukan `docs/task_registry.md` sebagai sumber status utama jika ada konflik dengan teks handoff.
- Jika menemukan konflik status, laporkan konflik dengan referensi file + lanjutkan dari status paling mutakhir.
- Jangan ubah status task tanpa menyebut evidence artefak yang ada.
