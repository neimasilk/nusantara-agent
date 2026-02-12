# Reset Konteks Human-Only — 82 Kasus vs Active Set 24

Tanggal: 2026-02-12  
Tujuan: mengunci konteks agar owner dapat fokus ke jalur HUMAN_ONLY tanpa terseret drift artefak AI.

## Putusan Ringkas

1. **82 kasus HUMAN_ONLY dinyatakan legit sebagai evidence kerja manusia** (proses, triangulasi, dan dokumen lapangan).
2. **24 kasus active set** adalah dataset operasional benchmark AI saat ini (bukan pembatalan kerja 82).
3. Sampai ada promosi dataset yang rapi, klaim harus dipisah:
   - klaim HUMAN_ONLY: basis 82
   - klaim benchmark AI otomatis: basis active set 24 (evaluable 22)

## Bukti Utama

1. Klaim 82 kasus:
   - `docs/gold_standard_consensus_report_complete_82_cases_2026-02-08.md`
   - `docs/agreement_report_ahli1_vs_ahli2_batch7_2026-02-08.md` (82 unik, 24 dual-judgment)
   - `docs/paket_kerja_4_jam_ahli3_batch2_terisi_2026-02-08.md` (skalasi kasus 25..82)
2. Jalur benchmark aktif 24:
   - `data/benchmark_manifest.json` (`total_cases_actual=24`, `evaluable_cases_excluding_split=22`)
   - runner menunjuk `data/processed/gold_standard/gs_active_cases.json`
3. Sumber kebingungan:
   - `data/processed/` di-ignore (`.gitignore`), sehingga perubahan dataset lokal tidak punya jejak commit yang kuat.

## Aturan Kerja Mulai Sekarang

1. Jangan campur angka 82 dan 24 dalam satu kalimat klaim.
2. Setiap laporan wajib menyebut:
   - `as_of_date`
   - sumber dataset (`82 human evidence pool` atau `active set 24`)
3. Jika fokus sesi adalah HUMAN_ONLY, hasil AI cukup dicatat sebagai konteks sekunder, bukan headline.

## Artefak Human-Only yang Dibuat pada Sesi Ini

1. `docs/human_only_register_82_master_v0_2026-02-12.csv`
2. Sumber pembentukan register:
   - `docs/paket_kerja_4_jam_ahli3_batch1_terisi_2026-02-08.md` (kasus 1-24)
   - `docs/paket_kerja_4_jam_ahli3_batch2_terisi_2026-02-08.md` (kasus 25-82)
3. Isi awal register:
   - `status_konsensus` dan `butuh_arbiter` masih `TBD` untuk diisi pada review manusia berikutnya.

## Jalur Lanjut yang Disarankan (Fokus HUMAN_ONLY)

## H1 — Lock Konteks Human
1. Jadikan dokumen ini sebagai pengantar wajib sebelum kerja batch baru.
2. Bekukan interpretasi: 82 = legitimate human evidence pool.

## H2 — Rapikan Register 82 (Non-koding, audit-friendly)
1. Buat satu tabel master 82 ID kasus dengan kolom:
   - `id_kasus`
   - `status_judgment` (single/dual/triangulated)
   - `status_konsensus` (unanimous/majority/split)
   - `butuh_arbiter` (ya/tidak)
   - `sumber_dokumen`
2. Tujuan: semua pihak membaca daftar yang sama, bukan narasi terpisah.

## H3 — Selesaikan Pending Split Human
1. Tutup seluruh kasus split yang masih belum final secara administratif.
2. Simpan alasan final + referensi hukum untuk setiap keputusan split.

## H4 — Lanjutkan Target 200 (tetap HUMAN_ONLY)
1. Lanjutkan batch kasus 83-200 dengan format paket kerja yang sama.
2. Prioritas kualitas: konsistensi antar ahli dan jejak referensi, bukan kecepatan.

## Yang Ditunda Sementara

1. Klaim performa AI paper-grade.
2. Perdebatan teknis baseline/statistik di luar kebutuhan langsung HUMAN_ONLY.

## Prompt Siap Pakai Untuk Agen Selanjutnya

"Fokuskan sesi ini ke jalur HUMAN_ONLY. Gunakan `docs/handoffs/20260212_human_only_context_reset.md` sebagai sumber konteks utama. Jangan campur klaim 82 human evidence pool dengan metrik active set 24. Kerjakan hanya artefak yang memperkuat register 82, resolusi split, dan ekspansi menuju 200 kasus."
