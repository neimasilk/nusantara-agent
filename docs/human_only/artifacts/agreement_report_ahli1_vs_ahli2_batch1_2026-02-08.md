# Agreement Report Ahli-1 vs Ahli-2 (Batch Acuan 12 Kasus)

Tanggal: 8 Februari 2026  
Sumber:
1. Ahli-1: `docs/human_only/artifacts/paket_kerja_4_jam_batch2_terisi_dr_hendra_2026-02-08.md`, `docs/human_only/artifacts/paket_kerja_4_jam_batch3_terisi_dr_hendra_2026-02-08.md`, `docs/human_only/artifacts/paket_kerja_4_jam_batch4_terisi_dr_hendra_2026-02-08.md`, `docs/human_only/artifacts/paket_kerja_4_jam_batch5_terisi_dr_hendra_2026-02-08.md`, `docs/human_only/artifacts/paket_kerja_4_jam_batch6_terisi_dr_hendra_2026-02-08.md`
2. Ahli-2: `docs/human_only/artifacts/paket_kerja_4_jam_ahli2_batch1_terisi_dr_indra_2026-02-08.md`

## Ringkasan Hasil

1. Total kasus dibandingkan: 12
2. Agreement label literal (A/B/C/D sama persis): 4/12
3. Persentase agreement awal: 33.3%
4. Status: perlu kalibrasi definisi label dan batas domain

## Tabel Perbandingan

| No | ID Kasus | Ahli-1 | Ahli-2 | Match |
|---|---|---|---|---|
| 1 | CS-MIN-011 | B | A | Tidak |
| 2 | CS-BAL-012 | C | C | Ya |
| 3 | CS-BAL-002 | B | B | Ya |
| 4 | CS-MIN-004 | A | B | Tidak |
| 5 | CS-JAW-006 | A | B | Tidak |
| 6 | CS-LIN-018 | C | A | Tidak |
| 7 | CS-MIN-019 | C | C | Ya |
| 8 | CS-BAL-023 | C | C | Ya |
| 9 | CS-JAW-025 | C | B | Tidak |
| 10 | CS-LIN-039 | C | B | Tidak |
| 11 | CS-LIN-052 | D | A | Tidak |
| 12 | CS-NAS-066 | A | C | Tidak |

## Catatan Interpretasi

1. Ahli-2 menggunakan definisi kode yang sedikit berbeda (terutama untuk label `D`).
2. Kasus lintas domain cenderung memiliki gap terbesar (CS-LIN-018, CS-LIN-039, CS-LIN-052).
3. Beberapa kasus adat murni cukup konsisten (CS-BAL-002, CS-MIN-019, CS-BAL-023).

## Tindak Lanjut Disarankan

1. Jalankan batch kalibrasi untuk ahli-2 pada 8 kasus yang mismatch.
2. Kunci definisi label final sebelum ahli-2 batch berikutnya:
   1. A = cenderung nasional
   2. B = cenderung adat
   3. C = sintesis/konflik
   4. D = perlu klarifikasi
3. Setelah kalibrasi, hitung agreement ulang untuk melihat stabilisasi.

