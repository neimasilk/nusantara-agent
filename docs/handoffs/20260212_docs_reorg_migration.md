# Handoff Reorganisasi Dokumen — 2026-02-12

## Tujuan

Menata ulang dokumentasi yang tersebar lintas sesi multi-agent agar:
1. owner bisa fokus ke jalur HUMAN_ONLY tanpa kehilangan konteks,
2. referensi lintas dokumen tetap valid,
3. struktur dokumen lebih sederhana dan stabil.

## Keputusan Struktur

1. Root `docs/` dipertahankan untuk dokumen governance/metodologi inti.
2. Seluruh artefak HUMAN_ONLY dipindahkan ke:
   - `docs/human_only/artifacts/`
3. Seluruh panduan workflow HUMAN_ONLY dipindahkan ke:
   - `docs/human_only/workflow/`
4. Peta migrasi path lama -> baru disimpan di:
   - `docs/human_only/reorg_map_2026-02-12.csv`

## Cakupan Migrasi

1. Total file dipindahkan: 63 file.
2. Kelompok file:
   - `agreement_report_*`
   - `gold_standard_consensus_report_*`
   - `paket_*` (kerja/interview/arbitrase)
   - `lembar_kerja_*`
   - `rekap_human_baseline_*`
   - `keputusan_ahli_final.md`
   - `human_only_register_82_master_v0_2026-02-12.csv`
   - workflow docs (`panduan`, `interview_online_workflow`, `operator_transkrip`, `template_pen_paper`)

## Perubahan Referensi

1. Referensi path lama pada dokumen, script, dan manifest diupdate ke lokasi baru.
2. `scripts/rebuild_benchmark_manifest.py` default reference-claim kini menunjuk:
   - `docs/human_only/artifacts/gold_standard_consensus_report_complete_82_cases_2026-02-08.md`
3. `data/benchmark_manifest.json` juga sudah menunjuk path baru yang sama.

## Dokumen Entry Point Baru

1. `docs/README.md` (hub dokumentasi utama)
2. `docs/human_only/README.md` (hub jalur HUMAN_ONLY)
3. `docs/handoffs/20260212_human_only_context_reset.md` (reset konteks 82 vs 24)

## Catatan Safety

1. Tidak ada dokumen yang dihapus permanen pada migrasi ini.
2. Migrasi fokus pada relokasi dan sinkronisasi referensi.
3. Semua perubahan mengikuti prinsip: simple is better, but not simpler.
