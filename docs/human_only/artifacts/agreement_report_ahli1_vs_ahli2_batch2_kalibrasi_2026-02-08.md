# Agreement Report Ahli-1 vs Ahli-2 (Batch-2 Kalibrasi, 12 Kasus)

Tanggal: 8 Februari 2026  
Sumber:
1. Ahli-1: `docs/human_only/artifacts/paket_kerja_4_jam_batch2_terisi_dr_hendra_2026-02-08.md`, `docs/human_only/artifacts/paket_kerja_4_jam_batch3_terisi_dr_hendra_2026-02-08.md`, `docs/human_only/artifacts/paket_kerja_4_jam_batch4_terisi_dr_hendra_2026-02-08.md`, `docs/human_only/artifacts/paket_kerja_4_jam_batch5_terisi_dr_hendra_2026-02-08.md`, `docs/human_only/artifacts/paket_kerja_4_jam_batch6_terisi_dr_hendra_2026-02-08.md`
2. Ahli-2 Batch-1: `docs/human_only/artifacts/paket_kerja_4_jam_ahli2_batch1_terisi_dr_indra_2026-02-08.md`
3. Ahli-2 Batch-2 Kalibrasi: `docs/human_only/artifacts/paket_kerja_4_jam_ahli2_batch2_kalibrasi_terisi_dr_indra_2026-02-08.md`

## Ringkasan Hasil

1. Total kasus dibandingkan: 12
2. Agreement awal (Batch-1): 4/12 (33.3%)
3. Agreement setelah kalibrasi (Batch-2): 6/12 (50.0%)
4. Delta agreement: +16.7 poin persentase (+2 kasus match)
5. Status: meningkat, namun belum stabil untuk langsung scale-up tanpa guardrail

## Tabel Perbandingan Batch-2 Kalibrasi

| No | ID Kasus | Ahli-1 | Ahli-2 Batch-2 | Match |
|---|---|---|---|---|
| 1 | CS-MIN-011 | B | A | Tidak |
| 2 | CS-MIN-004 | A | B | Tidak |
| 3 | CS-JAW-006 | A | C | Tidak |
| 4 | CS-LIN-018 | C | C | Ya |
| 5 | CS-JAW-025 | C | C | Ya |
| 6 | CS-LIN-039 | C | C | Ya |
| 7 | CS-LIN-052 | D | C | Tidak |
| 8 | CS-NAS-066 | A | C | Tidak |
| 9 | CS-BAL-012 | C | C | Ya |
| 10 | CS-BAL-002 | B | C | Tidak |
| 11 | CS-MIN-019 | C | C | Ya |
| 12 | CS-BAL-023 | C | C | Ya |

## Analisis Singkat

1. Terjadi konvergensi pada kasus lintas-domain dan konflik norma yang memang menuntut sintesis (`C`).
2. Gap masih tersisa pada batas antara `A`/`B` versus `C`, terutama saat Ahli-2 menilai kasus sebagai "solusi sintesis" meskipun Ahli-1 memberi label kecenderungan tunggal.
3. Ada 1 kasus keyakinan rendah (`R`) di Ahli-2 (`CS-LIN-052`) sehingga ketidakstabilan interpretasi masih terlihat.

## Rekomendasi Operasional

1. Jalankan **Ahli-2 Batch-3 (kalibrasi lanjutan terarah)** sebelum scale-up penuh.
2. Fokus Batch-3 pada 6 kasus mismatch yang tersisa + 6 kasus anchor baru dengan kriteria batas `A/B` vs `C`.
3. Setelah Batch-3, hitung ulang agreement; jika >= 0.67 pada set kalibrasi, lanjut onboarding Ahli-3 dengan paket definisi label yang sama.
