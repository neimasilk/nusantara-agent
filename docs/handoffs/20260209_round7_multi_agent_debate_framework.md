# Round 7 Multi-Agent Debate Framework (Stuck-Breaker)

Tanggal: 2026-02-09  
Owner: Codex Integrator  
Mode: Hard-critique, evidence-first, vote-backed decision

## 1) Tujuan
- Menembus kebuntuan eksperimen tanpa tuning buta.
- Memaksa kritik keras yang dapat diaudit.
- Menghasilkan keputusan `GO / HOLD / PIVOT` berbasis bukti lintas-agent.

## 2) Peserta dan Peran
- `Claude`: Lead critic untuk kelemahan metodologi dan decision architecture.
- `Gemini`: Consistency auditor untuk konteks panjang lintas dokumen.
- `DeepSeek`: Counterfactual designer untuk alternatif arsitektur/eksperimen.
- `Kimi`: Ops enforcer untuk checklist eksekusi, dependensi, dan reproducibility.
- `Trae` (opsional): Independent verifier (audit silang, mismatch finder).
- `Human Expert`: Penilai domain non-teknis untuk keputusan substansi hukum.
- `Codex`: Integrator final, quality gate, dan penentu rencana eksekusi.

## 3) Aturan Debat (Wajib)
- Kritik keras boleh, tetapi wajib menyertakan evidence (`file` + jika bisa `line` + artifact).
- Klaim tanpa bukti ditandai `UNSUPPORTED` dan tidak dihitung sebagai argumen valid.
- Setiap agent wajib menulis:
  - `Top 3 Fatal Risks`,
  - `Kill Shot`: satu alasan paling kuat kenapa rencana utama gagal,
  - `Counter-Plan`: alternatif yang lebih murah/lebih aman.
- Dilarang menghapus guardrail klaim ilmiah.
- Dilarang klaim performa final jika belum ada held-out yang memadai.

## 4) Struktur Round
- `R0` Freeze Context (Codex, 30 menit)
  - Freeze file acuan, metrik, dan daftar proposal.
- `R1` Independent Analysis (semua agent, 60-90 menit)
  - Tiap agent kirim analisis mandiri tanpa melihat voting akhir agent lain.
- `R2` Cross-Examination (Claude, Gemini, DeepSeek; 60 menit)
  - Masing-masing wajib menyerang minimal 2 asumsi agent lain.
- `R3` Revision (semua agent, 45 menit)
  - Revisi posisi setelah kritik silang.
- `R4` Weighted Vote (semua agent, 20 menit)
  - Isi ballot JSON dengan skor, confidence, blocker.
- `R5` Final Decision Gate (Codex, 30 menit)
  - Agregasi vote + blocker + artifact check -> keputusan final.

## 5) Proposal Menu (Default)
- `P1`: Lanjut arsitektur sekarang, fokus held-out + parity offline-vs-LLM.
- `P2`: Pivot ke baseline sederhana (single-agent + symbolic verifier).
- `P3`: Dual-track 70/30 (stabilisasi utama + eksplorasi alternatif murah).
- `P4`: Infra-first freeze (berhenti tuning sampai dependency lengkap).

## 6) Aturan Voting
- Ballot format: JSON standar (lihat template).
- Nilai vote:
  - `approve`: mendukung proposal.
  - `reject`: menolak proposal.
  - `abstain`: netral.
- Skor 1-5 untuk kekuatan dukungan/penolakan.
- Confidence 0.0-1.0.
- Bobot default agent:
  - `claude=1.00`
  - `gemini=0.90`
  - `deepseek=0.80`
  - `trae=0.75`
  - `kimi=0.60`
  - `human_expert=1.00` (hanya untuk issue domain/substansi hukum)
- Global gate:
  - Jika >=2 agent high-cap (`claude/gemini/deepseek`) melaporkan blocker `HIGH` unresolved, status default proposal = `HOLD`.

## 7) File Contract
- Report per-agent (Markdown):
  - `docs/handoffs/20260209_<agent>_round7_debate_report.md`
- Ballot per-agent (JSON):
  - `docs/handoffs/ballots/round7/20260209_<agent>_round7_ballot.json`
- Tally otomatis:
  - `docs/handoffs/20260209_round7_vote_tally.md`

## 8) Acceptance Criteria Round 7
- Minimal 4 ballot valid (disarankan 5).
- Semua proposal punya skor agregat + dissent summary.
- Ada keputusan final `GO/HOLD/PIVOT` dan alasan evidence-based.
- Ada action plan 7 hari + owner + deliverable + deadline.

## 9) Anti-Deadlock Rules
- Jika voting seri atau semua `HOLD`:
  - Aktifkan fallback keputusan `P3` (dual-track 70/30) selama 7 hari.
- Jika disagreement tinggi tetapi evidence lemah:
  - Jalankan micro-experiment 24 jam untuk membunuh asumsi utama.
- Jika disagreement tinggi dan evidence kuat:
  - Ikuti proposal dengan risk-adjusted score terbaik.
