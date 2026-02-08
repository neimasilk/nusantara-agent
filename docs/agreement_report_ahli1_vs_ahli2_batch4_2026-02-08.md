# Agreement Report Ahli-1 vs Ahli-2 (Batch-4 Kalibrasi Mikro, 8 Kasus)

Tanggal: 8 Februari 2026  
Sumber:
1. Ahli-1: `docs/rekap_human_baseline_sprint_2026-02-08.md` (Data kumulatif 72 kasus)
2. Ahli-2 Batch-4: `docs/paket_kerja_4_jam_ahli2_batch4_kalibrasi_mikro_terisi_dr_indra_2026-02-08.md`

## Ringkasan Hasil

1. Total kasus diuji: 8 (5 mismatch residual + 3 anchor kontrol)
2. Agreement pada 5 mismatch residual: 0/5 (0%)
3. Agreement pada 3 anchor kontrol: 3/3 (100%)
4. **Total Agreement Batch-4 (Literal Label): 3/8 (37.5%)**
5. Status Agreement Kumulatif (Set 12 kasus kalibrasi):
   - Batch-1: 4/12 (33.3%)
   - Batch-2: 6/12 (50.0%)
   - Batch-3: 7/12 (58.3%)
   - **Batch-4: 7/12 (58.3%)** -> Tidak ada perubahan pada total set 12 kasus karena 5 mismatch tetap tidak berubah.

## Tabel Perbandingan Batch-4 (Fokus Mismatch)

| No | ID Kasus | Ahli-1 | Ahli-2 Batch-4 | Match | Catatan |
|---|---|---|---|---|---|
| 1 | CS-MIN-011 | B | A | Tidak | Ahli-2 tetap pada argumen dominansi UUPA |
| 2 | CS-MIN-004 | A | B | Tidak | Ahli-2 tetap pada argumen dominansi status harta adat |
| 3 | CS-JAW-006 | A | C | Tidak | Ahli-2 menekankan perlunya sintesis eksekutorial |
| 4 | CS-NAS-066 | A | C | Tidak | Ahli-2 menekankan dual-komponen (UUD vs Sanksi Adat) |
| 5 | CS-BAL-002 | B | C | Tidak | Ahli-2 menekankan sintesis pasca Putusan MK 2010 |
| 6 | CS-LIN-052 | D | D | Ya | Anchor: Konsisten pada label D |
| 7 | CS-MIN-013 | B | B | Ya | Anchor: Konsisten pada label B |
| 8 | CS-NAS-010 | A | A | Ya | Anchor: Konsisten pada label A |

## Analisis Kegagalan Kalibrasi Mikro

1. **Inersia Profesional:** Ahli-2 (Dr. Indra) mempertahankan seluruh posisinya dari Batch-3 meskipun sudah diberikan rubric pengecekan ulang. Ini menunjukkan perbedaan bukan pada "kesalahan teknis", melainkan pada **paradigma interpretasi hukum**.
2. **Titik Tekan Sintesis (Label C):** Ahli-2 memiliki kecenderungan lebih tinggi (3/5 kasus mismatch) untuk melihat solusi sebagai sintesis (C), sementara Ahli-1 lebih cenderung membedah ke salah satu kutub (A atau B).
3. **Stagnasi Agreement:** Angka 58.3% pada set kalibrasi tampaknya merupakan *ceiling* (plafon) yang tidak bisa ditembus hanya dengan instruksi tertulis asinkron.

## Rekomendasi Gerbang (Gate Decision)

1. **BATALKAN onboarding Ahli-3 langsung:** Mengirim paket ke Ahli-3 saat dua ahli pertama masih memiliki sengketa fundamental pada 41.7% kasus akan menghasilkan data yang sangat bising.
2. **Lakukan Sinkronisasi Tatap Muka (Virtual/Sync):** Sesuai protokol di `collaboration_guide.md`, jika kalibrasi asinkron gagal 2x berturut-turut, diperlukan diskusi sinkron untuk menyamakan persepsi terhadap istilah "Dominansi Norma" vs "Kebutuhan Sintesis".
3. **Update ART-064:** Status tetap PENDING. Target agreement 0.67 belum tercapai.
