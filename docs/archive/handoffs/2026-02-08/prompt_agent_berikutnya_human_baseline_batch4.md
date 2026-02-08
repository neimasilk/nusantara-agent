# Prompt untuk Agent Berikutnya (Copy-Paste)

Kamu melanjutkan pekerjaan human-only baseline pada `ART-064`.

## Wajib dibaca dulu
1. `docs/archive/handoffs/2026-02-08/handoff_human_baseline_progress_batch4_ready_2026-02-08.md`
2. `CLAUDE.md`
3. `docs/task_registry.md`
4. `docs/rekap_human_baseline_sprint_2026-02-08.md`

## State saat ini
1. Ahli-1 tetap 72 kasus.
2. Ahli-2 sudah masuk sampai Batch-3 kalibrasi lanjutan.
3. Trend agreement literal Ahli-1 vs Ahli-2 (12 kasus):
   - Batch-1: 33.3%
   - Batch-2: 50.0%
   - Batch-3: 58.3%
4. Handout berikutnya sudah siap:
   - `docs/paket_kerja_4_jam_ahli2_batch4_kalibrasi_mikro_ready_to_handout.md`

## Tugas prioritasmu
1. Begitu hasil Ahli-2 Batch-4 masuk:
   - simpan dokumen terisi ke file `.md` baru di `docs/`.
   - buat/update report agreement batch-4.
   - hitung ulang agreement label literal.
   - berikan rekomendasi gerbang: onboarding Ahli-3 atau kalibrasi mikro tambahan.
2. Update dokumen tracking:
   - `docs/rekap_human_baseline_sprint_2026-02-08.md`
   - `docs/task_registry.md` (progress note ART-064)
3. Commit dan push setiap batch selesai.

## Aturan penting
1. Pertahankan format handout 4 jam yang self-contained.
2. Bahasa Indonesia untuk dokumentasi.
3. Jika hanya ubah dokumen (tanpa kode), tidak perlu pytest.
4. Jangan commit `.claude/settings.local.json`.
