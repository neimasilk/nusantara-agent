# Handoff Singkat — Offline Interview Pipeline Hardening (2026-02-08)

## Konteks Terakhir

Fokus sesi ini adalah menguatkan workflow **offline-first** untuk:
1. menjaga kualitas governance benchmark,
2. menyiapkan interview ahli hukum non-teknis (pen-and-paper / PDF),
3. memastikan ingest hasil interview ke dataset berjalan aman dan audit-friendly.

## Keputusan Penting

1. Benchmark aktif dinormalisasi ke dataset netral: `data/processed/gold_standard/gs_active_cases.json`.
2. Runner benchmark dibuat manifest-aware dan memiliki mode `--strict-manifest`.
3. Interview ahli non-teknis diprioritaskan via dokumen print-ready, lalu operator teknis melakukan ingest.
4. Manifest benchmark kini bisa direbuild otomatis (tanpa edit manual).
5. Mode biaya API tetap hemat: tidak perlu DeepSeek/Kimi untuk workflow ini.

## Asumsi Aktif

1. Dataset aktif saat ini berisi 24 entri, 22 evaluable (exclude `SPLIT`).
2. Dokumen klaim referensi masih menyatakan 82 kasus, sehingga validasi strict referensi akan fail sampai disinkronkan.
3. `review.md` memang dihapus secara sengaja oleh user (bukan kehilangan artefak tak sengaja).

## Status Milestone

1. Deterministic tests: **79/79 pass** (`python scripts/run_test_suite.py`).
2. Benchmark manifest validator: pass (warning mismatch referensi).
3. Workflow interview siap operasi:
   - export template split,
   - ingest hasil interview,
   - rebuild manifest,
   - validate manifest.
4. Dokumen print-ready untuk ahli hukum sudah tersedia.

## Risiko yang Diketahui

1. **Reference claim mismatch** (82 vs 24 aktif) masih terbuka.
2. Baseline ablation fairness masih perlu perbaikan lanjutan (B1-B5) agar defensible untuk klaim paper.
3. Jika ingest dilakukan `--in-place` tanpa verifikasi, risiko overwrite data tetap ada (mitigasi: default output file baru).

## Langkah Berikutnya (Direkomendasikan)

1. Jalankan interview Ahli-4 untuk menutup kasus split menggunakan paket print-ready.
2. Ingest hasil interview ke dataset aktif dan rebuild manifest.
3. Sinkronkan dokumen klaim 82 kasus agar lolos `--require-reference-match`.
4. Lanjut rehab baseline ablation agar non-strawman.

## Prompt Singkat untuk Agen Selanjutnya

```text
Lanjutkan dari workflow offline interview yang sudah disiapkan.
1) Baca docs/handoffs/20260208_offline_interview_pipeline_handoff.md dan docs/human_only/workflow/interview_online_workflow.md.
2) Prioritas: ingest hasil Ahli-4 dari template CSV ke gs_active_cases.json, lalu rebuild+validate manifest.
3) Setelah itu sinkronkan klaim dokumentasi yang masih menyebut 82 kasus pada konteks benchmark aktif.
4) Jangan gunakan API berbayar kecuali blocker kritis dan ada persetujuan eksplisit user.
```
