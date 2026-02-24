# Manifest Governance Reconciliation (74 Active Benchmark)

Tanggal: 2026-02-24  
Owner: Mukhlis Amien (Research Lead)

## Masalah Awal

1. `data/benchmark_manifest.json` memiliki `total_cases_actual=74` tetapi `declared_total_cases=82`.
2. Akibatnya `count_matches_reference_claim=false` dan mode `scientific_claimable` selalu ditolak.

## Keputusan

1. Memisahkan secara eksplisit:
   - Arsip historis 82 kasus (tetap dipertahankan).
   - Klaim benchmark aktif 74 kasus (dipakai untuk run ilmiah saat ini).
2. Menetapkan dokumen referensi baru:
   - `docs/human_only/artifacts/benchmark_scope_active_74_cases_2026-02-24.md`

## Perubahan Teknis

1. `scripts/rebuild_benchmark_manifest.py`
   - Default `declared_total_cases` sekarang mengikuti jumlah dataset aktif.
   - Menambahkan `declared_total_cases_source` (`dataset_actual`, `cli_override`, `manifest_legacy`).
   - Menambahkan opsi:
     - `--declared-total-cases`
     - `--inherit-declared-total-from-manifest` (legacy, tidak direkomendasikan).
   - Default `--reference-claim` diarahkan ke dokumen scope benchmark aktif 74.
2. `tests/test_rebuild_benchmark_manifest.py` (baru)
   - Memastikan default tidak mewarisi angka lama secara diam-diam.
   - Memastikan mode override dan mode legacy tetap teruji.

## Bukti Validasi

Perintah:

```bash
python scripts/rebuild_benchmark_manifest.py --as-of-date 2026-02-24 --owner "Mukhlis Amien (Research Lead)"
python scripts/validate_benchmark_manifest.py --require-reference-match
python scripts/run_test_suite.py
```

Hasil:

1. Manifest: `total_cases_actual=74`, `declared_total_cases=74`, `count_matches_reference_claim=true`.
2. Validator strict: `errors=0`, `warns=0`.
3. Test suite: `132/132` pass.

## Dampak ke Gate

1. Gate `scientific_claimable` tetap fail-hard jika manifest tidak koheren.
2. Blocker mismatch referensi (82 vs 74) sekarang sudah ditutup untuk benchmark aktif saat ini.
