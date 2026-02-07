# Context Reset Handoff — Exp 06 Automation State (2026-02-07)

Dokumen ini merangkum state operasional terakhir sebelum reset konteks, agar agent berikutnya bisa melanjutkan tanpa kehilangan jejak.

## 1) Ringkasan Status Saat Ini

- Fokus aktif: **Exp 06 Independent Evaluation Pipeline**.
- Precheck terbaru (`python experiments/06_independent_eval/run_precheck.py`):
  - Gold texts: `200 / 200`
  - Annotation files: `1000 / 1000`
  - MA decisions: `7 / 50`
  - Invalid annotations: `0`
  - Invalid MA decisions: `7`
- Implikasi:
  - `ART-028`: READY secara operasional (kuantitas + struktur)
  - `ART-030`: NOT_READY (kuantitas putusan + field primer belum lengkap)
  - `ART-031`: tetap BLOCKED oleh `ART-030`

## 2) Artefak Baru Utama

### Experiment scaffolding
- `experiments/06_independent_eval/PROTOCOL.md`
- `experiments/06_independent_eval/REVIEW.md`
- `experiments/06_independent_eval/analysis.md`

### Automation scripts (Exp 06)
- `experiments/06_independent_eval/run_precheck.py`
- `experiments/06_independent_eval/bootstrap_seed_data.py`
- `experiments/06_independent_eval/build_gold_texts_internal_pool.py`
- `experiments/06_independent_eval/generate_full_assignment.py`
- `experiments/06_independent_eval/generate_annotation_stubs.py`
- `experiments/06_independent_eval/generate_ma_stubs.py`
- `experiments/06_independent_eval/auto_fill_annotations_llm.py`
- `experiments/06_independent_eval/auto_fill_ma_stubs_llm.py`
- `experiments/06_independent_eval/fill_annotations_by_replication.py`

### Data artifacts
- `data/raw/gold_standard_texts/GS-0001..GS-0200`
- `data/raw/gold_standard_texts/index_seed.csv`
- `data/raw/gold_standard_texts/index_internal_pool.csv`
- `data/processed/gold_standard/pilot_assignment_20_items.csv`
- `data/processed/gold_standard/full_assignment_200x5.csv`
- `data/processed/gold_standard/annotations/GS-*.json` (1000 files)
- `data/raw/ma_decisions/candidates_from_internal_outputs.csv`
- `data/raw/ma_decisions/putusan_*.json` (7 files draft)

## 3) Command yang Sudah Terbukti Jalan

### Core checks
- `python experiments/06_independent_eval/run_precheck.py`

### Build & assignment
- `python experiments/06_independent_eval/build_gold_texts_internal_pool.py`
- `python experiments/06_independent_eval/generate_full_assignment.py`
- `python experiments/06_independent_eval/generate_annotation_stubs.py --assignment data/processed/gold_standard/full_assignment_200x5.csv`

### Draft generation (API)
- `python experiments/06_independent_eval/auto_fill_annotations_llm.py --provider kimi --filter-ann ann03 --refresh-from-marker --max-files 200 --max-triples 6`
- `python experiments/06_independent_eval/auto_fill_annotations_llm.py --provider kimi --filter-ann ann04 --refresh-from-marker --max-files 200 --max-triples 6`
- `python experiments/06_independent_eval/auto_fill_annotations_llm.py --provider kimi --filter-ann ann05 --refresh-from-marker --max-files 200 --max-triples 6`
- `python experiments/06_independent_eval/auto_fill_ma_stubs_llm.py --provider kimi --max-files 7`

### Fallback fill
- `python experiments/06_independent_eval/fill_annotations_by_replication.py`

## 4) Quality Caveat Penting (Wajib Dibaca)

- Data anotasi 1000 file **bukan gold final**; mayoritas merupakan auto-fill draft.
- Ada fallback replikasi untuk menutup file kosong, ditandai marker pada `notes` (`AUTO_DOMAIN_FALLBACK_*`, `AUTO_REPLICA_*`).
- Putusan MA saat ini masih draft dari konteks internal, belum tervalidasi sumber primer.
- Jangan gunakan artefak ini untuk klaim final paper tanpa validasi manusia/primer.

## 5) Dependency & Blocker Aktual

- `ART-028`: operasional ready, tetapi validitas ilmiah masih perlu verifikasi manusia.
- `ART-030`: blocker utama:
  - Kuantitas baru `7/50`
  - Field primer putusan banyak kosong (`tanggal_putusan`, `tingkat_peradilan`, `ratio_decidendi`, `amar_putusan`)
- `ART-031` tetap blocked sampai `ART-030` memenuhi syarat.

## 6) Rekomendasi Lanjutan untuk Agent Berikutnya

1. Fokus dulu ART-030:
- Isi 7 putusan draft dari sumber primer MA.
- Tambah hingga minimal 50 putusan.
- Pastikan field primer non-kosong sesuai validasi `run_precheck.py`.

2. Kurangi risiko homogenisasi anotasi:
- Jalankan sampling audit manual pada subset `GS-*`.
- Hitung agreement nyata antar annotator (bukan hanya struktur valid).

3. Setelah ART-030 siap:
- Unblock `ART-031` dan jalankan pipeline evaluasi independen dengan laporan statistik lengkap.

## 7) Dokumen yang Sudah Disinkronkan

- `docs/readiness_audit_exp06_exp09_exp10_2026-02-07.md`
- `docs/task_registry.md`
- `docs/failure_registry.md` (ditambah F-010)

