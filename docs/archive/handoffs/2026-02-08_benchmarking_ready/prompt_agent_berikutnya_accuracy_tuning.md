# Prompt untuk Agent Berikutnya (Accuracy Tuning Phase)

Kamu melanjutkan pengembangan Nusantara-Agent pada fase **Benchmarking & Tuning**.

## Wajib Dibaca Dulu
1. `docs/archive/handoffs/2026-02-08_benchmarking_ready/handoff_gs82_and_ai_benchmark_2026-02-08.md`
2. `experiments/09_ablation_study/analysis.md` (Pola kegagalan saat ini)
3. `data/processed/gold_standard/gs_82_cases.json` (Target Gold Standard)

## Kondisi Terkini
1. **82 Kasus Gold Standard** sudah siap (Stage 1).
2. **Pipeline sudah terintegrasi** dengan Multi-Agent Orchestrator.
3. **Akurasi saat ini: 54.55%** (Turun dari 68% karena agen terlalu sering mencari konflik norma/label C).

## Tugas Prioritasmu
1. **Accuracy Recovery:**
   - Ubah logika `src/agents/orchestrator.py` agar Adjudicator lebih memihak pada sistem tunggal (A atau B) kecuali terbukti ada konflik aturan yang nyata di `rule_results`.
   - Sinkronkan ekstraksi fakta di `src/pipeline/nusantara_agent.py` dengan skema yang ada di `src/symbolic/rules/*.lp` untuk menghilangkan Clingo Warnings.
   - Jalankan ulang `python experiments/09_ablation_study/run_bench_gs82.py` dan laporkan peningkatannya.
2. **Knowledge Base Expansion:**
   - Perkaya basis data nasional di `InMemoryVectorRetriever` agar agen nasional tidak kalah debat.
3. **Data Scaling:**
   - Mulai menyusun narasi untuk 118 kasus baru (CS-083 ke atas) guna mencapai target total 200 kasus.

## Aturan Penting
1. Gunakan Bahasa Indonesia untuk dokumentasi dan analisis.
2. Patuhi `Failure Registry` dan laporkan setiap hasil negatif.
3. Jangan mengubah Gold Standard yang sudah disepakati 3 ahli tanpa alasan metodologis yang sangat kuat.
