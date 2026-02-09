# Round 7 Execution Pack (Baseline + Debate + Vote)

Tanggal: 2026-02-09  
Owner: Codex Integrator  
Goal: Ambil keputusan cepat `lanjut / pivot / dual-track` dengan bukti.

## 1) Baseline Definition (Official for Round 7)
- `B0 (Current Official Baseline)`
  - Snapshot: `2026-02-09` (post-arbiter final).
  - Dataset aktif: `N=24`, `SPLIT=0`, mismatch `gold-vs-majority=0`.
  - Metric operasional: offline reproducible `41.67% (10/24)`.
  - Artifact: `experiments/09_ablation_study/results_post_patch_n24_offline_2026-02-09.json`.
- `B1 (Simple Comparator)`
  - Single-agent + symbolic verifier.
  - Tujuan: cek apakah arsitektur kompleks benar-benar memberi nilai tambah.
- `B2 (Minimal Comparator)`
  - Retrieval-first/rule-first sederhana.
  - Tujuan: lower-bound baseline untuk sanity check.

## 2) Round 7 Decision Proposals
- `P1`: Lanjutkan arsitektur saat ini, fokus held-out + parity offline-vs-LLM.
- `P2`: Pivot ke baseline sederhana (B1) sebagai kandidat utama.
- `P3`: Dual-track 70/30 selama 7 hari (B0 stabilisasi + B1/B2 eksplorasi).
- `P4`: Infra-first freeze (stop tuning sampai dependency lengkap).

## 3) Prompt Kirim ke Tiap Agent

### Claude (Critical Strategist)
```text
Peran: Red-team lead untuk keputusan arsitektur.
Tugas:
1) Serang asumsi utama B0 dan tunjukkan failure mode paling fatal.
2) Nilai P1..P4 dengan cost/risk/gain.
3) Beri rekomendasi final + trigger condition kapan harus pivot.
Wajib output:
- docs/handoffs/20260209_claude_round7_debate_report.md
- docs/handoffs/ballots/round7/20260209_claude_round7_ballot.json
Aturan:
- Semua kritik wajib evidence (file + angka).
- Sertakan Kill Shot + Counter-Plan.
```

### Gemini (Consistency + Statistical Auditor)
```text
Peran: Auditor konsistensi lintas dokumen + kekuatan statistik.
Tugas:
1) Audit konsistensi klaim B0 terhadap manifest/log/paper.
2) Evaluasi apakah P1..P4 valid secara metodologi.
3) Tandai mismatch dan risiko overclaim.
Wajib output:
- docs/handoffs/20260209_gemini_round7_debate_report.md
- docs/handoffs/ballots/round7/20260209_gemini_round7_ballot.json
Aturan:
- Fokus coherence, traceability, confidence interval, dan claim gate.
```

### DeepSeek (Counterfactual Designer)
```text
Peran: Perancang alternatif murah dengan efek paling besar.
Tugas:
1) Usulkan minimal 2 desain alternatif terhadap B0.
2) Beri micro-experiment 24 jam untuk membunuh asumsi utama.
3) Nilai P1..P4 dari sudut expected information gain.
Wajib output:
- docs/handoffs/20260209_deepseek_round7_debate_report.md
- docs/handoffs/ballots/round7/20260209_deepseek_round7_ballot.json
Aturan:
- Hindari opini umum; beri design + acceptance criteria terukur.
```

### Kimi (Ops Reliability)
```text
Peran: Eksekutor checklist, reproducibility, dan dependency gate.
Tugas:
1) Turunkan P1..P4 menjadi checklist operasional 7 hari.
2) Tandai dependency blocker yang membuat eksperimen invalid.
3) Verifikasi semua command dapat dieksekusi berurutan.
Wajib output:
- docs/handoffs/20260209_kimi_round7_debate_report.md
- docs/handoffs/ballots/round7/20260209_kimi_round7_ballot.json
Aturan:
- Jangan klaim performa model; fokus eksekusi dan risiko operasional.
```

### Trae (Independent Verifier, Optional)
```text
Peran: Verifikator independen untuk audit silang.
Tugas:
1) Cek apakah argumentasi agent lain didukung artefak nyata.
2) Tandai klaim unsupported.
3) Beri vote netral-keras berdasarkan kualitas bukti.
Wajib output:
- docs/handoffs/20260209_trae_round7_debate_report.md
- docs/handoffs/ballots/round7/20260209_trae_round7_ballot.json
```

## 4) File Input Wajib untuk Semua Agent
- `docs/handoffs/20260209_codex_arxiv_go_snapshot.md`
- `docs/handoffs/20260209_round7_multi_agent_debate_framework.md`
- `data/benchmark_manifest.json`
- `experiments/09_ablation_study/results_post_patch_n24_offline_2026-02-09.json`
- `docs/accuracy_tuning/daily_log_2026-02-09.md`
- `docs/task_registry.md`
- `paper/main.tex`

## 5) SLA Round 7
- R1 analysis: 90 menit
- R2 cross-exam: 60 menit
- R3 revision + ballot: 45 menit
- Integrator tally + decision: 30 menit

## 6) Tally Command (Codex)
Gunakan setelah minimal 4 ballot masuk:

```powershell
python scripts/tally_round7_votes.py `
  --ballots-dir docs/handoffs/ballots/round7 `
  --output docs/handoffs/20260209_round7_vote_tally.md
```

## 7) Decision Gate
- Jika >=2 high-cap agents (`claude/gemini/deepseek`) melaporkan blocker `HIGH` unresolved:
  - proposal status default = `HOLD`.
- Jika tidak ada proposal clear winner:
  - fallback ke `P3` selama 7 hari.
- Semua keputusan wajib sertakan:
  - alasan,
  - bukti,
  - next action 7 hari (owner + due date + output).
