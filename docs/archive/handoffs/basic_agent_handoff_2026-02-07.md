# Basic Agent Handoff (Cost-Efficient Mode)
**Tanggal:** 2026-02-07  
**Tujuan:** Menjalankan pekerjaan lanjutan dengan agent kapabilitas biasa (murah) tanpa merusak kualitas riset.

---

## 1) Status Singkat Proyek

1. Proyek **layak dilanjutkan**, tetapi **belum siap submit Q1**.
2. Blokir utama Q1 masih sama:
   - `ART-028` (human annotation) belum selesai.
   - `ART-030` (putusan MA primer) belum selesai.
   - `ART-031` tetap `BLOCKED`.
   - Ablation fair (`Exp 09`) dan validasi CCS (`Exp 10`) belum jalan penuh.
3. Engineering hygiene sudah naik:
   - parser debat dibuat lebih robust,
   - evaluator independen provider handling diperbaiki,
   - test suite deterministik offline sudah tersedia.

---

## 2) Source of Truth (Wajib Diprioritaskan)

Urutan baca:
1. `CLAUDE.md`
2. `docs/task_registry.md`
3. `docs/methodology_fixes.md`
4. `docs/failure_registry.md`
5. `docs/testing_framework.md`

Catatan:
- Dokumen handoff bertanggal lama sudah dipindah ke `docs/archive/`.
- Untuk konflik status, **selalu menang** `docs/task_registry.md`.

---

## 3) Perubahan Engineering yang Sudah Dilakukan

1. `src/agents/debate.py`
   - parser fenced JSON lebih aman,
   - hapus return duplikat.
2. `src/evaluation/llm_judge.py`
   - provider split lebih benar (`openai/kimi` vs `anthropic` native SDK).
3. Test framework baru:
   - `scripts/run_test_suite.py`
   - `tests/` (19 test saat ini pass).
4. Governance docs:
   - `docs/testing_framework.md`
   - `docs/eagle_review_2026-02-07.md`
   - `docs/archive/README.md`

---

## 4) Tugas Aman untuk Basic Agent (Prioritas)

### P1 — Sinkronisasi dokumentasi task agar tidak kontradiktif
- Fokus: rapikan status/dependency yang ambigu di `docs/task_registry.md` (tanpa mengubah fakta).
- Output: status lebih konsisten + progress note eksplisit.

### P2 — Perkuat test coverage modul deterministik
- Tambah test untuk:
  - util parse JSON lain yang serupa,
  - edge-case `search` dan `router`.
- Wajib jalankan:
  ```bash
  python scripts/run_test_suite.py
  ```

### P3 — Rapikan drift dokumentasi operasional
- Pastikan root `docs/` hanya berisi dokumen aktif.
- Dokumen transien baru harus diarahkan ke `docs/archive/`.

---

## 5) Larangan untuk Basic Agent

1. Jangan klaim `ART-028/030/031` selesai tanpa evidence manusia/sumber primer.
2. Jangan ubah angka hasil eksperimen historis.
3. Jangan hapus audit trail historis (arsip/failure log).
4. Jangan melakukan refactor besar multi-file tanpa test pass.

---

## 6) Definition of Done (untuk tiap task basic agent)

1. Perubahan kecil, jelas, dan bisa ditelusuri.
2. `python scripts/run_test_suite.py` pass.
3. Tidak menambah kontradiksi status task.
4. Jika ada risiko metodologis baru, tambahkan catatan ke `docs/failure_registry.md`.
