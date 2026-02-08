# Rekap Human Baseline Sprint - 2026-02-08

Dokumen ini merangkum progres sprint human-only untuk mendukung `ART-050` dan `ART-064`.

## Sumber Data Sprint

1. `docs/paket_kerja_4_jam_ahli_domain_terisi_dr_hendra_2026-02-08.md` (Batch 1)
2. `docs/paket_kerja_4_jam_batch2_terisi_dr_hendra_2026-02-08.md` (Batch 2)
3. `docs/paket_kerja_4_jam_batch3_terisi_dr_hendra_2026-02-08.md` (Batch 3)
4. `docs/paket_kerja_4_jam_batch4_terisi_dr_hendra_2026-02-08.md` (Batch 4)
5. `docs/paket_kerja_4_jam_batch5_terisi_dr_hendra_2026-02-08.md` (Batch 5)
6. `docs/paket_kerja_4_jam_batch6_terisi_dr_hendra_2026-02-08.md` (Batch 6)
7. `docs/paket_kerja_4_jam_ahli2_batch1_terisi_dr_indra_2026-02-08.md` (Ahli-2 Batch 1)
8. `docs/paket_kerja_4_jam_ahli2_batch2_kalibrasi_terisi_dr_indra_2026-02-08.md` (Ahli-2 Batch 2 Kalibrasi)
9. `docs/paket_kerja_4_jam_ahli2_batch3_kalibrasi_lanjutan_terisi_dr_indra_2026-02-08.md` (Ahli-2 Batch 3 Kalibrasi Lanjutan)
10. `docs/agreement_report_ahli1_vs_ahli2_batch3_kalibrasi_lanjutan_2026-02-08.md` (Laporan agreement pasca kalibrasi batch-3)
11. `docs/paket_kerja_4_jam_ahli2_batch5_terisi_dr_indra_2026-02-08.md` (Ahli-2 Batch 5 - Ekspansi)
12. `docs/agreement_report_ahli1_vs_ahli2_batch5_2026-02-08.md` (Laporan agreement Batch 5)
16. `docs/gold_standard_consensus_report_batch1_2026-02-08.md` (Laporan Konsensus Gold Standard Batch 1)
17. `docs/paket_kerja_4_jam_ahli3_batch2_terisi_2026-02-08.md` (Ahli-3 Batch 2 - Full 82 Cases)
18. `docs/gold_standard_consensus_report_complete_82_cases_2026-02-08.md` (Laporan Konsensus Final 82 Kasus)
19. `experiments/09_ablation_study/results_phase1.json` (Hasil Benchmark AI N=22)

## Cakupan & Statistik Final

1. **Total Kasus Unik (Ground Truth): 82 kasus** (Minangkabau, Bali, Jawa, Nasional).
2. **Total Gold Standard (3-Expert Consensus): 75 kasus (91%)**.
3. **Total Split Decision (Need Expert 4): 7 kasus (9%)**.
4. **Performa AI (Baseline Exp 09):**
   - Heuristic + Local Judge: **68.18%**.
   - Integrated Multi-Agent (Current): **54.55%** (Tercatat sebagai kegagalan F-011).

## Temuan Kunci (Key Insights)

1. **Blokade HUMAN_ONLY Teratasi:** Fondasi data 82 kasus sudah sangat kuat untuk melatih model.
2. **The Intelligence Paradox:** Penambahan agen cerdas tanpa kalibrasi justru menurunkan akurasi karena "Hallucination of Conflict" (AI terlalu rajin mencari konflik norma).
3. **Bias Konteks:** Sistem saat ini terlalu "Adat-centric" dan membutuhkan penguatan pada pilar Hukum Nasional (National Law Knowledge Base).

## Tugas Tersisa (Remaining Backlog)

1. **Skalasi Data:** Menambah 118 kasus baru untuk mencapai target 200 kasus (ART-050).
2. **Resolusi Split:** Melibatkan Ahli-4 untuk 7 kasus sengketa konsensus.
3. **Prompt Tuning:** Memperbaiki Adjudicator Agent agar lebih selektif terhadap label C (Sintesis).
4. **National Retrieval:** Memperkaya `InMemoryVectorRetriever` dengan basis data UU Nasional yang lebih luas.
