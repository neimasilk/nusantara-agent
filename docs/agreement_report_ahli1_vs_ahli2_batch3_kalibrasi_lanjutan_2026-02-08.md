# Agreement Report Ahli-1 vs Ahli-2 (Batch-3 Kalibrasi Lanjutan, 12 Kasus)

Tanggal: 8 Februari 2026  
Sumber:
1. Ahli-1: `docs/paket_kerja_4_jam_batch2_terisi_dr_hendra_2026-02-08.md`, `docs/paket_kerja_4_jam_batch3_terisi_dr_hendra_2026-02-08.md`, `docs/paket_kerja_4_jam_batch4_terisi_dr_hendra_2026-02-08.md`, `docs/paket_kerja_4_jam_batch5_terisi_dr_hendra_2026-02-08.md`, `docs/paket_kerja_4_jam_batch6_terisi_dr_hendra_2026-02-08.md`
2. Ahli-2 Batch-2: `docs/paket_kerja_4_jam_ahli2_batch2_kalibrasi_terisi_dr_indra_2026-02-08.md`
3. Ahli-2 Batch-3: `docs/paket_kerja_4_jam_ahli2_batch3_kalibrasi_lanjutan_terisi_dr_indra_2026-02-08.md`

## Ringkasan Hasil

1. Total kasus dibandingkan: 12
2. Agreement Batch-1: 4/12 (33.3%)
3. Agreement Batch-2 kalibrasi: 6/12 (50.0%)
4. Agreement Batch-3 kalibrasi lanjutan: 7/12 (58.3%)
5. Delta Batch-2 ke Batch-3: +8.3 poin persentase (+1 kasus match)
6. Status: tren membaik, namun masih di bawah ambang kesiapan onboarding Ahli-3 (>= 0.67)

## Tabel Perbandingan Batch-3 Kalibrasi Lanjutan

| No | ID Kasus | Ahli-1 | Ahli-2 Batch-3 | Match |
|---|---|---|---|---|
| 1 | CS-MIN-011 | B | A | Tidak |
| 2 | CS-MIN-004 | A | B | Tidak |
| 3 | CS-JAW-006 | A | C | Tidak |
| 4 | CS-LIN-052 | D | D | Ya |
| 5 | CS-NAS-066 | A | C | Tidak |
| 6 | CS-BAL-002 | B | C | Tidak |
| 7 | CS-NAS-010 | A | A | Ya |
| 8 | CS-LIN-017 | A | A | Ya |
| 9 | CS-MIN-013 | B | B | Ya |
| 10 | CS-BAL-014 | B | B | Ya |
| 11 | CS-JAW-015 | C | C | Ya |
| 12 | CS-LIN-016 | C | C | Ya |

## Analisis Singkat

1. Kasus anchor menunjukkan konsistensi baik pada kategori tegas `A`, `B`, dan `C`.
2. Mismatch tersisa terkonsentrasi pada batas konseptual antara label tunggal (`A/B`) dan label sintesis (`C`).
3. Perbaikan pada `CS-LIN-052` (dari `C` ke `D`) menunjukkan kalibrasi definisi `D` mulai terinternalisasi.

## Rekomendasi Operasional

1. Lakukan **Ahli-2 Batch-4 kalibrasi mikro** (maks 8 kasus) dengan fokus eksklusif pada 5 mismatch tersisa.
2. Gunakan rubric keputusan eksplisit per kasus: cek dominansi norma, cek kebutuhan dual-komponen wajib, lalu tetapkan label.
3. Tunda onboarding Ahli-3 sampai agreement kalibrasi mencapai >= 0.67 pada batch validasi berikutnya.
