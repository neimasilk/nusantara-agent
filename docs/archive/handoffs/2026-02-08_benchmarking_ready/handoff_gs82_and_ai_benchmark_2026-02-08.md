# HANDOFF: Gold Standard Established & AI Benchmarking Started

Tanggal: 2026-02-08  
Branch: `main`  
Repo: `nusantara-agent`

## Ringkasan Eksekutif

1. **Human Baseline (Stage 1) SELESAI:** Kita telah mencapai target 82 kasus unik dengan triangulasi 3 ahli independen. 75 kasus (91%) telah memiliki label Gold Standard tetap.
2. **Pipeline Upgrade:** `NusantaraAgentPipeline` kini telah terintegrasi dengan `parallel_orchestrator` (Multi-Agent System). Rule Engine, Retrieval, dan LLM Synthesis berjalan dalam satu alur terpadu.
3. **Hasil Benchmark AI Tahap 1:**
   - Heuristic Method: 68.18% Accuracy.
   - Multi-Agent Integrated: 54.55% Accuracy (F-011).
   - Masalah: Hallucination of conflict dan bias kontekstual adat yang terlalu kuat.

## Artefak Kunci yang Sudah Ada

1. **Data Gold Standard:** `data/processed/gold_standard/gs_82_cases.json`
2. **Evaluator Script:** `experiments/09_ablation_study/run_bench_gs82.py`
3. **Analisis Terkini:** `experiments/09_ablation_study/analysis.md`
4. **Registry Kegagalan:** `docs/failure_registry.md` (Lihat F-011).

## Status ART Terkait

- **ART-064 (Human Baseline):** DONE untuk Tahap 1 (82 kasus).
- **ART-050 (Test Cases):** IN_PROGRESS (82/200 kasus).
- **ART-049 (Full Pipeline Integration):** DONE (Sudah integrasi agen cerdas).
- **ART-065 (Run Baselines):** IN_PROGRESS (Benchmark Phase 1 sudah jalan).

## Prioritas untuk Agent Berikutnya

1. **Perbaikan Akurasi (The Accuracy Recovery):**
   - Refactor `src/agents/orchestrator.py` agar lebih selektif.
   - Perkaya `InMemoryVectorRetriever` di `src/pipeline/nusantara_agent.py` dengan data hukum nasional (KUHPerdata, KHI, UU terbaru).
   - Sinkronkan fakta simbolik yang masih memicu Clingo Warnings.
2. **Resolusi Split Kasus:** Siapkan paket 7 kasus split untuk **Ahli-4**.
3. **Skalasi Kasus:** Draft 118 kasus baru (CS-083 s.d. CS-200) menggunakan aturan yang tersedia di `data/rules/*.json`.

## Catatan Operasional

- Jalankan benchmark dengan: `python experiments/09_ablation_study/run_bench_gs82.py`.
- Gunakan `CLAUDE.md` sebagai panduan konvensi koding dan bahasa (Bahasa Indonesia).
- Hindari penggunaan label C (Sintesis) yang berlebihan oleh agen.
