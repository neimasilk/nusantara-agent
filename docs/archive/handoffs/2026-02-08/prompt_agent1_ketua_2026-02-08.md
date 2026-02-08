# Prompt untuk Agent 1 (Ketua) — Sinkronisasi Paralel

Peran kamu: **Ketua koordinasi** untuk 3 agent yang bekerja paralel pada repo `nusantara-agent`.

## Tujuan sprint saat ini

Selesaikan P1 sinkronisasi dokumentasi yang masih tertinggal, dengan aturan:

1. Jangan ubah file `test_*.py`.
2. Jangan klaim `HUMAN_ONLY` selesai tanpa evidence.
3. Jangan ubah angka hasil eksperimen historis.
4. Jangan hapus audit trail.

## Status dari Agent 3 (selesai)

1. Agent 3 sudah audit dependency dan menambahkan catatan di:
   - `docs/task_registry.md` (`ART-021`, `ART-022`)  
   bahwa keduanya `DONE` tetapi masih bergantung ke `ART-020 (IN_PROGRESS)`.
2. Laporan lengkap Agent 3 ada di:
   - `docs/archive/handoffs/2026-02-08/agent3_p1_sync_report_2026-02-08.md`
3. Test suite wajib sudah dijalankan oleh Agent 3:
   - `python scripts/run_test_suite.py` => **FAILED** (existing issues code, bukan perubahan docs Agent 3).

## Tugas ketua (kamu)

1. Konsolidasikan output Agent 2 + Agent 3 ke satu narasi status yang konsisten lintas:
   - `CLAUDE.md` (Current State),
   - `docs/task_registry.md`,
   - `docs/testing_framework.md`,
   - `docs/methodology_fixes.md`.
2. Putuskan policy dependency mismatch:
   - Opsi A: status `ART-021/022` disesuaikan;
   - Opsi B: tetap `DONE` dengan guardrail audit note + penjelasan milestone verifikasi human di `ART-020`.
3. Siapkan final report tunggal (format wajib):
   - ringkasan masalah,
   - file changed,
   - hasil test,
   - risiko residual,
   - next step (maks 3 poin).

## Checklist verifikasi sebelum finalisasi

1. Jalankan `python scripts/run_test_suite.py`.
2. Pastikan tidak ada file handoff/transien baru di `docs/` root (taruh di `docs/archive/handoffs/<tanggal>/`).
3. Pastikan semua perubahan kecil, jelas, dan traceable per file.
