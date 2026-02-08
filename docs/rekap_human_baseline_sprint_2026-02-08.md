# Rekap Human Baseline Sprint - 2026-02-08

Dokumen ini merangkum progres sprint human-only untuk mendukung `ART-050` dan `ART-064`.

## Sumber Data Sprint

1. `docs/paket_kerja_4_jam_ahli_domain_terisi_dr_hendra_2026-02-08.md` (Batch 1)
2. `docs/paket_kerja_4_jam_batch2_terisi_dr_hendra_2026-02-08.md` (Batch 2)
3. `docs/paket_kerja_4_jam_batch3_terisi_dr_hendra_2026-02-08.md` (Batch 3)
4. `docs/paket_kerja_4_jam_batch4_terisi_dr_hendra_2026-02-08.md` (Batch 4)
5. `docs/paket_kerja_4_jam_batch5_terisi_dr_hendra_2026-02-08.md` (Batch 5)
6. `docs/paket_kerja_4_jam_batch6_terisi_dr_hendra_2026-02-08.md` (Batch 6)
7. `docs/paket_kerja_4_jam_ahli2_batch1_terisi_dr_indra_2026-02-08.md` (Ahli-2 Batch 1)
8. `docs/paket_kerja_4_jam_ahli2_batch2_kalibrasi_terisi_dr_indra_2026-02-08.md` (Ahli-2 Batch 2 Kalibrasi)
9. `docs/paket_kerja_4_jam_ahli2_batch3_kalibrasi_lanjutan_terisi_dr_indra_2026-02-08.md` (Ahli-2 Batch 3 Kalibrasi Lanjutan)
10. `docs/agreement_report_ahli1_vs_ahli2_batch1_2026-02-08.md` (Laporan agreement awal)
11. `docs/agreement_report_ahli1_vs_ahli2_batch2_kalibrasi_2026-02-08.md` (Laporan agreement pasca kalibrasi batch-2)
12. `docs/agreement_report_ahli1_vs_ahli2_batch3_kalibrasi_lanjutan_2026-02-08.md` (Laporan agreement pasca kalibrasi batch-3)

## Cakupan

1. Total kasus terisi batch 1: 12
2. Total kasus terisi batch 2: 12
3. Total kasus terisi batch 3: 12
4. Total kasus terisi batch 4: 12
5. Total kasus terisi batch 5: 12
6. Total kasus terisi batch 6: 12
7. Total kumulatif sprint ahli-1: 72 kasus
8. Agreement ahli-1 vs ahli-2 (12 kasus kalibrasi):
   - Batch-1: 4/12 (33.3%)
   - Batch-2 kalibrasi: 6/12 (50.0%)
   - Batch-3 kalibrasi lanjutan: 7/12 (58.3%)

## Distribusi Kesimpulan Ahli-2 (Batch-3 Kalibrasi Lanjutan)

1. A (cenderung nasional): 3
2. B (cenderung adat): 3
3. C (sintesis): 5
4. D (klarifikasi): 1

## Dampak ke Task

### ART-050 (200 test case)
1. Sprint human-only terus menambah judgment terstruktur.
2. Masih perlu perluasan hingga target 200 kasus lintas domain.

### ART-064 (human expert baseline)
1. Tren agreement antarahli membaik bertahap (33.3% -> 50.0% -> 58.3%).
2. Acceptance `ART-064` belum tercapai karena:
   - Belum 3 ahli independen.
   - Belum mencakup 200 kasus penuh.
   - Agreement antarahli belum mencapai tingkat memadai.

## Aksi Lanjut Disarankan

1. Jalankan Ahli-2 batch-4 kalibrasi mikro fokus 5 mismatch tersisa (`CS-MIN-011`, `CS-MIN-004`, `CS-JAW-006`, `CS-NAS-066`, `CS-BAL-002`).
2. Gunakan rubric keputusan eksplisit per kasus untuk mengunci batas label `A/B` vs `C`.
3. Onboarding Ahli-3 dilakukan setelah agreement kalibrasi mencapai >= 0.67 pada batch validasi berikutnya.
