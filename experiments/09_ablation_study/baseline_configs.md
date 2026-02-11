# Baseline Configurations (Exp 09)

Dokumen ini mendefinisikan 8 baseline secara reproduksibel.

## Konvensi Umum

1. Jalankan dari project root.
2. Input query: string hukum Indonesia.
3. Output: JSON berisi `baseline_id`, `query`, `jawaban`, dan metadata komponen aktif.
4. Eksekusi batch ART-065 gunakan:
   - `python experiments/09_ablation_study/run_all_baselines.py --mode operational_offline`
5. Analisis statistik ART-066 gunakan:
   - `python experiments/09_ablation_study/statistical_analysis.py --results-dir experiments/09_ablation_study/results --reference-baseline B5`
6. Rule files default:
   1. `src/symbolic/rules/nasional.lp`
   2. `src/symbolic/rules/minangkabau.lp`
   3. `src/symbolic/rules/bali.lp`
   4. `src/symbolic/rules/jawa.lp`

## B1 — DeepSeek Direct Prompting

1. File: `experiments/09_ablation_study/baselines/b1_direct_prompting.py`
2. Komponen aktif:
   1. LLM direct answer (tanpa retrieval, tanpa rule engine).
3. Komponen non-aktif:
   1. Graph retrieval
   2. Vector retrieval
   3. Rule engine
   4. Debate

## B2 — DeepSeek + Vector RAG (No Graph)

1. File: `experiments/09_ablation_study/baselines/b2_vector_rag.py`
2. Komponen aktif:
   1. Vector retrieval
   2. Synthesis jawaban dari konteks vector
3. Komponen non-aktif:
   1. Graph retrieval
   2. Rule engine
   3. Debate

## B3 — DeepSeek + Graph Retrieval (No Vector)

1. File: `experiments/09_ablation_study/baselines/b3_graph_only.py`
2. Komponen aktif:
   1. Graph retrieval
   2. Synthesis jawaban dari konteks graph
3. Komponen non-aktif:
   1. Vector retrieval
   2. Rule engine
   3. Debate

## B4 — Full Pipeline sans Rule Engine

1. File: `experiments/09_ablation_study/baselines/b4_no_rules.py`
2. Komponen aktif:
   1. Router
   2. Graph retrieval
   3. Vector retrieval
3. Komponen non-aktif:
   1. Rule engine (semua domain)
   2. Debate

## B5 — Full Pipeline sans Debate

1. File: `experiments/09_ablation_study/baselines/b5_no_debate.py`
2. Komponen aktif:
   1. Router
   2. Graph retrieval
   3. Vector retrieval
   4. Rule engine lintas domain
3. Komponen non-aktif:
   1. Debate

## B6 — GPT-4 + Same Pipeline

1. File: `experiments/09_ablation_study/baselines/b6_gpt4_pipeline.py`
2. Komponen aktif:
   1. Full pipeline (router + retrieval + rules)
   2. Synthesis oleh GPT-4 (jika API tersedia)
3. Fallback:
   1. Jika API tidak tersedia, fallback ke synthesis lokal deterministik.

## B7 — Claude + Same Pipeline

1. File: `experiments/09_ablation_study/baselines/b7_claude_pipeline.py`
2. Komponen aktif:
   1. Full pipeline (router + retrieval + rules)
   2. Synthesis oleh Claude (jika API tersedia)
3. Fallback:
   1. Jika API tidak tersedia, fallback ke synthesis lokal deterministik.

## B8 — Human Expert Baseline

1. Executor: HUMAN_ONLY.
2. Komponen aktif:
   1. Analisis manusia tanpa bantuan AI.
3. Komponen non-aktif:
   1. Seluruh modul AI.
