# Round 7 R2 Execution Prompts (Post-Decision)

Tanggal: 2026-02-09  
Context: Keputusan resmi Round 7 adalah `HOLD` dengan urutan eksekusi `P4 -> P3`.

## Shared Rules (Kirim ke semua agent)
- Tidak ada debat strategi baru di R2.
- Fokus: tutup blocker dan hasilkan artefak yang bisa diaudit.
- Semua klaim wajib evidence path.
- Jangan ubah ulang voting R1.

## Shared Context Files
- `docs/handoffs/20260209_round7_final_decision_no_trae.md`
- `docs/handoffs/20260209_round7_vote_tally_no_trae.md`
- `docs/handoffs/20260209_codex_arxiv_go_snapshot.md`
- `data/benchmark_manifest.json`
- `docs/accuracy_tuning/daily_log_2026-02-09.md`
- `docs/task_registry.md`

---

## Prompt Kimi (Infra Execution)
```text
R2 Execution - Infra Closure.

Tugas:
1) Tutup blocker dependency (clingo, fitz/pymupdf, langchain_openai, langgraph).
2) Beri verification table: module -> import OK/FAIL.
3) Jalankan smoke checks dan catat output ringkas.
4) Mapping blocker status: resolved true/false + alasan.

Output:
- docs/handoffs/20260209_kimi_round7_r2_infra_execution.md

Format minimum:
- Environment info
- Command list (copy-paste ready)
- Verification matrix
- Blocker closure report
- Remaining risks
```

## Prompt Claude (Gate QA)
```text
R2 Execution - QA Gate.

Tugas:
1) Audit report eksekusi Kimi.
2) Putuskan gate PASS/FAIL untuk transisi HOLD -> GO-P3.
3) Jika FAIL: tulis blocker yang tersisa dan requirement exact.
4) Jika PASS: keluarkan run-order parity benchmark yang aman.

Output:
- docs/handoffs/20260209_claude_round7_r2_gate_decision.md

Format minimum:
- Gate decision: PASS/FAIL
- Evidence table
- Hard blockers (jika ada)
- Next executable steps
```

## Prompt Gemini (Method Sync)
```text
R2 Execution - Methodology and Claim Sync.

Tugas:
1) Sinkronkan guardrails klaim dengan status terbaru.
2) Konsistenkan CI/method notes (Wilson, asumsi kelas, ukuran sampel).
3) Buat patch notes dokumen yang harus diupdate setelah gate result.

Output:
- docs/handoffs/20260209_gemini_round7_r2_method_sync.md

Format minimum:
- Consistency check table
- Claim guardrail updates
- Required doc patches (prioritas)
```

## Prompt DeepSeek (Kill-Test Ready Plan)
```text
R2 Execution - Kill-Test Preparation.

Tugas:
1) Finalkan 24h kill-test plan (A/B) yang siap run setelah gate PASS.
2) Definisikan acceptance criteria numerik GO/PIVOT.
3) Definisikan minimal artifacts agar hasil bisa diaudit.

Output:
- docs/handoffs/20260209_deepseek_round7_r2_killtest_plan.md

Format minimum:
- Experiment matrix
- Run steps
- Metrics + thresholds
- Decision mapping
```

## Prompt Trae (Opsional, Independent Verify)
```text
R2 Execution - Independent Verification.

Tugas:
1) Verifikasi independen hasil Kimi dan keputusan gate Claude.
2) Tandai klaim unsupported.
3) Beri verdict singkat: trusted / needs recheck.

Output:
- docs/handoffs/20260209_trae_round7_r2_verification.md
```
