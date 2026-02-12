# PAKET KEPUTUSAN AHLI FINAL - 6 KASUS MISMATCH

Tanggal: 2026-02-09
Tujuan: Finalisasi label hukum substantif untuk 6 kasus mismatch pasca-ingest Ahli-4.

## Petunjuk Isi
- Pilih 1 `label_final` untuk setiap kasus: `A/B/C/D`.
- Isi `keyakinan`: `Tinggi/Sedang/Rendah`.
- Isi `alasan_singkat` maksimal 3 kalimat.
- Isi `referensi` 1-2 dasar hukum/norma.
- Jika data belum cukup, isi `butuh_klarifikasi=Y` dan tulis fakta yang kurang.

## Legend Label
- `A`: Cenderung hukum nasional
- `B`: Cenderung hukum adat
- `C`: Sintesis nasional + adat
- `D`: Perlu klarifikasi

## Ringkasan Kasus
| id | gold_saat_ini | pola_suara_ahli | catatan |
| --- | --- | --- | --- |
| CS-MIN-011 | C | B, C, A, B | Mayoritas condong B (2-1-1) |
| CS-MIN-004 | B | A, C, C, C | Mayoritas C (3-1) |
| CS-LIN-052 | D | D, C, D, C | Seri 2-2 (C vs D) |
| CS-LIN-017 | A | A, C, C, A | Seri 2-2 (A vs C) |
| CS-BAL-014 | B | B, C, B, C | Seri 2-2 (B vs C) |
| CS-LIN-016 | C | C, A, C, A | Seri 2-2 (A vs C) |

## Form Keputusan (Isi)
| id | label_final (A/B/C/D) | keyakinan (Tinggi/Sedang/Rendah) | alasan_singkat (maks 3 kalimat) | referensi_1 | referensi_2 | butuh_klarifikasi (Y/T) | fakta_yang_kurang (jika Y) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CS-MIN-011 |  |  |  |  |  |  |  |
| CS-MIN-004 |  |  |  |  |  |  |  |
| CS-LIN-052 |  |  |  |  |  |  |  |
| CS-LIN-017 |  |  |  |  |  |  |  |
| CS-BAL-014 |  |  |  |  |  |  |  |
| CS-LIN-016 |  |  |  |  |  |  |  |

## Validasi Internal (Opsional)
- Pastikan semua kasus memiliki `label_final`.
- Pastikan alasan konsisten dengan referensi.
- Jika memilih `D`, jelaskan fakta apa yang wajib dilengkapi agar bisa diputus A/B/C.

## Output Final
Gunakan file ini sebagai sumber kebenaran keputusan ahli final untuk patch dataset.
