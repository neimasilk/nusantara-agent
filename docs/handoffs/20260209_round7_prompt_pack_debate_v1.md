# Prompt Pack Round 7 (Debate + Voting)

Tanggal: 2026-02-09  
Baseline resmi: `B0_2026-02-09` (active N=24, offline reproducible 41.67%)

## 0) Shared Context (kirim ke semua agent)
- `docs/handoffs/20260209_codex_arxiv_go_snapshot.md`
- `docs/handoffs/20260209_round7_multi_agent_debate_framework.md`
- `docs/handoffs/20260209_round7_execution_pack.md`
- `data/benchmark_manifest.json`
- `experiments/09_ablation_study/results_post_patch_n24_offline_2026-02-09.json`
- `docs/accuracy_tuning/daily_log_2026-02-09.md`
- `docs/task_registry.md`
- `paper/main.tex`

Proposal yang wajib dinilai:
- `P1` lanjut B0
- `P2` pivot B1
- `P3` dual-track 70/30
- `P4` infra-first freeze

## 1) Prompt Claude
```text
Peran: Lead critic + decision architect.

Tugas:
1) Lakukan hard critique terhadap B0 (metodologi, risiko klaim, failure mode).
2) Nilai P1..P4 dengan cost/risk/information gain.
3) Beri rekomendasi final + trigger kondisi pivot.

Output wajib:
- docs/handoffs/20260209_claude_round7_debate_report.md
- docs/handoffs/ballots/round7/20260209_claude_round7_ballot.json

Format report wajib:
- Ringkasan 5 poin
- Top 3 Fatal Risks
- Kill Shot (1 poin paling fatal)
- Counter-Plan (1 rencana alternatif yang lebih baik)
- Keputusan: GO/HOLD/PIVOT + syarat

Constraint:
- Semua klaim harus punya evidence (file/artifact).
- Jika bukti lemah, tandai UNSUPPORTED.
```

## 2) Prompt Gemini
```text
Peran: Long-context consistency + statistical QA.

Tugas:
1) Audit konsistensi lintas dokumen terhadap baseline B0.
2) Cek validitas klaim statistik untuk P1..P4.
3) Beri rekomendasi proposal paling defensible untuk arXiv pilot.

Output wajib:
- docs/handoffs/20260209_gemini_round7_debate_report.md
- docs/handoffs/ballots/round7/20260209_gemini_round7_ballot.json

Format report wajib:
- Consistency Matrix (klaim vs bukti)
- Statistical Risk Notes
- Top 3 Fatal Risks
- Kill Shot + Counter-Plan
- Keputusan: GO/HOLD/PIVOT + syarat
```

## 3) Prompt DeepSeek
```text
Peran: Counterfactual experiment designer.

Tugas:
1) Desain minimal 2 alternatif arsitektur terhadap B0.
2) Definisikan micro-experiment 24 jam untuk uji asumsi paling kritis.
3) Nilai P1..P4 berdasarkan expected information gain.

Output wajib:
- docs/handoffs/20260209_deepseek_round7_debate_report.md
- docs/handoffs/ballots/round7/20260209_deepseek_round7_ballot.json

Format report wajib:
- 2 desain alternatif (input, proses, output, risiko)
- 24h experiment plan + acceptance criteria
- Top 3 Fatal Risks
- Kill Shot + Counter-Plan
- Keputusan: GO/HOLD/PIVOT + syarat
```

## 4) Prompt Kimi
```text
Peran: Ops reliability + execution checklist.

Tugas:
1) Ubah P1..P4 menjadi checklist eksekusi 7 hari.
2) Tandai blocker dependency yang bikin evaluasi invalid.
3) Beri runbook eksekusi reproducible yang paling aman.

Output wajib:
- docs/handoffs/20260209_kimi_round7_debate_report.md
- docs/handoffs/ballots/round7/20260209_kimi_round7_ballot.json

Format report wajib:
- Action Checklist (task/owner/deadline)
- Dependency Gate
- Risk Escalation List
- Top 3 Fatal Risks
- Keputusan: GO/HOLD/PIVOT + syarat
```

## 5) Prompt Trae (opsional)
```text
Peran: Independent verifier.

Tugas:
1) Audit bukti dari report agent lain.
2) Tandai klaim unsupported.
3) Beri vote berbasis kualitas bukti, bukan preferensi.

Output wajib:
- docs/handoffs/20260209_trae_round7_debate_report.md
- docs/handoffs/ballots/round7/20260209_trae_round7_ballot.json
```

## 6) Ballot Rules (semua agent)
- Pakai template:
  - `docs/handoffs/ballots/round7/round7_ballot_template.json`
- Vote values:
  - `approve`, `reject`, `abstain`
- Score:
  - `1` sampai `5`
- Confidence:
  - `0.0` sampai `1.0`
- Evidence:
  - wajib isi path dokumen/artifact.

## 7) Codex Tally
```powershell
python scripts/tally_round7_votes.py `
  --ballots-dir docs/handoffs/ballots/round7 `
  --output docs/handoffs/20260209_round7_vote_tally.md
```

Jika hasil seri atau gate blocker aktif:
- fallback default = `P3` selama 7 hari.
