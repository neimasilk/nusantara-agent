# Round 7 R3 Prompt Pack: Topic Stable, Solution Re-Explore

Tanggal: 2026-02-09  
Coordinator: Codex  
Prinsip: topik tetap (hukum adat vs nasional), metode dipertandingkan ulang berbasis data.

## Shared Context (Wajib untuk semua agent)
- `docs/handoffs/20260209_round7_final_decision_no_trae.md`
- `docs/handoffs/20260209_round7_vote_tally_no_trae.md`
- `docs/handoffs/20260209_claude_round7_r2_gate_decision.md`
- `docs/handoffs/20260209_kimi_round7_r2_infra_execution.md`
- `docs/handoffs/20260209_gemini_round7_r2_method_sync.md`
- `docs/handoffs/20260209_deepseek_round7_r2_killtest_plan.md`
- `experiments/09_ablation_study/results_post_patch_n24_offline_2026-02-09.json`
- `experiments/09_ablation_study/results_full_pipeline_n24_parity_2026-02-09.json`
- `paper/main.tex`

## Known Facts (Jangan diubah)
- Offline proxy: `10/24 = 41.67%`
- Full pipeline parity: `13/24 = 54.17%`
- Delta: `+3 case`, `+12.5pp`
- Test suite: `79/79` pass
- Status: `GO-P3-READY` (dengan guardrails klaim tetap aktif)

---

## Prompt Claude (Architecture Decision + Comparator Design)
```text
Peran: Decision Architect.

Misi:
1) Tetapkan kerangka keputusan "tetap kompleks vs sederhanakan" berbasis data, bukan preferensi.
2) Rancang comparator benchmark yang adil untuk B1/B2/B3 pada dataset N=24 yang sama.
3) Definisikan GO/HOLD/PIVOT gate final untuk 7 hari ke depan.

Keluaran wajib:
- docs/handoffs/20260209_claude_round7_r3_architecture_decision.md

Format wajib:
- Ringkasan 5 poin
- Decision matrix: Full pipeline vs B1/B2/B3 (cost, risk, expected signal)
- Kriteria menang/kalah numerik (bukan narasi)
- 7-day execution gate dengan acceptance criteria

Batasan:
- Tidak boleh klaim generalisasi publik.
- Wajib bedakan "pilot signal" vs "paper claim".
```

## Prompt Gemini (Narrative Reframe + Claim Safety)
```text
Peran: Methodology & Paper Consistency Auditor.

Misi:
1) Reframe narasi paper: masalah tetap sama, metode dieksplor ulang secara terkontrol.
2) Sinkronkan semua guardrails agar tidak overclaim.
3) Siapkan patch text untuk bagian abstract/introduction/limitations/conclusion.

Keluaran wajib:
- docs/handoffs/20260209_gemini_round7_r3_paper_reframe.md

Format wajib:
- Claim policy table: Allowed vs Forbidden
- Patch snippets siap tempel untuk paper/main.tex
- Risk notes untuk reviewer (N kecil, held-out belum aktif, parity baru tersedia)

Batasan:
- Jangan mengubah angka tanpa artifact.
- Jangan menyamakan pilot metric dengan final metric.
```

## Prompt Kimi (Execution Ops for P3)
```text
Peran: Ops Execution Owner.

Misi:
1) Ubah P3 menjadi runbook 7 hari yang benar-benar bisa dieksekusi.
2) Breakdown task harian: owner, command, output file, pass/fail check.
3) Prioritaskan pekerjaan yang memberi sinyal keputusan tercepat.

Keluaran wajib:
- docs/handoffs/20260209_kimi_round7_r3_execution_runbook.md

Format wajib:
- Day-by-day plan (D1..D7)
- Command checklist (copy-paste)
- Artifact checklist (required/optional)
- Escalation rules jika command gagal

Batasan:
- Tidak membahas strategi tingkat tinggi.
- Fokus eksekusi, dependency, dan reproducibility.
```

## Prompt DeepSeek (Alternative Solution Tracks)
```text
Peran: Counterfactual Solution Designer.

Misi:
1) Usulkan 2 jalur simplifikasi metode tanpa mengubah topik riset.
2) Update kill-test threshold menggunakan baseline aktual full pipeline (54.17%), bukan 41.67%.
3) Definisikan kapan harus PIVOT ke metode lebih sederhana.

Keluaran wajib:
- docs/handoffs/20260209_deepseek_round7_r3_solution_tracks.md

Format wajib:
- Track-S (simplified): single-agent + verifier
- Track-M (moderate): light multi-agent
- Threshold numerik per track:
  - keep
  - hold
  - pivot
- Daftar artifact untuk audit

Batasan:
- Jangan pakai threshold dari data lama yang tidak konsisten.
- Wajib refer ke `results_full_pipeline_n24_parity_2026-02-09.json`.
```
