# Docs Hub

Tanggal pembaruan: 2026-02-12

Dokumen proyek sempat tersebar lintas sesi multi-agent. Mulai tanggal ini, pintu masuk dokumen disederhanakan.

## Start Here

1. Registry tugas riset: `docs/task_registry.md`
2. SOP eksperimen: `docs/experiment_template.md`
3. Protokol review: `docs/review_protocol.md`
4. Framework testing: `docs/testing_framework.md`
5. Catatan failure: `docs/failure_registry.md`

## Human-Only Track (Owner Focus)

1. Entry point human-only: `docs/human_only/README.md`
2. Context reset 82 vs 24: `docs/handoffs/20260212_human_only_context_reset.md`
3. Register master 82 kasus: `docs/human_only/artifacts/human_only_register_82_master_v0_2026-02-12.csv`

## Struktur Direktori Utama

1. `docs/human_only/`
   1. `artifacts/`: semua paket kerja, agreement report, consensus report, dan output human-only.
   2. `workflow/`: panduan operasional non-teknis human-only.
   3. `reorg_map_2026-02-12.csv`: peta migrasi path lama ke path baru.
2. `docs/handoffs/`: handoff aktif lintas sesi.
3. `docs/archive/`: arsip historis.

## Aturan Dokumentasi Baru

1. Hindari menaruh dokumen human-only baru di root `docs/`; simpan di `docs/human_only/artifacts/` atau `docs/human_only/workflow/`.
2. Setiap dokumen status wajib menyebut `as_of_date` dan basis dataset (`human evidence pool 82` atau `active set 24`).
3. Jika ada perubahan lokasi file, update referensi dan catat di `docs/human_only/reorg_map_2026-02-12.csv` atau handoff terbaru.
