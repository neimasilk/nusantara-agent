# Prompt untuk Agent Berikutnya (Copy-Paste)

Kamu melanjutkan pekerjaan dari agent sebelumnya.

## Wajib dibaca dulu
1. `docs/archive/handoffs/2026-02-08/handoff_human_baseline_progress_2026-02-08.md`
2. `CLAUDE.md`
3. `docs/task_registry.md`

## Ringkasan state saat ini
1. ART-040/041/042 DONE (Bali/Jawa/Nasional ASP rules).
2. ART-049 DONE (unified pipeline di `src/pipeline/nusantara_agent.py`).
3. ART-056 s.d. ART-063 DONE (baseline ablation scripts sudah ada).
4. Human baseline ongoing:
   1. Ahli-1 (Dr. Hendra) sudah 72 kasus.
   2. Ahli-2 (Dr. Indra) batch-1 sudah masuk.
   3. Agreement awal ahli-1 vs ahli-2: 33.3% (lihat agreement report).
5. Kalibrasi ahli-2 batch-2 sudah siap handout:
   1. `docs/paket_kerja_4_jam_ahli2_batch2_kalibrasi_ready_to_handout.md`

## Tugas prioritasmu
1. Begitu hasil ahli-2 batch-2 masuk:
   1. dokumentasikan hasil terisi ke file `.md` baru di `docs/`,
   2. update `docs/agreement_report_ahli1_vs_ahli2_batch1_2026-02-08.md` (atau buat versi v2 jika lebih rapi),
   3. hitung ulang agreement label literal,
   4. tulis rekomendasi: lanjut ahli-2 batch-3 atau mulai onboarding ahli-3.
2. Update progress note di:
   1. `docs/rekap_human_baseline_sprint_2026-02-08.md`
   2. `docs/task_registry.md`
3. Commit dan push setiap batch yang selesai.

## Aturan penting
1. Pertahankan format self-contained handout 4 jam.
2. Bahasa Indonesia untuk dokumentasi.
3. Jalankan `python -m pytest tests/ -v` jika ada perubahan kode.
4. Jangan commit `.claude/settings.local.json`.

