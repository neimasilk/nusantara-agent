# Codex ArXiv-Go Snapshot (2026-02-09)

## Scope
- Tujuan snapshot: menyiapkan draf preprint pilot yang reproducible dan jujur secara metodologis.
- Batas snapshot: active benchmark set (`N=24`) dengan rekonsiliasi label pasca-arbiter final.

## Data State (Frozen Snapshot)
- Active cases: `24`
- Gold label `SPLIT`: `0`
- Mismatch `gold_label` vs derived majority vote: `0`
- Expert-4 coverage: `16/24`
- Arbiter coverage: `4/24` (khusus kasus tie final)

## Key Artifacts
- Manifest terbaru: `data/benchmark_manifest.json`
- Offline benchmark artifact: `experiments/09_ablation_study/results_post_patch_n24_offline_2026-02-09.json`
- Audit script: `scripts/audit_gold_vs_votes.py`
- Patch script: `scripts/patch_gold_labels.py`
- Paper draft: `paper/main.tex`
- Paper PDF: `paper/main.pdf`

## Reproducible Metrics (Current)
- Offline reproducible accuracy (active set, forced offline): `41.67%` (`10/24`)
- Wilson 95% CI: sekitar `[24.47%, 61.17%]`
- Consensus profile: `Unanimous=4`, `Majority=20`, `Tie=0`
- Label distribution: `A=7`, `B=4`, `C=13`, `D=0`

## Verification Checklist
- [x] `python scripts/audit_gold_vs_votes.py` -> mismatch `0`, tie `0`
- [x] `python scripts/validate_benchmark_manifest.py` -> `errors=0` (warning claim 82 vs active 24 tetap ada)
- [x] `NUSANTARA_FORCE_OFFLINE=1 python experiments/09_ablation_study/run_bench_active.py --strict-manifest --output ...`
- [x] `pdflatex -output-directory=paper paper/main.tex` -> `paper/main.pdf` terbangun
- [x] Referensi paper >= 20 (saat ini 29 entri bibliography)

## Claim Guardrails (Wajib)
- Jangan klaim angka ini sebagai generalization final.
- Wajib labeli hasil sebagai `pilot`, `active set N=24`, dan `offline reproducible`.
- Klaim publikasi berbasis performa final tetap `HOLD` sampai:
  1. held-out evaluation dijalankan, dan
  2. dependency-complete rerun (clingo + fitz + mode LLM terkontrol) selesai.

## Immediate Next Steps
1. Aktivasi held-out set dari klaim 82 kasus untuk evaluasi generalisasi.
2. Jalankan benchmark LLM-mode pada label freeze yang sama untuk parity offline-vs-LLM.
3. Lengkapi environment dependencies (`clingo`, `fitz`) agar full test suite dan symbolic checks dapat dieksekusi end-to-end.
